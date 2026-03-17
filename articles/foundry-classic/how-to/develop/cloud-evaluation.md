---
title: "Cloud Evaluation with the Microsoft Foundry SDK (classic)"
description: "Run scalable evaluations for generative AI applications using the Microsoft Foundry SDK. Learn how to integrate evaluations into your development pipeline. (classic)"
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - references_regions
  - ignite-2024
ms.topic: how-to
ms.date: 02/14/2026
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
# customer intent: As a developer, I want to run evaluations in the cloud using the Microsoft Foundry SDK so I can test my generative AI application on large datasets without managing local compute infrastructure.
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# Run evaluations in the cloud by using the Microsoft Foundry SDK (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/how-to/develop/cloud-evaluation.md)

[!INCLUDE [feature-preview](../../../foundry/includes/feature-preview.md)]

In this article, you learn how to run evaluations in the cloud (preview) for predeployment testing on a test dataset. The Azure AI Evaluation SDK lets you run evaluations locally on your machine and in the cloud. For example, run local evaluations on small test data to assess your generative AI application prototypes, and then move into predeployment testing to run evaluations on a large dataset.

Use cloud evaluations for most scenarios—especially when testing at scale, integrating evaluations into continuous integration and continuous delivery (CI/CD) pipelines, or performing predeployment testing. Running evaluations in the cloud eliminates the need to manage local compute infrastructure and supports large scale, automated testing workflows. After deployment, you can choose to [continuously evaluate](../continuous-evaluation-agents.md) your agents for post-deployment monitoring.

When you use the Foundry SDK, it logs evaluation results in your Foundry project for better observability. This feature supports all Microsoft-curated [built in evaluators](../../concepts/built-in-evaluators.md). and your own [custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md). Your evaluators can be located in the [evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library) and have the same project-scope, role-based access control.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md).
- An Azure OpenAI deployment with a GPT model that supports chat completion (for example, `gpt-5-mini`).
- **Azure AI User** role on the Foundry project.
- Optionally, you can [use your own storage account](../../concepts/evaluation-regions-limits-virtual-network.md#bring-your-own-storage) to run evaluations.

> [!NOTE]
> Some evaluation features have regional restrictions. See [supported regions](../../concepts/evaluation-evaluators/risk-safety-evaluators.md#foundry-project-configuration-and-region-support) for details.

## Get started

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
   model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"] # E.g. gpt-5-mini

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

## <a name = "uploading-evaluation-data"></a> Prepare input data

```python
# Upload a local JSONL file. Skip this step if you already have a dataset registered.
data_id = project_client.datasets.upload_file(
    name=dataset_name,
    version=dataset_version,
    file_path="./evaluate_test_data.jsonl",
).id
```

To learn more about input data formats for evaluating generative AI applications, see:

- [Single-turn data](./evaluate-sdk.md#single-turn-support-for-text)
- [Conversation data](./evaluate-sdk.md#conversation-support-for-text)
- [Conversation data for images and multi-modalities](./evaluate-sdk.md#conversation-support-for-images-and-multimodal-text-and-image)

To learn more about input data formats for evaluating agents, see [Evaluate Azure AI agents](./agent-evaluate-sdk.md#evaluate-microsoft-foundry-agents) and [Evaluate other agents](./agent-evaluate-sdk.md#evaluating-other-agents).

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

# Specify the evaluator name that appears in the evaluator catalog.
evaluator_name = "AnswerLenEvaluator"

# Register the evaluator to the evaluator catalog.
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

After you register your custom evaluator, view it in your [evaluator catalog](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library). In your Foundry project, select **Evaluation**, then select **evaluator catalog**.

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

# Specify the evaluator name that appears in the evaluator catalog.
evaluator_name = "FriendlinessEvaluator"

# Register the evaluator to the evaluator catalog.
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

After you register your custom evaluator, you can view it in your [evaluator catalog](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library). In your Foundry project, select **Evaluation**, then select **evaluator catalog**.

## Get results

## Troubleshooting

## Related content

- [Evaluate your generative AI applications locally](./evaluate-sdk.md)
- [Monitor your generative AI applications](../monitor-applications.md)
- [Learn about simulating test datasets for evaluation](./simulator-interaction-data.md)
- [See evaluation results in the Foundry portal](../../how-to/evaluate-results.md)
- [Get started with Foundry](../../quickstarts/get-started-code.md)
- [Get started with evaluation samples](https://aka.ms/aistudio/eval-samples)
- [REST API Reference Documentation](/rest/api/aifoundry/aiprojects/evaluations)

