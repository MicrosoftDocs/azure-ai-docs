---
title: Include file
description: Include file
author: alexeyo26
ms.reviewer: sgilley
ms.author: alexeyo
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

The Azure OpenAI GPT Realtime API is now Generally Available (GA). This migration guide helps you update existing applications to use the GA protocol. The GA version introduces changes to SDK usage, endpoint URLs, event names, and session configuration.

**What's changing**: SDK packages, endpoint URL format, event names, and session configuration structure.

**What's not changing**: Core functionality, audio format support, and model capabilities.

**Time to migrate**: Most migrations take 30-60 minutes.

> [!IMPORTANT]
> The Preview version of the API is deprecated starting April 30, 2026. Migrate to the GA version before this date to avoid service disruption.

> [!NOTE]
> If you're building a new application, refer to the [Realtime API quickstart](../how-to/realtime-audio.md#quickstart) instead. This guide is only for migrating existing Preview applications to GA.

## Prerequisites

Before you begin the migration, verify you have:

- An existing Azure OpenAI resource with a Realtime API deployment that uses the Preview (Beta) protocol
- Access to the Azure portal with permissions to manage Azure OpenAI resources
- Ability to update SDK dependencies in your development environment
- A test environment where you can validate changes before deploying to production
- Understanding of your current implementation (WebSocket or WebRTC)
