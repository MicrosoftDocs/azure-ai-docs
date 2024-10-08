---
manager: nitinme
author: mrbullwinkle
ms.author: mbullwin
ms.service: azure-ai-openai
ms.topic: include
ms.date: 10/0//2024
ms.custom: devex-track-js, devex-track-typescript
---

[!INCLUDE [environment-variables](environment-variables.md)]

Add additional environment variables for the deployment name and API version: 
* `AZURE_OPENAI_DEPLOYMENT_NAME`: Your deployment name as shown in the Azure portal.
* `OPENAI_API_VERSION`: Learn more about [API Versions](/azure/ai-services/openai/concepts/model-versions).

# [Command Line](#tab/command-line)

```cmd
setx AZURE_OPENAI_DEPLOYMENT_NAME "REPLACE_WITH_YOUR_DEPLOYMENT_NAME" 
setx OPENAI_API_VERSION "REPLACE_WITH_YOUR_API_VERSION" 
```

# [PowerShell](#tab/powershell)

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_DEPLOYMENT_NAME', 'REPLACE_WITH_YOUR_DEPLOYMENT_NAME', 'User')
[System.Environment]::SetEnvironmentVariable('OPENAI_API_VERSION', 'REPLACE_WITH_YOUR_API_VERSION', 'User')
```

# [Bash](#tab/bash)

```bash
export AZURE_OPENAI_DEPLOYMENT_NAME="REPLACE_WITH_YOUR_DEPLOYMENT_NAME"
export OPENAI_API_VERSION="REPLACE_WITH_YOUR_API_VERSION"
```