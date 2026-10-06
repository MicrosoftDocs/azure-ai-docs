---
title: "Create an agent with Microsoft Foundry Toolkit for Visual Studio Code"
description: "Choose a prompt or hosted agent and start with Agent Builder, samples, or GitHub Copilot in Microsoft Foundry Toolkit for Visual Studio Code."
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
content_well_notification:
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 09/10/2026
ms.reviewer: erichen
ms.author: rotabor
author: bobtabor-msft
ms.custom: doc-kit-assisted
#CustomerIntent: As a developer, I want to choose an agent creation route in Foundry Toolkit so that I can build an agent with the right level of control.
---

# Create an agent with Microsoft Foundry Toolkit for Visual Studio Code

Use Microsoft Foundry Toolkit for Visual Studio Code to configure a prompt
agent or develop a code-based hosted agent. Choose a creation route based on
whether instructions and supported tools meet your needs, or you need custom
runtime logic.

## Prerequisites

- [Install Microsoft Foundry Toolkit for Visual Studio Code](install-foundry-toolkit-visual-studio-code.md).
- For agents that use Foundry resources,
  [set up a Foundry project](set-up-foundry-project-visual-studio-code.md).
  Follow the guide for your chosen route for model, permission, and runtime
  requirements.
- For Copilot-assisted coding, access to
  [GitHub Copilot in Visual Studio Code](https://code.visualstudio.com/docs/copilot/overview).

## Choose an agent type

Foundry supports [prompt agents and hosted agents](../../agents/concepts/development-lifecycle.md#agent-types-in-microsoft-foundry).
Both agent types can use tools and integrate into applications. Prompt agents aren't
limited to prototypes.

| Compare | Prompt agent | Hosted agent |
| --- | --- | --- |
| Define behavior | Configure a model, instructions, and supported tools. | Implement custom logic with a framework or your own code. |
| Use it for | Tasks that instructions and supported tools can handle, such as answering questions or summarizing documents. | Custom orchestration, dependencies, or runtime behavior, such as a multi-agent workflow. |
| What you maintain | The agent configuration and saved versions. | The agent code, dependencies, packaging, and deployment configuration. |
| Where to start | Agent Builder. | Hosted-agent samples or Copilot-assisted coding. |

Start with a prompt agent when its configuration options meet your needs.
Choose a hosted agent when you need more control over execution. For details,
see [When to use hosted agents](../../agents/concepts/hosted-agents.md#when-to-use-hosted-agents).

## Open Create Agent

Open the creation page to choose how to build your agent.

1. In the Activity Bar, select **Foundry Toolkit**.
1. Under **Developer Tools**, expand **Build**, and select **Create Agent**.

   :::image type="content" source="../../media/how-to/create-agent-vs-code/create-agent.png" alt-text="Screenshot of Create Agent with options to code from samples, code with Copilot, or build an agent in Agent Builder." lightbox="../../media/how-to/create-agent-vs-code/create-agent.png":::

If Developer Tools uses **Group by Resource**, find **Create Agent** under
**Agent Dev Tools** instead of **Build**.

## Choose a creation route

Select the route that matches your agent type, and then follow its guide to
configure, test, and save or deploy the agent.

| Route | Action in Create Agent | Next guide |
| --- | --- | --- |
| Agent Builder | Select **Build an agent** to configure a prompt agent without a hosted-agent code project. | [Create a prompt agent](create-prompt-agent-visual-studio-code.md). |
| Hosted-agent samples | Under **Code an agent from samples**, select a framework or **Browse all samples**. Choose a sample for your scenario. | For code-based orchestration, [create hosted agents](vs-code-agents-workflow-pro-code.md). For other scenarios, follow the selected sample's generated `README.md`. |
| Copilot-assisted coding | Select **Code an agent with Copilot** to develop agent code with GitHub Copilot and Foundry skills. | [Use the Microsoft Foundry Skill in coding agents](use-microsoft-foundry-skill.md). Review generated code and test it before deployment. |

Agent Builder also supports locally stored prompts. Their storage, tools, and
evaluation options differ from Foundry prompt agents. See
[Work with local prompts](create-prompt-agent-visual-studio-code.md#work-with-local-prompts).

## Choose how to orchestrate or schedule work

For new code-based workflows, use Microsoft Agent Framework through the sample
or Copilot route. To invoke an existing agent on a trigger or schedule, see
[Routines in Foundry Agent Service (preview)](../../agents/concepts/routines.md).

> [!IMPORTANT]
> Declarative workflows in Microsoft Foundry are in preview and retire on
> December 1, 2026. This retirement doesn't affect code-based orchestration in
> hosted agents. To work with an existing declarative workflow, see
> [Use and migrate declarative agent workflows](vs-code-agents-workflow-low-code.md).

## Related content

Use these guides as you develop and integrate your agent:

- [Microsoft Foundry Toolkit for Visual Studio Code overview](get-started-projects-visual-studio-code.md)
- [Agent development lifecycle](../../agents/concepts/development-lifecycle.md)
- [Publish an agent application](../../agents/how-to/agent-applications.md)
