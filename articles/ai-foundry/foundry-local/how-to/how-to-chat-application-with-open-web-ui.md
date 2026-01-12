---
title: Integrate Open WebUI with Foundry Local
titleSuffix: Foundry Local
description: Learn how to create a chat application using Foundry Local and Open WebUI
keywords: Foundry Tools, cognitive, AI models, local inference
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: how-to
ms.date: 01/06/2026
ms.author: jburchel
ms.reviewer: samkemp
author: jonburchel
reviewer: samuel100
ms.custom:
   - build-2025
   - dev-focus
ai-usage: ai-assisted
#customer intent: As a developer, I want to get started with Foundry Local so that I can run AI models locally.
---

# Integrate Open WebUI with Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

This article shows you how to create a chat application by using Foundry Local and Open WebUI. When you finish, you have a working chat interface that runs entirely on your local device.

## Prerequisites

Before you start, make sure you have the following prerequisites:

- **Foundry Local** installed on your computer. For installation instructions, see [Get started with Foundry Local](../get-started.md).
- **Open WebUI** installed. Follow the instructions in the [Open WebUI GitHub repository](https://github.com/open-webui/open-webui).
- **Azure RBAC**: Not applicable (runs locally).

## Start Foundry Local and verify the endpoint

1. **Start a model** (or confirm one is already running):

   ```bash
   foundry model run qwen2.5-0.5b
   ```

   Keep this terminal open.

   Reference: [Foundry Local CLI reference](../reference/reference-cli.md)

1. **Find your local service endpoint**. In a second terminal, run:

   ```bash
   foundry service status
   ```

   Copy the endpoint URL from the output. Foundry Local dynamically assigns a port each time the service starts.

   Reference: [Foundry Local CLI reference](../reference/reference-cli.md)

1. **Verify the REST server is reachable**. Run this command, replacing `PORT` with your endpoint port:

   ```bash
   curl http://localhost:PORT/openai/status
   ```

   A successful response is JSON that includes `Endpoints`, `ModelDirPath`, and `PipeName`.

   Reference: [Foundry Local REST API reference](../reference/reference-rest.md)

## Set up Open WebUI for chat

1. **Install Open WebUI** by following the instructions from the [Open WebUI GitHub repository](https://github.com/open-webui/open-webui).

1. **Launch Open WebUI** by using this command in your terminal:

   ```bash
   open-webui serve
   ```

   Reference: [Open WebUI GitHub repository](https://github.com/open-webui/open-webui)

1. Open your web browser and go to [http://localhost:8080](http://localhost:8080).

1. Enable Direct Connections:
   1. Select **Settings** and **Admin Settings** in the profile menu.
   1. Select **Connections** in the navigation menu.
   1. Enable **Direct Connections** by turning on the toggle. This setting allows users to connect to their own OpenAI compatible API endpoints.

1. **Connect Open WebUI to Foundry Local**:

   1. Select **Settings** in the profile menu.
   1. Select **Connections** in the navigation menu.
   1. Select **+** by **Manage Direct Connections**.
   1. For the **URL**, enter `http://localhost:PORT/v1` where `PORT` is the port from `foundry service status` (for example, `http://localhost:5272/v1`). Foundry Local dynamically assigns a port, so it isn't always the same.
   1. For the **Auth**, select **None**.
   1. Select **Save**.

1. **Start chatting with your model**:
   1. Confirm your loaded models appear in the dropdown at the top.
   1. Select a model from the list.
   1. Type your message in the input box at the bottom.

That's it! You're now chatting with an AI model running entirely on your local device.

## Troubleshooting

- If `foundry service status` reports an error, run `foundry service restart` and try again.
- If no models appear in Open WebUI, start a model with `foundry model run <model>` and then reload Open WebUI.
- If Open WebUI doesn't connect, confirm you're using the current port from `foundry service status`.

## Next steps

- [Use chat completions via REST server with Foundry Local](how-to-integrate-with-inference-sdks.md)
- [Compile Hugging Face models to run on Foundry Local](../how-to/how-to-compile-hugging-face-models.md)
