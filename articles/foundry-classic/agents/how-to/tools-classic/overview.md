---
title: 'What are tools in Foundry Agent Service'
titleSuffix: Microsoft Foundry
description: Learn how to use the various tools available in the Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/16/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
---

# What are tools in Foundry Agent Service?

> [!NOTE]
> This document refers to the classic version of the agents API. 
>
> 🔍 [View the new tool catalog documentation](../../../default/agents/concepts/tool-catalog.md?view=foundry&preserve-view=true).

To empower your AI agent with grounded data or the capability to take actions and automating workflows, the Foundry Agent Service provides a wide range of built-in tools, such as Grounding with Bing Search, Azure AI Search, Azure Logic Apps, as well as third-party partner tools, such as Tripadvisor. This page is designed to provide an overview of tools provided in the Foundry Agent Service. 

> [!NOTE]
> The new Microsoft Foundry portal and agents API provide additional tools. See the [tool catalog article](../../../default/agents/concepts/tool-catalog.md) for more information.  


## Knowledge tools

To keep your AI agent informed with richer context from various data sources. The Foundry Agent Service has covered a wide range of data types:

- **private data**: Azure AI Search, File Search, Microsoft Fabric, and more
- **public web data**: Grounding with Bing Search
- **licensed data**: Tripadvisor, Morningstar
- **unstructured data**: Azure AI Search, File Search
- **structured data**: Microsoft Fabric and more

## Action tools

To streamline workflows with your AI agent with capabilities to take actions, the Foundry Agent Service provides different action tools for you with different level of flexibility, control, and ease of integration:

- **Deep Research tool**: Web-based integrated deep research pipeline with the `o3-deep-research` model and Grounding with Bing Search.
- **Azure Logic Apps**: Low-code / no-code solution to add a workflow to your AI Agent
- **OpenAPI Spec tool**: Bring an existing OpenAPI specification of a service API you want to add to your AI agent, with no or minor changes.
- **MCP tool**: Bring an existing Model Context Protocol (MCP) endpoint that you want to add to your AI agent.
- **Function calling**: Write your own custom, stateless functions to define the expected behaviors.
- **Azure Functions**: Write and manage your own custom, stateful functions. 
- **Browser Automation**: Perform real-world browser tasks through natural language prompts.

## How does a tool work in the Foundry Agent Service?

Tools are optional capabilities you can add to your AI agent for AI models to decide and pick based on the user query and context. When a user sends a query, the AI model identifies the intent with the context and potentially rewrites the user query. Then the AI model decides which tools to be called for each run. For example, if you add both the Grounding with Bing Search tool and the Azure AI Search tool to your agent and ask "*what is the weather in Seattle today?*", the model will identify your intent to ask about real-time information and more likely to invoke the Grounding with Bing Search tool.

You can add tools at the agent, thread, or run level. By providing tools at a narrower level, the tool resources will **override** tool resources at a broader level. For example, tool resources at the run level override tool resources at thread level.

> [!IMPORTANT]
> **Tool instance limitation**: You can add multiple tools, but only **one instance of each** knowledge tool type: File Search, Azure AI Search, Grounding with Bing Search, Grounding with Bing Custom Search, Microsoft Fabric, and other tools under the `knowledge` section. To use multiple indexes with Azure AI Search, consider using [connected agents](../connected-agents.md).

When a user sends a query to the agent, it will create a [thread, run, and message](../../concepts/threads-runs-messages.md). For each run, the AI model decides what tools to invoke based on the user intent and available tool resources. Based on the tool outputs, the AI model might decide to invoke another tool or call the same tool again to get more context. For example, when you use Grounding with Bing Search tool, you might see multiple Bing Search queries when [tracing a thread](../../../how-to/develop/trace-agents-sdk.md). This means the AI model actually calls the Grounding with Bing Search tool multiple times with different queries to get more information. If you want to learn more about what tools are called and how the AI model invokes them, check the run step details.

### Controlling tool invocation

There are two main ways to influence how your AI agent invokes tools:

| Method | Behavior | Use when |
|--------|----------|----------|
| `tool_choice` parameter | Deterministic - forces or prevents specific tool use | You need guaranteed tool invocation or want to disable tools |
| `instructions` parameter | Non-deterministic - guides the model's decision | You want the model to intelligently choose based on context |

#### Using `tool_choice`

The `tool_choice` parameter is the most deterministic way of controlling which (if any) tool is called by the model. By default, it is set to `auto`, which means the AI model will decide. If you want to **force** the model to call a specific tool, you can provide the specification of this tool, for example

  ```python
  run = project_client.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
        tool_choice={"type": "bing_grounding"}  # specify the tool to use
        )
  ```

#### Using `instructions`

The `instructions` parameter is non-deterministic but provides flexible guidance. Use instructions to help the AI model understand your use case and the purposes of each tool. Tell the model what information or actions each tool can provide:

- **Route to specific tools**: "*Use the AI Search tool `<tool_name>` for product-related information, use the Fabric tool `<tool_name>` for sales-related information.*"
- **Prefer tools over base knowledge**: "*Use the tool outputs to generate a response, don't use your own knowledge.*"
- **Describe tool capabilities**: "*The Bing Search tool has access to real-time information including current weather, news, and stock prices.*"

## Prerequisites 

* [A created agent](../../quickstart.md)
* Make sure your AI model has enough Tokens-Per-Minute (TPM) allocated. We recommend having a minimum of 30k TPM. You can change the TPM allocation by going to **models + endpoints** in the [Foundry portal](https://ai.azure.com/?cid=learnDocs) and edit your model.

## Built-in tools 

The Foundry Agent Service provides the following built-in tools. You can use them with the REST API, SDK, and Microsoft Foundry portal.  

|Tool  |Description  |
|---------|---------|
|[Azure AI Search](azure-ai-search.md)     | Use an existing Azure AI Search index to ground agents with data in the index, and chat with your data.        |
|[Azure Functions](azure-functions.md)     | Leverage your Azure Functions to create intelligent, event-driven applications.        |
|[Browser Automation](browser-automation.md)     | Perform real-world browser tasks through natural language prompts.         |
|[Code Interpreter](code-interpreter.md)     | Enable agents to write and run Python code in a sandboxed execution environment.         |
|[Deep Research (preview)](./deep-research.md) | Use OpenAI's advanced agentic research capability for analysis and reasoning. | 
|[File Search](file-search.md)     | Augment agents with knowledge from outside its model, such as proprietary product information or documents provided by your users.          |
|[Function calling](function-calling.md)     |Describe the structure of functions you create to an agent and have them be called when appropriate during the agent's interactions with users.         |
|[Grounding with Bing Search](bing-grounding.md)     | Enable your agent to use Grounding with Bing Search to access and return information from the internet.         |
| [Grounding with Bing Custom Search (preview)](bing-custom-search.md) | Enhance your Agent response with selected web domains |
| [Model Context Protocol (preview)](./model-context-protocol.md) | Give the agent access to tools hosted on an existing MCP endpoint |
| [Microsoft Fabric (preview)](fabric.md) | Integrate your agent with the [Microsoft Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312815) to unlock powerful data analysis capabilities. |
| [OpenAPI 3.0 Specified tool ](openapi-spec.md) | Connect your Azure AI Agent to external APIs using functions with an OpenAPI 3.0 specification. |

## Non-Microsoft tools

The following tools are authored by third-party partners. Use the links below to view the documentation and code samples. 

> [!IMPORTANT]
> * Your use of connected non-Microsoft services is subject to the terms between you and the service provider. By connecting to a non-Microsoft service, you acknowledge that some of your data, such as prompt content, is passed to the non-Microsoft service, and/or your application might receive data from the non-Microsoft service. You are responsible for your use (and any charges associated with your use) of non-Microsoft services and data. 
> * The code in these non-Microsoft files were created by third parties, not Microsoft, and have not been tested or verified by Microsoft. Your use of the code samples is subject to the terms provided by the relevant third party. By using any third-party sample in this file, you are acknowledging that Microsoft has no responsibility to you or others with respect to these samples.

|Tool  |Description  |
|---------|---------|
| [Auquan](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/python/getting-started-agents/3p-tools/auquan) | AI-powered workflow automation for institutional finance |
| [Celonis](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/python/getting-started-agents/3p-tools/Celonis) | Celonis delivers Process Intelligence to accelerate enterprise AI at scale |
| [InsureMO Insurance Quotation](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/python/getting-started-agents/3p-tools/InsureMO) | Action APIs for insurance quotations for Car, Home, and Travel |
| [LEGALFLY](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/python/getting-started-agents/3p-tools/legalfly) | Legal insights grounded in trusted sources from your jurisdiction. |
| [LexisNexis](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/python/getting-started-agents/3p-tools/LexisNexis) | Seamless access to LexisNexis content. |
| [MiHCM](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/python/getting-started-agents/3p-tools/MiHCM) | seamless integration with MiHCM's HR functionalities |
| [Morningstar](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/python/getting-started-agents/3p-tools/Morningstar) | Access up-to-date investment research and data such as analyst research, expert commentary, and essential Morningstar data. |
| [Trademo](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/python/getting-started-agents/3p-tools/Trademo_Global_trade) | Provide latest duties and past shipment data for trade between multiple countries/regions |
| [Tripadvisor](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/python/getting-started-agents/3p-tools/Tripadvisor) | Get travel data, guidance and reviews |

## Best Practices

### Use system instruction to help model invoke the right tool

In order for the model to understand which tools to use, you want to provide detailed instruction for the model to describe when and how to use the tool. You might want to consider providing the following information:
- Primary Objective: what is the objective of this agent? what is the goal of related tasks? what are the expected outcomes?
- Your responsibilities: what tasks you expect the agent to perform. For example, calling Grounding with Bing Search tool to get the latest information about local events.
- Inputs you may receive: what inputs do you expect the agent to receive?
- For each tool:
   - The tool name
   - A description of the tool
   - Triggers: when do you expect this tool to be called? What type of information will be searched? What will queries contain?
   - An example of a query

For example, you might provide tool instructions like the following for the Grounding with Bing Search tool:

Grounding with Bing Search tool
- Use: Gather external trends or news to enrich the post with real-time insights. 
- Trigger this when:
    - The user asks to reference recent data or competitive context.
    - Example: "Can you reference the latest industry trends?" or "What are competitors doing?".
