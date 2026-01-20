---
applyTo: "**/samples/**/*.py,**/samples/**/*.cs,**/samples/**/*.js,**/samples/**/*.ts,**/samples/**/*.java,**/samples/**/*.go"
---

# Azure SDK Code Sample Guidelines

Apply these conventions when creating or editing code samples for Azure documentation.

## Required Elements

Every code sample must include:

1. **Package imports** - All required imports at the top
2. **Authentication** - Use DefaultAzureCredential or environment variables
3. **Error handling** - Try/catch with specific exception types
4. **Resource cleanup** - Close clients, dispose resources

## Authentication Pattern

### Python
```python
import os
from azure.identity import DefaultAzureCredential

endpoint = os.environ["AZURE_ENDPOINT"]
credential = DefaultAzureCredential()
```

### C#
```csharp
using Azure.Identity;

var endpoint = Environment.GetEnvironmentVariable("AZURE_ENDPOINT");
var credential = new DefaultAzureCredential();
```

### JavaScript/TypeScript
```javascript
import { DefaultAzureCredential } from "@azure/identity";

const endpoint = process.env.AZURE_ENDPOINT;
const credential = new DefaultAzureCredential();
```

## Never Hardcode

- API keys
- Connection strings
- Passwords
- Tokens
- Subscription IDs
- Resource names (use variables)

## Comments

- Add comments explaining "why" not "what"
- Document non-obvious behavior
- Include placeholder comments for user customization

```python
# Replace with your model deployment name
deployment_name = os.environ.get("DEPLOYMENT_NAME", "gpt-4")
```

## Error Handling

Always catch specific exceptions:

```python
from azure.core.exceptions import HttpResponseError, ServiceRequestError

try:
    result = client.operation()
except HttpResponseError as e:
    print(f"Azure service error: {e.message}")
except ServiceRequestError as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```
