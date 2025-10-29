---
title: Content Filter Prompt Shields
description: Learn about prompt shield content in Azure OpenAI, including user prompt attacks and indirect attack severity definitions.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: conceptual
ms.date: 09/16/2025
ms.author: pafarley
---

# Prompt shields content filtering

Prompt shields are a feature of the Azure OpenAI content filtering system that helps detect and mitigate user prompt attacks. These attacks occur when a user attempts to manipulate the model's behavior by embedding harmful or inappropriate content within their input.

Prompt shields analyzes LLM inputs and detects adversarial user input attacks.

[!INCLUDE [prompt-shield-attack-info](../../../ai-services/content-safety/includes/prompt-shield-attack-info.md)]

## Spotlighting for prompt shields (preview)

Spotlighting is a feature that enhances protection against indirect attacks by tagging the input documents with special formatting to indicate lower trust to the model. When spotlighting is enabled, the service transforms the document content using base-64 encoding, and the model treats this content as less trustworthy than direct user and system prompts. This protection helps prevent the model from executing unintended commands or actions that are found in the content of the documents.

Spotlighting is turned off by default. You can enable it when [configuring their content filter](../how-to/content-filters.md) in the Azure AI Foundry portal or REST API. Spotlighting is only available for [models in the Chat Completions API](/azure/ai-foundry/openai/how-to/chatgpt).

There is no direct cost for spotlighting, but it adds more tokens to a user's prompt and to the system prompt, which could increase the total costs. Also note that spotlighting could make a lengthy document surpass the input size limit.

An occasional known side effect of spotlighting is the model response mentioning the fact that the document content was base-64 encoded, even when neither the user nor the system prompt asked about encodings.