---
title: "Use the GPT Realtime API via WebSockets"
description: "Learn how to use the GPT Realtime API for speech and audio via WebSockets."
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/29/2026
author: PatrickFarley
ms.author: pafarley
ms.custom:
  - references_regions
  - classic-and-new
  - doc-kit-assisted
recommendations: false
ai-usage: ai-assisted
---

# Use the GPT Realtime API via WebSockets

[!INCLUDE [realtime-audio-websockets 1](../includes/how-to-realtime-audio-websockets-1.md)]

## Prerequisites

Before you can use GPT real-time audio, you need:

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource. Create the resource in one of the [supported regions](#supported-models). For setup steps, see [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal).
- A deployment of a GPT realtime model in a supported region as described in the [supported models](#supported-models) section in this article.
  - In the Foundry portal, load your project. Select **Build** in the upper-right menu, then select the **Models** tab on the left pane, and select **Deploy a base model**. Search for the model you want, and select **Deploy** on the model page.
- **Required libraries**:
  - Python: `pip install websockets azure-identity`
  - JavaScript/Node.js: `npm install ws @azure/identity`

[!INCLUDE [realtime-audio-websockets 2](../includes/how-to-realtime-audio-websockets-2.md)]

## Connection and authentication

The Realtime API (via `/realtime`) is built on [the WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) to facilitate fully asynchronous streaming communication between the end user and model. 

The Realtime API is accessed via a secure WebSocket connection to the `/realtime` endpoint of your Azure OpenAI resource.

You can construct a full request URI by concatenating:

- The secure WebSocket (`wss://`) protocol.
- Your Azure OpenAI resource endpoint hostname, for example, `my-aoai-resource.openai.azure.com`
- The `openai/realtime` API path.
- A `model` query string parameter with the name of your `gpt-realtime`, `gpt-realtime-1.5`, or `gpt-realtime-mini` model deployment.
- **(Preview version only)** An `api-version` query string parameter for a supported API version such as `2025-04-01-preview` and a `deployment` query parameter instead of `model`.

The following example is a well-constructed `/realtime` request URI:

#### [GA version](#tab/ga)

```http
wss://my-eastus2-openai-resource.openai.azure.com/openai/v1/realtime?model=gpt-realtime-deployment-name
```

#### [Preview version](#tab/preview)

```http
wss://my-eastus2-openai-resource.openai.azure.com/openai/realtime?api-version=2025-04-01-preview&deployment=gpt-4o-mini-realtime-preview-deployment-name
```

---

> [!NOTE]
> The GA API uses `model=` as the query parameter name, while the preview API uses `deployment=`. Both refer to your deployed model name.

To authenticate:
- **Microsoft Entra** (recommended): Use token-based authentication with the `/realtime` API for an Azure OpenAI resource with managed identity enabled. Apply a retrieved authentication token using a `Bearer` token with the `Authorization` header.
- **API key**: An `api-key` can be provided in one of two ways:
  - Using an `api-key` connection header on the pre-handshake connection. This option isn't available in a browser environment.
  - Using an `api-key` query string parameter on the request URI. Query string parameters are encrypted when using HTTPS/WSS.

[!INCLUDE [realtime-audio-websockets 3](../includes/how-to-realtime-audio-websockets-3.md)]
