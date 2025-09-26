---
title: "Developer journey stage 1: Idea to prototype - Build and evaluate an enterprise agent"
description: "Prototype an enterprise agent: scaffold a repo, add SharePoint grounding and an MCP tool, run local batch evaluation, extend to multiple agents, and package for container deployment to Azure AI Foundry."
ms.service: azure-ai-foundry
ms.topic: tutorial
ms.date: 09/26/2025
ms.author: jburchel
author: jonburchel
ms.reviewer: dantaylo
#customer intent: As a developer I want to quickly prototype an enterprise-grade agent with real data, tools, evaluation, and a deployment path so I can validate feasibility before scaling.
---

# Developer journey stage 1: Idea to prototype - Build and evaluate an enterprise agent

This tutorial covers the first stage of the Azure AI Foundry developer journey: from an initial idea to a working prototype. You create a working agent using the Azure AI Foundry SDK. The tutorial covers the following critical steps:

> [!div class="checklist"]
> - Scaffold a new agent repository structure (code-first)
> - Build a declarative single agent (model + instructions + tools)
> - Ground the agent with SharePoint content (SharePoint tool)
> - Add an MCP tool to call an external API (Model Context Protocol)
> - Batch evaluate the agent locally for groundedness & relevance
> - Expand to a simple multi‑agent pattern (connected agents) in code
> - Package the agent logic into a container image
> - Prepare for deployment to Azure AI Foundry (next stage)

This prototype helps you de-risk data access, tool orchestration, and evaluation early-before investing in full production hardening.

## Prerequisites

[!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]
- An Azure AI Foundry **project** (with a deployed model such as `gpt-5-mini` or `gpt-4o`) 
- Python 3.10 or later
- Docker installed (for container packaging)
- Access to a SharePoint site and required Microsoft 365 Copilot license per SharePoint tool prerequisites
- Appropriate Azure RBAC (for example, `Azure AI User`) for the project
- An MCP server endpoint you control (local or remote) exposing at least one tool capability [TO VERIFY exact MCP registration flow]
- (Optional) Azure Container Registry (ACR) for pushing the prototype image

## Architecture overview

| Layer | Purpose |
|-------|---------|
| Agent core | Model + instructions + tool list (SharePoint knowledge + MCP action) |
| Tools | SharePoint tool for grounding; MCP tool for external API / data; later additional tools (e.g., Bing, Azure AI Search) |
| Evaluation | Local batch script generating metrics (groundedness, relevance, coherence) |
| Multi-agent (extension) | Introduce a “Research” or “Summarizer” secondary agent connected to the main agent |
| Packaging | Container with minimal API surface or CLI for invocation/testing |

> [!NOTE]
> Connected agents remove the need for hand-written orchestration logic. This tutorial introduces how to structure code so you can evolve toward multi-agent scenarios.

## Step 1: Scaffold a new agent repository

Create a working folder structure:

```text
proto-agent/
  src/
    agent_app/
      __init__.py
      config.py
      build_agent.py
      run_batch_eval.py
      multi_agent.py
      mcp_client.py
  assets/
    eval_questions.jsonl
  tests/
    test_agent_smoke.py
  requirements.txt
  Dockerfile
  .env               # local secrets & endpoints (DO NOT COMMIT)
  README.md
```

### Minimal `requirements.txt`

```text
azure-ai-projects[agents]  # [TO VERIFY] exact package name/version
azure-identity
azure-ai-evaluation[remote]  # for metrics (if supported for agents) [TO VERIFY]
python-dotenv
httpx
rich
```

> [!IMPORTANT]
> Confirm the current package names in official docs. Replace placeholders if the SDK surface changed. Use pinned versions for reproducibility once validated.

### `.env` example (local only)

```text
PROJECT_ENDPOINT=https://<your-project-endpoint>  # from Azure AI Foundry portal
MODEL_DEPLOYMENT_NAME=gpt-4o-mini                 # match your deployed model
SHAREPOINT_RESOURCE_NAME=<sharepoint-conn-name>   # from Connected resources
MCP_ENDPOINT=http://localhost:3333                # sample local MCP server
```

Add `.env` to `.gitignore` to avoid committing credentials.

## Step 2: Implement configuration loading

`src/agent_app/config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    project_endpoint: str = os.environ.get("PROJECT_ENDPOINT", "")
    model_deployment: str = os.environ.get("MODEL_DEPLOYMENT_NAME", "")
    sharepoint_resource: str = os.environ.get("SHAREPOINT_RESOURCE_NAME", "")
    mcp_endpoint: str = os.environ.get("MCP_ENDPOINT", "")

    def validate(self):  # quick sanity checks
        missing = [k for k,v in self.__dict__.items() if not v]
        if missing:
            raise ValueError(f"Missing required env settings: {missing}")

settings = Settings()
```

## Step 3: Build a single declarative agent (SharePoint + MCP)

`src/agent_app/build_agent.py` (core creation logic). The following snippet outlines typical usage patterns based on current docs excerpts. Replace names/classes if the SDK changed.

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient  # [TO VERIFY import path]
from azure.ai.agents.models import SharepointTool  # [TO VERIFY]
# [TO VERIFY] Confirm MCP tool class naming/location
# e.g., from azure.ai.agents.models import MCPTool  (placeholder)

from .config import settings

SYSTEM_INSTRUCTIONS = """
You are an enterprise knowledge assistant. Use SharePoint grounding when user queries reference internal policies, procedures, or documents. Use MCP tools for real-time external API enrichment when needed. Answer concisely, cite retrieved document titles when grounding applies.
""".strip()

def create_agent(project_client):
    # Initialize tools
    sharepoint_tool = SharepointTool(connection_name=settings.sharepoint_resource)  # [TO VERIFY] parameter name
    mcp_tool = None  # [TO VERIFY] instantiate MCP tool with endpoint/capabilities

    agent = project_client.agents.create(  # [TO VERIFY] method signature
        model=settings.model_deployment,
        instructions=SYSTEM_INSTRUCTIONS,
        tools=[sharepoint_tool, mcp_tool] if mcp_tool else [sharepoint_tool],
        name="proto-stage1-agent",  # human-friendly label
    )
    return agent

if __name__ == "__main__":
    settings.validate()
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(endpoint=settings.project_endpoint, credential=credential)
    agent = create_agent(project_client)
    print(f"Created agent id: {agent.id} [TO VERIFY id attribute]")
```

> [!CAUTION]
> The MCP tool instantiation details are placeholder. Mark and confirm before publishing. Add `[TO VERIFY]` where necessary.

### Add a test prompt (smoke)

```python
# In same file or test harness
thread = project_client.threads.create()  # [TO VERIFY]
project_client.messages.create(
    thread_id=thread.id,
    role="user",
    content="Summarize key policy points from our SharePoint site about remote work."  # Should trigger SharePoint tool
)
run = project_client.runs.create(thread_id=thread.id, assistant_id=agent.id)  # [TO VERIFY names]
print("Run started:", run.id)
```

## Step 4: Add external APIs via MCP (Model Context Protocol)

MCP enables standardized tool exposure. Steps (conceptual):

1. Operate or point to an MCP server offering capabilities (e.g., `weather.get_current`, `finance.lookup_ticker`).
2. Register an MCP tool referencing the server endpoint / schema.
3. Include it in the agent’s tool list.
4. Observe tool invocation in run traces (later, use tracing docs).

> [!NOTE]
> Insert final MCP Python SDK usage once official class & arguments are confirmed. For now, annotate with `[TO VERIFY]` in code.

`src/agent_app/mcp_client.py` (placeholder abstraction):

```python
# Placeholder adapter until official MCP tool class is confirmed.
# [TO VERIFY] Replace with actual import and creation pattern from docs when available.
class MCPToolPlaceholder:
    def __init__(self, endpoint: str, name: str = "mcp-tool"):
        self.endpoint = endpoint
        self.name = name
```

## Step 5: Create an evaluation dataset

Create `assets/eval_questions.jsonl`:

```jsonl
{"id": 0, "question": "Summarize the remote work policy", "expected_contains": ["remote", "policy"]}
{"id": 1, "question": "List security training requirements", "expected_contains": ["security", "training"]}
{"id": 2, "question": "What external API data can you enrich?", "expected_contains": ["API"]}
{"id": 3, "question": "Summarize last quarter financials", "expected_contains": ["quarter"]}
```

> [!TIP]
> Keep Stage 1 datasets tiny - focus on signal, not completeness.

## Step 6: Batch evaluate locally

`src/agent_app/run_batch_eval.py` (conceptual harness):

```python
import json, time
from pathlib import Path
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient  # [TO VERIFY]
# from azure.ai.evaluation import ???  # [TO VERIFY evaluator import]

from .config import settings

EVAL_FILE = Path("assets/eval_questions.jsonl")

# Simple custom metric helpers (stop-gap until evaluator integration confirmed)

def groundedness_score(response: str):
    # Placeholder heuristic; replace with official evaluator call [TO VERIFY]
    return 1.0 if len(response.split()) > 3 else 0.0

def run_eval(agent_id: str):
    credential = DefaultAzureCredential()
    client = AIProjectClient(endpoint=settings.project_endpoint, credential=credential)
    results = []
    for line in EVAL_FILE.read_text().splitlines():
        row = json.loads(line)
        thread = client.threads.create()  # [TO VERIFY]
        client.messages.create(thread_id=thread.id, role="user", content=row["question"])  # [TO VERIFY]
        run = client.runs.create(thread_id=thread.id, assistant_id=agent_id)  # [TO VERIFY]
        # (Pseudo) poll for completion
        while True:
            run_status = client.runs.get(thread_id=thread.id, run_id=run.id)  # [TO VERIFY]
            if getattr(run_status, "status", None) in {"succeeded", "failed", "completed"}:
                break
            time.sleep(1)
        messages = client.messages.list(thread_id=thread.id)  # [TO VERIFY]
        final = messages[-1].content if messages else ""
        score = groundedness_score(final)
        results.append({"id": row["id"], "question": row["question"], "response": final, "groundedness": score})
    return results

if __name__ == "__main__":
    settings.validate()
    # [TO VERIFY] Retrieve agent id from persisted state or parameter
    agent_id = "[TO VERIFY_AGENT_ID]"
    out = run_eval(agent_id)
    print(out)
```

> [!IMPORTANT]
> Replace the heuristic with official evaluation SDK usage once confirmed. Add metrics like relevance/coherence if available.

## Step 7: Evolve to a simple multi-agent pattern

Introduce a secondary agent specialized for research summarization or external enrichment.

`src/agent_app/multi_agent.py` (concept sketch):

```python
# [TO VERIFY] Adjust API names for connected agents
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from .config import settings

PRIMARY_INSTRUCTIONS = "Primary coordinator. Delegate factual enrichment to 'research-agent' when queries require external or broad context."
RESEARCH_INSTRUCTIONS = "Research agent. Provide concise factual expansions from grounded sources, citing titles."  # Keep narrow scope

def create_connected_agents():
    cred = DefaultAzureCredential()
    client = AIProjectClient(endpoint=settings.project_endpoint, credential=cred)

    research = client.agents.create(
        model=settings.model_deployment,
        instructions=RESEARCH_INSTRUCTIONS,
        name="research-agent",
        tools=[]  # Could add Bing / MCP variant [TO VERIFY]
    )

    primary = client.agents.create(
        model=settings.model_deployment,
        instructions=PRIMARY_INSTRUCTIONS,
        name="primary-agent",
        tools=[],  # Provide connection references [TO VERIFY]
        connected_agents=[research.id]  # [TO VERIFY] property name for linking
    )
    return primary, research
```

> [!NOTE]
> Confirm the exact property or method for establishing connected/child agents. Use `[TO VERIFY]` until verified.

## Step 8: Package as a container (prototype)

`Dockerfile` (minimal development image):

```dockerfile
# [TO VERIFY] Use official Azure AI Foundry base image if recommended
FROM mcr.microsoft.com/devcontainers/python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY assets ./assets
ENV PYTHONPATH=/app/src
CMD ["python", "-m", "agent_app.run_batch_eval"]  # default cmd (adjust as needed)
```

Build & tag (example):

```bash
docker build -t proto-agent:local .
```

Push to ACR (if desired):

```bash
# [TO VERIFY] Replace with your registry name
az acr login --name <registry>
docker tag proto-agent:local <registry>.azurecr.io/proto-agent:stage1
docker push <registry>.azurecr.io/proto-agent:stage1
```

## Step 9: Prepare for deployment

At Stage 1 you verify packaging; actual deployment steps (registering the container, binding environment configs, observability) can be performed in Stage 2 (Productionization). For future work:

- Register container-based runtime (if supported) [TO VERIFY container deployment workflow]
- Configure tracing & Application Insights
- Set up CI pipeline to rebuild image on main branch merges

## Step 10: Trace runs & iterate

Early diagnostics:

1. Use thread and run listing to inspect message ordering.
2. Enable tracing (link to tracing docs) [TO VERIFY add link]
3. Adjust system instructions and retest batch evaluation.

> [!TIP]
> Keep a changelog of prompt & tool configuration changes correlated with metric shifts.

## Clean up resources

Delete unnecessary threads, and remove model deployments or the entire resource group if no longer needed.

## Next steps

- Harden identity: On-Behalf-Of passthrough for SharePoint + enforce RBAC scoping
- Add Azure AI Search for hybrid retrieval
- Introduce continuous evaluation pipeline (scheduled or on-PR)
- Add network isolation / VNet and private endpoints
- Implement BYO thread storage (Cosmos DB) if required for compliance

## Related content

- [What is Azure AI Foundry Agent Service?](../../agents/overview.md)  [TO VERIFY relative path]
- [Tools overview](../../agents/how-to/tools/overview.md) [TO VERIFY path]
- [SharePoint tool usage](../../agents/how-to/tools/sharepoint.md) [TO VERIFY path]
- [Connected agents](../../agents/how-to/connected-agents.md) [TO VERIFY path]
- [Evaluation results overview](../../how-to/evaluate-results.md) [TO VERIFY path]
- [Tracing agents](../../how-to/develop/trace-agents-sdk.md) [TO VERIFY path]

> [!IMPORTANT]
> Replace all `[TO VERIFY]` placeholders with confirmed values (package names, method signatures, relative links) before publishing.
