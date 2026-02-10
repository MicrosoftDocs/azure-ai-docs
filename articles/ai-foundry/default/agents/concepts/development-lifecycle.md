---
title: Agent development lifecycle
titleSuffix: Microsoft Foundry
description: Learn the agent development lifecycle in Microsoft Foundry, from creating and versioning to tracing, evaluation, publishing, and monitoring.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 02/02/2026
author: aahill
ms.author: aahi
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Agent development lifecycle

The agent development lifecycle in Microsoft Foundry spans from initial creation through production monitoring. Following this lifecycle helps you build reliable agents, catch issues early, and ship with confidence. Use the Foundry portal or code to build, customize, and test your agent's behavior. Then iterate with tracing, evaluation, and monitoring to improve quality and reliability. When you're ready, publish your agent as an agent application to share it and integrate it into your apps.

This article is for developers who want to build, test, and ship production-ready agents.

## Prerequisites

- A [Microsoft Foundry project](../../../how-to/create-projects.md)
- Familiarity with the [Agents playground](../../../concepts/concept-playgrounds.md)
- For code development: Familiarity with the [development environment setup](../../../how-to/develop/install-cli-sdk.md)

## Lifecycle at a glance

Use this lifecycle as a practical checklist while you build and ship an agent.

1. **Choose an agent type**: Start with a prompt-based agent, a workflow, or a hosted agent.
1. **Create your agent and start testing**: Iterate in the playground or in code.
1. **Add tools and data**: Attach tools for retrieval and actions, and validate the configuration before you save.
1. **Save changes as versions**: Capture meaningful milestones and compare versions.
1. **Debug with tracing**: Use tracing to confirm tool calls, latency, and end-to-end behavior. For details, see [Agent tracing overview](../../observability/concepts/trace-agent-concept.md).
1. **Evaluate quality and safety**: Run repeatable evaluations to catch regressions before publishing. For conceptual guidance, see [Agent evaluators](../../../concepts/evaluation-evaluators/agent-evaluators.md).
1. **Publish and integrate**: Publish a stable endpoint and integrate it into your application. For steps, see [Publish and share agents in Microsoft Foundry](../how-to/publish-agent.md).
1. **Monitor and iterate**: Monitor performance and quality in production, then update and republish as needed. For guidance, see [Monitor quality and safety](../../../how-to/monitor-quality-safety.md).

## Agent types in Microsoft Foundry

There are three types of agents:

- **Prompt-based**: A prompt-based agent is a declaratively defined single agent that combines model configuration, instructions, tools, and natural language prompts to drive behavior. Extend it by attaching tools for knowledge and memory. Edit, version, test, evaluate, monitor, and publish prompt-based agents from the [Agents playground](../../../concepts/concept-playgrounds.md) in the Foundry portal.

- **Workflow**: Use workflows to build a more advanced workflow that orchestrates a sequence of actions or coordinates multiple agents. Workflows have their own interface in the portal, but the same lifecycle applies. For details, see [Build a workflow in Microsoft Foundry](./workflow.md).

- **Hosted (preview)**: Hosted agents are containerized agents that you build in code by using supported frameworks or custom code. Foundry Agent Service deploys and manages these agents. You don't edit hosted agents in the agent-building UI, but you can still invoke, evaluate, monitor, and publish them. For details, see [What are hosted agents?](./hosted-agents.md)

Create prompt-based agents and workflows in the Foundry portal or your own development environment by using the CLI, SDK, or REST API. For more information, see the [quickstart](../../../quickstarts/get-started-code.md).

## Creating a prompt-based agent

If you already know what kind of agent you want to create, name it and then start configuring its model instructions and tools.

> [!NOTE]
> After you name your agent, you can't change the name. In code, you refer to your agent by `<agent_name>:<version>`.

## Develop agents in code

If you prefer to work in code, use supported ways to bring your agent code into a development environment from which you can test locally and then deploy to Azure.

From the **Code** tab in the agent playground's chat pane, you can take a code snippet that references your agent to a dedicated Visual Studio Code for the Web cloud environment. The snippet comes preconfigured with the packages and extensions that you need, along with instructions to efficiently develop and deploy your Foundry agent to Azure. You can also copy the code snippet directly to your preferred development environment. For details, see the [playground documentation](../../../concepts/concept-playgrounds.md#open-in-vs-code-capability).

## Core capabilities for the agent development lifecycle

The agent building experience offers integrated experiences for each core step of the agent development lifecycle. Use these core capabilities as you develop your production-ready agent application. Each capability has in-depth documentation where you can learn more.

### Save changes as versions

After you create the first version of a prompt-based agent or a workflow, save subsequent changes as new versions. You can test unsaved changes in the agent playground. But if you want to view conversation history, monitor your agent's performance, or run full evaluations, you need to save your changes.

Agent versioning provides the following capabilities for managing agent configurations and iterations. This system ensures that all changes are tracked, testable, and comparable across versions.

- **Version immutability**: Each version of an agent is immutable after you save it. Any modifications to an existing version require saving and creating a new version. This requirement helps ensure version integrity and prevents accidental overwrites.
- **Draft state management**: You can test agents in an unsaved state for experimentation. You lose unsaved changes if you leave the Foundry portal, so save frequently to preserve important modifications.
- **Version control operations**: You can direct requests to specific agent versions to enable controlled deployment and rollback capabilities.
- **Version history navigation**: Access the version history for any agent, go to any specific version, and perform the following comparisons:

  | Comparison type | Description |
  | --------------- | ----------- |
  | Agent setup | Compare configuration settings between versions using the version dropdown list |
  | Chat output | Analyze response differences between agent versions using identical inputs |
  | YAML definition | Review differences in agent definitions |

### Add tools

Make your agent more powerful by giving it knowledge (specific files or indexes) or by allowing it to take actions (calling external APIs). Tools are available for most use cases, from simple file uploads to custom Model Context Protocol (MCP) server connections. For more complicated tools, you might need to configure authentication or add connections as part of attaching them to an agent.

To save an agent with a tool attached, you must successfully configure the tool. Reuse configured tools across agents. For information about available tools, see the [tools catalog](./tool-catalog.md).

### Debug and validate by using tracing (preview)

As you add tools and iterate on prompts, use tracing to validate end-to-end behavior:

- Confirm whether the agent called the tools you expected.
- Inspect tool inputs and outputs.
- Identify latency hotspots across model and tool calls.

For more information, see [Agent tracing overview](../../observability/concepts/trace-agent-concept.md).

### Evaluate quality and safety (preview)

Before you publish your agent (and after any meaningful change), run evaluations to catch regressions and measure quality consistently across versions.

- For the key evaluation dimensions for agents, see [Agent evaluators](../../../concepts/evaluation-evaluators/agent-evaluators.md).
- For a code-first workflow you can automate, see [Evaluate your AI agents locally](../../../how-to/develop/agent-evaluate-sdk.md).

### Monitor after publishing

After you publish an agent application, treat it like production software:

- Monitor quality and safety signals.
- Review traces when behavior changes.
- Update and republish when you fix issues or make improvements.

For guidance, see [Monitor quality and safety](../../../how-to/monitor-quality-safety.md).

### Plan for identity and permissions

Tools and downstream resources often require authentication. When you publish an agent, its identity and permission model can change. Make sure your published agent has only the access it needs.

For details, see [Agent identity concepts in Microsoft Foundry](./agent-identity.md).

### Security and access

Treat your agent configuration like application code. Protect secrets and permissions throughout the lifecycle:

- Use least privilege and role assignments instead of embedding keys. For more information, see [Role-based access control in Foundry portal](../../../concepts/rbac-foundry.md).
- Store secrets in a managed secret store and reference them through connections instead of hardcoding them in code, configuration files, or prompts. For guidance, see [Set up a Key Vault connection](../../../how-to/set-up-key-vault-connection.md).
- Before publishing, confirm that the agent identity and tool connections in the published agent application have only the access they need. For details, see [Agent identity concepts in Microsoft Foundry](./agent-identity.md).

### Publish your agent or workflow

After you create an agent or workflow version that you're happy with, [publish it as an agent application](../how-to/publish-agent.md). You get a stable endpoint that you can open and test in the browser, share with others, or embed in your existing applications. You and your collaborators can validate performance and identify what needs refinement. Make any necessary updates and republish a new version at any time.

> [!IMPORTANT]
> Permissions assigned to the project identity don't automatically transfer to the published agent. After publishing, reassign the necessary privileges to the agent application's identity.

## Common agent development pitfalls

- **Unsaved changes are temporary**: If you want to compare versions, view history, or run full evaluations, save your changes as a version.
- **Tools must be configured before saving**: If a tool requires authentication or a connection, complete setup before you save.
- **Publishing can require permission updates**: After publishing, recheck resource access for the published agent identity and remove any access the agent no longer needs.

## Related content

**Learn more about agent types:**

- [What are hosted agents?](./hosted-agents.md)
- [Agent runtime components](./runtime-components.md)

**Configure and extend agents:**

- [Discover tools in Foundry Tools](./tool-catalog.md)
- [Best practices for using tools in Microsoft Foundry Agent Service](./tool-best-practice.md)

**Publish and monitor agents:**

- [Publish and share agents in Microsoft Foundry](../how-to/publish-agent.md)
- [Monitor quality and safety](../../../how-to/monitor-quality-safety.md)

**Debug and evaluate:**

- [Agent tracing overview](../../observability/concepts/trace-agent-concept.md)
- [Agent evaluators](../../../concepts/evaluation-evaluators/agent-evaluators.md)
