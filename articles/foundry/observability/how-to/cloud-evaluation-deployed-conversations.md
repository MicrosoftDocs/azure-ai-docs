---
title: "Evaluate deployed model and agent conversations with the Microsoft Foundry SDK"
description: "Learn how to use the Microsoft Foundry SDK to evaluate traced production conversations by conversation ID or agent filter."
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom:
  - references_regions
ms.topic: how-to
ms.date: 08/31/2026
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
# customer intent: As a developer, I want to evaluate deployed model and agent conversations so that I can investigate issues and assess production quality.
---

# Evaluate deployed model and agent conversations with Microsoft Foundry SDK (preview)

Evaluate complete production conversations captured in Application Insights to investigate specific interactions or sample deployed agent traffic.

## Prerequisites

- Complete the [cloud evaluation prerequisites](cloud-evaluation.md#prerequisites) and [client setup](cloud-evaluation.md#set-up-the-sdk-client).
- Traced production conversations in Application Insights.
- Conversation-level evaluators that support the selected evaluation level.

The examples use the SDK client configured in [Set up the SDK client](cloud-evaluation.md#set-up-the-sdk-client).

## Evaluate conversations by ID from traces

Evaluate specific conversations from Application Insights by providing their conversation IDs. Use this option to root-cause problems or verify fixes on specific interactions. For example, you can investigate a conversation flagged by an alert or verify a fix for a known issue.

### Where to find conversation IDs

Find conversation IDs in:

- **Application Insights trace logs UI** — Browse to interesting traces and locate the `conversation_id` field in the trace details.
- **Your application's logging output** — If you set `conversation_id` explicitly when creating agent responses, retrieve it from your logs.
- **OpenTelemetry trace context** — The `conversation_id` might also be derived from the [traceparent header](https://www.w3.org/TR/trace-context/#traceparent-header) if your agent uses standard trace context propagation.

> [!NOTE]
> Tool definitions are automatically retrieved from the traces or queried from the agent registry. You don't need to provide them in the request.

### Parameters for conversation ID lookup

| Parameter | Required | Description |
|-----------|----------|-------------|
| `conversation_ids` | Yes | Array of conversation IDs to evaluate. |
| `lookback_hours` | No | Hours to search back from `end_time`. Defaults to seven days (168 hours). |
| `end_time` | No | End of the search window (ISO 8601 format). Defaults to the current time. |

# [Python](#tab/python)

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
model_deployment_name = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]

# Provide conversation IDs or trace IDs from App Insights
conversation_ids = ["conversation_1234", "conversation_5678"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    # Eval group for trace-based evaluations
    data_source_config = {
        "type": "azure_ai_source",
        "scenario": "traces",
    }

    testing_criteria = [
        TestingCriterionAzureAIEvaluator(
            type="azure_ai_evaluator",
            name="conversation_coherence",
            evaluator_name="builtin.coherence",
            initialization_parameters={"model": model_deployment_name},
            data_mapping={"messages": "{{item.messages}}"},
        ),
        TestingCriterionAzureAIEvaluator(
            type="azure_ai_evaluator",
            name="groundedness",
            evaluator_name="builtin.groundedness",
            initialization_parameters={"model": model_deployment_name},
            data_mapping={"messages": "{{item.messages}}"},
        ),
    ]

    # Create evaluation with traces scenario
    eval_object = openai_client.evals.create(
        name="Multi-turn Trace Evaluation (by ID)",
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )

    # Run evaluation on specific conversation IDs
    eval_run = openai_client.evals.runs.create(
        eval_id=eval_object.id,
        name="multiturn-trace-by-id-run",
        data_source={
            "type": "azure_ai_trace_data_source_preview",
            "trace_source": {
                "type": "conversation_id_source",
                "conversation_ids": conversation_ids,
            },
        },
        extra_body={"evaluation_level": "conversation"},
    )
```

# [JavaScript/TypeScript](#tab/javascript)

The current JavaScript/TypeScript SDK samples don't demonstrate conversation lookup by trace ID. Use the Python or cURL tab for this flow.

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals/${EVAL_ID}/runs?api-version=2025-11-15-preview" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "conversation-trace-eval",
    "evaluation_level": "conversation",
    "data_source": {
      "type": "azure_ai_trace_data_source_preview",
      "trace_source": {
        "type": "conversation_id_source",
        "conversation_ids": ["conversation_1234", "conversation_5678"],
        "lookback_hours": 24,
        "end_time": "2026-05-21T00:00:00Z"
      }
    }
  }'
```

---

> [!NOTE]
> - Application Insights data ingestion can cause a delay between when traces are generated and when they're available for evaluation. If the query doesn't find traces, wait a few minutes and retry.
> - The maximum lookback is **7 days (168 hours)**. To access older traces, use `start_time` and `end_time` within your App Insights retention limits.

For a complete runnable example, see [sample_multiturn_trace_evaluation_by_id.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_multiturn_trace_evaluation_by_id.py) on GitHub.

## Evaluate sampled conversations by agent filter

Evaluate a sampled set of conversations from Application Insights by filtering on agent name. Use this option to assess overall agent quality across production traffic. For example, run regular quality assessments or monitor for quality degradation in production.

The agent you specify for filtering can be part of a multi-agent conversation. The filter matches any conversation where that agent participated.

> [!NOTE]
> Tool definitions are automatically retrieved from the traces or queried from the agent registry. You don't need to provide them in the request.

### Agent identity fields

Specify the agent to filter by using one of these formats:

| Format | Example | Description |
|--------|---------|-------------|
| `agent_name` + `agent_version` | `"agent_name": "my-agent", "agent_version": "1"` | Two separate fields. If `agent_version` is omitted, use the latest version. |
| `agent_id` | `"agent_id": "my-agent:1"` | Single string in `"name:version"` format. |

#### Filter strategies

| Strategy | Description |
|----------|-------------|
| `random_sampling` | (Default) Uniformly random sample up to `max_traces` conversations. |
| `smart_filtering` | Service-managed heuristic that biases toward "interesting" traces - conversations with potential problems, edge cases, or anomalies. |

#### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `agent_name` | Yes | The agent name to filter traces by. |
| `agent_version` | No | The agent version. If omitted, uses the latest version. |
| `agent_id` | No | Alternative to `agent_name` + `agent_version`. Single string in format `"name:version"`. |
| `start_time` | Yes | Start of the time window (Unix epoch seconds, UTC). |
| `end_time` | Yes | End of the time window (Unix epoch seconds, UTC). Pad by +600 seconds to avoid ingestion delay. |
| `max_traces` | No | Maximum conversations to sample. Defaults to 1,000. |
| `filter_strategy` | No | `"random_sampling"` (default) or `"smart_filtering"` (service-managed heuristic that biases toward interesting traces). |

> [!IMPORTANT]
> The time window (`end_time - start_time`) must be at least **15 minutes** (900 seconds). This requirement exists because conversation-level queries apply a 5-minute inactivity buffer on each edge to avoid partial conversations.

# [Python](#tab/python)

```python
import os
import time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
model_deployment_name = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]
agent_name = os.environ["FOUNDRY_AGENT_NAME"]
agent_version = os.environ.get("FOUNDRY_AGENT_VERSION", "")

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    # Eval group for trace-based evaluations
    data_source_config = {
        "type": "azure_ai_source",
        "scenario": "traces",
    }

    testing_criteria = [
        TestingCriterionAzureAIEvaluator(
            type="azure_ai_evaluator",
            name="customer_satisfaction",
            evaluator_name="builtin.customer_satisfaction",
            initialization_parameters={"model": model_deployment_name},
            data_mapping={"messages": "{{item.messages}}"},
        ),
        TestingCriterionAzureAIEvaluator(
            type="azure_ai_evaluator",
            name="task_completion",
            evaluator_name="builtin.task_completion",
            initialization_parameters={"model": model_deployment_name},
            data_mapping={"messages": "{{item.messages}}"},
        ),
    ]

    eval_object = openai_client.evals.create(
        name="Multi-turn Trace Evaluation (Agent Filter)",
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )

    # Compute time window in unix seconds
    # Pad end_time by +600s (10 min) to avoid ingestion-delay edge exclusion
    now_unix = int(time.time())
    end_time = now_unix + 600
    start_time = now_unix - (24 * 3600)  # 24 hours lookback

    # Build trace_source with agent filter
    trace_source = {
        "type": "agent_filter",
        "agent_name": agent_name,
        "start_time": start_time,
        "end_time": end_time,
        "max_traces": 5,
    }
    if agent_version:
        trace_source["agent_version"] = agent_version

    # Run evaluation on sampled agent conversations
    eval_run = openai_client.evals.runs.create(
        eval_id=eval_object.id,
        name="multiturn-agent-filter-run",
        data_source={
            "type": "azure_ai_trace_data_source_preview",
            "trace_source": trace_source,
        },
        extra_body={"evaluation_level": "conversation"},
    )
```

# [JavaScript/TypeScript](#tab/javascript)

The current JavaScript/TypeScript SDK samples don't demonstrate conversation sampling by agent filter. Use the Python or cURL tab for this flow.

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals/${EVAL_ID}/runs?api-version=2025-11-15-preview" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "agent-quality-eval",
    "evaluation_level": "conversation",
    "data_source": {
      "type": "azure_ai_trace_data_source_preview",
      "trace_source": {
        "type": "agent_filter",
        "agent_name": "my-support-agent",
        "agent_version": "1",
        "start_time": 1743465600,
        "end_time": 1743552600,
        "max_traces": 100,
        "filter_strategy": "random_sampling"
      }
    }
  }'
```

---

> [!NOTE]
> The App Insights query timespan is currently limited to a maximum of **7 days (168 hours)**. You can't access traces older than 7 days without explicitly providing `start_time` and `end_time` within App Insights retention limits.

## Next steps

- To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).
- For a complete runnable example, see [sample_multiturn_trace_evaluation_agent_filter.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_multiturn_trace_evaluation_agent_filter.py) on GitHub.
- To evaluate stored conversations, see [Evaluate conversation datasets](cloud-evaluation-conversations.md).
- To generate synthetic conversations, see [Simulate agent conversations](cloud-evaluation-simulate-conversations.md).
