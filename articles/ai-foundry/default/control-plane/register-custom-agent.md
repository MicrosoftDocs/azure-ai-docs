---
title: Register and Manage Custom Agents in Microsoft Foundry Control Plane
description: Learn how to register a custom agent in Microsoft Foundry Control Plane for management and observability.
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

Microsoft Foundry Control Plane provides centralized management and observability for agents running across different platforms and infrastructures. You can register custom agents that run in Azure compute services or other cloud environments to gain visibility into their operations and control their behavior.

This article shows you how to register a custom agent in Foundry Control Plane. You learn how to configure your agent for registration, set up data collection, and use the management capabilities of Foundry Control Plane.

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]

- An [AI gateway configured in your Foundry resource](../configuration/enable-ai-api-management-gateway-portal.md#create-an-ai-gateway). Foundry uses Azure API Management to register agents as APIs.

- An agent that you deploy and expose through a reachable endpoint. The endpoint can be either a public endpoint or an endpoint that's reachable from the network where you deploy the Foundry resource.

[!INCLUDE [capability-new-portal](../includes/capability-new-portal.md)]

## Add a custom agent

You can register a custom agent in Foundry Control Plane. Develop the agent in the technology of your choice, for both platform and infrastructure solutions.

When you register a custom agent, Foundry uses API Management to act as a proxy for communications to your agent, so it can control access and monitor activity.

The following diagram shows the resulting architecture when you register a custom agent.

:::image type="content" source="media/register-custom-agent/custom-agent-architecture.png" alt-text="Diagram that shows the resulting architecture after a custom agent is registered and configured." lightbox="media/register-custom-agent/custom-agent-architecture.png":::

### Verify your agent

Verify that your agent meets the requirements for registration:

> [!div class="checklist"]
>
> - Your agent exposes an exclusive endpoint.
> - The network where you deploy the Foundry resource can reach the agent's endpoint.
> - The agent communicates by using one of the supported protocols: HTTP (general) or A2A (more specific).
> - Your agent emits data by using the OpenTelemetry semantic conventions for generative AI solutions (or you don't need this capability).
> - You can configure the endpoint that users use to communicate with the agent. After you register an agent, Foundry Control Plane generates a new URL. *Clients and users must use this URL to communicate with the agent*.

### Prepare your Foundry project

Before you register the custom agent that you added to a Foundry project, make sure that you configured the project correctly:

1. [!INCLUDE [foundry-sign-in](../../default/includes/foundry-sign-in.md)]

1. Ensure that an AI gateway is configured in your project:

    1. On the toolbar, select **Operate**.

    1. On the left pane, select **Admin**.

    1. Open the **AI Gateway** tab.

    1. The pane lists all the AI gateways configured and mapped to a Foundry resource. Check if the Foundry resource that you want to use has an associated AI gateway.

        :::image type="content" source="media/register-custom-agent/verify-ai-gateway.png" alt-text="Screenshot of the Foundry administration portal that shows steps for verifying if a project has an AI gateway configured." lightbox="media/register-custom-agent/verify-ai-gateway.png":::

    1. If the Foundry resource that you want to use doesn't have an AI gateway configured (it isn't listed), add one by using the **Add AI Gateway** option.

       An AI gateway is free to set up and unlocks powerful governance features like security, diagnostic data, and rate limits for your agents, tools, and models. For more information, see [Create an AI gateway](../configuration/enable-ai-api-management-gateway-portal.md#create-an-ai-gateway).

1. Ensure that you have observability configured in the project. Foundry Control Plane uses the Application Insights resource associated with your selected project for emitting data to help you diagnose your agent.

    1. On the toolbar, select **Operate**.

    1. On the left pane, select **Admin**.

    1. Under **All projects**, use the search box to look for your project.

    1. Select the project.

    1. Select the **Connected resources** tab.

    1. Ensure that there's an associated resource in the **AppInsights** category.

        :::image type="content" source="media/register-custom-agent/verify-app-insights.png" alt-text="Screenshot of the administration portal that shows steps to verify if a project has an associated Application Insights resource." lightbox="media/register-custom-agent/verify-app-insights.png":::

    1. If there's no associated resource, add one by selecting **Add connection** > **Application Insights**.

Your project is configured for observability and tracing.

### Register the agent

1. On the toolbar, select **Operate**.

1. On the **Overview** pane, select **Register agent**.

    :::image type="content" source="media/register-custom-agent/register-custom-agent.png" alt-text="Screenshot of the button for registering an agent on the Overview pane of the Foundry portal." lightbox="media/register-custom-agent/register-custom-agent.png":::

1. The registration wizard appears. First, complete the details about the agent that you want to register. The following properties describe the agent as it runs on its platform:

    | Property | Description | Required |
    | -------- | ----------- | -------- |
    | **Agent URL** | The endpoint (URL) where your agent runs and receives requests. In general, but depending on your protocol, you indicate the base URL that your clients use. For example, if your agent uses the OpenAI Chat Completions API, you indicate `https://<host>/v1/` without `/chat/completions` because clients generally add it. | Yes |
    | **Protocol** | The communication protocol that your agent supports. Use HTTP in general. Or if your agent supports A2A more specifically, indicate that one. | Yes |
    | **A2A agent card URL** | The path to the agent card's JSON specification. If you don't specify it, the system uses the default `/.well-known/agent-card.json`. | No |
    | **OpenTelemetry Agent ID** | The agent ID that your agent uses to emit traces according to OpenTelemetry semantic conventions for generative AI. Traces indicate it in the `gen_ai.agents.id` attribute for spans with the operation name `create_agent`. If you don't specify this value, the system uses the **Agent name** value to find traces and logs that this new agent reports. | No |
    | **Admin portal URL** | The administration portal URL where you can perform further administration operations for this agent. Foundry can store this value for convenience. Foundry doesn't have any access to perform operations directly to this portal. | No |

1. Configure how you want the agent to appear in Foundry Control Plane:

    | Property | Description | Required |
    | -------- | ----------- | -------- |
    | **Project** | The project where you register the agent. Foundry uses the AI gateway configured in the resource that contains the project to configure the inbound endpoint to the agent. You can select only projects that have an AI gateway enabled in their resources. If you don't see any AI gateways, [configure an AI gateway in your Foundry resource](../configuration/enable-ai-api-management-gateway-portal.md#create-an-ai-gateway). We also recommend that you configure Application Insights in the selected project. Foundry uses the project's Application Insights resource to sink traces and logs. | Yes |
    | **Agent name** | The name of the agent as you want it to appear in Foundry. The system might also use this name to find relevant traces and logs in Application Insights if you don't specify a different value for **OpenTelemetry Agent ID**. | Yes |
    | **Description** | A clear description about this agent. | No |

1. Save the changes.

1. Foundry adds the new agent. To check the list of agents, select **Assets** on the left pane.

1. To show only custom agents, use the **Source** filter and select **Custom**.

    :::image type="content" source="media/register-custom-agent/register-custom-agent-example.png" alt-text="Screenshot of a registered custom agent." lightbox="media/register-custom-agent/register-custom-agent-example.png":::

### Connect clients to the agent

When you register your agent in Foundry, you get a new URL for your clients to use. Because Foundry acts as a proxy for communications to your agent, it can control access and monitor activity.

To distribute the new URL so that your clients can call the agent:

1. Select the custom agent.

1. On the details pane, under **Agent URL**, select the **Copy** option.

    :::image type="content" source="media/register-custom-agent/register-custom-agent-url.png" alt-text="Screenshot of steps to copy the new URL of the agent after registration." lightbox="media/register-custom-agent/register-custom-agent-url.png":::

1. Use the new URL to call the agent instead of the original endpoint.

In this example, you deploy a LangGraph agent. Clients use the LangGraph SDK to consume it. The client uses the *new agent URL* value. This code creates a thread, sends a message asking about the weather, and streams the response back.

```python
from langgraph_sdk import get_client

client = get_client(url="https://apim-my-foundry-resource.azure-api.net/my-custom-agent/") 

async def stream_run():
   thread = await client.threads.create()
   input_data = {"messages": [{"role": "human", "content": "What's the weather in LA?"}]}
   
   async for chunk in client.runs.stream(thread['thread_id'], assistant_id="your_assistant_id", input=input_data):
       print(chunk)
```

**Expected output**: The agent processes the message and streams back responses as chunks. Each chunk contains partial results from the agent's execution. These results might include tool calls to the weather function and the final response about Los Angeles weather.

> [!NOTE]
> Although Foundry acts as a proxy for incoming requests for your agent, the original authorization and authentication schema in the original endpoint still applies. When you consume the new endpoint, *provide the same authentication mechanism as if you're using the original endpoint.*

## Block and unblock the agent

For custom agents, Foundry doesn't have access to the underlying infrastructure where the agent runs, so start and stop operations aren't available. However, Foundry can block incoming requests to the agent so that clients can't consume it. This capability allows administrators to disable an agent if it misbehaves.

To block incoming requests to your agent:

1. On the toolbar, select **Operate**.

1. On the left pane, select **Assets**.

1. Select the agent that you want to block. The information pane appears.

1. Select **Update status**, and then select **Block**.

    :::image type="content" source="media/register-custom-agent/register-custom-agent-block.png" alt-text="Screenshot of steps to block incoming requests to an agent." lightbox="media/register-custom-agent/register-custom-agent-block.png":::

1. Confirm the operation.

After you block the agent, the **Status** value of the agent in Foundry is **Blocked**. Agents in the **Blocked** state run in their associated infrastructure but can't take incoming requests. Foundry blocks any attempt to interface with the agent.

To unblock the agent:

1. Select **Update status**, and then select **Unblock**.

1. Confirm the operation.

## Enable diagnostic data for the agent

Foundry uses the OpenTelemetry open standard to understand what agents are doing. If your project has Application Insights configured, Foundry logs requests into Application Insights by default. Foundry also uses this data to compute:

- Runs
- Error rate
- Usage (if available)

To get the best level of fidelity, Foundry expects custom agents to comply with the [semantic conventions for generative AI solutions in the OpenTelemetry standard](https://opentelemetry.io/docs/specs/semconv/gen-ai/).

### View traces and logs sent to Foundry

1. On the toolbar, select **Operate**.

1. On the left pane, select **Assets**.

1. Select the agent.

1. The **Traces** section shows one entry for each HTTP call made to the agent's endpoint.

   To see the details, select an entry.

    :::image type="content" source="media/register-custom-agent/custom-agent-trace.png" alt-text="Screenshot of a call to the agent's endpoint under the route for runs and streams." lightbox="media/register-custom-agent/custom-agent-trace.png":::

    > [!TIP]
    > In this example, you can see how clients use the new agent's endpoint to communicate with the agent. The example shows an agent served with the Agent Protocol from LangChain. Clients use the route `/runs/stream`.

In this example, the trace doesn't include any details beyond the HTTP post. The agent's code doesn't include any further instrumentation. In the next section, you learn how to instrument your code and get details like tool calls and large language model (LLM) calls.

### Instrument custom code agents

If you build your agent by using custom code, instrument your solution to emit traces according to the OpenTelemetry standard and send them to Application Insights. Instrumentation gives Foundry access to detailed information about what your agent is doing.

Send traces to the Application Insights resource of your project by using its instrumentation key. To get the instrumentation key associated with your project, follow the instructions at [Enable tracing in your project](../../how-to/develop/trace-application.md#enable-tracing-in-your-project).

In this example, you configure an agent developed with LangGraph to emit traces in the OpenTelemetry standard. The tracer captures all agent operations, including tool calls and model interactions. The tracer then sends the operations to Application Insights for monitoring.

This code uses the [langchain-azure-ai](http://pypi.org/project/langchain-azure-ai) package. For guidance on instrumenting specific solutions with OpenTelemetry, depending on the programming language and framework that your solution uses, see [Language APIs & SDKs](https://opentelemetry.io/docs/languages/).

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

**Expected output**: The agent runs normally while automatically emitting OpenTelemetry traces to Application Insights. Traces include operation names, durations, model calls, tool invocations, and token usage. You can view these traces in the Foundry portal, in the **Traces** section.

> [!TIP]
> You can pass the connection string to Application Insights by using the environment variable `APPLICATIONINSIGHTS_CONNECTION_STRING`.

### Instrument platform solutions

If your agent runs on a platform solution that supports OpenTelemetry but doesn't support Application Insights, deploy an OpenTelemetry collector and configure your software to send OTLP data to the collector (standard OpenTelemetry configuration).

Configure the collector with the Azure Monitor exporter to forward data to Application Insights by using your connection string. For details about how to implement it, see [Configure Azure Monitor OpenTelemetry](/azure/azure-monitor/app/opentelemetry-configuration).

### Troubleshoot traces

If you don't see traces, check the following items:

> [!div class="checklist"]
>
> - The project where you register your agent has Application Insights configured. If you configured Application Insights after you registered the custom agent, you need to unregister the agent and register it again. Application Insights configuration isn't automatically updated after registration if you changed it.
> - You configured the agent (running on its infrastructure) to send traces to Application Insights, and you're using the same Application Insights resource that your project uses.
> - Instrumentation complies with OpenTelemetry semantic conventions for generative AI.
> - Traces include spans with attributes `operation="create_agent"` and `gen_ai.agents.id="<agent-id>"` (or `gen_ai.agents.name="<agent-id>"`). In the latter attribute, `"<agent-id>"` is the **OpenTelemetry Agent ID** value that you configured during registration.

## Related content

- [What is Microsoft Foundry Control Plane?](overview.md)
- [Monitor agent health and performance across your fleet](monitoring-across-fleet.md)
- [Optimize model cost and performance](how-to-optimize-cost-performance.md)
