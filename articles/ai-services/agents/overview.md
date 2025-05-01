---
title: What is Azure AI Foundry Agent Service?
titleSuffix: Azure AI Foundry
description: Learn how to create agents that apply advanced language models for workflow automation.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: overview
ms.date: 01/10/2025
ms.custom: azure-ai-agents
---

# What is Azure AI Foundry Agent Service (Preview)?

[Azure AI Foundry Agent Service](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/introducing-azure-ai-agent-service/4298357) is a fully managed service designed to empower developers to securely build, deploy, and scale high-quality, and extensible AI agents without needing to manage the underlying compute and storage resources. What originally took hundreds of lines of code to support [client side function calling](/azure/ai-services/openai/how-to/function-calling) can now be done in just a few lines of code with Azure AI Foundry Agent Service.

## What is an AI agent?

Within Azure AI Foundry, an AI Agent acts as a "smart" microservice that can be used to answer questions (RAG), perform actions, or completely automate workflows. It achieves this by combining the power of generative AI models with tools that allow it to access and interact with real-world data sources.

Because Azure AI Foundry Agent Service uses the same wire protocol as [Azure OpenAI Assistants](/azure/ai-services/openai/how-to/assistant), you can use either [OpenAI SDKs](./quickstart.md?pivots=programming-language-python-openai) or [Azure AI Foundry SDKs](./quickstart.md?programming-language-python-azure) to create and run an agent in just a few lines of code. For example, to create an AI Agent with Azure AI Foundry SDK, you can simply  define which model the AI uses, the instructions for how it should complete tasks, and the tools it can use to access and interact with other services.

```python
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-agent",
    instructions="You are helpful agent",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
```

After defining an agent, you can start asking it to perform work by invoking a run on top of an activity thread, which is simply a conversation between multiple agents and users. 

```python
# Create a thread with messages
thread = project_client.agents.create_thread()
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Could you please create a bar chart for the operating profit using the following data and provide the file to me? Company A: $1.2 million, Company B: $2.5 million, Company C: $3.0 million, Company D: $1.8 million",
)

# Ask the agent to perform work on the thread
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)

# Fetch and log all messages to see the agent's response
messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")
```

Whenever the run operation is invoked, Azure AI Foundry Agent Service will complete the entire tool calling lifecycle for you by 1) running the model with the provided instructions, 2) invoking the tools as the agent calls them, and 3) returning the results back to you.

Once you've gotten the basics, you can start using multiple agents together to automate even more complex workflows with [AutoGen](https://microsoft.github.io/autogen/0.2/docs/Getting-Started/) and [Semantic Kernel](/semantic-kernel). Because Azure AI Foundry Agent Service is a fully managed service, you can focus on building workflows and the agents that power them without needing to worry about scaling, security, or management of the underlying infrastructure for individual agents.

## Why use Azure AI Foundry Agent Service?

When compared to developing with the [Model Inference API](/rest/api/aifoundry/modelinference) directly, Azure AI Foundry Agent Service provides a more streamlined and secure way to build and deploy AI agents. This includes:
- **Automatic tool calling** – no need to parse a tool call, invoke the tool, and handle the response; all of this is now done server-side
- **Securely managed data** – instead of managing your own conversation state, you can rely on threads to store all the information you need
- **Out-of-the-box tools** – In addition to the file retrieval and code interpreter tools provided by Azure OpenAI Assistants, Azure AI Foundry Agent Service also comes with a set of tools that you can use to interact with your data sources, such as Bing, Azure AI Search, and Azure Functions.

What originally took hundreds of lines of code can now be done in just a few with Azure AI Foundry Agent Service.

### Comparing Azure agents and Azure OpenAI assistants

Both services enable you to build agents using the same API and SDKs, but if you have additional enterprise requirements, you might want to consider using Azure AI Foundry Agent Service. Azure AI Foundry Agent Service provides all the capabilities of assistants in addition to:

**Flexible model selection** - Create agents that use Azure OpenAI models, or others such as Llama 3, Mistral and Cohere. Choose the most suitable model to meet your business needs.

**Extensive data integrations** - Ground your AI agents with relevant, secure enterprise knowledge from various data sources, such as Microsoft Bing, Azure AI Search, and other APIs. 

**Enterprise grade security** - Ensure data privacy and compliance with secure data handling, keyless authentication, and no public egress. 

**Choose your storage solution** - Either bring your own Azure Blob storage for full visibility and control of your storage resources, or use platform-managed storage for secure ease-of-use.  

## Responsible AI

At Microsoft, we're committed to the advancement of AI driven by principles that put people first. Generative models such as the ones available in Azure OpenAI have significant potential benefits, but without careful design and thoughtful mitigations, such models have the potential to generate incorrect or even harmful content. Microsoft has made significant investments to help guard against abuse and unintended harm, which includes incorporating Microsoft’s <a href="https://www.microsoft.com/ai/responsible-ai?activetab=pivot1:primaryr6" target="_blank">principles for responsible AI use</a>, adopting a [Code of Conduct](/legal/ai-code-of-conduct?context=/azure/ai-services/agents/context/context) for use of the service, building [content filters](/azure/ai-services/content-safety/overview) to support customers, and providing responsible AI [information and guidance](/legal/cognitive-services/openai/transparency-note?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=image) that customers should consider when using Azure AI Foundry Agent Service.

## Get started with Azure AI Foundry Agent Service

To get started with Azure AI Foundry Agent Service, you need to create an Azure AI Foundry hub and an Agent project in your Azure subscription. 

Start with the [quickstart](./quickstart.md) guide if it's your first time using the service.
1. You can create a AI hub and project with the required resources. 
1. After you create a project, you can deploy a compatible model such as GPT-4o.
1. When you have a deployed model, you can also start making API calls to the service using the SDKs.


## Next steps

Learn more about the [models that power agents](./concepts/model-region-support.md).