---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

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

Now that you've done the above steps, you can follow the instructions in the [Realtime API quickstart](../how-to/realtime-audio.md#quickstart) to get started with the Realtime API via WebSockets.

## Related content

* Try the [real-time audio quickstart](../how-to/realtime-audio.md#quickstart)
* See the [Realtime API reference](../realtime-audio-reference.md)
* Learn more about Azure OpenAI [quotas and limits](../quotas-limits.md)
