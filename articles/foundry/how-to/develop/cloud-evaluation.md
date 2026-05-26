---
title: "Cloud Evaluation with the Microsoft Foundry SDK"
description: "Run scalable evaluations for generative AI applications using the Microsoft Foundry SDK. Learn how to integrate evaluations into your development pipeline."
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom:
  - classic-and-new
  - references_regions
  - ignite-2024
ms.topic: how-to
ms.date: 06/02/2026
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
# customer intent: As a developer, I want to run evaluations in the cloud using the Microsoft Foundry SDK so I can test my generative AI application on large datasets without managing local compute infrastructure.
ai-usage: ai-assisted
---

# Run evaluations in the cloud by using the Microsoft Foundry SDK

In this article, you learn how to run evaluations in the cloud for predeployment testing on a test dataset.

Use cloud evaluations for most scenarios—especially when testing at scale, integrating evaluations into continuous integration and continuous delivery (CI/CD) pipelines, or performing predeployment testing. Running evaluations in the cloud eliminates the need to manage local compute infrastructure and supports large-scale, automated testing workflows. You can also [schedule evaluations](../../observability/how-to/how-to-monitor-agents-dashboard.md) to run on a recurring basis, or set up [continuous evaluation](../../observability/how-to/how-to-monitor-agents-dashboard.md#) to automatically evaluate sampled agent responses in production.

Cloud evaluation results are stored in your Foundry project. You can review results in the portal, retrieve them through the SDK, or route them to Application Insights if connected. Cloud evaluation supports all Microsoft-curated [built-in evaluators](../../concepts/observability.md#what-are-evaluators) and your own [custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md). Evaluators are managed in the [evaluator catalog](../evaluate-generative-ai-app.md) with the same project-scope, role-based access control.

> [!TIP]
> For complete runnable examples, see the [Python SDK evaluation samples](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/README.md) on GitHub.

## How cloud evaluation works

To run a cloud evaluation, you create an evaluation definition with your data schema and testing criteria (evaluators), then create an evaluation run. The run executes each evaluator against your data and returns scored results that you can poll for completion.

Cloud evaluation supports the following scenarios:

| Scenario | When to use | Data source type | Target |
|----------|-------------|------------------|--------|
| **[Dataset evaluation](#dataset-evaluation)** | Evaluate pre-computed responses in a JSONL file. | `jsonl` | — |
| **[CSV dataset evaluation](#csv-dataset-evaluation)** | Evaluate pre-computed responses in a CSV file. | `csv` | — |
| **[Model target evaluation](#model-target-evaluation)** | Provide queries and generate responses from a model at runtime for evaluation. | `azure_ai_target_completions` | `azure_ai_model` |
| **[Agent target evaluation](#agent-target-evaluation)** | Provide queries and generate responses from a Foundry agent (prompt or hosted) at runtime for evaluation. | `azure_ai_target_completions` | `azure_ai_agent` |
| **[Agent response evaluation](#agent-response-evaluation)** | Retrieve and evaluate Foundry agent responses by response IDs. | `azure_ai_responses` | — |
| **[Trace evaluation](#trace-evaluation)** | Evaluate agent interactions already captured in Application Insights by trace ID. Use this approach for non-Foundry agents (LangChain and custom frameworks that adhere to OpenTelemetry based logging). Use azure_ai_trace_data_source_preview to also evaluate conversational traces by conversation ID. | `azure_ai_traces_preview` or `azure_ai_trace_data_source_preview` | — |
| **[Synthetic data evaluation (preview)](#synthetic-data-evaluation-preview)** | Generate synthetic test queries, send them to a model or agent, and evaluate the responses. | `azure_ai_synthetic_data_gen_preview` | `azure_ai_model` or `azure_ai_agent` |
| **[Conversation evaluation](#multiturn-conversation-evaluation)** | Evaluate complete multi-turn conversations from input conversation data. | `jsonl` | — |
| **[Conversation simulation](#conversation-simulation)** | Generate simulated multi-turn conversations from scenario descriptions and evaluate them. | `azure_ai_target_completions` | `azure_ai_agent` |
| **[Red team evaluation](run-ai-red-teaming-cloud.md)** | Run automated adversarial testing against a model or agent. | `azure_ai_red_team` | `azure_ai_model` or `azure_ai_agent` |

Most scenarios require input data. You can provide data in two ways:

| Source type | Description |
|-------------|-------------|
| `file_id` | Reference an uploaded dataset by ID. |
| `file_content` | Provide data inline in the request. |

Every evaluation requires a `data_source_config` that tells the service what fields to expect in your data:

- **`custom`** — You define an `item_schema` with your field names and types. Set `include_sample_schema` to `true` when using a target so evaluators can reference generated responses.
- **`azure_ai_source`** — The schema is inferred from the service. Set `"scenario"` to `"responses"` for agent response evaluation, `"traces"` for [trace evaluation](#trace-evaluation), `"synthetic_data_gen_preview"` for [synthetic data evaluation (preview)](#synthetic-data-evaluation-preview), `"conversation_simulation"` for [conversation simulation](#conversation-simulation), or `"red_team"` for [red teaming](run-ai-red-teaming-cloud.md).

Each scenario requires evaluators that define your testing criteria. For guidance on selecting evaluators, see [built-in evaluators](../../concepts/observability.md#what-are-evaluators).

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md).
- An Azure OpenAI deployment with a GPT model that supports chat completion (for example, `gpt-5-mini`).
- **Foundry User** role on the Foundry project.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]
- Optionally, you can [use your own storage account](../../concepts/evaluation-regions-limits-virtual-network.md#bring-your-own-storage) to run evaluations.

> [!NOTE]
> Some evaluation features have regional restrictions. See [supported regions](../../concepts/evaluation-evaluators/risk-safety-evaluators.md#foundry-project-configuration-and-region-support) for details.

## Get started

Install the SDK and set up your client:

```bash
pip install "azure-ai-projects>=2.0.0"
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

Upload a JSONL or CSV file to create a versioned dataset in your Foundry project. Datasets support versioning and reuse across multiple evaluation runs. Use this approach for production testing and CI/CD workflows.

Prepare a JSONL file with one JSON object per line containing the fields your evaluators need:

```json
{"query": "What is machine learning?", "response": "Machine learning is a subset of AI.", "ground_truth": "Machine learning is a type of AI that learns from data."}
{"query": "Explain neural networks.", "response": "Neural networks are computing systems inspired by biological neural networks.", "ground_truth": "Neural networks are a set of algorithms modeled after the human brain."}
```

Or prepare a CSV file with column headers matching your evaluator fields:

```csv
query,response,ground_truth
What is machine learning?,Machine learning is a subset of AI.,Machine learning is a type of AI that learns from data.
Explain neural networks.,Neural networks are computing systems inspired by biological neural networks.,Neural networks are a set of algorithms modeled after the human brain.
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
            "model": model_deployment_name
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
            "model": model_deployment_name
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
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/v1/evals" \
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
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/v1/evals" \
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
        "initialization_parameters": { "model": "gpt-5-mini" },
        "data_mapping": {
          "query": "{{item.query}}",
          "response": "{{item.response}}"
        }
      },
      {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "initialization_parameters": { "model": "gpt-5-mini" },
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
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/v1/evals/${EVAL_ID}/runs" \
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

## CSV dataset evaluation

Evaluate pre-computed responses in a CSV file using the `csv` data source type. This scenario works the same way as [dataset evaluation](#dataset-evaluation) but accepts CSV files instead of JSONL. Use CSV when your data is already in spreadsheet or tabular format.

> [!TIP]
> Before you begin, complete [Get started](#get-started) and [Prepare input data](#uploading-evaluation-data).

### Prepare a CSV file

Create a CSV file with column headers matching the fields your evaluators need. Each row represents one test case:

```csv
query,response,context,ground_truth
What is cloud computing?,Cloud computing delivers computing services over the internet.,Cloud computing is a technology for on-demand resource delivery.,Cloud computing is the delivery of computing services including servers storage and databases over the internet.
What is machine learning?,Machine learning is a subset of AI that learns from data.,Machine learning is a branch of artificial intelligence.,Machine learning is a type of AI that enables computers to learn from data without being explicitly programmed.
Explain neural networks.,Neural networks are computing systems inspired by biological neural networks.,Neural networks are used in deep learning.,Neural networks are a set of algorithms modeled after the human brain designed to recognize patterns.
```

### Upload and run

Upload the CSV file as a dataset, then create an evaluation using the `csv` data source type. The schema definition and evaluator configuration are the same as for JSONL evaluations — the only difference is the `"type": "csv"` in the data source.

```python
# Upload the CSV file
data_id = project_client.datasets.upload_file(
    name="eval-csv-data",
    version="1",
    file_path="./evaluation_data.csv",
).id

# Define the schema matching your CSV columns
data_source_config = DataSourceConfigCustom(
    type="custom",
    item_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "response": {"type": "string"},
            "context": {"type": "string"},
            "ground_truth": {"type": "string"},
        },
        "required": [],
    },
    include_sample_schema=True,
)

# Define evaluators with data mappings to CSV columns
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
        "initialization_parameters": {"model": model_deployment_name},
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
        "initialization_parameters": {"model": model_deployment_name},
    },
    {
        "type": "azure_ai_evaluator",
        "name": "f1",
        "evaluator_name": "builtin.f1_score",
    },
]

# Create the evaluation
eval_object = client.evals.create(
    name="CSV evaluation with built-in evaluators",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

# Create a run using the CSV data source type
eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="csv-evaluation-run",
    data_source={
        "type": "csv",
        "source": {
            "type": "file_id",
            "id": data_id,
        },
    },
)
```

To poll for completion and interpret results, see [Get results](#get-results).

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
            "model": model_deployment_name,
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

For a complete runnable example, see [sample_model_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_model_evaluation.py) on GitHub. To poll for completion and interpret results, see [Get results](#get-results).

> [!TIP]
> To add another evaluation run, you can use the same code.

## Agent target evaluation

Send queries to a Foundry agent at runtime and evaluate the responses using the `azure_ai_target_completions` data source type with an `azure_ai_agent` target. This scenario works for both [prompt agents](../../agents/overview.md) and [hosted agents](../../agents/concepts/hosted-agents.md).

> [!TIP]
> Before you begin, complete [Get started](#get-started) and [Prepare input data](#uploading-evaluation-data).
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
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "model": model_deployment_name,
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
            "model": model_deployment_name,
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

For a complete runnable example, see [sample_agent_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_agent_evaluation.py) on GitHub. To poll for completion and interpret results, see [Get results](#get-results).

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
eval_object = client.evals.create(
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

eval_run = client.evals.runs.create(
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
            "model": model_deployment_name,
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
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/v1/evals/${EVAL_ID}/runs" \
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

## Trace evaluation

Evaluate agent interactions that were already captured in [Application Insights](/azure/azure-monitor/app/app-insights-overview). Use the `azure_ai_traces` data source type. This scenario is useful for post-deployment evaluation of real production traffic — you select traces from your monitoring pipeline and run evaluators against them without replaying any requests.

> [!IMPORTANT]
> Trace evaluation is the recommended approach for evaluating **agents not built with the Microsoft Foundry Agent Service** — including LangChain and custom frameworks. As long as your agent emits [OpenTelemetry spans following the GenAI semantic conventions](#trace-data-requirements) to Application Insights, trace evaluation can assess its interactions using the same evaluators available for Foundry agents.

Trace evaluation supports two modes:

- **By trace IDs** — Evaluate specific agent interactions by providing their `operation_Id` values from Application Insights.
- **By agent filter** — Automatically discover and evaluate recent traces for a given agent, without manually collecting trace IDs.

> [!TIP]
> Before you begin, complete [Get started](#get-started). This scenario also requires an [Application Insights resource connected to your Foundry project](../../observability/how-to/trace-agent-setup.md).

### Trace data requirements

Trace evaluation requires your agent to emit spans following the [OpenTelemetry semantic conventions for generative AI](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/). Specifically, the evaluation service reads **`invoke_agent` spans** from Application Insights and extracts conversation data from their attributes.

The following span attributes are used:

| Attribute | Required | Description |
|-----------|----------|-------------|
| `gen_ai.operation.name` | **Yes** | Must equal `"invoke_agent"`. The service ignores all other spans. |
| `gen_ai.agent.id` | For agent filter mode | Unique agent identifier (format: `agent-name:version`). |
| `gen_ai.agent.name` | For agent filter mode | Human-readable agent name. |
| `gen_ai.input.messages` | For evaluators query inputs | JSON array of input messages following the [GenAI semantic conventions message format](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/#invoke-agent-span). Messages with role `user` or `system` map to `query`; messages with role `assistant` or `tool` map to `response`. |
| `gen_ai.output.messages` | For evaluators query inputs | JSON array of model-generated output messages. All output messages map to `response`. If output also contains type: tool_call or type: tool_result, it maps to `tool_calls` |
| `gen_ai.tool.definitions` | Optional | JSON array of tool schemas available to the agent. If absent, the service attempts to infer tool definitions from tool call messages, but inferred schemas may be incomplete. |
| `gen_ai.conversation.id` | Optional | Conversation identifier, passed through to evaluation results for correlation. |

> [!NOTE]
> If `gen_ai.input.messages` and `gen_ai.output.messages` are empty or missing, quality evaluators (coherence, fluency, relevance, intent resolution) will return `score=None`. Safety evaluators (violence, self-harm, sexual, hate/unfairness) can still produce scores with partial data but they may not produce meaningful results.

For Python agents built with the Azure AI Agent Server SDK, add the `[tracing]` extra to enable automatic span emission:

```bash
pip install "azure-ai-agentserver-core[tracing]"
```

### Prerequisites for trace evaluation

In addition to the general [prerequisites](#prerequisites), trace evaluation requires:

- An [Application Insights resource](/azure/azure-monitor/app/app-insights-overview) connected to your Foundry project. See [Set up tracing in Microsoft Foundry](../../observability/how-to/trace-agent-setup.md).
- The project's managed identity must have the **Log Analytics Reader** role on both the Application Insights resource and its linked Log Analytics workspace.
- The `azure-monitor-query` Python package (only needed if you collect trace IDs manually).

```bash
pip install "azure-ai-projects>=2.2.0" azure-monitor-query
```

Set these environment variables:

- `APPINSIGHTS_RESOURCE_ID` — The Application Insights resource ID (for example, `/subscriptions/<subscription_id>/resourceGroups/<rg_name>/providers/Microsoft.Insights/components/<resource_name>`).
- `AGENT_ID` — The agent identifier emitted by the tracing integration (`gen_ai.agent.id` attribute), used to filter traces. Format: `agent-name:version`.
- `TRACE_LOOKBACK_HOURS` — (Optional) Number of hours to look back when querying traces. Defaults to `1`.

### Option A: Evaluate by agent filter

The simplest approach — let the service automatically discover and evaluate recent traces for a specific agent. No manual trace ID collection needed.

```python
import os

agent_id = os.environ["AGENT_ID"]  # e.g., "my-weather-agent:1"
trace_lookback_hours = int(os.environ.get("TRACE_LOOKBACK_HOURS", "1"))

# Create the evaluation
data_source_config = {
    "type": "azure_ai_source",
    "scenario": "traces",
}

eval_object = client.evals.create(
    name="Agent Trace Evaluation (by agent)",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,  # See "Set up evaluators" below
)

# Create a run — the service queries App Insights for matching traces
data_source = {
    "type": "azure_ai_traces",
    "agent_id": agent_id,
    "max_traces": 50,           # Maximum number of traces to evaluate
    "lookback_hours": trace_lookback_hours,
}

eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="agent-trace-eval-run",
    data_source=data_source,
)

print(f"Evaluation run started: {eval_run.id}")
```

The service filters `invoke_agent` spans by the `gen_ai.agent.id` attribute, samples up to `max_traces` unique trace IDs, and evaluates all spans from those traces.

### Option B: Evaluate by trace IDs

For more control, collect specific trace IDs from Application Insights and evaluate them. This is useful when you want to evaluate a curated set of interactions (for example, traces flagged by alerts or sampled for quality review).

#### Collect trace IDs from Application Insights

Query Application Insights for `operation_Id` values from your agent's traces. Each `operation_Id` represents a complete agent interaction:

```python
import os
from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus

appinsights_resource_id = os.environ["APPINSIGHTS_RESOURCE_ID"]
agent_id = os.environ["AGENT_ID"]
trace_query_hours = int(os.environ.get("TRACE_LOOKBACK_HOURS", "1"))

end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(hours=trace_query_hours)

query = f"""dependencies
| where timestamp between (datetime({start_time.isoformat()}) .. datetime({end_time.isoformat()}))
| extend agent_id = tostring(customDimensions["gen_ai.agent.id"])
| where agent_id == "{agent_id}"
| distinct operation_Id"""

credential = DefaultAzureCredential()
logs_client = LogsQueryClient(credential)
response = logs_client.query_resource(
    appinsights_resource_id,
    query=query,
    timespan=None,  # Time range is specified in the query itself
)

trace_ids = []
if response.status == LogsQueryStatus.SUCCESS:
    for table in response.tables:
        for row in table.rows:
            trace_ids.append(row[0])

print(f"Found {len(trace_ids)} trace IDs")
```

#### Create evaluation and run with trace IDs

```python
# Create the evaluation
data_source_config = {
    "type": "azure_ai_source",
    "scenario": "traces",
}

eval_object = client.evals.create(
    name="Agent Trace Evaluation (by trace IDs)",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,  # See "Set up evaluators" below
)

# Create a run using the collected trace IDs
data_source = {
    "type": "azure_ai_traces",
    "trace_ids": trace_ids,
    "lookback_hours": trace_query_hours,
}

eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="agent-trace-eval-run",
    metadata={
        "agent_id": agent_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    },
    data_source=data_source,
)

print(f"Evaluation run started: {eval_run.id}")
```

### Set up evaluators and data mappings

When evaluating traces, the service automatically extracts conversation data from the OpenTelemetry span attributes. Use these field names directly in `data_mapping` (without the `item.` or `sample.` prefixes used in other scenarios):

| Variable | Source attribute | Description |
|----------|----------------|-------------|
| `{{item.query}}` | `gen_ai.input.messages` (user/system roles) | The user query extracted from the trace. |
| `{{item.response}}` | `gen_ai.input.messages` (assistant/tool roles) + `gen_ai.output.messages` | The agent's response extracted from the trace. |
| `{{item.tool_definitions}}` | `gen_ai.tool.definitions` | Tool schemas available to the agent. Only required for tool-related evaluators |
| `{{item.tool_calls}}` | Extracted from assistant messages in `gen_ai.input.messages` / `gen_ai.output.messages` | Tool calls made by the agent during the interaction. Used by tool evaluators. Only required for tool-related evaluators |

```python
testing_criteria = [
    # Quality evaluators — require query and response from trace data
    {
        "type": "azure_ai_evaluator",
        "name": "intent_resolution",
        "evaluator_name": "builtin.intent_resolution",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
            "tool_definitions": "{{item.tool_definitions}}",
        },
        "initialization_parameters": {
            "model": model_deployment_name,
        },
    },
    # Tool evaluators — assess tool usage quality
    {
        "type": "azure_ai_evaluator",
        "name": "tool_call_accuracy",
        "evaluator_name": "builtin.tool_call_accuracy",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
            "tool_calls": "{{item.tool_calls}}",
            "tool_definitions": "{{item.tool_definitions}}",
        },
        "initialization_parameters": {
            "model": model_deployment_name,
        },
    },
    # Safety evaluators — work even with partial trace data
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
        "initialization_parameters": {
            "threshold": 4,
        },
    },
]
```

For a complete runnable example, see [sample_evaluations_builtin_with_traces.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_builtin_with_traces.py) on GitHub. To poll for completion and interpret results, see [Get results](#get-results).

## Synthetic data evaluation (preview)

Generate synthetic test queries, send them to a deployed model or Foundry agent, and evaluate the responses using the `azure_ai_synthetic_data_gen_preview` data source type. Use this scenario when you don't have a test dataset — the service generates queries based on a prompt you provide (and/or from the agent's instructions), runs them against your target, and evaluates the responses.

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
| `samples_count` | Yes | Maximum number of synthetic test queries to generate. |
| `model_deployment_name` | Yes | Model deployment to use for generating synthetic queries. Only models with Responses API capability are supported. For availability, see [Responses API region availability](https://aka.ms/aoai/responsesapi/availability). |
| `prompt` | No | Instructions describing the type of queries to generate. Optional when the agent target has instructions configured. |
| `output_dataset_name` | No | Name for the output dataset where generated queries are stored. If not provided, the service generates a name automatically. |
| `sources` | No | Seed data files (by file ID) to improve relevance of generated queries. Currently only one file is supported. |

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
            "model": model_deployment_name,
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

To poll for completion and interpret results, see [Get results](#get-results). The response includes an `output_dataset_id` property that contains the ID of the generated dataset, which you can use to retrieve or reuse the synthetic data.

## Multiturn conversation evaluation

Evaluate complete multi-turn conversations to assess agent quality across entire user interactions—not just individual responses. Use multiturn evaluation to identify conversation-level quality issues like incomplete task resolution, user frustration, and tool-call regressions that single-turn evaluation misses.

For example, consider a support agent where the user grows frustrated over multiple turns:

> **Turn 1** — User: "I need to reset my password." Agent: "I found your account. I'll send a reset link."
>
> **Turn 2** — User: "I didn't get the email." Agent: "I've resent the link. Please check spam."
>
> **Turn 3** — User: "Still nothing. Can you just reset it directly?" Agent: "I've sent another reset link."

A single-turn evaluator scores only the last response—which is polite and takes action—so it scores well. A multiturn evaluator grading **customer satisfaction** across the conversation flags that the agent repeated the same failing action three times without trying an alternative, leaving the user's problem unresolved.

Multiturn evaluation differs from single-turn evaluation in several ways:

| Aspect | Single-turn | Multiturn |
|--------|------------|----------|
| **Scope** | Individual query-response pairs | Complete conversations with multiple exchanges |
| **Metrics** | Per-response quality and safety | Conversation-level outcomes and user satisfaction |
| **Data format** | JSONL with `query` and `response` fields | JSONL with `messages` array containing the full conversation |
| **Use case** | Testing individual model responses | Testing end-to-end agent experiences |

Multiturn evaluation supports four data source options:

| Option | When to use | Data source type |
|--------|-------------|------------------|
| [From dataset or inline](#prepare-conversation-data) | You have local conversation traces or test data | `jsonl` with `file_id` or `file_content` |
| [By conversation ID](#evaluate-conversations-by-id-from-traces) | You want to evaluate specific conversations from App Insights | `azure_ai_trace_data_source_preview` with `trace_source` |
| [By agent filter with sampling](#evaluate-sampled-conversations-by-agent-filter) | You want to assess overall agent quality across sampled production traffic | `azure_ai_trace_data_source_preview` with `trace_source` |
| [Simulated conversations](#conversation-simulation) | You want to generate synthetic test conversations | `simulator` with target configuration |

### Choose an evaluation level

The `evaluation_level` parameter on the run determines whether evaluators score individual turns or complete conversations:

| Value | Behavior |
|-------|----------|
| `"turn"` | Evaluators score each turn independently. |
| `"conversation"` | Evaluators score the entire conversation as a whole. |
| (omitted) | Defaults to `"turn"`. |

> [!IMPORTANT]
> **Evaluator compatibility**: Each evaluator supports specific evaluation levels. Check the evaluator's `supported_evaluation_levels` field in the [evaluator catalog](../evaluate-generative-ai-app.md).
>
> - **Turn-only evaluators** (for example, `fluency`, `relevance`) can't be used with `evaluation_level="conversation"`.
> - Currently, all multiturn evaluators support both `"turn"` and `"conversation"` levels.

#### Common errors

| Error | Cause | Solution |
|-------|-------|----------|
| Incompatible evaluation level | Using `evaluation_level="conversation"` with a turn-only evaluator | Remove the turn-only evaluator or change to `evaluation_level="turn"` |

### Prepare conversation data

Create a JSONL file where each line contains a complete conversation in the `messages` field. Each message should include a `role` (user, assistant, or system) and `content`:

```json
 {"messages": [{"role": "user", "content": "What's my account balance?"}, {"role": "assistant", "content": "Your current balance is $1,234.56."}, {"role": "user", "content": "Thanks!"}, {"role": "assistant", "content": "You're welcome! Is there anything else?"}]}
```

You can also include tool definitions and tool calls if your agent uses tools:

```json
{"messages": [{"role": "user", "content": "What is the capital of France?"}, {"role": "assistant", "content": "Paris"}]}
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

### Define the data schema and evaluators

Specify the schema for your conversation data, "messages", and select evaluators designed for multi-turn conversations. Conversation-level evaluators assess the entire interaction rather than individual turns.

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

### Create evaluation and run

# [Python](#tab/python)

```python
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileID,
)

# Upload conversation data
data_id = project_client.datasets.upload_file(
    name="multiturn-conversation-data",
    version="1",
    file_path="./conversations.jsonl",
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

To poll for completion and interpret results, see [Get results](#get-results).

### Evaluate conversations by ID from traces

Evaluate specific conversations from Application Insights by providing their conversation IDs. Use this option to root-cause issues or verify fixes on specific interactions—for example, investigating a conversation flagged by an alert or verifying a fix for a known issue.

#### Where to find conversation IDs

You can find conversation IDs in:

- **Application Insights trace logs UI** — Browse to interesting traces and locate the `conversation_id` field in the trace details.
- **Your application's logging output** — If you set `conversation_id` explicitly when creating agent responses, retrieve it from your logs.
- **OpenTelemetry trace context** — The `conversation_id` may also be derived from the [traceparent](https://www.w3.org/TR/trace-context/#traceparent-header) header if your agent uses standard trace context propagation.

> [!NOTE]
> Tool definitions are automatically retrieved from the traces or queried from the agent registry—you don't need to provide them in the request.

#### Parameters for conversation ID lookup

| Parameter | Required | Description |
|-----------|----------|-------------|
| `conversation_ids` | Yes | Array of conversation IDs to evaluate. |
| `lookback_hours` | No | Hours to search back from `end_time`. Defaults to 7 days (168 hours). |
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
> - There may be a delay between when traces are generated and when they become available for evaluation due to Application Insights data ingestion. If traces aren't found, wait a few minutes and retry.
> - The maximum lookback is **7 days (168 hours)**. To access older traces, use `start_time` and `end_time` within your App Insights retention limits.

### Evaluate sampled conversations by agent filter

Evaluate a sampled set of conversations from Application Insights by filtering on agent name. Use this option to assess overall agent quality across production traffic—for example, running regular quality assessments or monitoring for quality degradation in production.

The agent you specify for filtering can be part of a multi-agent conversation. The filter matches any conversation where that agent participated.

> [!NOTE]
> Tool definitions are automatically retrieved from the traces or queried from the agent registry—you don't need to provide them in the request.

#### Agent identity fields

Specify the agent to filter by using one of these formats:

| Format | Example | Description |
|--------|---------|-------------|
| `agent_name` + `agent_version` | `"agent_name": "my-agent", "agent_version": "1"` | Two separate fields. If `agent_version` is omitted, uses the latest version. |
| `agent_id` | `"agent_id": "my-agent:1"` | Single string in `"name:version"` format. |

#### Filter strategies

| Strategy | Description |
|----------|-------------|
| `random_sampling` | (Default) Uniformly random sample up to `max_traces` conversations. |
| `smart_filtering` | Service-managed heuristic that biases toward "interesting" traces—conversations with potential issues, edge cases, or anomalies. |

#### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `agent_name` | Yes | The agent name to filter traces by. |
| `agent_version` | No | The agent version. If omitted, uses the latest version. |
| `agent_id` | No | Alternative to `agent_name` + `agent_version`. Single string in format `"name:version"`. |
| `start_time` | Yes | Start of the time window (Unix epoch seconds, UTC). |
| `end_time` | Yes | End of the time window (Unix epoch seconds, UTC). Pad by +600 seconds to avoid ingestion delay. |
| `max_traces` | No | Maximum conversations to sample. Defaults to 1000. |
| `filter_strategy` | No | `"random_sampling"` (default) or `"smart_filtering"` (service-managed heuristic that biases toward interesting traces). |

> [!IMPORTANT]
> The time window (`end_time - start_time`) must be at least **15 minutes** (900 seconds). This is required because conversation-level queries apply a 5-minute inactivity buffer on each edge to avoid partial conversations.

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
> The App Insights query timespan is currently limited to a maximum of **7 days (168 hours)**. Traces older than 7 days aren't reachable without explicitly providing `start_time`/`end_time` within App Insights retention limits.

To poll for completion and interpret results, see [Get results](#get-results).

## Conversation simulation

Generate simulated multi-turn conversations from scenario descriptions and evaluate them. Use this scenario to test your agent's behavior in controlled scenarios before deployment—the service generates realistic conversations based on your scenario descriptions and then evaluates them.

This approach is useful for:

- **Pre-deployment testing**: Validate agent behavior across diverse scenarios without real user traffic.
- **Edge case coverage**: Test scenarios that rarely occur naturally but are important to handle well.
- **Regression testing**: Ensure agent updates don't degrade performance on known scenarios.
- **Scale testing**: Generate many conversations quickly to stress-test agent capabilities.

### How conversation simulation works

1. You provide a dataset of scenario descriptions—each row describes a situation the simulated user will try to accomplish.
2. The service uses a simulator model to play the role of the user, interacting with your agent based on the scenario.
3. Each scenario generates one or more complete conversations.
4. The generated conversations are evaluated using conversation-level evaluators.
5. Both the conversations and evaluation results are stored in your project.

### Prepare scenario data

Create a JSONL file where each line describes a scenario for the simulated user. Schema requires: id, test_case_description, and desired_num_turns. Include details about the user's goal, context, and any constraints:

```json

{"id": "walmart_refund_timeline", "test_case_description": "Customer returned an item to Walmart 5 days ago and hasn't received their refund yet. They want to know how long Walmart refunds take.", "desired_num_turns": 10}
{"id": "walmart_store_hours_lookup", "test_case_description": "Customer wants to know what time the Walmart store closes today. Simple single-fact question with possibly one clarifying turn about which location.", "desired_num_turns": 3}
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `num_conversations` | No | Number of conversations to generate per scenario. Defaults to 5, server-side cap of 5. |
| `max_turns` | No | Maximum number of turns (exchanges) per conversation. Defaults to 10, server-side cap of 20. |
| `model` | Yes | Model deployment to use for simulating the user. For example, `gpt-4.1`. |
| `sampling_params` | No | Sampling parameters for the simulator model, including `temperature`, `top_p`, and `max_completion_tokens`. |
| `data_mapping` | No | Maps fields from your scenario JSONL to simulation parameters. Common mappings: `test_case_description`, `id`, `desired_num_turns`. |

### Define evaluators

Select evaluators designed for conversation-level assessment. The simulated conversations are automatically mapped to the evaluators.

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
    file_path="./scenarios.jsonl",
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

To poll for completion and interpret results, see [Get results](#get-results).

## Get results

After an evaluation run completes, retrieve the scored results and review them in the portal or programmatically.

### Poll for results

Evaluation runs are asynchronous. Poll the run status until it completes, then retrieve the results:

```python
import time
from print import print

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
- Your account has the **Foundry User** role on the Foundry project.
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
- [Trace-based evaluation sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_builtin_with_traces.py)
- [Set up tracing in Microsoft Foundry](../../observability/how-to/trace-agent-setup.md)
- [Set up continuous evaluation](../../observability/how-to/how-to-monitor-agents-dashboard.md#set-up-continuous-evaluation)
- [See evaluation results in the Foundry portal](../../how-to/evaluate-results.md)
- [Get started with Foundry](../../quickstarts/get-started-code.md)
- [REST API reference](../../reference/foundry-project-rest-preview.md#openai-evals---list-evals)
