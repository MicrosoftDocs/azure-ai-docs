---
title: "Register and manage custom agents in Microsoft Foundry Control Plane"
description: "Learn how to register a custom agent in Microsoft Foundry Control Plane for management and observability."
author: santiagxf
ms.author: scottpolly
ms.reviewer: fasantia
ms.date: 11/18/2025
ms.manager: mcleans
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Register and manage custom agents

The Microsoft Foundry Control Plane provides centralized management and observability for agents running across different platforms and infrastructures. You can register custom agents—whether they run in Azure compute services or other cloud environments—to gain visibility into their operations and control their behavior.

This article shows you how to register a custom agent in the Foundry Control Plane. You learn how to configure your agent for registration, set up telemetry collection, and use the Control Plane's management capabilities.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

Before getting started, make sure you have:

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]
- Foundry uses Azure API Management to register custom APIs as agents. [Configure AI Gateway in your Foundry resource](../configuration/enable-ai-api-management-gateway-portal.md#create-an-ai-gateway).
- To use observability capabilities, configure Azure Application Insights in your project. Review the section [Enable telemetry for your agent](#enable-telemetry-for-your-agent) for more details and requirements.

    > [!IMPORTANT]
    > Viewing statistics, runs, and traces for custom agents requires observability to be configured.

- An agent that you deploy and expose through a reachable endpoint (either a public endpoint or an endpoint reachable from the network where you deploy the Foundry resource).

[!INCLUDE [capability-new-portal](../includes/capability-new-portal.md)]

## Add a custom agent

You can register a custom agent in the Foundry Control Plane. You can develop the agent in the technology of your choice, both platform and infrastructure solutions. 

### Before you start

Verify that your agent meets the requirements for registration:

> [!div class="checklist"]
> * Your agent exposes an exclusive endpoint.
> * The network where you deploy the Foundry resource can reach the agent.
> * The agent communicates by using one of the supported protocols: either general HTTP or specifically A2A.
> * Your agent emits telemetry by using the OpenTelemetry semantic conventions for GenAI solutions (or you don't need this capability).

### Register the agent

To register the agent, follow these steps:

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]

1. Select **Operate** from the upper-right navigation.

1. Select the **Overview** pane.

1. Select **Register agent**.

    :::image type="content" source="../media/register-custom-agent/register-custom-agent.png" alt-text="Screenshot of the Register agent button in the Foundry portal Overview pane." lightbox="../media/register-custom-agent/register-custom-agent.png":::

1. The registration wizard appears. First, complete the details about the agent you want to register. The following properties describe the agent as it runs on its platform

    | Property  | Description | Required |
    |-----------|-------------|----------|
    | **Agent URL** | It represents the endpoint (URL) where your agent runs and receives requests. In general, but depending on your protocol, you indicate the base URL that your clients use. For example, if your agent talks OpenAI Chat Completions API, you indicate `https://<host>/v1/` - without `/chat/completions` as clients generally add it. | Yes |
    | **Protocol**  | The communication protocol supported by your agent. Use HTTP in general, or if your agent supports more specifically A2A, indicate that one | Yes |
    | **A2A agent card URL** | Path to the agent card JSON specification. If you don't specify this, the system uses the default `/.well-known/agent-card.json`. | No |
    | **OpenTelemetry Agent ID** | The Agent ID your agent uses to emit traces according to OpenTelemetry Generative AI semantic conventions. Traces indicate it in attribute `gen_ai.agents.id` for spans with operation name `create_agent`. If you don't specify this, the system uses the **Agent name** value to find traces and logs that this new agent reports. | No |
    | **Admin portal URL** | The administration portal URL where you can perform further administration operations for this agent. Foundry can store this value for easy access convenience. Foundry doesn't have any access to perform operations directly to such management portal. | No |

1. Then, configure how you want the agent to show up in the Foundry Control Plane:

    | Property  | Description | Required |
    |-----------|-------------|----------|
    | **Project** | The project where you register the agent. Foundry uses the AI Gateway configured in the resource where the project lives to configure the inbound endpoint to the agent. You can only select projects with AI Gateway enabled in their resources. It's also advisable to configure Azure Application Insights in the selected project. Foundry uses the project's Azure Application Insights resource to sink traces and logs. | Yes |
    | **Agent name** | The name of the agent as you want it to appear in Foundry. The system might also use this name to find relevant traces and logs in Azure Application Insights if you don't specify a different value in the field **OpenTelemetry Agent ID**. | Yes |
    | **Description** | A clear description about this agent. | No |

1. Once you fill in all the properties, the field **new agent URL** displays the new URL for clients.

1. Save the changes.

1. Foundry adds the new agent. Select the **Assets** tab in the left pane to check the list of agents.

### Use the agent

When you register your agent in Foundry, you get a new URL for your clients to use. Foundry acts as a proxy for communications to your agent, so it can control access and monitor activity.

Distribute the new URL to your clients.

> [!NOTE]
> Foundry acts as a proxy for incoming requests for your agent. However, the original authorization and authentication schema in the original endpoint still applies. When you consume the new endpoint, **provide the same authentication mechanism as if you use the original endpoint.**

In this example, you deploy a LangGraph agent and clients use the LangGraph SDK to consume it. The client uses the **new agent URL** value from the registration process. This code creates a thread, sends a message asking about the weather, and streams the response back.

```python
from langgraph_sdk import get_client

client = get_client(url="https://apim-my-foundry-resource.azure-api.net/my-cool-agent/") 

async def stream_run():
   thread = await client.threads.create()
   input_data = {"messages": [{"role": "human", "content": "What's the weather in LA?"}]}
   
   async for chunk in client.runs.stream(thread['thread_id'], assistant_id="your_assistant_id", input=input_data):
       print(chunk)
```

**Expected output**: The agent processes the message and streams back responses as chunks. Each chunk contains partial results from the agent's execution, which might include tool calls to the weather function and the final response about Los Angeles weather.


## Control the agent

Foundry enables developers to monitor and control agents across different platforms. The available actions for each agent depend on the platform running the agent and, in some cases, the type of agent.

For custom agents, Foundry doesn't have access to the underlying infrastructure where the agent runs, so start and stop operations aren't available. However, Foundry can block incoming requests to the agent, preventing clients from consuming it. This capability allows administrators to disable an agent if it misbehaves.

To block incoming requests to your agent:

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]

1. Select **Operate** from the upper-right navigation.

1. Select **Assets** in the left pane.

1. Select the agent you want to block. The information panel appears.

1. Select **Update status** and then select **Block**.

1. Confirm the operation.

After you block the agent, the **Status** of the agent in Foundry shows as **Blocked**. Agents in the **Blocked** state run in their associated infrastructure but can't take incoming requests. Foundry blocks any attempt to interface with the agent.

To unblock the agent:

1. Select **Update status** and then select **Unblock**.

1. Confirm the operation.

## Enable telemetry for your agent

Foundry uses the OpenTelemetry open standard to understand what agents are doing. To get the best level of fidelity, Foundry expects custom agents to comply with the [semantic conventions for Generative AI solution in the OpenTelemetry standard](https://opentelemetry.io/docs/specs/semconv/gen-ai/). 

Send traces to the Azure Application Insights resource of your project by using its instrumentation key. To get the instrumentation key associated with your project, follow the instructions at [Enable tracing in your project](../../how-to/develop/trace-application.md#enable-tracing-in-your-project).

### Instrumenting custom code agents

If you build your agent with custom code, you need to instrument your solution to emit traces according to the OpenTelemetry standard and sink them to Azure Application Insights.

> [!TIP]
> Learn how to instrument specific solutions with OpenTelemetry depending on the programming language and the framework used in your solution at [Language APIs & SDKs.](https://opentelemetry.io/docs/languages/)

In this example, you configure an agent developed with LangGraph to emit traces in the OpenTelemetry standard. The tracer captures all agent operations, including tool calls and model interactions, and sends them to Azure Application Insights for monitoring.

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

If your agent runs on a platform solution that supports OpenTelemetry but doesn't support Azure Application Insights, you need to deploy an OpenTelemetry Collector and configure your software to send OTLP data to the Collector (standard OpenTelemetry configuration).

Configure the Collector with the Azure Monitor exporter to forward data to Application Insights by using your connection string. For details about how to implement, see [Configure Azure Monitor OpenTelemetry](/azure/azure-monitor/app/opentelemetry-configuration).

## View runs and traces

You can view traces and logs sent to Foundry. To view them:

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]

1. Select **Operate** from the upper-right navigation.

1. Select **Assets** in the left pane.

1. Select the agent and select **Monitor in build**.

1. The monitoring sections show up.

1. Select **Traces** in the top navigation.

1. Your traces show in the portal.


### Troubleshooting

If you don't see traces, check the following checklist:

> [!div class="checklist"]
> * The project where you register your agent has Azure Application Insights configured.
> * You configure the agent (running on its infrastructure) to send traces to Azure Application Insights.
> * Instrumentation complies with OpenTelemetry semantic conventions for Generative AI.
> * Traces include spans with attributes `operation="create_agent"`, and `gen_ai.agents.id="<agent-id>"` or `gen_ai.agents.name="<agent-id>"`; where `"<agent-id>"` is the **OpenTelemetry Agent ID** you configure during registration.

## Related content

- [What is the Microsoft Foundry Control Plane?](overview.md)
- [Monitor agents across your fleet](monitoring-across-fleet.md)
- [Optimize cost and performance across your agent fleet](how-to-optimize-cost-performance.md)
