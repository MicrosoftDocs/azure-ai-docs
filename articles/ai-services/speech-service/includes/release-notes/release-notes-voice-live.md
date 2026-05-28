---
author: PatrickFarley
reviewer: patrickfarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 02/20/2026
ms.author: pafarley
ai-usage: ai-assisted
---

### May 2026 release

The Voice Live evaluation harness is available in preview. Evaluate the quality of your Voice Live voice agents by running pre-recorded audio through different session configurations and scoring responses with Microsoft Foundry built-in evaluators. For more information, see [How to evaluate Voice Live agents](../../how-to-voice-live-evaluate.md).

### April 2026 release

Voice Live API version `2026-04-10` is available, adding new generally available features and preview capabilities. For the full API reference, see [Voice Live API Reference 2026-04-10](../../voice-live-api-reference-2026-04-10.md).

The following previously preview features are now generally available:
- [Proactive messages](../../how-to-voice-live-proactive-messages.md) — allow your voice agent to speak first before user interaction.
- [Auto-truncation](../../how-to-voice-live-auto-truncation.md) — handle voice interruptions in chat history.
- [MCP server integration](../../how-to-voice-live-mcp-server.md) — add Model Context Protocol servers to Voice Live sessions.
- [Voice Agent integration with Foundry Agent Service](../../how-to-voice-agent-integration.md) — build real-time voice agents with Foundry Agent Service.
- Java and JavaScript SDK support.

New GA feature:
- [Telemetry and tracing](../../how-to-voice-live-telemetry.md) — built-in OpenTelemetry instrumentation for monitoring Voice Live sessions.

New preview feature:
- [MAI Transcribe-1](../../mai-transcribe.md) is available in preview as a speech recognition model option for Voice Live.

Updated GA SDK versions:
- Python `azure-ai-voicelive` 1.2.0
- C# `Azure.AI.VoiceLive` 1.1.0
- Java `azure-ai-voicelive` 1.0.0
- JavaScript `@azure/ai-voicelive` 1.0.0

### February 2026 release

Voice Agent integration with Foundry Agent Service is available in preview with SDK support for Python, Java, C#, and JavaScript. Build real-time voice agents with the new quickstart and how-to guidance. For more information, see [Get started with Voice Live and Foundry Agent Service](../../voice-live-agents-quickstart.md) and [How to build a voice agent](../../how-to-voice-agent-integration.md).

New how-to guides are available:
- [Improve tool calling and latency wait times with interim responses](../../how-to-voice-live-interim-response.md)
- [Add proactive messages](../../how-to-voice-live-proactive-messages.md)
- [Handle voice interruptions in chat history](../../how-to-voice-live-auto-truncation.md)

### January 2026 release

The Voice Live API Reference `2026-01-01-preview` is available in preview, with updated event and configuration coverage for Voice Live sessions. For more information, see [Voice Live API Reference 2026-01-01-preview](../../voice-live-api-reference-2026-01-01-preview.md).

### November 2025

The Voice Live API is generally available. Transform conversations into seamless experiences with Voice Live API—the all-in-one solution that combines speech recognition, generative AI, and text-to-speech into a single low-latency interface for building intelligent voice agents. For more information, see [Voice Live](../../voice-live.md).
