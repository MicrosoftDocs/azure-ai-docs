---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
author: PatrickFarley
ms.author: pafarley
ms.date: 09/25/2024
recommendations: false
---

Models deployed to Microsoft Foundry (formerly known Azure AI Services) include default safety settings applied to all models, excluding Azure OpenAI Whisper. These configurations provide you with a [responsible experience by default](../../openai/concepts/default-safety-policies.md).

Certain models allow customers to configure content filters and create custom safety policies that are tailored to their use case requirements. The configurability feature allows customers to adjust the settings, separately for prompts and completions, to filter content for each content category at different severity levels as described in the table below. Content detected at the 'safe' severity level is labeled in annotations but is not subject to filtering and isn't configurable.

| Severity filtered | Configurable for prompts | Configurable for completions | Descriptions |
|-------------------|--------------------------|------------------------------|--------------|
| Low, medium, high | Yes | Yes | Strictest filtering configuration. Content detected at severity levels low, medium, and high is filtered.|
| Medium, high      | Yes | Yes | Content detected at severity level low isn't filtered, content at medium and high is filtered.|
| High              | Yes| Yes | Content detected at severity levels low and medium isn't filtered. Only content at severity level high is filtered. |
| No filters | If approved<sup>1</sup>| If approved<sup>1</sup>| No content is filtered regardless of severity level detected. Requires approval<sup>1</sup>.|
|Annotate only | If approved<sup>1</sup>| If approved<sup>1</sup>| Disables the filter functionality, so content will not be blocked, but annotations are returned via API response. Requires approval<sup>1</sup>.|

<sup>1</sup> For Azure OpenAI models, only customers who have been approved for modified content filtering have full content filtering control and can turn off content filters. Apply for modified content filters via this form: [Azure OpenAI Limited Access Review: Modified Content Filters](https://ncv.microsoft.com/uEfCgnITdR). For Azure Government customers, apply for modified content filters via this form: [Azure Government - Request Modified Content Filtering for Azure OpenAI in Foundry Models](https://aka.ms/AOAIGovModifyContentFilter).

Content filtering configurations are created within a resource in Foundry portal, and can be associated with Deployments. Learn how to [configure a content filter](../how-to/configure-content-filters.md)