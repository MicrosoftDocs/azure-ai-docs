---
title: "Register and manage custom agents in Azure AI Foundry Control Hub"
description: "Learn how to register a custom agent in Azure AI Foundry Control Hub for management and observability."
author: santiagxf
ms.author: fasantia
ms.date: 10/30/2025
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
---

# Register and manage custom agents

Azure AI Foundry Control Hub can operate agents across multiple platforms, including custom agents running in compute services in Azure or even on a different cloud.

In this article, you learn how to register a custom agent in Azure AI Foundry Control Hub to gain management and observability capabilities on it.

## Prerequisites

Before getting started, make sure:

* An Azure AI Foundry resource and project.
* The Next
* Azure AI Foundry uses Azure API Management to register custom APIs as agents. [Configure AI Gateway in your Azure AI Foundry resource]().
* To use observability capabilities, [configure Azure Application Insights]() in your project. Review the section [Enable telemetry for your agent](#enable-telemetry-for-your-agent) for more details and requirements.

    > [!IMPORTANT]
    > Viewing statistics, runs, and traces for custom agents requires observability configured.

* An agent deploy and exposed through a reachable endpoint (either a public endpoint or reachable from the network where the Azure AI Foundry resource is deployed).

## Add a custom agent

You can register a custom agent in Azure AI Foundry Control Hub. The agent can be developed in the technology of your choice, both platform and infrastructure solutions. 

### Before you start

Verify that your agent meets the requirements for registration:

> [!div class="checklist"]
> * Your agent is exposed through an exclusive endpoint.
> * The agent is reachable from withing the network where the Azure AI Foundry resource is deployed.
> * The agent communicates using one of the supported protocols: either general HTTP, or specifically, A2A.
> Your agent emits telemetry using the OpenTelemetry semantic conventions for GenAI solutions (or either you don't need this capability).

### Register the agent

To register the agent, follow these steps:

1. Navigate to the [Azure AI Foundry portal](https://ai.azure.com).

1. On the top navigation bar, select **Operate**.

1. From the **Overview** page, select the option **Register agent**.

1. The registration wizard shows up. First, complete the details about the agent you want to register. The following properties describe the agent as it is running on its platform:

    | Property  | Description | Required |
    |-----------|-------------|----------|
    | **Agent URL** | It represents the endpoint (URL) where you agent is running and receives requests. In general, but depending on your protocol, you indicate the base URL that your clients use. For example, if your agent talks OpenAI Chat Completions API, you indicate `https://<host>/v1/` - without `/chat/completions` as it's generally added by your clients. | Yes |
    | **Protocol**  | The communication protocol supported by your agent. Use HTTP in general, or if your agent supports more specifically A2A, indicate that one | Yes |
    | **A2A agent card URL** | Path to the agent card JSON specification. If not indicated, the default `/.well-known/agent-card.json` is used. | No |
    | **OpenTelemetry Agent ID** | The Agent ID used to emit traces according to OpenTelemetry Generative AI semantic conventions. On generated traces, it's indicated in the attribute `gen_ai.agents.id` for spans with operation name `create_agent`. If not indicated, **Agent name** value is used to find traces and logs reported by this new agent. | No |
    | **Admin portal URL** | The administration portal URL where further administration operations can be performed for this agent. Azure AI Foundry can store this value so it's easily accesible from the portal. Azure AI Foundry won't have any access to perform operations directly to such management portal. | No |

1. Then, configure how you want the agent to show up in Azure AI Foundry Control Hub:

    | Property  | Description | Required |
    |-----------|-------------|----------|
    | **Project** | The project where the agent gets registered. Azure AI Foundry uses the AI Gateway configured in the resource where the project lives to configure the inbound endpoint to the agent. Only projects with AI Gateway enabled in their resourses are availabile for selection. It's also advisable to configure Azure Application Insights in the selected project. Azure AI Foundry uses the project's Azure Application Insights resource to sink traces and logs. | Yes |
    | **Agent name** | The name of the agent as you want it to show up in Azure AI Foundry. This name may also be used to find relevant traces and logs in Azure Application Insights if you have not indicated a different value in the field **OpenTelemetry Agent ID**. | Yes |
    | **Description** | A clear description about this agent. | No |

1. Once all the properties have been filled in, the field **new agent URL** displays the new URL that clients.

1. Save the changes.

1. The new agent is added to Azure AI Foundry. You can check the list of agents on the **Assets** tab at the left navigation.

### Use the agent

Once your agent is registed in Azure AI Foundry, a new URL is generated for your clients to use. Azure AI Foundry acts as a proxy for communications to your agent so it can control its access and monitor activity.

Use the new generated URL to distribute to your clients.

> [!NOTE]
> Azure AI Foundry acts as a proxy for incoming requests for your agent. However, the original authorization and authentication schema in the original endpoint still applies. When consuming the new endpoint, provide the same authentication mechanism as if you were using the original endpoint.

In this example, we have deployed a LangGraph agent and clients are using the LangGraph SDK to consume it. Notice how the URL used of the client is using the **new agent URL** value mentioned above.

```python
from langgraph_sdk import get_client

client = get_client(url="https://apim-my-foundry-resource.azure-api.net/my-cool-agent/") 

async def stream_run():
   thread = await client.threads.create()
   input_data = {"messages": [{"role": "human", "content": "What's the weather in LA?"}]}
   
   async for chunk in client.runs.stream(thread['thread_id'], assistant_id="your_assistant_id", input=input_data):
       print(chunk)
```

## Control the custom agent

Azure AI Foundry allows developers to monitor and control the agents across different platform. The actions available for each agent depend on the platform running the agent and in some cases the type of agent.

For custom agents, because Azure AI Foundry doesn't have access to the underlying infrastructure where the agent is running, start and stop operations are not available. However, Azure AI Foundry can block incoming requests to the agent preventing clients to consume it. Such capability allows administrators to disable an agent in case it's misbehaving.

To block incoming requests to your agent:

1. Navigate to the [Azure AI Foundry portal](https://ai.azure.com).

1. On the top navigation bar, select **Operate**.

1. On the left navigation, select **Assets**.

1. Select the agent you want to block. The information panel shows up on the right.

1. Select **Update status** and then select **Block**.

1. Confirm the operation.

Once the agent is block, the **Status** of the agent in Azure AI Foundry shows as **Blocked**. Agents in the **Blocked** state are running in their associated infrastructure but they can't take incoming requests. Azure AI Foundry blocks any attempt to interface with the agent.

To unblock the agent:

1. Select **Update status** and then select **Unblock**.

1. Confirm the operation.

## Enable telemetry for your agent

Azure AI Foundry uses OpenTelemetry open standard to understand what agents are doing. In particular, to get the best level of fidelity, Azure AI Foundry expects custom agents to comply with the [semantic conventions for Generative AI solution in the OpenTelemetry standard](https://opentelemetry.io/docs/specs/semconv/gen-ai/). 

Traces should be sent to the Azure Applications Insights resource of your project using its instrumentation key. You can get the instrumentation key associated with your project following the instructions at [Enable tracing in your project](../../how-to/develop/trace-application.md#enable-tracing-in-your-project).

### Instrumenting custom code agents

If your agent is built using custom code you control, you need to instrument your solution to emit traces and logging information according to the OpenTelemetry standard and sink them to Azure Applications Insights.

> [!TIP]
> Learn how to instrument specific solutions with OpenTelemetry depending on the programming language and the framework used in your solution at [Language APIs & SDKs](https://opentelemetry.io/docs/languages/).

In this tutorial, we demostrate how you can configure an agent developed with LangGraph to emit traces in OpenTelemetry standard for LangGraph:

```python
from langchain.agents import create_agent
from langchain_azure_ai.callbacks.tracers import AzureAIOpenTelemetryTracer

application_insights_connection_string = 'InstrumentationKey="12345678...'

azure_tracer = AzureAIOpenTelemetryTracer(
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
).with_config({ "tracer": azure_tracer })
```

### Instumenting platform solutions

If your agent runs on a platform solution that supports OpenTelemetry, but it doesn't support Azure Applications Insights, you need to deploy an OpenTelemetry Collector and configure your software to send OTLP data to the Collector (standard OpenTelemetry configuration).

Configure the Collector with the Azure Monitor exporter to forward data to Application Insights using your connection string. For details about how to implement, see [Configure Azure Monitor OpenTelemetry](/azure/azure-monitor/app/opentelemetry-configuration.md).

## View runs and traces

You can view traces and logs sent to Azure AI Foundry. To view them:

1. Navigate to the [Azure AI Foundry portal](https://ai.azure.com).

1. On the top navigation bar, select **Operate**.

1. On the left navigation, select **Assets**.

1. Select the agent and select **Monitor in build**.

1. Monitoring sections shows up.

1. In the top navigation, select the option **Traces**.

1. Your traces show in the portal.


### Troubleshooting

If you don't see traces, check the following:

> [!div class="checklist"]
> * The project where your agent was registered has Azure Application Insights configured.
> * The agent (running on its infrastructure) is configured to send traces to Azure Application Insights.
> * Instrumentation complies with OpenTelemetry semantic conventions for Generative AI.
> * Traces include spans with attributes `operation="create_agent"`, and `gen_ai.agents.id="<agent-id>"` or `gen_ai.agents.name="<agent-id>"`; where `"<agent-id>"` is the **OpenTelemetry Agent ID** configured during registration.
