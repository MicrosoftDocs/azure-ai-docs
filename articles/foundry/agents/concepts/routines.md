---
title: "Routines in Foundry Agent Service (preview)"
description: "Learn how routines in Foundry Agent Service invoke agents from project-native timers, recurring schedules, and events such as GitHub issues, with governed connections and run history."
author: aahill
ms.author: aahi
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: concept-article
ms.date: 07/08/2026
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
---

# Routines in Foundry Agent Service (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Routines in Foundry Agent Service let you run an agent automatically when a defined trigger fires. Use a routine when you want a project-native way to say, "When a specific time, schedule, or event occurs, invoke this agent."

Without routines, teams often build this trigger layer themselves by combining technologies such as schedulers, Logic Apps, Azure Functions, queues, custom storage, and authentication code. Routines move that operational glue into Foundry so the trigger, action, permissions, connections, and run history live with the agent in the same Foundry project.

Use routines for lightweight agent automation, such as daily summaries, one-time reminders, or periodic checks. If your scenario needs branching, multiple agents, human approval steps, or complex state, use a workflow instead.

## What a routine contains

A routine has one trigger and one action.

| Component | Description |
| --- | --- |
| **Trigger** | Defines when the routine starts. A trigger can be a one-time timer, a recurring schedule, or an event such as a GitHub issue being opened or closed. |
| **Action** | Defines what happens after the trigger fires. In the preview, the action invokes one prompt agent or hosted agent through the existing agent endpoint. |
| **Input** | Provides the user input sent to the agent. Input can be text or JSON. |
| **Lifecycle state** | Determines whether the routine is enabled or disabled. You can update, enable, disable, or delete a routine without recreating the agent. |
| **Run history** | Records each trigger run, including inputs, outputs, status, and a link to the related agent response and trace details. |

The one-trigger, one-action model keeps routines focused on a single question: *when should this agent run?* It doesn't replace orchestration. When you need multiple actions, multiple agents, or conditional logic, create a workflow instead. The agent that a routine invokes can implement its own internal workflow by using frameworks such as Microsoft Agent Framework or LangGraph.

## Trigger types

Routines support three trigger types in the preview: timer, recurring, and event. The recurring trigger is also referred to as a recursive trigger.

| Trigger type | When to use it | Example |
| --- | --- | --- |
| **Timer** | Run an agent once at a specific date and time. After the timer fires, the routine becomes inactive. | Run a migration-readiness agent at `2026-06-01T09:00:00Z`. |
| **Recurring** | Run an agent repeatedly on a cron-style schedule. | Run a support-summary agent every weekday at 7 AM. |
| **Event** | Run an agent when an external event fires. In the preview, the `github_issue` event fires when an issue is opened or closed in a watched GitHub repository. | Triage an issue when it's opened in a GitHub repository. |

## How routines run

When you enable a routine, Foundry manages the trigger and dispatch path for you.

1. The trigger fires from a timer, a recurring schedule, or an external event.
1. Foundry creates a routine run record in the project.
1. Foundry invokes the configured agent endpoint with the routine input.
1. The agent processes the request by using its configured model, instructions, tools, and identity.
1. Foundry stores the routine run status and links the run to the agent response and trace details.

This flow uses the existing agent invocation path, so routines don't introduce a separate runtime for agent logic. The agent continues to use the same configuration, tools, and observability features that it uses when invoked from an application or playground.

## Connections, identity, and governance

Routines are scoped to a Foundry project. You manage routines with the same project governance model you use for agents, tools, and connections. For more information, see [Azure role-based access control in Foundry](../../concepts/rbac-foundry.md).

Event triggers use project connections to authenticate to the external system. For example, the `github_issue` trigger relies on a GitHub connector connection that Foundry provisions in your account's connector namespace. For more information, see [Add managed MCP servers powered by connector namespaces](../how-to/tools/connectors.md).

This project-scoped design provides the following benefits:

- **No separate scheduler resource to manage**: Create and operate routines from Foundry instead of provisioning separate automation infrastructure.
- **Shared governance**: Apply project-level access control to routine management and agent invocation.
- **Observable runs**: Review routine runs alongside the agent responses and traces that they create.

Don't include secrets, credentials, or personal access tokens in routine input or prompts. Use project connections and Microsoft Entra ID-based access wherever supported.

## Monitor and operate routines

After you create a routine, use the run history to understand what happened each time the trigger fired. Run history helps you answer operational questions such as:

- Did the trigger fire?
- What input was sent to the agent?
- Did the agent invocation complete or fail?
- What response did the agent produce?
- Which trace contains the detailed model, tool, and latency information for that invocation?

You can pause a routine by disabling it and resume it by enabling it again. You can also update the trigger, action, or input for an existing routine without recreating the agent.

## Agent-scheduled reminders

Routines start an agent from an external trigger. A hosted agent can also schedule *itself* to run again later by calling a built-in reminder tool that you expose through a [toolbox](../how-to/tools/toolbox.md). The agent decides during a run that it needs to follow up, chooses the delay, and the service re-invokes the agent on the same conversation when the delay elapses. Use this pattern for agent-driven follow-ups, such as checking back on a long-running task. For steps, see [Automate agents with routines](../how-to/use-routines.md#let-an-agent-schedule-its-own-reminders).

## Routines and workflows

Routines and workflows both help automate agent scenarios, but they solve different problems.

| Dimension | Routines | Workflows |
| --- | --- | --- |
| **Question answered** | When should my agent run? | How should multiple steps, decisions, or agents connect? |
| **Mental model** | Trigger to agent. | Graph of nodes, edges, branching, and state. |
| **Agent relationship** | Extends an existing agent with an automatic trigger. | Orchestrates agents and business logic in a separate workflow. |
| **Multi-agent support** | No. A routine invokes one agent. | Yes. Use workflows for multi-agent orchestration. |
| **Best for** | Timers, schedules, and lightweight automation. | Branching, approvals, multi-step processes, and complex stateful automation. |

Use a routine first when the automation is simply "run this agent when something happens." Move to workflows when the automation needs coordination logic beyond a single agent invocation.

## Preview limitations

The preview has the following limitations:

- A routine has exactly one trigger and one action.
- The only action type is invoking one Foundry agent.
- Supported trigger types are timer, recurring, and event (GitHub issue) triggers.

## Related content

- [Agent development lifecycle](./development-lifecycle.md)
- [Build a workflow in Microsoft Foundry](./workflow.md)
- [Automate agents with routines](../how-to/use-routines.md)
- [Agent tracing in Microsoft Foundry](../../observability/concepts/trace-agent-concept.md)
