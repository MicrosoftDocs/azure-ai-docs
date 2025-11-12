---
titleSuffix: Azure OpenAI
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom:
  - ignite-2024
ms.topic: include
author: aahill
ms.author: aahi
ms.date: 09/12/2025
recommendations: false
---

## Add your data using Microsoft Foundry portal

> [!TIP]
> Alternatively, you can [use the Azure Developer CLI](../how-to/azure-developer-cli.md) to programmatically create the resources needed for Azure OpenAI On Your Data.

To add your data using the portal:

1. [!INCLUDE [classic-sign-in](../../includes/classic-sign-in.md)]
1. Select your Azure OpenAI resource. If you have a Foundry resource, you can [create a Foundry project](../../../ai-foundry/how-to/create-projects.md).

1. From the left pane, select **Playgrounds** > **Chat**.

1. In the **Setup** pane, select your model deployment.

1. Select **Add your data** > **Add a data source**.

    :::image type="content" source="../media/use-your-data/chat-playground.png" alt-text="A screenshot of the chat playground in  Foundry." lightbox="../media/use-your-data/chat-playground.png":::

1. On the **Data source** page:

    1. Under **Select data source**, select **Upload files (preview)**.

        > [!TIP]
        > + This option requires an Azure Blob Storage resource and Azure AI Search resource to access and index your data. For more information, see [Data source options](../concepts/use-your-data.md#supported-data-sources) and [Supported file types and formats](../concepts/use-your-data.md#data-formats-and-file-types).
        > + For documents and datasets with long text, we recommend that you use the [data preparation script](https://go.microsoft.com/fwlink/?linkid=2244395). 

    1. [Cross-origin resource sharing](https://go.microsoft.com/fwlink/?linkid=2237228) (CORS) is required for Azure OpenAI to access your storage account. If CORS isn't already enabled for your Azure Blob Storage resource, select **Turn on CORS**. 

    1. Select your Azure AI Search resource.
    
    1. Enter a name for your new index.

    1. Select the checkbox that acknowledges the billing effects of using Azure AI Search.
    
    1. Select **Next**.

    :::image type="content" source="../media/quickstarts/add-your-data-source.png" alt-text="A screenshot showing options for selecting a data source in Foundry portal." lightbox="../media/quickstarts/add-your-data-source.png":::

1. On the **Upload files** page:

    1. Select **Browse for a file**, and then select your own data or the sample data you downloaded from the [prerequisites](#prerequisites).
    
    1. Select **Upload files**.
    
    1. Select **Next**.

1. On the **Data management** page:

    1. Choose whether to enable [semantic search or vector search](../concepts/use-your-data.md#search-types) for your index.
    
        > [!IMPORTANT]
        > * [Semantic search](/azure/search/semantic-search-overview#availability-and-pricing) and [vector search](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) are subject to additional pricing. Your Azure AI Search resource must be on the Basic tier or higher to enable semantic search or vector search. For more information, see [Choose a tier](/azure/search/search-sku-tier) and [Service limits](/azure/search/search-limits-quotas-capacity).
        > * To help improve the quality of the information retrieval and model response, we recommend that you enable [semantic search](/azure/search/semantic-search-overview) for the following data source languages: English, French, Spanish, Portuguese, Italian, Germany, Chinese(Zh), Japanese, Korean, Russian, and Arabic.
    
    1. Select **Next**.

1. On the **Data connection** page:

    1. Choose whether to authenticate using a **System assigned managed identity** or an **API key**.

    1. Select **Next**.

1. Review your configurations, and then select **Save and close**.

    You can now chat with the model, which uses your data to construct the response.
