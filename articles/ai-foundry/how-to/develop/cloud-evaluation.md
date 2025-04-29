---
title: Cloud evaluation with Azure AI Projects SDK
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to evaluate a Generative AI application on the cloud.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - references_regions
  - ignite-2024
ms.topic: how-to
ms.date: 02/21/2025
ms.reviewer: changliu2
ms.author: lagayhar
author: lgayhardt
---
# Evaluate your Generative AI application on the cloud with Azure AI Projects SDK (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

While Azure AI Evaluation SDK client supports running evaluations locally on your own machine, you might want to delegate the job remotely to the cloud. For example, after you ran local evaluations on small test data to help assess your generative AI application prototypes, now you move into pre-deployment testing and need run evaluations on a large dataset. Cloud evaluation frees you from managing your local compute infrastructure, and enables you to integrate evaluations as tests into your CI/CD pipelines. After deployment, you might want to [continuously evaluate](../online-evaluation.md) your applications for post-deployment monitoring.

In this article, you learn how to run cloud evaluation (preview) in pre-deployment testing on a test dataset. Using the Azure AI Projects SDK, you'll have evaluation results automatically logged into your Azure AI project for better observability. This feature supports all Microsoft curated [built-in evaluators](./evaluate-sdk.md#built-in-evaluators) and your own [custom evaluators](./evaluate-sdk.md#custom-evaluators) which can be located in the [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library) and have the same project-scope RBAC.

## Prerequisites

- Azure AI project in the same [regions](./evaluate-sdk.md#region-support) as risk and safety evaluators (preview). If you don't have an existing project, follow the guide [How to create Azure AI project](../create-projects.md?tabs=ai-studio) to create one.

- Azure OpenAI Deployment with GPT model supporting `chat completion`, for example `gpt-4`.
- `Connection String` for Azure AI project to easily create `AIProjectClient` object. You can get the **Project connection string** under **Project details** from the project's **Overview** page.
- Make sure you're first logged into your Azure subscription by running `az login`.

### Installation Instructions

1. Create a **virtual Python environment of you choice**. To create one using conda, run the following command:

    ```bash
    conda create -n cloud-evaluation
    conda activate cloud-evaluation
    ```

2. Install the required packages by running the following command:

    ```bash
   pip install azure-identity azure-ai-projects azure-ai-ml
    ```

    Optionally you can use `pip install azure-ai-evaluation` if you want a code-first experience to fetch evaluator ID for built-in evaluators in code.

Now you can define a client and a deployment which will be used to run your evaluations in the cloud:

```python

import os, time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import Evaluation, Dataset, EvaluatorConfiguration, ConnectionType
from azure.ai.evaluation import F1ScoreEvaluator, RelevanceEvaluator, ViolenceEvaluator

# Load your Azure OpenAI config
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
api_version = os.environ.get("AZURE_OPENAI_API_VERSION")

# Create an Azure AI Client from a connection string. Available on Azure AI project Overview page.
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="<connection_string>"
)
```

## Uploading evaluation data

Prepare the data according the [input data requirements for built-in evaluators](./evaluate-sdk.md#data-requirements-for-built-in-evaluators). For example in text evaluation, a `"./evaluate_test_data.jsonl"` file may contain single-turn data inputs like this: 
```json
{"query":"What is the capital of France?","response":"Paris."}
{"query":"What atoms compose water?","response":"Hydrogen and oxygen."}
{"query":"What color is my shirt?","response":"Blue."}
```
or contain conversation data like this:
```json
{"conversation":
    {
        "messages": [
        {
            "content": "Which tent is the most waterproof?", 
            "role": "user"
        },
        {
            "content": "The Alpine Explorer Tent is the most waterproof",
            "role": "assistant", 
            "context": "From the our product list the alpine explorer tent is the most waterproof. The Adventure Dining Table has higher weight."
        },
        {
            "content": "How much does it cost?",
            "role": "user"
        },
        {
            "content": "The Alpine Explorer Tent is $120.",
            "role": "assistant",
            "context": null
        }
        ]
    }
}
```

For more details on input data formats, refer to [single-turn data](./evaluate-sdk.md#single-turn-support-for-text), [conversation data](./evaluate-sdk.md#conversation-support-for-text), and [conversation data for images and multi-modalities](./evaluate-sdk.md#conversation-support-for-images-and-multi-modal-text-and-image). 

For agent evaluation, refer to [evaluator support for agent messages](./agent-evaluate-sdk.md#evaluators-with-agent-message-support).
 

We provide two ways to register your data in Azure AI project required for evaluations in the cloud:

1. **From SDK**: Upload new data from your local directory to your Azure AI project in the SDK, and fetch the dataset ID as a result. 



```python
data_id, _ = project_client.upload_file("./evaluate_test_data.jsonl")
```

**From UI**: Alternatively, you can upload new data or update existing data versions by following the UI walkthrough under the **Data** tab of your Azure AI project.

2. Given existing datasets uploaded to your Project:

- **From SDK**: if you already know the dataset name you created, construct the dataset ID in this format: `/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<project-name>/data/<dataset-name>/versions/<version-number>`

- **From UI**: If you don't know the dataset name, locate it under the **Data** tab of your Azure AI project and construct the dataset ID as in the format previously.

## Specifying evaluators from Evaluator library

We provide a list of built-in evaluators registered in the [Evaluator library](../evaluate-generative-ai-app.md#view-and-manage-the-evaluators-in-the-evaluator-library) under **Evaluation** tab of your Azure AI project. You can also register custom evaluators and use them for Cloud evaluation. We provide two ways to specify registered evaluators:

### Specifying built-in evaluators

- **From SDK**: Use built-in evaluator `id` property supported by `azure-ai-evaluation` SDK:

```python
from azure.ai.evaluation import F1ScoreEvaluator, RelevanceEvaluator, ViolenceEvaluator
print("F1 Score evaluator id:", F1ScoreEvaluator.id)
```

- **From UI**: Follows these steps to fetch evaluator IDs after they're registered to your project:
  - Select **Evaluation** tab in your Azure AI project;
  - Select Evaluator library;
  - Select your evaluators of choice by comparing the descriptions;
  - Copy its "Asset ID" which will be your evaluator ID, for example, `azureml://registries/azureml/models/Groundedness-Evaluator/versions/1`.

### Specifying custom evaluators

- For code-based custom evaluators, register them to your Azure AI project and fetch the evaluator IDs as in this example:

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

- For prompt-based custom evaluators, use this snippet to register them. For example, let's register our `FriendlinessEvaluator` built as described in [Prompt-based evaluators](./evaluate-sdk.md#prompt-based-evaluators):

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

## Cloud evaluation (preview) with Azure AI Projects SDK

Putting the above altogether, you can now submit a cloud evaluation with Azure AI Projects SDK via a Python API. See the following example specifying an NLP evaluator (F1 score), AI-assisted quality and safety evaluator (Relevance and Violence), and a custom evaluator (Friendliness) with their [evaluator IDs](#specifying-evaluators-from-evaluator-library):

```python
import os, time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import Evaluation, Dataset, EvaluatorConfiguration, ConnectionType
from azure.ai.evaluation import F1ScoreEvaluator, RelevanceEvaluator, ViolenceEvaluator

# Load your Azure OpenAI config
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
api_version = os.environ.get("AZURE_OPENAI_API_VERSION")

# Create an Azure AI Client from a connection string. Avaiable on project overview page on Azure AI project UI.
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="<connection_string>"
)

# Construct dataset ID per the instruction above
data_id = "<dataset-id>"

default_connection = project_client.connections.get_default(connection_type=ConnectionType.AZURE_OPEN_AI)

# Use the same model_config for your evaluator (or use different ones if needed)
model_config = default_connection.to_evaluator_model_config(deployment_name=deployment_name, api_version=api_version)

# select the list of evaluators you care about
evaluators = {
        # Note the evaluator configuration key must follow a naming convention
        # the string must start with a letter with only alphanumeric characters 
        # and underscores. Take "f1_score" as example: "f1score" or "f1_evaluator" 
        # will also be acceptable, but "f1-score-eval" or "1score" will result in errors.
        "f1_score": EvaluatorConfiguration(
            id=F1ScoreEvaluator.id,
        ),
        "relevance": EvaluatorConfiguration(
            id=RelevanceEvaluator.id,
            init_params={
                "model_config": model_config
            },
        ),
        "violence": EvaluatorConfiguration(
            id=ViolenceEvaluator.id,
            init_params={
                "azure_ai_project": project_client.scope
            },
        ),
        "friendliness": EvaluatorConfiguration(
            id="<custom_evaluator_id>",
            init_params={
                "model_config": model_config
            }
        )
}

# Create an evaluation
evaluation = Evaluation(
    display_name="Cloud evaluation",
    description="Evaluation of dataset",
    data=Dataset(id=data_id),
    evaluators=evaluators
)

# Create evaluation
evaluation_response = project_client.evaluations.create(
    evaluation=evaluation,
)

# Get evaluation result
get_evaluation_response = project_client.evaluations.get(evaluation_response.id)

print("----------------------------------------------------------------")
print("Created evaluation, evaluation ID: ", get_evaluation_response.id)
print("Evaluation status: ", get_evaluation_response.status)
print("AI project URI: ", get_evaluation_response.properties["AiStudioEvaluationUri"])
print("----------------------------------------------------------------")
```

Following the URI, you will be redirected to Foundry to view your evaluation results in your Azure AI project and debug your application. Using reason fields and pass/fail, you will be able to better assess the quality and safety performance of your applications. You can run and compare multiple runs to test for regression or improvements.  

## Related content

- [Evaluate your Generative AI applications locally](./evaluate-sdk.md)
- [Evaluate your Generative AI applications online](https://aka.ms/GenAIMonitoringDoc)
- [Learn more about simulating test datasets for evaluation](./simulator-interaction-data.md)
- [View your evaluation results in Azure AI project](../../how-to/evaluate-results.md)
- [Get started building a chat app using the Azure AI Foundry SDK](../../quickstarts/get-started-code.md)
- [Get started with evaluation samples](https://aka.ms/aistudio/eval-samples)
