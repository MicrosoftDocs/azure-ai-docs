---
title: How to Set Up Tracing in Microsoft Foundry
ms.service: azure-ai-foundry
titleSuffix: Microsoft Foundry
description: "Enable tracing in Microsoft Foundry to monitor agent performance, debug issues, and analyze runtime behavior using Azure Application Insights and OpenTelemetry."
ai-usage: ai-assisted
author: yanchen-ms
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 11/18/2025
ms.topic: how-to
---

# How to set up tracing in Microsoft Foundry

Tracing is a powerful tool to understand how your agent works. It helps you identify issues like latency, runtime exceptions, incorrect prompts, poor retrieval, and more.

## Enable tracing in Foundry project

Microsoft Foundry stores traces in [Azure Application Insights](/azure/azure-monitor/app/app-insights-overview) using [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/). To enable tracing and monitoring in your Foundry project, create or connect an Application Insights resource in monitor settings. After configuring the connection, tracing is ready to use for your Foundry project.

> [!IMPORTANT]
> Make sure you have the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader) assigned in your Application Insights resource. To learn more about assigning roles, see [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal), and use [Microsoft Entra groups](../../../concepts/rbac-azure-ai-foundry.md#use-microsoft-entra-groups-with-foundry) to manage user access more easily.
> Using a project's endpoint requires configuring Microsoft Entra ID in your application. If you don't configure Entra ID, use the Azure Application Insights connection string.

## Instrumenting AI Agents

### Server-side Tracing

We recommend starting with the auto-instrumentation first. Foundry makes it easy to log traces.

- Foundry automatically logs server-side traces for Prompt agents, Host agents, and workflows in the Foundry portal. Once tracing is enabled in your Foundry project, you’ll have access to out-of-the-box traces for the past 90 days.
- Foundry also allows for easy [integration](trace-agent-framework.md) with top agent frameworks.

### Client-side Tracing with Microsoft Foundry SDK

Install OpenTelemetry and the Azure SDK tracing plugin using:

```bash
pip install azure-ai-projects azure-identity opentelemetry-sdk azure-core-tracing-opentelemetry
```

After running your agent, you can begin to [view and analyze traces in Foundry portal](#view-traces-in-the-foundry-portal).

For detailed instructions and SDK-specific code examples, see [instructions](https://github.com/Azure/azure-sdk-for-python/tree/feature/azure-ai-projects/2.0.0b1/sdk/ai/azure-ai-projects#tracing) and [samples](https://github.com/Azure/azure-sdk-for-python/tree/feature/azure-ai-projects/2.0.0b1/sdk/ai/azure-ai-projects/samples/agents/telemetry).

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

:::image type="content" source="../../media/observability/tracing/conversation.png" alt-text="Screenshot of a trace." lightbox="../../media/observability/tracing/conversation.png":::

## Related content

- [Agent tracing overview](../concepts/trace-agent-concept.md)
- [Tracing integrations](trace-agent-framework.md)