---
title: "Export hosted agent telemetry by using OpenTelemetry"
description: "Export traces, logs, and metrics from a Microsoft Foundry hosted agent to Application Insights or any OpenTelemetry (OTLP) endpoint."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 07/01/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
# customer intent: As a developer, I want to export my hosted agent's telemetry to my existing observability backend so that I can monitor agents alongside the rest of my services.
---

# Export hosted agent telemetry by using OpenTelemetry

Configure a [hosted agent](../concepts/hosted-agents.md) to export its trace, log, and metric data in an OpenTelemetry format. Hosted agents generate telemetry from the protocol runtime (the Responses or Invocations server) and from your agent code. By default, the agent sends this telemetry to the Application Insights resource that Foundry links to your project. You can also export the same data - by using OpenTelemetry semantics - to any other OpenTelemetry-compliant endpoint or a self-hosted [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/).

When you export hosted agent telemetry by using OpenTelemetry, you get these benefits:

- Correlation of data across traces and logs from both the protocol runtime and your agent code.
- Consistent, standards-based generation of exportable telemetry.
- Integration with any observability provider that consumes OpenTelemetry-compliant data.

Keep these considerations in mind:

- You configure telemetry export entirely through **environment variables** on the agent version. You don't add or change instrumentation code. The protocol runtime autodetects the configuration at startup.
- You set environment variables per version and they're **immutable** once the version is created. To change the export destination, you create a new agent version.
- You can enable Application Insights and an OTLP exporter at the same time. When you configure both, the agent sends telemetry to both destinations.

## Prerequisites

- A Foundry project with a deployed hosted agent. To create one, see [Deploy a hosted agent](deploy-hosted-agent.md).
- An OpenTelemetry-compliant endpoint if you export to a provider other than Application Insights. Get the endpoint URL and any required authentication headers from your provider's documentation.

## How hosted agents emit OpenTelemetry

Each hosted agent protocol (Responses, Invocations) uses a lightweight library that handles the HTTP or WebSocket server, health checks, and **OpenTelemetry integration**. These libraries bundle the OpenTelemetry distro, so your agent emits traces, logs, and metrics without any telemetry setup in your code. The runtime chooses its exporters based on the environment variables it detects at startup:

- When the platform-injected `APPLICATIONINSIGHTS_CONNECTION_STRING` setting is present, the runtime exports to **Application Insights**. Foundry injects this setting automatically when project monitoring is enabled.
- When `OTEL_EXPORTER_OTLP_ENDPOINT` is present, the runtime also exports over **OTLP** to that endpoint.

Because both exporters use independent settings, you can send telemetry to Application Insights, to an OTLP endpoint, or to both simultaneously.

> [!NOTE]
> `APPLICATIONINSIGHTS_CONNECTION_STRING` is a platform-reserved setting that Foundry injects into your container—you can't set or override it in `agent.yaml`. Foundry injects it only when monitoring is configured on the project. To stop sending telemetry to Application Insights, disable monitoring at the project level rather than trying to remove the setting from the agent.

## Configure the export destination

Configure environment variables on your agent based on where you want telemetry sent. The following tabs describe the settings for each destination.

# [Application Insights](#tab/app-insights)

Application Insights is the default destination and requires no configuration on the agent. When project monitoring is enabled, Foundry links an Application Insights resource to the project and injects its connection string into every hosted agent container.

**`APPLICATIONINSIGHTS_CONNECTION_STRING`**: The connection string for the linked Application Insights resource. Foundry sets this value automatically. It's reserved and can't be overridden in `agent.yaml`.

Telemetry appears in the linked Application Insights resource under **Investigate** > **Transaction search** or **Investigate** > **Performance**. For analysis guidance, see [Enable tracing in your project](../../observability/concepts/trace-agent-concept.md).

# [OTLP exporter](#tab/otlp-export)

Hosted agents support exporting OpenTelemetry data to any OTLP-compliant endpoint. The specific values depend on your chosen observability provider or a self-hosted collector.

Most providers require:

**`OTEL_EXPORTER_OTLP_ENDPOINT`**: The OTLP endpoint URL provided by your observability backend—for example, `https://otlp.example-provider.com`. The endpoint URL isn't a secret.

**`OTEL_EXPORTER_OTLP_PROTOCOL`**: The OTLP transport to use. Use `http/protobuf` (OTLP over HTTP) unless your provider requires otherwise—it's the most widely supported option for sending telemetry to an external endpoint. The exporter also supports `grpc` (OTLP over gRPC), but gRPC availability varies by provider (some accept only HTTP), so confirm your backend supports it before choosing it. Match the protocol your endpoint expects.

Many providers also require:

**`OTEL_EXPORTER_OTLP_HEADERS`**: Headers for authentication credentials, such as an API key. This header follows the standard OpenTelemetry mechanism for authenticating to an OTLP backend, and most SaaS providers support it. The value is a comma-separated list of `key=value` pairs—for example, `api-key=<your-key>` or `x-provider-team=<token>,x-provider-dataset=<name>`. Keep these format rules in mind:

- Provide the header name and format exactly as your provider documents them. A stray space or comma is a common cause of silent authentication failures.
- For providers that use HTTP Basic authentication, the OpenTelemetry OTLP exporter passes headers verbatim and doesn't build the `Authorization` header for you. Base64-encode the credentials yourself and pass `Authorization=Basic <base64-encoded-credentials>`.
- URL-encode any value that contains reserved characters.
- To use different headers per signal, set the per-signal variants instead: `OTEL_EXPORTER_OTLP_TRACES_HEADERS`, `OTEL_EXPORTER_OTLP_LOGS_HEADERS`, and `OTEL_EXPORTER_OTLP_METRICS_HEADERS`. `OTEL_EXPORTER_OTLP_HEADERS` applies to all signals.

Because the header value is a secret, store it in a connection instead of in `agent.yaml`. See [Store the OTLP authentication header in a connection](#store-the-otlp-authentication-header-in-a-connection).

Hosted agents support the standard environment variables defined in the [OpenTelemetry SDK configuration documentation](https://opentelemetry.io/docs/languages/sdk-configuration/). The specific variables and values you need vary by provider. Consult your observability provider's documentation for:

- Required endpoint URLs and authentication methods.
- Recommended configuration settings.
- Provider-specific environment variables.
- Any additional setup steps.

---

## Set environment variables on your agent

Add the export settings to the `environment_variables` section of your agent's `agent.yaml` file. When you deploy by using `azd`, these values are applied to the new agent version.

```yaml
environment_variables:
  - name: AZURE_AI_MODEL_DEPLOYMENT_NAME
    value: gpt-5-mini
  # Export OpenTelemetry traces, logs, and metrics over OTLP.
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: https://<your-provider-otlp-endpoint>     # not secret
  - name: OTEL_EXPORTER_OTLP_PROTOCOL
    value: http/protobuf
```

Telemetry continues to flow to Application Insights unless you disable monitoring at the project level, so this configuration sends data to *both* destinations. To send data only to the OTLP endpoint, disable monitoring at the project level.

> [!TIP]
> If your own infrastructure provisions the endpoint (for example, an OpenTelemetry Collector you deploy alongside the agent), reference the endpoint with a deployment output - for example `value: ${OTEL_EXPORTER_OTLP_ENDPOINT}` - so Foundry resolves the value at deploy time instead of hard-coding it.

## Store the OTLP authentication header in a connection

The OTLP endpoint URL isn't a secret, but the authentication header usually is. Keep the secret out of `agent.yaml` by storing it in a Foundry **Custom keys** project connection and referencing it with a placeholder.

1. Create a **Custom keys** (`CustomKeys`) connection on the project. In the Foundry portal, go to **Connected resources** > **Add connection** > **Custom keys**, or create the connection with infrastructure as code. Add a field that holds the full OTLP header string - for example a field named `otlp_headers` set to `<header-name>=<secret>`. The exact header name and format come from your provider's documentation.

1. Reference the connection field from `agent.yaml` with a placeholder:

   ```yaml
   environment_variables:
     - name: OTEL_EXPORTER_OTLP_ENDPOINT
       value: https://<your-provider-otlp-endpoint>     # not secret
     - name: OTEL_EXPORTER_OTLP_PROTOCOL
       value: http/protobuf
     - name: OTEL_EXPORTER_OTLP_HEADERS
       value: ${{connections.otel-secrets.credentials.otlp_headers}}   # secret via connection
   ```

   Foundry resolves the placeholder when the session sandbox starts and injects the value as a plain environment variable. For more information, see [Reference project connections in environment variables](deploy-hosted-agent.md#reference-project-connections-in-environment-variables).

Keep these points in mind when you use a connection:

- Create the connection **before** you deploy the agent version. If the connection is missing when the sandbox starts, the placeholder resolves to an empty value.
- Secrets are write-only. A read of the connection returns `credentials: null`, so verify the value by reading the environment variable from inside the running container - not by inspecting the connection.
- The placeholder path must match the connection field name exactly. Record the field name yourself, because it isn't returned when you read the connection.

## Send telemetry to both Application Insights and an OTLP endpoint

Because two exporters use independent settings, you don't need extra configuration to use both. When both `APPLICATIONINSIGHTS_CONNECTION_STRING` (injected by the platform) and `OTEL_EXPORTER_OTLP_ENDPOINT` (set on your agent) are present, the agent sends telemetry to both destinations in parallel. This behavior lets you keep the built-in Application Insights experience while also forwarding data to your existing observability backend.

To send telemetry *only* to your OTLP endpoint, disable monitoring at the project level so Foundry doesn't inject the Application Insights connection string.

## Service name

Hosted agents report telemetry under a `service.name` fixed to the **agent's name** - shown as `cloud_RoleName` in Application Insights and as the service/resource name in your OTLP backend. This applies to both exports and is set by the platform.

The standard `OTEL_SERVICE_NAME` environment variable has **no effect** on a hosted agent; the platform overrides it. To use a different service name, name the agent accordingly.

## Tune exporter behavior

You can adjust exporter behavior - such as trace sampling with `OTEL_TRACES_SAMPLER` - by using the standard OpenTelemetry environment variables. These variables provide a consistent way to control behavior across languages and runtimes. Trace sampling affects spans only; log records are exported regardless. The platform sets some values itself (for example, service.name), so resource attributes set through environment variables might be overridden. For the full list of supported variables, see the [OpenTelemetry SDK configuration documentation](https://opentelemetry.io/docs/languages/sdk-configuration/).

## Considerations for OpenTelemetry

When you export your data by using OpenTelemetry, keep these considerations in mind:

- **Immutable versions**: Set environment variables per agent version. You can't change them after creating the version. To change the export destination or headers, create a new agent version.
- **Reserved Application Insights setting**: You can't set or override `APPLICATIONINSIGHTS_CONNECTION_STRING` in `agent.yaml`. Control it through project monitoring.
- **Third-party data flow**: When you export to a non-Microsoft observability provider, telemetry (which can include prompt, tool, and response content depending on your instrumentation) flows to that provider. Review the provider's data handling, retention, and location policies, and confirm the flow meets your organization's compliance and geographic requirements. For more information, see [Security and data handling](../concepts/hosted-agents.md#security-and-data-handling).
- **Batched export**: Telemetry is exported in batches, so allow a few seconds after invoking the agent before data appears in your backend.

## Troubleshooting

When you export your data by using OpenTelemetry, keep these common issues and solutions in mind.

### No telemetry appears at the OTLP endpoint

Confirm the deployed agent has the endpoint set and that the export configuration is correct:

- Verify `OTEL_EXPORTER_OTLP_ENDPOINT` is set on the deployed agent version and points to the correct URL.
- Confirm `OTEL_EXPORTER_OTLP_PROTOCOL` matches what your endpoint expects (`http/protobuf` or `grpc`).
- Invoke the agent to generate telemetry, then allow a few seconds for the batched export.

### Authentication failures at the OTLP endpoint

If the endpoint rejects the connection with an authentication error:

- Confirm the `CustomKeys` connection exists and was created **before** the agent version was deployed.
- Verify the placeholder path in `agent.yaml` matches the connection field name exactly.
- Confirm the header string format matches your provider's documentation (for example, `api-key=<value>`).
- Because secrets are write-only, verify the resolved value by reading `OTEL_EXPORTER_OTLP_HEADERS` from inside the running container rather than by reading the connection.

### Telemetry still flows to Application Insights after configuring OTLP

Configuring an OTLP exporter doesn't disable Application Insights—both destinations receive telemetry when both are configured. To stop sending telemetry to Application Insights, disable monitoring at the project level so Foundry doesn't inject `APPLICATIONINSIGHTS_CONNECTION_STRING`.

## Related content

- [Hosted agents in Foundry Agent Service](../concepts/hosted-agents.md)
- [Deploy a hosted agent](deploy-hosted-agent.md)
- [Enable tracing in your project](../../observability/concepts/trace-agent-concept.md)
- [OpenTelemetry SDK configuration](https://opentelemetry.io/docs/languages/sdk-configuration/)
