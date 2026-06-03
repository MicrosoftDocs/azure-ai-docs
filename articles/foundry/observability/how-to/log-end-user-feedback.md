---
title: Log end user feedback
description: Learn how to log end user feedback such as thumbs up/down or rating scales from your AI application using OpenTelemetry semantics in Microsoft Foundry.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 06/02/2026
ai-usage: ai-assisted
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-observability
---

# Log end user feedback (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Capture end user feedback, such as thumbs up or thumbs down reactions or numeric rating scales, from your AI application and route it to your observability backend by using OpenTelemetry (OTel) semantics. When you log user feedback, you can correlate subjective quality signals with trace data, measure user satisfaction over time, and drive continuous improvement of your agents and models.

## Overview

End user feedback logging uses OTel semantic conventions to emit structured feedback events that are associated with a specific trace or span. This means feedback data flows through the same telemetry pipeline as your traces and metrics, giving you a unified view of application behavior and user sentiment.

Key capabilities:

- **Thumbs up or thumbs down:** Record binary user approval signals that tie to a specific agent response.
- **Rating scale:** Capture numeric scores, such as 1–5 stars, to quantify user satisfaction.
- **Trace correlation:** Each feedback event links back to the originating trace and span, so you can drill down from aggregate satisfaction metrics to individual interactions.
- **Standard OTel transport:** Feedback events use the OpenTelemetry Events API, so they're exported through your existing OTel pipeline to Application Insights or any compatible backend.

## Prerequisites

- A Foundry project with an [Application Insights resource](/azure/azure-monitor/app/app-insights-overview) connected. See [Set up tracing](trace-agent-setup.md).
- OpenTelemetry instrumentation configured in your application. See [Set up tracing in Microsoft Foundry](trace-agent-setup.md) for setup instructions.
- Python 3.9 or later, or a supported language with OTel SDK support.
- The `azure-ai-projects` and `azure-monitor-opentelemetry` packages installed:

  ```bash
  pip install "azure-ai-projects>=2.0.0" azure-monitor-opentelemetry python-dotenv
  ```

## Evaluation types

Capture human feedback as a `gen_ai.evaluation.result` OpenTelemetry event. The system supports two evaluation types:

| Type | Description | UI rendering | Score range |
|------|-------------|--------------|-------------|
| **Binary** | A pass/fail evaluation. | Thumbs up or thumbs down | `0.0` (fail) or `1.0` (pass) |
| **Likert 5-point** | An ordinal evaluation on a 5-point scale. | 5-star rating or Likert scale (Strongly Disagree → Strongly Agree) | `1.0` to `5.0` |

Two source types can provide feedback:

- **Builder:** A human evaluating with a Microsoft observability solution, such as in Foundry or Azure Monitor portal.
- **End user:** A human evaluating through an application interface that a Microsoft observability solution is monitoring.

## Event attributes

Each human evaluation is emitted as a `gen_ai.evaluation.result` event. The following sections describe the required attributes for each evaluation type. For a complete reference implementation, see [sample_human_evaluations.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_human_evaluations.py).

## Emit a binary evaluation (thumbs up or down)

Binary evaluations capture pass or fail feedback. The score must be `0.0` (fail) or `1.0` (pass).

Rules:

- `gen_ai.evaluation.score.value`: `0.0` or `1.0`
- `gen_ai.evaluation.score.label`: `"fail"` or `"pass"`
- `internal_properties.gen_ai.evaluation.type`: `"boolean"`
- `internal_properties.gen_ai.evaluation.min_value`: `0.0`
- `internal_properties.gen_ai.evaluation.max_value`: `1.0`
- `internal_properties.gen_ai.evaluation.threshold`: `1.0`
- `internal_properties.gen_ai.evaluation.desirable_direction`: `"increase"`

### Example: End user gives thumbs up

For a runnable example, see [sample_human_evaluations.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_human_evaluations.py).

## Emit a Likert 5-point evaluation (rating scale)

Likert 5-point evaluations capture ordinal feedback on a 1–5 scale. A score at or above the threshold (default `3.0`) is considered a pass.

Rules:

- `gen_ai.evaluation.score.value`: a value between `1.0` and `5.0`
- `gen_ai.evaluation.score.label`: `"pass"` if score ≥ threshold, otherwise `"fail"`
- `internal_properties.gen_ai.evaluation.type`: `"ordinal"`
- `internal_properties.gen_ai.evaluation.min_value`: `1.0`
- `internal_properties.gen_ai.evaluation.max_value`: `5.0`
- `internal_properties.gen_ai.evaluation.threshold`: `3.0`
- `internal_properties.gen_ai.evaluation.desirable_direction`: `"increase"`

### Example: Builder rates relevance in Foundry portal

For a runnable example, see [sample_human_evaluations.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_human_evaluations.py).

## View feedback in Application Insights

After feedback events are exported through your OTel pipeline, you can query them in Application Insights using KQL:

```kusto
customEvents
| where name == "gen_ai.evaluation.result"
| extend
    eval_name = tostring(customDimensions["gen_ai.evaluation.name"]),
    score = todouble(customDimensions["gen_ai.evaluation.score.value"]),
    label = tostring(customDimensions["gen_ai.evaluation.score.label"]),
    eval_source = tostring(customDimensions["microsoft.gen_ai.human_evaluation.source"]),
    internal = parse_json(tostring(customDimensions["internal_properties"]))
| extend
    eval_type = tostring(internal["gen_ai.evaluation.type"])
| where eval_source in ("builder", "end_user")
| summarize
    total = count(),
    pass_rate = round(countif(label == "pass") * 100.0 / count(), 1),
    avg_score = round(avg(score), 2)
  by eval_name, eval_type, bin(timestamp, 1h)
| order by timestamp desc
```

## Related content

- [Set up tracing in Microsoft Foundry](trace-agent-setup.md)
- [Monitor agents with the Agent Monitoring Dashboard](how-to-monitor-agents-dashboard.md)
- [Tracing integrations](trace-agent-framework.md)
