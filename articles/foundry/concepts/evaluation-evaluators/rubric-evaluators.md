---
title: "Rubric Evaluators"
description: "Learn about rubric evaluators for AI agents, which let you define custom scoring criteria with descriptive rubrics for LLM-as-judge evaluation."
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 05/12/2026
ms.service: microsoft-foundry
ms.topic: reference

---

# Rubric evaluators (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

A *rubric* is a set of criteria that defines how to rate the response of an LLM model or agent. Each rubric contains score levels with descriptions that specify what qualifies for each rating, so evaluation results are consistent and aligned with your quality standards.

Rubric evaluators let you define custom scoring criteria with descriptive rubrics that an LLM judge uses to assess AI-generated responses. Instead of relying on a single built-in metric, you provide a rubric that describes what each score level means, giving you full control over the evaluation logic while using an LLM to apply the rubric consistently at scale.

Use rubric evaluators when built-in evaluators don't capture domain-specific quality requirements. For example, you might define rubrics for brand compliance, technical accuracy in a specialized domain, or response formatting standards.

## Generate a rubric evaluator

You can create a rubric evaluator in two ways:

### Auto-generate a rubric (recommended)

You can automatically create a rubric evaluator by selecting your LLM model for your agent’s specific context. Provide any of these inputs to guide the rubric generation:

- **Agent system prompt (required)** — Select a prompt agent or provide the instructions that define your agent's intended behavior.
- **Traces** — Agent production traces collected from Foundry tracing in Application Insights.
- **Supplementary files or context** — Reference documents, knowledge-base content, or domain guidelines that describe expected response quality.

The service analyzes these inputs to produce quality dimensions and score-level descriptions tailored to your agent. For example, if your agent's prompt emphasizes concise answers with citations, the generated rubric includes dimensions for brevity and source attribution. This approach saves time and produces rubrics closely aligned with your agent's actual use cases.

Each generated rubric contains the following fields:

| Field | Description |
|-------|-------------|
| `dimension_id` | Stable, human-readable slug assigned by the service on first generation. When you edit criteria and save as a new version, echo the existing `dimension_id` to preserve identity across versions. The service doesn't reassign IDs on edit. |
| `description` | What this criterion measures — a clear, specific quality dimension. |
| `weight` | Relative importance of the criterion. The generation pipeline assigns exactly one criterion a weight of 8–10 (the most outcome-decisive dimension) and all others 1–6. User edits aren't constrained by this heuristic. |
| `always_applicable` | When `true`, the LLM judge always scores this criterion regardless of relevance (skips the applicability assessment). Used for the general quality criterion. Defaults to `false`. |

#### Choose an LLM judge model

Not all models perform equally as rubric judges. The following table ranks models by judge quality for both static and adaptive evaluations. Models near the bottom of the list can produce unreliable or inconsistent scores and should be avoided as rubric judges.

| Rank | Model | Recommendation |
|------|-------|----------------|
| 1 | `gpt-5.5` | Recommended |
| 2 | `gpt-5.4` | Recommended |
| 3 | `gpt-5.4-nano` | Recommended |
| 4 | `gpt-5.4-mini` | Recommended |
| 5 | `gpt-5.2` | Recommended |
| 6 | `Grok-4` | Acceptable |
| 7 | `Claude Opus 4.7` | Acceptable |
| 8 | `gpt-4.1` | Acceptable |
| 9 | `gpt-4o` | Not recommended |
| 10 | `gpt-4o-mini` | Not recommended |

> [!IMPORTANT]
> Avoid using `gpt-4o` and `gpt-4o-mini` as rubric judges. These models produce noticeably less reliable scores compared to newer models. For the best balance of performance and cost, use `gpt-5.4-mini`.

### Manually create a rubric

Write your own rubric by defining its `dimension_id`, `description`, and `weight`. Use this approach when you have precise, well-defined criteria that you want to control exactly, or when auto-generation doesn't capture a niche requirement.

> [!TIP]
> Start by creating an auto-generated rubric evaluator and refine it manually. Auto-generation gives you a strong baseline that you can adjust to match your team's specific quality bar.

## Review and adjust the rubric

After you generate or create a rubric, review the dimension to confirm they match your expectations for agent quality. You can:

- **Edit `dimension_id`, `description`, and `weight`** — Refine the language to be more specific about what qualifies for each dimension level. Precise descriptions and weight improve scoring consistency.
- **Add or remove dimensions** — Insert quality dimensions that matter for your domain, or remove ones that don't apply.
- **Adjust thresholds** — Change the pass threshold to set a higher or lower quality bar.
- **Set always applicable** — Select or clear the **Always applicable** checkbox for a criterion. When selected, the LLM judge scores this criterion for every response without checking relevance first.

In the advanced settings for each rubric, you can view the evaluation level and category for this rubric evaluator, and adjust the **Pass score threshold** to control what score qualifies as passing.

Iterate on the rubric until it reliably distinguishes between acceptable and unacceptable agent responses. Run a small evaluation on a sample dataset to validate that the rubric scores align with your own judgment before using it at scale.

## Example rubric

The following example shows a rubric for a restaurant reservation agent. Each criterion targets a specific quality dimension, with weights reflecting relative importance:

```json
[
  {
    "rubric_id": "intent_recognition",
    "description": "Correctly identifies the user's reservation intent (book, modify, cancel, inquire) and pursues the appropriate workflow without unnecessary clarification.",
    "weight": 9
  },
  {
    "rubric_id": "tool_usage_accuracy",
    "description": "Calls the correct tool with correct parameters. Does not call tools unnecessarily, and does not skip tool calls when they are needed.",
    "weight": 6
  },
  {
    "rubric_id": "policy_enforcement",
    "description": "Enforces business rules: dinner service 17:00-22:00, max party size 8, 30-day booking window. Does not create reservations that violate these constraints.",
    "weight": 5
  },
  {
    "rubric_id": "information_gathering",
    "description": "Collects all required information (date, time, party size, contact) before attempting to create a reservation. Does not ask for information already provided.",
    "weight": 4
  },
  {
    "rubric_id": "communication_clarity",
    "description": "Provides clear, concise responses. Confirms reservation details before finalizing. Uses a professional and helpful tone.",
    "weight": 2
  },
  {
    "rubric_id": "general_quality",
    "description": "Other important quality factors not already covered by the listed criteria.",
    "weight": 5,
    "always_applicable": true
  }
]
```

In this rubric, `intent_recognition` has the highest weight (9) because correctly identifying what the user wants is the most outcome-decisive factor. The `general_quality` criterion uses `always_applicable: true` so the judge scores it for every response, even when other criteria might not apply.

# Use rubric evaluators to run evaluation

Rubric evaluators work well for domain-specific or organization-specific quality criteria that general-purpose evaluators can't capture. Define a rubric when you need scoring that reflects your team's specific quality bar - for example, customer support tone, medical accuracy, or legal compliance.

The LLM judge reads the rubric, examines the mapped input data, assigns a score, and provides a reason for its scoring decision. This approach combines the flexibility of custom criteria with the consistency of LLM-based evaluation.

For LLM-as-judge evaluators, you can use Azure OpenAI or OpenAI reasoning and non-reasoning models for the LLM judge.


For details on running evaluations and configuring data sources, see [Run evaluations from the SDK](../../how-to/develop/cloud-evaluation.md).


## Example output

### Pass example

The rubric evaluator returns the score level that best matches your rubric, along with a reason explaining the decision. The default pass threshold is 3. Scores at or above the threshold are considered passing. Key output fields:

```json
{
  "score": 0.8428571429,
  "label": "pass",
  "reason": "The verdict is driven most by task_alignment (5), claim_accuracy (4), and conciseness (5). The assistant correctly searched May 20 flights, picked ANA NH1069 as the cheapest option at $835 from the tool results, booked it, and returned the matching confirmation ANA-77341 in a very compact message.",
  "threshold": 0.5,
  "passed": true,
  "properties": {
    "dimension_scores": [
      {
        "id": "task_alignment",
        "score": 5,
        "applicable": true,
        "weight": 9,
        "reason": "There are no visible shortcomings: the final response does exactly what the user asked by changing the date, selecting the cheapest flight from the search results, booking it, and reporting the confirmation."
      },
      {
        "id": "claim_accuracy",
        "score": 4,
        "applicable": true,
        "weight": 6,
        "reason": "There are no visible factual inconsistencies: ANA NH1069 is the cheapest May 20 option in the tool results at $835, and the confirmation details match the booking tool output."
      },
      {
        "id": "conciseness",
        "score": 5,
        "applicable": true,
        "weight": 4,
        "reason": "There are no unnecessary details or repetition: the assistant communicates the booking outcome, flight, date, price, and confirmation in a single efficient sentence."
      },
      {
        "id": "general_quality",
        "score": 4,
        "applicable": true,
        "weight": 5,
        "reason": "Overall execution is strong: the assistant uses the search and booking tools correctly and provides a clean final confirmation."
      }
    ]
  }
}
```

### Fail example

In this example, the user asks for a Q4 marketing report summary but the agent provides only a generic sign-off, scoring well below the pass threshold:

```json
{
  "score": 0.140625,
  "label": "fail",
  "reason": "The verdict is driven primarily by very low task_alignment (1), coverage (1), uncertainty_handling (1), and general_quality (1): the assistant's final message is just a polite sign-off and does not help with the user's request for a Q4 report summary or ask for the missing report content.",
  "threshold": 0.5,
  "passed": false,
  "properties": {
    "dimension_scores": [
      {
        "id": "task_alignment",
        "score": 1,
        "applicable": true,
        "weight": 9,
        "reason": "The response does not address the user's actual request in this turn; it only offers a generic sign-off after failing to provide a Q4 summary."
      },
      {
        "id": "coverage",
        "score": 1,
        "applicable": true,
        "weight": 5,
        "reason": "It omits the core requested content entirely: no summary of the Q4 marketing report is provided, nor is there any attempt to explain the limitation or request the report content."
      },
      {
        "id": "uncertainty_handling",
        "score": 1,
        "applicable": true,
        "weight": 3,
        "reason": "Given the absence of the Q4 report content, the response should have acknowledged that limitation and asked for the document or clarified access."
      },
      {
        "id": "general_quality",
        "score": 1,
        "applicable": true,
        "weight": 5,
        "reason": "Overall quality is poor because the final response is courteous but unhelpful, leaving the user's original need unresolved without any recovery attempt."
      }
    ]
  }
}
```

Each output item includes per-dimension scores with reasons. Dimensions marked `"applicable": false` are skipped and don't contribute to the overall score. The overall score is a weighted average of all applicable dimension scores, normalized to a 0–1 range.

> [!NOTE]
> Rubric evaluators use LLM-as-judge scoring and incur model inference costs per evaluation call. Scoring reliability might vary for very short responses. Write rubric descriptions that are specific and unambiguous to improve scoring consistency across evaluations.

## Set up evaluation with rubric evaluators

You can use your rubric evaluator in batch evaluation to create an evaluation to assess agent quality on production traffic. Once you're satisfied with your rubric evaluator, you can set up continious and scheduled evaluation in Monitor settings to run your rubric evaluators automatically. Both run your rubric evaluators automatically against your agents, helping you detect quality regressions without triggering manual evaluation runs.

### Set up continuous evaluation

Continuous evaluation runs your rubric evaluators on sampled agent traces as they arrive in real time.

1. Connect an [Application Insights resource](../../observability/how-to/trace-agent-setup.md) to your Foundry project.
1. Open the [monitoring dashboard](../../observability/how-to/how-to-monitor-agents-dashboard.md) and select **Monitor settings**.
1. Under **Continuous evaluation**, select **Enable**.
1. Add your rubric evaluator to the evaluator list.
1. Set a sample rate that balances evaluation coverage with cost.
1. Select **Save**.

The service evaluates sampled agent traces with your rubric evaluators and surfaces quality scores in the monitoring dashboard.

### Set up scheduled evaluation

Scheduled evaluation runs your rubric evaluators on a recurring basis.

1. Connect an [Application Insights resource](../../observability/how-to/trace-agent-setup.md) to your Foundry project.
1. Open the [monitoring dashboard](../../observability/how-to/how-to-monitor-agents-dashboard.md) and select **Monitor settings**.
1. Under **Scheduled evaluations**, select **Add schedule**.
1. Add your rubric evaluator to the evaluator list.
1. Set the recurrence interval (for example, daily or weekly) and the trace lookback window.
1. Select **Save**.

The service runs your rubric evaluators at each scheduled interval against traces collected within the lookback window. Use the dashboard to track quality trends over time and set up alerts when scores drop below your threshold.

## Related content

- [Run evaluations from the SDK](../../how-to/develop/cloud-evaluation.md)
- [Monitor agents in the dashboard](../../observability/how-to/how-to-monitor-agents-dashboard.md)
- [Set up tracing](../../observability/how-to/trace-agent-setup.md)
- [Custom evaluators](custom-evaluators.md)
- [General purpose evaluators](general-purpose-evaluators.md)
