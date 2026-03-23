---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: aashishb
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

This article shows you how to estimate expenses before deployment, track spending in real time, and set up alerts to avoid budget surprises.

## Prerequisites

Before you begin, ensure you have:

- **Azure subscription:** An active Azure subscription with the resources you want to monitor.
- **Role-based access control (RBAC):** One or both of the following roles at the subscription or resource group scope:
  - [**Cost Management Reader**](/azure/role-based-access-control/built-in-roles/management-and-governance#cost-management-reader) – View costs and usage data.
   - [**AI User**](../concepts/rbac-foundry.md#built-in-roles) – View Foundry resource data and usage context.
- **Supported Azure account type:** One of the [supported account types for Cost Management](/azure/cost-management-billing/costs/understand-cost-mgt-data).
- **Region and model availability check:** Confirm required model and feature availability in your target regions before deployment. For details, see [Feature availability across cloud regions](../reference/region-support.md).
- **Resource topology awareness:** Know whether your cost views are scoped to subscription, resource group, or resource, and keep the same scope when you compare estimate versus actual cost.
- **Reporting latency expectation:** Cost and usage records can appear with delay depending on service ingestion timing. Use trend windows instead of minute-by-minute comparisons for reconciliation.

If you need to grant these roles to team members, see [Assign access to Cost Management data](/azure/cost-management-billing/costs/assign-access-acm-data) and [Foundry RBAC roles](../concepts/rbac-foundry.md).

Use this task-to-role mapping as a starting point:

- **View Cost Management data:** [Cost Management Reader](/azure/role-based-access-control/built-in-roles/management-and-governance#cost-management-reader).
- **View Foundry resources and related usage context:** [AI User](../concepts/rbac-foundry.md#built-in-roles).
- **Create or modify custom roles:** **Owner** at the target scope.

> [!NOTE]
> Foundry doesn't have a dedicated page in the Azure pricing calculator because Foundry is composed of several optional Azure services. This article shows how to use the calculator to estimate costs for these services.

## Estimate costs before using Foundry

Use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate costs before you add Foundry resources.

1. Go to the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).
1. Search for and select a product, such as Azure Speech in Foundry or Azure Language in Foundry.
1. Select additional products to estimate costs for multiple services. For example, add Azure AI Search to include potential search costs.
1. As you add resources to your project, return to the calculator and update estimates.

## Validate your cost plan before rollout

Before rolling out to production, validate the following:

1. Required models and services are available in your target regions. See [Feature availability across cloud regions](../reference/region-support.md).
1. The same resource scopes used in your estimates (subscription, resource group, and resource) are used in Cost Management views.
1. Meter-level cost breakdowns map to expected services and deployments in your architecture.
1. Built-in roles or custom roles required for cost visibility are assigned to operations and finance users.

### Worked example: estimate and verify

Use this lightweight workflow to reduce billing surprises:

1. Build an estimate in the Azure pricing calculator for the services in your architecture.
1. Deploy a small test workload and generate representative traffic.
1. In Cost Management, group costs by **Resource** and then by **Meter**.
1. Compare actual meter charges to your estimate assumptions, and adjust your baseline budget.

Expected result: You can map each major estimate assumption to one or more observed billing meters, and explain any material variance before production rollout.

### Reconcile estimates with actual costs

Use this checklist after each test cycle:

1. Confirm the evaluation scope (subscription, resource group, or resource) matches the scope used in your estimate.
1. Export or view meter-level charges for the same date range used during test traffic.
1. Verify that required tags are present and consistently applied to participating resources.
1. Compare estimate assumptions to observed meters, and record variance by service.
1. Update budgets and alert thresholds only after you validate at least one full billing cycle trend.

**Reference:** [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/)

## Costs associated with Foundry

When you create a Foundry resource, you pay for the Azure services you use, such as Azure OpenAI, Azure Speech in Foundry, Content Safety, Azure Vision in Foundry, Azure Document Intelligence, and Azure Language in Foundry. Costs vary by service and feature. For details, see the [Foundry Tools pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/).

## Understand billing models for Foundry

Foundry resources run on Azure infrastructure and accrue costs when deployed. When you create or use Foundry resources, you're charged based on the services you use.

Common billing approaches include:

- **Pay-as-you-go (Serverless API):** You're billed according to your usage of each Azure service.
- **Commitment tiers:** You commit to using service features for a fixed fee, providing predictable costs. For details, see [Commitment tier pricing](/azure/ai-services/commitment-tier).

> [!NOTE]
> If you use the resource above the quota provided by the commitment plan, you pay for the extra usage as described in the overage amount in the Azure portal when you buy a commitment plan.
