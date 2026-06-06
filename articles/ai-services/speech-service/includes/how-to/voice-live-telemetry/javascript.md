---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 04/28/2026
ms.author: pafarley
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/voice-live-javascript.md)]

## Additional prerequisites

- `@azure/ai-voicelive` package version 1.0.0 or later.
- Node.js version 18 or later.
- Install the telemetry dependencies:

  ```bash
  npm install @opentelemetry/api @opentelemetry/sdk-trace-node @azure/core-tracing
  ```

  For Azure Monitor export, install instead:

  ```bash
  npm install @azure/monitor-opentelemetry-exporter
  ```

  For browser-based applications, use `@opentelemetry/sdk-trace-web` instead of `@opentelemetry/sdk-trace-node`.

## Enable console tracing

Add the following code to your application before constructing the `VoiceLiveClient`. You first register an OpenTelemetry provider, then bridge `@azure/core-tracing` into OpenTelemetry via `useInstrumenter()` so the SDK emits spans.

:::code language="javascript" source="~/voice-live-samples-code/javascript/voice-live-quickstarts/TelemetryQuickstart/telemetry-console.js" id="enable_console_tracing":::

All connect, send, and receive operations now produce spans printed to stdout.

> [!NOTE]
> The samples in this article use `useInstrumenter()` for ESM compatibility. If your app is CommonJS, you can use the standard `createAzureSdkInstrumentation()` from `@azure/opentelemetry-instrumentation-azure-sdk` instead.

Reference: [NodeTracerProvider](https://open-telemetry.github.io/opentelemetry-js/classes/_opentelemetry_sdk_trace_node.NodeTracerProvider.html) | [VoiceLiveClient](/javascript/api/@azure/ai-voicelive/voiceliveclient)

> [!div class="nextstepaction"]
> [Complete console tracing sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/javascript/voice-live-quickstarts/TelemetryQuickstart/telemetry-console.js)

## Export traces to Azure Monitor

To send traces to Application Insights instead of the console, replace the console exporter with `AzureMonitorTraceExporter`. Set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable, then add the following code.

:::code language="javascript" source="~/voice-live-samples-code/javascript/voice-live-quickstarts/TelemetryQuickstart/telemetry-azure-monitor.js" id="enable_azure_monitor_tracing":::

View the results in the **Tracing** tab in your Foundry project page or in Application Insights.

Reference: [AzureMonitorTraceExporter](/javascript/api/@azure/monitor-opentelemetry-exporter/azuremonitortraceexporter)

> [!div class="nextstepaction"]
> [Complete Azure Monitor tracing sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/javascript/voice-live-quickstarts/TelemetryQuickstart/telemetry-azure-monitor.js)

## Add custom span attributes

To correlate Voice Live traces with your application context (session IDs, user IDs, or request identifiers), implement a custom `SpanProcessor` that adds attributes when each span starts.

:::code language="javascript" source="~/voice-live-samples-code/javascript/voice-live-quickstarts/TelemetryQuickstart/telemetry-custom-attributes.js" id="custom_span_processor":::

Register the custom processor with the tracer provider before registering it:

:::code language="javascript" source="~/voice-live-samples-code/javascript/voice-live-quickstarts/TelemetryQuickstart/telemetry-custom-attributes.js" id="add_custom_processor":::

Reference: [SpanProcessor](https://open-telemetry.github.io/opentelemetry-js/interfaces/_opentelemetry_sdk_trace_base.SpanProcessor.html)

> [!div class="nextstepaction"]
> [Complete custom attributes sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/javascript/voice-live-quickstarts/TelemetryQuickstart/telemetry-custom-attributes.js)

## Enable browser tracing

For browser-based applications, use `WebTracerProvider` instead of `NodeTracerProvider`. The same `useInstrumenter()` bridge applies. Spans can be exported to an in-page element, the browser console, or any OpenTelemetry-compatible backend.

:::code language="javascript" source="~/voice-live-samples-code/javascript/voice-live-quickstarts/TelemetryQuickstart/telemetry-browser.js" id="enable_browser_tracing":::

> [!NOTE]
> Browsers don't support `DefaultAzureCredential`. Use `AzureKeyCredential` or a bearer-token flow instead.

> [!div class="nextstepaction"]
> [Complete browser tracing sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/javascript/voice-live-quickstarts/TelemetryQuickstart/telemetry-browser.js)

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
> [Complete content recording sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/javascript/voice-live-quickstarts/TelemetryQuickstart/telemetry-content-recording.js)
