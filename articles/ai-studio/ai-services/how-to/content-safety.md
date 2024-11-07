---
title: Use Content Safety in Azure AI Studio
titleSuffix: Azure AI services
description: Learn how to use the Content Safety try it out page in Azure AI Studio to experiment with various content safety features such as text and image content, using adjustable thresholds to filter for inappropriate or harmful content.
ms.service: azure-ai-studio
ms.topic: how-to
author: PatrickFarley
manager: nitinme
ms.date: 11/09/2024
ms.author: pafarley
---

# Use Content Safety in Azure AI Studio 

Azure AI Studio includes a Content Safety **try it out** page that lets you use the core detection models and other content safety features.

## Prerequisites 

- An Azure account. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?icid=ai-services). 
- An [Azure AI resource](https://ms.portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/AIServices). 


## Setup

Follow these steps to use the Content Safety **try it out** page: 

1. Go to [AI Studio](https://ai.azure.com/) and navigate to your project/hub. Then select the **Safety+ Security** tab on the left nav and select the **Try it out** tab.
1. On the **Try it out** page, you can experiment with various content safety features such as text and image content, using adjustable thresholds to filter for inappropriate or harmful content.

:::image type="content" source="../../media/content-safety/try-it-out.png" alt-text="Screenshot of the try it out page for content safety.":::
    
## Analyze text

1. Select the **Moderate text content** panel.
1. Add text to the input field, or select sample text from the panels on the page. 
1. Select **Run test**.
    The service returns all the categories that were detected, with the severity level for each: 0-Safe, 2-Low, 4-Medium, 6-High. It also returns a binary **Accepted**/**Rejected** result, based on the filters you configure. Use the matrix in the **Configure filters** tab to set your allowed/prohibited severity levels for each category. Then you can run the text again to see how the filter works. 

### Use a blocklist 

The **Use blocklist** tab lets you create, edit, and add a blocklist to the moderation workflow. If you have a blocklist enabled when you run the test, you get a **Blocklist detection** panel under **Results**. It reports any matches with the blocklist.

:::image type="content" source="../../media/content-safety/blocklist-panel.png" alt-text="Screenshot of the Use blocklist panel.":::

## Analyze images

The **Moderate image** page provides capability for you to quickly try out image moderation.

1. Select the **Moderate image content** panel. 
1. Select a sample image from the panels on the page, or upload your own image. 
1. Select **Run test**. 
    The service returns all the categories that were detected, with the severity level for each: 0-Safe, 2-Low, 4-Medium, 6-High. It also returns a binary **Accepted**/**Rejected** result, based on the filters you configure. Use the matrix in the **Configure filters** tab on the right to set your allowed/prohibited severity levels for each category. Then you can run the text again to see how the filter works.

## View and export code 

You can use the **View Code** feature in either the **Analyze text content** or **Analyze image content** pages to view and copy the sample code, which includes configuration for severity filtering, blocklists, and moderation functions. You can then deploy the code on your end.

:::image type="content" source="../../media/content-safety/view-code-option.png" alt-text="Screenshot of the View code button.":::

## Use Prompt Shields 

The **Prompt Shields** panel lets you try out user input risk detection. Detect User Prompts designed to provoke the Generative AI model into exhibiting behaviors it was trained to avoid or break the rules set in the System Message. These attacks can vary from intricate role-play to subtle subversion of the safety objective. 

1. Select the **Prompt Shields** panel. 
1. Select a sample text on the page, or input your own content for testing.
1. Select **Run test**. 
    The service returns the risk flag and type for each sample. 

For more information, see the [Prompt Shields conceptual guide](/azure/ai-services/content-safety/concepts/jailbreak-detection). 

## Next step

To use Azure AI Content Safety features with your Generative AI models, see the [Content filtering](../../concepts/content-filtering.md) guide.