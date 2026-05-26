---
title: Log end user feedback
description: Learn how to log end user feedback such as thumbs up/down or rating scales from your AI application using OpenTelemetry semantics in Microsoft Foundry.
ms.service: microsoft-foundry
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 05/22/2026
ms.topic: how-to
ms.custom: doc-kit-assisted
---

# Log end user feedback (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Capture end user feedback—such as thumbs up/down reactions or numeric rating scales—from your AI application and route it to your observability backend using OpenTelemetry (OTel) semantics. Logging user feedback enables you to correlate subjective quality signals with trace data, measure user satisfaction over time, and drive continuous improvement of your agents and models.

## Overview

End user feedback logging uses OTel semantic conventions to emit structured feedback events that are associated with a specific trace or span. This means feedback data flows through the same telemetry pipeline as your traces and metrics, giving you a unified view of application behavior and user sentiment.

Key capabilities:

- **Thumbs up/down** — Record binary user approval signals tied to a specific agent response.
- **Rating scale** — Capture numeric scores (for example, 1–5 stars) to quantify user satisfaction.
- **Trace correlation** — Each feedback event links back to the originating trace and span, enabling drill-down from aggregate satisfaction metrics to individual interactions.
- **Standard OTel transport** — Feedback events use the OpenTelemetry Events API, so they're exported through your existing OTel pipeline to Application Insights or any compatible backend.

## Prerequisites

- A Foundry project with an [Application Insights resource](/azure/azure-monitor/app/app-insights-overview) connected. See [Set up tracing](trace-agent-setup.md).
- OpenTelemetry instrumentation configured in your application. See [Set up tracing in Microsoft Foundry](trace-agent-setup.md) for setup instructions.
- Python 3.9 or later, or a supported language with OTel SDK support.
- The `opentelemetry-api` and `opentelemetry-sdk` packages installed:

  ```bash
  pip install opentelemetry-api opentelemetry-sdk
  ```

## Evaluation types

Human feedback is captured as a `gen_ai.evaluation.result` OpenTelemetry event. Two evaluation types are supported:

| Type | Description | UI rendering | Score range |
|------|-------------|--------------|-------------|
| **Binary** | A pass/fail evaluation. | Thumbs up or thumbs down | `0.0` (fail) or `1.0` (pass) |
| **Likert 5-point** | An ordinal evaluation on a 5-point scale. | 5-star rating or Likert scale (Strongly Disagree → Strongly Agree) | `1.0` to `5.0` |

Feedback can originate from two source types:

- **Builder** — A human evaluating with a Microsoft observability solution, such as in Foundry or Azure Monitor portal.
- **End user** — A human evaluating through an application interface that a Microsoft observability solution is monitoring.

## Event attributes

Each human evaluation is emitted as a `gen_ai.evaluation.result` event with the following top-level attributes:

| Attribute | Requirement Level | Type | Description | Example |
|-----------|-------------------|------|-------------|---------|
| `microsoft.custom_event.name` | Required | `string` | Must be `"gen_ai.evaluation.result"`. Routes the event to the `customEvents` table in Application Insights. | `"gen_ai.evaluation.result"` |
| `gen_ai.evaluation.name` | Required | `string` | The name of the evaluation metric. | `"task_completion"`, `"relevance"` |
| `gen_ai.evaluation.score.value` | Required | `double` | The numeric score. | `1.0`, `4.0` |
| `gen_ai.evaluation.score.label` | Required | `string` | Must be `"pass"` or `"fail"`. | `"pass"` |
| `gen_ai.evaluation.explanation` | Optional | `string` | Free-form explanation for the score. | `"The agent provided accurate information."` |
| `gen_ai.response.id` | Optional (recommended) | `string` | ID of the completion being evaluated. Helps correlate evaluation with the operation. | `"resp_64904952b208..."` |
| `enduser.id` | Optional (recommended) | `string` | Authenticated user identifier. Maps to `user_AuthenticatedId` in Application Insights. | `"oid:e37ded2a-b026-..."` |
| `enduser.pseudo.id` | Optional (recommended) | `string` | Pseudonymous user identifier. Maps to `user_Id` in Application Insights. | `"QdH5CAWJgqVT4rOr0qtumf"` |
| `microsoft.human_evaluation.tags.<tag>` | Optional | `string` | Custom metadata key-value pairs. | `"basic_plan"` (for `microsoft.human_evaluation.tags.subscription_tier`) |
| `microsoft.human_evaluation.id` | Optional (recommended) | `string` | Unique ID for the evaluation event itself. | `"69d937a7-32e2-412e-..."` |
| `error.type` | Conditionally required (on error) | `string` | Error class if the operation failed. | `"timeout"`, `"500"` |
| `internal_properties` | Required | `string` | JSON-encoded string with additional metadata. See [Internal properties](#internal-properties). | See examples below. |

### Internal properties

The `internal_properties` attribute is a JSON-encoded string containing metadata required by downstream Microsoft systems (Azure Monitor, Foundry). The following fields apply to human evaluations:

| Attribute | Requirement Level | Type | Description | Example |
|-----------|-------------------|------|-------------|---------|
| `gen_ai.evaluation.type` | Required | `string` | Value type: `"boolean"`, `"ordinal"`, or `"continuous"`. | `"boolean"` |
| `gen_ai.evaluation.min_value` | Required | `double` | Minimum possible score value. | `0.0` |
| `gen_ai.evaluation.max_value` | Required | `double` | Maximum possible score value. | `1.0` |
| `gen_ai.evaluation.threshold` | Required | `double` | Score at or above which the evaluation is a pass. | `1.0` |
| `gen_ai.evaluation.desirable_direction` | Required | `string` | Direction of improvement: `"increase"` or `"decrease"`. | `"increase"` |
| `microsoft.human_evaluation.source` | Required | `string` | Who performed the evaluation: `"builder"` or `"end_user"`. | `"end_user"` |
| `microsoft.human_evaluation.kind` | Required | `string` | Evaluation kind: `"binary"` or `"likert_5"`. | `"binary"` |
| `gen_ai.azure_ai_project.id` | Conditionally required (Foundry agents) | `string` | Azure resource ID for the Foundry project. | `"/subscriptions/.../projects/my-proj"` |
| `gen_ai.response.id.type` | Conditionally required (when `gen_ai.response.id` is set) | `string` | Clarifies what the response ID represents. | `"responses"`, `"session"` |
| `gen_ai.evaluation.azure_ai_scheduled` | Not required | `string` | Use `"one_off"` for human evaluations. | `"one_off"` |

## Emit a binary evaluation (thumbs up/down)

Binary evaluations capture pass/fail feedback. The score must be `0.0` (fail) or `1.0` (pass).

Rules:

- `gen_ai.evaluation.score.value`: `0.0` or `1.0`
- `gen_ai.evaluation.score.label`: `"fail"` or `"pass"`
- `internal_properties.gen_ai.evaluation.type`: `"boolean"`
- `internal_properties.gen_ai.evaluation.min_value`: `0.0`
- `internal_properties.gen_ai.evaluation.max_value`: `1.0`
- `internal_properties.gen_ai.evaluation.threshold`: `1.0`
- `internal_properties.gen_ai.evaluation.desirable_direction`: `"increase"`
- `internal_properties.microsoft.human_evaluation.kind`: `"binary"`

### Example: End user gives thumbs up

For a complete Python implementation of binary feedback logging, see the [Azure SDK for Python sample](https://github.com/Azure/azure-sdk-for-python/pull/46962/files).

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
- `internal_properties.microsoft.human_evaluation.kind`: `"likert_5"`

### Example: End user rates relevance

For a complete Python implementation of Likert 5-point feedback logging, see the [Azure SDK for Python sample](https://github.com/Azure/azure-sdk-for-python/pull/46962/files).

## View feedback in Application Insights

After feedback events are exported through your OTel pipeline, they appear in the `customEvents` table in Application Insights with `name == "gen_ai.evaluation.result"`. You can query and visualize this data using Log Analytics.

To learn how to view and query telemetry in Application Insights, see [View and analyze traces](trace-agent-setup.md#view-and-analyze-traces). For dashboard-based monitoring, see [Monitor agents with the Agent Monitoring Dashboard](how-to-monitor-agents-dashboard.md).

## Related content

- [Set up tracing in Microsoft Foundry](trace-agent-setup.md)
- [Monitor agents with the Agent Monitoring Dashboard](how-to-monitor-agents-dashboard.md)
- [Tracing integrations](trace-agent-framework.md)
