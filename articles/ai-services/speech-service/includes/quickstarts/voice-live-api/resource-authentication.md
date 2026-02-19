---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
reviewer: patrickfarley
ms.reviewer: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 10/31/2025
ms.subservice: azure-ai-foundry-openai
---

Create a new file named `.env` in the folder where you want to run the code. 

In the `.env` file, add the following environment variables for authentication:

```plaintext
AZURE_VOICELIVE_ENDPOINT=<your_endpoint>
AZURE_VOICELIVE_MODEL=<your_model>
AZURE_VOICELIVE_API_VERSION=2025-10-01
AZURE_VOICELIVE_API_KEY=<your_api_key> # Only required if using API key authentication
```

Replace the default values with your actual endpoint, model, API version, and API key.

#### [Microsoft Entra ID](#tab/keyless)

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_VOICELIVE_ENDPOINT` | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. |
| `AZURE_VOICELIVE_MODEL` | The model you want to use. For example, `gpt-4o` or `gpt-realtime-mini`. For more information about models availability, see the [Voice Live API overview documentation](../../../voice-live.md). |
| `AZURE_VOICELIVE_API_VERSION`| The API version you want to use. For example, `2025-10-01`. |

Learn more about [keyless authentication](/azure/ai-services/authentication) and [setting environment variables](/azure/ai-services/cognitive-services-environment-variables).

#### [API key](#tab/api-key)

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_VOICELIVE_ENDPOINT` | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. |
| `AZURE_VOICELIVE_MODEL` | The model you want to use. For example, `gpt-4o` or `gpt-realtime-mini`. For more information about models availability, see the [Voice Live API overview documentation](../../../voice-live.md). |
| `AZURE_VOICELIVE_API_VERSION`| The API version you want to use. For example, `2025-10-01`. |
| `AZURE_VOICELIVE_API_KEY` | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|

Learn more about finding API keys and setting environment variables in the [Environment variables guide](/azure/ai-services/cognitive-services-environment-variables).

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

---

