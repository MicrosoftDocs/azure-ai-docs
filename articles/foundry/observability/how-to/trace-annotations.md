---
title: Annotate traces with human feedback
description: Learn how to annotate traces with thumbs up or thumbs down feedback in Microsoft Foundry to track quality signals directly on production traces.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 06/15/2026
ai-usage: ai-assisted
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-observability
---

# Annotate traces with human feedback (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Add thumbs up or thumbs down annotations to traces in Microsoft Foundry to capture human quality signals on individual agent interactions. Trace annotations let you mark whether an agent response was helpful or unhelpful, and they appear inline on the trace detail page so you can quickly identify patterns in agent behavior.

Trace annotations support two workflows:

- **Builder annotations:** Builders and domain experts annotate traces from the Foundry portal while reviewing agent interactions. These annotations are automatically tagged with a source of `builder`.
- **End user feedback:** Log annotations programmatically from your application when end users provide thumbs up or thumbs down feedback. These annotations carry a source of `end_user` and appear on the trace page alongside builder annotations. For details on logging end user feedback, see [Log end user feedback](log-end-user-feedback.md).

All annotations are **appended** to the trace—adding a builder annotation never overwrites or replaces existing end-user feedback, and vice versa. Each annotation carries a source attribute so the signals remain independently queryable and filterable.

## Prerequisites

- A Foundry project with an [Application Insights resource](/azure/azure-monitor/app/app-insights-overview) connected. See [Set up tracing](trace-agent-setup.md).
- OpenTelemetry instrumentation configured in your application. See [Set up tracing in Microsoft Foundry](trace-agent-setup.md) for setup instructions.
- For programmatic annotations: the `azure-ai-projects` and `azure-monitor-opentelemetry` packages installed.

  ```bash
  pip install "azure-ai-projects>=2.0.0" azure-monitor-opentelemetry python-dotenv
  ```

## Default scoring template

Every Foundry project is preseeded with a default thumbs up/down scoring template that is immediately available with no additional setup. You can start annotating traces on day one. The default template uses binary pass/fail scoring:

- **Thumbs up** = score `1.0`, label `pass`
- **Thumbs down** = score `0.0`, label `fail`

Each scoring template requires a `gen_ai.evaluation.name attribute` to have value `task_completion` so every annotation is attributable to a specific evaluation dimension. `task_completion` supports thumbs up and down.  

## Annotate traces in the Foundry portal

Add annotations directly from the trace detail page to record your assessment of agent responses.

1. Open your Foundry project and navigate to **Tracing** in the left navigation.
1. Select a trace to open the trace detail view.
1. On the trace detail page, select the **Annotate** button in the upper-right corner.
1. Select **Thumbs up** or **Thumbs down** to submit your score. Optionally add a free-text explanation.
1. The annotation saves immediately and appears on the trace.

:::image type="content" source="../../media/observability/trace-annotations.png" alt-text="Screenshot of the Annotations tab on the trace detail page in the Foundry portal." lightbox="../../media/observability/trace-annotations.png":::

Annotations you add from the portal are automatically tagged with:

- `microsoft.gen_ai.human_evaluation.source` = `"builder"`
- Records will be with `microsoft.gen_ai.evaluation.actor.type` as `"human"`

### Score editing

Each user can annotate multiple times, however:

- Multiple users can each have their own annotation of the same type on the same trace.
- Prior annotations are never deleted in Application Insights, new annotations are appended, and the portal displays all annotations in *Annotation History* section of annotation panel.

## Log end user feedback as trace annotations

When end users provide thumbs up or thumbs down feedback in your application, you can log that feedback so it appears as annotations on the corresponding trace. This approach uses the `gen_ai.evaluation.result` OpenTelemetry event, with the feedback automatically correlated to the originating trace.

### Annotation attribute schema

Use the following attributes when you emit a thumbs up or thumbs down annotation:

| Attribute | Value | Description |
|-----------|-------|-------------|
| `gen_ai.evaluation.name` | `task_completion` | Evaluation metric name |
| `gen_ai.evaluation.score.value` | `1.0` (thumbs up) or `0.0` (thumbs down) | Numeric score |
| `gen_ai.evaluation.score.label` | `"pass"` or `"fail"` | Categorical label |
| `gen_ai.evaluation.explanation` | Optional free-text comment | Reviewer explanation |
| `gen_ai.response.id` | For example, `"chatcmpl-123"` | AI response ID used to correlate the annotation with the traced response |
| `microsoft.gen_ai.human_evaluation.source` | `"end_user"` or `"builder"` | Feedback provider type |
| `microsoft.gen_ai.evaluation.actor.type` | `"human"` | Indicates the annotation was submitted by a human reviewer, distinguishing it from automated evaluations |
| `operation_Id` | `trace_Id` | Links the annotation to the original trace request in Application Insights |
| `operation_ParentId` | `span_Id` | Includes span ID of the specific span within the trace being annotated |
| `gen_ai.agent.id` | Agent resource identifier string | Unique identifier of the agent that produced the response being annotated |
| `gen_ai.agent.name` | Agent display name string | Display name of the agent that produced the response being annotated |
| `gen_ai.agent.version` | Version string `1`, `2`, or `3` | Located inside `internal_properties`, version of the agent at the time the annotated response was produced |

You must emit the evaluation event within the same trace context (using the same trace ID and span ID) as the agent interaction it annotates. This correlation ensures the annotation appears on the correct trace in the portal.

For a complete runnable example, see [sample_human_evaluations.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_human_evaluations.py).

## View annotations on the trace page

After you add annotations (from the portal or programmatically), they appear on the trace detail page.

1. Open your Foundry project and go to **Tracing**.
1. Select a trace that has annotations.
1. On the trace detail page, annotation icons appear next to the annotated spans. A thumbs up icon indicates positive feedback and a thumbs down icon indicates negative feedback.
1. Hover over an annotation to see metadata, including the source (`builder` or `end_user`), evaluation name, and timestamp.

In the trace list view, annotations display with a compact treatment: only the most recent annotation shows inline, and when multiple annotations exist on a trace, a "+X more" indicator signals additional annotations are available. Select the trace to see all annotations.

### Filter traces by annotation

You can filter the trace list by:

- **Evaluation type** (`gen_ai.evaluation.name`): value is `"task_completion"`.
- **Score value or label** (`gen_ai.evaluation.score.value`, `gen_ai.evaluation.score.label`): for example, show only traces with a thumbs-down rating.
- **Source** (`microsoft.gen_ai.human_evaluation.source`): show only builder annotations or only end-user feedback.

These filter dimensions appear alongside existing trace filters (time range, agent, status, model).

## Query annotations in Application Insights

All annotations are published to Azure Monitor / Application Insights and attached to the original trace. You can query annotations by using Kusto Query Language (KQL) to analyze feedback patterns, build dashboards, or set up alerts.

### Summarize feedback by source and day

```kusto
customEvents
| where name == "gen_ai.evaluation.result"
| extend
    eval_name = tostring(customDimensions["task_completion"]),
    score = todouble(customDimensions["gen_ai.evaluation.score.value"]),
    label = tostring(customDimensions["gen_ai.evaluation.score.label"]),
    eval_source = tostring(customDimensions["microsoft.gen_ai.human_evaluation.source"]),
    trace_id = tostring(customDimensions["trace_id"])
| where eval_source in ("builder", "end_user")
| summarize
    thumbs_up = countif(score == 1.0),
    thumbs_down = countif(score == 0.0),
    total = count()
  by eval_source, bin(timestamp, 1d)
| order by timestamp desc
```

### Find traces with negative feedback

```kusto
customEvents
| where name == "gen_ai.evaluation.result"
| extend
    eval_name = tostring(customDimensions["task_completion"]),
    score = todouble(customDimensions["gen_ai.evaluation.score.value"]),
    eval_source = tostring(customDimensions["microsoft.gen_ai.human_evaluation.source"]),
    explanation = tostring(customDimensions["gen_ai.evaluation.explanation"]),
    trace_id = tostring(customDimensions["trace_id"])
| where score == 0.0
| project timestamp, trace_id, eval_name, eval_source, explanation
| order by timestamp desc
```

## Related content

- [Log end user feedback](log-end-user-feedback.md)
- [Set up tracing in Microsoft Foundry](trace-agent-setup.md)
- [Review agent interactions with Trace Replay](trace-agent-replay.md)
- [Monitor agents with the Agent Monitoring Dashboard](how-to-monitor-agents-dashboard.md)
