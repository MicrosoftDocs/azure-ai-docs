---
title: "Make your hosted agent optimization-ready in Foundry Agent Service (preview)"
description: "Add four lines of code to your hosted agent to enable automatic optimization of system instructions and skills in Foundry Agent Service."
author: aahill
ms.author: aahi
ms.date: 05/18/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Make your agent optimization-ready (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Adding optimization support to your agent requires **four lines of code**. No framework changes or conditional logic are needed. Call `load_config()` and use its values.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with a deployed hosted agent
- Familiarity with [hosted agents](../concepts/hosted-agents.md)
- Python 3.9 or later

## Add the `agent_optimization` package

Your project needs the `agent_optimization/` package. If you started from the [FAOS template](https://github.com/microsoft/faos-pri-preview), it's already included. Otherwise, copy the `agent_optimization/` directory from the [sample repository](https://github.com/microsoft/faos-pri-preview/tree/main/agent_optimization) into your project root.

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

## Import and call `load_config()`

Add this near the top of your `main.py`:

```python
from agent_optimization import load_config

config = load_config(
    default_instructions="You are a helpful assistant.",
    default_model="gpt-4.1-mini",
)
```

The `load_config()` function resolves the active configuration at startup and returns an `OptimizationConfig` object. When no optimization is active, it returns your defaults and the agent behaves normally.

**Parameters:**

| Parameter | Type | Description |
| ----------- | ------ | ------------- |
| `default_instructions` | `str` | Your current system prompt. Used when not under optimization. |
| `default_model` | `str \| None` | Default model deployment name |
| `default_temperature` | `float \| None` | Default temperature (optional) |
| `default_skills_dir` | `str \| None` | Directory for skill files (optional) |

**`OptimizationConfig` fields:**

| Field | Type | Description |
| ------- | ------ | ------------- |
| `instructions` | `str` | System prompt (optimized or default) |
| `model` | `str \| None` | Model deployment name |
| `temperature` | `float \| None` | Sampling temperature |
| `skills` | `list[Skill]` | Discovered skills (empty if none) |
| `source` | `str` | Where the config came from: `"defaults"`, `"env:..."`, or `"api:candidate:..."` |

## Use the config values

Use `config.model` and `config.compose_instructions()` when calling the model:

```python
MODEL = config.model or "gpt-4.1-mini"
INSTRUCTIONS = config.compose_instructions()
```

The `compose_instructions()` method returns the system prompt with any discovered skills appended as a skill catalog.

## Log the config source (recommended)

Add a log line to confirm where the config came from:

```python
import logging

logger = logging.getLogger("my-agent")
logger.info("Config loaded (source=%s, model=%s)", config.source, MODEL)
```

## Complete example

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

## How it works

1. **Normal operation**: No optimization environment variables are set. `load_config()` returns your defaults. The agent works exactly as before.

1. **During optimization**: The service sets `AGENT_OPTIMIZATION_CANDIDATE_ID`. `load_config()` calls the resolver API to fetch the candidate's configuration. Your agent uses the candidate's instructions.

1. **After deploying a winner**: The `azd ai agent optimize deploy` command sets `OPTIMIZATION_CONFIG` in the agent's environment. `load_config()` reads the JSON and your agent uses the optimized instructions permanently.

Your code never changes between these states. The config resolution is fully automatic.

## Verify

Confirm that the package is importable and the configuration loads correctly:

```bash
# Verify the package is importable
python -c "from agent_optimization import load_config; print('OK')"

# Run locally and check the log output
azd ai agent run
# Expected log: "Config loaded (source=defaults, model=gpt-4.1-mini)"
```

## Related content

- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
- [Create a custom evaluation dataset](create-optimization-dataset.md)
- [Optimize agent instructions and skills](optimize-agent-strategies.md)
- [Agent optimization overview](../concepts/agent-optimization-overview.md)
