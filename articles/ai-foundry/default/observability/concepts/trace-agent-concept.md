---
title: Agent Tracing Overview
titleSuffix: Microsoft Foundry
description: "Discover how Microsoft Foundry's tracing tools simplify debugging AI agents by capturing inputs, outputs, and tool usage for better observability."
ai-usage: ai-assisted
author: yanchen-ms
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 11/18/2025
ms.service: azure-ai-foundry
ms.topic: how-to
---
# Agent tracing overview (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

Microsoft Foundry provides an observability platform for monitoring and tracing AI agents. It captures everything happening during an agent run: inputs, outputs, tool usage, retries, latencies, and costs. Understanding the reasoning behind your agent's executions is important for troubleshooting and debugging. However, it can be difficult for complex agents for many reasons:

- There could be a high number of steps involved in generating a response, making it hard to keep track of all of them.
- The sequence of steps might vary based on user input.
- The inputs/outputs at each stage might be long and deserve more detailed inspection.
- Each step of an agent's runtime might also involve nesting. For example, an agent might invoke a tool, which uses another process, which then invokes another tool. If you notice strange or incorrect output from a top-level agent run, it might be difficult to determine exactly where in the execution the issue was introduced.

Trace results solve this by allowing you to view the inputs and outputs of each primitive involved in a particular agent run, displayed in the order they were invoked, making it easy to understand and debug your AI agent's behavior.

> [!NOTE]
> Agent tracing is only available in Sweden Central in Foundry (new).

## OpenTelemetry in Foundry

OpenTelemetry (OTel) provides standardized protocols for collecting and routing telemetry data. Foundry supports multiple ways to collect and analyze tracing data from OpenTelemetry-instrumented agents, whether you’re using Foundry infrastructure or a vendor-neutral setup.

## Trace key concepts overview

Here's a brief overview of key concepts before getting started:

| Key concepts             | Description            |
|---------------------|-----------------------------------------------------------------|
| Traces              | Traces capture the journey of a request or workflow through your application by recording events and state changes (function calls, values, system events). See [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/). |
| Spans               | Spans are the building blocks of traces, representing single operations within a trace. Each span captures start and end times, attributes, and can be nested to show hierarchical relationships, allowing you to see the full call stack and sequence of operations.                                                                                         |
| Attributes          | Attributes are key-value pairs attached to traces and spans, providing contextual metadata such as function parameters, return values, or custom annotations. These enrich trace data making it more informative and useful for analysis.                                                                                                 |
| Semantic conventions| OpenTelemetry defines semantic conventions to standardize names and formats for trace data attributes, making it easier to interpret and analyze across tools and platforms. To learn more, see [OpenTelemetry's Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).                  |
| Trace exporters     | Trace exporters send trace data to backend systems for storage and analysis. Azure AI supports exporting traces to Azure Monitor and other OpenTelemetry-compatible platforms, enabling integration with various observability tools.   |

## Extending OpenTelemetry with multi-agent observability

Microsoft, in collaboration with Cisco Outshift, has introduced new semantic conventions for multi-agent systems, built on [OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/) and W3C Trace Context-establish standardized practices. These conventions standardize telemetry for multi-agent workflows, enabling consistent logging of metrics for quality, performance, safety, and cost, including tool invocations and collaboration.

These enhancements are integrated into:

- Foundry
- Microsoft Agent Framework
- Semantic Kernel
- LangChain
- LangGraph
- OpenAI Agents SDK

To learn more, see [tracing integrations](../how-to/trace-agent-framework.md).

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

- Use consistent span attributes.
- Correlate evaluation run IDs for quality + performance analysis.
- Redact sensitive content; avoid storing secrets in attributes.

## Related content

- [Tracing integrations](../how-to/trace-agent-framework.md)
