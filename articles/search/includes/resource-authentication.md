---
author: eric-urban 
ms.author: eur 
ms.service: azure-ai-search
ms.topic: include
ms.date: 2/12/2025
---

You need to retrieve the following information to authenticate your application with your Azure AI Search service:

#### [Microsoft Entra ID](#tab/keyless)

|Variable name | Value |
|--------------------------|-------------|
| `SEARCH_API_ENDPOINT` | This value can be found in the Azure portal. Select your search service and then from the left menu, select **Overview**. The **Url** value under **Essentials** is the endpoint that you need. An example endpoint might look like `https://mydemo.search.windows.net`. |

Learn more about [keyless authentication](/azure/search/keyless-connections) and [setting environment variables](/azure/ai-services/cognitive-services-environment-variables).

#### [API key](#tab/api-key)

|Variable name | Value |
|--------------------------|-------------|
| `SEARCH_API_ENDPOINT` | This value can be found in the Azure portal. Select your search service and then from the left menu, select **Overview**. The **Url** value under **Essentials** is the endpoint that you need. An example endpoint might look like `https://mydemo.search.windows.net`. |
| `SEARCH_API_KEY` | This value can be found in the Azure portal. Select your search service and then from the left menu, select **Settings** > **Keys**. You can use either `KEY1` or `KEY2`.|

Learn more about [finding API keys](/azure/search/search-security-api-keys) and [setting environment variables](/azure/ai-services/cognitive-services-environment-variables).

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

---



