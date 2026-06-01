---
title: Include file
description: Include file
ai-usage: ai-assisted
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/06/2026
ms.custom: include
---

A structured deployment plan helps you avoid security gaps, cost overruns, and
access sprawl when you adopt Microsoft Foundry at scale. Use this guide to
define workload boundaries, choose a resource topology, and establish
governance for self-serve teams.

## Prerequisites

Before you begin planning, confirm that you have:

- An understanding of your organization's baseline Azure subscription and
  resource group organization.
- Inputs on your organization's security requirements for networking,
  encryption, and data isolation.
- An initial region plan based on model and feature availability. For details, see [feature availability across cloud regions](../reference/region-support.md).
- Agreement on security requirements for networking, encryption, and data isolation in your organization.
- An inventory of the Foundry features and APIs your teams plan to use.

## Define isolation boundaries

Start with Cloud Adoption Framework decision guidance for AI platform sharing,
then apply those decisions to Foundry:

- [Define AI platform sharing boundaries](/azure/cloud-adoption-framework/ai/platform/ai-platform-sharing-isolation-colocation#1-define-ai-platform-sharing-boundaries)

While every situation is unique, for the common organization we recommend the following sequence:
1. Define nonnegotiable sharing boundaries across business units, data domains,
   product ownership, and environment tiers.
1. Set a production policy that defaults to isolation, unless a documented
   exception allows colocation.
1. Set a preproduction policy that defaults to colocation for faster
   experimentation, unless compliance or validation requires isolation.
1. Assign ownership for each boundary, including security, cost, and incident
   response ownership.

## Identify capability and access requirements

Determine which Foundry features and APIs each workload requires before you
finalize your topology.

> [!NOTE]
> Not all Foundry APIs support the full variety of authentication modes, storage encryption levels and project-level isolation. Some of the Foundry Tools APIs can require
> role assignments at the parent Foundry resource scope.

For co-located use cases that share one Foundry resource, use Foundry projects as isolated workspaces for each use case. For example, teams experimenting with an
idea can create a project to organize coherent assets without repeating infrastructure
setup for security, model deployments and tool access.

Most newer, agent-centric Foundry APIs support project-scope permissioning. Some traditional Foundry Tools APIs (former Azure AI Services), such as speech-to-text, still require parent resource-scope access. Plan boundaries and RBAC so all required capabilities are accessible at your intended access-management scope.

| Capability area | Organize by project | Project-level RBAC isolation | Bring your own storage | Networking / encryption support | Planning implication |
|---|---|---|---|---|---|
| Agent capabilities (agents, responses, evaluations, datasets, indexes, files, and playground assets) | Yes | Yes | Yes | Limited in basic set up (managed storage). For full coverage, use 'standard'. | Good fit for project-per-use-case segmentation in shared environments. |
| Fine-tune training | No (default project only) | No | Partial (inputs only) | Yes |  If each team needs independent fine-tuning, use separate Foundry resources. Fine-tuned deployments are shared and consumeable across projects within a resource.
| OpenAI image, video, batch | No | No | Partial (only Batch) | Yes | Use an isolated workload setup, and if managed storage is required, validate RBAC constraints early.
| Content Understanding | Yes | No | Yes | Yes | If strict per-use-case access isolation is required, prefer separate Foundry resources. |
| Speech | Yes (fine-tune) | No | Yes | Limited in basic setup (managed storage).|  For full CMK encryption coverage, use BYO Storage. |
| Language | Yes (fine-tune) | No | Yes | Limited in basic setup (managed storage).|  For full CMK encryption coverage, use BYO Storage. |
| Translator | No | No | No | Yes | Use seperate Foundry resource if isolation is a must. |

> [!IMPORTANT]
> Confirm your exact capability mix before rollout. If a required API only works
> at Foundry resource scope, assign roles at that scope or isolate workloads into
> separate Foundry resources.

## Choose Foundry resource topology

After you define boundaries and capability needs, choose topology per
environment.

| Decision path | Recommended Foundry setup | Best fit | Main tradeoff |
|---|---|---|---|
| Co-located workloads | One Foundry resource with multiple projects (typically one project per use case) | Experimentation-heavy environments, early prototypes, and teams that benefit from shared deployments and shared connected data or tools | Shared blast radius for production incidents, quota exhaustion, and misconfiguration |
| Fully isolated workloads | One Foundry resource per production workload boundary (often with one primary project per workload) | Production workloads that require strict operational containment, independent access control, and independent quota or cost boundaries | Self-serve enablement harder with more resources to manage and higher setup overhead |

> [!TIP]
> For production, treat isolation as the default. Use colocation as a deliberate
> exception only when workload boundaries, data requirements, and risk acceptance
> are aligned.

:::image type="content" source="../media/planning/foundry-resource.png" alt-text="Screenshot of a diagram showing Foundry resource.":::

## Plan your security baseline

Use this reference table as a checklist for security design decisions.

| Area | What to decide | Start with |
|---|---|---|
| Identity and access | Define admin, project manager, and project user personas. Map each persona to least-privilege roles and Entra ID groups. | [Role-based access control in Foundry](../concepts/rbac-foundry.md) |
| Networking | Choose the network model per environment. Use managed virtual network for a more secure, straightforward setup. Use bring-your-own virtual network (BYO VNET) for advanced network control and custom routing requirements. Validate private DNS and endpoint approval flow before production. | [Configure managed virtual network](../how-to/managed-virtual-network.md), [Configure private link for Foundry](../how-to/configure-private-link.md), and [Network-secured setup (BYO virtual network)](../agents/how-to/virtual-networks.md) |
| Data protection and keys | Decide whether Microsoft-managed keys meet policy requirements or whether customer-managed keys are required. | [Customer-managed keys in Foundry](../concepts/encryption-keys-portal.md) |
| Authentication model | Prefer Entra ID and RBAC for people and services. Use API keys only where role granularity isn't required. | [Role-based access control in Foundry](../concepts/rbac-foundry.md) |

## Plan model, region, and capacity strategy

For each workload, define:

1. Model families and deployment types required by the use case.
1. Data processing requirements (for example, global or regional constraints).
1. Throughput and latency targets for interactive and batch scenarios.
1. Quota and provisioned capacity requirements for steady-state and peak loads.

Use these references:

- [Models sold directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Models from partners](../foundry-models/concepts/models-from-partners.md)
- [Quota in Foundry](../how-to/quota.md)
- [Quotas and limits for Foundry models](../foundry-models/quotas-limits.md)

## Plan connectivity and data integration

For each workload, identify external dependencies and connection patterns:

- Data sources and data stores.
- Internal APIs and line-of-business systems.
- Non-Azure SaaS tools required by agents or orchestration flows.
- Networking requirements, including private endpoints, DNS resolution,
  egress controls, and whether managed network or BYO VNET is required.

Use [Add connections in Foundry](../how-to/connections-add.md) to standardize
connection setup.

Connections can be created at both the parent Foundry resource-level and child project-level dependent on desired isolation scope. Connections configured at the parent level are availabile to all projects. 

:::image type="content" source="../media/planning/connectivity.png" alt-text="Screenshot of a diagram showing Foundry project connectivity and integration with other Azure services.":::

## Plan automation and operations

Define how teams create and manage resources consistently across environments.

- Use infrastructure as code to provision core resources and policy defaults.
- Standardize deployment pipelines for projects, connections, model deployments, and
  configuration changes.
- Define rollback and incident response procedures for model and policy changes.

For automation patterns and starter implementations, use:

- [Quickstart: Deploy a Microsoft Foundry resource by using a Bicep file](../how-to/create-resource-template.md)
- [Terraform on Azure](/azure/developer/terraform/overview)
- [Security configurations samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples)

The sample templates include end-to-end patterns for common security scenarios,
such as private networking, customer-managed keys, and role-based access
control.

## Define self-serve guardrails

Enable self-serve only within clear constraints:

1. Define which roles can create projects, deploy models, and connect external
   tools. 
1. Apply policy controls for model deployment and runtime behavior including which model providers, and which tool connections are allowed.
1. Set cost controls and budget alerts for shared and isolated environments.
1. Enforce trace logging into central observability across Microsoft Foundry, Microsoft Copilot Studio and Microsoft365.

Use these references:

- [Model deployment policy in Foundry](../how-to/model-deployment-policy.md)
- [Manage costs in Foundry](../concepts/manage-costs.md)
- [Agent 365 integration](../agents/concepts/agent-365-integration.md)

## Assign ownership and governance

Treat this step as the transition from provisioned infrastructure to operational
developer usage.

Most organizations already manage access through precreated Microsoft Entra ID
groups. Map those groups to Foundry roles at the required scope, then validate
both management and development access paths.

Foundry separates access across:

- **Control plane RBAC actions** for resource management.
- **Data plane RBAC actions** for development workloads.

> [!IMPORTANT]
> Management roles such as Owner or Contributor are not sufficient for all
development scenarios. For example, a user can manage resources but still need
data plane roles to chat with an agent in Foundry.

For role mapping guidance and required role combinations, see
[Role-based access control in Foundry](../concepts/rbac-foundry.md).

After onboarding your user groups, consider establishing or expanding governance dashboards to track Foundry usage, reliability, lineage, and compliance:
 
- [Monitoring across fleets in Foundry](../control-plane/monitoring-across-fleet.md)
- [Agent 365 integration](../agents/concepts/agent-365-integration.md)
- [Microsoft Defender for Cloud](/azure/defender-for-cloud/defender-for-cloud-introduction)
- [Azure Policy](/azure/governance/policy/overview)

## Sample platform deployment

The IT organization at Contoso needs to support multiple teams while balancing two priorities:
1. Rapid innovation, where developers can rigorously test the latest AI technologies using non-production data.
1. Fully isolated dev, test, and production environments for proven use cases that receive funding for operationalization.

The diagram below shows how Contoso co-locates a shared pre-production Foundry instance for innovation, available to all teams, with limited capacity and pre-connected data and tools. Historically, only a handful of use cases progress to proven feasibility or secure funding for a dev/test rollout. From those, an even smaller subset advances to production. As use cases mature, teams are assigned environments with progressively stronger isolation, culminating in full production-grade separation.

:::image type="content" source="../media/planning/sample-platform-deployment.svg" alt-text="Diagram showing Contoso use cases moving from a shared pre-production Foundry environment into isolated dev-test environments, and then into isolated production environments for a smaller number of workloads.":::