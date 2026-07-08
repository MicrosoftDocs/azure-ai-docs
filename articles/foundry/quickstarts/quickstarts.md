---
title: Microsoft Foundry quickstarts
description: "Find a Microsoft Foundry quickstart. Create resources, build your first agent, deploy hosted agents, and evaluate and trace them."
author: aahill
ms.author: aahi
ms.reviewer: aahi
ms.date: 06/19/2026
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: overview
ai-usage: ai-assisted
# customer intent: As a developer, I want a single list of Microsoft Foundry quickstarts so that I can pick the one that matches what I want to build.
---

# Microsoft Foundry quickstarts

Get hands-on with Microsoft Foundry. Each quickstart takes you from zero to a working result in a few minutes. Pick the one that matches what you want to do.

## Set up

| Quickstart | Description |
|---|---|
| [Create resources](../tutorials/quickstart-create-foundry-resources.md) | Create a Foundry project, deploy a model, and grant your team access. |

## Build your first agent

| Quickstart | Description |
|---|---|
| [Create a prompt agent](../agents/quickstarts/prompt-agent.md) | Build a prompt agent with the Microsoft Foundry SDK. |
| [Build agents using the Responses API](../agents/quickstarts/responses-api.md) | Call the Responses API from your own code with the Agent Framework or the OpenAI SDK. |
| [Chat with an agent in code](get-started-code.md) | Use the Microsoft Foundry SDK to build an AI chat application. |

## Deploy hosted agents

| Quickstart | Description |
|---|---|
| [Deploy a hosted agent](../agents/quickstarts/quickstart-hosted-agent.md) | Deploy a containerized agent with the Azure Developer CLI or the Microsoft Foundry Toolkit for Visual Studio Code. |
| [Deploy your own code as a hosted agent](../agents/quickstarts/quickstart-deploy-own-code.md) | Add one hosting library to your existing Python agent and deploy it. |
| [Build a toolbox and use it with a hosted agent](../agents/quickstarts/quickstart-toolbox-agent.md) | Combine web search and the Microsoft Learn MCP server, then use the toolbox from a hosted agent. |
| [Give a hosted agent persistent memory](../agents/quickstarts/quickstart-memory-hosted-agent.md) | Provision a Foundry memory store and deploy a Python hosted agent that remembers facts about each user across sessions. |
| [Add a Foundry IQ knowledge base to a hosted agent](../agents/quickstarts/quickstart-foundry-iq-hosted-agent.md) | Ground a hosted agent in a Foundry IQ knowledge base exposed through a toolbox. |
| [Optimize a hosted agent](../agents/quickstarts/quickstart-optimize-hosted-agent.md) | Run the agent optimizer to automatically improve a hosted agent's instructions, then deploy the winning candidate. |
| [Create a CI/CD pipeline](../agents/quickstarts/set-up-cicd-hosted-agent.md) | Establish a Continuous Integration and Continuous Deployment (CI/CD) pipeline for a hosted agent in Microsoft Foundry project.  |

## Evaluate and trace

| Quickstart | Description |
|---|---|
| [Evaluate a hosted agent](../observability/quickstarts/quickstart-evaluate-hosted-agent.md) | Generate a test suite, run an evaluation, and review the results. |
| [Trace your hosted agent](../observability/quickstarts/quickstart-tracing-hosted-agent.md) | View end-to-end traces with built-in OpenTelemetry instrumentation. |

## Related content

- [What is Microsoft Foundry?](../what-is-foundry.md)
- [Choose how to build](../concepts/choose-build-approach.md)
