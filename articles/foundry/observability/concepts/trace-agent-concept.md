---
title: "Agent tracing overview"
description: "Learn how agent tracing in Microsoft Foundry captures inputs, outputs, and tool usage with OpenTelemetry. Debug agent runs, identify latency issues, and improve reliability."
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: dchirasani
ms.date: 08/28/2026
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
ms.topic: concept-article
---
# Agent tracing overview

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

[!INCLUDE [trace-agent-preview](../../includes/trace-agent-preview.md)]

Microsoft Foundry provides an observability platform for monitoring and tracing AI agents. It captures key details during an agent run, such as inputs, outputs, tool usage, retries, latencies, and costs. Understanding the reasoning behind your agent's executions is important for troubleshooting and debugging. However, understanding complex agents presents challenges for several reasons:

- There can be a high number of steps involved in generating a response, making it hard to keep track of all of them.
- The sequence of steps might vary based on user input.
- The inputs and outputs at each stage might be long and deserve more detailed inspection.
- Each step of an agent's runtime might also involve nesting. For example, an agent might invoke a tool, which uses another process, which then invokes another tool. If you notice strange or incorrect output from a top-level agent run, it might be difficult to determine exactly where in the execution the issue was introduced.

Traces address these challenges by allowing you to view the inputs and outputs of each primitive involved in a particular agent run, displayed in the order they were invoked, making it easy to understand and debug your AI agent's behavior.

## Prerequisites

To use tracing end-to-end, you need:

- A Foundry project with tracing enabled. To set it up, see [How to set up tracing in Microsoft Foundry](../how-to/trace-agent-setup.md).
- Access to the Application Insights resource connected to your project. For background, see [Azure Monitor Application Insights](/azure/azure-monitor/app/app-insights-overview).
- A Log Analytics reader role to view traces, insights, and visualizations in Foundry.

> [!NOTE]
> Tracing stores telemetry data in Azure Monitor Application Insights, which might incur costs based on data volume and retention settings. For pricing details, see [Application Insights pricing](/azure/azure-monitor/cost-usage#application-insights-billing).

## OpenTelemetry in Foundry

OpenTelemetry (OTel) provides standardized protocols for collecting and routing telemetry data. Foundry uses OpenTelemetry semantic conventions so traces are consistent across supported tools and integrations.

## Trace key concepts

The following key concepts apply throughout this article:

| Key concepts             | Description            |
|---------------------|-----------------------------------------------------------------|
| Traces              | Traces capture the journey of a request or workflow through your application by recording events and state changes (function calls, values, system events). See [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/). |
| Spans               | Spans are the building blocks of traces, representing single operations within a trace. Each span captures start and end times, attributes, and can be nested to show hierarchical relationships, so you can see the full call stack and sequence of operations.                                                                                         |
| Attributes          | Attributes are key-value pairs attached to traces and spans, providing contextual metadata such as function parameters, return values, or custom annotations. These enrich trace data, making it more informative and useful for analysis.                                                                                                 |
| Semantic conventions| OpenTelemetry defines semantic conventions to standardize names and formats for trace data attributes, making it easier to interpret and analyze across tools and platforms. To learn more, see the [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai).                  |
| Trace exporters     | Trace exporters send trace data to backend systems for storage and analysis. In Foundry, traces are stored in Azure Monitor Application Insights. To learn how to enable and view traces, see [How to set up tracing in Microsoft Foundry](../how-to/trace-agent-setup.md). |

## How tracing works in Foundry

Tracing helps you answer questions like "Where did this response come from?" and "Which step introduced an error or latency spike?"

At a high level, tracing captures:

- User inputs and agent outputs.
- Tool usage, including tool calls and results.
- Token consumption.
- Time signals such as duration and latency.

When you enable tracing for your project, you can inspect traces in the Foundry portal and in Azure Monitor Application Insights. For the step-by-step setup and viewing options, see [How to set up tracing in Microsoft Foundry](../how-to/trace-agent-setup.md).

## Extend OpenTelemetry with multi-agent observability

Microsoft, in collaboration with Cisco Outshift, contributes semantic conventions for multi-agent systems. These conventions build on [OpenTelemetry GenAI agent and framework spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md) and [W3C Trace Context](https://www.w3.org/TR/trace-context/). They standardize telemetry for multi-agent workflows, including agent invocations, workflow orchestration, planning, model calls, and tool execution.

> [!IMPORTANT]
> The OpenTelemetry GenAI semantic conventions have Development status and might change in future releases.

These enhancements are integrated into:

- Foundry
- Microsoft Agent Framework
- LangChain
- LangGraph
- OpenAI Agents SDK

For more information, see [tracing integrations](../how-to/trace-agent-framework.md).

The following table describes common OpenTelemetry GenAI conventions for multi-agent observability. Spans capture operations, child spans show nested work, and attributes provide metadata. The parent spans shown are common examples; actual nesting depends on the instrumented agent or framework.

| Type | Context/Parent Span | Name/Attribute/Event | Purpose |
| --- | --- | --- | --- |
| Span | — | `invoke_agent` | Invokes an agent through a remote service or within the same process. |
| Child span | `invoke_agent` | `invoke_agent` | Traces an invocation of another agent through a parent-child span relationship. |
| Child span | `invoke_agent` | `plan` | Records an agent planning or task decomposition phase. |
| Span | — | `invoke_workflow` | Invokes a coordinated workflow that contains agents or other generative AI operations. |
| Child span | `invoke_agent` or `invoke_workflow` | `execute_tool` | Records a tool execution. |
| Child span | `invoke_agent` or `invoke_workflow` | `create_memory`, `search_memory`, `update_memory`, `upsert_memory`, or `delete_memory` | Records a memory operation. |
| Attribute | `invoke_agent` | `gen_ai.tool.definitions` | Records definitions of tools available to an agent or model. |
| Attribute | `execute_tool` | `gen_ai.tool.call.arguments` | Records the arguments passed to a tool call. |
| Attribute | `execute_tool` | `gen_ai.tool.call.result` | Records the result returned by a successful tool call. |

## Best practices

- **Use consistent span attributes**: Apply the same attribute names and formats across all agents and tools to simplify querying and analysis.
- **Correlate evaluation run IDs**: Link trace data with evaluation runs to analyze both quality and performance in a unified view.
- **Redact sensitive content**: Remove or mask personal data, secrets, and credentials from prompts, tool arguments, and span attributes before they reach telemetry.

## Security and privacy

Tracing can capture sensitive information, such as user inputs, model outputs, and tool arguments and results. Use these practices to reduce risk:

- Don't store secrets, credentials, or tokens in prompts, tool arguments, or span attributes.
- Redact or minimize personal data and other sensitive content before it appears in telemetry.
- Treat trace data as production telemetry and apply the same access controls and retention policies you use for logs and metrics.

To learn steps to route sensitive content to the dedicated table and restrict access to it, see [Restrict access to sensitive content](../how-to/traces-sensitive-content.md).

## Troubleshooting

If traces aren't appearing in the Foundry portal or Application Insights:

- Verify that your Foundry project is connected to an Application Insights resource.
- Check that your account has the required permissions to query telemetry.
- Ensure your agent code includes the necessary instrumentation. For framework-specific setup, see [Tracing integrations](../how-to/trace-agent-framework.md).

> [!TIP]
> Tracing is available in all regions where Foundry is supported. Trace data retention and sampling follow your Application Insights configuration. For details, see [Data retention and archive in Azure Monitor Logs](/azure/azure-monitor/logs/data-retention-configure).

## Related content

- [How to set up tracing in Microsoft Foundry](../how-to/trace-agent-setup.md)
- [Tracing integrations](../how-to/trace-agent-framework.md)
- [Monitor AI agents with the Agent Monitoring Dashboard](../how-to/how-to-monitor-agents-dashboard.md)
- [Observability in generative AI](../../concepts/observability.md)
