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

Register an OpenTelemetry tracer provider that listens to the `Azure.AI.VoiceLive` activity source before you construct the `VoiceLiveClient`. The SDK emits spans automatically when a provider is present.

```csharp
using Azure.AI.VoiceLive;
using Azure.Identity;
using OpenTelemetry;
using OpenTelemetry.Trace;

// Register an OpenTelemetry provider before constructing the VoiceLive client.
using TracerProvider tracerProvider = Sdk.CreateTracerProviderBuilder()
    .AddSource("Azure.AI.VoiceLive")
    .AddConsoleExporter()
    .Build();

string endpoint = Environment.GetEnvironmentVariable("AZURE_VOICELIVE_ENDPOINT")!;
VoiceLiveClient client = new(new Uri(endpoint), new DefaultAzureCredential());

// All connect, send, and receive operations now produce spans on the console.
VoiceLiveSession session = await client.StartSessionAsync("gpt-realtime");
```

All connect, send, and receive operations now produce spans printed to stdout.

Reference: [OpenTelemetry .NET](https://opentelemetry.io/docs/languages/dotnet/) | [VoiceLiveClient](/dotnet/api/azure.ai.voicelive.voiceliveclient)

> [!div class="nextstepaction"]
> [Complete console tracing sample](https://github.com/Azure/azure-sdk-for-net/tree/main/samples/voicelive/telemetry-tracing)

## Export traces to Azure Monitor

To send traces to Application Insights instead of the console, replace the console exporter with the Azure Monitor exporter. Set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable, then add the following code.

```csharp
using Azure.AI.VoiceLive;
using Azure.Identity;
using Azure.Monitor.OpenTelemetry.Exporter;
using OpenTelemetry;
using OpenTelemetry.Trace;

string connectionString = Environment.GetEnvironmentVariable("APPLICATIONINSIGHTS_CONNECTION_STRING")!;

using TracerProvider tracerProvider = Sdk.CreateTracerProviderBuilder()
    .AddSource("Azure.AI.VoiceLive")
    .AddAzureMonitorTraceExporter(options => options.ConnectionString = connectionString)
    .Build();

string endpoint = Environment.GetEnvironmentVariable("AZURE_VOICELIVE_ENDPOINT")!;
VoiceLiveClient client = new(new Uri(endpoint), new DefaultAzureCredential());
VoiceLiveSession session = await client.StartSessionAsync("gpt-realtime");
```

View the results in the **Tracing** tab in your Foundry project page or in Application Insights.

Reference: [Azure Monitor OpenTelemetry exporter for .NET](/dotnet/api/overview/azure/monitor.opentelemetry.exporter-readme)

## Add custom span attributes

To correlate Voice Live traces with your application context (session IDs, user IDs, or request identifiers), implement a processor that derives from `BaseProcessor<Activity>`.

```csharp
using System.Diagnostics;
using OpenTelemetry;

internal sealed class CustomAttributesProcessor : BaseProcessor<Activity>
{
    private readonly string _sessionId;
    private readonly string _userId;

    public CustomAttributesProcessor(string sessionId, string userId)
    {
        _sessionId = sessionId;
        _userId = userId;
    }

    public override void OnStart(Activity activity)
    {
        activity.SetTag("app.session_id", _sessionId);
        activity.SetTag("app.user_id", _userId);
    }
}
```

Register the custom processor with the tracer provider builder after adding the `Azure.AI.VoiceLive` source:

```csharp
using TracerProvider tracerProvider = Sdk.CreateTracerProviderBuilder()
    .AddSource("Azure.AI.VoiceLive")
    .AddProcessor(new CustomAttributesProcessor(sessionId: "sess-123", userId: "user-abc"))
    .AddConsoleExporter()
    .Build();
```

## Enable content recording

Content recording captures full message payloads (send and receive) on span events. This is useful for debugging but can capture personal data.

> [!CAUTION]
> Content recording may capture personal data. Only enable in development or controlled environments.

Set the `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` environment variable to `true` before starting your application. No code changes are required.

```bash
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```

When enabled, the SDK attaches event payloads as `gen_ai.event.content` attributes on the corresponding spans.
