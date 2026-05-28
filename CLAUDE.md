# Claude AI - Project Guidelines & Conventions

## Document Purpose
This document provides Claude-specific guidelines for working with the LLM Proxy codebase. It complements the main AGENTS.md documentation with Claude-focused patterns, reasoning approaches, and implementation preferences.

## Claude-Specific Guidelines

### Code Analysis Patterns

1. **Architecture-First Approach**
   - Always start by understanding the Factory Pattern implementation
   - Review provider interfaces before making changes
   - Map data flow through all layers before implementation

2. **Provider Implementation Strategy**
   - Follow the established abstract base class contract
   - Maintain consistency with existing providers (OpenAI, Anthropic)
   - Use httpx with 30-second timeout pattern
   - Validate API keys in `__init__` methods

3. **Error Handling Philosophy**
   - Use descriptive error messages that help debugging
   - Preserve original exception context when wrapping
   - Follow existing HTTP status code mapping patterns

### Implementation Priorities

1. **Maintainability Over Cleverness**
   - Prefer clear, explicit code over complex one-liners
   - Use descriptive variable names that reveal intent
   - Follow existing naming conventions strictly

2. **Consistency with Existing Codebase**
   - Match code style and structure of existing providers
   - Use the same import patterns and organization
   - Follow established error handling approaches

3. **Documentation Standards**
   - Update relevant documentation when changing architecture
   - Include docstrings for all new classes and methods
   - Comment non-obvious logic or business decisions

### Common Implementation Patterns

#### Provider Template
```python
class NewProvider(LLMProvider):
    def __init__(self, model: str):
        super().__init__(model)
        self.api_key = os.getenv("PROVIDER_API_KEY")
        if not self.api_key:
            raise ValueError("PROVIDER_API_KEY environment variable required")
    
    def generate_response(self, prompt: str) -> str:
        # Implementation following existing patterns
        pass

try:
    # API call logic
except HTTPError as e:
    raise Exception(f"API request failed: {str(e)}")
except Exception as e:
    raise Exception(f"Unexpected error: {str(e)}")