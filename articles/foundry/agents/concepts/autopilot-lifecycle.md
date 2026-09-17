---
title: "Autopilot lifecycle in Microsoft Foundry"
description: "Learn the stages of the autopilot lifecycle in Microsoft Foundry, from provisioning and publishing a blueprint to hiring, operating, and offboarding an instance."
author: fosteramanda
ms.author: fosteramanda
ms.reviewer: aahi
ms.date: 08/25/2026
ms.topic: concept-article
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to understand the whole autopilot lifecycle and who owns each decision so that I know what I control and what passes to someone else.
---

# Autopilot lifecycle in Microsoft Foundry

An autopilot moves through a defined lifecycle. An Azure administrator provisions the platform, a developer builds and publishes a blueprint, a tenant administrator approves it, and a manager hires and runs each instance. This article describes each stage, the role that owns it, and the points where responsibility passes from one role to the next.

Because you build a blueprint rather than an autopilot, the lifecycle runs at three layers: the blueprint you publish once, the instances that teams hire from it, and the fleet of instances your tenant governs as a whole. For the model behind that, see [What is an autopilot in Microsoft Foundry?](autopilot-overview.md)

## Lifecycle stages at a glance

| Stage | Layer | Owner | What it produces | Reversible |
| --- | --- | --- | --- | --- |
| Provision infrastructure | Blueprint | Azure administrator | A development environment and the agent's platform resources | Yes |
| Build and publish | Blueprint | Developer | A published blueprint with declared scopes and ceilings | Yes |
| Approve, configure, and consent | Blueprint | Tenant administrator | An activated blueprint that selected people can hire | Yes |
| Hire | Instance | Manager | An agent identity and an agent user account | Yes, by offboarding |
| Onboard | Instance | Manager or access manager | The instance's audience and its access to team resources | Yes |
| Operate | Instance | Manager, teammates, and business leads | Day-to-day work, observation, and coaching | Yes |
| Offboard | Instance | Manager | A removed instance | No |
| Retire or delete | Blueprint | Tenant administrator or developer | A blueprint that accepts no new hires, or no blueprint at all | Retire: yes. Delete: no |

## Who does what

Four roles own the four decisions that shape an autopilot. Other roles are optional and appear only in certain deployment patterns.

| Role | Layer | The decision they own | Their responsibilities |
| --- | --- | --- | --- |
| **Azure administrator** | Platform | What the platform runs on, and who can build on it | Provisions Foundry infrastructure and the agent's platform resources, assigns developer permissions, and assigns permissions to the default instance identity. |
| **Developer** | Blueprint | The role and capabilities of the blueprint, and the conditions it was built and tested for | Defines what the agent does and how it behaves, sets blueprint and instance authorization, declares permission scopes, and publishes, tests, and updates the blueprint. |
| **Tenant administrator** | Fleet | Whether the autopilot can operate in your tenant, and under what policy | Manages licensing, approves and activates the blueprint, grants admin consent, selects who can hire, observes the fleet, and blocks the blueprint. |
| **Manager** | Instance | The employment of the instance, from hire to offboard | Hires the instance, configures who can use it, grants team resources, requests workstream status, customizes and monitors the instance, and offboards it. |

Two more roles appear when those four can't cover the ground alone:

- An **executive business sponsor** joins when an executive wants the autopilot across an organization and funds it.
- An **access manager** joins when the person hiring the instance can't grant what the autopilot needs, or shouldn't be the one judging least privilege.

| Role | Layer | The decision they own | Their responsibilities |
| --- | --- | --- | --- |
| **Executive business sponsor** | Blueprint | Whether the blueprint's design is worth running at all | Sets blueprint-wide controls. Has no authority over any single instance. |
| **Access manager** | Instance | What to give the instance, which is half of the manager's decision | Hires and onboards the instance, authorizes its access, then transfers the manager role. |

These decisions don't overlap, and nothing important falls between them: what the platform runs on, the blueprint's role and capabilities, whether and how the autopilot operates in your tenant, and the employment of each instance. Every other question resolves to one of them.

The developer's decision covers more than it first appears to. It isn't only what the autopilot *can* do. It also includes the conditions the autopilot was built and tested for, which form the operating envelope that every other role trusts when they approve and hire it. When an autopilot fails outside that envelope, fault depends on whether the envelope was ever stated.

### Accountability compared with governance

Governance determines who *can* stop an instance, and by design almost everyone can. Accountability determines who is *obliged* to stop it. That's always the manager, regardless of who is at fault, because a broken autopilot shouldn't keep running while its manager waits for someone else to act.

An access failure shows the difference most clearly. An access manager configures a grant that the manager never made, and the instance misbehaves because of it. The manager is still the one obliged to stop it. Fault and obligation stay separate by design.

### Other participants

Two groups own no decision but still matter.

**Teammates** use the autopilot where the team already works: in Teams, email, and document comments. They assign it standing work and give objective corrections that update its grounding.

**Business leads** are other leads on the same work. They configure nothing and answer for nothing, but they can observe the instance and block it. They can't delete or transfer it. That design is intentional: anyone close enough to the work to see the autopilot misbehave should be able to stop it. The manager is the only role that both governs the autopilot and uses it daily, which is why the obligation to stop it falls to them.

Anyone in the tenant outside the configured audience is a **non-teammate**. Non-teammates are blocked by default, before the autopilot ever calls a model.

### How deployment patterns change the roles

The [autopilot pattern](autopilot-overview.md#types-of-autopilots-you-can-build) you choose determines which roles appear.

- **Group autopilot** — involves every role. This pattern is where the access manager split matters most, because the person who can grant an Azure DevOps project is rarely the team lead who works with the instance.
- **Company-wide autopilot** — has one instance and one manager answering for the whole organization, so "teammate" stops being a useful distinction.
- **Personal autopilot** — involves only the developer, who is usually the manager and the only user.

## How the layers fit together

:::image type="content" source="../media/autopilot/autopilot-lifecycle.png" alt-text="Diagram that shows the autopilot lifecycle at three layers: a fleet row, a blueprint row, and a repeating instance row." lightbox="../media/autopilot/autopilot-lifecycle.png":::

The lifecycle runs at three layers at once.

- **Blueprint** — runs once, from provisioning through approval. After approval, the developer's work continues as a standing activity that spans the working life of every instance and ends only when the blueprint is deleted. Optimization feeds new versions back into the build stage.
- **Instance** — runs once per hire. Many instances are alive at the same time, so one team can offboard an instance while another team hires one from the same blueprint.
- **Fleet** — isn't a stage. It's the tenant administrator's standing activity, and it begins at approval, because that's when the fleet starts to exist.

Approval is the point where one approved design becomes many instances. Deleting the blueprint cascades to every instance created from it.

The standing activities are described after the instance stages, because that's the point at which they have something to span.

A single example runs through every stage: a workstream manager, built by a platform team and hired by many teams. Example paragraphs are labeled **Example** and are optional.

## The blueprint layer

The blueprint stages run once. Every instance created from the blueprint inherits their results.

### Provision infrastructure — Azure administrator and developer

The Azure administrator sets up the environment and gives developers the minimum permissions they need to build, test, and deploy in it. This setup applies per environment, not per autopilot. It happens once, and every blueprint built there inherits it.

The Azure administrator also provisions what this specific autopilot needs to run, such as storage for tracked items and memory, and grants the autopilot's built-in identity access to those resources. This infrastructure belongs to the blueprint, not to any team's data. Provisioning resources and assigning permissions are the two things developers can't do for themselves. The Azure administrator is the only role that finishes before the autopilot reaches a user: their work is done when development can begin.

**Example**: At Contoso, the Azure administrator sets up a Foundry account and project and deploys the models. They create an Azure Container Registry, a Log Analytics workspace, and Application Insights, with project connections for the registry and Application Insights. The project managed identity is granted AcrPull and Log Analytics Reader. They also create a storage account with two tables, one for the direct-message allow list and one for tracked work items. After the agent is created, its identity is granted Storage Table Data Contributor. Every developer gets Foundry User scoped to the project, AcrPush scoped to the registry, and Monitoring Reader.

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

### Build and publish — developer

The developer defines the role and capabilities of the blueprint: what it does, how it behaves — when it replies, when it stays silent, when it asks for approval — and what it must never do. The platform provides foundational capabilities such as memory, routines, and self-improvement, so the developer enables and configures them rather than building them. A development instance lets the developer iterate without re-entering tenant approval for every change.

Publishing also records the declared permission scopes and two ceilings: who can hire the autopilot, and the widest access any manager can later grant. Together with the conditions the autopilot was built and tested for, these values form the operating envelope that every downstream role trusts.

Nothing in this stage grants access to anything. These values are declarations only. Publishing puts the blueprint in front of governance; it doesn't put the blueprint to work.

**Example**: At Contoso, the workstream manager gets Azure DevOps tools with identity passthrough, the built-in Microsoft 365 tools, and a custom work-item tracker. Its response logic decides when it speaks in a channel and when it stays silent. The autopilot declines group chats that include unapproved participants, and returns a fixed no-op response to cross-tenant messages. Before publishing, the developer declares the scopes that need consent and sets both ceilings.

### Approve, configure, and consent — tenant administrator

This stage is one gate with three actions. The tenant administrator reviews the published blueprint, grants consent to its declared scopes, approves it, and selects who can hire it. Consent and hirer selection are separate decisions with separate consequences: an administrator can approve a blueprint while consenting to only part of what it requested.

This stage is where the fleet-level decision is made: whether the autopilot can operate in your tenant, and under what policy. Consent governs the token, which determines what kinds of calls the autopilot is ever allowed to make. It grants no team's data to anyone.

Every new blueprint and every widened scope re-enters this gate, so include administrator review time in your rollout plans.

**Example**: At Contoso, the administrator opens the pending workstream manager request in the Microsoft 365 admin center, consents to the scope set, publishes it, and names the organization's team leads as eligible hirers.

### Approval enables hiring

Approval is the exit condition for the entire blueprint layer: at least one manager can now hire an instance. It's the only point where the blueprint layer and the instance layer meet. Everything up to this point declares and consents to capability. Nothing has been granted yet. An autopilot can hold every scope it needs and still reach no data at all.

## The instance layer

The instance stages run once per hire. Many instances run at the same time, each at its own stage.

### Hire — manager

Hiring is a single action rather than a phase. It creates two objects:

- An **agent identity**, a service principal that authenticates and holds permissions.
- An **agent user account**, which holds a mailbox, Teams presence, a place in the organization chart, and a manager.

The person who hires the autopilot becomes its manager.

**Example**: At Contoso, three team leads hire three workstream managers from the same blueprint. One design is now a fleet, and everything from this point on happens three times, independently.

### Onboard — manager

Onboarding is where employment really begins. The manager configures five settings.

| Setting | What it controls |
| --- | --- |
| **Audience** | Who can use the instance |
| **Listening scope** | Which conversations and surfaces the instance receives |
| **Messaging scope** | Who the instance can message |
| **Access** | Which business resources the instance can reach |
| **Source of truth** | Which content grounds the instance's answers |

The access grants — security-group membership, an Azure DevOps project, a SharePoint site — are the first grant of business resources anywhere in the lifecycle. They turn a capable blueprint into a working teammate.

Every audience starts as the manager alone and extends up to the developer's ceiling, and no further. Anyone in the tenant outside the configured audience is blocked by default, and the autopilot never calls a model on their behalf.

**Consent and access are different gates.** Scopes and consent govern the token, which determines what kinds of calls are allowed. Group memberships and roles govern the account, which determines what data those calls reach. Microsoft Entra ID enforces the first gate. Each resource enforces the second gate against its own membership lists and never checks consent. For a person, IT closes both gates long before their first day. For an autopilot, both gates are new at hire, so onboarding includes work that feels like it should already be done.

Authorization starts here but never finishes. Teams change, resources change, and grants get revoked. The autopilot eventually needs a SharePoint site that nobody anticipated at hire.

**When the person hiring can't make these grants, the stage splits.** Managers are knowledge workers who often don't hold the rights to add an account to a security group or an Azure DevOps organization, and least privilege is a security judgment most team leads have never had to make. An access manager takes this stage instead: they hire, onboard, and authorize the instance, then transfer the manager role to the lead who works with it. The employment decision itself doesn't move.

**Example**: At Contoso, one lead sets their workstream as teammates and the engineering and product leads as business leads. They add the agent account to the team's security group and distribution list, which is what grants the Azure DevOps project and SharePoint site, and they give it write access to the GitHub organization. On another team, the lead can't grant the Azure DevOps project, so an access manager onboards the instance and hands over the manager role.

### Operate — manager, teammates, and business leads

Four activities run at the same time for as long as the instance lives, and each activity involves a different set of roles.

**Use — teammates and manager.** The autopilot performs its role across its configured surfaces, including Teams direct messages, group chats and channels, email, and document comments. Its context spans every interaction, regardless of surface or user. Teammates assign routines, which are standing instructions given in a single message.

**Observe — manager and business leads.** They review what the instance did, for whom, at what cost, and whether anything needs investigating. Day-to-day accountability happens here.

**Govern — manager and business leads.** These controls are all reversible: tighten access, revoke access, or block the instance. Governing follows from observing, because you block in response to something you saw. Blocking is intentionally asymmetric. Anyone close enough to the work to see a problem can stop the instance, but only a tenant administrator can start it again.

**Coach and customize — manager.** Improvement arrives through two unequal channels. Objective corrections, such as a slipped date or a wrong owner, can come from anyone who works with the instance, and they update its grounding. Coaching and customization — style, memory edits, and shaping routines — belong to the manager alone, which settles conflicts automatically: what the manager sets stands. Coaching changes one team's autopilot. When the developer optimizes the blueprint, it changes what every instance *is*.

**Example**: At Contoso, teammates each set standing work in a single message: a Friday internal recap, an external weekly draft that stays unsent until a lead approves it, and an end-of-day digest that mentions every owner with an open item. The manager reviews the instance's recent activity. When the instance keeps burying the main point in its recaps, the lead coaches it once and the new style holds.

### Offboard the instance — manager

Offboarding is the one irreversible instance action. The agent user account is removed, its memberships are revoked, and its access ends immediately. Only one team is affected, and no other instance is touched. Nothing can be restored.

The decision belongs to the manager, and it's the one judgment nobody else can make: whether the instance still delivers enough value to justify running it. Administrators can act on fleet-wide signals, but they can't see whether a single instance still earns its cost. Offboarding isn't a stronger version of the controls in the operate stage. Every control there can be undone, and offboarding can't, which is why it's a separate stage.

**Example**: At Contoso, one workstream finishes and its lead offboards their instance. Its memberships are revoked. The other two workstream managers are unaffected.

## Standing blueprint and fleet activities

Two activities run for the entire working life of every instance: the developer's operation of the blueprint, and the tenant administrator's management of the fleet.

### Operate the blueprint — developer

The developer governs, observes, evaluates, and optimizes the blueprint. They observe production deployments without receiving private conversation content by default. They filter telemetry by version and by instance to watch rollouts, and they run evaluations against the operating envelope the autopilot was built and tested for. Fixes ship as new versions that flow to every instance.

A new version that widens its scopes doesn't bypass governance. Added permissions re-enter the consent gate. The gate applies to the ceiling rather than to the change itself, which is why the tenant administrator's decision is standing rather than one-time.

The developer also holds blueprint-level governance. They can block the blueprint they shipped, and like everyone else, they can't unblock it. Don't confuse this activity with the coaching a manager does. The developer changes what every instance *is*. A manager changes how one instance *behaves*.

### Manage the fleet — tenant administrator

The tenant administrator observes, governs, and secures the fleet from the moment a blueprint enters approval. A single registry lists every hire with its team, blueprint, and version, along with every action attributed to its identity. The administrator holds the widest control in the system: blocking the blueprint stops every instance at once, because every instance token chains back to the blueprint's credential.

That control reflects how blueprints fail. A blueprint defect is always systemic. If a workstream manager sends email outside the tenant, that isn't one team's instance misbehaving. Every instance carries the same flaw and waits for the same conditions. The block applies to the blueprint, not to the instance that someone happened to notice.

### Retire and delete the blueprint — tenant administrator and developer

A blueprint has two exits.

- **Retire** — a tenant administrator stops new hires, and the blueprint ends when no active instances remain. Retiring prevents future hires without affecting current instances.
- **Delete** — every instance created from the blueprint is removed with it. Delete is the blueprint-layer equivalent of a manager offboarding a single instance.

That difference is the line that organizes the whole lifecycle. Every control in the operate stages and the standing activities can be undone. Deleting a blueprint can't.

## Related content

- [What is an autopilot in Microsoft Foundry?](autopilot-overview.md) explains the identity model and why autopilots use blueprints.
- [Quickstart: Build your first autopilot](../how-to/agent-365.md) covers provisioning, building, publishing, approval, and hiring your first instance.
- [Microsoft Agent 365 integration with Foundry](agent-365-integration.md) covers registry sync, data collection, and data residency.
