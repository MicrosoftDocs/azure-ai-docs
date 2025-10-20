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

The agent building experience in Azure AI Foundry brings many development and observability features, from agent creation all the way to embedding your agent into your applications. You can use the Azure AI Foundry portal or code build, customize, and test your agent's behavior, and then iterate with capabilities like tracing, monitoring, and evaluation to improve your agent's performance. When you're ready, you can publish your agent to preview, share, and see your agent in action within your applications.

## Types of agents

* Declarative - prompt agents, workflow agents
* Code-based - hosted agents, containerized agents

You can create declarative agents in the Azure AI Foundry portal or your own development environment using the CLI, SDK, or REST API. See the quickstart for more information. After you create agents, you can view, test, monitor, and publish them.
<!--The rest of this document will focus on declarative agents.-->

## Creating a prompt agent

If you already know what kind of agent you want to create, you can start creating it and configure your model  instructions and tools. If you'd like to start with some examples, pick an agent manifest closest to your use case, and expand your agent capabilities from there. <!--See more details about agent manifests [here](agent-manifest-doc).-->

<!--
Once you create your first agent, it will show in your agent list, which you can return to at any time via the **Build** top nav item, and selecting **Agents** in the left navigation. Here there will be a grid of Agents, with columns for details of each agent you have in your current Foundry project. Selecting an agent will take you to that agent's playground.
-->


## The agent development lifecycle
The agent building experience offers integrated experiences for each core step of the agent development lifecycle. We recommend utilizing these core capabilities as you develop your production-ready agent application. Each capability has in depth documentation you can go to learn more.

### Saving and versioning
After you create the first version of your agent, you can then save subsequent changes as new versions. You can test unsaved changes in the agent playground, but if you want to view conversation history, monitor your agents performance or run full evaluations, you'll be prompted to save your changes. <!--Learn more about versioning [here](versioning-doc-page).-->

### Adding Tools
You can make your agent more powerful by giving it knowledge (specific files or indexes), or allowing it to take actions (like searching the web or calling external APIs). There are tools available for most use cases, from simple file uploads to custom MCP server connections. For more complicated tools, you may need to configure authentication or add connections as part of attaching it to an agent. You must successfully configure a tool to be able to save an agent with it attached. You can reuse configured tools across agents. See the [tools overview](../../../agents/how-to/tools/overview.md) for more about available tools.

### Publishing your agent

Once you have an agent version you are happy with, publish it (for example to Microsoft 365 or Microsoft Teams) to get a stable endpoint that you can easily see in action in a web app, share, manage, or embed in your existing applications. You and your collaborators can validate the agent's performance, and identify what needs refinement. You can make any necessary updates, and republish a new version at any time. <!--Learn more about what you can do with your published agent [here](publishing-agent-doc-page).-->

### Developing a workflow

If you want to develop a more advanced agentic workflow, for example you want to trigger an action on certain criteria, or orchestrate multiple agents together, you can do so with **Workflows**. This interactive interface lets you define how agentic components like agents, tools, and actions flow together in prescriptive ways. You can test, iterate, monitor, and publish a workflow in similar way to individual Foundry agents. <!--Learn more about developing workflows [here](workflows-doc-page).-->


## Agent playground in Azure AI Foundry portal

The agent playground is where you do your agent development. You can craft your agent's identity, compare models, test different instructions and tool configurations, add specific knowledge and memory customizations, and set restrictions on your agent's behavior. At any point, you can transition to code to continue development in your preferred development environment. For example, you can work on your agent in Visual Studio Code from the Foundry portal, which offers a preconfigured cloud environment to further iterate on your agent using the [Visual Studio extension](../../../how-to/develop/vs-code-agents.md?context=/azure/ai-services/agents/context/context).

### Agent identity configurations

Configurations that define agent identity (what the agent is and what the agent knows), as well as behavior restrictions (how the agent behaves) can be found in the left pane of the agent playground.

### Agent state actions
Actions that change the state of the agent can be found in the top right action bar of the agent playground. These are actions like saving, versioning, deploying and publishing the agent.

### Chat interaction configurations

Configurations that are specific to the chat interactions seen per turn can be found in the top right of the chat pane. Options for interacting with the agent via code instead of via the portal can be found here as well.

### Iterative capabilities

Capabilities used for iterative development and improvement of the agent output like traces, evaluation, and monitoring can be found as separate tabs next to the agent playground. Most of these capabilities have inline experiences within the agent playground, but also have dedicated pages for the full-fledged capabilities. You must save or discard playground changes before navigating to these tabs.

### Moving to code

If you prefer to work in code, there are a couple supported ways to get your agent code into a development environment from which you can test locally and then deploy to Azure.

From the Code tab in the agent playground chat pane, you can take a code snippet that references your agent by ID to a dedicated VS Code for the Web cloud environment, which comes preconfigured with the packages and extensions you need, as well as instructions, to efficiently develop and deploy your Foundry agent to Azure. You can also copy the code snippet directly to your preferred development environment.

## Summary
The NextGen Foundry Portal offers a more cohesive and feature-rich agent building experience, with a robust playground, as well as publishing and observability features that help you move from development into production. Bring your agents to life and get them in the hands of others faster than ever before.