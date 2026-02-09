---
title: Microsoft Foundry content filtering
titleSuffix: Microsoft Foundry
description: Learn about the content filtering capabilities of Azure OpenAI in Microsoft Foundry portal.
manager: nitinme
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: concept-article
ms.date: 12/30/2025
ms.author: pafarley
author: PatrickFarley
---

# Content filtering in Microsoft Foundry portal

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

[Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) includes a content filtering system that works alongside core models and image generation models.

> [!IMPORTANT]
> The content filtering system isn't applied to prompts and completions processed by the Whisper model in Foundry Models. Learn more about the [Whisper model in Azure OpenAI](../foundry-models/concepts/models-sold-directly-by-azure.md).

## How it works 

The content filtering system is powered by [Azure AI Content Safety](../../ai-services/content-safety/overview.md), and it works by running both the model prompt input and completion output through a set of classification models designed to detect and prevent harmful content. Variations in API configurations and application design might affect completions and thus filtering behavior.

With Azure OpenAI model deployments, you can use the default content filter or create your own content filter (described later). Models available through **serverless API deployments** have content filtering enabled by default. To learn more about the default content filter enabled for serverless API deployments, see [Content safety for Models Sold Directly by Azure ](model-catalog-content-safety.md).

## Language support

The content filtering models are trained and tested on the following languages: English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. However, the service can work in many other languages, but the quality can vary. In all cases, you should do your own testing to ensure that it works for your application.

## Content risk filters (input and output filters)

The following special filters work for both input and output of generative AI models: 

### Categories

|Category|Description|
|--------|-----------|
| Hate   |The hate category describes language attacks or uses that include pejorative or discriminatory language with reference to a person or identity group based on certain differentiating attributes of these groups including but not limited to race, ethnicity, nationality, gender identity and expression, sexual orientation, religion, immigration status, ability status, personal appearance, and body size. |
| Sexual | The sexual category describes language related to anatomical organs and genitals, romantic relationships, acts portrayed in erotic or affectionate terms, physical sexual acts, including those portrayed as an assault or a forced sexual violent act against one's will, prostitution, pornography, and abuse. |
| Violence | The violence category describes language related to physical actions intended to hurt, injure, damage, or kill someone or something; describes weapons, etc.   |
| Self-Harm | The self-harm category describes language related to physical actions intended to purposely hurt, injure, or damage one's body, or kill oneself.|

### Severity levels

|Category|Description|
|--------|-----------|
|Safe    | Content might be related to violence, self-harm, sexual, or hate categories but the terms are used in general, journalistic, scientific, medical, and similar professional contexts, which are appropriate for most audiences. |
|Low | Content that expresses prejudiced, judgmental, or opinionated views, includes offensive use of language, stereotyping, use cases exploring a fictional world (for example, gaming, literature), and depictions at low intensity.|
| Medium | Content that uses offensive, insulting, mocking, intimidating, or demeaning language towards specific identity groups, includes depictions of seeking and executing harmful instructions, fantasies, glorification, promotion of harm at medium intensity. |
|High | Content that displays explicit and severe harmful instructions, actions, damage, or abuse; includes endorsement, glorification, or promotion of severe harmful acts, extreme or illegal forms of harm, radicalization, or nonconsensual power exchange or abuse.|



### Other input filters

You can also enable special filters for generative AI scenarios: 
- **Jailbreak attacks**: Jailbreak Attacks are User Prompts designed to provoke the Generative AI model into exhibiting behaviors it was trained to avoid or to break the rules set in the System Message.
- **Indirect attacks**: Indirect Attacks, also referred to as Indirect Prompt Attacks or Cross-Domain Prompt Injection Attacks, are a potential vulnerability where third parties place malicious instructions inside of documents that the Generative AI system can access and process.

### Other output filters

You can also enable the following special output filters:
- **Protected material for text**: Protected material text describes known text content (for example, song lyrics, articles, recipes, and selected web content) that a large language model might output.
- **Protected material for code**: Protected material code describes source code that matches a set of source code from public repositories, which a large language models might output without proper citation of source repositories.
- **Groundedness**: The groundedness detection filter detects whether the text responses of large language models (LLMs) are grounded in the source materials provided by the users.
- **Personally identifiable information (PII)**: The PII filter detects whether the text responses of large language models (LLMs) contain personally identifiable information (PII). PII refers to any information that can be used to identify a particular individual, such as a name, address, phone number, email address, social security number, driver's license number, passport number, or similar information.

[!INCLUDE [create-content-filter](../includes/create-content-filter.md)]

## Configurability (preview)

[!INCLUDE [content-filter-configurability](../openai/includes/content-filter-configurability.md)]


## Related content

- Learn more about the [underlying models that power Azure OpenAI](../foundry-models/concepts/models-sold-directly-by-azure.md).
- Foundry content filtering is powered by [Azure AI Content Safety](../../ai-services/content-safety/overview.md).
- Learn more about understanding and mitigating risks associated with your application: [Overview of Responsible AI practices for Azure OpenAI models](/azure/ai-foundry/responsible-ai/openai/overview).
- Learn more about evaluating your generative AI models and AI systems via [Azure AI Evaluation](https://aka.ms/genaiopsevals). 
