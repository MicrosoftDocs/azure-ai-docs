---
title: "Quickstart: Use prompt shields in the Foundry portal"
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


## Use Prompt Shields 

The **Prompt Shields** panel lets you try out user input risk detection. Detect User Prompts designed to provoke the Generative AI model into exhibiting behaviors it was trained to avoid or break the rules set in the System Message. These attacks can vary from intricate role-play to subtle subversion of the safety objective. 

1. Select the **Prompt Shields** panel. 
1. Select a sample text on the page, or input your own content for testing.
1. Select **Run test**. 
    The service returns the risk flag and type for each sample. 

For more information, see the [Prompt Shields conceptual guide](/azure/ai-services/content-safety/concepts/jailbreak-detection). 

