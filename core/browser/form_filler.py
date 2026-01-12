"""Form filler to populate detected fields."""

from typing import Dict, Any, Optional
from playwright.async_api import Page
from loguru import logger

from core.browser.page_analyzer import FormField


class FormFiller:
    """Fills form fields with provided data."""
    
    async def fill_field(
        self,
        page: Page,
        field: FormField,
        value: Any,
        force: bool = False
    ) -> bool:
        """Fill a single form field with a value."""
        if not value:
            return False
        
        try:
            selector = field.selector
            
            if field.element_type == 'input':
                return await self._fill_input(page, selector, field.field_type, value, force)
            
            elif field.element_type == 'textarea':
                return await self._fill_textarea(page, selector, value, force)
            
            elif field.element_type == 'select':
                return await self._fill_select(page, selector, value)
            
            else:
                logger.warning(f"Unknown field type: {field.element_type}")
                return False
        
        except Exception as e:
            logger.error(f"Error filling field {field.selector}: {e}")
            return False
    
    async def _fill_input(
        self,
        page: Page,
        selector: str,
        field_type: str,
        value: str,
        force: bool
    ) -> bool:
        """Fill an input field."""
        try:
            # Wait for element to be visible
            await page.wait_for_selector(selector, timeout=5000, state='visible')
            
            # Clear existing value if force
            if force:
                await page.fill(selector, '')
            
            # Type the value (more human-like)
            await page.type(selector, str(value), delay=50)
            
            logger.debug(f"Filled input {selector} with value: {value}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to fill input {selector}: {e}")
            return False
    
    async def _fill_textarea(
        self,
        page: Page,
        selector: str,
        value: str,
        force: bool
    ) -> bool:
        """Fill a textarea field."""
        try:
            await page.wait_for_selector(selector, timeout=5000, state='visible')
            
            if force:
                await page.fill(selector, '')
            
            await page.fill(selector, str(value))
            
            logger.debug(f"Filled textarea {selector}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to fill textarea {selector}: {e}")
            return False
    
    async def _fill_select(
        self,
        page: Page,
        selector: str,
        value: str
    ) -> bool:
        """Fill a select dropdown."""
        try:
            await page.wait_for_selector(selector, timeout=5000, state='visible')
            
            # Try to select by value, then by label
            try:
                await page.select_option(selector, value=value)
            except:
                await page.select_option(selector, label=value)
            
            logger.debug(f"Selected option {value} in {selector}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to fill select {selector}: {e}")
            return False
    
    async def fill_form(
        self,
        page: Page,
        field_mappings: Dict[FormField, Any],
        force: bool = False
    ) -> Dict[str, bool]:
        """Fill multiple form fields.
        
        Args:
            page: The Playwright page
            field_mappings: Dictionary mapping FormField objects to values
            force: Whether to force-fill even if field already has a value
        
        Returns:
            Dictionary mapping field selectors to success status
        """
        results = {}
        
        for field, value in field_mappings.items():
            success = await self.fill_field(page, field, value, force)
            results[field.selector] = success
        
        success_count = sum(1 for v in results.values() if v)
        logger.info(f"Filled {success_count}/{len(results)} fields successfully")
        
        return results


# Global form filler instance
form_filler = FormFiller()
