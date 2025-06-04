---
title: Customer Copyright Commitment Required Mitigations | Azure OpenAI Service
description: Customer Copyright Commitment Required Mitigations for Azure OpenAI Service
keywords: Code of Conduct for Azure OpenAI Service
author: mrbullwinkle
ms.author: mbullwin
ms.service: azure-ai-openai
ms.topic: article
ms.reviewer: nitinme
ms.date: 05/21/2024
---

# Customer Copyright Commitment Required Mitigations

> [!NOTE]
> The requirements described below apply only to customers using Azure OpenAI Service and other Covered Products with configurable Metaprompts or other safety systems ("Configurable GAI Services"). They do not apply to customers using other Covered Products including Copilots with safety systems that are fixed.

The Customer Copyright Commitment ("CCC") is a provision in the Microsoft Product Terms that describes Microsoft's obligation to defend customers against certain third-party intellectual property claims relating to Output Content. For Azure OpenAI Service and any Configurable GAI Service, Customer also must have implemented all mitigations required by the Azure OpenAI Service documentation in the offering that delivered the Output Content that is the subject of the claim. The required mitigations to maintain CCC coverage are set forth below.

This page describes only the required mitigations necessary to maintain CCC coverage for Azure OpenAI Service and Configurable GAI Services. It is not an exhaustive list of requirements or mitigations required to use Azure OpenAI Service (or Configurable GAI Services) responsibly in compliance with the documentation. Azure OpenAI Service customers must comply with the [Code of Conduct](/azure/ai-foundry/responsible-ai/openai/code-of-conduct?context=/azure/ai-services/openai/context/context) at all times.

The section "Required Mitigations for GitHub Offerings" are the only requirements that apply to GitHub offerings, and separately took effect on November 1, 2023. The other mitigations below took effect on the dates indicated. For new Configurable GAI Services, features, models, or use cases, new CCC requirements will be posted and take effect at or following the launch of such Configurable GAI Service, feature, model, or use case. Otherwise, customers will have six months from the date of publication on this page to implement any new mitigations required to maintain coverage under the CCC. The Effective Date indicates when the mitigation must be deployed. If a customer tenders a claim for defense, the customer will be required to demonstrate compliance with all relevant requirements, both on this page and as listed in the Product Terms.

## Universal Required Mitigations

Universal required mitigations must be implemented to maintain CCC coverage for all offerings delivering Output Content from Azure OpenAI Service and Configurable GAI Services, with the exception of GitHub Offerings. The requirements are set forth here:

**Azure OpenAI Service & Configurable GAI Services - Universal Required Mitigations:**

|**Category**|**Required Mitigation**|**Effective Date**|
|---|---|---|
| Metaprompt | The customer offering must include a metaprompt directing the model to prevent copyright infringement in its output, for example, the sample metaprompt, "To Avoid Copyright Infringements" at: [System message framework and template recommendations for Large Language Models(LLMs)](/azure/ai-services/openai/concepts/system-message)|December 1, 2023|
| Testing and Evaluation Report | The customer offering must have been subjected to evaluations (e.g., guided red teaming, systematic measurement, or other equivalent approach) by the customer using tests designed to detect the output of third-party content. Significant ongoing reproduction of third-party content determined through evaluation must be addressed. The report of results and mitigations must be retained by the customer and provided to Microsoft in the event of a claim. Customer is under no obligation to conduct direct testing of Microsoft services to maintain CCC coverage. More information on guided red teaming is at: [Red teaming large language models (LLMs)](/azure/ai-services/openai/concepts/red-teaming). More information on systematic measurement is at: [Overview of Responsible AI practices for Azure OpenAI models - Azure AI services - Microsoft Learn.](overview.md) |December 1, 2023|

## Additional Required Mitigations Per Azure OpenAI Service Use Case

Additional required mitigations are required to maintain CCC coverage for offerings delivering Output Content from Azure OpenAI Service, depending on what use cases the customer is using. As used below, “use case” refers to a major intended use of your application by your users. Use cases may have been indicated on a Limited Access Form. More information about use cases is available at: [Transparency Note for Azure OpenAI - Azure AI services | Microsoft Learn](transparency-note.md). Requirements are cumulative, meaning that the customer offering must include the required mitigations for all use cases. These additional requirements do not apply to Configurable GAI Services, only Azure OpenAI Service.

Not all content types can be generated by every application. The following required mitigations must be enabled for any use case described below. Azure OpenAI content filters include protected material detection and Prompt Shield. Protected material detection can analyze both text and code. Different filters must be on depending on content type.

The required mitigations are set forth here:

**Azure OpenAI Service Only - Additional Required Mitigations Per Use Case**

**Text and Code Use Cases:**

| **Content type** | **Use Case** | **Category** | **Required Mitigation** | **Effective Date** |
|---|---|---|---|---|
| Code generation | Code generation or transformation scenarios, or other open code generation scenarios | Content filters | The protected material code model must be configured on in either annotate or filter mode. If choosing to use annotate mode, customer must comply with any cited license provided for Output Content that is the subject of the claim.<br><br>The jailbreak model (i.e., Prompt Shield for jailbreak attacks) must be configured on in filter mode. | December 1, 2023 |
||  |  |If using the asynchronous filter feature, Output Content retroactively flagged as protected material code is not covered by the CCC, unless customer complies with its cited license.| May 21, 2024 |
| Text generation | Journalistic content, writing assistance, or other open text generation scenarios | Content filters | The protected material text model must be configured on in filter mode. The jailbreak model (i.e., Prompt Shield for jailbreak attacks) must be configured on in filter mode.|December 1, 2023 |
|  |  |  | If using the asynchronous filter feature, Output Content retroactively flagged as protected material text is not covered by the CCC.   | May 21, 2024 |

**Image generation models, OpenAI Whisper model, and all other use cases:**

No additional requirements.

## Required Mitigations for GitHub Offerings

The below are the only required mitigations that apply to GitHub Offerings, and separately took effect in the Product Terms on November 1, 2023.

**Required Mitigations for GitHub Offerings Only**

|**Category**|**Required Mitigation**|**Effective Date**|
|---|---|---|
|GitHub Offerings| Either the Duplicate Detection filtering feature must be set to the "Block" setting, or, if using annotate mode, customers must comply with cited licenses. Customers can learn how to enable the Duplicate Detection filter at [https://gh.io/cfb-dd](https://gh.io/cfb-dd).|November 1, 2023|
