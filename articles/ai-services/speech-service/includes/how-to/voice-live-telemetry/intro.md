---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 04/28/2026
ms.author: pafarley
---

The Voice Live SDK includes built-in [OpenTelemetry](https://opentelemetry.io/) instrumentation that automatically traces connection, send, and receive operations. Use telemetry to monitor session health, diagnose latency issues, and correlate Voice Live operations with your application traces.

## What gets traced

When you enable telemetry, the SDK automatically creates OpenTelemetry spans for:

| Operation | Span name prefix | Description |
|---|---|---|
| WebSocket connect | `connect` | Connection establishment and lifecycle |
| Send events | `send` | Session updates, conversation items, response requests |
| Receive events | `recv` | Server events including responses, VAD, and errors |

## Prerequisites

- A working Voice Live setup. Complete one of the following quickstarts:
  - [Voice Live with Foundry models](../../../voice-live-quickstart.md)
  - [Voice Live with Foundry agents](../../../voice-live-agents-quickstart.md)
