---
title: "What is an autopilot in Microsoft Foundry?"
description: "Learn what an autopilot is in Microsoft Foundry, how its identity model differs from other agents, and why you build a blueprint rather than an autopilot."
author: fosteramanda
ms.author: fosteramanda
ms.reviewer: aahi
ms.date: 08/25/2026
ms.topic: concept-article
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to understand what makes an agent an autopilot so that I can decide whether to build one and how it differs from the agents I build today.
---

# What is an autopilot in Microsoft Foundry?

An autopilot is a type of agent that works under its own identity as a persistent, named member of your organization. It holds a standing role rather than answering one request at a time. It has its own security profile in your tenant and a manager who's responsible for it.

Every Foundry agent has a Microsoft Entra [agent identity](/entra/agent-id/what-are-agent-identities) from the moment you create it. What makes an autopilot different is that it also has an Entra [agent user account](/entra/agent-id/agent-users). That account gives the autopilot its own email, calendar, OneDrive, Teams presence, and a place in the organization chart, and it lets the autopilot perform Microsoft 365 actions as itself.

## Why autopilots exist

Without an agent user account, an agent can perform Microsoft 365 actions, such as sending an email or editing a document, only on behalf of a signed-in user. That works well for a one-to-one assistant, but it breaks down in two common situations.

- **No user in the loop.** An agent triggered by an event has no signed-in user to act for, so it can't take Microsoft 365 actions at all.
- **Group settings.** In a group chat, the agent has to guess on whose behalf to act, and there's no right answer. Whoever it picks, that person's permissions apply to the whole thread. Actions get attributed to someone who didn't ask, and members can be exposed to content they can't access.

An agent user account resolves both problems. The autopilot performs Microsoft 365 actions as itself, so it can work with a whole team at once and respond to a trigger when no user is present.

## What doesn't define an autopilot

Autopilots are often described by a set of capabilities: memory, proactivity, reasoning, planning, and learning. Those capabilities describe what an autopilot can do. They don't establish who is acting, and they change with every release. If capabilities defined the category, an agent that adds memory in a later release would become an autopilot without anything changing about who it is, what it can do, or who answers for it. That's a feature list, not a definition.

Autonomy doesn't define an autopilot either, and the two are independent. A background service agent can run on its own all day and isn't an autopilot. An autopilot doesn't have to be fully autonomous: your organization controls when it responds, who it can interact with, what it can access, and which actions it can take.

Capabilities describe an autopilot. Identity establishes it.

## What autopilots enable

You rarely do enterprise work alone. Most enterprise work is collaborative and continuous, spread across teams, meetings, documents, and group chats. Autopilots are built for that kind of work. They work with a whole team rather than one user at a time, and they can act without being prompted.

An autopilot holds a role and the jobs that come with it, and its context spans every interaction regardless of surface or user. Assign it work in Outlook and ask for the result in Teams. Because its role is standing and its permissions are its own, it can work proactively when you want it to, while staying inside a scope you define.

Accountability comes with the autonomy. Every autopilot has a manager who answers for it, and it's subject to the security, privacy, and governance controls you already run.

## How autopilots compare to other Foundry agents

Autopilots and other Foundry agents differ in the identity they hold, how you build them, and how they reach the people who use them.

### The identity model

A regular Foundry agent has a one-to-one shape: one agent, one blueprint, one agent identity, and no agent user account. The blueprint consists of an agent blueprint application and an agent blueprint service principal, which provides the security context and credentials.

:::image type="content" source="../media/autopilot/foundry-agent-identity-model.png" alt-text="Diagram that shows a Foundry custom blueprint creating exactly one agent identity, with no agent user account." lightbox="../media/autopilot/foundry-agent-identity-model.png":::

An autopilot has a one-to-many shape: one blueprint, and many hired instances, where each instance gets its own agent identity *and* its own agent user account.

:::image type="content" source="../media/autopilot/foundry-autopilot-identity-model.png" alt-text="Diagram that shows one Foundry blueprint hired into two team instances, each with its own agent identity and agent user account." lightbox="../media/autopilot/foundry-autopilot-identity-model.png":::

The two identity objects do different jobs and are never interchangeable.

| Object | What it is | What it holds |
| --- | --- | --- |
| **Agent identity** | A service principal | The agent ID, agent name, sponsor, and the permissions the agent authenticates with. For an autopilot, this identity secures the infrastructure that runs the agent. |
| **Agent user account** | A user object | The display name, manager, and user principal name that give the autopilot a presence in Microsoft 365. |

The distinction between an agent and an autopilot is binary. An agent either has its own agent user account or it doesn't, which is what makes identity a reliable definition.

Creating either type of agent starts the same way: Foundry creates an agent identity blueprint and an agent identity. For a regular agent, the agent identity represents the agent at runtime. For an autopilot, the agent identity serves as its infrastructure identity, while the agent user account represents the autopilot when it performs Microsoft 365 actions.

### Types of agents you can build in Foundry

Foundry supports three agent types, and only one of them is an autopilot.

| Type | Identity | What it can do | Best for |
| --- | --- | --- | --- |
| **Assistive** | Agent identity with signed-in user context | Acts on behalf of a user. It can take actions only within that user's permissions. | Personal productivity, such as a meeting-prep agent that drafts a deck on request. |
| **Background service** | Agent identity | Acts as itself through app-only permissions, without a signed-in user or agent user account. It can act autonomously but can't perform Microsoft 365 actions. | App automation and backend workflows, such as an operations agent that restarts a virtual machine in response to an alert. |
| **Autopilot** | Agent identity and agent user account | Acts as itself in Microsoft 365, including in group settings. It can act autonomously within the scope you define. | Digital coworkers, such as a release manager that coordinates work in a Teams group chat. |

### Why you build a blueprint, not an autopilot

You don't build an autopilot. You build a blueprint that teams use to create their own autopilot instances, each with its own identity and its own team-scoped access.

Building the agent directly ties it to one team, because the access that makes it useful is the same access that locks it down. If you add an agent user account to your team's security group and grant it your project and SharePoint site, that access is the point of the agent. It's also why nobody else can reuse it: they'd inherit access they shouldn't have, so they build their own. Ten teams later, the organization has ten near-identical agents, each governed separately. Their controls drift apart, and a compromised tool has to be chased down one agent at a time.

:::image type="content" source="../media/autopilot/blueprint-sharing.png" alt-text="Diagram that compares rebuilding an agent for every team with one blueprint producing per-team instances that share logic but hold separate access." lightbox="../media/autopilot/blueprint-sharing.png":::

A blueprint solves that problem. It defines two things: what the agent knows how to do, such as which APIs it can call, and the platform infrastructure the agent needs, such as storage for tracked items and memory. What it never grants is access to a specific team's business resources. An agent ships knowing how to update Azure DevOps work items and read SharePoint, while each manager decides which Azure DevOps project and SharePoint site their instance can access. Every instance created from the blueprint has its own identity, permissions, and assignment.

That separation holds at runtime too. Holding a tool isn't the same as holding access to the data behind it. Giving an autopilot a SharePoint tool doesn't give it any SharePoint site, and giving it a mailbox doesn't give it the ability to send mail.

Policy is a separate governance layer. Configure policy once and every instance inherits it. Update the blueprint and every instance updates. Block the blueprint and every instance stops.

Only Foundry hosted agents can be published as autopilot blueprints.

### Types of autopilots you can build

Autopilots fall into three patterns, which differ in who they serve.

- **Group autopilot** — works for a team. It lives where the team works, holds context the whole team shares, and coordinates across people instead of serving one at a time.
- **Company-wide autopilot** — provides a centrally managed capability available to everyone in the organization, typically as one production instance per business process.
- **Personal autopilot** — works for one person, as an isolated instance created and used by that person.

## Related content

- [Autopilot lifecycle in Microsoft Foundry](autopilot-lifecycle.md) covers the stages from building a blueprint to ending an instance.
- [Agent identity concepts in Microsoft Foundry](agent-identity.md) covers how Foundry provisions and uses agent identities at runtime.
- [Microsoft Agent 365 integration with Foundry](agent-365-integration.md) covers registry sync and which agent types support autopilot publishing.
