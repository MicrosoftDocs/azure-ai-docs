---
title: "How to use block lists in Microsoft Foundry models (classic)"
description: "Learn how to use block lists with Azure OpenAI (classic)"
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/10/2026
author: PatrickFarley
ms.author: pafarley
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
ROBOTS: NOINDEX, NOFOLLOW
---

# How to use blocklists in Microsoft Foundry models (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/use-blocklists.md)

The [configurable content filters](/azure/ai-foundry/openai/how-to/content-filters) available in Azure OpenAI are sufficient for most content moderation needs. However, you might need to filter terms specific to your use case—such as competitor names, internal project names, or domain-specific sensitive terms. For this, you can create custom block lists that automatically filter content containing your specified terms.

In this article, you learn how to:

- Create and manage custom blocklists
- Add terms using exact match or regex patterns
- Apply blocklists to your content filters
- Test blocklist behavior with your deployments

[!INCLUDE [use-blocklists 1](../../../foundry/openai/includes/how-to-use-blocklists-1.md)]
