---
title: "Register and manage custom agents in Microsoft Foundry Control Plane"
description: "Learn how to register a custom agent in Microsoft Foundry Control Plane for management and observability."
author: santiagxf
ms.author: scottpolly
ms.reviewer: fasantia
ms.date: 02/04/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Register and manage custom agents

The Microsoft Foundry Control Plane provides centralized management and observability for agents running across different platforms and infrastructures. You can register custom agents running in Azure compute services or other cloud environments to gain visibility into their operations and control their behavior.

This article shows you how to register a custom agent in the Foundry Control Plane. You learn how to configure your agent for registration, set up telemetry collection, and use the Control Plane's management capabilities.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

Before getting started, make sure you have:

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]

- Foundry uses Azure API Management to register agents as APIs. [Configure AI Gateway in your Foundry resource](../configuration/enable-ai-api-management-gateway-portal.md#create-an-ai-gateway).

- An agent that you deploy and expose through a reachable endpoint (either a public endpoint or an endpoint reachable from the network where you deploy the Foundry resource).

[!INCLUDE [capability-new-portal](../includes/capability-new-portal.md)]

## Add a custom agent

You can register a custom agent in the Control Plane. Develop the agent in the technology of your choice, both platform and infrastructure solutions. 

When you register a custom agent, Foundry uses Azure API Management to act as a proxy for communications to your agent, so it can control access and monitor activity. 

When you register a custom agent, the resulting architecture is as follows:

:::image type="content" source="media/register-custom-agent/custom-agent-architecture.png" alt-text="A diagram showing the resulting architecture once a custom agent is registered and configured." lightbox="media/register-custom-agent/custom-agent-architecture.png":::

### Verify your agent

Verify that your agent meets the requirements for registration:

> [!div class="checklist"]
> * Your agent exposes an exclusive endpoint.
> * The network where you deploy the Foundry resource can reach the agent's endpoint.
> * The agent communicates by using one of the supported protocols: either general HTTP or specifically A2A.
> * Your agent emits telemetry by using the OpenTelemetry semantic conventions for GenAI solutions (or you don't need this capability).
> * You can configure the endpoint that end users use to communicate with the agent. Once you register an agent in Control Plane, it generates a new URL. **Clients and end users must use this URL to communicate with the agent**.

### Prepare your Foundry project

Add custom agents to Foundry projects. Before registering the agent, make sure you configured the project correctly.

1. [!INCLUDE [foundry-sign-in](../../default/includes/foundry-sign-in.md)]

1. Ensure AI Gateway is configured in your project:

    1. Select **Operate** > **Admin console**.

    1. Open the **AI Gateway** tab.

    1. The page lists all the AI Gateways configured and mapped to a Foundry resource. Check if the Foundry resource you want to use has an AI Gateway associated.

        :::image type="content" source="media/register-custom-agent/verify-ai-gateway.png" alt-text="Screenshot of the Foundry administration portal showing how to verify if your project has AI Gateway configured." lightbox="media/register-custom-agent/verify-ai-gateway.png":::

    1. If the Foundry resource you want to use doesn't have an AI Gateway configured (it isn't listed), add one by using the **Add AI Gateway** option. AI Gateway is free to set up and unlocks powerful governance features like security, telemetry, and rate limits for your agents, tools, and models.

    1. For more details about how to configure AI Gateway, see [Create an AI Gateway](../configuration/enable-ai-api-management-gateway-portal.md#create-an-ai-gateway).

1. Ensure you have observability configured in the project. Control Plane uses the Azure Application Insights resource associated with your selected project for emitting telemetry to help you diagnose your agent:
    
    1. Select **Operate** > **Admin console**.

    1. Under **All projects**, use the search box to look for your project.

    1. Select the project.
    
    1. Select the tab **Connected resources**.

    1. Ensure there is a resource associated under the category **Application Insights**.

        :::image type="content" source="media/register-custom-agent/verify-app-insights.png" alt-text="Screenshot of the administration portal showing how to verify if your project has an Azure Application Insights associated." lightbox="media/register-custom-agent/verify-app-insights.png":::

    1. If there's no resource associated, add one by selecting **Add connection** and select **Application Insights**.

    1. Your project is configured for observability and tracing.

### Register the agent

To register the agent, follow these steps:

1. Select **Operate** from the upper-right navigation.

1. Select the **Overview** pane.

1. Select **Register agent**.

    :::image type="content" source="media/register-custom-agent/register-custom-agent.png" alt-text="Screenshot of the Register agent button in the Foundry portal Overview pane." lightbox="media/register-custom-agent/register-custom-agent.png":::

1. The registration wizard appears. First, complete the details about the agent you want to register. The following properties describe the agent as it runs on its platform

    | Property  | Description | Required |
    |-----------|-------------|----------|
    | **Agent URL** | It represents the endpoint (URL) where your agent runs and receives requests. In general, but depending on your protocol, you indicate the base URL that your clients use. For example, if your agent talks OpenAI Chat Completions API, you indicate `https://<host>/v1/` - without `/chat/completions` as clients generally add it. | Yes |
    | **Protocol**  | The communication protocol supported by your agent. Use HTTP in general, or if your agent supports more specifically A2A, indicate that one | Yes |
    | **A2A agent card URL** | Path to the agent card JSON specification. If you don't specify it, the system uses the default `/.well-known/agent-card.json`. | No |
    | **OpenTelemetry Agent ID** | The Agent ID your agent uses to emit traces according to OpenTelemetry Generative AI semantic conventions. Traces indicate it in attribute `gen_ai.agents.id` for spans with operation name `create_agent`. If you don't specify this value, the system uses the **Agent name** value to find traces and logs that this new agent reports. | No |
    | **Admin portal URL** | The administration portal URL where you can perform further administration operations for this agent. Foundry can store this value for easy access convenience. Foundry doesn't have any access to perform operations directly to such management portal. | No |

1. Then, configure how you want the agent to show up in the Control Plane:

    | Property  | Description | Required |
    |-----------|-------------|----------|
    | **Project** | The project where you register the agent. Foundry uses the AI Gateway configured in the resource where the project lives to configure the inbound endpoint to the agent. You can only select projects with AI Gateway enabled in their resources. If you don't see any, [configure AI Gateway in your Foundry resource](../configuration/enable-ai-api-management-gateway-portal.md#create-an-ai-gateway). It's also advisable to configure Azure Application Insights in the selected project. Foundry uses the project's Azure Application Insights resource to sink traces and logs. | Yes |
    | **Agent name** | The name of the agent as you want it to appear in Foundry. The system might also use this name to find relevant traces and logs in Azure Application Insights if you don't specify a different value in the field **OpenTelemetry Agent ID**. | Yes |
    | **Description** | A clear description about this agent. | No |

1. Save the changes.

1. Foundry adds the new agent. Select the **Assets** tab in the left pane to check the list of agents.

1. To show only custom agents, use the **Source** filter and select **Custom**.

    :::image type="content" source="media/register-custom-agent/register-custom-agent-example.png" alt-text="Screenshot of a custom agent registered." lightbox="media/register-custom-agent/register-custom-agent-example.png":::

### Connect clients to the agent

When you register your agent in Foundry, you get a new URL for your clients to use. Foundry acts as a proxy for communications to your agent, so it can control access and monitor activity.

To distribute the new URL for your clients to call the agent:

1. Select the custom agent by using the radio selector.

1. On the details panel on the right, under **Agent URL**, select the copy option.

    :::image type="content" source="media/register-custom-agent/register-custom-agent-url.png" alt-text="Screenshot of how to copy the new URL of the agent after registration." lightbox="media/register-custom-agent/register-custom-agent-url.png":::

1. Use the new URL to call the agent instead of the original endpoint.

In this example, you deploy a LangGraph agent and clients use the LangGraph SDK to consume it. The client uses the **new agent URL** value. This code creates a thread, sends a message asking about the weather, and streams the response back.

```python
from langgraph_sdk import get_client

client = get_client(url="https://apim-my-foundry-resource.azure-api.net/my-custom-agent/") 

async def stream_run():
   thread = await client.threads.create()
   input_data = {"messages": [{"role": "human", "content": "What's the weather in LA?"}]}
   
   async for chunk in client.runs.stream(thread['thread_id'], assistant_id="your_assistant_id", input=input_data):
       print(chunk)
```

**Expected output**: The agent processes the message and streams back responses as chunks. Each chunk contains partial results from the agent's execution, which might include tool calls to the weather function and the final response about Los Angeles weather.


> [!NOTE]
> Foundry acts as a proxy for incoming requests for your agent. However, the original authorization and authentication schema in the original endpoint still applies. When you consume the new endpoint, **provide the same authentication mechanism as if you use the original endpoint.**


## Block and unblock the agent

For custom agents, Foundry doesn't have access to the underlying infrastructure where the agent runs, so start and stop operations aren't available. However, Foundry can block incoming requests to the agent, preventing clients from consuming it. This capability allows administrators to disable an agent if it misbehaves.

To block incoming requests to your agent:

1. Select **Operate** from the upper-right navigation.

1. Select **Assets** in the left pane.

1. Select the agent you want to block. The information panel appears.

1. Select **Update status** and then select **Block**.

    :::image type="content" source="media/register-custom-agent/register-custom-agent-block.png" alt-text="Screenshot of how to block incoming requests to the agent." lightbox="media/register-custom-agent/register-custom-agent-block.png":::

1. Confirm the operation.

After you block the agent, the **Status** of the agent in Foundry shows as **Blocked**. Agents in the **Blocked** state run in their associated infrastructure but can't take incoming requests. Foundry blocks any attempt to interface with the agent.

To unblock the agent:

1. Select **Update status** and then select **Unblock**.

1. Confirm the operation.

## Enable telemetry for your agent

Foundry uses the OpenTelemetry open standard to understand what agents are doing. If your project has Azure Application Insights configured, Foundry logs requests into Azure Application Insights by default. Foundry also uses this telemetry to compute:

* Runs
* Error rate
* Usage (if available)

To get the best level of fidelity, Foundry expects custom agents to comply with the [semantic conventions for Generative AI solution in the OpenTelemetry standard](https://opentelemetry.io/docs/specs/semconv/gen-ai/). 

### View runs and traces

You can view traces and logs sent to Foundry. To view them:

1. Select **Operate** from the upper-right navigation.

1. Select **Assets** in the left pane.

1. Select the agent.

1. The **Traces** sections appear.

1. You see one entry for each HTTP call made to the agent's endpoint.

1. To see the details, select an entry: 

    :::image type="content" source="media/register-custom-agent/custom-agent-trace.png" alt-text="Screenshot of a call to the agent's endpoint under the route 'runs/stream'." lightbox="media/register-custom-agent/custom-agent-trace.png":::

    > [!TIP]
    > In this example, you can see how clients use the new agent's endpoint to communicate with the agent. The example shows an agent served with the Agent Protocol from LangChain. Clients use the route `/runs/stream`.

1. In this example, the trace doesn't include any details besides the HTTP post. The agent's code doesn't include any further instrumentation. For more information about how to instrument your code and gain further details like tool calls, LLM calls, and more, see the next section.

### Instrument custom code agents

If you build your agent with custom code, instrument your solution to emit traces according to the OpenTelemetry standard and send them to Azure Application Insights. Instrumentation gives Foundry access to detailed information about what your agent is doing.

Send traces to the Azure Application Insights resource of your project by using its instrumentation key. To get the instrumentation key associated with your project, follow the instructions at [Enable tracing in your project](../../how-to/develop/trace-application.md#enable-tracing-in-your-project).

In this example, you configure an agent developed with LangGraph to emit traces in the OpenTelemetry standard. The tracer captures all agent operations, including tool calls and model interactions, and sends them to Azure Application Insights for monitoring. 

This code uses the [langchain-azure-ai](http://pypi.org/project/langchain-azure-ai) package. For guidance on instrumenting specific solutions with OpenTelemetry, depending on the programming language and framework used in your solution, see [Language APIs & SDKs](https://opentelemetry.io/docs/languages/).

```bash
pip install -U langchain-azure-ai[opentelemetry]
```

Then, instrument your agent:


```python
from langchain.agents import create_agent
from langchain_azure_ai.callbacks.tracers import AzureAIOpenTelemetryTracer

application_insights_connection_string = 'InstrumentationKey="12345678...'

tracer = AzureAIOpenTelemetryTracer(
    connection_string=application_insights_connection_string,
    enable_content_recording=True,
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-5.1",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
).with_config({ "callbacks": [tracer] })
```

**Expected output**: The agent runs normally while automatically emitting OpenTelemetry traces to Azure Application Insights. Traces include operation names, durations, model calls, tool invocations, and token usage. You can view these traces in the Foundry portal under the Traces section.


> [!TIP]
> You can pass the connection string to Azure Application Insights by using the environment variable `APPLICATIONINSIGHTS_CONNECTION_STRING`. 

### Instrumenting platform solutions

If your agent runs on a platform solution that supports OpenTelemetry but doesn't support Azure Application Insights, deploy an OpenTelemetry Collector and configure your software to send OTLP data to the Collector (standard OpenTelemetry configuration).

Configure the Collector with the Azure Monitor exporter to forward data to Application Insights by using your connection string. For details about how to implement, see [Configure Azure Monitor OpenTelemetry](/azure/azure-monitor/app/opentelemetry-configuration).

### Troubleshooting traces

If you don't see traces, check the following items:

> [!div class="checklist"]
> * The project where you register your agent has Azure Application Insights configured. If you configured Azure Application Insights **after** you registered the custom agent, you need to **unregister** the agent and register it again. Azure Application Insights configuration isn't automatically updated after registration if changed.
> * You configure the agent (running on its infrastructure) to send traces to Azure Application Insights and you're using **the same** Azure Application Insights resource as your project.
> * Instrumentation complies with OpenTelemetry semantic conventions for Generative AI.
> * Traces include spans with attributes `operation="create_agent"`, and `gen_ai.agents.id="<agent-id>"` or `gen_ai.agents.name="<agent-id>"`; where `"<agent-id>"` is the **OpenTelemetry Agent ID** you configure during registration.

## Related content

- [What is the Microsoft Foundry Control Plane?](overview.md)
- [Monitor agents across your fleet](monitoring-across-fleet.md)
- [Optimize cost and performance across your agent fleet](how-to-optimize-cost-performance.md)
