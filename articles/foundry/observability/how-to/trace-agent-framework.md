---
title: Configure tracing for AI agent frameworks
titleSuffix: Microsoft Foundry
description: Debug issues and monitor AI agent performance in production by configuring OpenTelemetry tracing for LangChain, LangGraph, Semantic Kernel, and OpenAI Agents SDK.
ai-usage: ai-assisted
author: yanchen-ms
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 06/02/2026
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.topic: how-to
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
---

<!-- CustomerIntent: As a developer building AI agents, I want to configure tracing for my agent framework so that I can debug issues and monitor performance in production. -->

# Configure tracing for AI agent frameworks (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

[!INCLUDE [trace-agent-preview](../../includes/trace-agent-preview.md)]

When AI agents behave unexpectedly in production, tracing gives you the visibility to quickly identify the root cause. Tracing captures detailed telemetry—including LLM calls, tool invocations, and agent decision flows—so you can debug issues, monitor latency, and understand agent behavior across requests.

Microsoft Foundry provides tracing integrations for popular agent frameworks that require minimal code changes. In this article, you learn how to:

- Configure automatic tracing for Microsoft Agent Framework and Semantic Kernel
- Set up the Microsoft OpenTelemetry distro for LangChain and LangGraph
- Instrument the OpenAI Agents SDK with OpenTelemetry
- Verify that traces appear in the Foundry portal
- Troubleshoot common tracing issues

## Prerequisites

- A Foundry project. For more information, see [Create a Foundry project](../../how-to/create-projects.md).
- Tracing connected to an Azure Monitor Application Insights resource. To set it up, see [Set up tracing in Microsoft Foundry](trace-agent-setup.md).
- Contributor or higher role on the Application Insights resource for trace ingestion.
- Access to the connected Application Insights resource for viewing traces. For log-based queries, you might also need access to the associated Log Analytics workspace.
- Python 3.10 or later (required for all code samples in this article).
- The `microsoft-opentelemetry` package (required for LangChain and LangGraph samples).
- If you use LangChain or LangGraph, a Python environment with pip installed.

### Confirm you can view telemetry

To view trace data, make sure your account has access to the connected Application Insights resource.

1. In the Azure portal, open the Application Insights resource connected to your Foundry project.
1. Select **Access control (IAM)**.
1. Assign an appropriate role to your user or group.

    If you use log-based queries, start by granting the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader). If the underlying Log Analytics tables are [protected](/azure/azure-monitor/logs/protected-tables-configure), also grant the [Privileged Monitoring Data Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#privileged-monitoring-data-reader).

## Security and privacy

Tracing can capture sensitive information (for example, user inputs, model outputs, and tool arguments and results).

- Enable content recording during development and debugging to see full request and response data. Disable content recording in production environments to protect sensitive data. In the samples in this article, content recording is controlled by the environment variables `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`, `OTEL_SEMCONV_STABILITY_OPT_IN`, and `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING`.
- Don't store secrets, credentials, or tokens in prompts or tool arguments.

For more guidance, see [Security and privacy](../concepts/trace-agent-concept.md#security-and-privacy).

> [!NOTE]
> Trace data stored in Application Insights is subject to your workspace's data retention settings and Azure Monitor pricing. For cost management, consider adjusting sampling rates or retention periods in production. See [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/) and [Configure data retention and archive](/azure/azure-monitor/logs/data-retention-configure).

## Configure tracing for Microsoft Agent Framework and Semantic Kernel

Microsoft Foundry has native integrations with both Microsoft Agent Framework and Semantic Kernel. Agents built with either framework automatically emit traces when tracing is enabled for your Foundry project—no additional code or packages are required.

To verify tracing is working:

1. Run your agent at least once.
1. In the Foundry portal, go to **Observability** > **Traces**.
1. Confirm a new trace appears with spans for your agent's operations.

Traces typically appear within 2–5 minutes after agent execution. For advanced configuration, see the framework-specific documentation:

- [Microsoft Agent Framework Workflows – Observability](/agent-framework/user-guide/workflows/observability)
- [Semantic Kernel observability](/semantic-kernel/concepts/enterprise-readiness/observability)

## Configure tracing with OpenInference instrumentation libraries

Microsoft Foundry supports [OpenInference](https://pypi.org/search/?q=openinference) instrumentation libraries for tracing AI agents. These `openinference-*` packages provide automatic instrumentation for a wide range of frameworks and can be used to trace both hosted agents (agents deployed to Foundry) and non-Foundry agents (agents hosted outside of Foundry).

Browse available instrumentation packages on [PyPI](https://pypi.org/search/?q=openinference). For LangChain, see the [Microsoft OpenTelemetry distro LangChain sample](https://github.com/microsoft/opentelemetry-distro-python/tree/main/samples/langchain), which shows how to enable Azure Monitor export and LangChain auto-instrumentation with `use_microsoft_opentelemetry`.

The key requirement is correlating OpenInference traces to a specific agent. How you achieve this depends on where your agent runs:

### Hosted agents (deployed to Foundry)

When you deploy an agent to Foundry using one of the hosted agent server packages, trace correlation is handled automatically. The server package:

- Configures Azure Monitor export for OpenTelemetry spans.
- Enriches all spans with project, agent name, agent version, and agent ID attributes so the Foundry UI can query and display them.

No additional configuration is required. Install the relevant `openinference-*` instrumentation package for your framework and traces appear in the Foundry portal automatically.

### Microsoft Agent Framework agents hosted outside of Foundry

If your Microsoft Agent Framework agent isn't deployed with a Foundry hosted agent server package, configure Azure Monitor export and agent framework instrumentation with the [Microsoft OpenTelemetry distro](https://pypi.org/project/microsoft-opentelemetry/). The distro can enable the Azure Monitor exporter and add agent identity attributes to spans:

```python
from microsoft.opentelemetry import use_microsoft_opentelemetry

use_microsoft_opentelemetry(
    enable_azure_monitor=True,
    azure_monitor_connection_string="...",
    sampling_ratio=1.0,
    enable_sensitive_data=True,
    instrumentation_options={
        "agent-framework": {
            "enabled": True,
            "agent_id": "ms-imagination-agent",
            "agent_name": "ms-imagination-agent",
        },
    },
)
```

Set `azure_monitor_connection_string` to the Application Insights resource connected to your Foundry project. To capture prompt and completion content during development, set `enable_sensitive_data=True`.

### LangChain agents hosted outside of Foundry

If your agent isn't deployed with a Foundry hosted agent server package, configure Azure Monitor export and LangChain instrumentation with the [Microsoft OpenTelemetry distro](https://pypi.org/project/microsoft-opentelemetry/). The distro can enable the Azure Monitor exporter and add agent identity attributes to LangChain spans:

```python
from microsoft.opentelemetry import use_microsoft_opentelemetry

use_microsoft_opentelemetry(
    enable_azure_monitor=True,
    sampling_ratio=1.0,
    instrumentation_options={
        "langchain": {
            "enabled": True,
            "agent_id": "weather_info_agent_771929",
            "agent_name": "Weather information agent",
        },
    },
)
```

Set `APPLICATIONINSIGHTS_CONNECTION_STRING` to the Application Insights resource connected to your Foundry project. To capture prompt and completion content during development, set `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_AND_EVENT`, `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`, and `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true`.

## Configure tracing for LangChain and LangGraph

> [!NOTE]
> Tracing integration for LangChain and LangGraph is currently available only in Python.

Use the [Microsoft OpenTelemetry distro](https://pypi.org/project/microsoft-opentelemetry/) to emit OpenTelemetry-compliant spans for LangChain and LangGraph operations. These traces appear in the **Observability** > **Traces** view in the Foundry portal.

- [OpenTelemetry semantic conventions for generative AI](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)
- [Microsoft OpenTelemetry distro LangChain sample](https://github.com/microsoft/opentelemetry-distro-python/tree/main/samples/langchain)

### Sample: LangChain v1 agent with Azure AI tracing

Use this end-to-end sample to instrument a LangChain v1 (preview) agent using the Microsoft OpenTelemetry distro. The distro enables LangChain auto-instrumentation with the latest OpenTelemetry (OTel) semantic conventions, so you can view rich traces in the Foundry observability view.

#### LangChain v1: Install packages

```bash
pip install \
  microsoft-opentelemetry \
  langchain \
  langgraph \
  langchain-openai \
  azure-identity \
  python-dotenv \
  rich
```

#### LangChain v1: Configure environment

- `APPLICATIONINSIGHTS_CONNECTION_STRING`: Azure Monitor Application Insights connection string for tracing.
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL.
- `AZURE_OPENAI_CHAT_DEPLOYMENT`: The chat model deployment name.
- `AZURE_OPENAI_VERSION`: API version, for example `2024-08-01-preview`.
- The SDK resolves Azure credentials using `DefaultAzureCredential`, which supports environment variables, managed identity, and VS Code sign-in.

Store these values in a `.env` file for local development.

#### LangChain v1: Tracer setup

```python
from dotenv import load_dotenv
from microsoft.opentelemetry import use_microsoft_opentelemetry

load_dotenv(override=True)

use_microsoft_opentelemetry(
    enable_azure_monitor=True,
    sampling_ratio=1.0,
    instrumentation_options={
        "langchain": {
            "enabled": True,
            "agent_id": "weather_info_agent_771929",
            "agent_name": "Weather information agent",
        },
    },
)
```

#### LangChain v1: Model setup (Azure OpenAI)

```python
import os
import azure.identity
from langchain_openai import AzureChatOpenAI

token_provider = azure.identity.get_bearer_token_provider(
    azure.identity.DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default",
)

model = AzureChatOpenAI(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    openai_api_version=os.environ.get("AZURE_OPENAI_VERSION"),
    azure_ad_token_provider=token_provider,
)
```

#### LangChain v1: Define tools and prompt

```python
from dataclasses import dataclass
from langchain_core.tools import tool

system_prompt = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location.
If you can tell from the question that they mean wherever they are,
use the get_user_location tool to find their location."""

# Mock user locations keyed by user id (string)
USER_LOCATION = {
    "1": "Florida",
    "2": "SF",
}


@dataclass
class UserContext:
    user_id: str


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"
```

#### LangChain v1: Use runtime context and define a user-info tool

```python
from langgraph.runtime import get_runtime
from langchain_core.runnables import RunnableConfig

@tool
def get_user_info(config: RunnableConfig) -> str:
    """Retrieve user information based on user ID."""
    runtime = get_runtime(UserContext)
    user_id = runtime.context.user_id
    return USER_LOCATION[user_id]
```

#### LangChain v1: Create the agent

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from dataclasses import dataclass


@dataclass
class WeatherResponse:
    conditions: str
    punny_response: str


checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    prompt=system_prompt,
    tools=[get_user_info, get_weather],
    response_format=WeatherResponse,
    checkpointer=checkpointer,
)
```

#### LangChain v1: Run the agent with tracing

```python
from rich import print

def main():
    config = {"configurable": {"thread_id": "1"}}
    context = UserContext(user_id="1")

    r1 = agent.invoke(
        {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
        config=config,
        context=context,
    )
    print(r1.get("structured_response"))

    r2 = agent.invoke(
        {"messages": [{"role": "user", "content": "Thanks"}]},
        config=config,
        context=context,
    )
    print(r2.get("structured_response"))


if __name__ == "__main__":
    main()
```

With the Microsoft OpenTelemetry distro enabled, all LangChain v1 operations (LLM calls, tool invocations, agent steps) emit OpenTelemetry spans using the latest semantic conventions. These traces appear in the **Observability** > **Traces** view in the Foundry portal and are linked to your Application Insights resource.

> [!TIP]
> After running the agent, wait a few minutes for traces to appear. If you don't see traces, verify your Application Insights connection string is correct and check the [Troubleshoot common issues](#troubleshoot-common-issues) section.

#### Verify your LangChain v1 traces

After running the agent:

1. Wait 2–5 minutes for traces to propagate.
1. In the Foundry portal, go to **Observability** > **Traces**.
1. Look for a trace with the name you specified (for example, "Weather information agent").
1. Expand the trace to see spans for LLM calls, tool invocations, and agent steps.

If you don't see traces, check the [Troubleshoot common issues](#troubleshoot-common-issues) section.

### Sample: LangGraph agent with Azure AI tracing

This sample shows a simple LangGraph agent instrumented with the Microsoft OpenTelemetry distro to emit OpenTelemetry-compliant traces for graph steps, tool calls, and model invocations.

#### LangGraph: Install packages

```bash
pip install \
  microsoft-opentelemetry \
  "langgraph>=1.0.0" \
  "langchain>=1.0.0" \
  langchain-openai \
  azure-identity \
  python-dotenv
```

#### LangGraph: Configure environment

- `APPLICATIONINSIGHTS_CONNECTION_STRING`: Azure Monitor Application Insights connection string for tracing.
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL.
- `AZURE_OPENAI_CHAT_DEPLOYMENT`: The chat model deployment name.
- `AZURE_OPENAI_VERSION`: API version, for example `2024-08-01-preview`.

Store these values in a `.env` file for local development.

#### LangGraph tracer setup

```python
from dotenv import load_dotenv
from microsoft.opentelemetry import use_microsoft_opentelemetry

load_dotenv(override=True)

use_microsoft_opentelemetry(
    enable_azure_monitor=True,
    sampling_ratio=1.0,
    instrumentation_options={
        "langchain": {
            "enabled": True,
            "agent_name": "Music Player Agent",
        },
    },
)
```

#### LangGraph: Tools

```python
from langchain_core.tools import tool

@tool
def play_song_on_spotify(song: str):
    """Play a song on Spotify"""
    # Integrate with Spotify API here.
    return f"Successfully played {song} on Spotify!"


@tool
def play_song_on_apple(song: str):
    """Play a song on Apple Music"""
    # Integrate with Apple Music API here.
    return f"Successfully played {song} on Apple Music!"


tools = [play_song_on_apple, play_song_on_spotify]
```

#### LangGraph: Model setup (Azure OpenAI)

```python
import os
import azure.identity
from langchain_openai import AzureChatOpenAI

token_provider = azure.identity.get_bearer_token_provider(
    azure.identity.DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default",
)

model = AzureChatOpenAI(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    openai_api_version=os.environ.get("AZURE_OPENAI_VERSION"),
    azure_ad_token_provider=token_provider,
).bind_tools(tools, parallel_tool_calls=False)
```

#### Build the LangGraph workflow

```python
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

tool_node = ToolNode(tools)

def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    return "continue" if getattr(last_message, "tool_calls", None) else "end"


def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)
workflow.add_edge("action", "agent")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

#### LangGraph: Run with tracing

```python
from langchain_core.messages import HumanMessage

config = {"configurable": {"thread_id": "1"}}
input_message = HumanMessage(content="Can you play Taylor Swift's most popular song?")

for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()
```

With the Microsoft OpenTelemetry distro enabled, your LangGraph execution emits OpenTelemetry-compliant spans for model calls, tool invocations, and graph transitions. These traces flow to Application Insights and appear in the **Observability** > **Traces** view in the Foundry portal.

> [!TIP]
> Each graph node and edge transition creates a separate span, making it easy to visualize the agent's decision flow.

#### Verify your LangGraph traces

After running the agent:

1. Wait 2–5 minutes for traces to propagate.
1. In the Foundry portal, go to **Observability** > **Traces**.
1. Look for a trace with the name you specified (for example, "Music Player Agent").
1. Expand the trace to see spans for graph nodes, tool invocations, and model calls.

If you don't see traces, check the [Troubleshoot common issues](#troubleshoot-common-issues) section.

### Sample: LangChain 0.3 setup with Azure AI tracing

This minimal setup shows how to enable Azure AI tracing in a LangChain 0.3 application using the Microsoft OpenTelemetry distro and `AzureChatOpenAI`.

#### LangChain 0.3: Install packages

```bash
pip install \
  "langchain>=0.3,<0.4" \
  langchain-openai \
  microsoft-opentelemetry \
  python-dotenv
```

#### LangChain 0.3: Configure environment

- `APPLICATIONINSIGHTS_CONNECTION_STRING`: Application Insights connection string for tracing. To find this value, open your Application Insights resource in the Azure portal, select **Overview**, and copy the **Connection String**.
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL.
- `AZURE_OPENAI_CHAT_DEPLOYMENT`: Chat model deployment name.
- `AZURE_OPENAI_VERSION`: API version, for example `2024-08-01-preview`.
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key.

> [!NOTE]
> This sample uses API key authentication for simplicity. For production workloads, use `DefaultAzureCredential` with `get_bearer_token_provider` as shown in the LangChain v1 and LangGraph samples.

#### LangChain 0.3: Tracer and model setup

```python
import os
from dotenv import load_dotenv
from microsoft.opentelemetry import use_microsoft_opentelemetry
from langchain_openai import AzureChatOpenAI

load_dotenv(override=True)

# Enable Azure Monitor export and LangChain auto-instrumentation
use_microsoft_opentelemetry(
    enable_azure_monitor=True,
    sampling_ratio=1.0,
    instrumentation_options={
        "langchain": {
            "enabled": True,
            "agent_id": "trip_planner_orchestrator_v3",
            "agent_name": "Trip Planner Orchestrator",
        },
    },
)

# Model: Azure OpenAI
llm = AzureChatOpenAI(
    azure_deployment=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_version=os.environ.get("AZURE_OPENAI_VERSION"),
    temperature=0.2,
)
```

With the distro initialized, LangChain 0.3 operations are auto-instrumented globally. After you run your chain or agent, traces appear in the **Observability** > **Traces** view in the Foundry portal within 2-5 minutes.

## Configure tracing for OpenAI Agents SDK

The OpenAI Agents SDK supports OpenTelemetry instrumentation. Use the following snippet to configure tracing and export spans to Azure Monitor. If `APPLICATION_INSIGHTS_CONNECTION_STRING` isn't set, the exporter falls back to the console for local debugging.

Before you run the sample, install the required packages:

```bash
pip install opentelemetry-sdk opentelemetry-instrumentation-openai-agents azure-monitor-opentelemetry-exporter
```

```python
import os
from opentelemetry import trace
from opentelemetry.instrumentation.openai_agents import OpenAIAgentsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Configure tracer provider + exporter
resource = Resource.create({
    "service.name": os.getenv("OTEL_SERVICE_NAME", "openai-agents-app"),
})
provider = TracerProvider(resource=resource)

conn = os.getenv("APPLICATION_INSIGHTS_CONNECTION_STRING")
if conn:
    from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
    provider.add_span_processor(
        BatchSpanProcessor(AzureMonitorTraceExporter.from_connection_string(conn))
    )
else:
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

trace.set_tracer_provider(provider)

# Instrument the OpenAI Agents SDK
OpenAIAgentsInstrumentor().instrument(tracer_provider=trace.get_tracer_provider())

# Example: create a session span around your agent run
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("agent_session[openai.agents]"):
    # ... run your agent here
    pass
```

## Verify traces in the Foundry portal

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]
1. Confirm tracing is connected for your project. If needed, follow [Set up tracing in Microsoft Foundry](trace-agent-setup.md).
1. Run your agent at least once.
1. In the Foundry portal, go to **Observability** > **Traces**.
1. Confirm a new trace appears with spans for your agent's operations.

Traces typically appear within 2–5 minutes after agent execution. If traces still don't appear after this time, see [Troubleshoot common issues](#troubleshoot-common-issues).

## Troubleshoot common issues

| Issue | Cause | Resolution |
|---|---|---|
| You don't see traces in Foundry | Tracing isn't connected, there is no recent traffic, or ingestion is delayed | Confirm the Application Insights connection, generate new traffic, and refresh after 2–5 minutes. |
| You don't see LangChain or LangGraph spans | The Microsoft OpenTelemetry distro isn't initialized or LangChain instrumentation isn't enabled | Confirm you call `use_microsoft_opentelemetry(...)` with `"langchain": {"enabled": True}` before running your agent. |
| LangChain spans appear but tool calls are missing | Tools aren't bound to the model or tool node isn't configured | Verify tools are passed to `bind_tools()` on the model and that tool nodes are added to your graph. |
| Traces appear but are incomplete or missing spans | Content recording is disabled, the GenAI semantic convention opt-in isn't set, or some operations aren't instrumented | For LangChain and LangGraph, set `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_AND_EVENT`, `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`, and `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true` during development. For custom operations, add manual spans using the OpenTelemetry SDK. |
| You see authorization errors when you query telemetry | Missing RBAC permissions on Application Insights or Log Analytics | Confirm access in **Access control (IAM)** for the connected resources. For log queries, assign the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader). If the tables are [protected](/azure/azure-monitor/logs/protected-tables-configure), also assign [Privileged Monitoring Data Reader](/azure/azure-monitor/logs/manage-access?tabs=portal#privileged-monitoring-data-reader). |
| Sensitive content appears in traces | Content recording is enabled and prompts, tool arguments, or outputs include sensitive data | Disable content recording in production and redact sensitive data before it enters telemetry. |

## Related content

- Learn core concepts and architecture in the [Agent tracing overview](../concepts/trace-agent-concept.md).
- If you haven't enabled tracing yet, see [Set up tracing in Microsoft Foundry](trace-agent-setup.md).
- Visualize agent health and performance metrics with the [Agent Monitoring Dashboard](how-to-monitor-agents-dashboard.md).
- Explore the broader observability capabilities in [Observability in generative AI](../../concepts/observability.md).
