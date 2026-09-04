---
title: "Generate synthetic data with the Microsoft Foundry SDK"
description: "Learn how to use the Microsoft Foundry SDK to generate synthetic evaluation queries for model and agent targets."
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
# customer intent: As a developer, I want to generate synthetic evaluation data so that I can test models and agents before I have representative production data.
---

# Generate synthetic evaluation data with Microsoft Foundry SDK (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Generate individual test queries, send them to a model or agent target, and evaluate the target responses.

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

# [JavaScript/TypeScript](#tab/javascript)

The current JavaScript/TypeScript SDK samples don't demonstrate synthetic data evaluation. Use the Python or cURL tab for this flow.

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
