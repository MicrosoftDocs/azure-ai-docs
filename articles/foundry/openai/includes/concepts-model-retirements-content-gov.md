---
title: Include file
description: Include file
author: challenp
ms.author: chaparker
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/24/2026
ms.custom: include, classic-and-new
---

Microsoft Foundry Models in Azure Government move through a predictable lifecycle—from preview to general availability (GA) to eventual retirement—giving you time to evaluate replacements and migrate workloads. This article explains each lifecycle stage, the overlap commitments Microsoft makes when a model retires, and how you're notified in Azure Government. For specific retirement dates, see [Model retirement schedule](../concepts/model-retirement-schedule-gov.md).

This article focuses on where there are differences from Commercial for Azure Government. For general information, see [Foundry Models lifecycle and support policy](../concepts/model-retirements.md). 

## How model lifecycle works

Microsoft Foundry continuously refreshes its model catalog with newer, more capable models. When a model is superseded, it moves through a predictable lifecycle that gives customers time to evaluate replacements and migrate. The lifecycle applies across Foundry Models in Azure Government [sold directly by Azure](/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-gov).

### Lifecycle stages

Since Preview models are not delivered within Azure Government, every model in the Foundry catalog in Azure Government belongs to exactly one of four stages:

| Stage | What it means | Can create new deployments? | Existing deployments work? |
|-------|--------------|----------------------------|---------------------------|
| **Generally Available (GA)** | Production-ready. Weights and APIs are fixed. Runtime patches for security vulnerabilities don't affect outputs. No label shown (default state). | Yes | Yes |
| **Legacy** | Newer, more capable models exist. You should plan on migrating workloads. This stage is **optional**—models might skip directly from GA to Deprecated. | Yes (until deprecation) | Yes |
| **Deprecated** | Existing customers can continue to create and manage deployments. No longer available to new customers—new customers can't create deployments or access the model. "Existing customer" is determined at the subscription level: whether that Azure subscription has ever deployed the specific model version. A new subscription under the same tenant doesn't inherit access. | - Existing customers: Yes.<br> - New customers: **No** | Yes |
| **Retired** | Removed from service. All inference requests return `410 Gone`. | **No** | **No** |

## Model launch and availability

New models become available through deployment types in a predictable order:

| Order | Deployment type | When available |
|-------|----------------|---------------|
| 1 | **Data Zone Standard** | When first launched in Azure Government |
| 2 | **Data Zone Provisioned** | After Data Zone Standard - provides reserved throughput |
| 3 | **Standard** and **Provisioned** | Last—regional-only, as older models retire and capacity is reallocated |

### Availability rollout at a glance

```
Data Zone Standard  ──►  Data Zone Provisioned  ──►   Standard
                                                         and
    (at launch)        (expands to Provisioned)      Provisioned   
                                                     (as capacity
                                                       permits)
```

> [!TIP]
> For a full comparison of deployment types, see [Deployment type comparison](../../foundry-models/concepts/deployment-types-gov.md).

## Special considerations

Several factors affect how the standard lifecycle applies to your deployments, including the region you operate in, the type of deployment, and security requirements.

### Regional availability

- Not all model and version combinations are available in all regions.
- Successive model versions might not be available in the same regions. A newer version can appear in some regions before upgrades are scheduled in others.

### Generally Available (GA) replacement model overlap commitments

We commit to meaningful overlap between a retiring GA model and its replacement so customers can test, evaluate, and migrate with confidence. In Azure Government, this relies on a two-step process that leverages the earlier availability in Commercial cloud.

| Phase | Pattern |
|-------|---------|
| **Azure Government launch** | Each model launches per its own deployment type and region availability matrix. Retirement date in Azure Government is set to match the Commercial Cloud date and is available via the [Models API](/rest/api/aiservices/accountmanagement/models). |
| **Deprecated (existing customers only)** | At 12 months from Commercial launch, existing customers can continue to create and manage deployments. New customers can't access the model. |
| **Replacement available in global standard** | Customers can use and test the replacement model in global standard in Commercial Cloud approximately 90 days before retirement. |
| **Replacement available in Azure Government** | Replacement model becomes available to test in Azure Government where the predecessor is retiring approximately 30 days before retirement. |
| **Model version retired** | At 18 months from Commercial launch, all inference returns `410 Gone`. Where the Azure Government availability of the replacement is less than 30 days from this retirement date, that model's retirement date will be extended in Azure Government to allow at least 30 days of overlap in the Azure Government cloud.  |

### Understanding automatic upgrades

For **Data Zone Standard** and **Standard** deployment types, Microsoft manages automatic upgrades when a model version is retired where Deployment Type and Region align:

- Auto-upgrades are scheduled on a **rolling, region-by-region** basis.
- The upgrade schedule is published in advance in the [Model Retirement Schedule](../concepts/model-retirements-gov.md).
- For models where the upgrade target is not available in the same Deployment Type and Region, no model upgrade is performed.

> [!IMPORTANT]
> **Provisioned deployments are NOT auto-upgraded.** Provisioned customers must manually migrate to the replacement model.
>
> Use the [Models API](/rest/api/aiservices/accountmanagement/models) to programmatically check `lifecycleStatus`, `deprecation`, and per-SKU `deprecationDate` for any model at any time.

### Example: gpt-4o-0513 → gpt-4.1 upgrade

When gpt-4o version `2024-05-13` retired on **2026-03-31**, they were auto-upgraded to gpt-4.1 on the Standard and DataZone SKU if there was a matching offering. 

## Notifications

GA models have their retirement date set programmatically at Commercial launch to 18 months out—there's no separate "announcement." Legacy and Deprecated transitions follow the published timeline and are visible in real time via the [Models API](/rest/api/aiservices/accountmanagement/models).

### When you receive active notifications

| Event | Timing | Applies to |
|-------|--------|-----------|
| **Azure Government model retirement notice** | At least **60 days** before retirement | All GA models. Sent to subscription owners with active deployments. |
| **Azure Government model retirement warning** | At least **30 days** before retirement | All GA models. Sent to subscription owners with active deployments. |

### How you're notified

| Channel | Details |
|---------|---------|
| **Email** | Sent automatically to subscription owners with active deployments. |
| **Azure Service Health** | Health advisories appear for affected subscriptions. Go to [Service Health > Health advisories](https://portal.azure.us/#blade/Microsoft_Azure_Health/AzureHealthBrowseBlade/healthAdvisories), filter by `Azure OpenAI Service`, and create an alert rule for email, text messages, or webhook notifications. |

## Related content

- [Model Retirement Schedule in Azure Government](../concepts/model-retirements-gov.md) for specific dates for all current, deprecated, and retired models
- [Models API reference](/rest/api/aiservices/accountmanagement/models) to programmatically query `lifecycleStatus`, `deprecation`, and per-SKU `deprecationDate` for any model
- [Model versions in Microsoft Foundry Models in Azure Government](../../foundry-models/concepts/model-versions-gov.md) for how version upgrades work
- [Getting started with model evaluation](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/how-to-evaluate-amp-upgrade-model-versions-in-the-azure-openai/ba-p/4218880)
- [Managing models on provisioned deployment types](/azure/foundry/openai/how-to/working-with-models#managing-models-on-provisioned-deployment-types)
- [Set up Service Health alerts](/azure/service-health/alerts-activity-log-service-notifications-portal)
