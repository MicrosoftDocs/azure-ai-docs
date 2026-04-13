---
title: Include file
description: Include file
author: ssalgadodev
ms.reviewer: sgilley
ms.author: ssalgado
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

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
- [Configure content filtering in Azure OpenAI](../../../foundry-classic/openai/how-to/content-filters.md)
- [Content Safety concepts](../../../ai-services/content-safety/concepts/harm-categories.md)
