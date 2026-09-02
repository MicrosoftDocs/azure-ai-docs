---
title: "Simulate conversations with the Microsoft Foundry SDK"
description: "Use the Microsoft Foundry SDK to generate simulated conversations from scenarios and evaluate agent behavior."
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom:
  - references_regions
ms.topic: how-to
ms.date: 08/31/2026
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
# customer intent: As a developer, I want to simulate and evaluate conversations so that I can test agent behavior before deployment.
---

# Simulate conversations with the Microsoft Foundry SDK (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Generate simulated conversations from scenario descriptions and evaluate them at the conversation level. Use this scenario to test your agent's behavior in controlled situations before deployment. The service generates realistic conversations based on your scenario descriptions and then evaluates them.

## Prerequisites

- Complete the [cloud evaluation prerequisites](cloud-evaluation.md#prerequisites) and [client setup](cloud-evaluation.md#set-up-the-sdk-client).
- A model deployment to simulate users.
- An agent target to evaluate.
- Scenario data that describes the interactions to simulate.

The examples use the SDK client configured in [Set up the SDK client](cloud-evaluation.md#set-up-the-sdk-client).

## Understand conversation simulation

This approach is useful for:

- **Pre-deployment testing**: Validate agent behavior across diverse scenarios without real user traffic.
- **Edge case coverage**: Test scenarios that rarely occur naturally but are important to handle well.
- **Regression testing**: Ensure agent updates don't degrade performance on known scenarios.
- **Scale testing**: Generate many conversations quickly to stress-test agent capabilities.

Conversation simulation follows these steps:

1. You provide a dataset of scenario descriptions—each row describes a situation the simulated user tries to accomplish.
1. The service uses a simulator model to play the role of the user, interacting with your agent based on the scenario.
1. Each scenario generates one or more complete conversations.
1. Conversation-level evaluators assess the generated conversations.
1. Your project stores both the conversations and evaluation results.

## Prepare scenario data

> [!TIP]
> Instead of authoring scenarios by hand, generate them by using the **Simulation seed (multi-turn)** task type. The generated dataset contains the required `test_case_description` field and can also contain `id`, `category`, and `desired_num_turns`. Use the generated dataset's ID as `scenarios_id` in the simulation run and skip the upload step. See [Generate a simulation seed dataset](evaluation-dataset-synthetic.md#generate-a-simulation-seed-dataset-sdk).

Create a JSONL file where each line describes a scenario for the simulated user. Each row must contain `test_case_description`. The `id`, `category`, and `desired_num_turns` fields are optional. Include details about the user's goal, context, and constraints. For a complete example, see the [conversation evaluation samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations) in the SDK.

```json
{"id": "contoso_refund_timeline", "test_case_description": "Customer returned an item to Contoso Electronics 5 days ago and hasn't received their refund yet. They want to know how long Contoso refunds take.", "desired_num_turns": 10}
{"id": "contoso_store_hours_lookup", "test_case_description": "Customer wants to know what time the Contoso Electronics store closes today. Simple single-fact question with possibly one clarifying turn about which location.", "desired_num_turns": 3}
```

Use these parameters to configure the simulation:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `num_conversations` | No | Number of conversations to generate per scenario. Defaults to 5, server-side cap of 5. |
| `max_turns` | No | Maximum number of turns (exchanges) per conversation. Defaults to 10, server-side cap of 50. |
| `model` | Yes | Model deployment to use for simulating the user. For example, `gpt-4.1`. The [model router](../../openai/concepts/model-router.md) isn't supported as the simulator model; it can only be used as the evaluation target. |
| `sampling_params` | No | Sampling parameters for the simulator model, including `temperature`, `top_p`, and `max_completion_tokens`. |
| `data_mapping` | No | Maps fields from your scenario JSONL to simulation parameters. Common mappings: `test_case_description`, `id`, `desired_num_turns`. |

## Define evaluators

Select evaluators designed for conversation-level assessment. The simulated conversations automatically map to the evaluators.

# [Python](#tab/python)

```python
import os
from openai.types.eval_create_params import DataSourceConfigCustom
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator, PromptAgentDefinition

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
model_deployment_name = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]
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
    ]
```

# [JavaScript/TypeScript](#tab/javascript)

The current JavaScript/TypeScript SDK samples don't demonstrate conversation simulation. Use the Python or cURL tab for this flow.

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals?api-version=2025-11-15-preview" \
  --header "Authorization: ******" \
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

## Create the evaluation and run

# [Python](#tab/python)

Download [sample_data_simulation_scenarios.jsonl](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/data_folder/sample_data_simulation_scenarios.jsonl).

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
    file_path="./sample_data_simulation_scenarios.jsonl",
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

# [JavaScript/TypeScript](#tab/javascript)

The current JavaScript/TypeScript SDK samples don't demonstrate conversation simulation. Use the Python or cURL tab for this flow.

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url "https://${ACCOUNT}.services.ai.azure.com/api/projects/${PROJECT}/openai/evals/${EVAL_ID}/runs?api-version=2025-11-15-preview" \
  --header "Authorization: ******" \
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

## Next steps

- To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).
- For a complete runnable example, see [sample_multiturn_conversation_simulation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_multiturn_conversation_simulation.py) on GitHub.
- To evaluate stored conversations, see [Evaluate conversation datasets](cloud-evaluation-conversations.md).
- To evaluate production traces, see [Evaluate deployed model and agent conversations](cloud-evaluation-deployed-conversations.md).
