---
title: "Register external agents for observability and evaluation"
description: "Register third-party agents running on any host in Microsoft Foundry for tracing and evaluation, without migrating the runtime or provisioning an AI Gateway."
author: aahill
ms.author: aahi
ms.date: 05/20/2026
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As an AI developer running agents outside Foundry, I want to register them in Foundry so that I can use Foundry's trace view and evaluation experiences without migrating my runtime.
---

# Register external agents for observability and evaluation (preview)
[!INCLUDE [feature-preview](../../includes/feature-preview.md)]
Microsoft Foundry Agent Service lets you register agents that run outside Foundry, on any cloud, on-premises, or other host, so you can use Foundry's trace view and evaluation experiences. Foundry stores only registration metadata for these agents. It doesn't host, proxy, or invoke the runtime.

External agents differ from [Control Plane custom agents](../../control-plane/register-custom-agent.md), which route traffic through an AI Gateway. With external agents, your agent keeps its existing endpoint and shares only OpenTelemetry telemetry. No AI Gateway is required.

In this article, you learn how to:

- Instrument an external agent to emit OpenTelemetry spans to Application Insights.
- Register the agent in Foundry as an `external` agent.
- Verify traces in the Foundry portal.
- Run a trace-based evaluation over the agent's collected telemetry.

The following diagram shows the data flow: your external agent emits OpenTelemetry spans with a `gen_ai.agent.id` attribute to an Application Insights resource connected to your Foundry project. A separate registration call creates the agent record in Foundry. The Foundry portal then matches traces by agent ID and displays them in the agent trace view.

:::image type="content" source="../media/register-external/architecture.svg" alt-text="Diagram that shows the data flow for external agent observability. The external agent emits OpenTelemetry spans to Application Insights, which connects to the Foundry portal trace view. A separate registration call creates the agent record in the Foundry project." lightbox="../media/register-external/architecture.svg":::

> [!IMPORTANT]
> External agents are in public preview. Create and update requests require the `Foundry-Features: ExternalAgents=V1Preview` header. SDK callers enable this by constructing `AIProjectClient` with `allow_preview=True`.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with an [Application Insights resource connected](../../observability/how-to/trace-agent-setup.md#connect-application-insights-to-your-foundry-project).
- An agent running outside Foundry that can emit OpenTelemetry spans to that Application Insights resource.
- Python 3.11 or later.
- **Foundry User** role on the project.
- **Reader** role or **Monitoring Reader** role on the connected Application Insights resource to view traces.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

- `DefaultAzureCredential` configured. Sign in with `az login` or set up a managed identity or service principal.
- *(For evaluation only)* An Azure OpenAI deployment with a GPT model that supports chat completion (for example, `gpt-5-mini`).

## Instrument the external agent with OpenTelemetry

Before you register the agent in Foundry, configure it to export OpenTelemetry spans to the Application Insights resource connected to your Foundry project. Each span must carry the `gen_ai.agent.id` attribute so Foundry can attribute the span to the correct agent registration.

### Install the Microsoft OpenTelemetry package

```bash
pip install "microsoft-opentelemetry[langchain]"
```

### Configure the exporter

Run this code once during agent startup, before any framework imports that should be instrumented:

```python
import os

os.environ.setdefault("AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING", "true")
os.environ.setdefault("OTEL_SEMCONV_STABILITY_OPT_IN", "gen_ai_latest_experimental")
os.environ.setdefault("OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT", "SPAN_AND_EVENT")

from microsoft.opentelemetry import use_microsoft_opentelemetry

AGENT_NAME = os.environ.get("AGENT_NAME", "weather-agent")
OTEL_AGENT_ID = os.environ.get("OTEL_AGENT_ID", f"{AGENT_NAME}-v1")

use_microsoft_opentelemetry(
    enable_azure_monitor=True,
    azure_monitor_connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"],
    sampling_ratio=1.0,
    instrumentation_options={
        "fastapi": {"enabled": False},
        "langchain": {
            "enabled": True,
            "agent_id": OTEL_AGENT_ID,
            "agent_name": AGENT_NAME,
        },
    },
)
```

Set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable on the host where the agent runs. Use the connection string from the Application Insights resource linked to your Foundry project.

After configuration, subsequent OpenTelemetry spans from your agent framework automatically flow to Application Insights. Each span must set the `gen_ai.agent.id` attribute to the value you choose as `otel_agent_id` during registration.

If your agent framework doesn't set this attribute automatically, add it manually:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("agent-run") as span:
    span.set_attribute("gen_ai.agent.id", "travel-planner-agent")
    # ... your agent logic ...
```

> [!TIP]
> For framework-specific auto-instrumentation (LangChain, LangGraph), the [Microsoft OpenTelemetry distro for Python](https://github.com/microsoft/opentelemetry-distro-python) can set `gen_ai.agent.id` automatically via `instrumentation_options`. For .NET and JavaScript, see the [.NET distro](https://github.com/microsoft/opentelemetry-distro-dotnet) and [JavaScript distro](https://github.com/microsoft/opentelemetry-distro-javascript). For general guidance, see [Configure tracing for AI agent frameworks](../../observability/how-to/trace-agent-framework.md).

## Register the external agent in Foundry

After the agent emits spans to Application Insights, register it in Foundry so those spans appear in the Foundry trace view scoped to the agent.

### Install the SDK

```bash
pip install azure-ai-projects>=2.2.0 azure-identity>=1.17.0
```

### Create the registration

### [Foundry portal](#tab/portal)

### Foundry portal

You can create a registration in the [Foundry portal](https://ai.azure.com) by:
1. Opening your project and selecting **build** > **agents** > **New agent**.
1. Selecting **Link external agent**.
1. In the window that appears, entering the agent name, description and the OpenTelemetry ID. 

    :::image type="content" source="../media/register-external/foundry-button.png" alt-text="A screenshot showing the button to link an external agent" lightbox="../media/register-external/foundry-button.png":::

### [Python SDK](#tab/python)

### Python SDK 

Set the `FOUNDRY_PROJECT_ENDPOINT` environment variable to your project endpoint. You can find this value on the project's **Overview** page in the Foundry portal.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ExternalAgentDefinition
from azure.identity import DefaultAzureCredential

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

# Create the project client with preview features enabled.
project = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
    allow_preview=True,
)

# Register the externally hosted agent.
agent = project.agents.create_version(
    agent_name="travel-planner-agent",
    description="Travel planning agent hosted externally.",
    definition=ExternalAgentDefinition(
        # optional, defaults to agent_name
        otel_agent_id="travel-planner-agent",
    ),
)

print(f"Registered external agent: {agent.name}")
print(f"Resolved otel_agent_id: {agent.versions.latest.definition.otel_agent_id}")
```

```output
Registered external agent: travel-planner-agent
Resolved otel_agent_id: travel-planner-agent
```

> [!NOTE]
> The `otel_agent_id` parameter is optional and defaults to the agent `name`. Set it explicitly only when the running agent already emits a stable `gen_ai.agent.id` value that differs from the Foundry agent name.

The `create_version()` method atomically creates the agent record and its first registration revision when called with a new name. External agents are versionless from the user's perspective. Edits to `otel_agent_id` create a new internal revision under the same name.

---

## Run an evaluation

```python
openai_client = project.get_openai_client()

# Eval group: define what to measure.
eval_group = openai_client.evals.create(
    name="travel-planner-trace-eval",
    data_source_config={"type": "azure_ai_source", "scenario": "traces"},
    testing_criteria=[
        {
            "type": "azure_ai_evaluator",
            "name": "intent_resolution",
            "evaluator_name": "builtin.intent_resolution",
            "data_mapping": {
                "query": "{{item.query}}",
                "response": "{{item.response}}",
                "tool_definitions": "{{item.tool_definitions}}",
            },
            "initialization_parameters": {"deployment_name": "gpt-5-mini"},
        },
    ],
)

# Eval run: score this agent's recent traces.
run = openai_client.evals.runs.create(
    eval_id=eval_group.id,
    name="travel-planner-trace-run",
    data_source={
        "type": "azure_ai_traces",
        "agent_id": otel_agent_id,
        "lookback_hours": 24,
    },
)
# Poll openai_client.evals.runs.retrieve(...) until run.status
# is in {"completed", "failed", "canceled"}, then read run.result_counts
# and run.per_testing_criteria_results.
```

## Verify traces in the Foundry portal

After the agent sends traffic and spans ingest into Application Insights (typically 2–5 minutes), verify that traces appear in the Foundry portal:

1. Open the [Foundry portal](https://ai.azure.com).

1. Navigate to your project.

1. Select **Agents** from the left pane.

1. Select the external agent name (for example, **travel-planner-agent**).

1. Select the **Traces** tab to view spans attributed to this agent.

Traces are matched by `gen_ai.agent.id = <otel_agent_id>` from the Application Insights resource connected to the project. You can view inputs, outputs, tool calls, and latency for each span.

### Troubleshoot missing traces

If you don't see traces, check the following items:

> [!div class="checklist"]
> * The Application Insights resource is connected to the Foundry project where you registered the agent.
> * The `otel_agent_id` on the registration matches the `gen_ai.agent.id` attribute on the spans.
> * The agent process has `APPLICATIONINSIGHTS_CONNECTION_STRING` set to the correct Application Insights resource.
> * Spans comply with [OpenTelemetry semantic conventions for generative AI](https://opentelemetry.io/docs/specs/semconv/gen-ai/).

For more troubleshooting guidance, see [Troubleshoot evaluation and observability issues](../../observability/how-to/troubleshooting.md).

### Troubleshoot registration errors

If `create_version()` fails, check the following items:

> [!div class="checklist"]
> * You constructed `AIProjectClient` with `allow_preview=True`. Without this flag, external agent requests are rejected.
> * Your identity has the **Foundry User** role (or higher) on the project.
> * The `agent_name` value uses only alphanumeric characters, hyphens, and underscores.
> * No existing agent with the same name and a different kind already exists. Use `project.agents.get()` to check.

## Run a trace-based evaluation

After traces flow into Application Insights, you can run evaluations directly over those traces. No separate dataset construction is required. Foundry resolves traces by matching `(project, agent_id)` over a lookback window.

> [!NOTE]
> Trace-based evaluations use the OpenAI-compatible `evals` API (`project.get_openai_client().evals`). The native `project.evaluations` surface doesn't yet support trace-based evaluation.

### Resolve the agent's otel_agent_id

To get the agent's ID for traces, use the following:

```python
# Retrieve the registered agent and its resolved otel_agent_id.
agent = project.agents.get(agent_name="travel-planner-agent")
otel_agent_id = agent.versions.latest.definition.otel_agent_id
```

## Manage external agents

Use the same SDK methods to list, retrieve, and delete external agents.

### List external agents

```python
agents = project.agents.list(kind="external")
for a in agents:
    print(a.name)
```

### Delete an external agent

```python
# Delete the registration. This does not affect the running agent.
project.agents.delete(agent_name="travel-planner-agent")

#Use the following line to delete the registration for all versions of the agent
# project_client.agents.delete("travel-planner-agent", force=True)
```

Deleting the registration removes the agent from the Foundry portal and stops traces from appearing in the Foundry agent trace view. The spans remain in Application Insights, and the running agent is not affected.

## Related content

- [Agent tracing overview](../../observability/concepts/trace-agent-concept.md)
- [Set up tracing in Microsoft Foundry](../../observability/how-to/trace-agent-setup.md)
- [Configure tracing for AI agent frameworks](../../observability/how-to/trace-agent-framework.md)
- [Evaluate your AI agents](../../observability/how-to/evaluate-agent.md)
- [Register and manage custom agents (Control Plane)](../../control-plane/register-custom-agent.md)
- [Built-in evaluators](../../concepts/evaluation-evaluators/general-purpose-evaluators.md)
- [Azure Monitor OpenTelemetry overview](/azure/azure-monitor/app/opentelemetry-enable)
- [run cloud evaluations](../../how-to/develop/cloud-evaluation.md#prerequisites)