
## GEMINI.md

# Gemini AI - Project Implementation Guide

## Document Purpose
This guide provides Gemini-specific implementation patterns and reasoning approaches for the LLM Proxy project. It focuses on practical implementation details, code patterns, and integration strategies.

## Gemini Implementation Philosophy

### Core Principles

1. **Practical First Approach**
   - Focus on working, maintainable code over theoretical perfection
   - Implement minimal viable solutions that solve immediate needs
   - Prioritize clarity and readability in all code

2. **Pattern Consistency**
   - Strictly follow established Factory Pattern implementation
   - Maintain identical interfaces across all providers
   - Use consistent error handling and validation approaches

3. **Incremental Improvement**
   - Start with basic implementation matching existing patterns
   - Add optimizations and features iteratively
   - Preserve working state at each step

## Implementation Templates

### New Provider Implementation

```python
"""
Template for new LLM provider implementation
Follow this structure exactly for consistency
"""

import os
from typing import Dict, Any
import httpx
from .base import LLMProvider


class NewProvider(LLMProvider):
    """ProviderName provider implementation for LLM Proxy."""
    
    def __init__(self, model: str):
        super().__init__(model)
        self.api_key = os.getenv("PROVIDER_API_KEY")
        if not self.api_key:
            raise ValueError("PROVIDER_API_KEY environment variable is required")
        
        # Provider-specific initialization
        self.base_url = "https://api.provider.com/v1"
        self.timeout = 30.0
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate response using ProviderName API.
        
        Args:
            prompt: User input text
            
        Returns:
            Generated response text
            
        Raises:
            Exception: Detailed error message for API failures
        """
        headers = self._build_headers()
        data = self._build_request_data(prompt)
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/chat",
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                return self._parse_response(response.json())
                
        except httpx.HTTPError as e:
            raise Exception(f"ProviderName API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error with ProviderName: {str(e)}")
    
    def _build_headers(self) -> Dict[str, str]:
        """Build provider-specific headers."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _build_request_data(self, prompt: str) -> Dict[str, Any]:
        """Build provider-specific request payload."""
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
    
    def _parse_response(self, response_data: Dict[str, Any]) -> str:
        """Parse and extract response text from provider response."""
        # Implementation varies by provider API structure
        return response_data["choices"][0]["message"]["content"]