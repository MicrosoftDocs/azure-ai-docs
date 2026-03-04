---
title: "Cloud Evaluation with the Microsoft Foundry SDK"
description: "Run scalable evaluations for generative AI applications using the Microsoft Foundry SDK. Learn how to integrate evaluations into your development pipeline."
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - references_regions
  - ignite-2024
ms.topic: how-to
ms.date: 03/04/2026
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
# customer intent: As a developer, I want to run evaluations in the cloud using the Microsoft Foundry SDK so I can test my generative AI application on large datasets without managing local compute infrastructure.
ai-usage: ai-assisted
---

# Run evaluations in the cloud by using the Microsoft Foundry SDK
[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this article, you learn how to run evaluations in the cloud (preview) for predeployment testing on a test dataset. 

Use cloud evaluations for most scenarios—especially when testing at scale, integrating evaluations into continuous integration and continuous delivery (CI/CD) pipelines, or performing predeployment testing. Running evaluations in the cloud eliminates the need to manage local compute infrastructure and supports large-scale, automated testing workflows. You can also [schedule evaluations](../../observability/how-to/how-to-monitor-agents-dashboard.md) to run on a recurring basis, or set up [continuous evaluation](../../observability/how-to/how-to-monitor-agents-dashboard.md#set-up-continuous-evaluation-python-sdk) to automatically evaluate sampled agent responses in production.

Cloud evaluation results are stored in your Foundry project. You can review results in the portal, retrieve them through the SDK, or route them to Application Insights if connected. Cloud evaluation supports all Microsoft-curated [built-in evaluators](../../concepts/observability.md#what-are-evaluators) and your own [custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md). Evaluators are managed in the [evaluator catalog](../evaluate-generative-ai-app.md) with the same project-scope, role-based access control.

> [!TIP]
> For complete runnable examples, see the [Python SDK evaluation samples](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/README.md) on GitHub.

When you use the Foundry SDK, it logs evaluation results in your Foundry project for better observability. This feature supports all Microsoft-curated [built in evaluators](../../concepts/built-in-evaluators.md). and your own [custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md). Your evaluators can be located in the [evaluator library](../evaluate-generative-ai-app.md) and have the same project-scope, role-based access control.
## How cloud evaluation works

To run a cloud evaluation, you create an evaluation definition with your data schema and testing criteria (evaluators), then create an evaluation run. The run executes each evaluator against your data and returns scored results that you can poll for completion.

Cloud evaluation supports the following scenarios:

| Scenario | When to use | Data source type | Target |
|----------|-------------|------------------|--------|
| **[Dataset evaluation](#dataset-evaluation)** | Evaluate pre-computed responses in a JSONL file. | `jsonl` | — |
| **[Model target evaluation](#model-target-evaluation)** | Provide queries and generate responses from a model at runtime for evaluation. | `azure_ai_target_completions` | `azure_ai_model` |
| **[Agent target evaluation](#agent-target-evaluation)** | Provide queries and generate responses from a Foundry agent at runtime for evaluation. | `azure_ai_target_completions` | `azure_ai_agent` |
| **[Agent response evaluation](#agent-response-evaluation)** | Retrieve and evaluate Foundry agent responses by response IDs. | `azure_ai_responses` | — |
| **[Synthetic data evaluation (preview)](#synthetic-data-evaluation-preview)** | Generate synthetic test queries, send them to a model or agent, and evaluate the responses. | `azure_ai_synthetic_data_gen_preview` | `azure_ai_model` or `azure_ai_agent` |
| **[Red team evaluation](run-ai-red-teaming-cloud.md)** | Run automated adversarial testing against a model or agent. | `azure_ai_red_team` | `azure_ai_model` or `azure_ai_agent` |

Most scenarios require input data. You can provide data in two ways:

| Source type | Description |
|-------------|-------------|
| `file_id` | Reference an uploaded dataset by ID. |
| `file_content` | Provide data inline in the request. |

Every evaluation requires a `data_source_config` that tells the service what fields to expect in your data:

- **`custom`** — You define an `item_schema` with your field names and types. Set `include_sample_schema` to `true` when using a target so evaluators can reference generated responses.
- **`azure_ai_source`** — The schema is inferred from the service. Set `"scenario"` to `"responses"` for agent response evaluation, `"synthetic_data_gen_preview"` for [synthetic data evaluation (preview)](#synthetic-data-evaluation-preview), or `"red_team"` for [red teaming](run-ai-red-teaming-cloud.md).

Each scenario requires evaluators that define your testing criteria. For guidance on selecting evaluators, see [built-in evaluators](../../concepts/observability.md#what-are-evaluators).

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md).
- An Azure OpenAI deployment with a GPT model that supports chat completion (for example, `gpt-5-mini`).
- **Azure AI User** role on the Foundry project.
- Optionally, you can [use your own storage account](../../concepts/evaluation-regions-limits-virtual-network.md#bring-your-own-storage) to run evaluations.

> [!NOTE]
> Some evaluation features have regional restrictions. See [supported regions](../../concepts/evaluation-evaluators/risk-safety-evaluators.md#foundry-project-configuration-and-region-support) for details.

## Get started

Install the SDK and set up your client:

```bash
pip install --pre "azure-ai-projects>=2.0.0b4"
```

```python
import os
from azure.identity import DefaultAzureCredential 
from azure.ai.projects import AIProjectClient 
from openai.types.eval_create_params import DataSourceConfigCustom
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
    SourceFileID,
)

# Azure AI Project endpoint
# Example: https://<account_name>.services.ai.azure.com/api/projects/<project_name>
endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

# Model deployment name (for AI-assisted evaluators)
# Example: gpt-5-mini
model_deployment_name = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "")

# Dataset details (optional, for reusing existing datasets)
dataset_name = os.environ.get("DATASET_NAME", "")
dataset_version = os.environ.get("DATASET_VERSION", "1")

# Create the project client
project_client = AIProjectClient( 
    endpoint=endpoint, 
    credential=DefaultAzureCredential(), 
)

# Get the OpenAI client for evaluation API
client = project_client.get_openai_client()
```

## <a name = "uploading-evaluation-data"></a> Prepare input data

Most evaluation scenarios require input data. You can provide data in two ways:

### Upload a dataset (recommended)

Upload a JSONL file to create a versioned dataset in your Foundry project. Datasets support versioning and reuse across multiple evaluation runs. Use this approach for production testing and CI/CD workflows.

Prepare a JSONL file with one JSON object per line containing the fields your evaluators need:

```json
{"query": "What is machine learning?", "response": "Machine learning is a subset of AI.", "ground_truth": "Machine learning is a type of AI that learns from data."}
{"query": "Explain neural networks.", "response": "Neural networks are computing systems inspired by biological neural networks.", "ground_truth": "Neural networks are a set of algorithms modeled after the human brain."}
```

```python
# Upload a local JSONL file. Skip this step if you already have a dataset registered.
data_id = project_client.datasets.upload_file(
    name=dataset_name,
    version=dataset_version,
    file_path="./evaluate_test_data.jsonl",
).id
```

### Provide data inline

For quick experimentation with small test sets, provide data directly in the evaluation request using `file_content`.

```python
source = SourceFileContent(
    type="file_content",
    content=[
        SourceFileContentContent(
            item={
                "query": "How can I safely de-escalate a tense situation?",
                "ground_truth": "Encourage calm communication, seek help if needed, and avoid harm.",
            }
        ),
        SourceFileContentContent(
            item={
                "query": "What is the largest city in France?",
                "ground_truth": "Paris",
            }
        ),
    ],
)
```

Pass `source` as the `"source"` field in your data source configuration when creating a run. The scenario sections that follow use `file_id` by default.

## Dataset evaluation

Evaluate pre-computed responses in a JSONL file using the `jsonl` data source type. This scenario is useful when you already have model outputs and want to assess their quality.

> [!TIP]
> Before you begin, complete [Get started](#get-started) and [Prepare input data](#uploading-evaluation-data).

### Define the data schema and evaluators

Specify the schema that matches your JSONL fields, and select the evaluators (testing criteria) to run. Use the `data_mapping` parameter to connect fields from your input data to evaluator parameters with `{{item.field}}` syntax. Always include `data_mapping` with the required input fields for each evaluator. Your field names must match those in your JSONL file — for example, if your data has `"question"` instead of `"query"`, use `"{{item.question}}"` in the mapping. For the required parameters per evaluator, see [built-in evaluators](../../concepts/observability.md#what-are-evaluators).

# [Python](#tab/python)

```python
data_source_config = DataSourceConfigCustom(
    type="custom",
    item_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "response": {"type": "string"},
            "ground_truth": {"type": "string"},
        },
        "required": ["query", "response", "ground_truth"],
    },
)

testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "f1",
        "evaluator_name": "builtin.f1_score",
        "data_mapping": {
            "response": "{{item.response}}",
            "ground_truth": "{{item.ground_truth}}",
        },
    },
]
```

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals?api-version=v1" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "dataset-evaluation",
    "data_source_config": {
      "type": "custom",
      "item_schema": {
        "type": "object",
        "properties": {
          "query": { "type": "string" },
          "response": { "type": "string" },
          "ground_truth": { "type": "string" }
        },
        "required": ["query", "response", "ground_truth"]
      }
    },
    "testing_criteria": [
  }'
```

---

### Create evaluation and run

Create the evaluation, then start a run against your uploaded dataset. The run executes each evaluator on every row in the dataset.

# [Python](#tab/python)

```python
# Create the evaluation
eval_object = client.evals.create(
    name="dataset-evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

# Create a run using the uploaded dataset
eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="dataset-run",
    data_source=CreateEvalJSONLRunDataSourceParam(
        type="jsonl",
        source=SourceFileID(
            type="file_id",
            id=data_id,
        ),
    ),
)
```

# [cURL](#tab/curl)

```bash
# Step 1: Create the evaluation
EVAL_ID=$(curl --silent --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals?api-version=v1" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "dataset-evaluation",
    "data_source_config": {
      "type": "custom",
      "item_schema": {
        "type": "object",
        "properties": {
          "query": { "type": "string" },
          "response": { "type": "string" },
          "ground_truth": { "type": "string" }
        },
        "required": ["query", "response", "ground_truth"]
      }
    },
    "testing_criteria": [
      {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": { "deployment_name": "gpt-5-mini" },
        "data_mapping": {
          "query": "{{item.query}}",
          "response": "{{item.response}}"
        }
      },
      {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "initialization_parameters": { "deployment_name": "gpt-5-mini" },
        "data_mapping": {
          "query": "{{item.query}}",
          "response": "{{item.response}}"
        }
      },
      {
        "type": "azure_ai_evaluator",
        "name": "f1",
        "evaluator_name": "builtin.f1_score",
        "data_mapping": {
          "response": "{{item.response}}",
          "ground_truth": "{{item.ground_truth}}"
        }
      }
    ]
  }' | jq -r '.id')

# Step 2: Create a run against your dataset
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals/${EVAL_ID}/runs?api-version=v1" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "dataset-run",
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

For a complete runnable example, see [sample_evaluations_builtin_with_dataset_id.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_builtin_with_dataset_id.py) on GitHub. To poll for completion and interpret results, see [Get results](#get-results).

## Model target evaluation

Send queries to a deployed model at runtime and evaluate the responses using the `azure_ai_target_completions` data source type with an `azure_ai_model` target. Your input data contains queries; the model generates responses which are then evaluated.

> [!TIP]
> Before you begin, complete [Get started](#get-started) and [Prepare input data](#uploading-evaluation-data).

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
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    },
]
```

### Create evaluation and run

# [Python](#tab/python)

```python
eval_object = client.evals.create(
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

eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="model-target-evaluation",
    data_source=data_source,
)
```

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals/${EVAL_ID}/runs?api-version=v1" \
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

For a complete runnable example, see [sample_model_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_model_evaluation.py) on GitHub. To poll for completion and interpret results, see [Get results](#get-results).

> [!TIP]
> To add another evaluation run,  you can use the same code.

## Agent target evaluation

Send queries to a Foundry agent at runtime and evaluate the responses using the `azure_ai_target_completions` data source type with an `azure_ai_agent` target.

> [!TIP]
> Before you begin, complete [Get started](#get-started) and [Prepare input data](#uploading-evaluation-data).

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
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "task_adherence",
        "evaluator_name": "builtin.task_adherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
    },
]
```

### Create evaluation and run

# [Python](#tab/python)

```python
eval_object = client.evals.create(
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

agent_eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="agent-target-evaluation",
    data_source=data_source,
)
```

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals/${EVAL_ID}/runs?api-version=v1" \
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

For a complete runnable example, see [sample_agent_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_agent_evaluation.py) on GitHub. To poll for completion and interpret results, see [Get results](#get-results).

## Agent response evaluation

Retrieve and evaluate Foundry agent responses by response IDs using the `azure_ai_responses` data source type. Use this scenario to evaluate specific agent interactions after they occur.

> [!TIP]
> Before you begin, complete [Get started](#get-started).

A **response ID** is a unique identifier returned each time a Foundry agent generates a response. You can collect response IDs from agent interactions by using the [Responses API](/rest/api/aifoundry) or from your application's trace logs. Provide the IDs inline as file content, or upload them as a dataset (see [Prepare input data](#uploading-evaluation-data)).

### Collect response IDs

Each call to the Responses API returns a response object with a unique `id` field. Collect these IDs from your application's interactions, or generate them directly:

```python
# Generate response IDs by calling a model through the Responses API
response = client.responses.create(
    model=model_deployment_name,
    input="What is machine learning?",
)
print(response.id)  # Example: resp_abc123
```

You can also collect response IDs from agent interactions in your application's trace logs or monitoring pipeline. Each response ID uniquely identifies a stored response that the evaluation service can retrieve.

### Create evaluation and run

# [Python](#tab/python)

```python
data_source_config = {"type": "azure_ai_source", "scenario": "responses"}

testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
    },
]

eval_object = client.evals.create(
    name="Agent Response Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

data_source = {
    "type": "azure_ai_responses",
    "item_generation_params": {
        "type": "response_retrieval",
        "data_mapping": {"response_id": "{{item.resp_id}}"},
        "source": {
            "type": "file_content",
            "content": [
                {"item": {"resp_id": "resp_abc123"}},
                {"item": {"resp_id": "resp_def456"}},
            ]
        },
    },
}

eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="agent-response-evaluation",
    data_source=data_source,
)
```

# [cURL](#tab/curl) 

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals/${EVAL_ID}/runs?api-version=v1" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "agent-response-evaluation",
    "data_source": {
      "type": "azure_ai_responses",
      "item_generation_params": {
        "type": "response_retrieval",
        "data_mapping": {"response_id": "{{item.resp_id}}"},
        "source": {
          "type": "file_content",
          "content": [
            {"item": {"resp_id": "resp_abc123"}},
            {"item": {"resp_id": "resp_def456"}}
          ]
        }
      }
    }
  }'
```

---

For a complete runnable example, see [sample_agent_response_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_agent_response_evaluation.py) on GitHub. To poll for completion and interpret results, see [Get results](#get-results).

## Synthetic data evaluation (preview)

Generate synthetic test queries, send them to a deployed model or Foundry agent, and evaluate the responses using the `azure_ai_synthetic_data_gen_preview` data source type. Use this scenario when you don't have a test dataset — the service generates queries based on a prompt you provide (or from the agent's instructions), runs them against your target, and evaluates the responses.

> [!TIP]
> Before you begin, complete [Get started](#get-started).

### How synthetic data evaluation works

1. The service generates synthetic queries based on your `prompt` and optional seed data files.
1. Each query is sent to the specified target (model or agent) to generate a response.
1. Evaluators score each response using the generated query and response.
1. The generated queries are stored as a dataset in your project for reuse.

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `samples_count` | Yes | Number of synthetic test queries to generate. |
| `model_deployment_name` | Yes | Model deployment to use for generating synthetic queries. |
| `prompt` | No | Instructions describing the type of queries to generate. Optional when the agent target has instructions configured. |
| `output_dataset_name` | No | Name for the output dataset where generated queries are stored. If not provided, the service generates a name automatically. |
| `sources` | No | Seed data files (by file ID) to improve relevance of generated queries. |

### Set up evaluators and data mappings

The synthetic data generator produces queries in the `{{item.query}}` field. The target generates responses available in `{{sample.output_text}}`. Map these fields to your evaluators:

```python
data_source_config = {"type": "azure_ai_source", "scenario": "synthetic_data_gen_preview"}

testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name,
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_text}}",
        },
    },
]
```

### Create evaluation and run

# [Python](#tab/python)

#### Model target

Generate synthetic queries and evaluate a model:

```python
eval_object = client.evals.create(
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

eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="synthetic-data-evaluation",
    data_source=data_source,
)
```

You can optionally add a system prompt to shape the target model's behavior. When you use `input_messages` with synthetic data generation, include only `system` role messages — the service provides the generated queries as user messages automatically.

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

eval_run = client.evals.runs.create(
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
          "deployment_name": "gpt-5-mini"
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

To poll for completion and interpret results, see [Get results](#get-results).

## Get results

After an evaluation run completes, retrieve the scored results and review them in the portal or programmatically.

### Poll for results

Evaluation runs are asynchronous. Poll the run status until it completes, then retrieve the results:

```python
import time
from pprint import pprint

while True:
    run = client.evals.runs.retrieve(
        run_id=eval_run.id, eval_id=eval_object.id
    )
    if run.status in ("completed", "failed"):
        break
    time.sleep(5)
    print("Waiting for eval run to complete...")

# Retrieve results
output_items = list(
    client.evals.runs.output_items.list(
        run_id=run.id, eval_id=eval_object.id
    )
)
pprint(output_items)
print(f"Report URL: {run.report_url}")
```

### Interpret results

For a single data example, all evaluators output the following schema:  

- **Label**: a binary "pass" or "fail" label, similar to a unit test's output. Use this result to facilitate comparisons across evaluators.
- **Score**: a score from the natural scale of each evaluator. Some evaluators use a fine-grained rubric, scoring on a 5-point scale (quality evaluators) or a 7-point scale (content safety evaluators). Others, like textual similarity evaluators, use F1 scores, which are floats between 0 and 1. Any non-binary "score" is binarized to "pass" or "fail" in the "label" field based on the "threshold".
- **Threshold**: any non-binary scores are binarized to "pass" or "fail" based on a default threshold, which the user can override in the SDK experience.
- **Reason**: To improve intelligibility, all LLM-judge evaluators also output a reasoning field to explain why a certain score is given.
- **Details**: (optional) For some evaluators, such as tool_call_accuracy, there might be a "details" field or flags that contain additional information to help users debug their applications.

### Example output (single item)

```json
{
  "type": "azure_ai_evaluator",
  "name": "Coherence",
  "metric": "coherence",
  "score": 4.0,
  "label": "pass",
  "reason": "The response is well-structured and logically organized, presenting information in a clear and coherent manner.",
  "threshold": 3,
  "passed": true
}
```

### Example output (aggregate)

For aggregate results over multiple data examples (a dataset), the average rate of the examples with a "pass" forms the passing rate for that dataset.

```json
{
  "eval_id": "eval_abc123",
  "run_id": "run_xyz789",
  "status": "completed",
  "result_counts": {
    "passed": 85,
    "failed": 15,
    "total": 100
  },
  "per_testing_criteria_results": [
    {
      "name": "coherence",
      "passed": 92,
      "failed": 8,
      "pass_rate": 0.92
    },
    {
      "name": "relevance", 
      "passed": 78,
      "failed": 22,
      "pass_rate": 0.78
    }
  ]
}
```

## Troubleshooting

### Job running for a long time

Your evaluation job might remain in the **Running** state for an extended period. This typically occurs when the Azure OpenAI model deployment doesn't have enough capacity, causing the service to retry requests.

**Resolution:**

1. Cancel the current evaluation job using `client.evals.runs.cancel(run_id, eval_id=eval_id)`.
1. Increase the model capacity in the Azure portal.
1. Run the evaluation again.

### Authentication errors

If you receive a `401 Unauthorized` or `403 Forbidden` error, verify that:

- Your `DefaultAzureCredential` is configured correctly (run `az login` if using Azure CLI).
- Your account has the **Azure AI User** role on the Foundry project.
- The project endpoint URL is correct and includes both the account and project names.

### Data format errors

If the evaluation fails with a schema or data mapping error:

- Verify your JSONL file has one valid JSON object per line.
- Confirm that field names in `data_mapping` match the field names in your JSONL file exactly (case-sensitive).
- Check that `item_schema` properties match the fields in your dataset.

### Rate limit errors

Evaluation run creations are rate-limited at the tenant, subscription, and project levels. If you receive a `429 Too Many Requests` response:

- Check the `retry-after` header in the response for the recommended wait time.
- Review the response body for rate limit details.
- Use exponential backoff when retrying failed requests.

If an evaluation job fails with a `429` error during execution:

- Reduce the size of your evaluation dataset or split it into smaller batches.
- Increase the tokens-per-minute (TPM) quota for your model deployment in the Azure portal.

### Agent evaluator tool errors

If an agent evaluator returns an error for unsupported tools:

- Check the [supported tools](../../concepts/evaluation-evaluators/agent-evaluators.md#supported-tools) for agent evaluators.
- As a workaround, wrap unsupported tools as user-defined function tools so the evaluator can assess them.

## Related content

- [Complete working samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations)
- [Evaluate your AI agents continuously](../../../foundry-classic/how-to/continuous-evaluation-agents.md)
- [See evaluation results in the Foundry portal](../../how-to/evaluate-results.md)
- [Get started with Foundry](../../quickstarts/get-started-code.md)
- [REST API reference](../../reference/foundry-project-rest-preview.md#openai-evals---list-evals)
