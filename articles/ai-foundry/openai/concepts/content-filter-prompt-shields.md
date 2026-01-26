---
title: Content Filter Prompt Shields
description: Learn about prompt shield content in Azure OpenAI, including user prompt attacks and indirect attack severity definitions.
author: ssalgadodev
ms.author: ssalgado
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 11/05/2025
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Prompt shields in Foundry

::: moniker range="foundry"

Prompt shields are a feature of the Microsoft Foundry Guardrails and controls system that helps detect and mitigate user prompt attacks. These attacks occur when a user attempts to manipulate the model's behavior by embedding harmful or inappropriate content within their input.

Prompt shields analyzes LLM inputs and detects adversarial user input attacks.

[!INCLUDE [prompt-shield-attack-info](../../../ai-services/content-safety/includes/prompt-shield-attack-info.md)]

::: moniker-end

::: moniker range="foundry-classic"

Prompt shields are a feature of the Azure OpenAI content filtering system that helps detect and mitigate user prompt attacks. These attacks occur when a user attempts to manipulate the model's behavior by embedding harmful or inappropriate content within their input.

Prompt shields analyzes LLM inputs and detects adversarial user input attacks.

[!INCLUDE [prompt-shield-attack-info](../../../ai-services/content-safety/includes/prompt-shield-attack-info.md)]

::: moniker-end

## Spotlighting for prompt shields (preview)

Spotlighting is a feature that enhances protection against indirect attacks by tagging the input documents with special formatting to indicate lower trust to the model. When spotlighting is enabled, the service transforms the document content using base-64 encoding, and the model treats this content as less trustworthy than direct user and system prompts. This protection helps prevent the model from executing unintended commands or actions that are found in the content of the documents.  

When spotlighting is enabled, the service transforms document content using base-64 encoding so that the model treats it as less trustworthy than direct user and system prompts.  

Spotlighting is turned off by default. You can enable it when configuring content filters in the Foundry portal or through the REST API. Spotlighting is only available for models used via the Chat Completions API.  

There is no direct cost for spotlighting, but it adds tokens to user and system prompts, which can increase total costs. Spotlighting can also cause large documents to exceed input size limits.  

An occasional known side effect of spotlighting is the model response mentioning the fact that the document content was base-64 encoded, even when neither the user nor the system prompt asked about encodings.  

