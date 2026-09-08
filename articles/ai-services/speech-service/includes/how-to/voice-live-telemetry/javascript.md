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

First register an OpenTelemetry provider, then bridge `@azure/core-tracing` into OpenTelemetry via `useInstrumenter()` so the SDK emits spans. Add this code before constructing the `VoiceLiveClient`.

```javascript
import {
  NodeTracerProvider,
  SimpleSpanProcessor,
  ConsoleSpanExporter,
} from "@opentelemetry/sdk-trace-node";
import { useInstrumenter } from "@azure/core-tracing";
import { trace, context } from "@opentelemetry/api";
import { VoiceLiveClient } from "@azure/ai-voicelive";
import { DefaultAzureCredential } from "@azure/identity";

// 1. Configure OpenTelemetry with a console exporter.
const provider = new NodeTracerProvider({
  spanProcessors: [new SimpleSpanProcessor(new ConsoleSpanExporter())],
});
provider.register();

// 2. Bridge @azure/core-tracing into OpenTelemetry.
useInstrumenter({
  startSpan(name, spanOptions) {
    const ctx = spanOptions.tracingContext ?? context.active();
    const tracer = trace.getTracer(
      spanOptions.packageName ?? "@azure/ai-voicelive",
      spanOptions.packageVersion,
    );
    const span = tracer.startSpan(name, { attributes: spanOptions.spanAttributes, kind: 0 }, ctx);
    return {
      span: {
        end() { span.end(); },
        setStatus(s) {
          if (s.status === "error") span.setStatus({ code: 2, message: String(s.error ?? "") });
        },
        setAttribute(k, v) { span.setAttribute(k, v); },
        isRecording() { return span.isRecording(); },
        recordException(e) { span.recordException(e); },
      },
      tracingContext: trace.setSpan(ctx, span),
    };
  },
  withContext(ctx, fn, ...args) { return context.with(ctx, fn, undefined, ...args); },
  parseTraceparentHeader() { return undefined; },
  createRequestHeaders() { return {}; },
});

// 3. Use VoiceLive as normal — spans are emitted automatically.
const client = new VoiceLiveClient(
  process.env.AZURE_VOICELIVE_ENDPOINT,
  new DefaultAzureCredential(),
);
const session = client.createSession("gpt-realtime");
await session.connect();
```

All connect, send, and receive operations now produce spans printed to stdout.

> [!NOTE]
> The samples in this article use `useInstrumenter()` for ESM compatibility. If your app is CommonJS, you can use the standard `createAzureSdkInstrumentation()` from `@azure/opentelemetry-instrumentation-azure-sdk` instead.

Reference: [OpenTelemetry JavaScript SDK](https://opentelemetry.io/docs/languages/js/) | [VoiceLiveClient](/javascript/api/@azure/ai-voicelive/voiceliveclient)

> [!div class="nextstepaction"]
> [Complete console tracing sample](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/voicelive/ai-voicelive/samples/telemetry)

## Export traces to Azure Monitor

To send traces to Application Insights instead of the console, replace the console exporter with `AzureMonitorTraceExporter`. Set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable, then add the following code. The `useInstrumenter()` bridge from the previous section is still required.

```javascript
import { NodeTracerProvider, SimpleSpanProcessor } from "@opentelemetry/sdk-trace-node";
import { AzureMonitorTraceExporter } from "@azure/monitor-opentelemetry-exporter";

const exporter = new AzureMonitorTraceExporter({
  connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING,
});
const provider = new NodeTracerProvider({
  spanProcessors: [new SimpleSpanProcessor(exporter)],
});
provider.register();

// Register the same useInstrumenter() bridge shown in the console tracing section.
```

View the results in the **Tracing** tab in your Foundry project page or in Application Insights.

Reference: [Azure Monitor OpenTelemetry exporter for JavaScript](/javascript/api/overview/azure/monitor-opentelemetry-exporter-readme)

## Add custom span attributes

To correlate Voice Live traces with your application context (session IDs, user IDs, or request identifiers), implement a custom `SpanProcessor` that adds attributes when each span starts.

```javascript
class CustomAttributesProcessor {
  constructor(sessionId, userId) {
    this._sessionId = sessionId;
    this._userId = userId;
  }

  onStart(span) {
    span.setAttribute("app.session_id", this._sessionId);
    span.setAttribute("app.user_id", this._userId);
  }

  onEnd() { }
  async shutdown() { }
  async forceFlush() { }
}
```

Register the custom processor on the tracer provider before calling `provider.register()`:

```javascript
const provider = new NodeTracerProvider({
  spanProcessors: [
    new CustomAttributesProcessor("sess-123", "user-abc"),
    new SimpleSpanProcessor(new ConsoleSpanExporter()),
  ],
});
provider.register();
```

Reference: [OpenTelemetry JavaScript SDK](https://opentelemetry.io/docs/languages/js/)

## Enable browser tracing

For browser-based applications, use `WebTracerProvider` instead of `NodeTracerProvider`. The same `useInstrumenter()` bridge applies. Spans can be exported to an in-page element, the browser console, or any OpenTelemetry-compatible backend.

```javascript
import { WebTracerProvider, SimpleSpanProcessor } from "@opentelemetry/sdk-trace-web";
import { ConsoleSpanExporter } from "@opentelemetry/sdk-trace-base";
import { useInstrumenter } from "@azure/core-tracing";
import { trace, context } from "@opentelemetry/api";
import { VoiceLiveClient } from "@azure/ai-voicelive";

const provider = new WebTracerProvider({
  spanProcessors: [new SimpleSpanProcessor(new ConsoleSpanExporter())],
});
provider.register();

// Register the same useInstrumenter() bridge shown in the console tracing section.

// Browsers don't support DefaultAzureCredential. Use AzureKeyCredential instead.
const credential = { key: import.meta.env.VITE_VOICELIVE_API_KEY };
const client = new VoiceLiveClient(import.meta.env.VITE_VOICELIVE_ENDPOINT, credential);
const session = client.createSession("gpt-realtime");
await session.connect();
```

> [!NOTE]
> Browsers don't support `DefaultAzureCredential`. Use `AzureKeyCredential` or a bearer-token flow instead.

> [!div class="nextstepaction"]
> [Complete browser tracing sample](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/voicelive/ai-voicelive/samples/telemetry-browser)

## Enable content recording

Content recording captures full message payloads (send and receive) on span events. This is useful for debugging but can capture personal data.

> [!CAUTION]
> Content recording may capture personal data. Only enable in development or controlled environments.

Set the `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` environment variable to `true` before starting your application. No code changes are required.

```bash
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```

When enabled, the SDK attaches event payloads as `gen_ai.event.content` attributes on the corresponding spans.
