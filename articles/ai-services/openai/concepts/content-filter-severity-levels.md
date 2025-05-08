---
title: Content Filter Severity Levels
description: Overview of risk categories for content filtering in Azure OpenAI, including hate, fairness, sexual, violence, and more.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 05/07/2025
ms.author: pafarley
---

# Content filtering severity levels

<!--
Text and image models support Drugs as an additional classification. This category covers advice related to Drugs and depictions of recreational and non-recreational drugs.
-->

Content filtering ensures that AI-generated outputs align with ethical guidelines and safety standards. Azure OpenAI provides content filtering capabilities to help identify and mitigate risks associated with various categories of harmful or inappropriate content. This document outlines the key risk categories and their descriptions to help you better understand the built-in content filtering system.

> [!NOTE]
> The text content filtering models for the hate, sexual, violence, and self-harm categories have been specifically trained and tested on the following languages: English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. However, the service can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.


[!INCLUDE [severity-levels text, four-level](../../content-safety/includes/severity-levels-text-four.md)]

[!INCLUDE [severity-levels image](../../content-safety/includes/severity-levels-image.md)]