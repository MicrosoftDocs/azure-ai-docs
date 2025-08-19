---
title: Protected Material Detection Filter
description: Learn about the Protected Material Detection Filter for identifying and flagging known protected text and code content in large language model outputs.
author: PatrickFarley
ms.author: pafarley
ms.date: 05/08/2025
ms.topic: conceptual
ms.service: azure-ai-openai
---

# Protected material detection filter

The Protected material detection filter scans the output of large language models (LLMs) to identify and flag known protected material. It is designed to help organizations prevent the generation of content that closely matches copyrighted text or code.

The Protected material text filter flags known text content (for example, song lyrics, articles, recipes, and selected web content) that might be output by large language models.

The Protected material code filter flags protected code content (from known GitHub repositories, including software libraries, source code, algorithms, and other proprietary programming content) that might be output by large language models.

> [!IMPORTANT]
> The Contents Filter models for protected material, groundedness detection, and custom categories (standard) work with English only.
> 
> Other Contents Filter models have been specifically trained and tested on the following languages: Chinese, English, French, German, Spanish, Italian, Japanese, Portuguese. However, these features can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.

[!INCLUDE [protected-material-examples](../../../ai-services/content-safety/includes/protected-material-examples.md)]
