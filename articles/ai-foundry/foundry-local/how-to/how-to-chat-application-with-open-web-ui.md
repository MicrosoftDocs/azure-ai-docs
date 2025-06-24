---
title: Integrate Open Web UI with Foundry Local
titleSuffix: Foundry Local
description: Learn how to create a chat application using Foundry Local and Open Web UI
manager: scottpolly
keywords: Azure AI services, cognitive, AI models, local inference
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: how-to
ms.date: 02/20/2025
ms.reviewer: samkemp
ms.author: jburchel
ms.reviewer: samkemp
author: jonburchel
reviewer: samuel100
ms.custom: build-2025
#customer intent: As a developer, I want to get started with Foundry Local so that I can run AI models locally.
---

# Integrate Open Web UI with Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

This tutorial shows you how to create a chat application using Foundry Local and Open Web UI. When you finish, you have a working chat interface running entirely on your local device.

## Prerequisites

Before you start this tutorial, you need:

- **Foundry Local** installed on your computer. Read the [Get started with Foundry Local](../get-started.md) guide for installation instructions.

## Set up Open Web UI for chat

1. **Install Open Web UI** by following the instructions from the [Open Web UI GitHub repository](https://github.com/open-webui/open-webui).

2. **Launch Open Web UI** with this command in your terminal:

   ```bash
   open-webui serve
   ```

3. Open your web browser and go to [http://localhost:8080](http://localhost:8080).

4. **Connect Open Web UI to Foundry Local**:

   1. Select **Settings** in the navigation menu
   2. Select **Connections**
   3. Select **Manage Direct Connections**
   4. Select the **+** icon to add a connection
   5. For the **URL**, enter `http://localhost:PORT/v1` where `PORT` is replaced with the port of the Foundry Local endpoint, which you can find using the CLI command `foundry service status`. Note, that Foundry Local dynamically assigns a port, so it's not always the same.
   6. Type any value (like `test`) for the API Key, since it can't be empty.
   7. Save your connection

5. **Start chatting with your model**:
   1. Your loaded models appear in the dropdown at the top
   2. Select any model from the list
   3. Type your message in the input box at the bottom

That's it! You're now chatting with an AI model running entirely on your local device.

## Next steps

- [Integrate inferencing SDKs with Foundry Local](how-to-integrate-with-inference-sdks.md)
- [Compile Hugging Face models to run on Foundry Local](../how-to/how-to-compile-hugging-face-models.md)
