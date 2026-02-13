---
title: Cloud Evaluation with the Microsoft Foundry SDK
titleSuffix: Microsoft Foundry
description: Run scalable evaluations for generative AI applications using the Microsoft Foundry SDK. Learn how to integrate evaluations into your development pipeline.
ms.service: azure-ai-foundry
ms.custom:
  - references_regions
  - ignite-2024
ms.topic: how-to
ms.date: 11/18/2025
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
# customer intent: As a developer, I want to run evaluations in the cloud using the Microsoft Foundry SDK so I can test my generative AI application on large datasets without managing local compute infrastructure.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Run evaluations in the cloud by using the Microsoft Foundry SDK

[!INCLUDE [version-banner](../../includes/version-banner.md)]

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

::: moniker range="foundry-classic"

In this article, you learn how to run evaluations in the cloud (preview) for predeployment testing on a test dataset. The Azure AI Evaluation SDK lets you run evaluations locally on your machine and in the cloud. For example, run local evaluations on small test data to assess your generative AI application prototypes, and then move into predeployment testing to run evaluations on a large dataset.

Use cloud evaluations for most scenarios—especially when testing at scale, integrating evaluations into continuous integration and continuous delivery (CI/CD) pipelines, or performing predeployment testing. Running evaluations in the cloud eliminates the need to manage local compute infrastructure and supports large scale, automated testing workflows. After deployment, you can choose to [continuously evaluate](../continuous-evaluation-agents.md) your agents for post-deployment monitoring.

When you use the Foundry SDK, it logs evaluation results in your Foundry project for better observability. This feature supports all Microsoft-curated [built-in evaluators](../../concepts/observability.md#what-are-evaluators) and your own [custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md). Your evaluators can be located in the [evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library) and have the same project-scope, role-based access control.

::: moniker-end

::: moniker range="foundry"

In this article, you learn how to run evaluations in the cloud (preview) for predeployment testing on a test dataset. 

Use cloud evaluations for most scenarios—especially when testing at scale, integrating evaluations into continuous integration and continuous delivery (CI/CD) pipelines, or performing predeployment testing. Running evaluations in the cloud eliminates the need to manage local compute infrastructure and supports large scale, automated testing workflows. After deployment, you can choose to [continuously evaluate](../../default/observability/how-to/how-to-monitor-agents-dashboard.md#set-up-continuous-evaluation-python-sdk) your agents for post-deployment monitoring.

When you use the Foundry SDK, it logs evaluation results in your Foundry project for better observability. This feature supports all Microsoft-curated [built-in evaluators](../../concepts/observability.md#what-are-evaluators) and your own [custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md). Your evaluators can be located in the [evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library) and have the same project-scope, role-based access control.

> [!TIP]
> For complete runnable examples, see the [Python SDK evaluation samples](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/README.md) on GitHub.

::: moniker-end


## Prerequisites

- A [Foundry project](../create-projects.md).
- An Azure OpenAI deployment with a GPT model that supports chat completion (for example, `gpt-4` or `gpt-5-chat`).

> [!NOTE]
> Some evaluation features have regional restrictions. See [supported regions](../../concepts/evaluation-evaluators/risk-safety-evaluators.md#foundry-project-configuration-and-region-support) for details.

::: moniker range="foundry-classic"

[!INCLUDE [evaluation-foundry-project-storage](../../includes/evaluation-foundry-project-storage.md)]

::: moniker-end

::: moniker range="foundry"

## Data source types

The evaluation API supports different data source types depending on your scenario:

| Scenario | When to use | Data Source Type | Target |
|----------|-------------|------------------|--------|
| **[Dataset evaluation](#dataset-evaluation)** | Evaluate pre-computed responses in a JSONL file. | `jsonl` | — |
| **[Model target evaluation](#model-target-evaluation)** | Generate and evaluate responses from a model at runtime. Input contains queries; model generates responses. | `azure_ai_target_completions` | `azure_ai_model` |
| **[Agent target evaluation](#agent-target-evaluation)** | Generate and evaluate responses from a Foundry agent at runtime. Input contains queries; agent generates responses. | `azure_ai_target_completions` | `azure_ai_agent` |
| **[Agent response evaluation](#agent-response-evaluation)** | Retrieve and evaluate Foundry agent responses by response IDs. | `azure_ai_responses` | — |
| **Model red team evaluation** | Run automated adversarial testing against a model. | `azure_ai_red_team` | `azure_ai_model` |
| **Agent red team evaluation** | Run automated adversarial testing against a Foundry agent. | `azure_ai_red_team` | `azure_ai_agent` |

> [!NOTE]
> For red team evaluation details, see [Run AI red teaming evaluations](run-ai-red-teaming-cloud.md).

### Source options

Most scenarios require input data. You can provide input data in two ways:

| Source Type | Description | Supported By |
|-------------|-------------|--------------|
| `file_id` | Reference an uploaded dataset by ID | `jsonl`, `azure_ai_target_completions`, `azure_ai_responses` |
| `file_content` | Provide data inline in the request | `jsonl`, `azure_ai_target_completions` |

::: moniker-end

## Get started

::: moniker range="foundry-classic"

1. Install the Microsoft Foundry SDK project client to run evaluations in the cloud:

   ```bash
   pip install azure-ai-projects azure-identity
   ```

1. Set environment variables for your Foundry resources:

   ```python
   import os

   # Required environment variables:
   endpoint = os.environ["PROJECT_ENDPOINT"] # https://<account>.services.ai.azure.com/api/projects/<project>
   model_endpoint = os.environ["MODEL_ENDPOINT"] # https://<account>.services.ai.azure.com
   model_api_key = os.environ["MODEL_API_KEY"]
   model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"] # E.g. gpt-4o-mini

   # Optional: Reuse an existing dataset.
   dataset_name    = os.environ.get("DATASET_NAME",    "dataset-test")
   dataset_version = os.environ.get("DATASET_VERSION", "1.0")
   ```

1. Define a client to run evaluations in the cloud:

   ```python
   import os
   from azure.identity import DefaultAzureCredential
   from azure.ai.projects import AIProjectClient

   # Create the project client (Foundry project and credentials):
   project_client = AIProjectClient(
       endpoint=endpoint,
       credential=DefaultAzureCredential(),
   )
   ```

::: moniker-end

::: moniker range="foundry"

Install the SDK and set up your client:

```bash
pip install azure-ai-projects azure-identity 
```

```python
import os
from azure.identity import DefaultAzureCredential 
from azure.ai.projects import AIProjectClient 

# Azure AI Project endpoint
# Example: https://<account_name>.services.ai.azure.com/api/projects/<project_name>
endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

# Model deployment name (for AI-assisted evaluators)
# Example: gpt-4o-mini
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

::: moniker-end

## <a name = "uploading-evaluation-data"></a> Upload evaluation data

::: moniker range="foundry"

Upload your JSONL file to create a dataset. The file is stored in your Foundry project and can be reused across multiple evaluation runs.

Your JSONL file should contain one JSON object per line with the fields your evaluators need:

```json
{"query": "What is machine learning?", "response": "Machine learning is a subset of AI.", "ground_truth": "Machine learning is a type of AI that learns from data."}
{"query": "Explain neural networks.", "response": "Neural networks are computing systems inspired by biological neural networks.", "ground_truth": "Neural networks are a set of algorithms modeled after the human brain."}
```

::: moniker-end

```python
# Upload a local JSONL file. Skip this step if you already have a dataset registered.
data_id = project_client.datasets.upload_file(
    name=dataset_name,
    version=dataset_version,
    file_path="./evaluate_test_data.jsonl",
).id
```

::: moniker range="foundry-classic"

To learn more about input data formats for evaluating generative AI applications, see:

- [Single-turn data](./evaluate-sdk.md#single-turn-support-for-text)
- [Conversation data](./evaluate-sdk.md#conversation-support-for-text)
- [Conversation data for images and multi-modalities](./evaluate-sdk.md#conversation-support-for-images-and-multimodal-text-and-image)

To learn more about input data formats for evaluating agents, see [Evaluate Azure AI agents](./agent-evaluate-sdk.md#evaluate-microsoft-foundry-agents) and [Evaluate other agents](./agent-evaluate-sdk.md#evaluating-other-agents).

::: moniker-end

::: moniker range="foundry"

To learn more about input data formats for evaluating agents, see [Evaluate Azure AI agents](../../default/observability/how-to/evaluate-agent.md).

::: moniker-end

::: moniker range="foundry-classic"

## Specify evaluators

```python
from azure.ai.projects.models import (
    EvaluatorConfiguration,
    EvaluatorIds,
)

# Built-in evaluator configurations:
evaluators = {
    "relevance": EvaluatorConfiguration(
        id=EvaluatorIds.RELEVANCE.value,
        init_params={"deployment_name": model_deployment_name},
        data_mapping={
            "query": "${data.query}",
            "response": "${data.response}",
        },
    ),
    "violence": EvaluatorConfiguration(
        id=EvaluatorIds.VIOLENCE.value,
        init_params={"azure_ai_project": endpoint},
    ),
    "bleu_score": EvaluatorConfiguration(
        id=EvaluatorIds.BLEU_SCORE.value,
    ),
}
```

::: moniker-end

::: moniker range="foundry-classic"

## Create an evaluation

Finally, submit the remote evaluation run:

```python
from azure.ai.projects.models import (
    Evaluation,
    InputDataset
)

# Create an evaluation with the dataset and evaluators specified.
evaluation = Evaluation(
    display_name="Cloud evaluation",
    description="Evaluation of dataset",
    data=InputDataset(id=data_id),
    evaluators=evaluators,
)

# Run the evaluation.
evaluation_response = project_client.evaluations.create(
    evaluation,
    headers={
        "model-endpoint": model_endpoint,
        "api-key": model_api_key,
    },
)

print("Created evaluation:", evaluation_response.name)
print("Status:", evaluation_response.status)
```

## Specify custom evaluators

> [!NOTE]
> Foundry projects aren't supported for this feature. Use a Foundry hub project instead.

### Code-based custom evaluators

Register your custom evaluators to your Azure AI Hub project and fetch the evaluator IDs:

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model
from promptflow.client import PFClient

# Define ml_client to register the custom evaluator.
ml_client = MLClient(
       subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
       resource_group_name=os.environ["AZURE_RESOURCE_GROUP"],
       workspace_name=os.environ["AZURE_PROJECT_NAME"],
       credential=DefaultAzureCredential()
)

# Load the evaluator from the module.
from answer_len.answer_length import AnswerLengthEvaluator

# Convert it to an evaluation flow, and save it locally.
pf_client = PFClient()
local_path = "answer_len_local"
pf_client.flows.save(entry=AnswerLengthEvaluator, path=local_path)

# Specify the evaluator name that appears in the Evaluator library.
evaluator_name = "AnswerLenEvaluator"

# Register the evaluator to the Evaluator library.
custom_evaluator = Model(
    path=local_path,
    name=evaluator_name,
    description="Evaluator calculating answer length.",
)
registered_evaluator = ml_client.evaluators.create_or_update(custom_evaluator)
print("Registered evaluator id:", registered_evaluator.id)
# Registered evaluators have versioning. You can always reference any version available.
versioned_evaluator = ml_client.evaluators.get(evaluator_name, version=1)
print("Versioned evaluator id:", registered_evaluator.id)
```

After you register your custom evaluator, view it in your [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library). In your Foundry project, select **Evaluation**, then select **Evaluator library**.


### Prompt-based custom evaluators

Use this example to register a custom `FriendlinessEvaluator` built as described in [Prompt-based evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md#prompt-based-evaluators):

```python
# Import your prompt-based custom evaluator.
from friendliness.friend import FriendlinessEvaluator

# Define your deployment.
model_config = dict(
    azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_API_VERSION"),
    api_key=os.environ.get("AZURE_API_KEY"), 
    type="azure_openai"
)

# Define ml_client to register the custom evaluator.
ml_client = MLClient(
       subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
       resource_group_name=os.environ["AZURE_RESOURCE_GROUP"],
       workspace_name=os.environ["AZURE_PROJECT_NAME"],
       credential=DefaultAzureCredential()
)

# # Convert the evaluator to evaluation flow and save it locally.
local_path = "friendliness_local"
pf_client = PFClient()
pf_client.flows.save(entry=FriendlinessEvaluator, path=local_path) 

# Specify the evaluator name that appears in the Evaluator library.
evaluator_name = "FriendlinessEvaluator"

# Register the evaluator to the Evaluator library.
custom_evaluator = Model(
    path=local_path,
    name=evaluator_name,
    description="prompt-based evaluator measuring response friendliness.",
)
registered_evaluator = ml_client.evaluators.create_or_update(custom_evaluator)
print("Registered evaluator id:", registered_evaluator.id)
# Registered evaluators have versioning. You can always reference any version available.
versioned_evaluator = ml_client.evaluators.get(evaluator_name, version=1)
print("Versioned evaluator id:", registered_evaluator.id)
```

After you register your custom evaluator, you can view it in your [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library). In your Foundry project, select **Evaluation**, then select **Evaluator library**.

::: moniker-end

::: moniker range="foundry"

## Dataset evaluation

Evaluate pre-computed responses in a JSONL file using the `jsonl` data source type. This scenario is useful when you already have model outputs and want to assess their quality.

> [!TIP]
> Before you begin, complete [Get started](#get-started) and [Upload evaluation data](#uploading-evaluation-data) to set up your client and dataset.

### Define the data schema and evaluators

Specify the schema that matches your JSONL fields, and select the evaluators (testing criteria) to run. Use the `data_mapping` parameter to connect fields from your input data to evaluator parameters with `{{item.field}}` syntax. Your field names must match those in your JSONL file — for example, if your data has `"question"` instead of `"query"`, use `"{{item.question}}"` in the mapping.

# [Python](#tab/python)

```python
data_source_config = {
    "type": "custom",
    "item_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "response": {"type": "string"},
            "ground_truth": {"type": "string"},
        },
        "required": [],
    },
    "include_sample_schema": True,
}

testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
            "deployment_name": model_deployment_name
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
        "initialization_parameters": {
            "deployment_name": model_deployment_name
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "f1",
        "evaluator_name": "builtin.f1_score",
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
        "required": []
      },
      "include_sample_schema": true
    },
    "testing_criteria": [
      {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": {
          "deployment_name": "gpt-4o-mini"
        }
      },
      {
        "type": "azure_ai_evaluator",
        "name": "violence",
        "evaluator_name": "builtin.violence",
        "data_mapping": {
          "query": "{{item.query}}",
          "response": "{{item.response}}"
        },
        "initialization_parameters": {
          "deployment_name": "gpt-4o-mini"
        }
      }
    ]
  }'
```

---

### Create the evaluation and run it

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
            id=dataset.id if dataset.id else "",
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
        "required": []
      },
      "include_sample_schema": true
    },
    "testing_criteria": [
      {
        "type": "azure_ai_evaluator",
        "name": "coherence",
        "evaluator_name": "builtin.coherence",
        "initialization_parameters": { "deployment_name": "gpt-4o-mini" }
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

### Poll for results

Evaluation runs are asynchronous. Poll the run status until it completes, then retrieve the results:

```python
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

For a complete runnable example, see [sample_evaluations_builtin_with_dataset_id.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_evaluations_builtin_with_dataset_id.py) on GitHub.

## Agent target evaluation

Send queries to a Foundry agent at runtime and evaluate the responses using the `azure_ai_target_completions` data source type with an `azure_ai_agent` target.

> [!TIP]
> Before you begin, complete [Get started](#get-started). For polling and retrieving results, see [Poll for results](#poll-for-results).

### Define inline test data

Provide test cases inline using `file_content`. Each item contains the fields your evaluators need:

```python
source = {
    "type": "file_content",
    "content": [
        {
            "item": {
                "query": "How can I safely de-escalate a tense situation?",
                "ground_truth": "Encourage calm communication, seek help if needed, and avoid harm.",
            }
        },
        {
            "item": {
                "query": "What is the largest city in France?",
                "ground_truth": "Paris",
            }
        }
    ]
}
```

> [!NOTE]
> You can also use `file_id` to reference an uploaded dataset instead of inline data. See [Source options](#source-options).

### Define the message template

The `input_messages` template controls how queries are sent to the agent. Use `{{item.query}}` to reference fields from your test data:

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
```

### Define the agent target

Specify the Foundry agent to evaluate by name and version:

```python
target = {
    "type": "azure_ai_agent",
    "name": "my-agent",
    "version": "1.0"
}
```

### Create the evaluation run

Combine the data source components and create the run:

# [Python](#tab/python)

```python
data_source = {
    "type": "azure_ai_target_completions",
    "source": source,
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
        "type": "file_content",
        "content": [
          {
            "item": {
              "query": "How can I safely de-escalate a tense situation?",
              "ground_truth": "Encourage calm communication and avoid harm."
            }
          },
          {
            "item": {
              "query": "What is the largest city in France?",
              "ground_truth": "Paris"
            }
          }
        ]
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
        "version": "1.0"
      }
    }
  }'
```

---

For a complete runnable example, see [sample_agent_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_agent_evaluation.py) on GitHub.

## Agent response evaluation

Retrieve and evaluate Foundry agent responses by response IDs using the `azure_ai_responses` data source type. Use this scenario to evaluate specific agent interactions after they occur.

> [!TIP]
> Before you begin, complete [Get started](#get-started) and [Upload evaluation data](#uploading-evaluation-data). Your dataset should contain response IDs from previous agent interactions. For polling and retrieving results, see [Poll for results](#poll-for-results).

# [Python](#tab/python) 

```python
data_source = {
    "type": "azure_ai_responses",
    "source": {
        "type": "file_id",
        "id": dataset.id  # Dataset containing response IDs to evaluate
    }
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
      "source": {
        "type": "file_id",
        "id": "YOUR_DATASET_ID"
      }
    }
  }'
```

---

For a complete runnable example, see [sample_agent_response_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_agent_response_evaluation.py) on GitHub.

## Model target evaluation

Send queries to a deployed model at runtime and evaluate the responses using the `completions` data source type. Your input data contains queries; the model generates responses which are then evaluated.

> [!TIP]
> Before you begin, complete [Get started](#get-started) and [Upload evaluation data](#uploading-evaluation-data). For polling and retrieving results, see [Poll for results](#poll-for-results).

### Define the data source and model

Specify the uploaded dataset, message template, target model, and sampling parameters:

```python
data_source = {
    "type": "completions",
    "source": {
        "type": "file_id",
        "id": dataset.id,
    },
    "input_messages": {
        "type": "template",
        "template": [
            {
                "type": "message",
                "role": "developer",
                "content": {
                    "type": "input_text",
                    "text": "You are a helpful assistant. Answer the user's question accurately and concisely.",
                },
            },
            {
                "type": "message",
                "role": "user",
                "content": {
                    "type": "input_text",
                    "text": "{{item.query}}",
                },
            },
        ],
    },
    "model": "gpt-4o-mini",
    "sampling_params": {
        "seed": 42,
        "temperature": 1.0,
        "top_p": 1.0,
        "max_completion_tokens": 2048,
    },
}
```

### Create the evaluation run

# [Python](#tab/python)

```python
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
      "type": "completions",
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
              "text": "You are a helpful assistant. Answer the user question accurately and concisely."
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
      "model": "gpt-4o-mini",
      "sampling_params": {
        "seed": 42,
        "temperature": 1.0,
        "top_p": 1.0,
        "max_completion_tokens": 2048
      }
    }
  }'
```

---

For a complete runnable example, see [sample_model_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_model_evaluation.py) on GitHub.

## Interpretation of results

::: moniker range="foundry"

For a single data example, all evaluators always output the following schema:  

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

For aggregate results over multiple data examples (a dataset), the average rate of the examples with a "pass" will form the passing rate for that dataset.

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

::: moniker-end

## Troubleshooting

::: moniker range="foundry"

### Job stuck in running state

Your evaluation job might remain in the **Running** state for an extended period. This typically occurs when the Azure OpenAI model you select doesn't have enough capacity.

**Resolution:**

1. Cancel the current evaluation job using `client.evals.runs.cancel(eval_id=eval_id, run_id=run_id)`.
1. Increase the model capacity in the Azure portal.
1. Run the evaluation again.

For more information on monitoring evaluation jobs, see [View evaluation results](../../how-to/evaluate-results.md).

::: moniker-end

## Related content

::: moniker range="foundry-classic"

- [Evaluate your generative AI applications locally](./evaluate-sdk.md)
- [Monitor your generative AI applications](../monitor-applications.md)
- [Learn about simulating test datasets for evaluation](./simulator-interaction-data.md)
- [See evaluation results in the Foundry portal](../../how-to/evaluate-results.md)
- [Get started with Foundry](../../quickstarts/get-started-code.md)
- [Get started with evaluation samples](https://aka.ms/aistudio/eval-samples)
- [REST API Reference Documentation](/rest/api/aifoundry/aiprojects/evaluations)

::: moniker-end

::: moniker range="foundry"

- [Complete working samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations)
- [Evaluate your AI agents continuously](../continuous-evaluation-agents.md)
- [See evaluation results in the Foundry portal](../../how-to/evaluate-results.md)
- [Get started with Foundry](../../quickstarts/get-started-code.md)
- [REST API reference](../../reference/foundry-project-rest-preview.md#openai-evals---list-evals)

::: moniker-end
