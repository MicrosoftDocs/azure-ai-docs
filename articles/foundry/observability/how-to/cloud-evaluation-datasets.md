---
title: "Evaluate datasets with the Microsoft Foundry SDK"
description: "Learn how to use the Microsoft Foundry SDK to evaluate JSONL and CSV datasets with uploaded or inline data, schemas, and evaluator mappings."
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
# customer intent: As a developer, I want to evaluate existing datasets in the cloud so that I can measure application quality across reusable test cases.
---

# Evaluate datasets in the cloud

Evaluate precomputed responses in JSONL or CSV data by defining a schema, mapping fields to evaluators, and starting a cloud evaluation run.

## Prerequisites

- Complete the [cloud evaluation prerequisites](cloud-evaluation.md#prerequisites) and [client setup](cloud-evaluation.md#set-up-the-sdk-client).
- A JSONL or CSV dataset with the fields required by your evaluators.

The examples use the SDK client configured in [Set up the SDK client](cloud-evaluation.md#set-up-the-sdk-client).

## Prepare input data

Most evaluation scenarios require input data. You can provide data in two ways:

> [!TIP]
> If you don't have a hand-curated dataset, you can bootstrap one. Use [Generate a synthetic evaluation dataset](../../observability/how-to/evaluation-dataset-synthetic.md) when you're prelaunch or have low traffic, or [Convert agent traces into evaluation datasets](../../observability/how-to/traces-to-dataset.md) to build a dataset from real production traffic.

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

For quick experimentation with small test sets—or for scenarios that require inline data, such as agent response evaluation—provide data directly in the evaluation request by using `file_content`. For agent response evaluations, `file_content` is the only supported source type.

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

Pass `source` as the `"source"` field in your data source configuration when creating a run. The following scenario sections use `file_id` by default.

### Source type support by scenario

Not all scenarios support both source types. The following matrix shows which source type each scenario supports.

| Scenario | `file_id` | `file_content` |
|----------|-----------|----------------|
| Dataset (`jsonl`) | Yes | Yes |
| CSV (`csv`) | Yes | Yes |
| Model or agent target | Yes | Yes |
| Agent response (`azure_ai_responses`) | No | Yes |
| Trace (`azure_ai_traces`) | N/A | N/A |
| Synthetic data (preview) | N/A | N/A |

## Evaluate a JSONL dataset

Evaluate precomputed responses in a JSONL file by using the `jsonl` data source type. This scenario is useful when you already have model outputs and want to assess their quality.

> [!TIP]
> Before you begin, complete [client setup](cloud-evaluation.md#set-up-the-sdk-client) and [Prepare input data](cloud-evaluation-datasets.md#prepare-input-data).

### Define the data schema and evaluators

Specify the schema that matches your JSONL fields, and select the evaluators (testing criteria) to run. Use the `data_mapping` parameter to connect fields from your input data to evaluator parameters by using `{{item.field}}` syntax. Always include `data_mapping` with the required input fields for each evaluator. Your field names must match those in your JSONL file. For example, if your data has `"question"` instead of `"query"`, use `"{{item.question}}"` in the mapping. For the required parameters per evaluator, see [built-in evaluators](../../concepts/observability.md#what-are-evaluators).

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
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="coherence",
        evaluator_name="builtin.coherence",
        initialization_parameters={"model": model_deployment_name},
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="violence",
        evaluator_name="builtin.violence",
        initialization_parameters={"model": model_deployment_name},
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="f1",
        evaluator_name="builtin.f1_score",
        data_mapping={
            "response": "{{item.response}}",
            "ground_truth": "{{item.ground_truth}}",
        },
    ),
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
      {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {"model": "gpt-5-mini"},
        "data_mapping": {
          "query": "{{item.query}}",
          "response": "{{item.response}}"
        }
      },
      {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "initialization_parameters": {"model": "gpt-5-mini"},
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
  }'
```

---

### Create evaluation and run

Create the evaluation, and then start a run against your uploaded dataset. The run executes each evaluator on every row in the dataset.

# [Python](#tab/python)

```python
# Create the evaluation
eval_object = openai_client.evals.create(
    name="dataset-evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

# Create a run using the uploaded dataset
eval_run = openai_client.evals.runs.create(
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

For a complete runnable example, see [sample_evaluations_builtin_with_dataset_id.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_builtin_with_dataset_id.py) on GitHub. To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).

## Evaluate a CSV dataset

Evaluate precomputed responses in a CSV file by using the `csv` data source type. This scenario works the same way as [dataset evaluation](#evaluate-a-jsonl-dataset) but accepts CSV files instead of JSONL. Use CSV when your data is already in spreadsheet or tabular format.

> [!TIP]
> Before you begin, complete [client setup](cloud-evaluation.md#set-up-the-sdk-client) and [Prepare input data](cloud-evaluation-datasets.md#prepare-input-data).

### Prepare a CSV file

Create a CSV file with column headers that match the fields your evaluators need. Each row represents one test case.

```csv
query,response,context,ground_truth
What is cloud computing?,Cloud computing delivers computing services over the internet.,Cloud computing is a technology for on-demand resource delivery.,Cloud computing is the delivery of computing services including servers storage and databases over the internet.
What is machine learning?,Machine learning is a subset of AI that learns from data.,Machine learning is a branch of artificial intelligence.,Machine learning is a type of AI that enables computers to learn from data without being explicitly programmed.
Explain neural networks.,Neural networks are computing systems inspired by biological neural networks.,Neural networks are used in deep learning.,Neural networks are a set of algorithms modeled after the human brain designed to recognize patterns.
```

### Upload and run

Upload the CSV file as a dataset. Then, create an evaluation by using the `csv` data source type. The schema definition and evaluator configuration are the same as for JSONL evaluations. The only difference is the `"type": "csv"` in the data source.

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
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="coherence",
        evaluator_name="builtin.coherence",
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
        initialization_parameters={"model": model_deployment_name},
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="violence",
        evaluator_name="builtin.violence",
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
        initialization_parameters={"model": model_deployment_name},
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="f1",
        evaluator_name="builtin.f1_score",
    ),
]

# Create the evaluation
eval_object = openai_client.evals.create(
    name="CSV evaluation with built-in evaluators",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

# Create a run using the CSV data source type
eval_run = openai_client.evals.runs.create(
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

## Next steps

- To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).
- For a complete runnable example, see [sample_evaluations_builtin_with_csv.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_builtin_with_csv.py) on GitHub.
