---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 04/28/2026
ms.author: pafarley
---

## Production best practices

- **Batch export**: Use `BatchSpanProcessor` instead of `SimpleSpanProcessor` in production to reduce overhead.
- **Sampling**: Configure a sampling strategy to control trace volume at scale.
- **Sensitive data**: Don't enable content recording in production. Message payloads can contain personal data.
- **Correlation**: Use custom span attributes to add session or user identifiers so you can filter traces in your observability backend.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| No spans appear | Missing `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING` env var | Set `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true` |
| No spans appear | `VoiceLiveInstrumentor().instrument()` not called | Call `instrument()` before `connect()` |
| Spans missing in Azure Monitor | Missing or invalid connection string | Verify `APPLICATIONINSIGHTS_CONNECTION_STRING` is set correctly |
| Spans appear in console but not in Azure Monitor | Using `ConsoleSpanExporter` instead of Azure Monitor | Switch to `configure_azure_monitor()` |
| Custom attributes missing | Processor registered after spans are created | Register the custom processor before calling `connect()` |
