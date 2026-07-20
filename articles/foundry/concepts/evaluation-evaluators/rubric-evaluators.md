---
title: "Rubric evaluators"
description: "Learn about rubric evaluators for AI agents, which let you define custom scoring criteria with descriptive rubrics for LLM-as-judge evaluation."
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 06/02/2026
ms.service: microsoft-foundry
ms.topic: reference

---

# Rubric evaluators (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

A rubric evaluator scores an agent or model response against custom, weighted criteria that you define, using an LLM as the judge. It gives you full control over what "good" means for your use case while applying that judgment consistently at scale.

A *rubric* is a set of criteria that defines how to rate the response. Each rubric contains scoring *dimensions*; each dimension has a description of what it measures and a weight that reflects its relative importance. The LLM judge scores each applicable dimension from 1 to 5 on a single response or multi-turn conversation. The overall rubric score is the weighted average of those scores, normalized to a 0–1 range.

Use rubric evaluators as your primary measure of agent quality, because they let you express the exact criteria that matter for your use case. Pair them with built-in evaluators for safety, groundedness, and content harm to cover risks the rubric doesn't measure. The rest of this article describes how to generate a rubric, the fields it contains, how to choose an LLM judge model, and how to review the results.

## Generate a rubric evaluator

You can create a rubric evaluator in two ways:

### Auto-generate a rubric (recommended)

You can automatically create a rubric evaluator by selecting an LLM model to generate the rubric from your agent's context. Provide at least one of the following base inputs:

- **Foundry agent** — Select an existing Foundry agent. The service pulls the agent's instructions (for prompt agents) or its description (for hosted agents) to use as the generation context.
- **Agent system prompt** — Paste the instructions that define your agent's intended behavior. Use this when the agent isn't registered in Foundry or when its registered context doesn't fully capture its behavior.
- **Reference files** — Documents, knowledge-base content, or domain guidelines that describe your agent's context and the expected response quality.

For best results, add agent production traces on top of any base input above to ground the rubric in real usage:

- **Traces** — Agent production traces collected from Foundry tracing in Application Insights. Traces can't be used alone; pair them with a Foundry agent, an agent system prompt, or reference files.

Each generated rubric contains the following fields:

| Field | Description |
|-------|-------------|
| `id` | Stable, human-readable slug assigned by the service on first generation. When you edit criteria and save as a new version, echo the existing `id` to preserve identity across versions. The service doesn't reassign IDs on edit. |
| `description` | What this criterion measures — a clear, specific quality dimension. |
| `weight` | Relative importance of the criterion. The generation pipeline assigns exactly one criterion a weight of 8–10 (the most outcome-decisive dimension) and all others 1–6. User edits aren't constrained by this heuristic. |
| `always_applicable` | When `true`, the LLM judge always scores this criterion regardless of relevance (skips the applicability assessment). Used for the general quality criterion. Defaults to `false`. |

#### Choose an LLM judge model

Not all models perform equally as rubric judges. The following table ranks models by judge quality.

| Rank | Model | Recommendation |
|------|-------|----------------|
| 1 | `gpt-5.5` | Recommended |
| 2 | `gpt-5.4` | Recommended |
| 3 | `gpt-5.4-nano` | Recommended |
| 4 | `gpt-5.4-mini` | Recommended |
| 5 | `gpt-5.2` | Recommended |
| 8 | `gpt-4.1` | Acceptable |
| 9 | `gpt-4o` | Acceptable |
| 10 | `gpt-4o-mini` | Not recommended |

> [!IMPORTANT]
> Avoid using `gpt-4o-mini` as a rubric judge. This model produces noticeably less reliable scores compared to newer models. For the best balance of performance and cost, use `gpt-5.4-mini`.

### Manually create a rubric

Write your own rubric by defining each dimension's `id`, `description`, and `weight`. Use this approach when you already have a rubric defined elsewhere that you want to bring into Foundry.

> [!TIP]
> Start by creating an auto-generated rubric evaluator and refine it manually. Auto-generation gives you a strong baseline that you can adjust to fit your specific quality standards.

## Review and adjust the rubric

After you generate or create a rubric, review the dimensions to confirm they match your expectations for agent quality. You can:

- **Edit `id`, `description`, and `weight`** — Refine the language to be more specific about what qualifies for each dimension level. Precise descriptions and weight improve scoring consistency.
- **Add or remove dimensions** — Insert quality dimensions that matter for your domain, or remove ones that don't apply.
- **Adjust thresholds** — Set the pass threshold to control what overall score qualifies as passing. Values range from 0.0 to 1.0, where 1.0 is the highest score. Raise the threshold for a stricter quality standard, or lower it to be more permissive.
- **Set always applicable** — Select or clear the **Always applicable** checkbox for a criterion. When selected, the LLM judge scores this criterion for every response without checking relevance first.

In the advanced settings for each rubric, you can also view the evaluation level and category for this rubric evaluator.

Iterate on the rubric until it reliably distinguishes between acceptable and unacceptable agent responses. Run a small evaluation on a sample dataset to validate that the rubric scores align with your own judgment before using it at scale.

## Example rubric

The following example shows a rubric for a restaurant reservation agent. Each criterion targets a specific quality dimension, with weights reflecting relative importance:

```json
[
  {
    "id": "intent_recognition",
    "description": "Correctly identifies the user's reservation intent (book, modify, cancel, inquire) and pursues the appropriate workflow without unnecessary clarification.",
    "weight": 9
  },
  {
    "id": "tool_usage_accuracy",
    "description": "Calls the correct tool with correct parameters. Does not call tools unnecessarily, and does not skip tool calls when they are needed.",
    "weight": 6
  },
  {
    "id": "policy_enforcement",
    "description": "Enforces business rules: dinner service 17:00-22:00, max party size 8, 30-day booking window. Does not create reservations that violate these constraints.",
    "weight": 5
  },
  {
    "id": "information_gathering",
    "description": "Collects all required information (date, time, party size, contact) before attempting to create a reservation. Does not ask for information already provided.",
    "weight": 4
  },
  {
    "id": "communication_clarity",
    "description": "Provides clear, concise responses. Confirms reservation details before finalizing. Uses a professional and helpful tone.",
    "weight": 2
  },
  {
    "id": "general_quality",
    "description": "Other important quality factors not already covered by the listed criteria.",
    "weight": 5,
    "always_applicable": true
  }
]
```

In this rubric, `intent_recognition` has the highest weight (9) because correctly identifying what the user wants is the most outcome-decisive factor. The `general_quality` criterion uses `always_applicable: true` so the judge scores it for every response, even when other criteria might not apply.

## Use rubric evaluators to run evaluation

Rubric evaluators work well for domain-specific or organization-specific quality criteria that general-purpose evaluators can't capture. Define a rubric when you need scoring that reflects your team's specific quality standards—for example, customer support tone, medical accuracy, or legal compliance.

The LLM judge reads the rubric, examines the mapped input data, assigns a score, and provides a reason for its scoring decision. This approach combines the flexibility of custom criteria with the consistency of LLM-based evaluation.

For details on running evaluations and configuring data sources, see [Run evaluations from the SDK](../../how-to/develop/cloud-evaluation.md).

## Example output

The rubric evaluator returns a weighted score for each dimension, an overall score, a pass/fail label, and a reason explaining the decision. The default pass threshold is 0.5. Scores at or above the threshold are considered passing.

### Pass example

In this example, a user asks to book a table for 4 on Friday at 7:30 PM. The agent correctly identifies the booking intent, calls the reservation tool with valid parameters, and confirms the reservation:

```json
{
  "score": 0.9419354839,
  "label": "pass",
  "reason": "The verdict is driven most by intent_recognition (5), tool_usage_accuracy (5), and policy_enforcement (5). The assistant correctly identified the booking intent, called the reservation tool with valid parameters (Friday 7:30 PM, party of 4), and returned a clear confirmation with the reservation details.",
  "threshold": 0.5,
  "passed": true,
  "properties": {
    "dimension_scores": [
      {
        "id": "intent_recognition",
        "score": 5,
        "applicable": true,
        "weight": 9,
        "reason": "The user's request to book a table is correctly identified, and the assistant pursues the booking workflow without unnecessary clarification."
      },
      {
        "id": "tool_usage_accuracy",
        "score": 5,
        "applicable": true,
        "weight": 6,
        "reason": "The reservation tool is called once with the correct date, time, and party size parameters derived from the user's request."
      },
      {
        "id": "policy_enforcement",
        "score": 5,
        "applicable": true,
        "weight": 5,
        "reason": "The reservation falls within dinner service hours, the party size is within the maximum of 8, and the date is within the 30-day booking window."
      },
      {
        "id": "information_gathering",
        "score": 4,
        "applicable": true,
        "weight": 4,
        "reason": "All required information (date, time, party size, contact) is captured from the request without asking for details already provided."
      },
      {
        "id": "communication_clarity",
        "score": 5,
        "applicable": true,
        "weight": 2,
        "reason": "The confirmation is concise and includes the reservation date, time, and party size in a single clear message."
      },
      {
        "id": "general_quality",
        "score": 4,
        "applicable": true,
        "weight": 5,
        "reason": "Overall execution is strong: the assistant handles the booking end to end with no unnecessary turns or recovery steps."
      }
    ]
  }
}
```

### Fail example

In this example, a user asks to book a table for 12 people on Saturday. The maximum party size is 8, but the agent proceeds to book anyway without flagging the policy violation:

```json
{
  "score": 0.3548387097,
  "label": "fail",
  "reason": "The verdict is driven by very low policy_enforcement (1), tool_usage_accuracy (1), and general_quality (1). The user requested a table for 12, which exceeds the maximum party size of 8, but the assistant proceeded to call the reservation tool and confirmed a booking that violates business rules.",
  "threshold": 0.5,
  "passed": false,
  "properties": {
    "dimension_scores": [
      {
        "id": "intent_recognition",
        "score": 3,
        "applicable": true,
        "weight": 9,
        "reason": "The booking intent is identified, but the assistant fails to flag that the requested party size cannot be accommodated under business rules."
      },
      {
        "id": "tool_usage_accuracy",
        "score": 1,
        "applicable": true,
        "weight": 6,
        "reason": "The reservation tool is called with a party size that the business rules prohibit, producing an invalid booking."
      },
      {
        "id": "policy_enforcement",
        "score": 1,
        "applicable": true,
        "weight": 5,
        "reason": "The 8-person maximum party size is not enforced; the assistant should have declined or offered to split the party before attempting to book."
      },
      {
        "id": "information_gathering",
        "score": 2,
        "applicable": true,
        "weight": 4,
        "reason": "The assistant collected the party size and date but did not confirm a specific time, leaving required information incomplete."
      },
      {
        "id": "communication_clarity",
        "score": 2,
        "applicable": true,
        "weight": 2,
        "reason": "The final confirmation message is clear in form, but it asserts a booking that the system shouldn't have allowed, creating a misleading outcome."
      },
      {
        "id": "general_quality",
        "score": 1,
        "applicable": true,
        "weight": 5,
        "reason": "Overall quality is poor: the assistant violates a core business rule without warning the user or recovering, undermining trust in the booking outcome."
      }
    ]
  }
}
```

Each output item includes per-dimension scores with reasons. Dimensions marked `"applicable": false` are skipped and don't contribute to the overall score. The overall score is a weighted average of all applicable dimension scores, normalized to a 0–1 range.

> [!NOTE]
> Rubric evaluators use LLM-as-judge scoring and incur model inference costs per evaluation call. Scoring reliability might vary for very short responses. Write rubric descriptions that are specific and unambiguous to improve scoring consistency across evaluations.

## Set up continuous evaluation with rubric evaluators

Once your rubric evaluator reliably reflects your quality standards, configure it for continuous and scheduled evaluation in **Monitor settings**. Continuous evaluation runs the rubric automatically against new agent traffic, so you can catch quality regressions in production as they happen — without triggering manual runs.

For setup steps, see [Monitor agents in the dashboard](../../observability/how-to/how-to-monitor-agents-dashboard.md).

## Related content

- [Run evaluations from the SDK](../../how-to/develop/cloud-evaluation.md)
- [Monitor agents in the dashboard](../../observability/how-to/how-to-monitor-agents-dashboard.md)
- [Set up tracing](../../observability/how-to/trace-agent-setup.md)
- [Custom evaluators](custom-evaluators.md)
- [General purpose evaluators](general-purpose-evaluators.md)
