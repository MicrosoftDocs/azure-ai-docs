---
title: Cloud Evaluation with the Azure AI Foundry SDK
titleSuffix: Azure AI Foundry
description: The Azure AI Evaluation SDK supports running evaluations locally or in the cloud. Learn how to evaluate a generative AI application.
ms.service: azure-ai-foundry
ms.custom:
  - references_regions
  - ignite-2024
ms.topic: how-to
ms.date: 10/18/2025
ms.reviewer: changliu2
ms.author: lagayhar
author: lgayhardt
---

# Run evaluations in the cloud by using the Azure AI Foundry SDK (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this article, you learn how to run evaluations in the cloud (preview) in pre-deployment testing on a test dataset. The Azure AI Evaluation SDK supports running evaluations locally on your machine and in the cloud. For example, you can run local evaluations on small test data to assess your generative AI application prototypes. Then move into pre-deployment testing and run evaluations on a large dataset.

Evaluating your applications in the cloud frees you from managing your local compute infrastructure. You can also integrate evaluations as tests into your continuous integration and continuous delivery pipelines. After deployment, you can [continuously monitor](../monitor-applications.md) your applications for post-deployment monitoring.

When you use the Azure AI Projects SDK, it logs evaluation results in your Azure AI project for better observability. This feature supports all Microsoft-curated [built-in evaluators](../../concepts/observability.md#what-are-evaluators) and your own [custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md). Your evaluators can be located in the [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library) and have the same project-scope role-based access control.

## Prerequisites

- Azure AI Foundry project in the same supported [regions](../../concepts/evaluation-evaluators/risk-safety-evaluators.md#azure-ai-foundry-project-configuration-and-region-support) as risk and safety evaluators (preview). If you don't have a project, create one. See [Create a project for Azure AI Foundry](../create-projects.md?tabs=ai-studio).
- Azure OpenAI Deployment with GPT model supporting `chat completion`. For example, `gpt-4`.
- Make sure you're logged into your Azure subscription by running `az login`.

[!INCLUDE [evaluation-foundry-project-storage](../../includes/evaluation-foundry-project-storage.md)]

> [!NOTE]
> Virtual network configurations are currently not supported for cloud-based evaluations. Enable public network access for your Azure OpenAI resource.

## Get started

1. Install the Azure AI Foundry SDK project client that runs the evaluations in the cloud:

   ```python
   uv install azure-ai-projects azure-identity
   ```

   > [!NOTE]
   > For more information, see [REST API Reference Documentation](/rest/api/aifoundry/aiprojects/evaluations).

1. Set your environment variables for your Azure AI Foundry resources:

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

1. Define a client that runs your evaluations in the cloud:

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

## <a name = "uploading-evaluation-data"></a> Upload evaluation data

```python
# Upload a local JSONL file. Skip this step if you already have a dataset registered.
data_id = project_client.datasets.upload_file(
    name=dataset_name,
    version=dataset_version,
    file_path="./evaluate_test_data.jsonl",
).id
```

To learn more about input data formats for evaluating generative AI applications:

- [Single-turn data](./evaluate-sdk.md#single-turn-support-for-text)
- [Conversation data](./evaluate-sdk.md#conversation-support-for-text)
- [Conversation data for images and multi-modalities](./evaluate-sdk.md#conversation-support-for-images-and-multi-modal-text-and-image)

To learn more about input data formats for evaluating agents, see [Evaluate Azure AI agents](./agent-evaluate-sdk.md#evaluate-azure-ai-agents) and [Evaluate other agents](./agent-evaluate-sdk.md#evaluating-other-agents).

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

## Submit an evaluation in the cloud

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
> Azure AI Foundry projects aren't supported for this feature. Use an Azure AI Foundry hub project instead.

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

After you register your custom evaluator, you can view it in your [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library). In your Azure AI Foundry project, select **Evaluation**, then select **Evaluator library**.

### Prompt-based custom evaluators

Follow this example to register a custom `FriendlinessEvaluator` built as described in [Prompt-based evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md#prompt-based-evaluators):

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

After you register your custom evaluator, you can view it in your [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library). In your Azure AI Foundry project, select **Evaluation**, then select **Evaluator library**.

### Troubleshooting: Job Stuck in Running State

Your evaluation job might remain in the **Running** state for an extended period when using Azure AI Foundry Project or Hub. The Azure OpenAI model you selected might not have enough capacity.

**Resolution**

1. Cancel the current evaluation job.
1. Increase the model capacity to handle larger input data.
1. Run the evaluation again.

## Related content

- [Evaluate your generative AI applications locally](./evaluate-sdk.md)
- [Monitor your generative AI applications](../monitor-applications.md)
- [Learn more about simulating test datasets for evaluation](./simulator-interaction-data.md)
- [See evaluation results in the Azure AI Foundry portal](../../how-to/evaluate-results.md)
- [Get started with Azure AI Foundry](../../quickstarts/get-started-code.md)
- [Get started with evaluation samples](https://aka.ms/aistudio/eval-samples)
