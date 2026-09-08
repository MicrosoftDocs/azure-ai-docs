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

Register a global `OpenTelemetry` instance with a span exporter before constructing the `VoiceLiveAsyncClient`. The SDK defaults to `GlobalOpenTelemetry.getOrNoop()`, so tracing is picked up automatically once a global instance exists.

```java
import com.azure.ai.voicelive.VoiceLiveAsyncClient;
import com.azure.ai.voicelive.VoiceLiveClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;
import io.opentelemetry.exporter.logging.LoggingSpanExporter;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.SimpleSpanProcessor;

// 1. Register a global OpenTelemetry instance BEFORE building any client.
SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
    .addSpanProcessor(SimpleSpanProcessor.create(LoggingSpanExporter.create()))
    .build();

OpenTelemetrySdk.builder()
    .setTracerProvider(tracerProvider)
    .buildAndRegisterGlobal();

// 2. Build the client — it picks up GlobalOpenTelemetry automatically.
String endpoint = System.getenv("AZURE_VOICELIVE_ENDPOINT");
VoiceLiveAsyncClient client = new VoiceLiveClientBuilder()
    .endpoint(endpoint)
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();
```

All connect, send, and receive operations now produce spans printed to stdout.

> [!TIP]
> If you attach the [OpenTelemetry Java agent](https://opentelemetry.io/docs/languages/java/automatic/) (`-javaagent:opentelemetry-javaagent.jar`), the global instance is registered automatically and no code changes are required.

Reference: [OpenTelemetry Java](https://opentelemetry.io/docs/languages/java/) | [VoiceLiveClientBuilder](/java/api/com.azure.ai.voicelive.voiceliveclientbuilder)

> [!div class="nextstepaction"]
> [Complete console tracing sample (GlobalTracingSample.java)](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/voicelive/azure-ai-voicelive/src/samples/java/com/azure/ai/voicelive/telemetry/GlobalTracingSample.java)

## Export traces to Azure Monitor

To send traces to Application Insights instead of the console, replace the logging exporter with the Azure Monitor exporter. Set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable, then add the following code.

```java
import com.azure.ai.voicelive.VoiceLiveAsyncClient;
import com.azure.ai.voicelive.VoiceLiveClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.monitor.opentelemetry.exporter.AzureMonitorExporterBuilder;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.BatchSpanProcessor;

String connectionString = System.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING");

SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
    .addSpanProcessor(BatchSpanProcessor.builder(
        new AzureMonitorExporterBuilder()
            .connectionString(connectionString)
            .buildTraceExporter())
        .build())
    .build();

OpenTelemetrySdk.builder()
    .setTracerProvider(tracerProvider)
    .buildAndRegisterGlobal();

String endpoint = System.getenv("AZURE_VOICELIVE_ENDPOINT");
VoiceLiveAsyncClient client = new VoiceLiveClientBuilder()
    .endpoint(endpoint)
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();
```

View the results in the **Tracing** tab in your Foundry project page or in Application Insights.

Reference: [Azure Monitor OpenTelemetry exporter for Java](/java/api/overview/azure/monitor-opentelemetry-exporter-readme)

## Add custom span attributes

To correlate Voice Live traces with your application context (session IDs, user IDs, or request identifiers), implement a custom `SpanProcessor` that adds attributes when each span starts.

```java
import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.context.Context;
import io.opentelemetry.sdk.trace.ReadWriteSpan;
import io.opentelemetry.sdk.trace.ReadableSpan;
import io.opentelemetry.sdk.trace.SpanProcessor;

final class CustomAttributesProcessor implements SpanProcessor {
    private final String sessionId;
    private final String userId;

    CustomAttributesProcessor(String sessionId, String userId) {
        this.sessionId = sessionId;
        this.userId = userId;
    }

    @Override
    public void onStart(Context parentContext, ReadWriteSpan span) {
        span.setAttribute(AttributeKey.stringKey("app.session_id"), sessionId);
        span.setAttribute(AttributeKey.stringKey("app.user_id"), userId);
    }

    @Override
    public boolean isStartRequired() { return true; }

    @Override
    public void onEnd(ReadableSpan span) { }

    @Override
    public boolean isEndRequired() { return false; }
}
```

Register the custom processor with the tracer provider before registering the global `OpenTelemetry` instance:

```java
SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
    .addSpanProcessor(new CustomAttributesProcessor("sess-123", "user-abc"))
    .addSpanProcessor(SimpleSpanProcessor.create(LoggingSpanExporter.create()))
    .build();

OpenTelemetrySdk.builder()
    .setTracerProvider(tracerProvider)
    .buildAndRegisterGlobal();
```

Reference: [OpenTelemetry Java](https://opentelemetry.io/docs/languages/java/)

## Enable content recording

Content recording captures full message payloads (send and receive) on span events. This is useful for debugging but can capture personal data.

> [!CAUTION]
> Content recording may capture personal data. Only enable in development or controlled environments.

Set the `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` environment variable to `true` before starting your application. No code changes are required.

```bash
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```

When enabled, the SDK attaches event payloads as `gen_ai.event.content` attributes on the corresponding spans.
