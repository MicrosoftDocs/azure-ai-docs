---
title: "Generate synthetic data with the Microsoft Foundry SDK"
description: "Learn how to use the Microsoft Foundry SDK to generate synthetic evaluation queries and simulate conversations with model and agent targets."
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
# customer intent: As a developer, I want to generate synthetic evaluation data so that I can test models and agents before I have representative production data.
---

# Generate synthetic data (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Generate individual test queries or simulate complete conversations, and then evaluate the target responses.

## Prerequisites

- Complete the [cloud evaluation prerequisites](cloud-evaluation.md#prerequisites) and [client setup](cloud-evaluation.md#set-up-the-sdk-client).
- A model deployment that supports the Responses API for query generation.
- A model or agent target to evaluate.

The examples use the SDK client configured in [Set up the SDK client](cloud-evaluation.md#set-up-the-sdk-client).

## Generate synthetic queries

Use the `azure_ai_synthetic_data_gen_preview` data source type to generate synthetic test queries, send them to a deployed model or Foundry agent, and evaluate the responses. Use this scenario when you don't have a test dataset. The service generates queries based on a prompt you provide (and/or from the agent's instructions), runs them against your target, and evaluates the responses.

> [!IMPORTANT]
> Before you begin, complete [client setup](cloud-evaluation.md#set-up-the-sdk-client).

### How synthetic data evaluation works

1. The service generates synthetic queries based on your `prompt` and optional seed data files.
1. Each query is sent to the specified target (model or agent) to generate a response.
1. Evaluators score each response using the generated query and response.
1. The generated queries are stored as a dataset in your project for reuse.

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `samples_count` | Yes | Maximum number of synthetic test queries to generate. |
| `model_deployment_name` | Yes | Model deployment to use for generating synthetic queries. Only models with Responses API capability are supported. For availability, see [Responses API region availability](https://aka.ms/aoai/responsesapi/availability). The [model router](../../openai/concepts/model-router.md) isn't supported here; it can only be used as the evaluation target. |
| `prompt` | No | Instructions describing the type of queries to generate. Optional when the agent target has instructions configured. |
| `output_dataset_name` | No | Name for the output dataset where generated queries are stored. If you don't provide a name, the service generates one automatically. |
| `sources` | No | Seed data files (by file ID) to improve relevance of generated queries. Currently only one file is supported. |

### Set up evaluators and data mappings

The synthetic data generator produces queries in the `{{item.query}}` field. The target generates responses available in `{{sample.output_text}}`. Map these fields to your evaluators:

```python
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator

data_source_config = {"type": "azure_ai_source", "scenario": "synthetic_data_gen_preview"}

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

#### Model target

Generate synthetic queries and evaluate a model:

```python
eval_object = openai_client.evals.create(
    name="Synthetic Data Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

data_source = {
    "type": "azure_ai_synthetic_data_gen_preview",
    "item_generation_params": {
        "type": "synthetic_data_gen_preview",
        "samples_count": 5,
        "prompt": "Generate customer service questions about returning defective products",
        "model_deployment_name": model_deployment_name,
        "output_dataset_name": "my-synthetic-dataset",
    },
    "target": {
        "type": "azure_ai_model",
        "model": model_deployment_name,
    },
}

eval_run = openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name="synthetic-data-evaluation",
    data_source=data_source,
)
```

You can optionally add a system prompt to shape the target model's behavior. When you use `input_messages` with synthetic data generation, include only `system` role messages - the service provides the generated queries as user messages automatically.

```python
data_source = {
    "type": "azure_ai_synthetic_data_gen_preview",
    "item_generation_params": {
        "type": "synthetic_data_gen_preview",
        "samples_count": 5,
        "prompt": "Generate customer service questions about returning defective products",
        "model_deployment_name": model_deployment_name,
    },
    "target": {
        "type": "azure_ai_model",
        "model": model_deployment_name,
    },
    "input_messages": {
        "type": "template",
        "template": [
            {
                "type": "message",
                "role": "system",
                "content": {
                    "type": "input_text",
                    "text": "You are a helpful customer service agent. Be empathetic and solution-oriented."
                }
            }
        ]
    },
}
```
#### Agent target

Generate synthetic queries and evaluate a Foundry agent:

```python
data_source = {
    "type": "azure_ai_synthetic_data_gen_preview",
    "item_generation_params": {
        "type": "synthetic_data_gen_preview",
        "samples_count": 5,
        "prompt": "Generate questions about returning defective products",
        "model_deployment_name": model_deployment_name,
    },
    "target": {
        "type": "azure_ai_agent",
        "name": agent_name,
        "version": agent_version,
    },
}

eval_run = openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name="synthetic-agent-evaluation",
    data_source=data_source,
)
```

# [cURL](#tab/curl)

```bash
# Step 1: Create the evaluation
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals?api-version=v1" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Synthetic Data Evaluation",
    "data_source_config": {
      "type": "azure_ai_source",
      "scenario": "synthetic_data_gen_preview"
    },
    "testing_criteria": [
      {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
          "model": "gpt-5-mini"
        },
        "data_mapping": {
          "query": "{{item.query}}",
          "response": "{{sample.output_text}}"
        }
      },
      {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
          "query": "{{item.query}}",
          "response": "{{sample.output_text}}"
        }
      }
    ]
  }'

# Step 2: Create a run with synthetic data generation
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals/${EVAL_ID}/runs?api-version=v1" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "synthetic-data-evaluation",
    "data_source": {
      "type": "azure_ai_synthetic_data_gen_preview",
      "item_generation_params": {
        "type": "synthetic_data_gen_preview",
        "samples_count": 5,
        "prompt": "Generate customer service questions about returning defective products",
        "model_deployment_name": "gpt-5-mini",
        "output_dataset_name": "my-synthetic-dataset"
      },
      "target": {
        "type": "azure_ai_model",
        "model": "gpt-5-mini"
      }
    }
  }'
```

---

To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md). The response includes an `output_dataset_id` property that contains the ID of the generated dataset, which you can use to retrieve or reuse the synthetic data.

For complete runnable examples, see [sample_synthetic_data_agent_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_synthetic_data_agent_evaluation.py) and [sample_synthetic_data_model_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_synthetic_data_model_evaluation.py) on GitHub.

## Simulate conversations (preview)

Generate simulated conversations from scenario descriptions and evaluate them at the conversation level. Use this scenario to test your agent's behavior in controlled situations before deployment. The service generates realistic conversations based on your scenario descriptions and then evaluates them.

This approach is useful for:

- **Pre-deployment testing**: Validate agent behavior across diverse scenarios without real user traffic.
- **Edge case coverage**: Test scenarios that rarely occur naturally but are important to handle well.
- **Regression testing**: Ensure agent updates don't degrade performance on known scenarios.
- **Scale testing**: Generate many conversations quickly to stress-test agent capabilities.

### How conversation simulation works

1. You provide a dataset of scenario descriptions—each row describes a situation the simulated user tries to accomplish.
1. The service uses a simulator model to play the role of the user, interacting with your agent based on the scenario.
1. Each scenario generates one or more complete conversations.
1. Conversation-level evaluators assess the generated conversations.
1. Your project stores both the conversations and evaluation results.

### Prepare scenario data

> [!TIP]
> Instead of authoring scenarios by hand, you can generate them with the **Simulation seed (multi-turn)** task type in the synthetic data generation flow. The output uses the same `id` / `test_case_description` / `desired_num_turns` schema. See [Generate a simulation seed dataset](evaluation-dataset-synthetic.md#generate-a-simulation-seed-dataset-sdk).

Create a JSONL file where each line describes a scenario for the simulated user. The schema requires `id`, `test_case_description`, and `desired_num_turns`. Include details about the user's goal, context, and any constraints. For a complete example, see the [conversation evaluation samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations) in the SDK.

```json

{"id": "contoso_refund_timeline", "test_case_description": "Customer returned an item to Contoso Electronics 5 days ago and hasn't received their refund yet. They want to know how long Contoso refunds take.", "desired_num_turns": 10}
{"id": "contoso_store_hours_lookup", "test_case_description": "Customer wants to know what time the Contoso Electronics store closes today. Simple single-fact question with possibly one clarifying turn about which location.", "desired_num_turns": 3}
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `num_conversations` | No | Number of conversations to generate per scenario. Defaults to 5, server-side cap of 5. |
| `max_turns` | No | Maximum number of turns (exchanges) per conversation. Defaults to 10, server-side cap of 20. |
| `model` | Yes | Model deployment to use for simulating the user. For example, `gpt-4.1`. The [model router](../../openai/concepts/model-router.md) isn't supported as the simulator model; it can only be used as the evaluation target. |
| `sampling_params` | No | Sampling parameters for the simulator model, including `temperature`, `top_p`, and `max_completion_tokens`. |
| `data_mapping` | No | Maps fields from your scenario JSONL to simulation parameters. Common mappings: `test_case_description`, `id`, `desired_num_turns`. |

### Define evaluators

Select evaluators designed for conversation-level assessment. The simulated conversations automatically map to the evaluators.

# [Python](#tab/python)

```python
import os
from openai.types.eval_create_params import DataSourceConfigCustom
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator, PromptAgentDefinition

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
model_deployment_name = os.environ["FOUNDRY_MODEL_NAME"]
agent_name = os.environ.get("FOUNDRY_AGENT_NAME", "")

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    # Simulation uses the same "custom" eval group type as dataset evaluation (S1),
    # since the generated conversations follow the same messages schema.
    data_source_config = DataSourceConfigCustom(
        type="custom",
        item_schema={
            "type": "object",
            "properties": {
                "messages": {"type": "array"},
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

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals?api-version=2025-11-15-preview" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "conversation-simulation-evaluation",
    "data_source_config": {
      "type": "custom",
      "item_schema": {
        "type": "object",
        "properties": {
          "messages": {"type": "array"}
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

### Create evaluation and run

# [Python](#tab/python)

Prep: download [sample_data_simulation_scenarios.jsonl](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/data_folder/sample_data_simulation_scenarios.jsonl).

```python
# Create (or update) an agent to simulate against
agent = project_client.agents.create_version(
    agent_name=agent_name,
    definition=PromptAgentDefinition(
        model=model_deployment_name,
        instructions="You are a helpful customer service agent. Be empathetic and solution-oriented.",
    ),
)

# Upload scenario data
scenarios_id = project_client.datasets.upload_file(
    name="simulation-scenarios",
    version="1",
    file_path="./sample_data_simulation_scenarios.jsonl",
).id

# Create the evaluation
eval_object = openai_client.evals.create(
    name="Multi-turn Conversation Simulation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

# Create a simulation run
eval_run = openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name="conversation-simulation-run",
    data_source={
        "type": "azure_ai_target_completions",
        "source": {
            "type": "file_id",
            "id": scenarios_id,
        },
        "target": {
            "type": "azure_ai_agent",
            "name": agent.name,
            "version": agent.version,
        },
        "item_generation_params": {
            "type": "conversation_gen_preview",
            "model": model_deployment_name,
            "num_conversations": 2,
            "max_turns": 5,
            "sampling_params": {
                "temperature": 0.7,
                "top_p": 1.0,
                "max_completion_tokens": 800,
            },
            "data_mapping": {
                "test_case_description": "test_case_description",
                "id": "id",
                "desired_num_turns": "desired_num_turns",
            },
        },
    },
    extra_body={"evaluation_level": "conversation"},
)
```

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals/${EVAL_ID}/runs?api-version=2025-11-15-preview" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "conversation-simulation-run",
    "evaluation_level": "conversation",
    "data_source": {
      "type": "azure_ai_target_completions",
      "source": {
        "type": "file_id",
        "id": "YOUR_SCENARIOS_DATASET_ID"
      },
      "target": {
        "type": "azure_ai_agent",
        "name": "my-agent",
        "version": "1"
      },
      "item_generation_params": {
        "type": "conversation_gen_preview",
        "model": "gpt-4.1",
        "num_conversations": 2,
        "max_turns": 5,
        "sampling_params": {
          "temperature": 0.7,
          "top_p": 1.0,
          "max_completion_tokens": 800
        },
        "data_mapping": {
        }
      }
    }
  }'
```

---

## Next steps

- To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).
- For a complete runnable example, see [sample_multiturn_conversation_simulation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_multiturn_conversation_simulation.py) on GitHub.
