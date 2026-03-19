---
title: Trace LangChain and LangGraph apps with Microsoft Foundry and Azure Monitor
description: Learn how to trace LangChain and LangGraph applications in Foundry with the AzureAIOpenTelemetryTracer callback handler.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 03/05/2026
ms.author: fasantia
author: santiagxf
ms.reviewer: sgilley
ms.custom:
  - dev-focus
ai-usage: ai-assisted
# customer intent: As a developer, I want to trace my LangChain and LangGraph applications with langchain-azure-ai so that I can inspect execution, tool calls, and model usage in Azure Monitor.
---

# Trace LangChain and LangGraph apps with Microsoft Foundry and Azure Monitor

Use the `langchain-azure-ai` integration package to emit OpenTelemetry traces from LangChain and
LangGraph applications and sink them in Azure Application Insights. In this article, you configure
`AzureAIOpenTelemetryTracer`, attach it to your runnable, and inspect traces in
Azure Monitor.

The tracer emits spans for agent execution, model calls, tool execution, and
retrieval operations. You can use it for apps that run fully local, hybrid
flows that call Foundry Agent Service, or multi-agent LangGraph solutions.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- A [Foundry project](../create-projects.md).
- A deployed Azure OpenAI chat model (for example, `gpt-4.1`).
- Python 3.10 or later.
- Azure CLI signed in (`az login`) so `DefaultAzureCredential` can
  authenticate.

### Configure your environment

Install required packages:

```bash
pip install -U "langchain-azure-ai[opentelemetry]" azure-identity
```

Set the environment variables used in this article:

```python
import os

# Option 1: Project endpoint (recommended)
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = (
	"https://<resource>.services.ai.azure.com/api/projects/<project>"
)

# Option 2: Direct OpenAI-compatible endpoint + API key
os.environ["OPENAI_BASE_URL"] = (
	"https://<resource>.services.ai.azure.com/openai/v1"
)
os.environ["OPENAI_API_KEY"] = "<your-api-key>"
os.environ["APPLICATION_INSIGHTS_CONNECTION_STRING"] = "InstrumentationKey=0ab1c2d3..."
```

To control whether content from messages and tool calls is recorded in the trace,
pass `enable_content_recording` to the `AzureAIOpenTelemetryTracer` constructor.
Content recording is enabled by default.

> [!TIP]
> Set `enable_content_recording=False` in the `AzureAIOpenTelemetryTracer` constructor
> to redact message content and tool call arguments from traces.

## Create the tracer

Create one tracer instance and reuse it across your workflow.

```python
import os

from azure.identity import DefaultAzureCredential
from langchain_azure_ai.callbacks.tracers import AzureAIOpenTelemetryTracer

tracer = AzureAIOpenTelemetryTracer(
	project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
	credential=DefaultAzureCredential(),
	name="langchain-tracing-sample",
	agent_id="support-bot",
	trace_all_langgraph_nodes=True,
)
```

**What this snippet does:** Configures a tracer that resolves the associated
Application Insights connection string from your Foundry project endpoint and
enables tracing for LangGraph nodes. Use `agent_id` parameter to set the attribute
`gen_ai.agent.id` when invoking agents. The `name` parameter sets the
OpenTelemetry tracer name.

The tracer supports common controls for production workflows:

- Pass `connection_string` to target a specific Application Insights resource or by configuring
  the environment variable `APPLICATION_INSIGHTS_CONNECTION_STRING`.
- Set `trace_all_langgraph_nodes=True` to trace all nodes by default.
- Use node metadata like `otel_trace: True` or `otel_trace: False` to include
  or skip specific nodes.
- Use `message_keys` and `message_paths` when your messages are nested under a
  custom state shape, for example `chat_history`.

Reference:
- [AzureAIOpenTelemetryTracer](https://python.langchain.com/api_reference/azure_ai/callbacks/langchain_azure_ai.callbacks.tracers.inference_tracing.AzureAIOpenTelemetryTracer.html)

## Trace an agent

Start with a minimal LangChain agent so you can verify tracing quickly. For 
LangGraph, attach the tracer with `with_config` on the compiled graph.

```python
from langchain.agents import create_agent

agent = create_agent(
    model="azure_ai:gpt-5.2", 
    system_prompt="You're an informational agent. Answer questions cheerfully.", 
).with_config(
    {"callbacks": [tracer]}
)

response = agent.invoke({"messages": "what's your name?"})
response["messages"][-1].pretty_print()
```

```output
================================== Ai Message ==================================

I’m ChatGPT, your AI assistant.
```

**What this snippet does:** Creates a simple LangGraph agent, attach
the tracer, and invokes the agent with a message.

Reference:
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [OpenTelemetry](https://opentelemetry.io/docs/)

## Trace a LangChain runnable

Start with a minimal LangChain flow so you can verify tracing quickly.

```python
import os

from azure.identity import DefaultAzureCredential
from langchain_core.prompts import ChatPromptTemplate
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
	endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
	credential=DefaultAzureCredential(),
	model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
)

prompt = ChatPromptTemplate.from_template(
	"You are concise. Answer in one sentence: {question}"
)
chain = prompt | model

response = chain.invoke(
	{"question": "What does OpenTelemetry help me do?"},
	config={"callbacks": [tracer]},
)

print(response.content)
```

```output
OpenTelemetry helps you observe requests, latency, dependencies, and failures across your AI workflow.
```

**What this snippet does:** Runs a standard LangChain pipeline and sends chat
spans to OpenTelemetry through `AzureAIOpenTelemetryTracer`.

Reference:
- [AzureAIChatCompletionsModel](https://python.langchain.com/api_reference/azure_ai/chat_models/langchain_azure_ai.chat_models.inference.AzureAIChatCompletionsModel.html)
- [ChatPromptTemplate](https://python.langchain.com/api_reference/core/prompts/langchain_core.prompts.chat.ChatPromptTemplate.html)

## Trace a LangGraph graph

For LangGraph, attach the tracer with `with_config` on the compiled graph.
This snippet reuses `model` and `tracer` from earlier examples.

```python
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_azure_ai.utils.agents import pretty_print

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

tool_node = ToolNode([play_song_on_apple, play_song_on_spotify])
model_with_tools = model.bind_tools([play_song_on_apple, play_song_on_spotify])

def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    return "continue" if getattr(last_message, "tool_calls", None) else "end"

def call_model(state: MessagesState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

memory = MemorySaver()
workflow = (
    StateGraph(MessagesState)
    .add_node("agent", call_model)
    .add_node("action", tool_node)
    .add_edge(START, "agent")
    .add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "action",
            "end": END,
        },
    )
    .add_edge("action", "agent")
    .compile(checkpointer=memory)
)
```

Then, you can run the graph as usual:

```python
from langchain_core.messages import HumanMessage

config = {"configurable": {"thread_id": "1"}, "callbacks": [tracer]}
message = HumanMessage(content="Can you play Taylor Swift's most popular song?")

result = workflow.invoke({"messages": [message]}, config)
pretty_print(result)
```

```output
================================ Human Message =================================

Can you play Taylor Swift's most popular song?
================================== Ai Message ==================================
Tool Calls:
  play_song_on_spotify (call_xxx)
 Call ID: call_xxx
  Args:
    song: Anti-Hero
================================= Tool Message =================================
Name: play_song_on_spotify

Successfully played Anti-Hero on Spotify!
================================== Ai Message ==================================

I played Taylor Swift's popular song "Anti-Hero" on Spotify.
```

**What this snippet does:** Creates a simple LangGraph app, marks the node for
tracing, and emits `invoke_agent` and model/tool spans into the same trace.

Reference:
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [OpenTelemetry](https://opentelemetry.io/docs/)

## Understand trace structure

The tracer emits spans that follow the [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/).
Each span type uses a specific `gen_ai.operation.name` value:

| Span type | `gen_ai.operation.name` | Description |
|---|---|---|
| Agent/chain invocation | `invoke_agent` | Each LangGraph node or chain step. Span name is `invoke_agent {gen_ai.agent.name}`. |
| Chat model call | `chat` | LLM inference requests. Span name is `chat {gen_ai.request.model}`. |
| Text completion | `text_completion` | Non-chat LLM calls. |
| Tool execution | `execute_tool` | Tool calls triggered by the model. Span name is `execute_tool {gen_ai.tool.name}`. |
| Retriever | `execute_tool` | Retrieval operations from vector stores or search. |

Spans also carry these key attributes:

- `gen_ai.agent.name` — The agent or node name.
- `gen_ai.agent.id` — Set from the `agent_id` constructor parameter.
- `gen_ai.agent.description` — A description of the agent.
- `gen_ai.provider.name` — The model provider (for example, `openai`, `azure.ai.inference`).
- `gen_ai.request.model` — The model name used for inference.
- `gen_ai.conversation.id` — Thread or session identifier, when available.
- `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens` — Token counts from model responses.
- `gen_ai.input.messages` / `gen_ai.output.messages` — Message content (when content recording is enabled).

### How the tracer resolves `gen_ai.agent.name`

The tracer resolves the agent name from the first non-empty value in this order:

1. `agent_name` in the node metadata.
2. `langgraph_node` in the node metadata (set automatically by LangGraph).
3. `agent_type` in the node metadata.
4. The `name` keyword argument from the LangChain callback.
5. `langgraph_path` (last element) if the above are generic placeholders.
6. The serialized chain ID or class name.
7. The `name` parameter from the `AzureAIOpenTelemetryTracer` constructor (fallback default).

### How the tracer resolves `gen_ai.agent.id`

The tracer resolves the agent ID from:

1. `agent_id` in the node metadata (per-node override).
2. The `agent_id` constructor parameter (default for all spans).

### Customize attributes with node metadata

You can set `agent_name`, `agent_id`, and `agent_description` per node using
LangGraph metadata. Any metadata key starting with `gen_ai.` is also forwarded
as a span attribute.

```python
config = {
    "callbacks": [tracer],
    "metadata": {
        "agent_name": "support-bot",
        "agent_id": "support-bot-v2",
        "agent_description": "Handles customer support requests",
        "thread_id": "session-abc-123",
    },
}
result = graph.invoke({"messages": [message]}, config)
```

When using LangGraph, you can also set metadata per node in the graph definition:

```python
workflow = StateGraph(MessagesState)
workflow.add_node(
    "planner",
    planner_fn,
    metadata={
        "agent_name": "PlannerAgent",
        "agent_id": "planner-v1",
        "otel_agent_span": True,
    },
)
```

Reference:
- [OpenTelemetry GenAI Agent Spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)
- [OpenTelemetry GenAI Spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/)

## View traces in Azure Monitor

Traces are sent to Azure Application Insights and can be queried using Azure Monitor:

1. Go to the [Azure portal](https://portal.azure.com).

2. Navigate to the Azure Application Insights you configured.

3. Using the left navigation bar, select **Investigate** > **Agents (Preview)**.

4. You see a dashboard showing agent, model, and tool executions. Use this view to understand the overall activity of your agents.

5. Select **View Traces with Agent Runs**. The side panel shows all the traces generated by agent runs.

	:::image type="content" source="../media/langchain-agents/langchain-monitor-runs.png" lightbox="../media/langchain-agents/langchain-monitor-runs.png" alt-text="Screenshot showing the Agents (Preview) section in Azure Monitor displaying multiple runs.":::

6. Select one of the traces. You should see the details.

	:::image type="content" source="../media/langchain-agents/langchain-monitor-trace.png" lightbox="../media/langchain-agents/langchain-monitor-trace.png" alt-text="Screenshot showing the trace details of the selected run.":::

## View traces in Foundry Control Plane

If you deployed your LangGraph or LangChain solution, you can register that deployment into [Foundry Control Plane](../../control-plane/overview.md)
to gain visibility and governance.

[Register your application into Foundry Control Plane](../../control-plane/register-custom-agent.md) to view traces in the Foundry portal. 

Follow these steps:

1. Ensure that you meet the requirements to use the Foundry Control Plane custom agent capability:

    - An [AI gateway configured in your Foundry resource](../../configuration/enable-ai-api-management-gateway-portal.md#create-an-ai-gateway). Foundry uses Azure API Management to register agents as APIs.

    - An agent that you deploy and expose through a reachable endpoint. The endpoint can be either a public endpoint or an endpoint that's reachable from the network where you deploy the Foundry resource.

2. Ensure that you have [observability configured in the project](../../control-plane/monitoring-across-fleet.md).

3. When configuring the class `AzureAIOpenTelemetryTracer`, make sure to use the project's endpoint you want the agent to be registered at. Ensure you configure `agent_id`.

4. Go to the [Foundry portal](https://ai.azure.com).

5. On the toolbar, select **Operate**.

6. On the **Overview** pane, select **Register agent**.

7. The registration wizard appears. First, complete the details about the agent that you want to register.

    - **Agent URL**: The endpoint (URL) where your agent runs and receives requests.
    - **Protocol**: The communication protocol that your agent supports.
    - **OpenTelemetry Agent ID**: The `agent_id` parameter that you configured in the `AzureAIOpenTelemetryTracer` class.
    - **Project**: The project that you configured to receive traces in the `AzureAIOpenTelemetryTracer` class.
    - **Agent name**: The name of the agent (it can be the same as `agent_id`).

8. Invoke the agent to make sure it has runs.

9. On the toolbar, select **Operate**.

10. On the left pane, select **Assets**.

11. Select the agent you created.

12. The **Traces** section shows one entry for each HTTP call made to the agent's endpoint.

    To see the details, select an entry.

    :::image type="content" source="../../control-plane/media/register-custom-agent/custom-agent-trace.png" alt-text="Screenshot of a call to the agent's endpoint under the route for runs and streams." lightbox="../../control-plane/media/register-custom-agent/custom-agent-trace.png":::

## Troubleshoot

- If no traces appear, verify that either `connection_string` is configured or
  your project endpoint exposes telemetry.
- If message content appears redacted, set
  `enable_content_recording=True` in the `AzureAIOpenTelemetryTracer` constructor.
- If some LangGraph nodes are missing, set `trace_all_langgraph_nodes=True` or
  add node metadata `otel_trace: True`.

> [!div class="nextstepaction"]
> [Use Foundry Memory with LangChain and LangGraph](langchain-memory.md)

## Related content

- [Get started with langchain-azure-ai](langchain.md)
- [Use LangGraph with the Agent Service](langchain-agents.md)
- [Set up tracing integrations for agent frameworks](../../observability/how-to/trace-agent-framework.md)
