---
title: Agent tracing in Microsoft Foundry (preview)
titleSuffix: Microsoft Foundry
description: Learn how agent tracing in Microsoft Foundry captures inputs, outputs, and tool usage with OpenTelemetry. Debug agent runs, identify latency issues, and improve reliability.
ai-usage: ai-assisted
author: yanchen-ms
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 01/20/2026
ms.service: azure-ai-foundry
ms.custom: pilot-ai-workflow-jan-2026
ms.topic: concept-article
---
# Agent tracing overview (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

Microsoft Foundry provides an observability platform for monitoring and tracing AI agents. It captures key details during an agent run, such as inputs, outputs, tool usage, retries, latencies, and costs. Understanding the reasoning behind your agent's executions is important for troubleshooting and debugging. However, understanding complex agents presents challenges for several reasons:

- There could be a high number of steps involved in generating a response, making it hard to keep track of all of them.
- The sequence of steps might vary based on user input.
- The inputs/outputs at each stage might be long and deserve more detailed inspection.
- Each step of an agent's runtime might also involve nesting. For example, an agent might invoke a tool, which uses another process, which then invokes another tool. If you notice strange or incorrect output from a top-level agent run, it might be difficult to determine exactly where in the execution the issue was introduced.

Trace results solve this by allowing you to view the inputs and outputs of each primitive involved in a particular agent run, displayed in the order they were invoked, making it easy to understand and debug your AI agent's behavior.

## Prerequisites

To use tracing end-to-end, you need:

- A Foundry project with tracing enabled. To set it up, see [How to set up tracing in Microsoft Foundry](../how-to/trace-agent-setup.md).
- Access to the Azure Application Insights resource connected to your project. For background, see [Azure Application Insights](/azure/azure-monitor/app/app-insights-overview).

> [!NOTE]
> Tracing stores telemetry data in Azure Application Insights, which may incur costs based on data volume and retention settings. For pricing details, see [Application Insights pricing](/azure/azure-monitor/cost-usage#application-insights-billing).

## OpenTelemetry in Foundry

OpenTelemetry (OTel) provides standardized protocols for collecting and routing telemetry data. Foundry uses OpenTelemetry semantic conventions so traces are consistent across supported tools and integrations.

## Trace key concepts

Here's a brief overview of key concepts before getting started:

| Key concepts             | Description            |
|---------------------|-----------------------------------------------------------------|
| Traces              | Traces capture the journey of a request or workflow through your application by recording events and state changes (function calls, values, system events). See [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/). |
| Spans               | Spans are the building blocks of traces, representing single operations within a trace. Each span captures start and end times, attributes, and can be nested to show hierarchical relationships, allowing you to see the full call stack and sequence of operations.                                                                                         |
| Attributes          | Attributes are key-value pairs attached to traces and spans, providing contextual metadata such as function parameters, return values, or custom annotations. These enrich trace data making it more informative and useful for analysis.                                                                                                 |
| Semantic conventions| OpenTelemetry defines semantic conventions to standardize names and formats for trace data attributes, making it easier to interpret and analyze across tools and platforms. To learn more, see [OpenTelemetry's Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).                  |
| Trace exporters     | Trace exporters send trace data to backend systems for storage and analysis. In Foundry, traces are stored in Azure Monitor Application Insights. To learn how to enable and view traces, see [How to set up tracing in Microsoft Foundry](../how-to/trace-agent-setup.md). |

## How tracing works in Foundry

Tracing helps you answer questions like "Where did this response come from?" and "Which step introduced an error or latency spike?"

At a high level, tracing captures:

- User inputs and agent outputs.
- Tool usage, including tool calls and results.
- Timing signals such as latency.

Once tracing is enabled for your project, you can inspect traces in the Foundry portal and in Azure Monitor Application Insights. For the step-by-step setup and viewing options, see [How to set up tracing in Microsoft Foundry](../how-to/trace-agent-setup.md).

## Extending OpenTelemetry with multi-agent observability

Microsoft, in collaboration with Cisco Outshift, has introduced new semantic conventions for multi-agent systems, built on [OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/) and [W3C Trace Context](https://www.w3.org/TR/trace-context/). These conventions standardize telemetry for multi-agent workflows, enabling consistent logging of metrics for quality, performance, safety, and cost, including tool invocations and collaboration.

These enhancements are integrated into:

- Foundry
- Microsoft Agent Framework
- Semantic Kernel
- LangChain
- LangGraph
- OpenAI Agents SDK

To learn more, see [tracing integrations](../how-to/trace-agent-framework.md).

The following table describes the semantic conventions for multi-agent observability. Spans capture discrete operations, child spans show nested operations within a parent span, attributes provide metadata, and events mark significant occurrences during execution.

| Type         | Context/Parent Span   | Name/Attribute/Event           | Purpose |
|--------------|----------------------|-------------------------------|---------------|
| Span         | —                    | execute_task                  | Captures task planning and event propagation, providing insights into how tasks are decomposed and distributed. |
| Child Span   | invoke_agent         | agent_to_agent_interaction    | Traces communication between agents. |
| Child Span   | invoke_agent         | agent.state.management        | Effective context, short or long term memory management. |
| Child Span   | invoke_agent         | agent_planning                | Logs the agent's internal planning steps. |
| Child Span   | invoke_agent         | agent orchestration           | Captures agent-to-agent orchestration. |
| Attribute    | invoke_agent         | tool_definitions              | Describes the tool's purpose or configuration. |
| Attribute    | invoke_agent         | llm_spans                     | Records model call spans. |
| Attribute    | execute_tool         | tool.call.arguments           | Logs the arguments passed during tool invocation. |
| Attribute    | execute_tool         | tool.call.results             | Records the results returned by the tool. |
| Event        | —                    | Evaluation (name, error.type, label) | Enables structured evaluation of agent performance and decision-making. |

## Best practices

- **Use consistent span attributes**: Apply the same attribute names and formats across all agents and tools to simplify querying and analysis.
- **Correlate evaluation run IDs**: Link trace data with evaluation runs to analyze both quality and performance in a unified view.
- **Redact sensitive content**: Remove or mask personal data, secrets, and credentials from prompts, tool arguments, and span attributes before they reach telemetry.

## Security and privacy

Tracing can capture sensitive information (for example, user inputs, model outputs, and tool arguments and results). Use these practices to reduce risk:

- Don't store secrets, credentials, or tokens in prompts, tool arguments, or span attributes.
- Redact or minimize personal data and other sensitive content before it appears in telemetry.
- Treat trace data as production telemetry and apply the same access controls and retention policies you use for logs and metrics.

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
- [Observability in generative AI](../../../concepts/observability.md)
