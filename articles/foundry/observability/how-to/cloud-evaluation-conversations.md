---
title: "Evaluate conversation datasets with the Microsoft Foundry SDK"
description: "Learn how to use the Microsoft Foundry SDK to evaluate complete conversation datasets at the turn or conversation level."
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
# customer intent: As a developer, I want to evaluate complete conversation datasets so that I can detect quality issues that individual-turn evaluation misses.
---

# Evaluate conversation datasets with Microsoft Foundry SDK (preview)

Assess complete conversations from datasets at the turn or conversation level.

## Prerequisites

- Complete the [cloud evaluation prerequisites](cloud-evaluation.md#prerequisites) and [client setup](cloud-evaluation.md#set-up-the-sdk-client).
- Conversation data with a `messages` array.
- Evaluators that support the selected evaluation level, such as coherence and groundedness.

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

Choose the conversation workflow that matches your data source:

| Workflow | When to use | Data source type |
|--------|-------------|------------------|
| [From dataset or inline](#prepare-conversation-data) | You have local conversation traces or test data | `jsonl` with `file_id` or `file_content` |
| [Deployed conversations](cloud-evaluation-deployed-conversations.md) | You want to evaluate specific conversations or sampled production traffic from Application Insights | `azure_ai_trace_data_source_preview` with `trace_source` |
| [Simulated conversations](cloud-evaluation-simulate-conversations.md) | You want to generate synthetic test conversations | `azure_ai_target_completions` with `conversation_gen_preview` |

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

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
model_deployment_name = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]

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

## Next steps

- To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).
- To evaluate production traces, see [Evaluate deployed model and agent conversations](cloud-evaluation-deployed-conversations.md).
- To generate synthetic conversations, see [Simulate agent conversations](cloud-evaluation-simulate-conversations.md).
