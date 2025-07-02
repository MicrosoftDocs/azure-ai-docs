---
title: 'Environment variables'
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: set up environment variables for your key and endpoint
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 08/28/2023
---


### Environment variables

Create and assign persistent environment variables for your key and endpoint.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/microsoft-entra-id-akv-expanded.md)]

# [Command Line](#tab/command-line)

```cmd
setx AZURE_OPENAI_API_KEY "REPLACE_WITH_YOUR_KEY_VALUE_HERE" 
setx AZURE_OPENAI_ENDPOINT "REPLACE_WITH_YOUR_ENDPOINT_HERE" 
```

# [PowerShell](#tab/powershell)

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_API_KEY', 'REPLACE_WITH_YOUR_KEY_VALUE_HERE', 'User')
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_ENDPOINT', 'REPLACE_WITH_YOUR_ENDPOINT_HERE', 'User')
```

# [Bash](#tab/bash)

```bash
export AZURE_OPENAI_API_KEY="REPLACE_WITH_YOUR_KEY_VALUE_HERE"
export AZURE_OPENAI_ENDPOINT="REPLACE_WITH_YOUR_ENDPOINT_HERE"
```

---
