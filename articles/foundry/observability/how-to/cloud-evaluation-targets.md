---
title: "Evaluate models and agents with the Microsoft Foundry SDK"
description: "Learn how to use the Microsoft Foundry SDK to evaluate model, prompt-agent, and hosted-agent targets with responses and invocations protocols."
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
# customer intent: As a developer, I want to invoke models and agents during evaluation so that I can score generated responses against test inputs.
---

# Evaluate models and agents in the cloud

Send test queries to deployed models, prompt agents, or hosted agents and evaluate the responses generated at run time.

## Prerequisites

- Complete the [cloud evaluation prerequisites](cloud-evaluation.md#prerequisites) and [client setup](cloud-evaluation.md#set-up-the-sdk-client).
- A JSONL or CSV dataset of input queries.
- A deployed model, prompt agent, or hosted agent to use as the target.

The examples use the SDK client configured in [Set up the SDK client](cloud-evaluation.md#set-up-the-sdk-client).

## Evaluate a model target

Send queries to a deployed model at runtime. Evaluate the responses by using the `azure_ai_target_completions` data source type with an `azure_ai_model` target. Your input data contains queries. The model generates responses, which you then evaluate.

> [!IMPORTANT]
> Before you begin, complete [client setup](cloud-evaluation.md#set-up-the-sdk-client) and [Prepare input data](cloud-evaluation-datasets.md#prepare-input-data).

> [!NOTE]
> You can use the [model router](../../openai/concepts/model-router.md) as the target model. Model router is supported *only* as the evaluation target. It can't be selected as a model for any other evaluation feature.

### Define the message template and target

The `input_messages` template controls how queries are sent to the model. Use `{{item.query}}` to reference fields from your input data. Specify the model to evaluate and optional sampling parameters:

```python
input_messages = {
    "type": "template",
    "template": [
        {
            "type": "message",
            "role": "user",
            "content": {
                "type": "input_text",
                "text": "{{item.query}}"
            }
        }
    ]
}

target = {
    "type": "azure_ai_model",
    "model": "gpt-5-mini",
    "sampling_params": {
        "top_p": 1.0,
        "max_completion_tokens": 2048,
    },
}
```

### Set up evaluators and data mappings

When the model generates responses at runtime, use `{{sample.output_text}}` in `data_mapping` to reference the model's output. Use `{{item.field}}` to reference fields from your input data.

```python
data_source_config = DataSourceConfigCustom(
    type="custom",
    item_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
        },
        "required": ["query"],
    },
    include_sample_schema=True,
)

testing_criteria = [
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="coherence",
        evaluator_name="builtin.coherence",
        initialization_parameters={"model": model_deployment_name},
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="violence",
        evaluator_name="builtin.violence",
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    ),
]
```

### Create evaluation and run

# [Python](#tab/python)

```python
eval_object = openai_client.evals.create(
    name="Model Target Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

data_source = {
    "type": "azure_ai_target_completions",
    "source": {
        "type": "file_id",
        "id": data_id,
    },
    "input_messages": input_messages,
    "target": target,
}

eval_run = openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name="model-target-evaluation",
    data_source=data_source,
)
```

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/v1/evals/${EVAL_ID}/runs" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "model-target-evaluation",
    "data_source": {
      "type": "azure_ai_target_completions",
      "source": {
        "type": "file_id",
        "id": "YOUR_DATASET_ID"
      },
      "input_messages": {
        "type": "template",
        "template": [
          {
            "type": "message",
            "role": "user",
            "content": {
              "type": "input_text",
              "text": "{{item.query}}"
            }
          }
        ]
      },
      "target": {
        "type": "azure_ai_model",
        "model": "gpt-5-mini",
        "sampling_params": {
          "top_p": 1.0,
          "max_completion_tokens": 2048
        }
      }
    }
  }'
```

---

For a complete runnable example, see [sample_model_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_model_evaluation.py) on GitHub. To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).

> [!TIP]
> To add another evaluation run, use the same code.

## Evaluate an agent target

Send queries to a Foundry agent at runtime and evaluate the responses by using the `azure_ai_target_completions` data source type with an `azure_ai_agent` target. This scenario works for both [prompt agents](../../agents/overview.md) and [hosted agents](../../agents/concepts/hosted-agents.md).

> [!IMPORTANT]
> Before you begin, complete [client setup](cloud-evaluation.md#set-up-the-sdk-client) and [Prepare input data](cloud-evaluation-datasets.md#prepare-input-data).

> [!TIP]
> Hosted agents that use the responses protocol work with the same code samples shown here. For hosted agents that use the invocations protocol, the `input_messages` format is different. See [Hosted agent invocations protocol](#hosted-agent-invocations-protocol) for details.

### Define the message template and target

The `input_messages` template controls how queries are sent to the agent. Use `{{item.query}}` to reference fields from your input data. Specify the agent to evaluate by name:

```python
input_messages = {
    "type": "template",
    "template": [
        {
            "type": "message",
            "role": "developer",
            "content": {
                "type": "input_text",
                "text": "You are a helpful assistant. Answer clearly and safely."
            }
        },
        {
            "type": "message",
            "role": "user",
            "content": {
                "type": "input_text",
                "text": "{{item.query}}"
            }
        }
    ]
}

target = {
    "type": "azure_ai_agent",
    "name": "my-agent",
    "version": "1"  # Optional. Uses latest version if omitted.
}
```

### Set up evaluators and data mappings

When the agent generates responses at runtime, use `{{sample.*}}` variables in `data_mapping` to reference the agent's output:

| Variable | Description | Use for |
|----------|-------------|---------|
| `{{sample.output_text}}` | The agent's plain text response. | Evaluators that expect a string response (for example, `coherence`, `violence`). |
| `{{sample.output_items}}` | The agent's structured JSON output, including tool calls. | Evaluators that need full interaction context (for example, `task_adherence`). |
| `{{item.field}}` | A field from your input data. | Input fields like `query` or `ground_truth`. |

> [!TIP]
> The `query` field can contain structured JSON, including system messages and conversation history. Some agent evaluators such as `task_adherence` use this context for more accurate scoring. For details on query formatting, see [agent evaluators](../../concepts/evaluation-evaluators/agent-evaluators.md).

```python
data_source_config = DataSourceConfigCustom(
    type="custom",
    item_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
        },
        "required": ["query"],
    },
    include_sample_schema=True,
)

testing_criteria = [
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="coherence",
        evaluator_name="builtin.coherence",
        initialization_parameters={"model": model_deployment_name},
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="violence",
        evaluator_name="builtin.violence",
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="task_adherence",
        evaluator_name="builtin.task_adherence",
        initialization_parameters={"model": model_deployment_name},
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
    ),
]
```

### Create evaluation and run

# [Python](#tab/python)

```python
eval_object = openai_client.evals.create(
    name="Agent Target Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

data_source = {
    "type": "azure_ai_target_completions",
    "source": {
        "type": "file_id",
        "id": data_id,
    },
    "input_messages": input_messages,
    "target": target,
}

agent_eval_run = openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name="agent-target-evaluation",
    data_source=data_source,
)
```

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/v1/evals/${EVAL_ID}/runs" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "agent-target-evaluation",
    "data_source": {
      "type": "azure_ai_target_completions",
      "source": {
        "type": "file_id",
        "id": "YOUR_DATASET_ID"
      },
      "input_messages": {
        "type": "template",
        "template": [
          {
            "type": "message",
            "role": "developer",
            "content": {
              "type": "input_text",
              "text": "You are a helpful assistant. Answer clearly and safely."
            }
          },
          {
            "type": "message",
            "role": "user",
            "content": {
              "type": "input_text",
              "text": "{{item.query}}"
            }
          }
        ]
      },
      "target": {
        "type": "azure_ai_agent",
        "name": "my-agent",
        "version": "1"
      }
    }
  }'
```

---

For a complete runnable example, see [sample_agent_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_agent_evaluation.py) on GitHub. To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).

### Hosted agent invocations protocol

[Hosted agents](../../agents/concepts/hosted-agents.md) that use the invocations protocol support the same `azure_ai_agent` target type but use a **freeform `input_messages`** format. Instead of the structured template format, provide a JSON object that maps directly to the agent's `/invocations` request body. Use `{{item.*}}` placeholders to substitute fields from your input data.

If a hosted agent supports both the responses and invocations protocols, the service defaults to using the invocations protocol.

#### Define the message format and target

```python
input_messages = {"message": "{{item.query}}"}

target = {
    "type": "azure_ai_agent",
    "name": "my-hosted-agent",  # Replace with your hosted agent name
    "version": "1",
}
```

#### Create evaluation and run

# [Python](#tab/python)

```python
eval_object = openai_client.evals.create(
    name="Hosted Agent Invocations Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

data_source = {
    "type": "azure_ai_target_completions",
    "source": {
        "type": "file_id",
        "id": data_id,
    },
    "input_messages": input_messages,
    "target": target,
}

eval_run = openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name="hosted-agent-invocations-evaluation",
    data_source=data_source,
)
```

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/v1/evals/${EVAL_ID}/runs" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "hosted-agent-invocations-evaluation",
    "data_source": {
      "type": "azure_ai_target_completions",
      "source": {
        "type": "file_id",
        "id": "YOUR_DATASET_ID"
      },
      "input_messages": {
        "message": "{{item.query}}"
      },
      "target": {
        "type": "azure_ai_agent",
        "name": "my-hosted-agent",
        "version": "1"
      }
    }
  }'
```

---

The evaluator setup and data mappings are the same as for [prompt agent evaluation](#set-up-evaluators-and-data-mappings-1). Use `{{sample.output_text}}` for the agent's text response and `{{sample.output_items}}` for the full structured output including tool calls.

## Related content

- [Cloud evaluation overview](cloud-evaluation.md)
- [Prepare cloud evaluation data](cloud-evaluation-datasets.md#prepare-input-data)
- [Get cloud evaluation results](cloud-evaluation-results.md)
