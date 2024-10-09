---
manager: nitinme
author: mrbullwinkle
ms.author: mbullwin
ms.service: azure-ai-openai
ms.topic: include
ms.date: 10/0//2024
ms.custom: devex-track-js, devex-track-typescript
---
|Variable name | Value |
|--------------------------|-------------|
| `ENDPOINT`               | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. Alternatively, you can find the value in **Azure OpenAI Studio** > **Playground** > **View code**. An example endpoint is: `https://docs-test-001.openai.azure.com/`.|
| `DEPLOYMENT-NAME` | This value will correspond to the custom name you chose for your deployment when you deployed a model. This value can be found under **Resource Management** > **Model Deployments** in the Azure portal or alternatively under **Management** > **Deployments** in Azure OpenAI Studio.|
| `OPENAI_API_VERSION`|Learn more about [API Versions](/azure/ai-services/openai/concepts/model-versions).|

# [Command Line](#tab/command-line)

```cmd
setx AZURE_OPENAI_ENDPOINT "REPLACE_WITH_YOUR_ENDPOINT_HERE"
setx AZURE_OPENAI_DEPLOYMENT_NAME "REPLACE_WITH_YOUR_DEPLOYMENT_NAME" 
setx OPENAI_API_VERSION "REPLACE_WITH_YOUR_API_VERSION"  
```

# [PowerShell](#tab/powershell)

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_ENDPOINT', 'REPLACE_WITH_YOUR_ENDPOINT_HERE', 'User')
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_DEPLOYMENT_NAME', 'REPLACE_WITH_YOUR_DEPLOYMENT_NAME', 'User')
[System.Environment]::SetEnvironmentVariable('OPENAI_API_VERSION', 'REPLACE_WITH_YOUR_API_VERSION', 'User')
```

# [Bash](#tab/bash)

```bash
export AZURE_OPENAI_ENDPOINT="REPLACE_WITH_YOUR_ENDPOINT_HERE"
export AZURE_OPENAI_DEPLOYMENT_NAME="REPLACE_WITH_YOUR_DEPLOYMENT_NAME"
export OPENAI_API_VERSION="REPLACE_WITH_YOUR_API_VERSION"
```

