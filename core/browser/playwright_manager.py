"""Playwright browser manager for ApplyMate."""

from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright
from loguru import logger

from config import settings


class PlaywrightManager:
    """Manages Playwright browser lifecycle."""
    
    def __init__(self):
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self._is_running = False
    
    async def start(self):
        """Start Playwright and launch browser."""
        if self._is_running:
            logger.warning("Playwright already running")
            return
        
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=settings.BROWSER_HEADLESS,
                args=['--disable-blink-features=AutomationControlled']  # Less detectable
            )
            
            # Create context with realistic viewport
            self.context = await self.browser.new_context(
                viewport={
                    'width': settings.BROWSER_VIEWPORT_WIDTH,
                    'height': settings.BROWSER_VIEWPORT_HEIGHT
                },
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            self._is_running = True
            logger.info("Playwright browser started successfully")
        
        except Exception as e:
            logger.error(f"Failed to start Playwright: {e}")
            raise
    
    async def new_page(self) -> Page:
        """Create a new page in the browser context."""
        if not self._is_running or not self.context:
            await self.start()
        
        page = await self.context.new_page()
        
        # Set default timeout
        page.set_default_timeout(settings.BROWSER_TIMEOUT)
        
        logger.info("Created new browser page")
        return page
    
    async def navigate_to(self, page: Page, url: str) -> bool:
        """Navigate to a URL and wait for page load."""
        try:
            logger.info(f"Navigating to: {url}")
            await page.goto(url, wait_until='domcontentloaded')
            
            # Wait a bit for dynamic content
            await page.wait_for_load_state('networkidle', timeout=10000)
            
            logger.info(f"Successfully loaded: {url}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            return False
    
    async def close_page(self, page: Page):
        """Close a specific page."""
        try:
            await page.close()
            logger.info("Page closed")
        except Exception as e:
            logger.error(f"Failed to close page: {e}")
    
    async def stop(self):
        """Stop browser and cleanup."""
        if not self._is_running:
            return
        
        try:
            if self.context:
                await self.context.close()
            
            if self.browser:
                await self.browser.close()
            
            if self.playwright:
                await self.playwright.stop()
            
            self._is_running = False
            logger.info("Playwright browser stopped")
        
        except Exception as e:
            logger.error(f"Error stopping Playwright: {e}")
    
    async def __aenter__(self):
        """Context manager entry."""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.stop()


# Global browser manager instance
browser_manager = PlaywrightManager()
