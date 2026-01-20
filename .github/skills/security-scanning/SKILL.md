---
name: security-scanning
description: Scan code samples for security vulnerabilities including hardcoded credentials, missing error handling, deprecated APIs, and insecure patterns. Use this skill before publishing any documentation with code.
---

# Security Scanning Skill

This skill scans code samples for common security vulnerabilities before documentation publication.

## When to Use

- Before publishing any documentation with code samples
- When reviewing code examples for security best practices
- After generating or retrieving code from SDK repositories
- When validating code in tutorials and how-to guides

## Security Checks

### 1. Hardcoded Credentials

**Check for**:
- API keys
- Passwords
- Connection strings
- Tokens
- Secrets

**Bad Patterns**:
```python
# VULNERABLE: Hardcoded API key
client = AIProjectsClient(api_key="sk-1234567890abcdef")

# VULNERABLE: Hardcoded connection string
conn_str = "Endpoint=https://myaccount.azure.com;Key=abc123"

# VULNERABLE: Hardcoded password
password = "MySecretPassword123!"
```

**Secure Patterns**:
```python
# SECURE: Environment variable
import os
api_key = os.environ.get("AZURE_API_KEY")

# SECURE: Azure Identity
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()

# SECURE: Key Vault reference
from azure.keyvault.secrets import SecretClient
secret = secret_client.get_secret("my-secret")
```

### 2. Missing Error Handling

**Check for**:
- Unhandled exceptions
- Missing try/except blocks
- Silent failures
- Unclosed resources

**Bad Pattern**:
```python
# VULNERABLE: No error handling
client = AIProjectsClient(endpoint, credential)
result = client.some_operation()  # May fail
print(result)
```

**Secure Pattern**:
```python
# SECURE: Proper error handling
from azure.core.exceptions import HttpResponseError

try:
    client = AIProjectsClient(endpoint, credential)
    result = client.some_operation()
    print(f"Success: {result}")
except HttpResponseError as e:
    print(f"Azure error: {e.message}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    client.close()
```

### 3. Deprecated APIs

**Check for**:
- Deprecated methods/classes
- Old SDK versions
- Legacy authentication
- Sunset APIs

**Deprecated Patterns to Flag**:
```python
# DEPRECATED: Old authentication
from azure.common.credentials import ServicePrincipalCredentials

# DEPRECATED: Legacy client
from azure.cognitiveservices.vision import ComputerVisionClient

# DEPRECATED: Old method name
client.old_method_name()  # Replaced by new_method_name()
```

**Current Patterns**:
```python
# CURRENT: Modern authentication
from azure.identity import DefaultAzureCredential

# CURRENT: Latest SDK client
from azure.ai.projects import AIProjectsClient
```

### 4. Insecure Patterns

**Check for**:
- HTTP instead of HTTPS
- Disabled SSL verification
- Weak cryptography
- Overly permissive permissions

**Insecure Patterns**:
```python
# INSECURE: HTTP endpoint
endpoint = "http://my-service.azure.com"

# INSECURE: Disabled SSL
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# INSECURE: Weak hash
import hashlib
hashlib.md5(data)  # Use SHA-256 instead
```

**Secure Patterns**:
```python
# SECURE: HTTPS endpoint
endpoint = "https://my-service.azure.com"

# SECURE: Strong cryptography
import hashlib
hashlib.sha256(data)
```

## Scanning Output Format

Report security issues using this structure:

```markdown
### Security Issue {number}

**Severity**: [CRITICAL | HIGH | MEDIUM | LOW]
**Category**: [Credentials | Error Handling | Deprecated | Insecure Pattern]
**Location**: Line {number} or code block in Section "{name}"

**Issue**: {Description of the vulnerability}

**Vulnerable Code**:
\`\`\`{language}
{problematic code}
\`\`\`

**Secure Alternative**:
\`\`\`{language}
{fixed code}
\`\`\`

**Risk**: {What could go wrong if not fixed}
```

## Severity Classifications

| Severity | Examples | Action |
|----------|----------|--------|
| CRITICAL | Hardcoded secrets, disabled SSL | Block publication |
| HIGH | Missing error handling, HTTP endpoints | Must fix |
| MEDIUM | Deprecated APIs, silent failures | Should fix |
| LOW | Could use more specific exception handling | Consider fixing |

## Security Checklist

After scanning, verify:

- [ ] No hardcoded API keys, passwords, or tokens
- [ ] No hardcoded connection strings
- [ ] All operations have error handling
- [ ] Resources are properly closed/disposed
- [ ] HTTPS used for all endpoints
- [ ] SSL/TLS verification not disabled
- [ ] No deprecated authentication methods
- [ ] No deprecated API calls
- [ ] Strong cryptography used
- [ ] Credentials loaded from environment or Key Vault

## Language-Specific Patterns

### Python

```python
# Secure credential pattern
import os
from azure.identity import DefaultAzureCredential

endpoint = os.environ["AZURE_ENDPOINT"]
credential = DefaultAzureCredential()
```

### C#

```csharp
// Secure credential pattern
using Azure.Identity;

var endpoint = Environment.GetEnvironmentVariable("AZURE_ENDPOINT");
var credential = new DefaultAzureCredential();
```

### JavaScript

```javascript
// Secure credential pattern
const { DefaultAzureCredential } = require("@azure/identity");

const endpoint = process.env.AZURE_ENDPOINT;
const credential = new DefaultAzureCredential();
```
