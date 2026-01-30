---
title: Tracing integrations for agent frameworks
titleSuffix: Microsoft Foundry
description: Set up agent tracing integrations in Microsoft Foundry for Microsoft Agent Framework, Semantic Kernel, LangChain, LangGraph, and OpenAI Agents SDK.
ai-usage: ai-assisted
author: yanchen-ms
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 01/20/2026
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom: pilot-ai-workflow-jan-2026
---
# Tracing integrations (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

Microsoft Foundry makes it easy to capture agent traces with minimal code changes by using integrations with Microsoft Agent Framework, Semantic Kernel, LangChain, LangGraph, and OpenAI Agents SDK.

## Prerequisites

- A Foundry project. For more information, see [Create a Foundry project](../../../how-to/create-projects.md).
- Tracing connected to an Azure Monitor Application Insights resource. To set it up, see [Set up tracing in Microsoft Foundry](trace-agent-setup.md).
- Access to the connected Application Insights resource. For log-based queries, you might also need access to the associated Log Analytics workspace.
- If you use LangChain or LangGraph, a Python environment.

### Confirm you can view telemetry

To view trace data, make sure your account has access to the connected Application Insights resource.

1. In the Azure portal, open the Application Insights resource connected to your Foundry project.
1. Select **Access control (IAM)**.
1. Assign an appropriate role to your user or group.

    If you use log-based queries, start by granting the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader).

## Security and privacy

Tracing can capture sensitive information (for example, user inputs, model outputs, and tool arguments and results).

- Enable content recording only when you need it. In the samples in this article, this is controlled by settings like `enable_content_recording` and `OTEL_RECORD_CONTENT`.
- Don't store secrets, credentials, or tokens in prompts or tool arguments.

For more guidance, see [Security and privacy](../concepts/trace-agent-concept.md#security-and-privacy).

## Microsoft Agent Framework

Foundry has native integrations with Microsoft Agent Framework. Agents built with Microsoft Agent Framework get out-of-the-box tracing in observability after you enable tracing for your Foundry project.

To learn more about tracing and observability in Microsoft Agent Framework, see [Microsoft Agent Framework Workflows - Observability](/agent-framework/user-guide/workflows/observability).

## Semantic Kernel

Foundry has native integrations with Semantic Kernel. Agents built with Semantic Kernel get out-of-the-box tracing in observability after you enable tracing for your Foundry project.

Learn more about tracing and observability in [Semantic Kernel](/semantic-kernel/concepts/enterprise-readiness/observability).

## LangChain & LangGraph

> [!NOTE]
> Tracing integration for LangChain and LangGraph is currently available only in Python.
> LangChain and LangGraph "v1" releases are currently under active development. API surface and tracing behavior can change as part of this release. Track updates at the [LangChain v1.0 release notes page](https://docs.langchain.com/oss/python/releases/langchain-v1).

Use the `langchain-azure-ai` package to emit OpenTelemetry-compliant spans for LangChain and LangGraph operations so you can view rich traces in Foundry.

- OpenTelemetry semantic conventions: <https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/>
- Package and usage guidance: <https://pypi.org/project/langchain-azure-ai/>

### Sample: LangChain v1 agent with Azure AI tracing

Use this end-to-end sample to instrument a LangChain v1 agent using the `langchain-azure-ai` tracer, which implements the latest OpenTelemetry (OTel) spec so you can view rich traces in Observability.

#### LangChain v1: Install packages

```bash
pip install \
  langchain-azure-ai \
  langchain \
  langgraph \
  langchain-openai \
  azure-identity \
  python-dotenv \
  rich
```

#### LangChain v1: Configure environment

- `APPLICATION_INSIGHTS_CONNECTION_STRING`: Azure Monitor Application Insights connection string for tracing.
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL.
- `AZURE_OPENAI_CHAT_DEPLOYMENT`: The chat model deployment name.
- `AZURE_OPENAI_VERSION`: API version, for example `2024-08-01-preview`.
- Azure credentials are resolved via `DefaultAzureCredential` (supports environment variables, managed identity, VS Code sign-in, etc.).

You can store these in a `.env` file for local development.

#### LangChain v1: Tracer setup

```python
from dotenv import load_dotenv
import os
from langchain_azure_ai.callbacks.tracers import AzureAIOpenTelemetryTracer

load_dotenv(override=True)

azure_tracer = AzureAIOpenTelemetryTracer(
    connection_string=os.environ.get("APPLICATION_INSIGHTS_CONNECTION_STRING"),
    enable_content_recording=True,
    name="Weather information agent",
    id="weather_info_agent_771929",
)

tracers = [azure_tracer]
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
    config = {"configurable": {"thread_id": "1"}, "callbacks": [azure_tracer]}
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

With `langchain-azure-ai` enabled, all LangChain v1 operations (LLM calls, tool invocations, agent steps) are traced using the latest OpenTelemetry semantic conventions and appear in Observability, linked to your Application Insights resource.

### Sample: LangGraph agent with Azure AI tracing

This sample shows a simple LangGraph agent instrumented with `langchain-azure-ai` to emit OpenTelemetry-compliant traces for graph steps, tool calls, and model invocations.

#### LangGraph: Install packages

```bash
pip install \
  langchain-azure-ai \
  langgraph==1.0.0a4 \
  langchain==1.0.0a10 \
  langchain-openai \
  azure-identity \
  python-dotenv
```

#### LangGraph: Configure environment

- `APPLICATION_INSIGHTS_CONNECTION_STRING`: Azure Monitor Application Insights connection string for tracing.
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL.
- `AZURE_OPENAI_CHAT_DEPLOYMENT`: The chat model deployment name.
- `AZURE_OPENAI_VERSION`: API version, for example `2024-08-01-preview`.

You can store these in a `.env` file for local development.

#### LangGraph tracer setup

```python
import os
from dotenv import load_dotenv
from langchain_azure_ai.callbacks.tracers import AzureAIOpenTelemetryTracer

load_dotenv(override=True)

azure_tracer = AzureAIOpenTelemetryTracer(
    connection_string=os.environ.get("APPLICATION_INSIGHTS_CONNECTION_STRING"),
    enable_content_recording=os.getenv("OTEL_RECORD_CONTENT", "true").lower() == "true",
    name="Music Player Agent",
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

config = {"configurable": {"thread_id": "1"}, "callbacks": [azure_tracer]}
input_message = HumanMessage(content="Can you play Taylor Swift's most popular song?")

for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()
```

With `langchain-azure-ai` enabled, your LangGraph execution emits OpenTelemetry-compliant spans for model calls, tool invocations, and graph transitions. These traces flow to Application Insights and surface in Observability.

### Sample: LangChain 0.3 setup with Azure AI tracing

This minimal setup shows how to enable Azure AI tracing in a LangChain 0.3 application using the `langchain-azure-ai` tracer and `AzureChatOpenAI`.

#### LangChain 0.3: Install packages

```bash
pip install \
  "langchain>=0.3,<0.4" \
  langchain-openai \
  langchain-azure-ai \
  python-dotenv
```

#### LangChain 0.3: Configure environment

- `APPLICATION_INSIGHTS_CONNECTION_STRING`: Application Insights connection string for tracing.
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL.
- `AZURE_OPENAI_CHAT_DEPLOYMENT`: Chat model deployment name.
- `AZURE_OPENAI_VERSION`: API version, for example `2024-08-01-preview`.
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key.

#### LangChain 0.3: Tracer and model setup

```python
import os
from dotenv import load_dotenv
from langchain_azure_ai.callbacks.tracers import AzureAIOpenTelemetryTracer
from langchain_openai import AzureChatOpenAI

load_dotenv(override=True)

# Tracer: emits spans conforming to updated OTel spec
azure_tracer = AzureAIOpenTelemetryTracer(
    connection_string=os.environ.get("APPLICATION_INSIGHTS_CONNECTION_STRING"),
    enable_content_recording=True,
    name="Trip Planner Orchestrator",
    id="trip_planner_orchestrator_v3",
)
tracers = [azure_tracer]

# Model: Azure OpenAI with callbacks for tracing
llm = AzureChatOpenAI(
    azure_deployment=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_version=os.environ.get("AZURE_OPENAI_VERSION"),
    temperature=0.2,
    callbacks=tracers,
)
```

Attach `callbacks=[azure_tracer]` to your chains, tools, or agents to ensure LangChain 0.3 operations are traced and visible in Observability.

## OpenAI Agents SDK

Use this snippet to configure OpenTelemetry tracing for the OpenAI Agents SDK and instrument the framework. It exports to Azure Monitor if `APPLICATION_INSIGHTS_CONNECTION_STRING` is set; otherwise, it falls back to the console.

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

## Verify traces appear

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]
1. Confirm tracing is connected for your project. If needed, follow [Set up tracing in Microsoft Foundry](trace-agent-setup.md).
1. Run your agent at least once.
1. In your Foundry project, open the traces view and confirm a new trace appears.

If you don't see new traces, wait a few minutes and refresh, and then see [Troubleshooting](#troubleshooting).

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| You don't see traces in Foundry | Tracing isn't connected, there is no recent traffic, or ingestion is delayed | Confirm the Application Insights connection, generate new traffic, and refresh after a few minutes. |
| You don't see LangChain or LangGraph spans | Tracing callbacks aren't attached to the run | Confirm you pass the tracer in `callbacks` (for example, `config = {"callbacks": [azure_tracer]}`) for the run you want to trace. |
| You see authorization errors when you query telemetry | Missing RBAC permissions on Application Insights or Log Analytics | Confirm access in **Access control (IAM)** for the connected resources. For log queries, assign the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader). |
| Sensitive content appears in traces | Content recording is enabled and prompts, tool arguments, or outputs include sensitive data | Disable content recording when you don't need it and redact sensitive data before it enters telemetry. |

## Next steps

- [Agent tracing overview](../concepts/trace-agent-concept.md)
- [Set up tracing in Microsoft Foundry](trace-agent-setup.md)
- [Monitor AI agents with the Agent Monitoring Dashboard](how-to-monitor-agents-dashboard.md)
- [Observability in generative AI](../../../concepts/observability.md)
