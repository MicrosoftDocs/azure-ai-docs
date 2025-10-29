---
title: Trace and Observe AI Agents in Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Trace and Observe AI Agents in Azure AI Foundry using OpenTelemetry. Learn to see execution traces, debug performance, and monitor AI agent behavior step-by-step.
author: yanchen-ms
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 09/29/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ai-usage: ai-assisted
ms.custom: references_regions
---

# Trace and Observe AI Agents in Azure AI Foundry (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this article, you learn how to:

- Understand key tracing concepts
- Trace and observe AI agents in AI Foundry
- Explore new semantic conventions with multi-agent observability
- Integrate with popular agent frameworks
- View traces in the AI Foundry portal and Azure Monitor
- View agent threads in the Agents playground

Determining the reasoning behind your agent's executions is important for troubleshooting and debugging. However, it can be difficult for complex agents for many reasons:

- There could be a high number of steps involved in generating a response, making it hard to keep track of all of them.
- The sequence of steps might vary based on user input.
- The inputs/outputs at each stage might be long and deserve more detailed inspection.
- Each step of an agent's runtime might also involve nesting. For example, an agent might invoke a tool, which uses another process, which then invokes another tool. If you notice strange or incorrect output from a top-level agent run, it might be difficult to determine exactly where in the execution the issue was introduced.

Trace results solve this by allowing you to view the inputs and outputs of each primitive involved in a particular agent run, displayed in the order they were invoked, making it easy to understand and debug your AI agent's behavior.

## Trace key concepts overview

Here's a brief overview of key concepts before getting started:

| Key concepts             | Description            |
|---------------------|-----------------------------------------------------------------|
| Traces              | Traces capture the journey of a request or workflow through your application by recording events and state changes (function calls, values, system events). See [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/). |
| Spans               | Spans are the building blocks of traces, representing single operations within a trace. Each span captures start and end times, attributes, and can be nested to show hierarchical relationships, allowing you to see the full call stack and sequence of operations.                                                                                         |
| Attributes          | Attributes are key-value pairs attached to traces and spans, providing contextual metadata such as function parameters, return values, or custom annotations. These enrich trace data making it more informative and useful for analysis.                                                                                                 |
| Semantic conventions| OpenTelemetry defines semantic conventions to standardize names and formats for trace data attributes, making it easier to interpret and analyze across tools and platforms. To learn more, see [OpenTelemetry's Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).                  |
| Trace exporters     | Trace exporters send trace data to backend systems for storage and analysis. Azure AI supports exporting traces to Azure Monitor and other OpenTelemetry-compatible platforms, enabling integration with various observability tools.   |

### Best practices

- Use consistent span attributes.
- Correlate evaluation run IDs for quality + performance analysis.
- Redact sensitive content; avoid storing secrets in attributes.
                                                                          
## Extending OpenTelemetry with multi-agent observability

Microsoft is enhancing multi-agent observability by introducing new semantic conventions to [OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/), developed collaboratively with Outshift, Cisco's incubation engine. These additions—built upon OpenTelemetry and W3C Trace Context—establish standardized practices for tracing and telemetry within multi-agent systems, facilitating consistent logging of key metrics for quality, performance, safety, and cost. This systematic approach enables more comprehensive visibility into multi-agent workflows, including tool invocations and collaboration.
These advancements have been integrated into Azure AI Foundry, Microsoft Agent Framework, Semantic Kernel, and Azure AI packages for LangChain, LangGraph, and the OpenAI Agents SDK, enabling customers to get unified observability for agentic systems built using any of these frameworks with Azure AI Foundry. Learn more about [tracing integrations](#integrations).

| Type         | Context/Parent Span   | Name/Attribute/Event           | Purpose |
|--------------|----------------------|-------------------------------|---------|
| Span         | —                    | execute_task                  | Captures task planning and event propagation, providing insights into how tasks are decomposed and distributed. |
| Child Span   | invoke_agent         | agent_to_agent_interaction    | Traces communication between agents. |
| Child Span   | invoke_agent         | agent.state.management        | Effective context, short or long term memory management. |
| Child Span   | invoke_agent         | agent_planning                | Logs the agent's internal planning steps. |
| Child Span   | invoke_agent         | agent orchestration           | Captures agent-to-agent orchestration. |
| Attribute    | invoke_agent         | tool_definitions              | Describes the tool's purpose or configuration. |
| Attribute    | invoke_agent         | llm_spans                     | Records model call spans. |
| Attribute    | execute_tool         | tool.call.arguments           | Logs the arguments passed during tool invocation. |
| Attribute    | execute_tool         | tool.call.results             | Records the results returned by the tool. |
| Event        | —                    | Evaluation (name, error.type, label) | Enables structured evaluation of agent performance and decision-making. |
                                                                          

## Set up tracing in Azure AI Foundry SDK

For chat completions or building agents with Azure AI Foundry, install:

```bash
pip install azure-ai-projects azure-identity
```

To instrument tracing, you need to install the following instrumentation libraries:

```bash
pip install azure-monitor-opentelemetry opentelemetry-sdk
```

To view traces in Azure AI Foundry, you need to connect an Application Insights resource to your Azure AI Foundry project.

1. Navigate to **Tracing** in the left navigation pane of the Azure AI Foundry portal.
2. Create a new Application Insights resource if you don't already have one.
3. Connect the resource to your AI Foundry project.

## Instrument tracing in your code

To trace the content of chat messages, set the `AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED` environment variable to true (case insensitive). Keep in mind this might contain personal data. To learn more, see [Azure Core Tracing OpenTelemetry client library for Python](/python/api/overview/azure/core-tracing-opentelemetry-readme).

```python
import os
os.environ["AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED"] = "true" # False by default
```
Let's begin instrumenting our agent with OpenTelemetry tracing by starting with authenticating and connecting to your Azure AI Project using the `AIProjectClient`.

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ["PROJECT_ENDPOINT"],
)
```

Next, retrieve the connection string from the Application Insights resource connected to your project and set up the OTLP exporters to send telemetry into Azure Monitor.

```python
from azure.monitor.opentelemetry import configure_azure_monitor

connection_string = project_client.telemetry.get_application_insights_connection_string()
configure_azure_monitor(connection_string=connection_string) #enable telemetry collection
```

Now, trace your code where you create and execute your agent and user message in your Azure AI Project, so you can see detailed steps for troubleshooting or monitoring.

```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("example-tracing"):
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-assistant",
        instructions="You are a helpful assistant"
    )
    thread = project_client.agents.threads.create()
    message = project_client.agents.messages.create(
        thread_id=thread.id, role="user", content="Tell me a joke"
    )
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
```

After running your agent, you can begin to [view traces in Azure AI Foundry Portal](#view-traces-in-the-azure-ai-foundry-portal).

### Log traces locally

To connect to [Aspire Dashboard](https://aspiredashboard.com/#start) or another OpenTelemetry compatible backend, install the OpenTelemetry Protocol (OTLP) exporter. This enables you to print traces to the console or use a local viewer such as Aspire Dashboard.

```bash
pip install azure-core-tracing-opentelemetry opentelemetry-exporter-otlp opentelemetry-sdk
```

Next, configure tracing for console output:

```python
from azure.core.settings import settings
settings.tracing_implementation = "opentelemetry"

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# Setup tracing to console
span_exporter = ConsoleSpanExporter()
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))
trace.set_tracer_provider(tracer_provider)
```

Or modify the above code, based on [Aspire Dashboard](https://aspiredashboard.com/#start), to trace to a local OTLP viewer.

Now enable Agent instrumentation and run your Agent:

```python
from azure.ai.agents.telemetry import AIAgentsInstrumentor
AIAgentsInstrumentor().instrument()

# Start tracing
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("example-tracing"):
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-assistant",
        instructions="You are a helpful assistant"
    )
    thread = project_client.agents.threads.create()
    message = project_client.agents.messages.create(
        thread_id=thread.id, role="user", content="Tell me a joke"
    )
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
```

### Alternative: AI Toolkit for VS Code

AI Toolkit gives you a simple way to trace locally in VS Code. It uses a local OTLP-compatible collector, making it ideal for development and debugging. 

The toolkit supports AI frameworks like Azure AI Foundry Agents Service, OpenAI, Anthropic, and LangChain through OpenTelemetry. You can see traces instantly in VS Code without needing cloud access.

For detailed setup instructions and SDK-specific code examples, see [Tracing in AI Toolkit](https://code.visualstudio.com/docs/intelligentapps/tracing).

## Trace custom functions

To trace your custom functions, use the OpenTelemetry SDK to instrument your code.

1. **Set up a tracer provider**: Initialize a tracer provider to manage and create spans.
2. **Create spans**: Wrap the code you want to trace with spans. Each span represents a unit of work and can be nested to form a trace tree.
3. **Add attributes**: Enrich spans with attributes to provide more context for the trace data.
4. **Configure an exporter**: Send the trace data to a backend for analysis and visualization.

Here's an example of tracing a custom function:

```python
from opentelemetry import trace
from opentelemetry.trace import SpanKind

# Initialize tracer
tracer = trace.get_tracer(__name__)

def custom_function():
    with tracer.start_as_current_span("custom_function") as span:
        span.set_attribute("custom_attribute", "value")
        # Your function logic here
        print("Executing custom function")

custom_function()
```

For detailed instructions and advanced usage, refer to the [OpenTelemetry documentation](https://opentelemetry.io/docs/).

## Attach user feedback to traces

To attach user feedback to traces and visualize it in the Azure AI Foundry portal, you can instrument your application to enable tracing and log user feedback using OpenTelemetry's semantic conventions.

By correlating feedback traces with their respective chat request traces using the response ID or thread ID, you can view and manage these traces in the Azure AI Foundry portal. OpenTelemetry's specification allows for standardized and enriched trace data, which can be analyzed in the Azure AI Foundry portal for performance optimization and user experience insights. This approach helps you use the full power of OpenTelemetry for enhanced observability in your applications.

To log user feedback, follow this format:

The user feedback evaluation event can be captured if and only if the user provided a reaction to the GenAI model response. It SHOULD, when possible, be parented to the GenAI span describing such response.


The user feedback event body has the following structure:

| Body Field | Type | Description | Examples | Requirement Level |
|---|---|---|---|---|
| `comment` | string | Additional details about the user feedback | `"I did not like it"` | `Opt-in` |

## Using service name in trace data

To identify your service via a unique ID in Application Insights, you can use the service name OpenTelemetry property in your trace data. This is useful if you're logging data from multiple applications to the same Application Insights resource, and you want to differentiate between them.

For example, let's say you have two applications: **App-1** and **App-2**, with tracing configured to log data to the same Application Insights resource. Perhaps you'd like to set up **App-1** to be evaluated continuously by **Relevance** and **App-2** to be evaluated continuously by **Relevance**. You can use the service name to filter by `Application` when monitoring your application in AI Foundry Portal.

To set up the service name property, you can do so directly in your application code by following the steps, see [Using multiple tracer providers with different Resource](https://opentelemetry.io/docs/languages/python/cookbook/#using-multiple-tracer-providers-with-different-resource). Alternatively, you can set the environment variable `OTEL_SERVICE_NAME` before deploying your app. To learn more about working with the service name, see [OTEL Environment Variables](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration) and [Service Resource Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/resource/#service).

To query trace data for a given service name, query for the `cloud_roleName` property.

```sql
| where cloud_RoleName == "service_name"
```

## Integrations

Azure AI Foundry makes it easy to log traces with minimal changes by using our tracing integrations with Microsoft Agent Framework, Semantic Kernel, LangChain, LangGraph, and OpenAI Agent SDK.

### Tracing agents built on Microsoft Agent Framework and Semantic Kernel

Azure AI Foundry has native integrations with Microsoft Agent Framework and Semantic Kernel. Agents built on these two frameworks get out-of-the-box tracing in Azure AI Foundry Observability.

- Learn more about tracing and observability in [Semantic Kernel](/semantic-kernel/concepts/enterprise-readiness/observability) and [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/user-guide/workflows/observability).


### Enable tracing for Agents built on LangChain & LangGraph

> [!NOTE]
> Tracing integration for LangChain and LangGraph described here is currently available only in Python.

You can enable tracing for LangChain that follows OpenTelemetry standards as per [opentelemetry-instrumentation-langchain](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/).

Once necessary packages are installed, you can easily begin to [Instrument tracing in your code](https://pypi.org/project/langchain-azure-ai/).

> [!NOTE]
> LangChain and LangGraph "v1" releases are currently under active development. API surface and tracing behavior can change as part of this release. Track updates at the [LangChain v1.0 release notes page](https://docs.langchain.com/oss/python/releases/langchain-v1)

#### Sample: LangChain v1 agent with Azure AI tracing

Use this end-to-end sample to instrument a LangChain v1 agent using the `langchain-azure-ai` tracer, which implements the latest OpenTelemetry (OTel) spec so you can view rich traces in Azure AI Foundry Observability.

##### Install packages

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

##### Configure environment

- `APPLICATION_INSIGHTS_CONNECTION_STRING`: Azure Monitor Application Insights connection string for tracing.
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL.
- `AZURE_OPENAI_CHAT_DEPLOYMENT`: The chat model deployment name.
- `AZURE_OPENAI_VERSION`: API version, for example `2024-08-01-preview`.
- Azure credentials are resolved via `DefaultAzureCredential` (supports environment variables, managed identity, VS Code sign-in, etc.).

You can store these in a `.env` file for local development.

##### Tracer setup

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

##### Model setup (Azure OpenAI)

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

##### Define tools and prompt

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

##### Use runtime context and define a user-info tool

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

##### Create the agent

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

##### Run the agent with tracing

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

With `langchain-azure-ai` enabled, all LangChain v1 operations (LLM calls, tool invocations, agent steps) are traced using the latest OpenTelemetry semantic conventions and appear in Azure AI Foundry Observability, linked to your Application Insights resource.

#### Sample: LangGraph agent with Azure AI tracing

This sample shows a simple LangGraph agent instrumented with `langchain-azure-ai` to emit OpenTelemetry-compliant traces for graph steps, tool calls, and model invocations.

##### Install packages

```bash
pip install \
  langchain-azure-ai \
  langgraph==1.0.0a4 \
  langchain==1.0.0a10 \
  langchain-openai \
  azure-identity \
  python-dotenv
```

##### Configure environment

- `APPLICATION_INSIGHTS_CONNECTION_STRING`: Azure Monitor Application Insights connection string for tracing.
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL.
- `AZURE_OPENAI_CHAT_DEPLOYMENT`: The chat model deployment name.
- `AZURE_OPENAI_VERSION`: API version, for example `2024-08-01-preview`.

You can store these in a `.env` file for local development.

##### Tracer setup

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

##### Tools

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

##### Model setup (Azure OpenAI)

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

##### Build the LangGraph workflow

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

##### Run with tracing

```python
from langchain_core.messages import HumanMessage

config = {"configurable": {"thread_id": "1"}, "callbacks": [azure_tracer]}
input_message = HumanMessage(content="Can you play Taylor Swift's most popular song?")

for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()
```

With `langchain-azure-ai` enabled, your LangGraph execution emits OpenTelemetry-compliant spans for model calls, tool invocations, and graph transitions. These traces flow to Application Insights and surface in Azure AI Foundry Observability.

#### Sample: LangChain 0.3 setup with Azure AI tracing

This minimal setup shows how to enable Azure AI tracing in a LangChain 0.3 application using the `langchain-azure-ai` tracer and `AzureChatOpenAI`.

##### Install packages

```bash
pip install \
  "langchain>=0.3,<0.4" \
  langchain-openai \
  langchain-azure-ai \
  python-dotenv
```

##### Configure environment

- `APPLICATION_INSIGHTS_CONNECTION_STRING`: Application Insights connection string for tracing.
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL.
- `AZURE_OPENAI_CHAT_DEPLOYMENT`: Chat model deployment name.
- `AZURE_OPENAI_VERSION`: API version, for example `2024-08-01-preview`.
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key.

##### Tracer and model setup

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

Attach `callbacks=[azure_tracer]` to your chains, tools, or agents to ensure LangChain 0.3 operations are traced and visible in Azure AI Foundry Observability.

### Enable tracing for Agents built on OpenAI Agents SDK

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

## View traces in the Azure AI Foundry portal

In your project, go to **Tracing** to filter your traces as you see fit.

By selecting a trace, you can step through each span and identify issues while observing how your application is responding. This can help you debug and pinpoint issues in your application.

## View traces in Azure Monitor

If you logged traces using the previous code snippet, then you're all set to view your traces in Azure Monitor Application Insights. You can open Application Insights from **Manage data source** and use the **End-to-end transaction details view** to further investigate.

For more information on how to send Azure AI Inference traces to Azure Monitor and create Azure Monitor resource, see [Azure Monitor OpenTelemetry documentation](/azure/azure-monitor/app/opentelemetry-enable).

## View thread results in the Azure AI Foundry Agents playground

The Agents playground in the Azure AI Foundry portal lets you view results for threads and runs that your agents produce. To see thread results, select **Thread logs** in an active thread. You can also optionally select **Metrics** to enable automatic evaluations of the model's performance across several dimensions of **AI quality** and **Risk and safety**.

> [!NOTE]
> Evaluation in the playground is billed as outlined under Trust and Azure AI Foundry Observability on [the pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/?msockid=1f44c87dd9fa6d1e257fdd6dd8406c42). Results are available for 24 hours before expiring. To get evaluation results, select your desired metrics and chat with your agent.
> - Evaluations aren't available in the following regions.
>     - `australiaeast`
>     - `japaneast`
>     - `southindia`
>     - `uksouth`

:::image type="content" source="../../media/trace/trace-agent-playground.png" alt-text="A screenshot of the agent playground in the Azure AI Foundry portal." lightbox="../../media/trace/trace-agent-playground.png":::

After selecting **Thread logs**, review:

- Thread details
- Run information
- Ordered run steps and tool calls
- Inputs and outputs between user and agent
- Linked evaluation metrics (if enabled)

:::image type="content" source="../../agents/media/thread-trace.png" alt-text="A screenshot of a trace." lightbox="../../agents/media/thread-trace.png":::

> [!TIP]
> If you want to view thread results from a previous thread, select **My threads** in the **Agents** screen. Choose a thread, and then select **Try in playground**.
> :::image type="content" source="../../agents/media/thread-highlight.png" alt-text="A screenshot of the threads screen." lightbox="../../agents/media/thread-highlight.png":::
> You'll be able to see the **Thread logs** button at the top of the screen to view the thread results.

> [!NOTE]
> Observability features such as Risk and Safety Evaluation are billed based on consumption as listed in the [Azure pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/).

## Related content

- [Python samples](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/samples/sample_chat_completions_with_tracing.py) containing fully runnable Python code for tracing using synchronous and asynchronous clients.
- [Python samples for tracing agents with console tracing and Azure Monitor](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-agents/samples/agents_telemetry)
- [JavaScript samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples/v1-beta/typescript/src) containing fully runnable JavaScript code for tracing using synchronous and asynchronous clients.
- [C# Samples](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.Inference_1.0.0-beta.2/sdk/ai/Azure.AI.Inference/samples/Sample8_ChatCompletionsWithOpenTelemetry.md) containing fully runnable C# code for doing inference using synchronous and asynchronous methods.
