---
title: 'Use the GPT Realtime API via WebSockets'
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Learn how to use the GPT Realtime API for speech and audio via WebSockets.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/29/2026
author: PatrickFarley
ms.author: pafarley
ms.custom: references_regions
recommendations: false
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted


---

# Use the GPT Realtime API via WebSockets

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Azure OpenAI GPT Realtime API for speech and audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. 

You can use the Realtime API via WebRTC, SIP, or WebSocket to send audio input to the model and receive audio responses in real time. 

Follow the instructions in this article to get started with the Realtime API via WebSockets. Use the Realtime API via WebSockets in server-to-server scenarios where low latency isn't a requirement.

> [!TIP] 
> In most cases, use the [Realtime API via WebRTC](./realtime-audio-webrtc.md) for real-time audio streaming in client-side applications such as a web application or mobile app. WebRTC is designed for low-latency, real-time audio streaming and is the best choice for most scenarios.

## Prerequisites

Before you can use GPT real-time audio, you need:


:::moniker range="foundry"
- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource. Create the resource in one of the [supported regions](#supported-models). For setup steps, see [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal).
- A deployment of the `gpt-4o-realtime-preview`, `gpt-4o-mini-realtime-preview`, `gpt-realtime`, `gpt-realtime-mini`, or `gpt-realtime-mini-2025-12-15` model in a supported region as described in the [supported models](#supported-models) section in this article.
  - In the Foundry portal, load your project. Select **Build** in the upper-right menu, then select the **Models** tab on the left pane, and select **Deploy a base model**. Search for the model you want, and select **Deploy** on the model page.
:::moniker-end

:::moniker range="foundry-classic"

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource created in a [supported region](#supported-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](create-resource.md).
- A deployment of the `gpt-4o-realtime-preview`, `gpt-4o-mini-realtime-preview`, `gpt-realtime`, `gpt-realtime-mini`, or `gpt-realtime-mini-2025-12-15` model in a supported region as described in the [supported models](#supported-models) section in this article. You can deploy the model from the [Foundry model catalog](../../../ai-foundry/how-to/model-catalog-overview.md) or from your project in the Foundry portal.
:::moniker-end

## Supported models

The GPT real-time models are available for global deployments in the [East US 2 and Sweden Central regions](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).
- `gpt-4o-mini-realtime-preview` (`2024-12-17`)
- `gpt-4o-realtime-preview` (`2024-12-17`)
- `gpt-realtime` (`2025-08-28`)
- `gpt-realtime-mini` (`2025-10-06`)
- `gpt-realtime-mini-2025-12-15` (`2025-12-15`)

For more information about supported models, see the [models and versions documentation](../../foundry-models/concepts/models-sold-directly-by-azure.md#audio-models).

## Connection and authentication

The Realtime API (via `/realtime`) is built on [the WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) to facilitate fully asynchronous streaming communication between the end user and model. 

The Realtime API is accessed via a secure WebSocket connection to the `/realtime` endpoint of your Azure OpenAI resource.

You can construct a full request URI by concatenating:

- The secure WebSocket (`wss://`) protocol.
- Your Azure OpenAI resource endpoint hostname, for example, `my-aoai-resource.openai.azure.com`
- The `openai/realtime` API path.
- A `deployment` query string parameter with the name of your `gpt-4o-realtime-preview`, `gpt-4o-mini-realtime-preview`, or `gpt-realtime` model deployment.
- **(Preview version only)** An `api-version` query string parameter for a supported API version such as `2025-04-01-preview`.

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

To authenticate:
- **Microsoft Entra** (recommended): Use token-based authentication with the `/realtime` API for an Azure OpenAI resource with managed identity enabled. Apply a retrieved authentication token using a `Bearer` token with the `Authorization` header.
- **API key**: An `api-key` can be provided in one of two ways:
  - Using an `api-key` connection header on the pre-handshake connection. This option isn't available in a browser environment.
  - Using an `api-key` query string parameter on the request URI. Query string parameters are encrypted when using HTTPS/WSS.

## Realtime API via WebSockets architecture

Once the WebSocket connection session to `/realtime` is established and authenticated, the functional interaction takes place via events for sending and receiving WebSocket messages. These events each take the form of a JSON object. 

:::image type="content" source="../media/how-to/real-time/realtime-api-sequence.png" alt-text="Diagram of the Realtime API authentication and connection sequence." lightbox="../media/how-to/real-time/realtime-api-sequence.png":::

<!--
sequenceDiagram
  actor User as End User
  participant MiddleTier as /realtime host
  participant AOAI as Azure OpenAI
  User->>MiddleTier: Begin interaction
  MiddleTier->>MiddleTier: Authenticate/Validate User
  MiddleTier--)User: audio information
  User--)MiddleTier: 
  MiddleTier--)User: text information
  User--)MiddleTier: 
  MiddleTier--)User: control information
  User--)MiddleTier: 
  MiddleTier->>AOAI: connect to /realtime
  MiddleTier->>AOAI: configure session
  AOAI->>MiddleTier: session start
  MiddleTier--)AOAI: send/receive WS commands
  AOAI--)MiddleTier: 
  AOAI--)MiddleTier: create/start conversation responses
  AOAI--)MiddleTier: (within responses) create/start/add/finish items
  AOAI--)MiddleTier: (within items) create/stream/finish content parts
-->

Events can be sent and received in parallel and applications should generally handle them both concurrently and asynchronously.

- A client-side caller establishes a connection to `/realtime`, which starts a new [`session`](../realtime-audio-reference.md#realtimerequestsession).
- A `session` automatically creates a default `conversation`. Multiple concurrent conversations aren't supported.
- The `conversation` accumulates input signals until a `response` is started, either via a direct event by the caller or automatically by voice activity detection (VAD).
- Each `response` consists of one or more `items`, which can encapsulate messages, function calls, and other information.
- Each message `item` has `content_part`, allowing multiple modalities (text and audio) to be represented across a single item.
- The `session` manages configuration of caller input handling (for example, user audio) and common output generation handling.
- Each caller-initiated [`response.create`](../realtime-audio-reference.md#realtimeclienteventresponsecreate) can override some of the output [`response`](../realtime-audio-reference.md#realtimeresponse) behavior, if desired.
- Server-created `item` and the `content_part` in messages can be populated asynchronously and in parallel. For example, receiving audio, text, and function information concurrently in a round robin fashion.

## Try the quickstart

Now that you've done the above steps, you can follow the instructions in the [Realtime API quickstart](../realtime-audio-quickstart.md) to get started with the Realtime API via WebSockets.

## Related content

* Try the [real-time audio quickstart](../realtime-audio-quickstart.md)
* See the [Realtime API reference](../realtime-audio-reference.md)
* Learn more about Azure OpenAI [quotas and limits](../quotas-limits.md)
