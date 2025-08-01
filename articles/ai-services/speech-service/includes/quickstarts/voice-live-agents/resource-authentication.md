---
author: eric-urban 
ms.author: eur 
ms.service: azure-ai-speech
ms.topic: include
ms.date: 7/31/2025
---

Create a new file named `.env` in the folder where you want to run the code. 

In the `.env` file, add the following environment variables for authentication:

```plaintext
AZURE_VOICE_LIVE_ENDPOINT=<your_endpoint>
AI_FOUNDRY_PROJECT_NAME=<your_project_name>
AI_FOUNDRY_AGENT_ID=<your_agent_id>
AZURE_VOICE_LIVE_API_VERSION=2025-05-01-preview
AZURE_VOICE_LIVE_API_KEY=<your_api_key> # Only required if using API key authentication
```

Replace the default values with your actual project name, agent ID, API version, and API key.

#### [Microsoft Entra ID](#tab/keyless)

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_VOICE_LIVE_ENDPOINT` | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. |
| `AI_FOUNDRY_PROJECT_NAME` | The name of your Azure AI Foundry project. |
| `AI_FOUNDRY_AGENT_ID` | The ID of your Azure AI Foundry agent. |
| `AZURE_VOICE_LIVE_API_VERSION`| The API version you want to use. For example, `2025-05-01-preview`. |

Learn more about [keyless authentication](/azure/ai-services/authentication) and [setting environment variables](/azure/ai-services/cognitive-services-environment-variables).

#### [API key](#tab/api-key)

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_VOICE_LIVE_ENDPOINT` | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. |
| `AI_FOUNDRY_PROJECT_NAME` | The name of your Azure AI Foundry project. |
| `AI_FOUNDRY_AGENT_ID` | The ID of your Azure AI Foundry agent. |
| `AZURE_VOICE_LIVE_API_VERSION`| The API version you want to use. For example, `2025-05-01-preview`. |
| `AZURE_VOICE_LIVE_API_KEY` | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|

Learn more about [finding API keys](/azure/ai-services/cognitive-services-environment-variables) and [setting environment variables](/azure/ai-services/cognitive-services-environment-variables).

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

---
