---
author: eric-urban 
ms.author: eur 
ms.service: azure-ai-openai
ms.topic: include
ms.date: 5/19/2025
---

You need to retrieve the following information to authenticate your application with your Azure AI Foundry resource:

#### [Microsoft Entra ID](#tab/keyless)

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_VOICE_LIVE_ENDPOINT` | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. |
| `VOICE_LIVE_MODEL` | The model you want to use. For example, `gpt-4o` or `gpt-4o-mini-realtime-preview`. For more information about models availability, see the [Voice Live API overview documentation](../../../voice-live.md). |
| `AZURE_VOICE_LIVE_API_VERSION`| The API version you want to use. For example, `2025-05-01-preview`. |

Learn more about [keyless authentication](/azure/ai-services/authentication) and [setting environment variables](/azure/ai-services/cognitive-services-environment-variables).

#### [API key](#tab/api-key)

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_VOICE_LIVE_ENDPOINT`               | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. |
| `AZURE_VOICE_LIVE_API_KEY` | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|

Learn more about [finding API keys](/azure/ai-services/cognitive-services-environment-variables) and [setting environment variables](/azure/ai-services/cognitive-services-environment-variables).

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

---



