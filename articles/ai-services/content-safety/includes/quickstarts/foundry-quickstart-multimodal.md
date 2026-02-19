---
title: "Quickstart: Analyze multimodal content with the AI Foundry portal"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 07/28/2025
ms.author: pafarley
---

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource</a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, [supported region](../../overview.md#region-availability), and supported pricing tier. Then select **Create**.

## Setup 

1. Go to the [Azure AI Foundry portal](https://ai.azure.com/), and sign in with your Azure account that has the Content Safety resource.
1. On the left nav, select **AI Services**. On the next page, select **Content Safety**.
1. Select the **Moderate multimodal content** pane.
1. Select your resource in the **Azure AI Services** dropdown menu.

## Analyze multimodal content

Choose one of the provided sample images, or upload your own. You also enter text that's to be associated with the image. 

When you select **Run test**, the service analyzes the graphic image content, any text that appears in the image, and the provided text that's associated with the image. If any content type triggers any of the harm category content filters, that information appears in the **Category and risk level detection results** pane.

