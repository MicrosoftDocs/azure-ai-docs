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

* Prompt-based
* Workflows
* Hosted

You can create prompt-based agents and workflows in the Azure AI Foundry portal or your own development environment using the CLI, SDK, or REST API. See the quickstart for more information.

A **prompt-based agent** is a declaratively defined single agent that combines model configuration, instruction, tools, and natural language prompts to drive behavior. You can also make your agent even more powerful by attaching knowledge and memory capabilities. Prompt-based agents can be edited, versioned, tested, evaluated, monitored and published from the agent building interface. <!-- Learn more about the playground interface [here](link-to-appropriate-playground-platform-doc).-->

If you want to develop a more advanced agentic workflow, for example you want to trigger an action on certain criteria, or orchestrate multiple agents together, you can do so with **Workflows**. **Workflows** have their own development interface in the portal, but the same lifecycle applies. <!--Learn more about developing workflows [here](workflows-doc-page).-->

**Hosted agents** are containerized agents created and deployed in code that are hosted by Foundry. They can't be edited in the agent building interface, but they can be viewed, tested, evaluated, monitored and published just like prompt-based agents and workflows. <!--Learn more about developing hosted agents [here](hosted-agents-doc-page).-->


## Creating a prompt-based agent

If you already know what kind of agent you want to create, you can name it and then quickly start configuring your model instructions and tools. If you don't already have a model deployed, an available model will be deployed for you. If you'd like to start with some examples, pick a manifest (a pre-defined agent definition to help you get started) from the agent catalog that most closely matches your use case, and expand your agent capabilities from there. <!--See more details about agent manifests [here](agent-manifest-doc).-->

> [!NOTE]
> Once you name your agent, the name cannot be changed. In code, you will refer to your agent by `<agent_name>:<version>`. You will be able to set the display name of your agent in your published application scenarios.

## Developing in code

If you prefer to work in code, there are a couple supported ways to bring your agent code into a development environment from which you can test locally and then deploy to Azure.

From the Code tab in the agent playground chat pane, you can take a code snippet that references your agent to a dedicated VS Code for the Web cloud environment, which comes preconfigured with the packages and extensions you need, as well as instructions to efficiently develop and deploy your Foundry agent to Azure. You can also copy the code snippet directly to your preferred development environment. <!--Learn more about the VS Code capability here [here](/azure/ai-foundry/concepts/concept-playgrounds#open-in-vs-code-capability).-->

## The agent development lifecycle
The agent building experience offers integrated experiences for each core step of the agent development lifecycle. We recommend utilizing these core capabilities as you develop your production-ready agent application. Each capability has in depth documentation you can dive into to learn more.

### Saving and versioning
After you create the first version of a prompt-based agent or a workflow, you can then save subsequent changes as new versions. You can test unsaved changes in the agent playground, but if you want to view conversation history, monitor your agents performance or run full evaluations, you'll be prompted to save your changes. <!--Learn more about versioning [here](versioning-doc-page).-->

### Adding tools
You can make your agent more powerful by giving it knowledge (specific files or indexes), or allowing it to take actions (like searching the web or calling external APIs). There are tools available for most use cases, from simple file uploads to custom MCP server connections. For more complicated tools, you may need to configure authentication or add connections as part of attaching it to an agent. You must successfully configure a tool to be able to save an agent with it attached. You can reuse configured tools across agents. See the [tools overview](../../../agents/how-to/tools/overview.md) for more about available tools.

### Publishing your agent or workflow

Once you have an agent or workflow version you're happy with, publish it to get a stable endpoint that you can easily see in action in a web app, share, manage, or embed in your existing applications. You and your collaborators can validate performance, and identify what needs refinement. You can make any necessary updates, and re-publish a new version at any time. The Foundry portal also offers a streamlined way to publish your agent or workflow to Microsoft 365 Copilot and Microsoft Teams. <!--Learn more about publishing [here](publishing-agent-doc-page).-->

