---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 04/28/2026
ms.author: pafarley
---

[!INCLUDE [Header](../../common/voice-live-python.md)]

## Additional prerequisites

- `azure-ai-voicelive` package version 1.2.0 or later.
- Install the telemetry dependencies:

  ```bash
  pip install opentelemetry-sdk azure-core-tracing-opentelemetry
  ```

  For Azure Monitor export, install instead:

  ```bash
  pip install azure-monitor-opentelemetry
  ```

## Enable console tracing

Add the following code to your application before calling `connect()`. This is the smallest code change to start seeing Voice Live spans in your terminal.

:::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/TelemetryQuickstart/telemetry-console.py" id="enable_console_tracing":::

All `connect`, `send`, and `recv` operations now produce spans printed to stdout.

> [!div class="nextstepaction"]
> [Complete console tracing sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/python/voice-live-quickstarts/TelemetryQuickstart/telemetry-console.py)

## Export traces to Azure Monitor

To send traces to Application Insights instead of the console, replace the console setup with Azure Monitor configuration. Set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable, then add the following code.

:::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/TelemetryQuickstart/telemetry-azure-monitor.py" id="enable_azure_monitor_tracing":::

View the results in the **Tracing** tab in your Azure AI Foundry project page or in Application Insights.

> [!div class="nextstepaction"]
> [Complete Azure Monitor tracing sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/python/voice-live-quickstarts/TelemetryQuickstart/telemetry-azure-monitor.py)

## Add custom span attributes

To correlate Voice Live traces with your application context (session IDs, user IDs, or request identifiers), create a custom `SpanProcessor`.

:::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/TelemetryQuickstart/telemetry-custom-attributes.py" id="custom_span_processor":::

Register the custom processor with the global tracer provider after your standard telemetry setup:

:::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/TelemetryQuickstart/telemetry-custom-attributes.py" id="add_custom_processor":::

> [!div class="nextstepaction"]
> [Complete custom attributes sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/python/voice-live-quickstarts/TelemetryQuickstart/telemetry-custom-attributes.py)

## Enable content recording

Content recording captures full message payloads (send and receive) in span events as `gen_ai.event.content` attributes. This is useful for debugging but can capture personal data.

> [!CAUTION]
> Content recording may capture personal data. Only enable in development or controlled environments.

:::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/TelemetryQuickstart/telemetry-content-recording.py" id="enable_content_recording":::

> [!div class="nextstepaction"]
> [Complete content recording sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/python/voice-live-quickstarts/TelemetryQuickstart/telemetry-content-recording.py)
