---
title: "Deploy and use Claude models in Microsoft Foundry (classic)"
description: "Deploy Anthropic's Claude models in Microsoft Foundry to integrate advanced conversational AI into your apps. Learn how to use Claude Opus, Sonnet, and Haiku models. (classic)"
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 03/11/2026
ms.custom:
  - ignite-2024, dev-focus, pilot-ai-workflow-jan-2026
  - classic-and-new
author: msakande
ms.author: mopeakande
ms.reviewer: ambadal
reviewer: AmarBadal
ai-usage: ai-assisted

#CustomerIntent: As a developer or AI practitioner, I want to deploy and use Claude models in Microsoft Foundry so I can integrate advanced conversational AI capabilities into my applications. 
ROBOTS: NOINDEX, NOFOLLOW
---

# Deploy and use Claude models in Microsoft Foundry (preview) (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/foundry-models/how-to/use-foundry-models-claude.md)

[!INCLUDE [use-foundry-models-claude 1](../../../foundry/foundry-models/includes/how-to-use-foundry-models-claude-1.md)]

## Responsible AI considerations

When using Claude models in Foundry, consider these responsible AI practices:

- Configure AI content safety during model inference, because Foundry doesn't provide built-in content filtering for Claude models at deployment time. To learn how to create and use content filters, see [Configure content filtering for Foundry Models](configure-content-filters.md).

- Ensure your applications comply with [Anthropic's Acceptable Use Policy](https://www.anthropic.com/legal/aup). Also, see details of safety evaluations for [Claude Opus 4.6](https://www.anthropic.com/claude-opus-4-6-system-card), [Claude Opus 4.5](http://www.anthropic.com/claude-opus-4-5-system-card), [Claude Opus 4.1](https://assets.anthropic.com/m/4c024b86c698d3d4/original/Claude-4-1-System-Card.pdf), [Claude Sonnet 4.6](https://www.anthropic.com/claude-sonnet-4-6-system-card), [Claude Sonnet 4.5](https://assets.anthropic.com/m/12f214efcc2f457a/original/Claude-Sonnet-4-5-System-Card.pdf), and [Claude Haiku 4.5](https://assets.anthropic.com/m/99128ddd009bdcb/Claude-Haiku-4-5-System-Card.pdf).

[!INCLUDE [use-foundry-models-claude 2](../../../foundry/foundry-models/includes/how-to-use-foundry-models-claude-2.md)]
