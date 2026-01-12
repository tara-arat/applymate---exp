"""Page analyzer to detect form fields."""

from typing import List, Dict, Any, Optional
from playwright.async_api import Page
from loguru import logger


class FormField:
    """Represents a detected form field."""
    
    def __init__(
        self,
        element_type: str,
        field_type: str,
        name: Optional[str] = None,
        id: Optional[str] = None,
        label: Optional[str] = None,
        placeholder: Optional[str] = None,
        required: bool = False,
        selector: Optional[str] = None,
        options: Optional[List[str]] = None
    ):
        self.element_type = element_type  # input, textarea, select
        self.field_type = field_type  # text, email, tel, etc.
        self.name = name
        self.id = id
        self.label = label
        self.placeholder = placeholder
        self.required = required
        self.selector = selector
        self.options = options or []  # For select/radio/checkbox
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'element_type': self.element_type,
            'field_type': self.field_type,
            'name': self.name,
            'id': self.id,
            'label': self.label,
            'placeholder': self.placeholder,
            'required': self.required,
            'selector': self.selector,
            'options': self.options
        }
    
    def __repr__(self):
        return f"<FormField(type={self.field_type}, label='{self.label}', name='{self.name}')>"


class PageAnalyzer:
    """Analyzes web pages to detect form fields."""
    
    async def detect_form_fields(self, page: Page) -> List[FormField]:
        """Detect all form fields on the current page."""
        fields = []
        
        try:
            # Detect input fields
            input_fields = await self._detect_input_fields(page)
            fields.extend(input_fields)
            
            # Detect textarea fields
            textarea_fields = await self._detect_textarea_fields(page)
            fields.extend(textarea_fields)
            
            # Detect select dropdowns
            select_fields = await self._detect_select_fields(page)
            fields.extend(select_fields)
            
            logger.info(f"Detected {len(fields)} form fields on page")
            
        except Exception as e:
            logger.error(f"Error detecting form fields: {e}")
        
        return fields
    
    async def _detect_input_fields(self, page: Page) -> List[FormField]:
        """Detect input fields."""
        fields = []
        
        # JavaScript to extract input field information
        js_code = """
        () => {
            const inputs = document.querySelectorAll('input:not([type="hidden"]):not([type="submit"]):not([type="button"])');
            return Array.from(inputs).map(input => {
                const label = this._findLabelForInput(input);
                return {
                    type: input.type || 'text',
                    name: input.name || '',
                    id: input.id || '',
                    placeholder: input.placeholder || '',
                    required: input.required || false,
                    label: label
                };
            });
        }
        
        this._findLabelForInput = function(input) {
            // Try to find associated label
            if (input.id) {
                const label = document.querySelector(`label[for="${input.id}"]`);
                if (label) return label.textContent.trim();
            }
            
            // Check parent label
            const parentLabel = input.closest('label');
            if (parentLabel) return parentLabel.textContent.replace(input.value, '').trim();
            
            // Check previous sibling
            const prevSibling = input.previousElementSibling;
            if (prevSibling && (prevSibling.tagName === 'LABEL' || prevSibling.tagName === 'SPAN')) {
                return prevSibling.textContent.trim();
            }
            
            // Check aria-label
            if (input.getAttribute('aria-label')) {
                return input.getAttribute('aria-label');
            }
            
            return '';
        }
        """
        
        try:
            # Simpler approach: get all visible inputs
            inputs = await page.query_selector_all('input:not([type="hidden"]):not([type="submit"]):not([type="button"])')
            
            for idx, input_elem in enumerate(inputs):
                try:
                    field_type = await input_elem.get_attribute('type') or 'text'
                    name = await input_elem.get_attribute('name') or ''
                    id_attr = await input_elem.get_attribute('id') or ''
                    placeholder = await input_elem.get_attribute('placeholder') or ''
                    required = await input_elem.get_attribute('required') is not None
                    
                    # Try to find label
                    label = await self._find_label_for_element(page, input_elem, id_attr)
                    
                    # Create selector
                    if id_attr:
                        selector = f'#{id_attr}'
                    elif name:
                        selector = f'input[name="{name}"]'
                    else:
                        selector = f'input:nth-of-type({idx + 1})'
                    
                    field = FormField(
                        element_type='input',
                        field_type=field_type,
                        name=name,
                        id=id_attr,
                        label=label,
                        placeholder=placeholder,
                        required=required,
                        selector=selector
                    )
                    fields.append(field)
                
                except Exception as e:
                    logger.warning(f"Error processing input field: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error detecting input fields: {e}")
        
        return fields
    
    async def _detect_textarea_fields(self, page: Page) -> List[FormField]:
        """Detect textarea fields."""
        fields = []
        
        try:
            textareas = await page.query_selector_all('textarea')
            
            for idx, textarea_elem in enumerate(textareas):
                try:
                    name = await textarea_elem.get_attribute('name') or ''
                    id_attr = await textarea_elem.get_attribute('id') or ''
                    placeholder = await textarea_elem.get_attribute('placeholder') or ''
                    required = await textarea_elem.get_attribute('required') is not None
                    
                    label = await self._find_label_for_element(page, textarea_elem, id_attr)
                    
                    if id_attr:
                        selector = f'#{id_attr}'
                    elif name:
                        selector = f'textarea[name="{name}"]'
                    else:
                        selector = f'textarea:nth-of-type({idx + 1})'
                    
                    field = FormField(
                        element_type='textarea',
                        field_type='textarea',
                        name=name,
                        id=id_attr,
                        label=label,
                        placeholder=placeholder,
                        required=required,
                        selector=selector
                    )
                    fields.append(field)
                
                except Exception as e:
                    logger.warning(f"Error processing textarea field: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error detecting textarea fields: {e}")
        
        return fields
    
    async def _detect_select_fields(self, page: Page) -> List[FormField]:
        """Detect select dropdown fields."""
        fields = []
        
        try:
            selects = await page.query_selector_all('select')
            
            for idx, select_elem in enumerate(selects):
                try:
                    name = await select_elem.get_attribute('name') or ''
                    id_attr = await select_elem.get_attribute('id') or ''
                    required = await select_elem.get_attribute('required') is not None
                    
                    label = await self._find_label_for_element(page, select_elem, id_attr)
                    
                    # Get options
                    options = []
                    option_elements = await select_elem.query_selector_all('option')
                    for opt in option_elements:
                        opt_text = await opt.text_content()
                        if opt_text and opt_text.strip():
                            options.append(opt_text.strip())
                    
                    if id_attr:
                        selector = f'#{id_attr}'
                    elif name:
                        selector = f'select[name="{name}"]'
                    else:
                        selector = f'select:nth-of-type({idx + 1})'
                    
                    field = FormField(
                        element_type='select',
                        field_type='select',
                        name=name,
                        id=id_attr,
                        label=label,
                        required=required,
                        selector=selector,
                        options=options
                    )
                    fields.append(field)
                
                except Exception as e:
                    logger.warning(f"Error processing select field: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error detecting select fields: {e}")
        
        return fields
    
    async def _find_label_for_element(self, page: Page, element, element_id: str) -> str:
        """Find label text for an element."""
        try:
            # Try label with 'for' attribute
            if element_id:
                label = await page.query_selector(f'label[for="{element_id}"]')
                if label:
                    text = await label.text_content()
                    if text:
                        return text.strip()
            
            # Try aria-label
            aria_label = await element.get_attribute('aria-label')
            if aria_label:
                return aria_label.strip()
            
            # Try parent label
            parent = await element.evaluate_handle('el => el.closest("label")')
            if parent:
                text = await parent.text_content()
                if text:
                    return text.strip()
        
        except Exception as e:
            logger.debug(f"Could not find label: {e}")
        
        return ""


# Global page analyzer instance
page_analyzer = PageAnalyzer()
