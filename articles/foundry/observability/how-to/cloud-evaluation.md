---
title: "Introduction to cloud evaluation with Microsoft Foundry SDK"
description: "Set up the Microsoft Foundry SDK and choose a cloud evaluation workflow for datasets, targets, interactions, conversations, or synthetic data."
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom:
  - classic-and-new
  - references_regions
ms.topic: how-to
ms.date: 08/31/2026
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
# customer intent: As a developer, I want to set up cloud evaluations and choose the right workflow so that I can assess my generative AI application at scale.
---

# Introduction to cloud evaluation with Microsoft Foundry SDK

Use cloud evaluations to test generative AI applications at scale without managing local compute. This article sets up the shared SDK client and helps you choose a workflow for predeployment or production evaluation.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md).
- An Azure OpenAI deployment with a GPT model that supports chat completion, such as `gpt-5-mini`.
- The **Foundry User** role on the Foundry project.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]
- Optionally, [your own storage account](../../concepts/evaluation-regions-limits-virtual-network.md#bring-your-own-storage)
  for evaluation data.

Some evaluation features have regional restrictions. Review the [supported regions](../../concepts/evaluation-evaluators/risk-safety-evaluators.md#foundry-project-configuration-and-region-support) before you begin.

## Set up the SDK client

Install the SDK for your language. Set these shared environment variables:

- `AZURE_AI_PROJECT_ENDPOINT`: Your Foundry project endpoint, for example, `https://<account_name>.services.ai.azure.com/api/projects/<project_name>`.
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`: The model deployment used by AI-assisted evaluators.
- `DATASET_NAME` and `DATASET_VERSION`: Optional values for reusable datasets.

Authenticate with `DefaultAzureCredential`, create the project client, and get the OpenAI client used by the evaluation API.

# [Python](#tab/python)

```bash
pip install "azure-ai-projects>=2.2.0"
```

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator
from openai.types.eval_create_params import DataSourceConfigCustom
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
    SourceFileID,
)

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
model_deployment_name = os.environ.get(
    "AZURE_AI_MODEL_DEPLOYMENT_NAME", ""
)
dataset_name = os.environ.get("DATASET_NAME", "")
dataset_version = os.environ.get("DATASET_VERSION", "1")

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()
```

# [JavaScript/TypeScript](#tab/javascript)

```bash
npm install @azure/ai-projects @azure/identity dotenv
```

```javascript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "";
const modelDeploymentName =
  process.env["AZURE_AI_MODEL_DEPLOYMENT_NAME"] || "";
const datasetName = process.env["DATASET_NAME"] || "";
const datasetVersion = process.env["DATASET_VERSION"] || "1";

const projectClient = new AIProjectClient(
  projectEndpoint,
  new DefaultAzureCredential(),
);
const openaiClient = projectClient.getOpenAIClient();
```

Reference: [AIProjectClient class](/javascript/api/@azure/ai-projects/aiprojectclient)

---

To use a model connected through admin connections as a target, judge model, or conversation simulator, see [Use admin-connected models in cloud evaluations](evaluate-admin-connected-models.md).

## Understand the evaluation workflow

A cloud evaluation has three steps:

1. Define the data shape and the evaluators that score it.
1. Create the evaluation with `openai_client.evals.create()`.
1. Start a run with `openai_client.evals.runs.create()`, poll until it completes, and retrieve the scored results.

Cloud evaluation results are stored in your Foundry project. You can retrieve them through the SDK, review them in the portal, or route them to Application Insights when it's connected.

## Choose evaluators

Evaluators bind to fields in your data through column mappings. Dataset workflows expose item fields, while target-generated workflows also expose the model or agent output through the sample schema.

Review the [built-in evaluators](../../concepts/built-in-evaluators.md) and [custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md) before you configure testing criteria.

## Choose your starting point

| Evaluation unit | Starting point | Workflow |
|---|---|---|
| Individual turn | You have JSONL or CSV test data with a query and response. | [Evaluate query-response datasets](cloud-evaluation-datasets.md) |
| Individual turn | You have queries and want a model or agent to generate responses. | [Evaluate model and agent responses](cloud-evaluation-targets.md) |
| Individual turn | You have stored responses or traces from individual interactions with a deployed model or agent. | [Evaluate deployed model and agent interactions](cloud-evaluation-deployed-interactions.md) |
| Individual turn | You need to generate synthetic queries. | [Generate synthetic queries](cloud-evaluation-synthetic-data.md#generate-synthetic-queries) |
| Complete conversation | You have a dataset of complete conversations. | [Evaluate conversation datasets](cloud-evaluation-conversations.md) |
| Complete conversation | You have traces that capture complete conversations with a deployed model or agent. | [Evaluate deployed model and agent conversations](cloud-evaluation-deployed-conversations.md) |
| Complete conversation | You need to generate and evaluate simulated agent conversations. | [Simulate agent conversations](cloud-evaluation-simulate-conversations.md) |
| Any evaluation unit | You need to poll, interpret, cancel, or troubleshoot a run. | [Get evaluation results](cloud-evaluation-results.md) |

For adversarial safety testing, use [AI red teaming](../../how-to/develop/run-ai-red-teaming-cloud.md). To create a standalone dataset, see [Generate a synthetic evaluation dataset](../../observability/how-to/evaluation-dataset-synthetic.md).

## Related content

- [Get cloud evaluation results](cloud-evaluation-results.md)
- [View evaluation results in the Foundry portal](../../how-to/evaluate-results.md)
- [Set up continuous evaluation](../../observability/how-to/how-to-monitor-agents-dashboard.md#set-up-continuous-evaluation)
- [Complete Python SDK evaluation samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations)
- [REST API reference](https://ai.azure.com/api-reference)
