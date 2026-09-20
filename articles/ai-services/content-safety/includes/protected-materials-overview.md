---
title: "Protected Material overview include"
description: "Details about Protected material detection."
author: ssalgadodev
ms.date: 09/08/2026
ms.topic: include
ms.author: ssalgado
---

The protected material detection filter scans the output of large language models (LLMs) to identify and flag known protected material. It helps organizations prevent the generation of content that closely matches copyrighted text or code.

The protected material text filter flags known text content that large language models might output, such as song lyrics, articles, recipes, and selected web content.

The protected material code filter flags protected code content that large language models might output. This content comes from known GitHub repositories and includes software libraries, source code, algorithms, and other proprietary programming content.

> [!IMPORTANT]
> Protected material detection works with English only.

[!INCLUDE [protected-material-examples](./protected-material-examples.md)]

## Troubleshooting

### False positives

If protected material detection flags content that isn't actually protected:

- Verify the detection category (lyrics, news, recipes, code) matches your use case.
- Check if the flagged content exceeds the character or word thresholds (40 characters for recipes, 200 characters for news, 11 words for lyrics).
- Review the "Considered acceptable" criteria in the detection categories table.

### Content not detected

If the system doesn't flag the expected protected material:

- For code: Verify the repository was indexed before April 6, 2023.
- For text: Confirm the content matches one of the four detection categories (Recipes, Web Content, News, Lyrics).
- Check that language support requirements are met (English).
