---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 04/28/2026
ms.author: pafarley
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/voice-live-csharp.md)]

## Additional prerequisites

- `Azure.AI.VoiceLive` package version 1.1.0 or later.
- .NET 10.0 or later.
- Install the telemetry dependencies:

  ```dotnetcli
  dotnet add package OpenTelemetry
  dotnet add package OpenTelemetry.Exporter.Console
  ```

  For Azure Monitor export, install instead:

  ```dotnetcli
  dotnet add package Azure.Monitor.OpenTelemetry.Exporter
  ```

## Enable console tracing

Add the following code to your application before constructing the `VoiceLiveClient`. The SDK emits spans automatically when an OpenTelemetry provider is registered for the `Azure.AI.VoiceLive` source.

:::code language="csharp" source="~/voice-live-samples-code/csharp/voice-live-quickstarts/TelemetryQuickstart/telemetry-console.cs" id="enable_console_tracing":::

All connect, send, and receive operations now produce spans printed to stdout.

Reference: [TracerProviderBuilder](/dotnet/api/opentelemetry.tracerproviderbuilder) | [VoiceLiveClient](/dotnet/api/azure.ai.voicelive.voiceliveclient)

> [!div class="nextstepaction"]
> [Complete console tracing sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/csharp/voice-live-quickstarts/TelemetryQuickstart/telemetry-console.cs)

## Export traces to Azure Monitor

To send traces to Application Insights instead of the console, replace the console exporter with the Azure Monitor exporter. Set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable, then add the following code.

:::code language="csharp" source="~/voice-live-samples-code/csharp/voice-live-quickstarts/TelemetryQuickstart/telemetry-azure-monitor.cs" id="enable_azure_monitor_tracing":::

View the results in the **Tracing** tab in your Foundry project page or in Application Insights.

Reference: [AddAzureMonitorTraceExporter](/dotnet/api/azure.monitor.opentelemetry.exporter.azuremonitorexporterextensions.addazuremonitortraceexporter)

> [!div class="nextstepaction"]
> [Complete Azure Monitor tracing sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/csharp/voice-live-quickstarts/TelemetryQuickstart/telemetry-azure-monitor.cs)

## Add custom span attributes

To correlate Voice Live traces with your application context (session IDs, user IDs, or request identifiers), create a custom processor that derives from `BaseProcessor<Activity>`.

:::code language="csharp" source="~/voice-live-samples-code/csharp/voice-live-quickstarts/TelemetryQuickstart/telemetry-custom-attributes.cs" id="custom_span_processor":::

Register the custom processor with the tracer provider builder after adding the `Azure.AI.VoiceLive` source:

:::code language="csharp" source="~/voice-live-samples-code/csharp/voice-live-quickstarts/TelemetryQuickstart/telemetry-custom-attributes.cs" id="add_custom_processor":::

Reference: [BaseProcessor&lt;T&gt;](/dotnet/api/opentelemetry.baseprocessor-1) | [AddProcessor](/dotnet/api/opentelemetry.trace.tracerproviderbuilderextensions.addprocessor)

> [!div class="nextstepaction"]
> [Complete custom attributes sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/csharp/voice-live-quickstarts/TelemetryQuickstart/telemetry-custom-attributes.cs)

## Enable content recording

Content recording captures full message payloads (send and receive) on span events. This is useful for debugging but can capture personal data.

> [!CAUTION]
> Content recording may capture personal data. Only enable in development or controlled environments.

Set the `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` environment variable to `true` before starting your application. No code changes are required.

```bash
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```

When enabled, the SDK attaches event payloads as `gen_ai.event.content` attributes on the corresponding spans.

> [!div class="nextstepaction"]
> [Complete content recording sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/csharp/voice-live-quickstarts/TelemetryQuickstart/telemetry-content-recording.cs)
