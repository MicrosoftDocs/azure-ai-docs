---
title: "Quickstart: Use groundedness detection"
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



## Use Groundedness detection

The Groundedness detection panel lets you detect whether the text responses of large language models (LLMs) are grounded in the source materials provided by the users.

1. Select the **Groundedness detection** panel.
1. Select a sample content set on the page, or input your own for testing.
1. Optionally, enable the reasoning feature and select your Azure OpenAI resource from the dropdown.
1. Select **Run test**. 
    The service returns the groundedness detection result.


For more information, see the [Groundedness detection conceptual guide](/azure/ai-services/content-safety/concepts/groundedness).

