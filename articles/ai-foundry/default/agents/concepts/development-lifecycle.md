---
title: 'Understanding the agent development lifecycle'
titleSuffix: Azure AI Foundry
description: Understanding the agent development lifecycle
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: conceptual
ms.date: 10/16/2025
author: aahill
ms.author: aahi
---

# Understanding the agent development lifecycle

The agent building experience in Azure AI Foundry brings many development and observability features, from agent creation all the way to embedding your agent into your applications. You can use the Azure AI Foundry portal, or code, to build, customize, and test your agent's behavior, and then iterate with capabilities like tracing, evaluation and monitoring to improve your agent's performance. When you're ready, you can publish your agent to preview, share, and see your agent in action within your applications.

## Types of agents

* Declarative - prompt agents, workflow agents
* Hosted agents

You can create declarative agents in the Azure AI Foundry portal or your own development environment using the CLI, SDK, or REST API. See the quickstart for more information. After you create or select a declarative prompt agent, it can be viewed, edited, tested, evaluated, monitored and published.

Workflows have their own development interface in the portal, but the same lifecycle applies. <!--Learn more about developing workflows [here](workflows-doc-page).-->

Hosted agents must be created and developed in code, and can't be edited in the agent building interface. But they can be viewed, tested, evaluated, monitored and published just like declarative agents. <!--Learn more about developing hosted agents [here](hosted-agents-doc-page).-->


## Creating a prompt agent

If you already know what kind of agent you want to create, you can name it and then start configuring your model instructions and tools. If you'd like to start with some examples, pick an agent manifest from the catalog that matches most closely to your use case, and expand your agent capabilities from there. <!--See more details about agent manifests [here](agent-manifest-doc).-->

> **Note**: Once you name your agent, the name cannot be changed. In code, you will refer to your agent by <agent_name>:\<version>. You will be able to set the display name of your agent in your published application scenarios.

## Developing in code

If you prefer to work in code, there are a couple supported ways to bring your agent code into a development environment from which you can test locally and then deploy to Azure.

From the Code tab in the agent playground chat pane, you can take a code snippet that references your agent to a dedicated VS Code for the Web cloud environment, which comes preconfigured with the packages and extensions you need, as well as instructions to efficiently develop and deploy your Foundry agent to Azure. You can also copy the code snippet directly to your preferred development environment. <!--Learn more about the VS Code capability here [here](/azure/ai-foundry/concepts/concept-playgrounds#open-in-vs-code-capability).-->

## The agent development lifecycle
The agent building experience offers integrated experiences for each core step of the agent development lifecycle. We recommend utilizing these core capabilities as you develop your production-ready agent application. Each capability has in depth documentation you can dive into to learn more.

### Saving and versioning
After you create the first version of a declarative agent, you can then save subsequent changes as new versions. You can test unsaved changes in the agent playground, but if you want to view conversation history, monitor your agents performance or run full evaluations, you'll be prompted to save your changes. <!--Learn more about versioning [here](versioning-doc-page).-->

### Adding tools
You can make your agent more powerful by giving it knowledge (specific files or indexes), or allowing it to take actions (like searching the web or calling external APIs). There are tools available for most use cases, from simple file uploads to custom MCP server connections. For more complicated tools, you may need to configure authentication or add connections as part of attaching it to an agent. You must successfully configure a tool to be able to save an agent with it attached. You can reuse configured tools across agents. See the [tools overview](../../../agents/how-to/tools/overview.md) for more about available tools.

### Publishing your agent

Once you have an agent version you are happy with, publish it to get a stable endpoint that you can easily see in action in a web app, share, manage, or embed in your existing applications. You and your collaborators can validate the agent's performance, and identify what needs refinement. You can make any necessary updates, and re-publish a new version at any time. The Foundry portal also offers a streamlined way to publish your agent to Microsoft 365 Copilot and Microsoft Teams. <!--Learn more about publishing your agent [here](publishing-agent-doc-page).-->

### Developing a workflow

If you want to develop a more advanced agentic workflow, for example you want to trigger an action on certain criteria, or orchestrate multiple agents together, you can do so with **Workflows**. This interactive interface lets you define how agentic components like agents, tools, and actions flow together in prescriptive ways. You can test, iterate, monitor, and publish a workflow in similar way to individual Foundry agents. <!--Learn more about developing workflows [here](workflows-doc-page).-->
