---
title: "Protected Material Detection Filter (classic)"
description: "Learn about the Protected Material Detection Filter for identifying and flagging known protected text and code content in large language model outputs. (classic)"
author: ssalgadodev
ms.author: ssalgado
ms.date: 11/05/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
ROBOTS: NOINDEX, NOFOLLOW
---

# Protected material detection filter (classic)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

The protected material detection filter scans the output of large language models (LLMs) to identify and flag known protected material. It helps organizations prevent the generation of content that closely matches copyrighted text or code.

The protected material text filter flags known text content that large language models might output, such as song lyrics, articles, recipes, and selected web content.

The protected material code filter flags protected code content that large language models might output. This is content found in known GitHub repositories and includes software libraries, source code, algorithms, and other proprietary programming content.

> [!IMPORTANT]
> The content filtering models for protected material detection, groundedness detection, and custom categories (standard) work with English only.
> 
> Other content filtering models are specifically trained and tested on the following languages: Chinese, English, French, German, Spanish, Italian, Japanese, Portuguese. However, these features can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.

[!INCLUDE [protected-material-examples](../../../ai-services/content-safety/includes/protected-material-examples.md)]
