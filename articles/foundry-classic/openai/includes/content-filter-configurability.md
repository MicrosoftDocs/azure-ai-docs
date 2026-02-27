---
titleSuffix: Azure OpenAI
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
author: PatrickFarley
ms.author: pafarley
ms.date: 09/16/2025
recommendations: false
---



Azure OpenAI in Microsoft Foundry Models includes default safety settings applied to all models (excluding audio API models such as Whisper). These configurations provide you with a responsible experience by default, including content filtering models, blocklists, prompt transformation, [content credentials](../concepts/content-credentials.md), and others. [Read more about it here](/azure/ai-foundry/openai/concepts/default-safety-policies). 

All customers can also configure content filters and create custom content policies that are tailored to their use case requirements. The configurability feature allows customers to adjust the settings, separately for prompts and completions, to filter content for each content category at different severity levels as described in the table below. Content detected at the 'safe' severity level is labeled in annotation output but isn't subject to filtering and isn't configurable.

| Severity filtered | Configurable for prompts | Configurable for completions | Descriptions |
|-------------------|-----------------|-----------|--------------|
| Low, medium, high | Yes | Yes | Strictest filtering configuration. Content detected at severity levels low, medium, and high is filtered.|
| Medium, high      | Yes | Yes | Content detected at severity level low isn't filtered, content at medium and high is filtered.|
| High              | Yes| Yes | Content detected at severity levels low and medium isn't filtered. Only content at severity level high is filtered. |
| No filters | If approved<sup>1</sup>| If approved<sup>1</sup>| No content is filtered regardless of severity level detected. Requires approval<sup>1</sup>.|
|Annotate only | If approved<sup>1</sup>| If approved<sup>1</sup>| Disables the filter functionality, so content will not be blocked, but annotations are returned via API response. Requires approval<sup>1</sup>.|

<sup>1</sup> For Azure OpenAI models, only customers who have been approved for modified content filtering have full content filtering control and can turn off content filters. Apply for modified content filters via this form: [Limited Access Review: Modified Content Filters](https://ncv.microsoft.com/uEfCgnITdR). For Azure Government customers, apply for modified content filters via this form: [Azure Government - Request Modified Content Filtering](https://aka.ms/AOAIGovModifyContentFilter).

Configurable content filters for inputs (prompts) and outputs (completions) are available for all Azure OpenAI models.

Content filtering configurations are created within a Resource in Foundry portal, and can be associated with Deployments. [Learn more about configuring content filters here](../how-to/content-filters.md).  

Customers are responsible for ensuring that applications integrating Azure OpenAI comply with the [Code of Conduct](/legal/ai-code-of-conduct?context=/azure/ai-foundry/openai/context/context). 
