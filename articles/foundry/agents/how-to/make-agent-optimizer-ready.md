---
title: "Make your hosted agent optimizer-ready in Foundry Agent Service (preview)"
description: "Add a few lines of code to your hosted agent to enable the agent optimizer for automatic improvement of system instructions, tools, and skills in Foundry Agent Service."
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

Adding support for the agent optimizer to your agent requires a few lines of code. No framework changes or conditional logic are needed. You install the optimization package, set up a configuration directory, and call `load_config()` at startup.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with a deployed hosted agent
- Familiarity with [hosted agents](../concepts/hosted-agents.md)
- Python 3.10 or later

## Install the optimization package

Install the `azure-ai-agentserver-optimization` package:

```bash
pip install azure-ai-agentserver-optimization
```

This package is part of the `azure-ai-agentserver-*` family (alongside `azure-ai-agentserver-responses` and `azure-ai-agentserver-core`). It depends on `pyyaml`, `azure-core`, and `azure-identity`.

Add it to your `requirements.txt`:

```
azure-ai-agentserver-optimization>=1.0.0b1
```

## Set up the configuration directory

Create the `.agent_configs/baseline/` directory at your project root. This directory defines your agent's baseline configuration — the starting point that the optimizer reads and improves upon.

```
my-agent/
├── main.py
├── agent.yaml
├── azure.yaml
├── requirements.txt
└── .agent_configs/
    ├── baseline/              ← your starting config
    │   ├── metadata.yaml
    │   ├── instructions.md
    │   ├── tools.json
    │   └── skills/
    │       └── (initially empty)
    └── <candidate_id>/        ← created by 'azd ai agent optimize apply'
        └── (same layout as baseline/)
```

### metadata.yaml

The metadata file tells the optimization loader where to find configuration files and which model to use:

```yaml
model: gpt-4.1-mini
instruction_file: instructions.md
tools_file: tools.json
skill_dir: skills
```

| Field | Required | Description |
|-------|----------|-------------|
| `model` | Yes | The model deployment name (for example, `gpt-4.1-mini`, `gpt-5.1`) |
| `instruction_file` | Yes | Relative path to the system prompt file |
| `tools_file` | No | Relative path to the tool definitions JSON file |
| `skill_dir` | No | Relative path to the skills directory |
| `temperature` | No | Model temperature for generation |

### instructions.md

Your agent's system prompt. Write it as plain text or markdown:

```markdown
You are a travel approval agent for Contoso Ltd. You review travel
requests and enforce company travel policy. Check travel policy limits,
department budget, and suggest cheaper alternatives when appropriate.
Enforce policy rules strictly — do not auto-approve everything.
```

The optimizer improves this prompt during optimization runs. After you apply an optimized candidate, this file contains the improved version.

### tools.json

Declare the tools your agent can call using the [OpenAI function-calling format](https://platform.openai.com/docs/guides/function-calling):

```json
[
  {
    "type": "function",
    "function": {
      "name": "lookup_travel_policy",
      "description": "Look up the company travel policy rules and limits.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_flight_alternatives",
      "description": "Find cheaper flight alternatives for the given destination.",
      "parameters": {
        "type": "object",
        "properties": {
          "destination": {
            "type": "string",
            "description": "The travel destination city"
          }
        },
        "required": ["destination"]
      }
    }
  }
]
```

The optimizer can improve tool descriptions to help the model call tools more accurately. After optimization, you apply improved descriptions back into this file.

### skills/ (Agent Skills format)

Skills use the open [Agent Skills](https://agentskills.io) format. Each skill is a folder containing a `SKILL.md` file:

```
skills/
└── policy-reviewer/
    └── SKILL.md
```

A `SKILL.md` file has YAML frontmatter for metadata and markdown body for instructions:

```markdown
---
name: policy-reviewer
description: Reviews travel requests. Use when someone submits a travel request.
---

# Policy Reviewer Skill

When reviewing a travel request:
1. Check destination against restricted countries list
2. Verify trip cost is within department budget
3. Confirm travel dates don't conflict with blackout periods
4. Suggest alternatives if the request exceeds policy limits
```

The YAML frontmatter (`name` and `description`) enables progressive disclosure — the agent loads only metadata at startup, then activates the full skill instructions when a matching task is detected.

The optimizer can discover and create new skills during optimization. These skills are written to the `skills/` directory when you apply an optimized candidate.

Learn more about the Agent Skills format at [agentskills.io](https://agentskills.io).

## Load the optimization config

Add the config loader at the top of your agent's entry point:

```python
from azure.ai.agentserver.optimization import load_config

config = load_config()
```

The `load_config()` function reads from `.agent_configs/` (either a candidate directory if `OPTIMIZATION_CANDIDATE_ID` is set, or `baseline/` otherwise) and returns an `OptimizationConfig` object. When no optimization candidate is active, it returns your baseline configuration.

**Parameters:**

| Parameter | Description |
|-----------|-------------|
| `config_dir` | Custom config directory path (defaults to `.agent_configs/`) |
| `required` | If `False`, returns `None` instead of raising when no config is found (default: `True`) |

**`OptimizationConfig` fields:**

| Field | Type | Description |
|-------|------|-------------|
| `instructions` | `str` | System prompt (optimized or baseline) |
| `model` | `str` | Model deployment name |
| `temperature` | `float` | Sampling temperature |
| `skills` | `list[Skill]` | Discovered skills (empty if none) |
| `skills_dir` | `str` | Path to skills directory |
| `tool_definitions` | `list` | Tool definitions with optimized descriptions |
| `source` | `str` | Where the config came from (`baseline`, `resolver`, `env`, etc.) |

## Use the config values

Use the model and composed instructions when calling the model:

```python
model = config.model or "gpt-4.1-mini"
instructions = config.compose_instructions()
```

The `compose_instructions()` method returns the system prompt with any discovered skills appended as a skill catalog.

### Apply optimized tool descriptions

If your agent uses tools (functions), apply optimized descriptions to them:

```python
tools = [lookup_travel_policy, check_department_budget, get_flight_alternatives]
config.apply_tool_descriptions(tools)
```

The `apply_tool_descriptions()` method patches each tool function's metadata with the improved descriptions from the optimization config. This improves the model's accuracy when deciding which tool to call.

### Load skills from a directory

If your optimization config doesn't include skills, you can load them from a local directory:

```python
from azure.ai.agentserver.optimization import load_skills_from_dir
from pathlib import Path

if not config.skills and config.skills_dir:
    config.skills.extend(load_skills_from_dir(Path(config.skills_dir)))
```

## Log the config source (recommended)

Add a log line to confirm where the config came from:

```python
import logging

logger = logging.getLogger("my-agent")
logger.info(
    "Config source=%s | model=%s | prompt_len=%d | skills=%d",
    config.source, model, len(instructions), len(config.skills),
)
```

## Apply the optimized config locally

After running `azd ai agent optimize` and selecting a winning candidate, apply it to your local project before deploying:

```bash
# 1. Run optimization
azd ai agent optimize

# 2. Review results
azd ai agent optimize status <job-id>

# 3. Apply the winning candidate locally
azd ai agent optimize apply --candidate <candidate_id>

# 4. Deploy with the optimized config
azd deploy
```

The `apply` command downloads the optimized `instructions.md`, `tools.json`, and `skills/` from the candidate and writes them into `.agent_configs/<candidate_id>/` in your project. On next startup, `load_config()` detects the candidate and uses the optimized configuration.

> [!WARNING]
> If you use `azd ai agent optimize deploy --candidate <id>` instead of `apply`, the optimized config deploys directly via the API without updating your local files. Use the `apply` → `deploy` workflow for production to maintain reproducibility.

## Complete example

The following example shows a travel approval agent that uses the optimization config for instructions, tools, and skills:

```python
import json
import logging
import os
from pathlib import Path
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from pydantic import Field
from azure.ai.agentserver.optimization import load_config, load_skills_from_dir

logger = logging.getLogger(__name__)


@tool(approval_mode="never_require")
def lookup_travel_policy() -> str:
    """Look up the company travel policy rules and limits."""
    return json.dumps({
        "company": "Contoso Ltd.",
        "approval_thresholds": {
            "auto": 1500, "manager": 3000,
            "director": 7500, "vp": "above 7500"
        },
        "lodging_per_night": {"domestic": 250, "international": 400},
        "airfare": "economy only; business class if flight > 6 hours",
        "advance_booking_days": 14,
    })


@tool(approval_mode="never_require")
def check_department_budget() -> str:
    """Check the remaining travel budget for the employee's department."""
    return json.dumps({
        "department": "Engineering",
        "total_budget": 50000, "remaining": 14800,
    })


@tool(approval_mode="never_require")
def get_flight_alternatives(
    destination: Annotated[str, Field(description="The travel destination city")],
) -> str:
    """Find cheaper flight alternatives for the given destination."""
    return json.dumps({
        "alternatives": [
            {"option": "Flexible dates (±2 days)", "savings": "$200-800"},
            {"option": "Nearby alternate airport", "savings": "$100-400"},
        ],
    })


def main():
    # Load optimization config from .agent_configs/
    config = load_config()

    # Load skills from local directory if not provided by optimization
    if not config.skills and config.skills_dir:
        config.skills.extend(load_skills_from_dir(Path(config.skills_dir)))

    model = config.model or os.environ.get(
        "AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini"
    )
    instructions = config.compose_instructions()

    # Apply optimized tool descriptions
    tools = [lookup_travel_policy, check_department_budget, get_flight_alternatives]
    config.apply_tool_descriptions(tools)

    logger.info(
        "Config source=%s | model=%s | prompt_len=%d | skills=%d",
        config.source, model, len(instructions), len(config.skills),
    )

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=model,
        credential=DefaultAzureCredential(),
    )

    agent = Agent(
        client=client,
        instructions=instructions,
        tools=tools,
        default_options={"store": False},
    )

    server = ResponsesHostServer(agent)
    server.run()


if __name__ == "__main__":
    main()
```

## How it works

1. **Normal operation**: No optimization environment variables are set. The config loader reads `.agent_configs/baseline/` and returns your baseline config. The agent works with your original instructions.

1. **During optimization**: The optimizer sets `OPTIMIZATION_CANDIDATE_ID` and `OPTIMIZATION_RESOLVE_ENDPOINT`. The config loader calls the resolver API to fetch the candidate's configuration. Your agent uses the candidate's instructions and tool descriptions during evaluation.

1. **After applying a winner**: You run `azd ai agent optimize apply --candidate <id>` to write the optimized config files into `.agent_configs/<candidate_id>/` in your project. Then `azd deploy` deploys the agent with the improved configuration.

Your code never changes between these states. The config resolution is fully automatic.

### Configuration resolution order

The `load_config()` function resolves configuration using a priority chain (first match wins):

| Priority | Source | Environment variables | Description |
|----------|--------|----------------------|-------------|
| 1 | Inline JSON | `OPTIMIZATION_CONFIG` | Full config as a JSON string |
| 2 | Resolver API | `OPTIMIZATION_CANDIDATE_ID` + `OPTIMIZATION_RESOLVE_ENDPOINT` | Fetches config from the optimization service |
| 3 | Local directory | `OPTIMIZATION_LOCAL_DIR` (defaults to `.agent_configs/`) | Reads `baseline/` or a specific candidate directory |
| 4 | No config | — | Raises `ValueError` (or returns `None` if `required=False`) |

## Verify

Confirm that the package is importable and the configuration loads correctly:

```bash
# Verify the package is importable
python -c "from azure.ai.agentserver.optimization import load_config; print('OK')"

# Run locally and check the log output
azd ai agent run
# Expected log: "Config source=baseline | model=gpt-4.1-mini | ..."
```

## Related content

- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
- [Create a custom evaluation dataset](create-optimizer-dataset.md)
- [Optimize agent instructions and skills](optimize-agent-targets.md)
- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
- [Agent Skills format](https://agentskills.io) — open standard for portable agent skills
