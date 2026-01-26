---
title: Content Filter Severity Levels
description: Overview of risk categories for content filtering in Azure OpenAI, including hate, fairness, sexual, violence, and more.
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

# Content filter severity levels

Content filters ensure that AI-generated outputs align with ethical guidelines and safety standards. Azure OpenAI provides content filters to help identify and mitigate risks associated with various categories of harmful or inappropriate content. This article outlines the key risk categories and their descriptions to help you better understand the built-in content filters system.

Content filtering ensures that AI-generated outputs align with ethical guidelines and safety standards. Azure OpenAI provides content filtering capabilities to help identify and mitigate risks associated with various categories of harmful or inappropriate content. This article outlines the key risk categories and their descriptions to help you better understand the built-in content filtering system.

> [!NOTE]
> The text content filtering models for the hate, sexual, violence, and self-harm categories are specifically trained and tested on the following languages: English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. However, the service can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.


[!INCLUDE [severity-levels text, four-level](../../../ai-services/content-safety/includes/severity-levels-text-four.md)]

[!INCLUDE [severity-levels image](../../../ai-services/content-safety/includes/severity-levels-image.md)]
