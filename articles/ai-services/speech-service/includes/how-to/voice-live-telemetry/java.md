---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 04/28/2026
ms.author: pafarley
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/voice-live-java.md)]

## Additional prerequisites

- `azure-ai-voicelive` package version 1.0.0 or later.
- Java Development Kit (JDK) version 8 or later.
- Add the OpenTelemetry dependencies to your `pom.xml`:

  ```xml
  <dependency>
      <groupId>io.opentelemetry</groupId>
      <artifactId>opentelemetry-sdk</artifactId>
      <version>1.45.0</version>
  </dependency>
  <dependency>
      <groupId>io.opentelemetry</groupId>
      <artifactId>opentelemetry-exporter-logging</artifactId>
      <version>1.45.0</version>
  </dependency>
  ```

  For Azure Monitor export, add:

  ```xml
  <dependency>
      <groupId>com.azure</groupId>
      <artifactId>azure-monitor-opentelemetry-exporter</artifactId>
      <version>1.0.0-beta.31</version>
  </dependency>
  ```

## Enable console tracing

Register a global `OpenTelemetry` instance with a console-style span exporter before constructing the `VoiceLiveAsyncClient`. The SDK defaults to `GlobalOpenTelemetry.getOrNoop()`, so tracing is picked up automatically once a global instance exists.

:::code language="java" source="~/voice-live-samples-code/java/voice-live-quickstarts/TelemetryQuickstart/src/main/java/TelemetryConsole.java" id="enable_console_tracing":::

All connect, send, and receive operations now produce spans printed to stdout.

> [!TIP]
> If you attach the [OpenTelemetry Java agent](https://opentelemetry.io/docs/languages/java/automatic/) (`-javaagent:opentelemetry-javaagent.jar`), the global instance is registered automatically and no code changes are required.

Reference: [OpenTelemetrySdk](https://www.javadoc.io/doc/io.opentelemetry/opentelemetry-sdk/latest/io/opentelemetry/sdk/OpenTelemetrySdk.html) | [VoiceLiveClientBuilder](/java/api/com.azure.ai.voicelive.voiceliveclientbuilder)

> [!div class="nextstepaction"]
> [Complete console tracing sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/java/voice-live-quickstarts/TelemetryQuickstart/src/main/java/TelemetryConsole.java)

## Export traces to Azure Monitor

To send traces to Application Insights instead of the console, replace the console exporter with `AzureMonitorExporterBuilder`. Set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable, then add the following code.

:::code language="java" source="~/voice-live-samples-code/java/voice-live-quickstarts/TelemetryQuickstart/src/main/java/TelemetryAzureMonitor.java" id="enable_azure_monitor_tracing":::

View the results in the **Tracing** tab in your Foundry project page or in Application Insights.

Reference: [AzureMonitorExporterBuilder](/java/api/com.azure.monitor.opentelemetry.exporter.azuremonitorexporterbuilder)

> [!div class="nextstepaction"]
> [Complete Azure Monitor tracing sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/java/voice-live-quickstarts/TelemetryQuickstart/src/main/java/TelemetryAzureMonitor.java)

## Add custom span attributes

To correlate Voice Live traces with your application context (session IDs, user IDs, or request identifiers), implement a custom `SpanProcessor` that adds attributes when each span starts.

:::code language="java" source="~/voice-live-samples-code/java/voice-live-quickstarts/TelemetryQuickstart/src/main/java/TelemetryCustomAttributes.java" id="custom_span_processor":::

Register the custom processor with the tracer provider before registering the global `OpenTelemetry` instance:

:::code language="java" source="~/voice-live-samples-code/java/voice-live-quickstarts/TelemetryQuickstart/src/main/java/TelemetryCustomAttributes.java" id="add_custom_processor":::

Reference: [SpanProcessor](https://www.javadoc.io/doc/io.opentelemetry/opentelemetry-sdk-trace/latest/io/opentelemetry/sdk/trace/SpanProcessor.html) | [SdkTracerProvider](https://www.javadoc.io/doc/io.opentelemetry/opentelemetry-sdk-trace/latest/io/opentelemetry/sdk/trace/SdkTracerProvider.html)

> [!div class="nextstepaction"]
> [Complete custom attributes sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/java/voice-live-quickstarts/TelemetryQuickstart/src/main/java/TelemetryCustomAttributes.java)

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
> [Complete content recording sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/java/voice-live-quickstarts/TelemetryQuickstart/src/main/java/TelemetryContentRecording.java)
