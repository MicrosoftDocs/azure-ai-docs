---
#services: cognitive-services
manager: nitinme
author: travisw
ms.author: travisw
ms.service: azure-ai-openai
ms.topic: include
ms.date: 08/29/2023
---

## Retrieve required variables

To successfully make a call against Azure OpenAI, you need the following variables. This quickstart assumes you've uploaded your data to an Azure blob storage account and have an Azure AI Search index created. See [Add your data using Azure AI Foundry](../use-your-data-quickstart.md?pivots=programming-language-studio)

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_OPENAI_ENDPOINT`               | This value can be found in the **Keys & Endpoint** section when examining your Azure OpenAI resource from the Azure portal. Alternatively, you can find the value in **Azure AI Foundry** > **Chat playground** > **Code view**. An example endpoint is: `https://my-resoruce.openai.azure.com`.|
| `AZURE_OPENAI_API_KEY` | This value can be found in **Resource management** > **Keys & Endpoint** section when examining your Azure OpenAI resource from the Azure portal. You can use either `KEY1` or `KEY2`. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption. |
| `AZURE_OPENAI_DEPLOYMENT_ID` | This value corresponds to the custom name you chose for your deployment when you deployed a model. This value can be found under **Resource Management** > **Deployments** in the Azure portal or alternatively under **Management** > **Deployments** in Azure AI Foundry portal.|
| `AZURE_AI_SEARCH_ENDPOINT` | This value can be found in the **Overview** section when examining your Azure AI Search resource from the Azure portal. |
| `AZURE_AI_SEARCH_API_KEY` | This value can be found in the **Settings** > **Keys** section when examining your Azure AI Search resource from the Azure portal. You can use either the primary admin key or secondary admin key. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption. |
| `AZURE_AI_SEARCH_INDEX` | This value corresponds to the name of the index you created to store your data. You can find it in the **Overview** section when examining your Azure AI Search resource from the Azure portal. |

### Environment variables

Create and assign persistent environment variables for your key and endpoint.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

# [Command Line](#tab/command-line)

```CMD
setx AZURE_OPENAI_ENDPOINT REPLACE_WITH_YOUR_AOAI_ENDPOINT_VALUE_HERE
```
```CMD
setx AZURE_OPENAI_API_KEY REPLACE_WITH_YOUR_AOAI_KEY_VALUE_HERE
```
```CMD
setx AZURE_OPENAI_DEPLOYMENT_ID REPLACE_WITH_YOUR_AOAI_DEPLOYMENT_VALUE_HERE
```
```CMD
setx AZURE_AI_SEARCH_ENDPOINT REPLACE_WITH_YOUR_AZURE_SEARCH_RESOURCE_VALUE_HERE
```
```CMD
setx AZURE_AI_SEARCH_API_KEY REPLACE_WITH_YOUR_AZURE_SEARCH_RESOURCE_KEY_VALUE_HERE
```
```CMD
setx AZURE_AI_SEARCH_INDEX REPLACE_WITH_YOUR_INDEX_NAME_HERE
```


# [PowerShell](#tab/powershell)

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_ENDPOINT', 'REPLACE_WITH_YOUR_AOAI_ENDPOINT_VALUE_HERE', 'User')
```

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_API_KEY', 'REPLACE_WITH_YOUR_AOAI_KEY_VALUE_HERE', 'User')
```

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_DEPLOYMENT_ID', 'REPLACE_WITH_YOUR_AOAI_DEPLOYMENT_VALUE_HERE', 'User')
```

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_AI_SEARCH_ENDPOINT', 'REPLACE_WITH_YOUR_AZURE_SEARCH_RESOURCE_VALUE_HERE', 'User')
```

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_AI_SEARCH_API_KEY', 'REPLACE_WITH_YOUR_AZURE_SEARCH_RESOURCE_KEY_VALUE_HERE', 'User')
```

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_AI_SEARCH_INDEX', 'REPLACE_WITH_YOUR_INDEX_NAME_HERE', 'User')
```

# [Bash](#tab/bash)

```Bash
export AZURE_OPENAI_ENDPOINT=REPLACE_WITH_YOUR_AOAI_ENDPOINT_VALUE_HERE
```
```Bash
export AZURE_OPENAI_API_KEY=REPLACE_WITH_YOUR_AOAI_KEY_VALUE_HERE
```
```Bash
export AZURE_OPENAI_DEPLOYMENT_ID=REPLACE_WITH_YOUR_AOAI_DEPLOYMENT_VALUE_HERE
```
```Bash
export AZURE_AI_SEARCH_ENDPOINT=REPLACE_WITH_YOUR_AZURE_SEARCH_RESOURCE_VALUE_HERE
```
```Bash
export AZURE_AI_SEARCH_API_KEY=REPLACE_WITH_YOUR_AZURE_SEARCH_RESOURCE_KEY_VALUE_HERE
```
```Bash
export AZURE_AI_SEARCH_INDEX=REPLACE_WITH_YOUR_INDEX_NAME_HERE
```

---

