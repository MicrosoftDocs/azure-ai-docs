---
name: sdk-code-retrieval
description: Retrieve actual code samples from Azure SDK repositories to prevent hallucinations. Use this skill when generating code examples for Azure AI Foundry documentation to ensure code accuracy and authenticity.
---

# SDK Code Retrieval Skill

This skill helps retrieve authentic code samples from Azure SDK repositories to prevent AI hallucinations in documentation.

## When to Use

- Before generating any code samples in documentation
- When verifying SDK method signatures and parameters
- When finding authentication patterns and error handling examples
- When ensuring multi-language code parity (Python, .NET, JavaScript, Java, Go)

## Repository Reference

### Azure AI SDK Packages

| Language | Repository | Packages |
|----------|------------|----------|
| Python | `Azure/azure-sdk-for-python` | azure-ai-projects, azure-ai-inference, azure-ai-evaluation, azure-ai-agents, azure-search-documents, azure-openai |
| .NET | `Azure/azure-sdk-for-net` | Azure.AI.Projects, Azure.AI.Inference, Azure.AI.Agents.Persistent, Azure.Search.Documents, Azure.AI.OpenAI |
| JavaScript | `Azure/azure-sdk-for-js` | @azure/ai-projects, @azure/ai-inference-rest, @azure/ai-agents, @azure/search-documents, @azure/openai |
| Java | `Azure/azure-sdk-for-java` | com.azure.ai.projects, com.azure.ai.inference, com.azure.ai.agents.persistent, com.azure.search.documents, com.azure.ai.openai |
| Go | `Azure/azure-sdk-for-go` | azopenai |

### OpenAI SDKs (for OpenAI-specific features)

| Language | Repository |
|----------|------------|
| Python | `openai/openai-python` |
| Go | `openai/openai-go` |

## Search Workflow

### Step 1: Identify the Operation

Determine what SDK operation you need to document:
- Client initialization
- Method calls
- Authentication patterns
- Error handling

### Step 2: Search SDK Repositories

Use GitHub search to find code:

```
# Example search queries
repo:Azure/azure-sdk-for-python path:sdk/ai/azure-ai-projects/ AIProjectsClient
repo:Azure/azure-sdk-for-net path:sdk/ai/Azure.AI.Projects/ AIProjectsClient
repo:Azure/azure-sdk-for-js path:sdk/ai/ai-projects/ AIProjectsClient
```

### Step 3: Extract Code Samples

Look for code in these locations:
1. `samples/` directories - Official sample code
2. `tests/` directories - Test cases with working code
3. `README.md` files - Quick start examples
4. Source code docstrings - Usage examples

### Step 4: Verify and Adapt

Before using code:
1. Verify the package version is current
2. Check for deprecated APIs
3. Ensure authentication patterns are secure
4. Add comments for clarity

## Code Quality Requirements

All retrieved code must:

- **Be complete**: Include imports, setup, and cleanup
- **Be secure**: Use environment variables for credentials
- **Include error handling**: Show try/except patterns
- **Be idiomatic**: Follow language conventions

## Example Output

When retrieving Python SDK code, format as:

```python
# Source: Azure/azure-sdk-for-python/sdk/ai/azure-ai-projects/samples/
# Package: azure-ai-projects
# Version: 1.0.0

from azure.ai.projects import AIProjectsClient
from azure.identity import DefaultAzureCredential
import os

# Initialize client with environment-based endpoint
client = AIProjectsClient(
    endpoint=os.environ["AZURE_AI_PROJECTS_ENDPOINT"],
    credential=DefaultAzureCredential()
)

try:
    # Your operation here
    result = client.some_operation()
    print(f"Success: {result}")
except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
```

## Fallback Strategy

If SDK samples are not found:

1. **Synthesize from signatures**: Create minimal example from method signature
2. **Mark as synthetic**: Clearly indicate the code is not from official samples
3. **Request verification**: Note that code should be verified against SDK docs

```python
# NOTE: This example is synthesized from SDK signatures.
# Verify with official SDK documentation before use.
```
