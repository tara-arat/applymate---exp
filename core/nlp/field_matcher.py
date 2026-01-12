"""Field matcher using NLP to map form fields to profile data."""

import re
from typing import Dict, List, Tuple, Optional, Any
from loguru import logger
import spacy
from spacy.matcher import PhraseMatcher

from core.browser.page_analyzer import FormField
from config import settings


class FieldMatcher:
    """Matches form fields to profile data using NLP."""
    
    # Predefined mappings for common field patterns
    FIELD_PATTERNS = {
        'first_name': [
            'first name', 'firstname', 'given name', 'fname', 'forename',
            'first', 'name first', 'first_name'
        ],
        'last_name': [
            'last name', 'lastname', 'surname', 'family name', 'lname',
            'last', 'name last', 'last_name'
        ],
        'email': [
            'email', 'e-mail', 'email address', 'e-mail address',
            'contact email', 'your email', 'mail'
        ],
        'phone': [
            'phone', 'telephone', 'phone number', 'tel', 'mobile',
            'cell', 'contact number', 'mobile number', 'cell phone'
        ],
        'address_line1': [
            'address', 'street address', 'address line 1', 'address 1',
            'street', 'address line1', 'street 1'
        ],
        'address_line2': [
            'address line 2', 'address 2', 'apartment', 'apt', 'suite',
            'unit', 'address line2', 'apt/suite'
        ],
        'city': [
            'city', 'town', 'municipality'
        ],
        'state': [
            'state', 'province', 'region', 'state/province'
        ],
        'zip_code': [
            'zip', 'zip code', 'postal code', 'postcode', 'postal',
            'zipcode', 'zip/postal'
        ],
        'country': [
            'country', 'nation'
        ],
        'linkedin_url': [
            'linkedin', 'linkedin url', 'linkedin profile', 'linkedin.com'
        ],
        'github_url': [
            'github', 'github url', 'github profile', 'github.com',
            'github username'
        ],
        'portfolio_url': [
            'portfolio', 'website', 'personal website', 'portfolio url',
            'personal site', 'web site'
        ],
        'current_company': [
            'current company', 'employer', 'company', 'current employer',
            'organization'
        ],
        'current_title': [
            'job title', 'title', 'current title', 'position',
            'current position', 'role', 'current role'
        ],
        'years_of_experience': [
            'years of experience', 'experience', 'years experience',
            'work experience', 'total experience'
        ],
        'education_level': [
            'education level', 'degree', 'highest degree', 'education',
            'level of education', 'qualification'
        ],
        'university': [
            'university', 'college', 'school', 'institution',
            'educational institution'
        ],
        'major': [
            'major', 'field of study', 'degree major', 'course',
            'specialization', 'subject'
        ],
        'graduation_year': [
            'graduation year', 'year of graduation', 'grad year',
            'graduated', 'completion year'
        ],
        'gpa': [
            'gpa', 'grade point average', 'cgpa', 'grades'
        ]
    }
    
    def __init__(self):
        self.nlp = None
        self.matcher = None
        self._initialized = False
    
    def initialize(self):
        """Initialize spaCy model and matcher."""
        if self._initialized:
            return
        
        try:
            logger.info(f"Loading spaCy model: {settings.SPACY_MODEL}")
            self.nlp = spacy.load(settings.SPACY_MODEL)
            self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
            
            # Add patterns to matcher
            for profile_field, patterns in self.FIELD_PATTERNS.items():
                patterns_doc = [self.nlp(pattern) for pattern in patterns]
                self.matcher.add(profile_field, patterns_doc)
            
            self._initialized = True
            logger.info("Field matcher initialized successfully")
        
        except Exception as e:
            logger.error(f"Failed to initialize field matcher: {e}")
            logger.warning("Field matching will use fallback method")
    
    def match_field(self, form_field: FormField) -> Tuple[Optional[str], float]:
        """Match a form field to a profile field.
        
        Returns:
            Tuple of (profile_field_name, confidence_score)
        """
        if not self._initialized:
            self.initialize()
        
        # Combine all available field information
        field_text = self._extract_field_text(form_field)
        
        if not field_text:
            return None, 0.0
        
        # Try NLP matching first
        if self.nlp:
            profile_field, score = self._nlp_match(field_text)
            if profile_field and score >= settings.MIN_FIELD_MATCH_SCORE:
                return profile_field, score
        
        # Fallback to pattern matching
        profile_field, score = self._pattern_match(field_text)
        return profile_field, score
    
    def match_fields(
        self,
        form_fields: List[FormField]
    ) -> Dict[FormField, Tuple[Optional[str], float]]:
        """Match multiple form fields to profile fields.
        
        Returns:
            Dictionary mapping FormField to (profile_field, confidence_score)
        """
        matches = {}
        
        for field in form_fields:
            profile_field, score = self.match_field(field)
            matches[field] = (profile_field, score)
        
        # Log matching results
        matched_count = sum(1 for pf, _ in matches.values() if pf is not None)
        logger.info(f"Matched {matched_count}/{len(form_fields)} fields")
        
        return matches
    
    def _extract_field_text(self, field: FormField) -> str:
        """Extract all text information from a form field."""
        texts = []
        
        if field.label:
            texts.append(field.label)
        if field.placeholder:
            texts.append(field.placeholder)
        if field.name:
            texts.append(field.name)
        if field.id:
            texts.append(field.id)
        
        # Combine and clean
        combined = ' '.join(texts).lower()
        # Remove special characters and normalize whitespace
        combined = re.sub(r'[^\w\s]', ' ', combined)
        combined = re.sub(r'\s+', ' ', combined).strip()
        
        return combined
    
    def _nlp_match(self, field_text: str) -> Tuple[Optional[str], float]:
        """Use spaCy to match field text."""
        if not self.nlp or not self.matcher:
            return None, 0.0
        
        try:
            doc = self.nlp(field_text)
            matches = self.matcher(doc)
            
            if matches:
                # Get the first match (highest priority)
                match_id, start, end = matches[0]
                profile_field = self.nlp.vocab.strings[match_id]
                
                # Calculate confidence based on match coverage
                match_length = end - start
                total_length = len(doc)
                confidence = min(match_length / total_length, 1.0) * 0.95
                
                logger.debug(f"NLP matched '{field_text}' -> '{profile_field}' ({confidence:.2f})")
                return profile_field, confidence
        
        except Exception as e:
            logger.debug(f"NLP matching error: {e}")
        
        return None, 0.0
    
    def _pattern_match(self, field_text: str) -> Tuple[Optional[str], float]:
        """Fallback pattern matching using simple string matching."""
        best_match = None
        best_score = 0.0
        
        for profile_field, patterns in self.FIELD_PATTERNS.items():
            for pattern in patterns:
                # Check if pattern is in field text
                if pattern in field_text:
                    # Score based on pattern coverage
                    score = len(pattern) / len(field_text)
                    score = min(score, 0.9)  # Cap at 0.9 for pattern matching
                    
                    if score > best_score:
                        best_score = score
                        best_match = profile_field
        
        if best_match:
            logger.debug(f"Pattern matched '{field_text}' -> '{best_match}' ({best_score:.2f})")
        
        return best_match, best_score
    
    def get_profile_value(self, profile: Dict[str, Any], field_name: str) -> Optional[Any]:
        """Get value from profile dictionary by field name."""
        return profile.get(field_name)


# Global field matcher instance
field_matcher = FieldMatcher()
