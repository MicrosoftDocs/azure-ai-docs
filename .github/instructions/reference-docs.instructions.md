---
applyTo: "**/reference/**/*.md,**/api/**/*.md"
---

# Reference Documentation Guidelines

Apply these conventions when creating or editing reference documentation.

## Reference Definition

Reference documentation is **information-oriented** content that provides complete technical details. Think of it as an ingredient list.

## Required Structure

### 1. Title
Format: "[API/Class/Command] reference" or "[Feature] specifications"

Examples:
- "AIProjectsClient class reference"
- "Chat completions API reference"
- "az ai deployment command reference"

### 2. Overview
- Brief description (1-2 sentences)
- Link to conceptual documentation
- Version/availability information

### 3. Syntax/Signature
Show the complete signature:

```python
class AIProjectsClient:
    def __init__(
        self,
        endpoint: str,
        credential: TokenCredential,
        **kwargs: Any
    ) -> None:
```

### 4. Parameters Table
Document ALL parameters:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| endpoint | str | Yes | - | The Azure AI Foundry endpoint URL |
| credential | TokenCredential | Yes | - | Azure credential for authentication |

### 5. Return Value
- Type
- Structure/schema
- Example response

### 6. Errors/Exceptions
Document ALL possible errors:

| Error | Code | Description | Resolution |
|-------|------|-------------|------------|
| HttpResponseError | 401 | Invalid credentials | Check authentication |
| ResourceNotFoundError | 404 | Resource doesn't exist | Verify resource name |

### 7. Examples
Short, focused examples:
- Minimal working example
- Common use case
- Edge case handling

### 8. See Also
- Related APIs
- How-to guides that use this API
- Conceptual documentation

## Writing Rules

- **Be complete** - Document everything, even obvious parameters
- **Be consistent** - Use the same format for all parameters
- **Be neutral** - No marketing language, just facts
- **Be scannable** - Use tables, not paragraphs

## Do Not Include

- Step-by-step instructions (→ how-to)
- Learning exercises (→ tutorial)
- Design decisions/rationale (→ explanation)
- "Why" content (→ explanation)
