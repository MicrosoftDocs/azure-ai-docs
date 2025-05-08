---
title: "Quickstart: Use protected material detection"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 04/10/2025
ms.author: pafarley
---


## Prerequisites 

- An Azure account. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?icid=ai-services). 
- An [Azure AI resource](https://ms.portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/AIServices). 


## Setup

Follow these steps to use the Content Safety **try it out** page: 

1. Go to [Azure AI Foundry](https://ai.azure.com/) and navigate to your project/hub. Then select the **Guardrails + controls** tab on the left nav and select the **Try it out** tab.
1. On the **Try it out** page, you can experiment with various content safety features such as text and image content, using adjustable thresholds to filter for inappropriate or harmful content.

:::image type="content" source="/azure/ai-foundry/media/content-safety/try-it-out.png" alt-text="Screenshot of the try it out page for content safety.":::


## Use Protected material detection

This feature scans AI-generated text for known text content (for example, song lyrics, articles, recipes, selected web content).

1. Select the **Protected material detection for text** or **Protected material detection for code** panel.
1. Select a sample text on the page, or input your own for testing.
1. Select **Run test**. 
    The service returns the protected content result.

For more information, see the [Protected material conceptual guide](/azure/ai-services/content-safety/concepts/protected-material).