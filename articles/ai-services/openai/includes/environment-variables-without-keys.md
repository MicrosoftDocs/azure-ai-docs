---
title: 'Environment variables'
titleSuffix: Azure OpenAI Service
description: set up environment variables for your key and endpoint
#services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 10/08/2024
---


### Environment variables without keys

Create and assign persistent environment variables for your key and endpoint.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

# [Command Line](#tab/command-line)

```cmd
setx AZURE_OPENAI_RESOURCE "REPLACE_WITH_YOUR_RESOURCE_NAME_HERE" 
setx AZURE_OPENAI_ENDPOINT "REPLACE_WITH_YOUR_ENDPOINT_HERE" 
```

# [PowerShell](#tab/powershell)

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_RESOURCE', 'REPLACE_WITH_YOUR_RESOURCE_NAME_HERE', 'User')
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_ENDPOINT', 'REPLACE_WITH_YOUR_ENDPOINT_HERE', 'User')
```

# [Bash](#tab/bash)

```bash
export AZURE_OPENAI_RESOURCE="REPLACE_WITH_YOUR_RESOURCE_NAME_HERE"
export AZURE_OPENAI_ENDPOINT="REPLACE_WITH_YOUR_ENDPOINT_HERE"
```

---
