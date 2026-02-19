---
title: "Quickstart: Use custom categories in the Foundry portal"
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
    

## Use custom categories

This feature lets you create and train your own custom content categories and scan text for matches. 

1. Select the **Custom categories** panel.
1. Select **Add a new category** to open a dialog box. Enter your category name and a text description, and connect a blob storage container with text training data. Select **Create and train**. 
1. Select a category and enter your sample input text, and select **Run test**. 
    The service returns the custom category result.


For more information, see the [Custom categories conceptual guide](/azure/ai-services/content-safety/concepts/custom-categories).