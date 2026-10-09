---
title: "Generate and evaluate synthetic conversations"
description: "Use the Microsoft Foundry SDK to generate scenarios, simulate multi-turn agent conversations, and evaluate the conversations."
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom:
  - references_regions
ms.topic: how-to
ms.date: 09/30/2026
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
# customer intent: As a developer, I want to generate and evaluate synthetic conversations so that I can test an agent without hand-authoring scenarios.
---

# Generate and evaluate synthetic conversations

Generate test scenarios from one or more agent, prompt, or reference-file sources, simulate multi-turn conversations against the agent, and evaluate the conversations in one evaluation run. Use this workflow when you don't have hand-authored scenarios or representative conversation data.

To provide your own scenarios instead, see [Simulate conversations with the Microsoft Foundry SDK](cloud-evaluation-simulate-conversations.md).

## Prerequisites

- Complete the [cloud evaluation prerequisites](cloud-evaluation.md#prerequisites) and [client setup](cloud-evaluation.md#set-up-the-sdk-client).
- Install the packages for your language:
  - Python: `pip install "azure-ai-projects>=2.5.0" python-dotenv`
  - C#: `dotnet add package Azure.AI.Projects --prerelease` and `dotnet add package Azure.Identity`
  - JavaScript: `npm install @azure/ai-projects @azure/identity dotenv`
- Deploy a model to generate scenarios, simulate users, and run AI-assisted evaluators.

Set these environment variables:

- `FOUNDRY_PROJECT_ENDPOINT`: Your Foundry project endpoint.
- `FOUNDRY_MODEL_NAME`: The model deployment used for scenario generation, user simulation, and AI-assisted evaluators.
- `FOUNDRY_AGENT_NAME`: Optional. The agent name. The example uses `MyAgent` when this variable isn't set.

## How synthetic conversation evaluation works

The `azure_ai_synthetic_data_generation_with_simulation` data source runs the complete workflow:

1. Generate test-case scenarios from one or more agent, prompt, or reference-file sources.
1. Save the generated scenarios as a dataset.
1. Simulate multi-turn conversations against the agent.
1. Save the generated conversations as a dataset.
1. Evaluate the conversations with conversation-level evaluators.

Generation and simulation happen in the same evaluation run. You don't need to create a separate synthetic-data generation job.

The `generation_sources` array accepts multiple sources in one job. Combining sources can produce broader scenario coverage. For example, use an agent definition to reflect the agent's instructions and persona, a prompt to steer scenario difficulty or domain, and a reference file to ground scenarios in longer source material. All generated scenarios feed the same multi-turn conversation simulation step.

You can combine these source types:

- **Agent definition** (`"type": "agent"`): Uses a deployed agent's name, version, and instructions.
- **Prompt** (`"type": "prompt"`): Uses inline text to describe the domain or steer the generated scenarios.
- **Reference file** (`"type": "file"`): Uses an uploaded file ID to ground scenarios in source material.

## Configure the client and agent

Create a project client and an agent to evaluate:

# [Python](#tab/python)

```python
import os
import time
from pprint import pprint

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AzureAIDataSourceConfig,
    PromptAgentDefinition,
    TestingCriterionAzureAIEvaluator,
)

SEED_COUNT = 1
CONVERSATIONS_PER_SEED = 1
MAX_TURNS = 2
DESIRED_TURNS = 1

load_dotenv()

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
model_deployment_name = os.environ["FOUNDRY_MODEL_NAME"]
agent_name = os.environ.get("FOUNDRY_AGENT_NAME", "MyAgent")

credential = DefaultAzureCredential()
project_client = AIProjectClient(endpoint=endpoint, credential=credential)
client = project_client.get_openai_client()

agent = project_client.agents.create_version(
    agent_name=agent_name,
    definition=PromptAgentDefinition(
        model=model_deployment_name,
        instructions="You are a helpful customer service agent. Be empathetic and solution-oriented.",
    ),
)
```

# [C#](#tab/csharp)

```csharp
using System.ClientModel;
using System.Text.Json;
using Azure.AI.Extensions.OpenAI;
using Azure.AI.Projects;
using Azure.AI.Projects.Agents;
using Azure.Identity;
using OpenAI.Evals;

#pragma warning disable OPENAI001

static string GetString(ClientResult result, string propertyName)
{
    using JsonDocument document = JsonDocument.Parse(
        result.GetRawResponse().Content.ToMemory());
    return document.RootElement.GetProperty(propertyName).GetString()
        ?? throw new InvalidOperationException(
            $"The response doesn't contain {propertyName}.");
}

const int SeedCount = 1;
const int ConversationsPerSeed = 1;
const int MaxTurns = 2;
const int DesiredTurns = 1;

var endpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException(
        "FOUNDRY_PROJECT_ENDPOINT isn't set.");
var modelDeploymentName = Environment.GetEnvironmentVariable(
    "FOUNDRY_MODEL_NAME")
    ?? throw new InvalidOperationException("FOUNDRY_MODEL_NAME isn't set.");
var agentName = Environment.GetEnvironmentVariable("FOUNDRY_AGENT_NAME")
    ?? "MyAgent";

AIProjectClient projectClient = new(
    endpoint: new Uri(endpoint),
    tokenProvider: new DefaultAzureCredential());
EvaluationClient evaluationClient = projectClient.ProjectOpenAIClient
    .GetEvaluationClient();

DeclarativeAgentDefinition agentDefinition = new(modelDeploymentName)
{
    Instructions =
        "You are a helpful customer service agent. Be empathetic and solution-oriented."
};
ProjectsAgentVersion agent = await projectClient.AgentAdministrationClient
    .CreateAgentVersionAsync(
        agentName: agentName,
        options: new(agentDefinition));
```

# [JavaScript/TypeScript](#tab/javascript)

```typescript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";
import "dotenv/config";

const SEED_COUNT = 1;
const CONVERSATIONS_PER_SEED = 1;
const MAX_TURNS = 2;
const DESIRED_TURNS = 1;

const endpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "";
const modelDeploymentName = process.env["FOUNDRY_MODEL_NAME"] || "";
const agentName = process.env["FOUNDRY_AGENT_NAME"] || "MyAgent";

const projectClient = new AIProjectClient(
  endpoint,
  new DefaultAzureCredential(),
);
const openAIClient = projectClient.getOpenAIClient();

const agent = await projectClient.agents.createVersion(agentName, {
  kind: "prompt",
  model: modelDeploymentName,
  instructions:
    "You are a helpful customer service agent. Be empathetic and solution-oriented.",
});
```

---

## Configure the evaluation

Use the `synthetic_data_gen` scenario for the evaluation group. Conversation-level evaluators receive the generated conversation through `{{item.messages}}`. Evaluators that assess tool use also receive `{{item.tool_definitions}}`.

# [Python](#tab/python)

```python
data_source_config = AzureAIDataSourceConfig(
    type="azure_ai_source",
    scenario="synthetic_data_gen",
)

testing_criteria = [
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="tool_use_quality",
        evaluator_name="builtin.tool_use_quality",
        initialization_parameters={"model": model_deployment_name},
        data_mapping={
            "messages": "{{item.messages}}",
            "tool_definitions": "{{item.tool_definitions}}",
        },
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="output_quality",
        evaluator_name="builtin.output_quality",
        initialization_parameters={"model": model_deployment_name},
        data_mapping={
            "messages": "{{item.messages}}",
            "tool_definitions": "{{item.tool_definitions}}",
        },
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="deflection_rate",
        evaluator_name="builtin.deflection_rate",
        initialization_parameters={"model": model_deployment_name},
        data_mapping={
            "messages": "{{item.messages}}",
            "tool_definitions": "{{item.tool_definitions}}",
        },
    ),
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
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="coherence",
        evaluator_name="builtin.coherence",
        initialization_parameters={"model": model_deployment_name},
        data_mapping={"messages": "{{item.messages}}"},
    ),
    TestingCriterionAzureAIEvaluator(
        type="azure_ai_evaluator",
        name="groundedness",
        evaluator_name="builtin.groundedness",
        initialization_parameters={"model": model_deployment_name},
        data_mapping={"messages": "{{item.messages}}"},
    ),
]

eval_object = client.evals.create(
    name="Synthetic Multi-turn Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)
```

# [C#](#tab/csharp)

```csharp
object dataSourceConfig = new
{
    type = "azure_ai_source",
    scenario = "synthetic_data_gen"
};

object[] testingCriteria =
[
    new
    {
        type = "azure_ai_evaluator",
        name = "tool_use_quality",
        evaluator_name = "builtin.tool_use_quality",
        initialization_parameters = new { model = modelDeploymentName },
        data_mapping = new
        {
            messages = "{{item.messages}}",
            tool_definitions = "{{item.tool_definitions}}"
        }
    },
    new
    {
        type = "azure_ai_evaluator",
        name = "output_quality",
        evaluator_name = "builtin.output_quality",
        initialization_parameters = new { model = modelDeploymentName },
        data_mapping = new
        {
            messages = "{{item.messages}}",
            tool_definitions = "{{item.tool_definitions}}"
        }
    },
    new
    {
        type = "azure_ai_evaluator",
        name = "deflection_rate",
        evaluator_name = "builtin.deflection_rate",
        initialization_parameters = new { model = modelDeploymentName },
        data_mapping = new
        {
            messages = "{{item.messages}}",
            tool_definitions = "{{item.tool_definitions}}"
        }
    },
    new
    {
        type = "azure_ai_evaluator",
        name = "customer_satisfaction",
        evaluator_name = "builtin.customer_satisfaction",
        initialization_parameters = new { model = modelDeploymentName },
        data_mapping = new { messages = "{{item.messages}}" }
    },
    new
    {
        type = "azure_ai_evaluator",
        name = "task_completion",
        evaluator_name = "builtin.task_completion",
        initialization_parameters = new { model = modelDeploymentName },
        data_mapping = new { messages = "{{item.messages}}" }
    },
    new
    {
        type = "azure_ai_evaluator",
        name = "coherence",
        evaluator_name = "builtin.coherence",
        initialization_parameters = new { model = modelDeploymentName },
        data_mapping = new { messages = "{{item.messages}}" }
    },
    new
    {
        type = "azure_ai_evaluator",
        name = "groundedness",
        evaluator_name = "builtin.groundedness",
        initialization_parameters = new { model = modelDeploymentName },
        data_mapping = new { messages = "{{item.messages}}" }
    }
];

BinaryData evaluationData = BinaryData.FromObjectAsJson(new
{
    name = "Synthetic Multi-turn Evaluation",
    data_source_config = dataSourceConfig,
    testing_criteria = testingCriteria
});
using BinaryContent evaluationContent = BinaryContent.Create(evaluationData);
ClientResult evaluation = await evaluationClient.CreateEvaluationAsync(
    evaluationContent);
string evaluationId = GetString(evaluation, "id");
```

# [JavaScript/TypeScript](#tab/javascript)

```typescript
const dataSourceConfig = {
  type: "azure_ai_source",
  scenario: "synthetic_data_gen",
};

const testingCriteria = [
  {
    type: "azure_ai_evaluator",
    name: "tool_use_quality",
    evaluator_name: "builtin.tool_use_quality",
    initialization_parameters: { model: modelDeploymentName },
    data_mapping: {
      messages: "{{item.messages}}",
      tool_definitions: "{{item.tool_definitions}}",
    },
  },
  {
    type: "azure_ai_evaluator",
    name: "output_quality",
    evaluator_name: "builtin.output_quality",
    initialization_parameters: { model: modelDeploymentName },
    data_mapping: {
      messages: "{{item.messages}}",
      tool_definitions: "{{item.tool_definitions}}",
    },
  },
  {
    type: "azure_ai_evaluator",
    name: "deflection_rate",
    evaluator_name: "builtin.deflection_rate",
    initialization_parameters: { model: modelDeploymentName },
    data_mapping: {
      messages: "{{item.messages}}",
      tool_definitions: "{{item.tool_definitions}}",
    },
  },
  {
    type: "azure_ai_evaluator",
    name: "customer_satisfaction",
    evaluator_name: "builtin.customer_satisfaction",
    initialization_parameters: { model: modelDeploymentName },
    data_mapping: { messages: "{{item.messages}}" },
  },
  {
    type: "azure_ai_evaluator",
    name: "task_completion",
    evaluator_name: "builtin.task_completion",
    initialization_parameters: { model: modelDeploymentName },
    data_mapping: { messages: "{{item.messages}}" },
  },
  {
    type: "azure_ai_evaluator",
    name: "coherence",
    evaluator_name: "builtin.coherence",
    initialization_parameters: { model: modelDeploymentName },
    data_mapping: { messages: "{{item.messages}}" },
  },
  {
    type: "azure_ai_evaluator",
    name: "groundedness",
    evaluator_name: "builtin.groundedness",
    initialization_parameters: { model: modelDeploymentName },
    data_mapping: { messages: "{{item.messages}}" },
  },
];

const evalObject = await openAIClient.evals.create({
  name: "Synthetic Multi-turn Evaluation",
  data_source_config: dataSourceConfig as any,
  testing_criteria: testingCriteria as any,
});
```

---

## Generate, simulate, and evaluate

Create one run with the `azure_ai_synthetic_data_generation_with_simulation` data source:

# [Python](#tab/python)

```python
eval_run = client.evals.runs.create(
    eval_id=eval_object.id,
    name="synthetic-multiturn-run",
    data_source={
        "type": "azure_ai_synthetic_data_generation_with_simulation",
        "synthetic_data_generation_configuration": {
            "test_case_count": SEED_COUNT,
            "output_test_case_dataset_name": f"{agent_name}-synthetic-scenarios",
            "generation_sources": [
                {
                    "type": "prompt",
                    "prompt": (
                        "Generate customer-support scenarios that test difficult "
                        "billing and refund conversations."
                    ),
                },
                {
                    "type": "agent",
                    "agent_name": agent.name,
                    "agent_version": agent.version,
                },
            ],
        },
        "model_configuration": {
            "model": model_deployment_name,
        },
        "default_simulation_configuration": {
            "max_num_turns": MAX_TURNS,
            "conversation_repetitions": CONVERSATIONS_PER_SEED,
            "desired_num_turns": DESIRED_TURNS,
            "enable_conversation_dataset_generation": True,
            "output_conversation_dataset_name": f"{agent_name}-synthetic-conversations",
        },
        "target": {
            "type": "azure_ai_agent",
            "name": agent.name,
            "version": agent.version,
        },
    },
    extra_body={"evaluation_level": "conversation"},
)
```

# [C#](#tab/csharp)

```csharp
BinaryData runData = BinaryData.FromObjectAsJson(new
{
    name = "synthetic-multiturn-run",
    evaluation_level = "conversation",
    data_source = new
    {
        type = "azure_ai_synthetic_data_generation_with_simulation",
        synthetic_data_generation_configuration = new
        {
            test_case_count = SeedCount,
            output_test_case_dataset_name =
                $"{agentName}-synthetic-scenarios",
            generation_sources = new object[]
            {
                new
                {
                    type = "prompt",
                    prompt =
                        "Generate customer-support scenarios that test difficult billing and refund conversations."
                },
                new
                {
                    type = "agent",
                    agent_name = agent.Name,
                    agent_version = agent.Version
                }
            }
        },
        model_configuration = new
        {
            model = modelDeploymentName
        },
        default_simulation_configuration = new
        {
            max_num_turns = MaxTurns,
            conversation_repetitions = ConversationsPerSeed,
            desired_num_turns = DesiredTurns,
            enable_conversation_dataset_generation = true,
            output_conversation_dataset_name =
                $"{agentName}-synthetic-conversations"
        },
        target = new
        {
            type = "azure_ai_agent",
            name = agent.Name,
            version = agent.Version
        }
    }
});
using BinaryContent runContent = BinaryContent.Create(runData);
ClientResult evaluationRun = await evaluationClient.CreateEvaluationRunAsync(
    evaluationId: evaluationId,
    content: runContent);
string runId = GetString(evaluationRun, "id");
```

# [JavaScript/TypeScript](#tab/javascript)

```typescript
const evalRun = await openAIClient.evals.runs.create(evalObject.id, {
  name: "synthetic-multiturn-run",
  evaluation_level: "conversation",
  data_source: {
    type: "azure_ai_synthetic_data_generation_with_simulation",
    synthetic_data_generation_configuration: {
      test_case_count: SEED_COUNT,
      output_test_case_dataset_name: `${agentName}-synthetic-scenarios`,
      generation_sources: [
        {
          type: "prompt",
          prompt:
            "Generate customer-support scenarios that test difficult billing and refund conversations.",
        },
        {
          type: "agent",
          agent_name: agent.name,
          agent_version: agent.version,
        },
      ],
    },
    model_configuration: {
      model: modelDeploymentName,
    },
    default_simulation_configuration: {
      max_num_turns: MAX_TURNS,
      conversation_repetitions: CONVERSATIONS_PER_SEED,
      desired_num_turns: DESIRED_TURNS,
      enable_conversation_dataset_generation: true,
      output_conversation_dataset_name:
        `${agentName}-synthetic-conversations`,
    },
    target: {
      type: "azure_ai_agent",
      name: agent.name,
      version: agent.version,
    },
  },
} as any);
```

---

> [!NOTE]
> `output_test_case_dataset_name` and `output_conversation_dataset_name` are optional. Specify them when you want recognizable dataset names; otherwise, omit them and the service generates the names.
>
> The OpenAI clients' typed methods don't currently expose all Azure-specific evaluation properties. Python uses `extra_body` to add `evaluation_level` to the top level of the REST request body. The TypeScript sample uses `as any` for the Azure-specific evaluation configuration, criteria, data source, and `evaluation_level`; the client forwards these properties to the service. C# sets the properties directly in its protocol request body.

The configuration uses these parameters:

| Parameter | Description |
|-----------|-------------|
| `test_case_count` | Number of synthetic scenarios to generate. |
| `generation_sources` | One or more agent, prompt, or reference-file sources used together to generate scenarios. This example combines a steering prompt with the agent's name, version, and instructions. |
| `output_test_case_dataset_name` | Optional name for the dataset that stores the generated scenarios. If omitted, the service generates the name. |
| `model_configuration.model` | Model deployment used to generate scenarios and simulate the user. |
| `max_num_turns` | Maximum number of turns in each conversation. |
| `conversation_repetitions` | Conversations to simulate for each generated scenario. |
| `desired_num_turns` | Preferred number of turns in each conversation. |
| `enable_conversation_dataset_generation` | Whether to save the simulated conversations as a dataset. |
| `output_conversation_dataset_name` | Optional name for the dataset that stores the generated conversations. If omitted, the service generates the name. |

## Get the results

Synthetic conversation runs can take several minutes. Poll until the run reaches a terminal state, then inspect its output items and report URL:

# [Python](#tab/python)

```python
while True:
    run = client.evals.runs.retrieve(
        run_id=eval_run.id,
        eval_id=eval_object.id,
    )
    if run.status in ("completed", "failed", "canceled"):
        break
    print(f"Waiting for simulation to complete... current status: {run.status}")
    time.sleep(10)

if run.status != "completed":
    raise RuntimeError(f"Simulation run failed: {run.error}")

print(f"Result Counts: {run.result_counts}")
if run.result_counts.errored:
    raise RuntimeError(
        f"{run.result_counts.errored} evaluation item(s) errored"
    )

expected_conversations = SEED_COUNT * CONVERSATIONS_PER_SEED
print(f"Expected up to: {expected_conversations} conversations")

output_items = list(
    client.evals.runs.output_items.list(
        run_id=run.id,
        eval_id=eval_object.id,
    )
)

if output_items:
    pprint(output_items[0])

print(f"Eval Run Report URL: {run.report_url}")
```

Delete the evaluation when you no longer need it:

```python
client.evals.delete(eval_id=eval_object.id)
client.close()
project_client.close()
credential.close()
```

# [C#](#tab/csharp)

```csharp
string runStatus = GetString(evaluationRun, "status");

while (runStatus != "completed"
    && runStatus != "failed"
    && runStatus != "canceled")
{
    await Task.Delay(TimeSpan.FromSeconds(10));
    evaluationRun = await evaluationClient.GetEvaluationRunAsync(
        evaluationId: evaluationId,
        evaluationRunId: runId,
        options: new());
    runStatus = GetString(evaluationRun, "status");
    Console.WriteLine(
        $"Waiting for simulation to complete... current status: {runStatus}");
}

if (runStatus != "completed")
{
    throw new InvalidOperationException(
        evaluationRun.GetRawResponse().Content.ToString());
}

using JsonDocument runDocument = JsonDocument.Parse(
    evaluationRun.GetRawResponse().Content.ToMemory());
JsonElement resultCounts = runDocument.RootElement.GetProperty(
    "result_counts");
Console.WriteLine($"Result Counts: {resultCounts}");

int errored = resultCounts.GetProperty("errored").GetInt32();
if (errored > 0)
{
    throw new InvalidOperationException(
        $"{errored} evaluation item(s) errored");
}

int expectedConversations = SeedCount * ConversationsPerSeed;
Console.WriteLine(
    $"Expected up to: {expectedConversations} conversations");

ClientResult outputItems = await evaluationClient
    .GetEvaluationRunOutputItemsAsync(
        evaluationId: evaluationId,
        evaluationRunId: runId,
        limit: 1,
        order: "asc",
        after: null,
        outputItemStatus: null,
        options: new());
using JsonDocument outputDocument = JsonDocument.Parse(
    outputItems.GetRawResponse().Content.ToMemory());
JsonElement firstPage = outputDocument.RootElement.GetProperty("data");
if (firstPage.GetArrayLength() > 0)
{
    Console.WriteLine(firstPage[0]);
}

Console.WriteLine(
    $"Eval Run Report URL: {GetString(evaluationRun, "report_url")}");

await evaluationClient.DeleteEvaluationAsync(
    evaluationId: evaluationId,
    options: new());
```

# [JavaScript/TypeScript](#tab/javascript)

```typescript
let run = evalRun;
while (!["completed", "failed", "canceled"].includes(run.status)) {
  run = await openAIClient.evals.runs.retrieve(run.id, {
    eval_id: evalObject.id,
  });
  console.log(
    `Waiting for simulation to complete... current status: ${run.status}`,
  );
  await new Promise((resolve) => setTimeout(resolve, 10000));
}

if (run.status !== "completed") {
  throw new Error(`Simulation run ended in ${run.status}`);
}

console.log("Result Counts:", run.result_counts);
if (run.result_counts.errored > 0) {
  throw new Error(
    `${run.result_counts.errored} evaluation item(s) errored`,
  );
}

const expectedConversations = SEED_COUNT * CONVERSATIONS_PER_SEED;
console.log(`Expected up to: ${expectedConversations} conversations`);

for await (const item of openAIClient.evals.runs.outputItems.list(run.id, {
  eval_id: evalObject.id,
  limit: 1,
})) {
  console.log(JSON.stringify(item, null, 2));
  break;
}

console.log(`Eval Run Report URL: ${run.report_url}`);

await openAIClient.evals.delete(evalObject.id);
```

---

## Next steps

- For the complete runnable and recorded example, see [sample_synthetic_multiturn_evaluation.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/sample_synthetic_multiturn_evaluation.py).
- For the complete JavaScript/TypeScript example, see [syntheticMultiturnEvaluation.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples-dev/evaluations/syntheticMultiturnEvaluation.ts).
- To provide your own scenario dataset, see [Simulate conversations with the Microsoft Foundry SDK](cloud-evaluation-simulate-conversations.md).
- To interpret evaluation results, see [Get cloud evaluation results](cloud-evaluation-results.md).
