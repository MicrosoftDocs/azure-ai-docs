---
title: "Make your hosted agent optimizer-ready in Foundry Agent Service (preview)"
description: "Add four lines of code to your hosted agent to enable the agent optimizer for automatic improvement of system instructions and skills in Foundry Agent Service."
author: aahill
ms.author: aahi
ms.date: 05/18/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Make your agent optimizer-ready (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Adding support for the agent optimizer to your agent requires a few lines of code. No framework changes or conditional logic are needed. Load the optimization config at startup and use its values.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with a deployed hosted agent
- Familiarity with [hosted agents](../concepts/hosted-agents.md)

# [Python](#tab/python)

- Python 3.9 or later

# [C#](#tab/csharp)

- .NET 8 or later

---

## Add the optimization config package

Your project needs the optimization config package. If you started from the [agent optimizer template](https://github.com/microsoft/faos-pri-preview), it's already included. Otherwise, copy the directory from the [sample repository](https://github.com/microsoft/faos-pri-preview/tree/main/samples) into your project root.

# [Python](#tab/python)

```
my-agent/
├── main.py
├── agent.yaml
├── azure.yaml
├── requirements.txt
└── agent_optimization/
    ├── __init__.py
    ├── _config.py
    └── _resolver.py
```

The package has no extra dependencies beyond `azure-identity` (which you already have for Foundry agents).

# [C#](#tab/csharp)

```
my-agent/
├── Program.cs
├── MyAgent.csproj
├── agent.yaml
├── azure.yaml
├── Dockerfile
└── AgentOptimization/
    ├── OptimizationConfigLoader.cs
    └── CandidateResolver.cs
```

The `AgentOptimization` namespace has no extra dependencies beyond `Azure.Identity` and `System.Text.Json`.

---

## Load the optimization config

Add the config loader near the top of your entry point:

# [Python](#tab/python)

```python
from agent_optimization import load_config

config = load_config(
    default_instructions="You are a helpful assistant.",
    default_model="gpt-4.1-mini",
)
```

# [C#](#tab/csharp)

```csharp
using AgentOptimization;

var config = OptimizationConfigLoader.LoadConfig(
    defaultInstructions: "You are a helpful assistant.",
    defaultModel: "gpt-4.1-mini"
);
```

---

The function resolves the active configuration at startup and returns an `OptimizationConfig` object. When no optimization is active, it returns your defaults and the agent behaves normally.

**Parameters:**

| Parameter | Python | C# | Description |
| ----------- | -------- | ---- | ------------- |
| Default instructions | `default_instructions` | `defaultInstructions` | Your current system prompt. Used when not under optimization. |
| Default model | `default_model` | `defaultModel` | Default model deployment name |
| Default temperature | `default_temperature` | `defaultTemperature` | Default temperature (optional) |
| Default skills dir | `default_skills_dir` | `defaultSkillsDir` | Directory for skill files (optional) |

**`OptimizationConfig` fields:**

| Description | Python | C# | Type |
| ------------- | -------- | ---- | ------ |
| System prompt (optimized or default) | `instructions` | `Instructions` | `str` / `string` |
| Model deployment name | `model` | `Model` | `str?` / `string?` |
| Sampling temperature | `temperature` | `Temperature` | `float?` / `double?` |
| Discovered skills (empty if none) | `skills` | `Skills` | `list[Skill]` / `List<Skill>` |
| Config source | `source` | `Source` | `str` / `string` |

## Use the config values

Use the model and composed instructions when calling the model:

# [Python](#tab/python)

```python
MODEL = config.model or "gpt-4.1-mini"
INSTRUCTIONS = config.compose_instructions()
```

# [C#](#tab/csharp)

```csharp
var modelName = config.Model ?? "gpt-4.1-mini";
var instructions = config.ComposeInstructions();
```

---

The `compose_instructions()` / `ComposeInstructions()` method returns the system prompt with any discovered skills appended as a skill catalog.

## Log the config source (recommended)

Add a log line to confirm where the config came from:

# [Python](#tab/python)

```python
import logging

logger = logging.getLogger("my-agent")
logger.info("Config loaded (source=%s, model=%s)", config.source, MODEL)
```

# [C#](#tab/csharp)

```csharp
Console.WriteLine($"[INFO] Config loaded (source={config.Source}, model={modelName})");
```

---

## Complete example

# [Python](#tab/python)

```python
import asyncio
import logging
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agentserver.responses import (
    CreateResponse, ResponseContext,
    ResponsesAgentServerHost, ResponsesServerOptions, TextResponse,
)

from agent_optimization import load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my-agent")

# ── Config (optimization-ready) ──────────────────────────────────────
config = load_config(
    default_instructions="You are a helpful coding assistant.",
    default_model=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini"),
)
MODEL = config.model or "gpt-4.1-mini"
INSTRUCTIONS = config.compose_instructions()
logger.info("Config loaded (source=%s, model=%s)", config.source, MODEL)

# ── Foundry client ───────────────────────────────────────────────────
endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)


async def handle_response(
    request: CreateResponse, context: ResponseContext
) -> TextResponse:
    """Handle a single response request."""
    response = client.inference.get_chat_completions_client().complete(
        model=MODEL,
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": request.input},
        ],
    )
    return TextResponse(text=response.choices[0].message.content)


if __name__ == "__main__":
    host = ResponsesAgentServerHost(
        options=ResponsesServerOptions(),
        handler=handle_response,
    )
    asyncio.run(host.run())
```

# [C#](#tab/csharp)

```csharp
using Azure.AI.AgentServer.Responses;
using Azure.AI.AgentServer.Responses.Models;
using Azure.AI.Extensions.OpenAI;
using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Extensions.Logging;
using OpenAI.Responses;
using AgentOptimization;

// ── Config (optimization-ready) ──────────────────────────────────────
var defaultModel = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    ?? "gpt-4.1-mini";

var config = OptimizationConfigLoader.LoadConfig(
    defaultInstructions: "You are a helpful coding assistant.",
    defaultModel: defaultModel
);

var modelName = config.Model ?? defaultModel;
Console.WriteLine($"[INFO] Config loaded (source={config.Source}, model={modelName})");

// ── Start the Responses server ───────────────────────────────────────
ResponsesServer.Run<HelloWorldHandler>(configure: builder =>
{
    var endpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
        ?? Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT")
        ?? throw new InvalidOperationException(
            "FOUNDRY_PROJECT_ENDPOINT or AZURE_AI_PROJECT_ENDPOINT must be set.");

    var projectClient = new AIProjectClient(new Uri(endpoint), new DefaultAzureCredential());
    var responsesClient = projectClient.ProjectOpenAIClient
        .GetProjectResponsesClientForModel(modelName);

    builder.Services.AddSingleton(responsesClient);
    builder.Services.AddSingleton(config);
});

public sealed class HelloWorldHandler(
    ProjectResponsesClient responsesClient,
    OptimizationConfig config,
    ILogger<HelloWorldHandler> logger) : ResponseHandler
{
    public override IAsyncEnumerable<ResponseStreamEvent> CreateAsync(
        CreateResponse request,
        ResponseContext context,
        CancellationToken cancellationToken)
    {
        return new TextResponse(context, request,
            createText: ct => GenerateTextAsync(context, ct));
    }

    private async Task<string> GenerateTextAsync(
        ResponseContext context,
        CancellationToken cancellationToken)
    {
        var userInput = await context.GetInputTextAsync(
            cancellationToken: cancellationToken) ?? "Hello!";

        logger.LogInformation("Processing request {ResponseId} (source={Source})",
            context.ResponseId, config.Source);

        var options = new CreateResponseOptions
        {
            Instructions = config.ComposeInstructions(),
        };

        options.InputItems.Add(ResponseItem.CreateUserMessageItem(userInput));

        var result = await responsesClient.CreateResponseAsync(options);
        return result.Value.GetOutputText() ?? string.Empty;
    }
}
```

---

## How it works

1. **Normal operation**: No optimization environment variables are set. The config loader returns your defaults. The agent works exactly as before.

1. **During optimization**: The agent optimizer sets `OPTIMIZATION_CANDIDATE_ID`. The config loader calls the resolver API to fetch the candidate's configuration. Your agent uses the candidate's instructions.

1. **After deploying a winner**: The `azd ai agent optimize deploy` command sets `OPTIMIZATION_CONFIG` in the agent's environment. The config loader reads the JSON and your agent uses the optimized instructions permanently.

Your code never changes between these states. The config resolution is fully automatic.

## Verify

Confirm that the package is importable and the configuration loads correctly:

# [Python](#tab/python)

```bash
# Verify the package is importable
python -c "from agent_optimization import load_config; print('OK')"

# Run locally and check the log output
azd ai agent run
# Expected log: "Config loaded (source=defaults, model=gpt-4.1-mini)"
```

# [C#](#tab/csharp)

```bash
# Build to verify the package compiles
dotnet build

# Run locally and check the log output
azd ai agent run
# Expected log: "[INFO] Config loaded (source=defaults, model=gpt-4.1-mini)"
```

---

## Related content

- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
- [Create a custom evaluation dataset](create-optimizer-dataset.md)
- [Optimize agent instructions and skills](optimize-agent-targets.md)
- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
