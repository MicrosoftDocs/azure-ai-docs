---
title: "Simulate conversations with the Microsoft Foundry SDK"
description: "Use the Microsoft Foundry SDK to generate simulated conversations from scenarios and evaluate agent behavior."
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom:
  - references_regions
ms.topic: how-to
ms.date: 09/11/2026
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

1. You provide scenario descriptions as JSONL data or strongly typed inline test cases. Each test case describes a situation the simulated user tries to accomplish.
1. The service uses a simulator model to play the role of the user, interacting with your agent based on the scenario.
1. Each scenario generates one or more complete conversations.
1. Conversation-level evaluators assess the generated conversations.
1. Your project stores the evaluation results. You can optionally persist all generated conversations as a versioned Foundry dataset.

The run uses the `azure_ai_user_conversation_simulation_preview` data source. Put settings that apply to every test case in `default_simulation_configuration`. A test case can override individual conversation settings in its `simulation_configuration`; settings that it doesn't override continue to use the run defaults.

## Prepare scenario data

> [!TIP]
> Instead of authoring scenarios by hand, generate them by using the **Simulation seed (multi-turn)** task type. Before using an existing generated dataset with this API, normalize `id` to `test_case_id` and move `desired_num_turns` into `simulation_configuration`. See [Generate a simulation seed dataset](evaluation-dataset-synthetic.md#generate-a-simulation-seed-dataset-sdk).

Supply test cases by using one of these source types:

- `file_id` or `file_content` for JSONL scenarios.
- `inline_user_conversation_simulation` for strongly typed test cases in the run request. Include at least one test case.

For JSONL, use the canonical property names shown in the following example. Include the user's goal, context, and behavioral constraints in `test_case_description`. The description can contain 1 through 2,500 characters.

```jsonl
{"test_case_id":"contoso_refund_timeline","test_case_description":"Customer returned an item five days ago and wants to know when the refund will arrive.","simulation_configuration":{"desired_num_turns":10}}
{"test_case_id":"contoso_store_hours_lookup","test_case_description":"Customer wants today's closing time and might need to clarify the store location.","simulation_configuration":{"desired_num_turns":3,"conversation_repetitions":2}}
```

When the JSONL data uses these canonical names, omit `data_mapping`. If it uses different names, map those attributes to `test_case_id`, `test_case_description`, and `simulation_configuration`. Don't use `data_mapping` with an `inline_user_conversation_simulation` source.

Each inline or JSONL test case supports these properties:

| Property | Description |
|---|---|
| `test_case_id` | Optional identifier. The service generates an identifier when you omit it. |
| `test_case_description` | Scenario, user goal, and behavioral constraints that guide the simulated conversation. |
| `simulation_configuration` | Optional settings that override the corresponding run defaults for this test case. |

## Configure the simulated user

Use the `model_configuration` object to configure the model that plays the simulated user. This model is separate from the `target` model or agent being evaluated.

| Property | Required | Description |
|---|---|---|
| `model` | Yes | Simulator deployment in `{connectionName}/{modelDeploymentName}` format. The [model router](../../openai/concepts/model-router.md) isn't supported as the simulator model; it can only be an evaluation target. |
| `sampling_params` | No | Sampling parameters applied when the simulator generates user turns. |
| `voice_model` | No | Converts simulated user text to speech through the Voice Live endpoint. Omit this property for text-only simulation. |

For voice simulation, `voice_model.type` must be `azure-standard`. Set `name` to an Azure standard neural voice name. You can also set `temperature` from 0 through 1; when omitted, the underlying voice model's default applies.

## Configure conversations

Set run-wide values in `default_simulation_configuration`. The conversation controls `max_num_turns`, `conversation_repetitions`, `desired_num_turns`, `audio_effects`, and `user_behavior` can also appear in a test case's `simulation_configuration` to override the corresponding run defaults. The dataset-generation properties `enable_conversation_dataset_generation` and `output_conversation_dataset_name` are valid only in `default_simulation_configuration` and can't be overridden per test case.

| Property | Scope | Default | Description |
|---|---|---|---|
| `max_num_turns` | Run or test case | `20` | Hard limit on turns in each conversation. Must be at least 1. |
| `conversation_repetitions` | Run or test case | `1` | Number of independent conversations generated for each test case. Must be at least 1. |
| `desired_num_turns` | Run or test case | None | Target conversation length. It can't exceed the effective `max_num_turns`. When omitted, the simulator determines the length from the scenario. |
| `audio_effects` | Run or test case | None | Effects applied to voice simulation. Ignored for text-only simulation. |
| `user_behavior` | Run or test case | None | Simulated user behavior, such as interruption. |
| `enable_conversation_dataset_generation` | Run only | `false` | Persists all generated conversations to a versioned Foundry dataset. |
| `output_conversation_dataset_name` | Run only | Service-generated | Dataset name used when conversation dataset generation is enabled. |

### Configure voice conditions and interruptions

Place `audio_effects` and `user_behavior` inside `default_simulation_configuration` to apply them to every test case. To override either setting for one test case, place it inside that test case's `simulation_configuration` instead.

Use `audio_effects` to test how the target performs under realistic listening conditions. Add one or more effects: `street_traffic`, `crowd_chatter`, `background_tv`, `metro_station`, or `telephonic_voice`. Set `volume_percentage` from 1 through 100 to control their combined volume. The default is `15`. Audio effects are ignored in text-only simulations.

Use `user_behavior.interruption` to test how the target handles a user speaking while the target is responding. Set its `type` to `default` to enable simulated interruptions. Omit `interruption` when interruptions aren't part of the test.

```json
{
  "default_simulation_configuration": {
    "audio_effects": {
      "effects": ["street_traffic", "telephonic_voice"],
      "volume_percentage": 20
    },
    "user_behavior": {
      "interruption": {
        "type": "default"
      }
    }
  }
}
```

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
simulator_model = os.environ["AZURE_AI_SIMULATOR_MODEL"]
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
    ]
```
# [C#](#tab/csharp)

```csharp
  object dataSourceConfig = new
  {
    type = "custom",
    item_schema = new
    {
      type = "object",
      properties = new { messages = new { type = "array" } },
      required = new[] { "messages" }
    },
    include_sample_schema = false
  };
  object[] testingCriteria =
  [
    new
    {
      type = "azure_ai_evaluator",
      name = "customer_satisfaction",
      evaluator_name = "builtin.customer_satisfaction",
      initialization_parameters = new { model = modelDeploymentName },
      data_mapping = new { messages = "{{item.messages}}" }
    }
  ];
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
      }
    ]
  }'
```

---

## Create the evaluation and run

# [Python](#tab/python)

Save the canonical JSONL rows from [Prepare scenario data](#prepare-scenario-data) as `simulation_scenarios.jsonl`.

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
    file_path="./simulation_scenarios.jsonl",
).id

# Create the evaluation
eval_object = openai_client.evals.create(
    name="Multi-turn Conversation Simulation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

# Create a simulation run. AZURE_AI_SIMULATOR_MODEL uses the format
# {connectionName}/{modelDeploymentName}.
eval_run = openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name="conversation-simulation-run",
    data_source={
        "type": "azure_ai_user_conversation_simulation_preview",
        "source": {
            "type": "file_id",
            "id": scenarios_id,
        },
        "target": {
            "type": "azure_ai_agent",
            "name": agent.name,
            "version": agent.version,
        },
        "model_configuration": {
            "model": simulator_model,
            "sampling_params": {
                "temperature": 0.7,
                "top_p": 1.0,
                "max_completion_tokens": 800,
            },
        },
        "default_simulation_configuration": {
            "max_num_turns": 8,
            "conversation_repetitions": 2,
            "desired_num_turns": 5,
            "enable_conversation_dataset_generation": True,
            "output_conversation_dataset_name": "support-simulations",
        },
    },
    extra_body={"evaluation_level": "conversation"},
)
```
# [C#](#tab/csharp)

Set `FOUNDRY_AGENT_NAME`, `FOUNDRY_AGENT_VERSION`, and `AZURE_AI_SIMULATOR_MODEL`. Save the canonical JSONL rows from [Prepare scenario data](#prepare-scenario-data) as `simulation_scenarios.jsonl`.

```csharp
  var agentName = Environment.GetEnvironmentVariable("FOUNDRY_AGENT_NAME")
    ?? throw new InvalidOperationException("FOUNDRY_AGENT_NAME isn't set.");
  var agentVersion = Environment.GetEnvironmentVariable(
    "FOUNDRY_AGENT_VERSION")
    ?? throw new InvalidOperationException("FOUNDRY_AGENT_VERSION isn't set.");
  var simulatorModel = Environment.GetEnvironmentVariable(
    "AZURE_AI_SIMULATOR_MODEL")
    ?? throw new InvalidOperationException("AZURE_AI_SIMULATOR_MODEL isn't set.");
  FileDataset scenarios = await projectClient.Datasets.UploadFileAsync(
    name: "simulation-scenarios",
    version: "1",
    filePath: "./simulation_scenarios.jsonl");

  BinaryData evaluationData = BinaryData.FromObjectAsJson(new
  {
    name = "Multi-turn Conversation Simulation",
    data_source_config = dataSourceConfig,
    testing_criteria = testingCriteria
  });
  using BinaryContent evaluationContent = BinaryContent.Create(evaluationData);
  ClientResult evaluation = await evaluationClient.CreateEvaluationAsync(
    evaluationContent);
  string evaluationId = GetString(evaluation, "id");

  BinaryData runData = BinaryData.FromObjectAsJson(new
  {
    name = "conversation-simulation-run",
    evaluation_level = "conversation",
    data_source = new
    {
      type = "azure_ai_user_conversation_simulation_preview",
      source = new { type = "file_id", id = scenarios.Id },
      target = new
      {
        type = "azure_ai_agent",
        name = agentName,
        version = agentVersion
      },
      model_configuration = new
      {
        model = simulatorModel,
        sampling_params = new
        {
          temperature = 0.7f,
          top_p = 1.0f,
          max_completion_tokens = 800
        }
      },
      default_simulation_configuration = new
      {
        max_num_turns = 8,
        conversation_repetitions = 2,
        desired_num_turns = 5,
        enable_conversation_dataset_generation = true,
        output_conversation_dataset_name = "support-simulations"
      }
    }
  });
  using BinaryContent runContent = BinaryContent.Create(runData);
  ClientResult evaluationRun = await evaluationClient.CreateEvaluationRunAsync(
    evaluationId: evaluationId,
    content: runContent);
  Console.WriteLine($"Evaluation run created: {GetString(evaluationRun, "id")}");
```

Reference: [`AIProjectDatasetsOperations.UploadFileAsync`](/dotnet/api/azure.ai.projects.aiprojectdatasetsoperations.uploadfileasync)
and [`EvaluationClient` protocol methods](https://github.com/openai/openai-dotnet/blob/main/OpenAI/src/Custom/Evals/EvaluationClient.Protocol.cs).
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
      "type": "azure_ai_user_conversation_simulation_preview",
      "source": {
        "type": "file_id",
        "id": "YOUR_SCENARIOS_DATASET_ID"
      },
      "target": {
        "type": "azure_ai_agent",
        "name": "my-agent",
        "version": "1"
      },
      "model_configuration": {
        "model": "my-connection/gpt-4.1",
        "sampling_params": {
          "temperature": 0.7,
          "top_p": 1.0,
          "max_completion_tokens": 800
        },
        "voice_model": {
          "type": "azure-standard",
          "name": "en-US-AvaMultilingualNeural",
          "temperature": 0.7
        }
      },
      "default_simulation_configuration": {
        "max_num_turns": 10,
        "conversation_repetitions": 2,
        "audio_effects": {
          "effects": ["street_traffic", "telephonic_voice"],
          "volume_percentage": 20
        },
        "user_behavior": {
          "interruption": {"type": "default"}
        },
        "enable_conversation_dataset_generation": true,
        "output_conversation_dataset_name": "voice-support-simulations"
      }
    }
  }'
```

---

## Use inline test cases

To define scenarios directly in the run request, set `data_source.source` to an `inline_user_conversation_simulation` source. Inline sources require at least one test case and don't use `data_mapping`.

# [Python](#tab/python)

```python
inline_source = {
    "type": "inline_user_conversation_simulation",
    "test_cases": [
        {
            "test_case_id": "refund-delay",
            "test_case_description": "A frustrated customer wants an update on a delayed refund.",
            "simulation_configuration": {
                "desired_num_turns": 6,
            },
        }
    ],
}

# In the run request:
# data_source={..., "source": inline_source}
```

# [C#](#tab/csharp)

```csharp
object inlineSource = new
{
  type = "inline_user_conversation_simulation",
  test_cases = new[]
  {
    new
    {
      test_case_id = "refund-delay",
      test_case_description =
        "A frustrated customer wants an update on a delayed refund.",
      simulation_configuration = new { desired_num_turns = 6 }
    }
  }
};

// In the run request:
// data_source = new { ..., source = inlineSource }
```

# [JavaScript/TypeScript](#tab/javascript)

```typescript
const inlineSource = {
  type: "inline_user_conversation_simulation",
  test_cases: [
    {
      test_case_id: "refund-delay",
      test_case_description:
        "A frustrated customer wants an update on a delayed refund.",
      simulation_configuration: {
        desired_num_turns: 6,
      },
    },
  ],
};

// In the run request:
// data_source: { ...dataSource, source: inlineSource }
```

# [cURL](#tab/curl)

```json
{
  "source": {
    "type": "inline_user_conversation_simulation",
    "test_cases": [
      {
        "test_case_id": "refund-delay",
        "test_case_description": "A frustrated customer wants an update on a delayed refund.",
        "simulation_configuration": {
          "desired_num_turns": 6
        }
      }
    ]
  }
}
```

---

## Get generated conversations

Poll the run until it reaches a terminal state as described in [Get cloud evaluation results](cloud-evaluation-results.md). When `enable_conversation_dataset_generation` is `true`, a completed run includes an `output_datasets` entry like this one:

```json
{
  "type": "simulated_user_conversations",
  "dataset": {
    "id": "dataset_123",
    "name": "support-simulations",
    "version": "1"
  }
}
```

Use the returned dataset `id`, `name`, and `version` to retrieve or reuse the generated conversations. If dataset generation is disabled, `output_datasets` is omitted.

---

## Next steps

- To poll for completion and interpret results, see [Get cloud evaluation results](cloud-evaluation-results.md).
- For a complete runnable example, see [sample_multiturn_conversation_simulation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_multiturn_conversation_simulation.py) on GitHub.
- To evaluate stored conversations, see [Evaluate conversation datasets](cloud-evaluation-conversations.md).
- To evaluate production traces, see [Evaluate deployed model and agent conversations](cloud-evaluation-deployed-conversations.md).
