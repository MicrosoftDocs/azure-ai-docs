---
title: Configure guided guardrail setup for an agent
titleSuffix: Azure AI services
description: Learn how to configure guardrails for your agent in Microsoft Foundry by answering guided questions about its users, data, and tools.
author: ssalgadodev
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: how-to
ms.date: 05/21/2026
ms.author: ssalgado
ai-usage: ai-assisted
---

# Configure guided guardrail setup for an agent

In this article, you configure safety and security guardrails for an agent using guided setup in Microsoft Foundry. Instead of selecting controls manually, you answer a short set of questions about your agent's intended users, data handling, and tool usage. Foundry maps your responses to relevant risk categories and applies targeted controls at the correct intervention points: user input, tool calls, tool responses, and output.

Each agent is purpose-built for a specific scenario, so guardrails should be tailored accordingly—not applied as a single default. Guided setup ensures that protections are scoped to where they're needed and that the agent stays both safe and usable. For more information about guardrails concepts, see [TO VERIFY: Guardrails overview link].

## Prerequisites

- An active agent in Microsoft Foundry. To create one, see [create a prompt agent quickstart](../../../foundry/agents/quickstarts/prompt-agent.md).

## Open guided guardrail setup

1. In [Microsoft Foundry](https://ai.azure.com), open a project.
1. In the left navigation, select **Agents**, then select the agent you want to configure.
1. On the agent detail page, select the **Guardrails** tab.
1. Select **Guided setup** to start the guided configuration experience.

## Specify who the agent is for

The first set of questions identifies who uses the agent and the level of trust to apply to their inputs.

1. For **Who will use this agent?**, select whether the agent is accessed by public users or internal teams.
   - **Public users**: applies stricter content safety filtering and jailbreak protections, because broader access increases exposure to unexpected or adversarial inputs.
   - **Internal teams**: applies lighter controls appropriate for trusted, authenticated users.
1. Select **Next** to continue.

## Define input and data handling

The second set of questions determines how the agent receives information and what data it processes. External or untrusted inputs increase the risk of prompt injection. Sensitive data increases the risk of unintended exposure.

1. For **Where does the agent receive inputs from?**, select all sources that apply—for example, user messages, uploaded files, or external APIs.
1. For **Will the agent access, process, or return sensitive data?**, select **Yes** or **No**.
   - If yes, select whether the data includes personally identifiable information (PII). Selecting **Yes** enables PII detection and data protection controls.
1. Select **Next** to continue.

## Configure tool and action usage

The third set of questions covers the agent's tool integrations and action capabilities. Tool usage and real-world actions introduce additional risks that require targeted controls.

1. For **Does the agent call external tools?**, select **Yes** or **No**.
   - If yes, Foundry enables tool response validation and spotlighting to guard against prompt injection via tool outputs.
1. For **Can the agent take real-world or consequential actions?** (for example, send emails, modify records, or call external services), select **Yes** or **No**.
   - If yes, task adherence controls and action validation are added to reduce the risk of misaligned or unintended actions.
1. For **Does the agent generate, modify, or execute code?**, select **Yes** or **No**.
   - If yes, protected material detection and code safety controls are enabled.
1. Select **Next** to review your recommendations.

## Review and apply guardrail recommendations

Foundry displays a summary of the recommended guardrails based on your answers, along with the intervention points where each control is applied.

| Intervention point | Description |
|--------------------|-------------|
| User input | Controls applied before the agent processes a message |
| Tool calls | Controls applied before the agent invokes a tool |
| Tool responses | Controls applied to content returned by tools |
| Output | Controls applied to the agent's final response |

1. Review the recommended controls. To adjust a recommendation, select **Edit** next to the control and modify the configuration.
1. When you're satisfied with the configuration, select **Apply guardrails**.
1. Confirm the changes when prompted.

The guardrails are now active for your agent. You can return to the **Guardrails** tab at any time to update the configuration as your agent's scenario evolves.

> [!NOTE]
> Agents built on the same model can require different guardrails depending on their scenario. If you deploy multiple agents, run guided setup independently for each one.

## Next step

> [!div class="nextstepaction"]
> [[TO VERIFY: Next step link text]](../how-to/monitor-agents.md)
