---
title: New Microsoft Foundry portal general availability overview
titleSuffix: Microsoft Foundry
description: Learn what general availability means for Microsoft Foundry, including GA scope, supported scenarios, feature readiness, and migration guidance.
author: sdgilley
ms.author: sgilley
ms.reviewer: shwinne
ms.date: 03/03/2026
ms.service: azure-ai-foundry
ms.topic: concept-article
ai-usage: ai-assisted
---

# New Microsoft Foundry portal general availability overview

The new Microsoft Foundry portal is now generally available (GA). This milestone marks a shift from pilot-focused usage to secure, reliable, enterprise-ready production usage for core scenarios.

Foundry is designed for teams that need to build, deploy, and operate AI systems at scale, with governance, security, and operational controls integrated throughout the lifecycle. Foundry unifies the end-to-end lifecycle across **Discover**, **Build**, and **Operate** so teams can move faster without trading off reliability, compliance, or operational rigor.

## Prerequisites

Before you standardize on GA features for production, make sure you:

- Understand your required scenarios across model deployment, agent development, and operations.
- Identify any current dependencies on preview-only or classic-only experiences.
- Define your organization policy for using only GA capabilities in production.
- Review migration guidance for existing Azure OpenAI and Foundry Classic workloads.
- Confirm required role assignments for your teams and service identities. For role details, see [Role-based access control for Microsoft Foundry](rbac-foundry.md).
- Define how your organization restricts preview feature access in production environments. For guidance, see [Disable preview features in Microsoft Foundry](../how-to/disable-preview-features.md).

## Key terms used in this article

- **GA**: Generally available features supported for production use.
- **Preview**: Features that are not yet generally available.
- **Foundry projects**: Workspace containers that organize your AI assets, deployments, and agent configurations within the new Foundry experience.
- **AOAI**: Azure OpenAI resources and workflows.

## What GA means for customers

At GA, the new Microsoft Foundry portal provides:

- **Production-ready core platform** with validated end-to-end core scenarios.
- **Enterprise capabilities** such as RBAC, audit logs, compliance controls, monitoring, alerting, virtual network integration. Also API keys are supported for all areas except for evals, dataset tab, content understanding, agents and workflows.
- **Governed lifecycle consistency** across the portal, APIs, SDKs, CLI, and developer tools.
- **Defined GA scope** for Foundry projects, with out-of-scope capabilities continuing in Foundry Classic experiences.

For governance-sensitive production workloads, use Microsoft Entra ID with RBAC for role-based access control. API key-based access is available, but it doesn't provide the same role-based permission granularity. For billing and cost management details, see [Plan and manage costs for Microsoft Foundry](planning.md).

## GA scope by project type

At GA, the new Foundry experience supports Foundry projects for core end-to-end scenarios. Confirm that your target regions support the models and features you need. For region details, see [Feature availability across cloud regions](../reference/region-support.md).

For scenarios not yet available in the new Foundry experience, you can continue to use Foundry Classic experiences to maintain continuity while capabilities continue to evolve.

## Core scenarios at GA

Core GA coverage includes:

- **Model core flows**: Discover models, deploy models, run inference, manage deployments, and transition to agent-based workflows.
- **Agent development**: Build agents and integrate evaluations, tracing, monitoring, red teaming, and fine-tuning where supported.
- **Operate experiences**: Manage agents and assets, enforce policies, and manage quota and administration features where supported.

## Feature readiness at GA

> [!IMPORTANT]
> The status values in this section include roadmap-sensitive items.
> Confirm current status before making production commitments.

The following table summarizes feature readiness. Most core capabilities across Home, Discover, Build, and Operate are GA, while some capabilities remain in Preview.

| Area | Feature | Status |
| --- | --- | --- |
| Home | All | GA |
| Discover | Overview | GA |
| Discover | Model | GA |
| Discover | Tools | GA |
| Discover | Solution Templates | GA |
| Discover | Agent Manifests | Preview |
| Discover | Search | GA |
| Discover | Ask AI | Preview |
| Build | Agents | GA (minus Voice Live, traces in agent builder in Preview) |
| Build | Workflows | Preview |
| Build | Models | GA |
| Build | Tracing and tracing VNet | GA |
| Build | Optimization (cluster analysis) | Preview |
| Build | Fine-tuning | GA |
| Build | Tools | GA (check label on individual tools in the catalog to determine if they are GA or Preview)|
| Build | Knowledge | Preview |
| Build | Data | GA (minus stored completions in Preview) |
| Build | Evaluations | GA |
| Build | Memory | Preview |
| Build | Guardrails | Agents = Preview; Models = GA; Controls and intervention = Preview |
| Build | Monitoring | GA |
| Build | Red teaming | GA |
| Build | AI services speech playgrounds | GA |
| Operate | Overview | Preview |
| Operate | Assets | Preview |
| Operate | Compliance | Preview |
| Operate | Quota | GA |
| Operate | Admin | GA (minus AI Gateway in Preview) |
| Docs | All | GA |

## Unsupported at GA

The following items are out of scope at GA for the new Foundry portal and require the classic portal:

- Standalone Azure OpenAI or other single-service resources that aren't connected to a Foundry project.
- Assistant creation and authoring in the new Foundry experience.
- Listing AOAI evaluation files as datasets for upgrade workflows.
- Audio playground.
- AI service fine-tuning.
- Content Understanding.
- Prebuilt prompts in video playground.
- Adding data directly from the Data tab (users can add data during agent creation workflows).
- Private/Government cloud support for the new Foundry experience.

## FAQ

### What does general availability mean for Microsoft Foundry?

GA means the new Foundry portal is supported for production use for defined core scenarios in Foundry projects, with validated end-to-end experiences, enterprise support readiness, and operational reliability.

### Which projects are supported at GA?

At GA, the new Foundry experience supports Foundry projects with end-to-end coverage for core scenarios. Other resource types can continue in the Foundry (classic) portal where needed.

### Are all Foundry features GA?

No. GA covers validated core experiences and required enterprise features. Some capabilities remain in public preview.

### How do I disable preview features?

[!INCLUDE [disable-preview](../includes/disable-preview.md)]

### What is the experience for existing Azure OpenAI users?

If you have existing Azure OpenAI resources, you can continue to use classic experiences for unsupported workflows while you plan your upgrade to Foundry projects.

For upgrade guidance, see [Upgrade Azure OpenAI to Microsoft Foundry](../how-to/upgrade-azure-openai.md).

For project migration guidance, see [Migrate from hub-based to Foundry projects](../../foundry-classic/how-to/migrate-project.md).

### Are assistants supported in Foundry projects?

Agents v2 are supported in the new Foundry UI. Existing assistants and v1 agents aren't supported in the new Foundry experience. To use or edit assistants, continue using Foundry Classic until assistant upgrade is available.

### Can customers use Foundry GA through APIs and developer tools?

Yes. Foundry provides support across portal, APIs, SDKs, and CLI for GA-supported scenarios.

To get started, see [Microsoft Foundry SDKs](../how-to/develop/sdk-overview.md) and [Microsoft Foundry API](/rest/api/aifoundry/).

### Is GA the final state of Microsoft Foundry?

No. GA is a production milestone, not an endpoint. Microsoft continues to expand workflow authoring, operations, and governance capabilities based on customer feedback and production usage.

## Validate GA-only usage

Before production rollout, validate the following:

- Required scenarios in your workload map to capabilities marked **GA** in this article.
- Dependencies on **Preview** features are documented and approved for nonproduction use only.
- Role assignments and authentication model are aligned to your governance policy, especially where API keys are used.
- Target-region model and feature availability are confirmed in [Feature availability across cloud regions](../reference/region-support.md).
- Teams supporting migration scenarios have a documented path between the new Foundry experience and Foundry Classic workflows.

## Common rollout pitfalls

- Treating Preview features as production dependencies without explicit approval. Check the [feature readiness table](#feature-readiness-at-ga) for current status.
- Assuming API key authentication provides the same governance granularity as Entra ID with RBAC. See [Role-based access control for Microsoft Foundry](rbac-foundry.md) for proper configuration.
- Skipping region availability validation for required models and services. See [Feature availability across cloud regions](../reference/region-support.md).
- Migrating assistants or AOAI workflows without a documented fallback path in Foundry Classic. See [Migrate to the new Foundry Agent Service](../agents/how-to/migrate.md).

## Next steps

- [What is Microsoft Foundry?](../what-is-foundry.md)
- [Microsoft Foundry rollout across my organization](planning.md)
- [Role-based access control for Microsoft Foundry](rbac-foundry.md)
- [How to configure a private link for Foundry](../how-to/configure-private-link.md)
- [Feature availability across cloud regions](../reference/region-support.md)
