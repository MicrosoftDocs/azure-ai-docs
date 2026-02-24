---
title: Protected Material Detection Filter
description: Learn about the Protected Material Detection Filter for identifying and flagging known protected text and code content in large language model outputs.
author: ssalgadodev
ms.author: ssalgado
ms.date: 11/05/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Protected material detection filter


The protected material detection filter scans the output of large language models (LLMs) to identify and flag known protected material. It helps organizations prevent the generation of content that closely matches copyrighted text or code.

The protected material text filter flags known text content that large language models might output, such as song lyrics, articles, recipes, and selected web content.

The protected material code filter flags protected code content that large language models might output. This is content found in known GitHub repositories and includes software libraries, source code, algorithms, and other proprietary programming content.

::: moniker range="foundry"

> [!IMPORTANT]
> The Guardrails and controls models for protected material detection, groundedness detection, and custom categories (standard) work with English only.
> 
> Other content filtering models are specifically trained and tested on the following languages: Chinese, English, French, German, Spanish, Italian, Japanese, Portuguese. However, these features can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.

::: moniker-end

::: moniker range="foundry-classic"

> [!IMPORTANT]
> The content filtering models for protected material detection, groundedness detection, and custom categories (standard) work with English only.
> 
> Other content filtering models are specifically trained and tested on the following languages: Chinese, English, French, German, Spanish, Italian, Japanese, Portuguese. However, these features can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.

::: moniker-end

> [!TIP]
> To learn how to use protected material detection in your applications, see [Quickstart: Protected material for text](../../../ai-services/content-safety/quickstart-protected-material.md) and [Quickstart: Protected material for code](../../../ai-services/content-safety/quickstart-protected-material-code.md).

[!INCLUDE [protected-material-examples](../../../ai-services/content-safety/includes/protected-material-examples.md)]

## Troubleshooting

### False positives

If protected material detection flags content that isn't actually protected:

- Verify the detection category (lyrics, news, recipes, code) matches your use case
- Check if the flagged content exceeds the character/word thresholds (40 chars for recipes, 200 chars for news, 11 words for lyrics)
- Review the 'Considered acceptable' criteria in the detection categories table

### Content not being detected

If expected protected material isn't flagged:

- For code: Verify the repository was indexed before April 6, 2023
- For text: Confirm the content matches one of the four detection categories (Recipes, Web Content, News, Lyrics)
- Check that language support requirements are met (English for Guardrails models)

### Integration issues

For integration problems:

- Verify your Azure AI Content Safety resource is properly configured
- Check that API authentication credentials are valid
- Review the [Content Safety quickstart](../../../ai-services/content-safety/quickstart-text.md) for correct API usage

## Next steps

- [Quickstart: Detect protected material in text](../../../ai-services/content-safety/quickstart-protected-material.md)
- [Quickstart: Detect protected material in code](../../../ai-services/content-safety/quickstart-protected-material-code.md)
- [Configure content filtering in Azure OpenAI](../how-to/content-filters.md)
- [Content Safety concepts](../../../ai-services/content-safety/concepts/harm-categories.md)
