---
title: Build a chat application with Open Web UI
titleSuffix: Foundry Local
description: Learn how to create a chat application using Foundry Local and Open Web UI
manager: scottpolly
keywords: Azure AI services, cognitive, AI models, local inference
ms.service: azure-ai-foundry
ms.topic: tutorial
ms.date: 02/20/2025
ms.reviewer: samkemp
ms.author: samkemp
author: samuel100
ms.custom: build-2025
#customer intent: As a developer, I want to get started with Foundry Local so that I can run AI models locally.
---

# Build a chat application with Open Web UI

This tutorial shows you how to create a chat application using Foundry Local and Open Web UI. When you finish, you'll have a working chat interface running entirely on your local device.

## Prerequisites

Before you start this tutorial, you need:

- **Foundry Local** [installed](../get-started.md) on your computer.
- **At least one model loaded** with the `foundry model load` command, like this:
  ```bash
  foundry model load Phi-4-mini-gpu-int4-rtn-block-32
  ```

## Set up Open Web UI for chat

1. **Install Open Web UI** by following the instructions from the [Open Web UI GitHub repository](https://github.com/open-webui/open-webui).

2. **Launch Open Web UI** with this command in your terminal:
   ```bash
   open-webui serve
   ```

3. Open your web browser and go to [http://localhost:8080](http://localhost:8080).

4. **Connect Open Web UI to Foundry Local**:

   - Click **Settings** in the navigation menu
   - Select **Connections**
   - Click **Manage Direct Connections**
   - Click the **+** icon to add a connection
   - Enter `http://localhost:5272/v1` for the URL
   - Type any value (like `test`) for the API Key, since it cannot be empty
   - Save your connection

5. **Start chatting with your model**:
   - Your loaded models will appear in the dropdown at the top
   - Select any model from the list
   - Type your message in the input box at the bottom

That's it! You're now chatting with an AI model running entirely on your local device.

## Next steps

- Try [different models](../how-to/manage.md) to compare performance and capabilities
