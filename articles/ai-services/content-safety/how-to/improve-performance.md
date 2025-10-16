---
title: "Mitigate false results in Azure AI Content Safety"
titleSuffix: Azure AI services
description: Learn techniques to improve the performance of Azure AI Content Safety models by handling false positives and false negatives.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: how-to
ms.date: 09/16/2025
ms.author: pafarley
#customer intent: As a user, I want to improve the performance of Azure AI Content Safety so that I can ensure accurate content moderation.
---

# Mitigate false results in Azure AI Content Safety

This guide shows you how to handle false positives and false negatives from Azure AI Content Safety models. 

False positives occur when the system incorrectly flags non-harmful content as harmful; false negatives occur when harmful content is not flagged as harmful. Address these instances to ensure the integrity and reliability of your content moderation process, including responsible generative AI deployment.

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.

## Review and verification

Conduct an initial assessment to confirm that you really have a false positive or false negative. This can involve: 
- Checking the context of the flagged content.  
- Comparing the flagged content against the content risk categories and severity definitions:
    - If you're using Guardrails & controls in Azure OpenAI, see the [Azure OpenAI content filtering doc](/azure/ai-foundry/openai/concepts/content-filter).
    - If you're using the Azure AI Content Safety standalone API, see the [Harm categories doc](/azure/ai-services/content-safety/concepts/harm-categories?tabs=warning) or the [Prompt Shields doc](/azure/ai-services/content-safety/concepts/jailbreak-detection), depending on which API you're using.

## Customize your severity settings

If your assessment confirms that you found a false positive or false negative, you can try customizing your severity settings to mitigate the issue. The settings depend on which platform you're using.

#### [Content Safety standalone API](#tab/standalone-api)

If you're using the Azure AI Content Safety standalone API directly, try experimenting by setting the severity threshold at different levels for [harm categories](/azure/ai-services/content-safety/concepts/harm-categories?tabs=definitions) based on API output. Alternatively, if you prefer the no-code approach, you can try out those settings in [Content Safety Studio](https://contentsafety.cognitive.azure.com/) or Azure AI Foundry’s [Content Safety page](https://ai.azure.com/explore/contentsafety). Instructions can be found [here](/azure/ai-foundry/concepts/content-filtering). 

In addition to adjusting the severity levels for false negatives, you can also use blocklists. More information on using blocklists for text moderation can be found in [Use blocklists for text moderation](/azure/ai-services/content-safety/how-to/use-blocklist?tabs=windows%2Crest).


#### [Azure OpenAI](#tab/azure-openai-studio)

Read the [Configurability](/en-us/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cuser-prompt%2Cpython-new#configurability-preview) documentation, as some content filtering configurations may require approval through the process mentioned there.

Follow the steps in the documentation to update configurations to handle false positives or negatives: [How to use content filters (preview) with Azure OpenAI in Azure AI Foundry Models](/azure/ai-foundry/openai/how-to/content-filters). 

In addition to adjusting the severity levels for false negatives, you can also use blocklists. Detailed instruction can be found in [How to use blocklists with Azure OpenAI](/azure/ai-foundry/openai/how-to/use-blocklists).

#### [Azure AI Foundry](#tab/azure-ai-studio)

Read the [Configurability](/azure/ai-foundry/concepts/content-filtering#configurability-preview) documentation, as some content filtering configurations may require approval through the process mentioned there.

Follow the steps in the documentation to update configurations to handle false positives or negatives: [Azure AI Foundry content filtering](/azure/ai-foundry/concepts/content-filtering#create-a-content-filter).

In addition to adjusting the severity levels for false negatives, you can also use blocklists. Detailed instruction can be found in [Azure AI Foundry content filtering](/azure/ai-foundry/concepts/content-filtering#use-a-blocklist-as-a-filter).

---

## Create a custom category based on your own RAI policy

Sometimes you might need to create a custom category to ensure the filtering aligns with your specific Responsible AI policy, as prebuilt categories or content filtering may not be enough. 

Refer to the [Custom categories documentation](/azure/ai-services/content-safety/concepts/custom-categories) to build your own categories with the Azure AI Content Safety API.

## Document issues and send feedback to Azure

If, after you’ve tried all the steps mentioned above, Azure AI Content Safety still can't resolve the false positives or negatives, there is likely a policy definition or model issue that needs further attention.

Document the details of the false positives and/or false negatives by providing the following information to the [Content safety support team](mailto:contentsafetysupport@microsoft.com):
- Description of the flagged content.
- Context in which the content was posted. 
- Reason given by Azure AI Content Safety for the flagging (if positive).
- Explanation of why the content is a false positive or negative.
- Any adjustments already attempted by adjusting severity settings or using custom categories. 
- Screenshots or logs of the flagged content and system responses.

This documentation helps in escalating the issue to the appropriate teams for resolution.

## Related content

- [Azure AI Content Safety overview](/azure/ai-services/content-safety/overview)
- [Harm categories](/azure/ai-services/content-safety/concepts/harm-categories?tabs=warning)