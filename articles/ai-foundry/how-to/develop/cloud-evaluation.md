---
title: Cloud evaluation with Azure AI Foundry SDK
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to evaluate a Generative AI application on the cloud.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - references_regions
  - ignite-2024
ms.topic: how-to
ms.date: 05/19/2025
ms.reviewer: changliu2
ms.author: lagayhar
author: lgayhardt
---
# Run evaluations in the cloud using Azure AI Foundry SDK (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

While Azure AI Evaluation SDK supports running evaluations locally on your own machine, you might want to delegate the job remotely to the cloud. For example, after you ran local evaluations on small test data to help assess your generative AI application prototypes, now you move into pre-deployment testing and need run evaluations on a large dataset. Cloud evaluation frees you from managing your local compute infrastructure, and enables you to integrate evaluations as tests into your CI/CD pipelines. After deployment, you might want to [continuously evaluate](../online-evaluation.md) your applications for post-deployment monitoring.

In this article, you learn how to run evaluations in the cloud (preview) in pre-deployment testing on a test dataset. Using the Azure AI Projects SDK, you'll have evaluation results automatically logged into your Azure AI project for better observability. This feature supports all Microsoft curated [built-in evaluators](../../concepts/observability.md#what-are-evaluators) and your own [custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md) which can be located in the [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library) and have the same project-scope RBAC.

## Prerequisite set up steps for Azure AI Foundry Projects

- Azure AI Foundry project in the same supported [regions](../../concepts/evaluation-evaluators/risk-safety-evaluators.md#azure-ai-foundry-project-configuration-and-region-support) as risk and safety evaluators (preview). If you don't have an existing project, follow the guide [How to create Azure AI Foundry project](../create-projects.md?tabs=ai-studio) to create one.

- Azure OpenAI Deployment with GPT model supporting `chat completion`, for example `gpt-4`.
- Make sure you're first logged into your Azure subscription by running `az login`.

If this is your first time running evaluations and logging it to your Azure AI Foundry project, you may need to do a few additional set up steps.

1. [Create and connect your storage account](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/infrastructure-setup/01-connections/connection-storage-account.bicep) to your Azure AI Foundry project at the resource level. This bicep template provisions and connects a storage account to your Foundry project with key authentication.
2. Make sure the connected storage account has access to all projects.
3. If you connected your storage account with Entra ID, make sure to give MSI (Microsoft Identity) permissions for Storage Blob Data Owner to both your account and Foundry project resource in Azure Portal.

### Getting started

First, install Azure AI Foundry SDK's project client which will run the evaluations in the cloud

```python
uv install azure-ai-projects azure-identity
```

> [!NOTE]
> For more detailed information, see the [REST API Reference Documentation](/rest/api/aifoundry/aiprojects/evaluations).
Then, set your environment variables for your Azure AI Foundry resources

```python
import os

# Required environment variables
endpoint = os.environ["PROJECT_ENDPOINT"] # https://<account>.services.ai.azure.com/api/projects/<project>
model_endpoint = os.environ["MODEL_ENDPOINT"] # https://<account>.services.ai.azure.com
model_api_key = os.environ["MODEL_API_KEY"]
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"] # e.g. gpt-4o-mini

# Optional – reuse an existing dataset
dataset_name    = os.environ.get("DATASET_NAME",    "dataset-test")
dataset_version = os.environ.get("DATASET_VERSION", "1.0")
```

Now you can define a client which will be used to run your evaluations in the cloud:

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Create the project client (Foundry project and credentials)
project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)
```

## Uploading evaluation data

```python
# Upload a local jsonl file (skip if you already have a Dataset registered)
data_id = project_client.datasets.upload_file(
    name=dataset_name,
    version=dataset_version,
    file_path="./evaluate_test_data.jsonl",
).id
```

To learn more about input data formats for evaluating GenAI applications, see [single-turn data](./evaluate-sdk.md#single-turn-support-for-text), [conversation data](./evaluate-sdk.md#conversation-support-for-text), and [conversation data for images and multi-modalities](./evaluate-sdk.md#conversation-support-for-images-and-multi-modal-text-and-image).

To learn more about input data formats for evaluating agents, see [evaluating Azure AI agents](./agent-evaluate-sdk.md#evaluate-azure-ai-agents) and [evaluating other agents](./agent-evaluate-sdk.md#evaluating-other-agents).

## Specifying evaluators

```python
from azure.ai.projects.models import (
    EvaluatorConfiguration,
    EvaluatorIds,
)

# Built-in evaluator configurations
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

## Submit evaluation in the cloud

Finally, submit the remote evaluation run:

```python
from azure.ai.projects.models import (
    Evaluation,
    InputDataset
)

# Create an evaluation with the dataset and evaluators specified
evaluation = Evaluation(
    display_name="Cloud evaluation",
    description="Evaluation of dataset",
    data=InputDataset(id=data_id),
    evaluators=evaluators,
)

# Run the evaluation 
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

## Specifying custom evaluators

> [!NOTE]
> Azure AI Foundry Projects are not supported for this feature, use an Azure AI Hub Project instead.

### Code-based custom evaluators

Register your custom evaluators to your Azure AI Hub project and fetch the evaluator IDs:

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model
from promptflow.client import PFClient

# Define ml_client to register custom evaluator
ml_client = MLClient(
       subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
       resource_group_name=os.environ["AZURE_RESOURCE_GROUP"],
       workspace_name=os.environ["AZURE_PROJECT_NAME"],
       credential=DefaultAzureCredential()
)

# Load evaluator from module
from answer_len.answer_length import AnswerLengthEvaluator

# Then we convert it to evaluation flow and save it locally
pf_client = PFClient()
local_path = "answer_len_local"
pf_client.flows.save(entry=AnswerLengthEvaluator, path=local_path)

# Specify evaluator name to appear in the Evaluator library
evaluator_name = "AnswerLenEvaluator"

# Finally register the evaluator to the Evaluator library
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

After registering your custom evaluator to your Azure AI project, you can view it in your [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library) under **Evaluation** tab in your Azure AI project.

### Prompt-based custom evaluators

Follow the example to register a custom `FriendlinessEvaluator` built as described in [Prompt-based evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md#prompt-based-evaluators):

```python
# Import your prompt-based custom evaluator
from friendliness.friend import FriendlinessEvaluator

# Define your deployment 
model_config = dict(
    azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_API_VERSION"),
    api_key=os.environ.get("AZURE_API_KEY"), 
    type="azure_openai"
)

# Define ml_client to register custom evaluator
ml_client = MLClient(
       subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
       resource_group_name=os.environ["AZURE_RESOURCE_GROUP"],
       workspace_name=os.environ["AZURE_PROJECT_NAME"],
       credential=DefaultAzureCredential()
)

# # Convert evaluator to evaluation flow and save it locally
local_path = "friendliness_local"
pf_client = PFClient()
pf_client.flows.save(entry=FriendlinessEvaluator, path=local_path) 

# Specify evaluator name to appear in the Evaluator library
evaluator_name = "FriendlinessEvaluator"

# Register the evaluator to the Evaluator library
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

After logging your custom evaluator to your Azure AI project, you can view it in your [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library) under **Evaluation** tab of your Azure AI project.

## Related content

- [Evaluate your Generative AI applications locally](./evaluate-sdk.md)
- [Evaluate your Generative AI applications online](https://aka.ms/GenAIMonitoringDoc)
- [Learn more about simulating test datasets for evaluation](./simulator-interaction-data.md)
- [View your evaluation results in Azure AI project](../../how-to/evaluate-results.md)
- [Get started building a chat app using the Azure AI Foundry SDK](../../quickstarts/get-started-code.md)
- [Get started with evaluation samples](https://aka.ms/aistudio/eval-samples)
