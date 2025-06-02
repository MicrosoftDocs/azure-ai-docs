---
titleSuffix: Azure OpenAI
manager: nitinme
ms.service: azure-ai-openai
ms.custom:
  - ignite-2024
ms.topic: include
author: aahill
ms.author: aahi
ms.date: 11/06/2024
recommendations: false
---

## Add your data using Azure AI Foundry portal

> [!TIP]
> You can [use the Azure Developer CLI](../how-to/azure-developer-cli.md) to programmatically create the resources needed for Azure OpenAI On Your Data 

Navigate to [Azure AI Foundry portal](https://ai.azure.com/) and sign-in with credentials that have access to your Azure OpenAI resource. 

1. You can either [create an Azure AI Foundry project](../../../ai-foundry/how-to/create-projects.md) by clicking **Create project**, or continue directly by clicking the button on the **Focused on Azure OpenAI in Azure AI Foundry Models** tile.  

    :::image type="content" source="../media/use-your-data/ai-foundry-homepage.png" alt-text="A screenshot of the Azure AI Foundry portal landing page." lightbox="../media/use-your-data/ai-foundry-homepage.png":::

1. Select **Chat** under **Playgrounds** in the left pane, and select your model deployment.

1. In the **Chat playground**, Select **Add your data** and then **Add a data source**

    :::image type="content" source="../media/use-your-data/chat-playground.png" alt-text="A screenshot of the chat playground in  Azure AI Foundry." lightbox="../media/use-your-data/chat-playground.png":::

1. In the pane that appears, select **Upload files (preview)** under **Select data source**. Azure OpenAI needs both a storage resource and a search resource to access and index your data. 

    > [!TIP]
    > * See the following resource for more information:
    >    * [Data source options](../concepts/use-your-data.md#supported-data-sources)
    >    * [supported file types and formats](../concepts/use-your-data.md#data-formats-and-file-types)
    > *  For documents and datasets with long text, we recommend using the available [data preparation script](https://go.microsoft.com/fwlink/?linkid=2244395). 

    1. For Azure OpenAI to access your storage account, you will need to turn on [Cross-origin resource sharing (CORS)](https://go.microsoft.com/fwlink/?linkid=2237228). If CORS isn't already turned on for the Azure Blob Storage resource, select **Turn on CORS**. 

    1. Select your Azure AI Search resource, and select the acknowledgment that connecting it will incur usage on your account. Then select **Next**.

    :::image type="content" source="../media/quickstarts/add-your-data-source.png" alt-text="A screenshot showing options for selecting a data source in Azure AI Foundry portal." lightbox="../media/quickstarts/add-your-data-source.png":::


1. On the **Upload files** pane, select **Browse for a file** and select the files you downloaded from the [prerequisites](#prerequisites) section, or your own data. Then select **Upload files**. Then select **Next**.

1. On the **Data management** pane, you can choose whether to enable [semantic search or vector search](../concepts/use-your-data.md#search-types) for your index.
    
    > [!IMPORTANT]
    > * [Semantic search](/azure/search/semantic-search-overview#availability-and-pricing) and [vector search](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) are subject to additional pricing. You need to choose **Basic or higher SKU** to enable semantic search or vector search. See [pricing tier difference](/azure/search/search-sku-tier) and [service limits](/azure/search/search-limits-quotas-capacity) for more information.
    > * To help improve the quality of the information retrieval and model response, we recommend enabling [semantic search](/azure/search/semantic-search-overview) for the following data source languages: English, French, Spanish, Portuguese, Italian, Germany, Chinese(Zh), Japanese, Korean, Russian, and Arabic.
    
1. Review the details you entered, and select **Save and close**. You can now chat with the model and it will use information from your data to construct the response.


