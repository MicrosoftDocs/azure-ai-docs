---
title: "Use admin-connected models in cloud evaluations"
description: "Learn how to use models connected through an enterprise AI gateway as evaluators, targets, and simulators in Microsoft Foundry cloud evaluations."
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom:
  - classic-and-new
  - references_regions
ms.topic: how-to
ms.date: 08/04/2026
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
# customer intent: As a developer, I want to use an admin-connected model in cloud evaluations so that model calls are routed through my organization's AI gateway.
---

# Use admin-connected models in cloud evaluations

Admin-connected models are models hosted behind an enterprise AI gateway, such as [Azure API Management](../../agents/how-to/ai-gateway.md) or a non-Azure AI model gateway, that an administrator connects to your Foundry project. You can use an admin-connected model for cloud evaluation scenarios that accept a model deployment.

Foundry resolves the connection endpoint and authentication, including API key, managed identity, or OAuth 2.0 authentication. Your evaluation request references the connection and deployment, not the gateway endpoint or its credentials.

> [!IMPORTANT]
> Cloud evaluation supports admin-connected models only when the connected deployment exposes the OpenAI **Chat Completions API**. 

> [!NOTE]
> Admin-connected model support in cloud evaluation is in preview and might not be available in all regions.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md).
- **Foundry User** role on the Foundry project.
- An administrator has created an Azure API Management or non-Azure AI model gateway connection on your Foundry resource and added the model on the **Manage** > **Resource details** > **Admin-connected models** tab. For setup instructions, see [Bring your own model to Foundry Agent Service](../../agents/how-to/ai-gateway.md).
- The connection name and deployment name for a model that supports the OpenAI Chat Completions API.

## Reference an admin-connected model

Use the following format anywhere a supported evaluation scenario accepts a model deployment:

```text
<connection-name>/<deployment-name>
```

The following table shows common evaluation surfaces and the field that accepts the reference:

| Scenario | Field |
|----------|-------|
| AI-assisted evaluator (judge) | `initialization_parameters.model` |
| Model target | `target.model` |
| Conversation simulation | `item_generation_params.model` |

## Use an admin-connected model as an evaluator judge model

Set `initialization_parameters.model` when you configure an AI-assisted evaluator. This example uses the admin-connected model as the judge for the coherence evaluator:

# [Python](#tab/python)

```python
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator

admin_connected_model = "my-apim-connection/gpt-4o"

testing_criteria = [
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="coherence",
        evaluator_name="builtin.coherence",
        initialization_parameters={"model": admin_connected_model},
        data_mapping={
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
    ),
]
```

# [JavaScript/TypeScript](#tab/javascript)

```typescript
const adminConnectedModel = "my-apim-connection/gpt-4o";

const testingCriteria = [
    {
        type: "azure_ai_evaluator",
        name: "coherence",
        evaluator_name: "builtin.coherence",
        initialization_parameters: { model: adminConnectedModel },
        data_mapping: {
            query: "{{item.query}}",
            response: "{{item.response}}",
        },
    },
];
```

---

- Reference: [`TestingCriterionAzureAIEvaluator`](/python/api/azure-ai-projects/azure.ai.projects.models.testingcriterionazureaievaluator) (Python)
- Reference: [OpenAI Evals API](https://platform.openai.com/docs/api-reference/evals) (`testing_criteria`, both languages)

## Use an admin-connected model as a target

Set `target.model` to send each evaluation input to the admin-connected model:

# [Python](#tab/python)

```python
admin_connected_model = "my-apim-connection/gpt-4o"

target = {
    "type": "azure_ai_model",
    "model": admin_connected_model,
    "sampling_params": {
        "top_p": 1.0,
        "max_completion_tokens": 2048,
    },
}
```

# [JavaScript/TypeScript](#tab/javascript)

```typescript
const adminConnectedModel = "my-apim-connection/gpt-4o";

const target = {
    type: "azure_ai_model",
    model: adminConnectedModel,
    sampling_params: {
        top_p: 1.0,
        max_completion_tokens: 2048,
    },
};
```

---

- Reference: [OpenAI Evals API](https://platform.openai.com/docs/api-reference/evals) (`data_source.target`, both languages)

Use this target with the [model target evaluation flow described in Run evaluations in the cloud](cloud-evaluation-targets.md#evaluate-a-model-target).

## Use other evaluation scenarios

Other model-based scenarios in [Run evaluations in the cloud by using the Microsoft Foundry SDK](cloud-evaluation.md) work similarly with admin-connected models. Wherever the scenario accepts a supported model deployment, replace the deployment name with `<connection-name>/<deployment-name>`. For example, conversation simulation accepts this reference in `item_generation_params.model`.

Keep the Foundry project endpoint unchanged, and don't add the gateway endpoint or credentials to the evaluation request. Foundry resolves those values from the admin-connected model connection.

> [!NOTE]
> Admin-connected model isn't available for synthetic data generation.

## Related content

- [Run evaluations in the cloud by using the Microsoft Foundry SDK](cloud-evaluation.md)
- [Bring your own model to Foundry Agent Service](../../agents/how-to/ai-gateway.md)
