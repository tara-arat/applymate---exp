"""Browser automation package for ApplyMate."""

from core.browser.playwright_manager import PlaywrightManager, browser_manager
from core.browser.page_analyzer import PageAnalyzer, FormField, page_analyzer
from core.browser.form_filler import FormFiller, form_filler

__all__ = [
    "PlaywrightManager",
    "browser_manager",
    "PageAnalyzer",
    "FormField",
    "page_analyzer",
    "FormFiller",
    "form_filler"
]
