---
title: Azure AI Foundry content filtering
titleSuffix: Azure AI Foundry
description: Learn about the content filtering capabilities of Azure OpenAI in Azure AI Foundry portal.
manager: nitinme
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: conceptual
ms.date: 04/29/2025
ms.reviewer: eur
ms.author: pafarley
author: PatrickFarley
---

# Content filtering in Azure AI Foundry portal

[Azure AI Foundry](https://ai.azure.com) includes a content filtering system that works alongside core models and image generation models.

> [!IMPORTANT]
> The content filtering system isn't applied to prompts and completions processed by the Whisper model in Azure OpenAI in Azure AI Foundry Models. Learn more about the [Whisper model in Azure OpenAI](../../ai-services/openai/concepts/models.md).

## How it works 

The content filtering system is powered by [Azure AI Content Safety](../../ai-services/content-safety/overview.md), and it works by running both the prompt input and completion output through a set of classification models designed to detect and prevent the output of harmful content. Variations in API configurations and application design might affect completions and thus filtering behavior.

With Azure OpenAI model deployments, you can use the default content filter or create your own content filter (described later on). Models available through **serverless APIs** have content filtering enabled by default. To learn more about the default content filter enabled for serverless APIs, see [Content safety for Azure Direct Models in the model catalog](model-catalog-content-safety.md).

## Language support

The content filtering models have been trained and tested on the following languages: English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. However, the service can work in many other languages, but the quality can vary. In all cases, you should do your own testing to ensure that it works for your application.

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
|Low | Content that expresses prejudiced, judgmental, or opinionated views, includes offensive use of language, stereotyping, use cases exploring a fictional world (for example, gaming, literature) and depictions at low intensity.|
| Medium | Content that uses offensive, insulting, mocking, intimidating, or demeaning language towards specific identity groups, includes depictions of seeking and executing harmful instructions, fantasies, glorification, promotion of harm at medium intensity. |
|High | Content that displays explicit and severe harmful instructions, actions, damage, or abuse; includes endorsement, glorification, or promotion of severe harmful acts, extreme or illegal forms of harm, radicalization, or nonconsensual power exchange or abuse.|



### Other input filters

You can also enable special filters for generative AI scenarios: 
- **Jailbreak attacks**: Jailbreak Attacks are User Prompts designed to provoke the Generative AI model into exhibiting behaviors it was trained to avoid or to break the rules set in the System Message.
- **Indirect attacks**: Indirect Attacks, also referred to as Indirect Prompt Attacks or Cross-Domain Prompt Injection Attacks, are a potential vulnerability where third parties place malicious instructions inside of documents that the Generative AI system can access and process.

### Other output filters

You can also enable the following special output filters:
- **Protected material for text**: Protected material text describes known text content (for example, song lyrics, articles, recipes, and selected web content) that can be outputted by large language models.
- **Protected material for code**: Protected material code describes source code that matches a set of source code from public repositories, which can be outputted by large language models without proper citation of source repositories.
- **Groundedness**: The groundedness detection filter detects whether the text responses of large language models (LLMs) are grounded in the source materials provided by the users.

[!INCLUDE [create-content-filter](../includes/create-content-filter.md)]

### Configurability (preview)

The default content filtering configuration for the GPT model series is set to filter at the medium severity threshold for all four content harm categories (hate, violence, sexual, and self-harm) and applies to both prompts (text, multi-modal text/image) and completions (text). This means that content that is detected at severity level medium or high is filtered, while content detected at severity level low isn't filtered by the content filters. For DALL-E, the default severity threshold is set to low for both prompts (text) and completions (images), so content detected at severity levels low, medium, or high is filtered. 

The configurability feature allows customers to adjust the settings, separately for prompts and completions, to filter content for each content category at different severity levels as described in the table below:

| Severity filtered | Configurable for prompts | Configurable for completions | Descriptions |
|-------------------|--------------------------|------------------------------|--------------|
| Low, medium, high | Yes | Yes | Strictest filtering configuration. Content detected at severity levels low, medium and high is filtered.|
| Medium, high      | Yes | Yes | Content detected at severity level low isn't filtered, content at medium and high is filtered.|
| High              | Yes| Yes | Content detected at severity levels low and medium isn't filtered. Only content at severity level high is filtered. Requires approval<sup>1</sup>.|
| No filters | If approved<sup>1</sup>| If approved<sup>1</sup>| No content is filtered regardless of severity level detected. Requires approval<sup>1</sup>.|

<sup>1</sup> For Azure OpenAI models, only customers who have been approved for modified content filtering have full content filtering control, including configuring content filters at severity level high only or turning off content filters. Apply for modified content filters via these forms: [Azure OpenAI Limited Access Review: Modified Content Filters](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUMlBQNkZMR0lFRldORTdVQzQ0TEI5Q1ExOSQlQCN0PWcu), and [Modified Abuse Monitoring](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUOE9MUTFMUlpBNk5IQlZWWkcyUEpWWEhGOCQlQCN0PWcu).

Customers are responsible for ensuring that applications integrating Azure OpenAI comply with the [Code of Conduct](/legal/ai-code-of-conduct?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext). 


## Related content

- Learn more about the [underlying models that power Azure OpenAI](../../ai-services/openai/concepts/models.md).
- Azure AI Foundry content filtering is powered by [Azure AI Content Safety](../../ai-services/content-safety/overview.md).
- Learn more about understanding and mitigating risks associated with your application: [Overview of Responsible AI practices for Azure OpenAI models](/legal/cognitive-services/openai/overview?context=/azure/ai-services/context/context).
- Learn more about evaluating your generative AI models and AI systems via [Azure AI Evaluation](https://aka.ms/genaiopsevals). 
