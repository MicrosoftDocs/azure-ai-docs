---
title: "Improve performance in Azure AI Content Safety"
titleSuffix: Azure AI services
description: tbd
#services: cognitive-services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: how-to
ms.date: 09/18/2024
ms.author: pafarley
---

# Improve performance in Azure AI Content Safety

This playbook provides a step-by-step guide for users of Azure AI Content Safety on how to handle false positives and false negatives effectively. False positives occur when the system incorrectly identifies non-harmful content as harmful, while false negatives occur when harmful content is not flagged. Properly addressing these instances ensures the integrity and reliability of the content moderation process, including responsible generative AI deployment. 

## Review and verification

Conduct an initial assessment to determine whether the flagged content is indeed a false positive or false negative. This can involve: 
- Checking the context of the flagged content.  
- Comparing the flagged content against the content safety risk categories and severity definitions. 
    - If you are using content safety in Azure OpenAI, go here 
    - If you are using the Azure AI Content Safety standalone API, go here for harm categories and here for Prompt Shields 

## Customize your severity settings 

If your assessment confirms that this is indeed a false positive or false negative, you can try customizing your severity settings to mitigate the issue before reaching out to Microsoft.

### Azure AI Content Safety standalone API users 

If you are using the Azure AI Content Safety standalone API , try experimenting by setting the severity threshold at different levels for [harm categories](/azure/ai-services/content-safety/concepts/harm-categories?tabs=definitions) based on API output. Alternatively, if you prefer the no-code approeach, you can try out those settings in [content safety studio](https://contentsafety.cognitive.azure.com/) or Azure AI Studio’s [content safety page](https://ai.azure.com/explore/contentsafety). Instructions can be found [here](/azure/ai-studio/quickstarts/content-safety?tabs=moderate-text-content). 

In addition to adjusting the severity levels for false negatives, you can also use blocklists. More information on using blocklists for text moderation can be found in [Use blocklists for text moderation](/azure/ai-services/content-safety/how-to/use-blocklist?tabs=windows%2Crest).

## Azure AI Studio Content Filtering users

Read the [Configurability](/azure/ai-studio/concepts/content-filtering#configurability-preview) documentation, as some content filtering configurations may require approval through the process mentioned there. 

Follow the steps in the documentation to update configurations to handle false positives or negatives: [Azure AI Studio content filtering](/azure/ai-studio/concepts/content-filtering#create-a-content-filter).

In addition to adjusting the severity levels for false negatives, you can also use blocklists. Detailed instruction can be found here:  [Azure AI Studio content filtering](/azure/ai-studio/concepts/content-filtering#use-a-blocklist-as-a-filter).

## Create a custom category based on your own RAI policy

Sometimes, you might need a custom category to ensure the filtering aligns with your specific Responsible AI policy, as pre-built categories or content filtering may not suffice. You may require an entirely new content category. 

Refer to the [custom categories documentation](/azure/ai-services/content-safety/custom-category) to build your own categories with the Azure AI Content Safety standalone API. 

We are currently working on integrating the custom categories feature into Azure OpenAI and AI Studio, which will be available soon. 

## Document issues and send feedback to Azure

If, after you’ve exhausted all the steps mentioned above, the false positives or negatives cannot be resolved by Azure AI Content Safety, it is likely a policy definition or model issue that needs further attention.

Document the details of the false positives and/or false negatives by providing the following information:
- Description of the flagged content. 
- Context in which the content was posted. 
- Reason given by Azure AI Content Safety for the flagging. 
- Explanation of why the content is a false positive or negative. 
- Any adjustments already attempted in severity settings or custom categories. 
- Screenshots or logs of the flagged content and system responses.

This documentation will help in escalating the issue to the appropriate teams for resolution. 

Send the feedback to our Azure CSS by following the instructions [here](tbd).