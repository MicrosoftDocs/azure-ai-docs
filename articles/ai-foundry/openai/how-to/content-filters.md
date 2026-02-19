---
title: 'Configure content filters'
titleSuffix: Azure OpenAI
description: Learn how to use and configure the content filters that come with Microsoft Foundry, including getting approval for gated modifications.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 12/03/2025
author: ssalgadodev
ms.author: ssalgado
recommendations: false
ms.custom: FY25Q1-Linter
# customer intent: As a developer, I want to learn how to configure content filters with Microsoft Foundry so that I can ensure that my applications comply with our Code of Conduct.
---

# Configure content filters

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

The content filtering system integrated into Microsoft Foundry runs alongside the core models, including image generation models. It uses an ensemble of multi-class classification models to detect four categories of harmful content (violence, hate, sexual, and self-harm) at four severity levels respectively (safe, low, medium, and high), and optional binary classifiers for detecting jailbreak risk, existing text, and code in public repositories. 

The default content filtering configuration is set to filter at the medium severity threshold for all four content harms categories for both prompts and completions. That means that content that is detected at severity level medium or high is filtered, while content detected at severity level low or safe is not filtered by the content filters. Learn more about content categories, severity levels, and the behavior of the content filtering system [here](../concepts/content-filter.md). 

Prompt shields and protected text and code models are optional and on by default. For prompt shields and protected material text and code models, the configurability feature allows all customers to turn the models on and off. The models are by default on and can be turned off per your scenario. Some models are required to be on for certain scenarios to retain coverage under the [Customer Copyright Commitment](/azure/ai-foundry/responsible-ai/openai/customer-copyright-commitment).

> [!NOTE]
> All customers have the ability to modify the content filters and configure the severity thresholds (low, medium, high). Approval is required for turning the content filters partially or fully off. Managed customers only may apply for full content filtering control via this form: [Limited Access Review: Modified Content Filters](https://ncv.microsoft.com/uEfCgnITdR). At this time, it is not possible to become a managed customer.

Content filters can be configured at the resource level. Once a new configuration is created, it can be associated with one or more deployments. For more information about model deployment, see the [resource deployment guide](create-resource.md).

## Prerequisites

* You must have an Azure OpenAI resource and a large language model (LLM) deployment to configure content filters. Follow a [quickstart](/azure/ai-foundry/openai/chatgpt-quickstart?) to get started.

## Understand content filter configurability

[!INCLUDE [content-filter-configurability](../includes/content-filter-configurability.md)]
 
## Understand other filters

You can configure the following filter categories in addition to the default harm category filters.

|Filter category  |Status |Default setting  |Applied to prompt or completion?  |Description  |
|---------|---------|---------|---------|---|
|Prompt Shields for direct attacks (jailbreak)     |GA|    On     |   User prompt      |   Filters / annotates user prompts that might present a Jailbreak Risk. For more information about annotations, visit [Foundry content filtering](/azure/ai-foundry/openai/concepts/content-filter?tabs=python#annotations-preview). |
|Prompt Shields for indirect attacks  | GA| Off | User prompt | Filter / annotate Indirect Attacks, also referred to as Indirect Prompt Attacks or Cross-Domain Prompt Injection Attacks, a potential vulnerability where third parties place malicious instructions inside of documents that the generative AI system can access and process. Requires: [Document embedding and formatting](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cuser-prompt%2Cpython-new#embedding-documents-in-your-prompt). |
| Protected material - code |GA| On | Completion | Filters protected code or gets the example citation and license information in annotations for code snippets that match any public code sources, powered by GitHub Copilot. For more information about consuming annotations, see the [Protected material concepts guide](/azure/ai-foundry/openai/concepts/content-filter-protected-material) |
| Protected material - text | GA| On | Completion | Identifies and blocks known text content from being displayed in the model output (for example, song lyrics, recipes, and selected web content).  |
| Groundedness | Preview |Off | Completion |Detects whether the text responses of large language models (LLMs) are grounded in the source materials provided by the users. Ungroundedness refers to instances where the LLMs produce information that is non-factual or inaccurate from what was present in the source materials. Requires: [Document embedding and formatting](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cuser-prompt%2Cpython-new#embedding-documents-in-your-prompt).|
| Personally identifiable information (PII) | Preview | Off | Completion | Filters information that can be used to identify a particular individual, such as a name, address, phone number, email address, social security number, driver's license number, passport number, or similar information. |


[!INCLUDE [create-content-filter](../../../ai-foundry/includes/create-content-filter.md)]

## Specify a content filtering configuration at request time 

In addition to the deployment-level content filtering configuration, we also provide a request header that allows you specify your custom configuration at request time for each API call. 

```bash
curl --request POST \ 
    --url 'URL' \ 
    --header 'Content-Type: application/json' \ 
    --header 'api-key: API_KEY' \ 
    --header 'x-policy-id: CUSTOM_CONTENT_FILTER_NAME' \ 
    --data '{ 
        "messages": [ 
            { 
                "role": "system", 
                "content": "You are a creative assistant." 
            }, 
            { 
                "role": "user", 
                "content": "Write a poem about the beauty of nature." 
            } 
        ] 
    }' 
```

The request-level content filtering configuration will override the deployment-level configuration, for the specific API call. 

> [!IMPORTANT]
> Content filter specification at request time is not available for image input (chat with images) scenarios. In those cases the default content filter will be used.

If a configuration is specified that does not exist, the following error message will be returned. 

```json
{ 
    "error": 
        { 
            "code": "InvalidContentFilterPolicy", 
            "message": "Your request contains invalid content filter policy. Please provide a valid policy." 
        } 
} 
```

## Report content filtering feedback

If you are encountering a content filtering issue, select the **Filters Feedback** button at the top of the playground. This is enabled in the **Images, Chat, and Completions** playground once you submit a prompt. 

When the dialog appears, select the appropriate content filtering issue. Include as much detail as possible relating to your content filtering issue, such as the specific prompt and content filtering error you encountered. Do not include any private or sensitive information. 

For support, please [submit a support ticket](https://ms.portal.azure.com/#view/Microsoft_Azure_Support/HelpAndSupportBlade/~/overview). 

## Follow best practices

We recommend informing your content filtering configuration decisions through an iterative identification (for example, red team testing, stress-testing, and analysis) and measurement process to address the potential harms that are relevant for a specific model, application, and deployment scenario. After you implement mitigations such as content filtering, repeat measurement to test effectiveness. Recommendations and best practices for Responsible AI for Azure OpenAI, grounded in the [Microsoft Responsible AI Standard](https://aka.ms/RAI) can be found in the [Responsible AI Overview for Azure OpenAI](/azure/ai-foundry/responsible-ai/openai/overview).

## Related content

- Learn more about Responsible AI practices for Azure OpenAI: [Overview of Responsible AI practices for Azure OpenAI models](/azure/ai-foundry/responsible-ai/openai/overview).
- Read more about [content filtering categories and severity levels](../concepts/content-filter.md) with Foundry.
- Learn more about red teaming from our: [Introduction to red teaming large language models (LLMs) article](../concepts/red-teaming.md).
- Learn how to [configure content filters using the API](/rest/api/aiservices/accountmanagement/rai-policies/create-or-update)
