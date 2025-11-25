---
title: Integrate Open WebUI with Foundry Local
titleSuffix: Foundry Local
description: Learn how to create a chat application using Foundry Local and Open WebUI
keywords: Foundry Tools, cognitive, AI models, local inference
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: how-to
ms.date: 09/24/2025
ms.author: jburchel
ms.reviewer: samkemp
author: jonburchel
reviewer: samuel100
ms.custom: build-2025
#customer intent: As a developer, I want to get started with Foundry Local so that I can run AI models locally.
---

# Integrate Open WebUI with Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

This tutorial shows you how to create a chat application using Foundry Local and Open WebUI. When you finish, you have a working chat interface running entirely on your local device.

## Prerequisites

Before you start this tutorial, you need:

- **Foundry Local** installed on your computer. Read the [Get started with Foundry Local](../get-started.md) guide for installation instructions.

## Set up Open WebUI for chat

1. **Install Open WebUI** by following the instructions from the [Open WebUI GitHub repository](https://github.com/open-webui/open-webui).

1. **Launch Open WebUI** with this command in your terminal:

   ```bash
   open-webui serve
   ```

1. Open your web browser and go to [http://localhost:8080](http://localhost:8080).

1. Enable Direct Connections:
   1. Select **Settings** and **Admin Settings** in the profile menu.
   1. Select **Connections** in the navigation menu.
   1. Enable **Direct Connections** by turning on the toggle. This allows users to connect to their own OpenAI compatible API endpoints.

1. **Connect Open WebUI to Foundry Local**:

   1. Select **Settings** in the profile menu.
   1. Select **Connections** in the navigation menu.
   1. Select **+** by **Manage Direct Connections**.
   1. For the **URL**, enter `http://localhost:PORT/v1` where `PORT` is the Foundry Local endpoint port (use the CLI command `foundry service status` to find it). Note that Foundry Local dynamically assigns a port, so it isn't always the same.
   1. For the **Auth**, select **None**.
   1. Select **Save**

1. **Start chatting with your model**:
   1. Your loaded models appear in the dropdown at the top
   1. Select any model from the list
   1. Type your message in the input box at the bottom

That's it! You're now chatting with an AI model running entirely on your local device.

## Next steps

- [Use chat completions via REST server with Foundry Local](how-to-integrate-with-inference-sdks.md)
- [Compile Hugging Face models to run on Foundry Local](../how-to/how-to-compile-hugging-face-models.md)
