---
title: 'Quickstart: Generate images with Azure OpenAI in Microsoft Foundry Models and Microsoft Foundry'
titleSuffix: Azure OpenAI
description: Learn how to generate images with Azure OpenAI in the DALL-E playground (Preview) in Microsoft Foundry.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom:
  - ignite-2023
ms.topic: include
ms.date: 12/05/2024
---

Use this guide to get started generating images with Azure OpenAI in your browser with Microsoft Foundry.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource created in a supported region. See [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).


## Go to Foundry

Browse to [Foundry](https://ai.azure.com/?cid=learnDocs) and sign in with the credentials associated with your Azure OpenAI resource. During or after the sign-in workflow, select the appropriate directory, Azure subscription, and Azure OpenAI resource.

From the Foundry landing page, create or select a new project. Navigate to the **Models + endpoints** page on the left nav. Select **Deploy model** and then choose one of the DALL-E models from the list. Complete the deployment process. 

On the model's page, select **Open in playground**.

## Try out image generation

Start exploring Azure OpenAI capabilities with a no-code approach through the **Images playground**. Enter your image prompt into the text box and select **Generate**. When the AI-generated image is ready, it appears on the page.

> [!NOTE]
> The Image APIs come with a content moderation filter. If Azure OpenAI recognizes your prompt as harmful content, it doesn't return a generated image. For more information, see [Content filtering](../concepts/content-filter.md).

In the **Images playground**, you can also view Python and cURL code samples, which are prefilled according to your settings. Select **View code** near the top of the page. You can use this code to write an application that completes the same task.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Explore the Image APIs in more depth with the [Image API how-to guide](../how-to/dall-e.md).
* Try examples in the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
* See the [API reference](../reference.md#image-generation)
