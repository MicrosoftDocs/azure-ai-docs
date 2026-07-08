---
title: "Migrate from stored completions to Responses API and Agent Traces in Microsoft Foundry (classic)"
description: "Learn how to migrate stored completions to Responses API and Agent Traces"
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.custom: references_regions
ms.date: 07/6/2026
author: alvinashcraft
ms.author: aashcraft
recommendations: false
---

# Migrate from stored completions to Responses API and Agent Traces in Microsoft Foundry (classic)

> [!IMPORTANT]
> Microsoft Foundry is retiring stored completions on October 15, 2026. After that date, the Stored Completions UI and API stop working.

This article helps you identify stored completions usage, choose the right replacement pattern, and move your workflows before retirement.

## Prerequisites

- A Microsoft Foundry project or Azure OpenAI resource where you use stored completions.
- Access to the application code, tools, or operational workflows that use stored completions.
- Access to any evaluation or fine-tuning workflows that rely on stored completions data.

## Why migrate

Stored completions are retiring. After October 15, 2026:

- The Stored Completions UI stops working.
- The Stored Completions API stops working.
- You can't use stored completions as a source for new workflows.

Migrate because different stored completions scenarios now map to different alternatives:

- Use the [Responses API](/azure/foundry/openai/how-to/responses) for response generation and response-based application workflows.
- Use [Agent Traces](/azure/foundry/observability/concepts/trace-agent-concept) for agent observability, debugging, trace-based evaluation, and finetuning datasets.

## Foundry-specific considerations

### Stored completions capture Chat Completions input and output

Stored completions capture model input and output from Chat Completions usage.

### Existing stored completions can't be exported or migrated

You can't directly export or migrate existing stored completions.

### Retention behavior remains time based

Stored completions data follows a rolling 30-day retention window from the date each stored completion is created.

After retirement, Microsoft cleans up service and storage to remove remaining service-owned resources.

### Choose an alternative based on your scenario

The recommended alternative depends on how you use stored completions today.

Use the Responses API for response workflows. Use Agent Traces for agent observability, trace-based evaluation, and finetuning datasets.

### Responses API doesn't require a special framework

You don't need a special framework to use the Responses API. You can call the Responses API directly through REST or a supported SDK.

### Agent Traces apply to agent workflows

[Agent Traces](/azure/foundry/observability/concepts/trace-agent-concept) are useful when you need to inspect agent runs, troubleshoot behavior, review tool calls, or create evaluation datasets from agent activity.

Agent Traces setup depends on how your agent is built:

- For Foundry-hosted agents or prompt agents, [connect the Foundry project to Application Insights](/azure/foundry/observability/how-to/trace-agent-setup) to view traces.
- For custom agents outside Foundry, use the [tracing setup for your agent framework or instrumentation](/azure/foundry/observability/how-to/trace-agent-framework).

If your workflow doesn't use agents or doesn't have traces, start with the Responses API instead.

Trace data is stored in the Application Insights resource connected to your Foundry project. Data retention follows your Application Insights and Log Analytics configuration. In the Foundry portal, you can search, filter, or sort ingested traces from the last 90 days.

## Key concept mapping

Use this table to map your stored completions scenario to the recommended alternative.

| Stored completions scenario | Recommended alternative | Details |
| --- | --- | --- |
| Continue generating model responses | Responses API | Move response generation to the Responses API. |
| Maintain multi-turn response context | Responses API | Use `previous_response_id` or carry response output items forward. |
| Stream generated output | Responses API | Use Responses API streaming. |
| Use tool or function calling | Responses API | Use Responses API tools or function calling. |
| Debug or review agent behavior | Agent Traces | Enable tracing and review agent runs in Foundry or Application Insights. |
| Create evaluation datasets from agent behavior | Agent Traces to datasets | Generate evaluation datasets from traces when agent traces are available. |

## Migration plan

Work through these steps before October 15, 2026.

1. **Inventory usage.** Find all stored completions usage in code, tools, and operational workflows. Search for Chat Completions calls that set `store=True` or `store: true`, Stored Completions UI usage, and Stored Completions API usage.

1. **Classify each workflow.** Decide whether each workflow is for response generation, multi-turn response state, agent debugging, or evaluation dataset generation.

1. **Move response workflows.** Use the Responses API for response generation, multi-turn response flows, streaming, and tool or function calling. You can call the Responses API through REST or a supported SDK.

1. **Move agent observability workflows.** Use Agent Traces when you need to inspect agent runs, troubleshoot behavior, review tool calls, or create evaluation datasets from agent activity. Connect Foundry-hosted agents to Application Insights, or configure tracing for your custom agent framework.

1. **Stop creating new dependencies.** Don't build new workflows that depend on stored completions.

## Frequently asked questions

### Can I export existing stored completions?

No. You can't directly export or migrate existing stored completions.

### Can Microsoft migrate my existing stored completions to Responses API or Agent Traces?

No. Responses API and Agent Traces are alternatives for future workflows. They aren't migration mechanisms for existing stored completions.

### What happens after October 15, 2026?

The Stored Completions UI and API stop working.

### What happens to existing stored completions data?

Stored completions data follows a rolling 30-day retention window from the date each stored completion is created.

### Will existing jobs created from stored-completions datasets continue to work?

Yes. Existing jobs created from stored-completions datasets continue to work. The training and validation file references for those jobs continue to work after stored completions is retired.

### What should I do if I have a business-critical need for existing stored completions data?

Contact support with your subscription ID, scenario, business impact, timeline, and required data format. Export or migration support isn't currently available and shouldn't be assumed.

## Related content

- [Azure OpenAI stored completions and distillation preview](/azure/ai-foundry/openai/how-to/stored-completions?tabs=python-secure)
- [Use the Azure OpenAI Responses API](/azure/foundry/openai/how-to/responses)
- [Agent tracing overview](/azure/foundry/observability/concepts/trace-agent-concept)
- [Set up tracing in Microsoft Foundry](/azure/foundry/observability/how-to/trace-agent-setup)
- [Convert agent traces into evaluation datasets](/azure/foundry/observability/how-to/traces-to-dataset)
- [Data, privacy, and security for Models sold by Azure in Microsoft Foundry](/azure/foundry/responsible-ai/openai/data-privacy)
