---
title: "Set Up Tracing for AI Agents in Microsoft Foundry"
ms.service: microsoft-foundry
ms.subservice: foundry-observability
description: "Learn how to set up tracing in Microsoft Foundry to debug AI agent runs and monitor behavior by sending telemetry to Azure Monitor Application Insights with OpenTelemetry."
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: dchirasani
ms.date: 07/31/2026
ms.topic: how-to
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
---

# Set up tracing in Microsoft Foundry

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

[!INCLUDE [trace-agent-preview](../../includes/trace-agent-preview.md)]

Use tracing to debug your AI agents and monitor their behavior in production. Tracing captures detailed telemetry - including latency, exceptions, prompt content, and retrieval operations - so you can identify and fix issues faster.

The recommended starting point is **server-side tracing**. Foundry enables it automatically after you connect an Application Insights resource to your project. No code changes are required, and traces are available within minutes of enabling it. Server-side tracing works for any agent hosted in Foundry. When you need visibility into your own application code - for example, to trace custom logic surrounding an agent call - you can add client-side instrumentation as a second step.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md).
- An [Azure Monitor Application Insights resource](/azure/azure-monitor/app/app-insights-overview) to store traces (create a new one or connect an existing one).
- Access to the Application Insights resource connected to your project.
- The [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader) on the connected Application Insights resource (required to query telemetry). If the underlying Log Analytics tables are [protected](/azure/azure-monitor/logs/protected-tables-configure), also assign the [Privileged Monitoring Data Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#privileged-monitoring-data-reader).

## Connect Application Insights to your Foundry project

Foundry stores traces in [Application Insights](/azure/azure-monitor/app/app-insights-overview) by using [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).

[!INCLUDE [trace setup connection from traces](../../includes/trace-setup-connection-from-traces.md)]

   - To connect an existing resource, select the resource, and then select **Connect**.
   - To create a new resource, select **Create new**, and then complete the
     wizard.

   A confirmation message appears when the connection succeeds.

[!INCLUDE [trace setup connection from project details](../../includes/trace-setup-connection-from-project-details.md)]

For Entra-authenticated trace ingestion, see [Configure Microsoft Entra
authentication for Foundry Agent trace ingestion (preview)](trace-ingestion-entra-authentication.md).

After you connect the resource, your project is ready to use tracing.
> [!IMPORTANT]
> Make sure you have the permissions you need to query telemetry.
>
> - For log-based queries, start by assigning the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader). If the underlying Log Analytics tables are [protected](/azure/azure-monitor/logs/protected-tables-configure), also assign the [Privileged Monitoring Data Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#privileged-monitoring-data-reader).
> - To learn how to assign roles, see [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal).
> - To manage access at scale, use [Microsoft Entra groups](../../concepts/rbac-foundry.md#use-microsoft-entra-groups-with-foundry).

## Instrument AI agents

Choose the approach that matches how you build and run your agent.

### Server-side traces in the Foundry portal

Start with server-side traces. Foundry logs traces for common agent and workflow scenarios without changing your code.

- Foundry automatically logs server-side traces for Prompt agents, Host agents, and workflows in the Foundry portal. After tracing is enabled in your Foundry project, you have access to out-of-the-box traces for the past 90 days.
- Foundry also supports easy [integration](trace-agent-framework.md) with top agent frameworks.

### Client-side traces with the Microsoft Foundry SDK (Python)

Install OpenTelemetry and the Azure SDK tracing plugin by using the following steps:

```bash
pip install azure-ai-projects azure-identity opentelemetry-sdk azure-core-tracing-opentelemetry
```

Reference: [azure-ai-projects](/python/api/overview/azure/ai-projects-readme), [azure-core-tracing-opentelemetry](/python/api/overview/azure/core-tracing-opentelemetry-readme)

> [!IMPORTANT]
> To use a project's endpoint in your application, you need to configure Microsoft Entra ID. If you don't configure Microsoft Entra ID, use the Application Insights connection string.

After running your agent, you can [view and analyze traces in Foundry portal](#view-traces-in-the-foundry-portal).

For detailed instructions and SDK-specific code examples, see [Tracing with azure-ai-projects (Python SDK)](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects#tracing) and [Telemetry samples for agents](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/agents/telemetry).

### Trace locally with the Microsoft Foundry Toolkit for Visual Studio Code extension

The Microsoft Foundry Toolkit for Visual Studio Code extension lets you trace locally in VS Code by using a local OTLP-compatible collector. This approach is ideal for development and debugging.

The toolkit supports AI frameworks such as Foundry Agent Service, OpenAI, Anthropic, and LangChain through OpenTelemetry. You can see traces instantly in VS Code without needing cloud access.

For detailed setup instructions and SDK-specific code examples, see [Tracing in Foundry Toolkit](https://code.visualstudio.com/docs/intelligentapps/tracing).

## View and analyze traces

### View traces in the Foundry portal

In your Foundry project, go to the **Traces** tab in your agents or workflows. You can search, filter, or sort ingested traces from the last 90 days.

Select a trace to step through each span, identify problems, and observe how your application responds. This process helps you debug and pinpoint problems in your application.

### View traces in Azure Monitor

Your traces are sent to Azure Monitor Application Insights, so you can view them there.

For more information on how to send traces to Azure Monitor and create an Azure Monitor resource, see [Azure Monitor OpenTelemetry documentation](/azure/azure-monitor/app/opentelemetry-enable).

### View conversation results

A **Conversation** is the persistent context of an end-to-end dialogue history between a user and an agent. In the Foundry portal, you can view **Conversation** results for your agent run out of the box along with traces on the **Traces** page.

Search by Response ID or by a Trace ID that maps to this conversation. Then select a **Conversation ID** to review:

- Conversation history details
- Response information and tokens in a run
- Ordered actions, run steps, and tool calls
- Inputs and outputs between a user and an agent

:::image type="content" source="../../media/observability/tracing/conversation.png" alt-text="Screenshot of the Conversation details pane in Foundry showing a conversation ID with a trace timeline and run-step details." lightbox="../../media/observability/tracing/conversation.png":::

## Verify tracing works

1. Confirm your project is connected to Application Insights. If needed, follow the steps in [Connect Application Insights to your Foundry project](#connect-application-insights-to-your-foundry-project).
1. Run your agent or workflow at least once (for example, by using the portal or your app).
1. In your Foundry project, open the **Traces** view and confirm a new trace appears.

   When tracing is working correctly, you see a list of recent traces with timestamps, durations, and status indicators. Select a trace to view its span details.

If you don't see new traces, wait a few minutes and refresh, and then see [Troubleshooting](#troubleshooting).

## Security and privacy

Tracing can capture sensitive information, such as user inputs, model outputs, and tool arguments and results. Use these practices to reduce risk:

- Don't store secrets, credentials, or tokens in prompts, tool arguments, or span attributes.
- Redact or minimize personal data and other sensitive content before it appears in telemetry.
- Treat trace data as production telemetry and apply the same access controls and retention policies you use for logs and metrics.

For more guidance, see [Security and privacy](../concepts/trace-agent-concept.md#security-and-privacy).

## Data retention and cost

Foundry stores traces in the Application Insights resource connected to your project. Data retention and billing follow your Application Insights and Log Analytics configuration.

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| You don't see any traces in the Foundry portal | Tracing isn't connected, there is no recent traffic, or ingestion is delayed | Confirm the Application Insights connection, generate new agent traffic, and refresh after a few minutes. |
| You see authorization errors when you query or view telemetry | Missing RBAC permissions on Application Insights or Log Analytics | Confirm access in **Access control (IAM)** for the connected resources. For log queries, assign the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader). If the tables are [protected](/azure/azure-monitor/logs/protected-tables-configure), also assign [Privileged Monitoring Data Reader](/azure/azure-monitor/logs/manage-access?tabs=portal#privileged-monitoring-data-reader). |
| Client-side traces don't appear | Instrumentation isn't installed or configured | Recheck your package installation and follow the SDK guidance linked in [Client-side traces with the Microsoft Foundry SDK (Python)](#client-side-traces-with-the-microsoft-foundry-sdk-python). |
| Sensitive content appears in traces | Prompts, tool arguments, or outputs contain sensitive data | Redact sensitive data before it enters telemetry and follow the guidance in [Security and privacy](#security-and-privacy). |

## Related content

Now that you set up tracing, explore these resources to deepen your understanding and extend your observability capabilities:

- [Agent tracing overview](../concepts/trace-agent-concept.md)
- [Tracing integrations](trace-agent-framework.md)
- [Monitor AI agents with the Agent Monitoring Dashboard](how-to-monitor-agents-dashboard.md)
- [Observability in generative AI](../../concepts/observability.md)
