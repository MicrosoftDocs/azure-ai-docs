---
title: Content Filter Prompt Shields
description: Learn about prompt shield content in Azure OpenAI, including user prompt attacks and indirect attack severity definitions.
author: ssalgadodev
ms.author: ssalgado
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: conceptual
ms.date: 11/05/2025
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Prompt shields in Foundry

::: moniker range="foundry"

Prompt shields are a feature of the Microsoft Foundry Guardrails and controls system that helps detect and mitigate user prompt attacks. These attacks occur when a user attempts to manipulate the model's behavior by embedding harmful or inappropriate content within their input.

Prompt shields analyzes LLM inputs and detects adversarial user input attacks.

<!-- BEGIN [!INCLUDE [prompt-shield-attack-info](../../../ai-services/content-safety/includes/prompt-shield-attack-info.md)] -->

::: moniker-end

::: moniker range="foundry-classic"

Prompt shields are a feature of the Azure OpenAI content filtering system that helps detect and mitigate user prompt attacks. These attacks occur when a user attempts to manipulate the model's behavior by embedding harmful or inappropriate content within their input.

Prompt shields analyze LLM inputs and detects adversarial user input attacks.

<!-- BEGIN [!INCLUDE [prompt-shield-attack-info](../../../ai-services/content-safety/includes/prompt-shield-attack-info.md)] -->

::: moniker-end

## Spotlighting for prompt shields (preview)

Spotlighting is a feature that enhances protection against indirect attacks for models accessed through the Chat Completions API by tagging input documents with special formatting that indicates lower trust to the model.  
<!-- Clarified the scope to specify that spotlighting applies only to models used via the Chat Completions API. -->

When spotlighting is enabled, the service transforms document content using base-64 encoding so that the model treats it as less trustworthy than direct user and system prompts.  
<!-- Simplified wording and removed a marginal sentence that restated the section heading. -->

Spotlighting is turned off by default. You can enable it when configuring content filters in the Foundry portal or through the REST API. Spotlighting is only available for models used via the Chat Completions API.  
<!-- Reduced repetition and tightened the availability statement to clearly scope the feature. -->

There is no direct cost for spotlighting, but it adds tokens to user and system prompts, which can increase total costs. Spotlighting can also cause large documents to exceed input size limits.  
<!-- Streamlined explanation while preserving the original meaning. -->

A known side effect of spotlighting is that the model might mention that document content was base-64 encoded, even when encoding was not requested.  
<!-- Removed hedging language and shortened the sentence for clarity. -->