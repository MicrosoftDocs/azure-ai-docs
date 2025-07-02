---
services: cognitive-services
manager: nitinme
author: mrbullwinkle # external contributor: gm2552
ms.author: mbullwin
ms.service: azure-ai-openai
ms.topic: include
ms.date: 11/27/2023
---

## Retrieve required variables

To successfully make a call against Azure OpenAI, you need the following variables. This quickstart assumes you've uploaded your data to an Azure blob storage account and have an Azure AI Search index created. For more information, see [Add your data using Azure AI Foundry](../use-your-data-quickstart.md?pivots=programming-language-studio).

| Variable name      | Value                                                                                                                                                                                                                                                                                                                     |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `AZURE_OPENAI_ENDPOINT`     | You can find this value in the **Keys & Endpoint** section when examining your Azure OpenAI resource from the Azure portal. Alternatively, you can find the value in **Azure AI Foundry** > **Chat playground** > **Code view**. An example endpoint is: `https://my-resource.openai.azure.com`.                           |
| `AZURE_OPENAI_API_KEY`          | You can find this value in **Resource management** > **Keys & Endpoint** section when examining your Azure OpenAI resource from the Azure portal. You can use either `KEY1` or `KEY2`. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.                     |
| `AZURE_OPEN_AI_DEPLOYMENT_ID` | This value corresponds to the custom name you chose for your deployment when you deployed a model. You can find this value under **Resource Management** > **Deployments** in the Azure portal or alternatively under **Management** > **Deployments** in Azure AI Foundry portal.                                                |
| `AZURE_AI_SEARCH_ENDPOINT`   | You can find this value in the **Overview** section when examining your Azure AI Search resource from the Azure portal.                                                                                                                                                                                            |
| `AZURE_AI_SEARCH_API_KEY`        | You can find this value in the **Settings** > **Keys** section when examining your Azure AI Search resource from the Azure portal. You can use either the primary admin key or secondary admin key. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption. |
| `AZURE_AI_SEARCH_INDEX`      | This value corresponds to the name of the index you created to store your data. You can find it in the **Overview** section when examining your Azure AI Search resource from the Azure portal.                                                                                                                    |

### Environment variables

Create and assign persistent environment variables for your key and endpoint.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

> [!NOTE]
> Spring AI defaults the model name to `gpt-35-turbo`. It's only necessary to provide the `SPRING_AI_AZURE_OPENAI_MODEL` value if you've deployed a model with a different name.

```bash
export SPRING_AI_AZURE_OPENAI_ENDPOINT=REPLACE_WITH_YOUR_AOAI_ENDPOINT_VALUE_HERE
export SPRING_AI_AZURE_OPENAI_API_KEY=REPLACE_WITH_YOUR_AOAI_KEY_VALUE_HERE
export SPRING_AI_AZURE_COGNITIVE_SEARCH_ENDPOINT=REPLACE_WITH_YOUR_AZURE_SEARCH_RESOURCE_VALUE_HERE
export SPRING_AI_AZURE_COGNITIVE_SEARCH_API_KEY=REPLACE_WITH_YOUR_AZURE_SEARCH_RESOURCE_KEY_VALUE_HERE
export SPRING_AI_AZURE_COGNITIVE_SEARCH_INDEX=REPLACE_WITH_YOUR_INDEX_NAME_HERE
export SPRING_AI_AZURE_OPENAI_MODEL=REPLACE_WITH_YOUR_MODEL_NAME_HERE
```
