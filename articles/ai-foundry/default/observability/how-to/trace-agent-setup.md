---
title: Set Up Tracing for AI Agents in Microsoft Foundry
ms.service: azure-ai-foundry
titleSuffix: Microsoft Foundry
description: Learn how to set up tracing in Microsoft Foundry to debug AI agent runs and monitor behavior by sending telemetry to Application Insights with OpenTelemetry.
ai-usage: ai-assisted
author: yanchen-ms
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 01/20/2026
ms.topic: how-to
ms.custom: pilot-ai-workflow-jan-2026
---

# Set up tracing in Microsoft Foundry (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

Use tracing (preview) to debug your AI agents and monitor their behavior in production. Tracing captures detailed telemetry—including latency, exceptions, prompt content, and retrieval operations—so you can identify and fix issues faster.

## Prerequisites

- A [Foundry project](../../../how-to/create-projects.md).
- An [Azure Monitor Application Insights resource](/azure/azure-monitor/app/app-insights-overview) to store traces (create a new one or connect an existing one).
- Access to the Application Insights resource connected to your project.

## Connect Application Insights to your Foundry project

Foundry stores traces in [Azure Application Insights](/azure/azure-monitor/app/app-insights-overview) by using [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]
1. Open your Foundry project.
1. In the left navigation, select **Tracing**.
1. Create or connect an Application Insights resource:
   - To connect an existing resource, select the resource and then select **Connect**.
   - To create a new resource, select **Create new** and complete the wizard.

   A confirmation message appears when the connection succeeds.

After you connect the resource, your project is ready to use tracing.

> [!IMPORTANT]
> Make sure you have the permissions you need to query telemetry.
>
> - For log-based queries, start by assigning the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader).
> - To learn how to assign roles, see [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal).
> - To manage access at scale, use [Microsoft Entra groups](../../../concepts/rbac-foundry.md#use-microsoft-entra-groups-with-foundry).

## Instrument AI agents

Choose the approach that matches how you build and run your agent.

### Server-side traces in the Foundry portal

Start with server-side traces. Foundry logs traces for common agent and workflow scenarios without changing your code.

- Foundry automatically logs server-side traces for Prompt agents, Host agents, and workflows in the Foundry portal. Once tracing is enabled in your Foundry project, you'll have access to out-of-the-box traces for the past 90 days.
- Foundry also allows for easy [integration](trace-agent-framework.md) with top agent frameworks.

### Client-side traces with the Microsoft Foundry SDK (Python)

Install OpenTelemetry and the Azure SDK tracing plugin using:

```bash
pip install azure-ai-projects azure-identity opentelemetry-sdk azure-core-tracing-opentelemetry
```

> [!IMPORTANT]
> Using a project's endpoint in your application requires configuring Microsoft Entra ID. If you don't configure Microsoft Entra ID, use the Azure Application Insights connection string.

After running your agent, you can begin to [view and analyze traces in Foundry portal](#view-traces-in-the-foundry-portal).

For detailed instructions and SDK-specific code examples, see [Tracing with azure-ai-projects (Python SDK)](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects#tracing) and [Telemetry samples for agents](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/agents/telemetry).

### Trace locally with AI Toolkit in VS Code

AI Toolkit lets you trace locally in VS Code using a local OTLP-compatible collector, which is ideal for development and debugging.

The toolkit supports AI frameworks such as Foundry Agents Service, OpenAI, Anthropic, and LangChain through OpenTelemetry. You can see traces instantly in VS Code without needing cloud access.

For detailed setup instructions and SDK-specific code examples, see [Tracing in AI Toolkit](https://code.visualstudio.com/docs/intelligentapps/tracing).

## View and analyze traces

### View traces in the Foundry portal

In your Foundry project, go to the **Traces** tab in your agents or workflows. You can search, filter, or sort ingested traces from the last 90 days.

Select a trace to step through each span, identify issues, and observe how your application responds. This helps you debug and pinpoint issues in your application.

### View traces in Azure Monitor

Your traces are sent to Azure Monitor Application Insights, so you can view them there.

For more information on how to send traces to Azure Monitor and create an Azure Monitor resource, see [Azure Monitor OpenTelemetry documentation](/azure/azure-monitor/app/opentelemetry-enable).


### View conversation results

A **Conversation** is the persistent context of an end-to-end dialogue history between a user and an agent. In the Foundry portal, you can view **Conversation** results for your agent run out of the box along with traces on the **Traces** page.

You can search for a known Conversation ID, search by a Response ID, or search by a Trace ID that maps to this conversation. Then, select **Conversation ID** to review the conversation:

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

Tracing can capture sensitive information (for example, user inputs, model outputs, and tool arguments and results). Use these practices to reduce risk:

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
| You see authorization errors when you query or view telemetry | Missing RBAC permissions on Application Insights or Log Analytics | Confirm access in **Access control (IAM)** for the connected resources. For log queries, assign the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader). |
| Client-side traces don't appear | Instrumentation isn't installed or configured | Recheck your package installation and follow the SDK guidance linked in [Client-side traces with the Microsoft Foundry SDK (Python)](#client-side-traces-with-the-microsoft-foundry-sdk-python). |
| Sensitive content appears in traces | Prompts, tool arguments, or outputs contain sensitive data | Redact sensitive data before it enters telemetry and follow the guidance in [Security and privacy](#security-and-privacy). |

## Related content

Now that tracing is set up, explore these resources to deepen your understanding and extend your observability capabilities:

- [Agent tracing overview](../concepts/trace-agent-concept.md)
- [Tracing integrations](trace-agent-framework.md)
- [Monitor AI agents with the Agent Monitoring Dashboard](how-to-monitor-agents-dashboard.md)
- [Observability in generative AI](../../../concepts/observability.md)
