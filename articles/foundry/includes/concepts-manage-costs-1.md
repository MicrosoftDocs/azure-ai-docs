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
  - [**AI User**](../concepts/rbac-foundry.md#built-in-roles) – View Foundry resource data and costs.
- **Supported Azure account type:** One of the [supported account types for Cost Management](/azure/cost-management-billing/costs/understand-cost-mgt-data).

If you need to grant these roles to team members, see [Assign access to Cost Management data](/azure/cost-management-billing/costs/assign-access-acm-data) and [Foundry RBAC roles](../concepts/rbac-foundry.md).

> [!NOTE]
> Foundry doesn't have a dedicated page in the Azure pricing calculator because Foundry is composed of several optional Azure services. This article shows how to use the calculator to estimate costs for these services.

## Estimate costs before using Foundry

Use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate costs before you add Foundry resources.

1. Go to the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).
1. Search for and select a product, such as Azure Speech in Foundry or Azure Language in Foundry.
1. Select additional products to estimate costs for multiple services. For example, add Azure AI Search to include potential search costs.
1. As you add resources to your project, return to the calculator and update estimates.

**Reference:** [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/)

## Costs associated with Foundry

When you create a Foundry resource, you pay for the Azure services you use, such as Azure OpenAI, Azure Speech in Foundry, Content Safety, Azure Vision in Foundry, Azure Document Intelligence, and Azure Language in Foundry. Costs vary by service and feature. For details, see the [Foundry Tools pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/).

## Understand billing models for Foundry

Foundry resources run on Azure infrastructure and accrue costs when deployed. When you create or use Foundry resources, you're charged based on the services you use.

Two billing models are available:

- **Pay-as-you-go (Serverless API):** You're billed according to your usage of each Azure service.
- **Commitment tiers:** You commit to using service features for a fixed fee, providing predictable costs. For details, see [Commitment tier pricing](/azure/ai-services/commitment-tier).

> [!NOTE]
> If you use the resource above the quota provided by the commitment plan, you pay for the extra usage as described in the overage amount in the Azure portal when you buy a commitment plan.
