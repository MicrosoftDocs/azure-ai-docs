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

This guide describes the Azure OpenAI content streaming experience and options. Customers can receive content from the API when it's generated, instead of waiting for chunks of content that have been verified to pass the content filters.

> [!NOTE]
> Asynchronous Filter configuration requires permission to modify content filtering policies in Foundry portal.

## Choose the right streaming mode

**Use Default streaming when:**
- Maximum safety and compliance are required
- You need immediate filtering before any content is displayed
- Your application cannot handle retroactive content removal
- Example: Customer-facing chatbots in regulated industries

**Use Asynchronous Filter when:**
- Low latency is critical to user experience
- You can implement client-side content redaction
- Your application has additional safety controls
- You're willing to handle delayed filtering signals
- Example: Internal development tools, creative writing assistants
