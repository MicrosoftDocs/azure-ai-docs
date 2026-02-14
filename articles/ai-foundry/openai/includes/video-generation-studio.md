---
title: 'Quickstart: Generate videos with Sora in Microsoft Foundry Models and Microsoft Foundry'
titleSuffix: Azure OpenAI
description: Learn how to generate videos with Sora in the video playground (preview) in Microsoft Foundry.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 09/08/2025
---


## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource created in a supported region. See [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

## Go to Microsoft Foundry portal

Browse to the [Foundry portal](https://ai.azure.com/?cid=learnDocs) and sign in with the credentials associated with your Azure OpenAI resource. During or after the sign-in workflow, select the appropriate directory, Azure subscription, and Azure OpenAI resource.

From the Foundry landing page, create or select a new project. Navigate to the **Models + endpoints** page on the left nav. Select **Deploy model** and then choose the Sora video generation model from the list. Complete the deployment process.

On the model's page, select **Open in playground**.

## Try out video generation

Start exploring Sora video generation with a no-code approach through the **Video playground**. Enter your prompt into the text box and select **Generate**. Video generation typically takes **1 to 5 minutes** depending on your settings. When the AI-generated video is ready, it appears on the page.

> [!NOTE]
> The content generation APIs come with a content moderation filter. If Azure OpenAI recognizes your prompt as harmful content, it doesn't return a generated video. For more information, see [Content filtering](../concepts/content-filter.md).

In the **Video playground**, you can also view Python and cURL code samples, which are prefilled according to your settings. Select the code button at the top of your video playback pane. You can use this code to write an application that completes the same task.
