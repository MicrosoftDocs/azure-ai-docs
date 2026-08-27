---
title: "Evaluate conversations with the Microsoft Foundry SDK"
description: "Learn how to use the Microsoft Foundry SDK to evaluate conversation datasets and production conversations by ID or agent filter."
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom:
  - references_regions
ms.topic: how-to
ms.date: 08/26/2026
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
# customer intent: As a developer, I want to evaluate complete conversations so that I can detect quality issues that individual-turn evaluation misses.
---

# Evaluate conversations in the cloud (preview)

Assess complete conversations from datasets or Application Insights traces at the turn or conversation level.

## Prerequisites

- Complete the [cloud evaluation prerequisites](cloud-evaluation.md#prerequisites) and [client setup](cloud-evaluation.md#set-up-the-sdk-client).
- Conversation data with a `messages` array, or traced production conversations in Application Insights.
- Conversation-level evaluators that support the selected evaluation level.

The examples use the SDK client configured in [Set up the SDK client](cloud-evaluation.md#set-up-the-sdk-client).

## Evaluate conversation datasets

Evaluate complete conversations to assess agent quality across entire user interactions - not just individual responses. Use conversation-level evaluation to identify quality problems like incomplete task resolution, user frustration, and tool-call regressions that turn-level evaluation misses.

For example, consider a support agent where the user grows frustrated over multiple turns:

> **Turn 1** — User: "I need to reset my password." Agent: "I found your account. I'll send a reset link."
>
> **Turn 2** — User: "I didn't get the email." Agent: "I've resent the link. Please check spam."
>
> **Turn 3** — User: "Still nothing. Can you just reset it directly?" Agent: "I've sent another reset link."

A turn-level evaluator scores only the last response - which is polite and takes action - so it scores well. A conversation-level evaluator grading **customer satisfaction** across the conversation flags that the agent repeated the same failing action three times without trying an alternative, leaving the user's problem unresolved.

Conversation-level evaluation differs from turn-level evaluation in several ways:

| Aspect | Turn-level | Conversation-level |
|--------|------------|--------------------|
| **Scope** | Individual query-response pairs | Complete conversations with multiple exchanges |
| **Metrics** | Per-response quality and safety | Conversation-level outcomes and user satisfaction |
| **Data format** | JSONL with `query` and `response` fields | JSONL with `messages` array containing the full conversation |
| **Use case** | Testing individual model responses | Testing end-to-end agent experiences |

Conversation-level evaluation supports four data source options:

| Option | When to use | Data source type |
|--------|-------------|------------------|
| [From dataset or inline](#prepare-conversation-data) | You have local conversation traces or test data | `jsonl` with `file_id` or `file_content` |
| [By conversation ID](#evaluate-conversations-by-id-from-traces) | You want to evaluate specific conversations from App Insights | `azure_ai_trace_data_source_preview` with `trace_source` |
| [By agent filter with sampling](#evaluate-sampled-conversations-by-agent-filter) | You want to assess overall agent quality across sampled production traffic | `azure_ai_trace_data_source_preview` with `trace_source` |
| [Simulated conversations](cloud-evaluation-synthetic-data.md#simulate-conversations-preview) | You want to generate synthetic test conversations | `azure_ai_target_completions` with `conversation_gen_preview` |

## Choose an evaluation level

The `evaluation_level` parameter on the run determines whether evaluators score individual turns or complete conversations:

| Value | Behavior |
|-------|----------|
| `"turn"` | Evaluators score each turn independently. |
| `"conversation"` | Evaluators score the entire conversation as a whole. |
| (omitted) | Defaults to `"turn"`. |

> [!IMPORTANT]
> **Evaluator compatibility**: Each evaluator supports specific evaluation levels. Check the evaluator's `supported_evaluation_levels` field in the [evaluator catalog](../../how-to/evaluate-generative-ai-app.md).
>
> - **Turn-only evaluators** (for example, `fluency`, `relevance`) can't be used with `evaluation_level="conversation"`.
> - Currently, all conversation-level evaluators support both `"turn"` and `"conversation"` levels.

### Common errors

| Error | Cause | Solution |
|-------|-------|----------|
| Incompatible evaluation level | Using `evaluation_level="conversation"` with a turn-only evaluator | Remove the turn-only evaluator or change to `evaluation_level="turn"` |

## Prepare conversation data

Create a JSONL file where each line contains a complete conversation in the `messages` field. Each message should include a `role` (user, assistant, or system) and `content`. For a complete example, see the [conversation evaluation samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations) in the SDK.

```json
 {"messages": [{"role": "user", "content": "What's my account balance?"}, {"role": "assistant", "content": "Your current balance is $1,234.56."}, {"role": "user", "content": "Thanks!"}, {"role": "assistant", "content": "You're welcome! Is there anything else?"}]}
```

You can also include tool definitions and tool calls if your agent uses tools:

```json
{"messages": [{"role": "user", "content": "What is the capital/major city of France?"}, {"role": "assistant", "content": "Paris"}]}
{"messages": [{"role": "user", "content": "How do I reverse a string in Python?"}, {"role": "assistant", "content": "You can reverse a string in Python by using slicing: string[::-1]"}]}
{"messages": [{"role": "user", "content": "What are the main causes of climate change?"}, {"role": "assistant", "content": "The main causes of climate change are the increase in greenhouse gases in the atmosphere, primarily due to human activities such as burning fossil fuels and deforestation."}]}
{"messages": [{"role": "user", "content": "What's my account balance?"}, {"role": "assistant", "content": null, "tool_calls": [{"id": "call_abc123", "type": "function", "function": {"name": "get_account_balance", "arguments": "{\"account_id\": \"ACCT-7890\"}"}}]}, {"role": "tool", "tool_call_id": "call_abc123", "content": "{ \"balance\": 1234.56, \"currency\": \"USD\" }"}, {"role": "assistant", "content": "Your current balance is 1,234.56."}, {"role": "user", "content": "Thanks!"}, {"role": "assistant", "content": "You're welcome! Is there anything else?"}], "tool_definitions": [{"name": "get_account_balance", "description": "Retrieves the current balance for a customer account", "parameters": {"type": "object", "properties": {"account_id": {"type": "string"}}, "required": ["account_id"]}}]}
{"messages": [{"role": "user", "content": "Explain the theory of relativity in simple terms."}, {"role": "assistant", "content": "Einstein's theory of relativity shows that space and time are interconnected and relative to the observer's frame of reference."}]}
{"messages": [{"role": "user", "content": "What's the weather in Seattle?"}, {"role": "assistant", "content": null, "tool_calls": [{"id": "call_002", "type": "function", "function": {"name": "get_weather", "arguments": "{\"location\": \"Seattle, WA\"}"}}]}, {"role": "tool", "tool_call_id": "call_002", "content": "{ \"temperature\": 55, \"condition\": \"Cloudy\" }"}, {"role": "assistant", "content": "It's currently 55F and cloudy in Seattle."}], "tool_definitions": [{"name": "get_weather", "description": "Get the current weather for a location", "parameters": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]}}]}
{"messages": [{"role": "user", "content": "What is the tallest mountain in the world?"}, {"role": "assistant", "content": "Mount Everest is the tallest mountain in the world."}]}
{"messages": [{"role": "user", "content": "Is 4 x 2 = 16?"}, {"role": "assistant", "content": "No, 4 x 2 = 8."}]}
{"messages": [{"role": "user", "content": "What is the best Italian desert?"}, {"role": "assistant", "content": "Tiramisu is a popular Italian dessert."}]}
{"messages": [{"role": "user", "content": "What is the chemical formula for water?"}, {"role": "assistant", "content": "The chemical formula for water is H2O."}]}
```

## Define the data schema and evaluators

Specify the schema for your conversation data, "messages", and select evaluators designed for conversation-level evaluation. Conversation-level evaluators assess the entire interaction rather than individual turns.

# [Python](#tab/python)

```bash
pip install "azure-ai-projects>=2.2.0"
```

```python
import os
from openai.types.eval_create_params import DataSourceConfigCustom
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
model_deployment_name = os.environ["FOUNDRY_MODEL_NAME"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    data_source_config = DataSourceConfigCustom(
        type="custom",
        item_schema={
            "type": "object",
            "properties": {
                "messages": {"type": "array"},
                "tool_definitions": {"type": "array"},
            },
            "required": ["messages"],
        },
        include_sample_schema=False,
    )

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
```

# [JavaScript/TypeScript](#tab/javascript)

The current JavaScript/TypeScript SDK samples don't demonstrate conversation-level evaluation. Use the Python or cURL tab for this flow.

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals?api-version=2025-11-15-preview" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "multiturn-conversation-evaluation",
    "data_source_config": {
      "type": "custom",
      "item_schema": {
        "type": "object",
        "properties": {
          "messages": {"type": "array"},
          "tool_definitions": {"type": "array"}
        },
        "required": ["messages"]
      },
      "include_sample_schema": false
    },
    "testing_criteria": [
      {
        "type": "azure_ai_evaluator",
        "name": "customer_satisfaction",
        "evaluator_name": "builtin.customer_satisfaction",
        "initialization_parameters": {"model": "gpt-5-mini"},
        "data_mapping": {"messages": "{{item.messages}}"}
      },
      {
        "type": "azure_ai_evaluator",
        "name": "task_completion",
        "evaluator_name": "builtin.task_completion",
        "initialization_parameters": {"model": "gpt-5-mini"},
        "data_mapping": {"messages": "{{item.messages}}"}
      },
      {
        "type": "azure_ai_evaluator",
        "name": "conversation_coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {"model": "gpt-5-mini"},
        "data_mapping": {"messages": "{{item.messages}}"}
      },
      {
        "type": "azure_ai_evaluator",
        "name": "groundedness",
        "evaluator_name": "builtin.groundedness",
        "initialization_parameters": {"model": "gpt-5-mini"},
        "data_mapping": {"messages": "{{item.messages}}"}
      }
    ]
  }'
```

---

## Create evaluation and run

# [Python](#tab/python)

Prep: download [sample_data_multiturn_conversations.jsonl](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/data_folder/sample_data_multiturn_conversations.jsonl)

```python
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileID,
)

# Upload conversation data
data_id = project_client.datasets.upload_file(
    name="multiturn-conversation-data",
    version="1",
    file_path="./sample_data_multiturn_conversations.jsonl",
).id

# Create the evaluation
eval_object = openai_client.evals.create(
    name="Multi-turn Conversation Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

# Create a run with evaluation_level set to "conversation"
eval_run = openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name="multiturn-conversation-run",
    data_source=CreateEvalJSONLRunDataSourceParam(
        type="jsonl",
        source=SourceFileID(
            type="file_id",
            id=data_id,
        ),
    ),
    extra_body={"evaluation_level": "conversation"},
)
```

# [JavaScript/TypeScript](#tab/javascript)

The current JavaScript/TypeScript SDK samples don't demonstrate conversation-level evaluation. Use the Python or cURL tab for this flow.

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals/${EVAL_ID}/runs?api-version=2025-11-15-preview" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "multiturn-conversation-run",
    "evaluation_level": "conversation",
    "data_source": {
      "type": "jsonl",
      "source": {
        "type": "file_id",
        "id": "YOUR_DATASET_ID"
      }
    }
  }'
```

---

To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).

For a complete runnable example, see [sample_multiturn_conversation_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_multiturn_conversation_evaluation.py) on GitHub.

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

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
model_deployment_name = os.environ["FOUNDRY_MODEL_NAME"]

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

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
model_deployment_name = os.environ["FOUNDRY_MODEL_NAME"]
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
