---
title: 'Use content filters (preview) with Azure AI Foundry'
titleSuffix: Azure OpenAI
description: Learn how to use and configure the content filters that come with Azure AI Foundry, including getting approval for gated modifications.
#services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 12/05/2024
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
ms.custom: FY25Q1-Linter
# customer intent: As a developer, I want to learn how to configure content filters with Azure AI Foundry so that I can ensure that my applications comply with our Code of Conduct.
---

# How to configure content filters with Azure AI Foundry

The content filtering system integrated into Azure AI Foundry runs alongside the core models, including DALL-E image generation models. It uses an ensemble of multi-class classification models to detect four categories of harmful content (violence, hate, sexual, and self-harm) at four severity levels respectively (safe, low, medium, and high), and optional binary classifiers for detecting jailbreak risk, existing text, and code in public repositories. 

The default content filtering configuration is set to filter at the medium severity threshold for all four content harms categories for both prompts and completions. That means that content that is detected at severity level medium or high is filtered, while content detected at severity level low or safe is not filtered by the content filters. Learn more about content categories, severity levels, and the behavior of the content filtering system [here](../concepts/content-filter.md). 

Jailbreak risk detection and protected text and code models are optional and off by default. For jailbreak and protected material text and code models, the configurability feature allows all customers to turn the models on and off. The models are by default off and can be turned on per your scenario. Some models are required to be on for certain scenarios to retain coverage under the [Customer Copyright Commitment](/legal/cognitive-services/openai/customer-copyright-commitment?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext).

> [!NOTE]
> All customers have the ability to modify the content filters and configure the severity thresholds (low, medium, high). Approval is required for turning the content filters partially or fully off. Managed customers only may apply for full content filtering control via this form: [Azure OpenAI Limited Access Review: Modified Content Filters](https://ncv.microsoft.com/uEfCgnITdR). At this time, it is not possible to become a managed customer.

Content filters can be configured at the resource level. Once a new configuration is created, it can be associated with one or more deployments. For more information about model deployment, see the [resource deployment guide](create-resource.md).

## Prerequisites

* You must have an Azure OpenAI resource and a large language model (LLM) deployment to configure content filters. Follow a [quickstart](/azure/ai-services/openai/chatgpt-quickstart?) to get started.

## Understand content filter configurability

[!INCLUDE [content-filter-configurability](../includes/content-filter-configurability.md)]
 
## Understand other filters

You can configure the following filter categories in addition to the default harm category filters.

|Filter category  |Status |Default setting  |Applied to prompt or completion?  |Description  |
|---------|---------|---------|---------|---|
|Prompt Shields for direct attacks (jailbreak)     |GA|    On     |   User prompt      |   Filters / annotates user prompts that might present a Jailbreak Risk. For more information about annotations, visit [Azure AI Foundry content filtering](/azure/ai-services/openai/concepts/content-filter?tabs=python#annotations-preview). |
|Prompt Shields for indirect attacks  | GA| Off | User prompt | Filter / annotate Indirect Attacks, also referred to as Indirect Prompt Attacks or Cross-Domain Prompt Injection Attacks, a potential vulnerability where third parties place malicious instructions inside of documents that the generative AI system can access and process. Requires: [Document embedding and formatting](/azure/ai-services/openai/concepts/content-filter?tabs=warning%2Cuser-prompt%2Cpython-new#embedding-documents-in-your-prompt). |
| Protected material - code |GA| On | Completion | Filters protected code or gets the example citation and license information in annotations for code snippets that match any public code sources, powered by GitHub Copilot. For more information about consuming annotations, see the [content filtering concepts guide](/azure/ai-services/openai/concepts/content-filter#annotations-preview) |
| Protected material - text | GA| On | Completion | Identifies and blocks known text content from being displayed in the model output (for example, song lyrics, recipes, and selected web content).  |
| Groundedness* | Preview |Off | Completion |Detects whether the text responses of large language models (LLMs) are grounded in the source materials provided by the users. Ungroundedness refers to instances where the LLMs produce information that is non-factual or inaccurate from what was present in the source materials. Requires: [Document embedding and formatting](/azure/ai-services/openai/concepts/content-filter?tabs=warning%2Cuser-prompt%2Cpython-new#embedding-documents-in-your-prompt).|

[!INCLUDE [create-content-filter](../../../ai-studio/includes/create-content-filter.md)]

## Report content filtering feedback

If you are encountering a content filtering issue, select the **Send Feedback** button at the top of the playground. This is enabled in the **Images, Chat, and Completions** playground.  

When the dialog appears, select the appropriate content filtering issue. Include as much detail as possible relating to your content filtering issue, such as the specific prompt and content filtering error you encountered. Do not include any private or sensitive information. 

For support, please [submit a support ticket](https://ms.portal.azure.com/#view/Microsoft_Azure_Support/HelpAndSupportBlade/~/overview). 

## Follow best practices

We recommend informing your content filtering configuration decisions through an iterative identification (for example, red team testing, stress-testing, and analysis) and measurement process to address the potential harms that are relevant for a specific model, application, and deployment scenario. After you implement mitigations such as content filtering, repeat measurement to test effectiveness. Recommendations and best practices for Responsible AI for Azure OpenAI, grounded in the [Microsoft Responsible AI Standard](https://aka.ms/RAI) can be found in the [Responsible AI Overview for Azure OpenAI](/legal/cognitive-services/openai/overview?context=/azure/ai-services/openai/context/context).

## Related content

- Learn more about Responsible AI practices for Azure OpenAI: [Overview of Responsible AI practices for Azure OpenAI models](/legal/cognitive-services/openai/overview?context=/azure/ai-services/openai/context/context).
- Read more about [content filtering categories and severity levels](../concepts/content-filter.md) with Azure AI Foundry.
- Learn more about red teaming from our: [Introduction to red teaming large language models (LLMs) article](../concepts/red-teaming.md).
