---
title: "Quickstart: Analyze image content"
description: In this quickstart, get started using Azure AI Content Safety to analyze image content for objectionable material.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom: 
ms.topic: include
ms.date: 04/10/2025
ms.author: pafarley
---

## Prerequisites

- An Azure account. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An [Azure AI resource](https://ms.portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/AIServices). 

## Setup

Follow these steps to use the Content Safety **try it out** page: 

1. Go to [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) and navigate to your project/hub. Then select the **Guardrails + controls** tab on the left nav and select the **Try it out** tab.
1. On the **Try it out** page, you can experiment with various Guardrails & controls features such as text and image content, using adjustable thresholds to filter for inappropriate or harmful content.

:::image type="content" source="/azure/ai-foundry/media/content-safety/try-it-out.png" alt-text="Screenshot of the try it out page for Guardrails & controls.":::

## Analyze images

The **Moderate image** page provides capability for you to quickly try out image moderation.

1. Select the **Moderate image content** panel. 
1. Select a sample image from the panels on the page, or upload your own image. 
1. Select **Run test**. 
    The service returns all the categories that were detected, with the severity level for each: 0-Safe, 2-Low, 4-Medium, 6-High. It also returns a binary **Accepted**/**Rejected** result, based on the filters you configure. Use the matrix in the **Configure filters** tab on the right to set your allowed/prohibited severity levels for each category. Then you can run the text again to see how the filter works.

## View and export code 

You can use the **View Code** feature in either the **Analyze text content** or **Analyze image content** pages to view and copy the sample code, which includes configuration for severity filtering, blocklists, and moderation functions. You can then deploy the code on your end.

:::image type="content" source="/azure/ai-foundry/media/content-safety/view-code-option.png" alt-text="Screenshot of the View code button.":::
