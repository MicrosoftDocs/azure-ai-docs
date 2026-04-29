---
title: Include file
description: Include file
author: msakande
ms.author: mopeakande
ms.reviewer: josander
reviewer: johnrsanders
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/29/2026
ms.custom: include, classic-and-new
---

Microsoft Foundry Models move through a predictable lifecycle—from preview to general availability (GA) to eventual retirement—giving you time to evaluate replacements and migrate workloads. This article explains each lifecycle stage, the overlap commitments Microsoft makes when a model retires, and how you're notified. For specific retirement dates, see [Model retirement schedule](../concepts/model-retirement-schedule.md).

## How model lifecycle works

Microsoft Foundry continuously refreshes its model catalog with newer, more capable models. When a model is superseded, it moves through a predictable lifecycle that gives customers time to evaluate replacements and migrate. The lifecycle applies uniformly across Foundry Models [sold directly by Azure](/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) and [from partners and community](/azure/foundry/foundry-models/concepts/models-from-partners), though notification timelines differ slightly by model origin.

### Lifecycle stages

Every model in the Foundry catalog belongs to exactly one of these five stages:

:::image type="content" source="../media/concepts/lifecycle-stage-transitions.png" alt-text="Screenshot showing model lifecycle stage transitions." lightbox="../media/concepts/lifecycle-stage-transitions.png":::

| Stage | What it means | Can create new deployments? | Existing deployments work? |
|-------|--------------|----------------------------|---------------------------|
| **Preview** | Experimental. Weights, runtime, and API schema might change. Not guaranteed to become GA. Labeled "Preview" in the catalog. | Yes | Yes |
| **Generally Available (GA)** | Production-ready. Weights and APIs are fixed. Runtime patches for security vulnerabilities don't affect outputs. No label shown (default state). | Yes | Yes |
| **Legacy** | Newer, more capable models exist. You should plan on migrating workloads. This stage is **optional**—models might skip directly from GA to Deprecated. | Yes (until deprecation) | Yes |
| **Deprecated** | Existing customers can continue to create and manage deployments. No longer available to new customers—new customers can't create deployments or access the model. "Existing customer" is determined at the subscription level: whether that Azure subscription has ever deployed the specific model version. A new subscription under the same tenant doesn't inherit access. | - Existing customers: Yes.<br> - New customers: **No** | Yes |
| **Retired** | Removed from service. All inference requests return `410 Gone`. | **No** | **No** |

> [!NOTE]
> - **Fine-tuned models** follow a separate retirement schedule for training and deployment. See [Fine-tuned models](#fine-tuned-models) for details.
> - **Foundry Models (catalog)**: Some model providers define a shorter GA lifecycle—for example, 12 months instead of 18. When a shorter lifecycle applies, it is noted directly on the model in the [Model Retirement Schedule](../concepts/model-retirement-schedule.md).

## Model launch and availability

New models become available through deployment types in this order:

:::image type="content" source="../media/concepts/lifecycle-availability-rollout.png" alt-text="Screenshot showing the order of deployment type availability for models." lightbox="../media/concepts/lifecycle-availability-rollout.png":::

| Order | Deployment type | When available |
|-------|----------------|---------------|
| 1 | **Global Standard** | At launch—broadest availability and lowest latency across regions |
| 2 | **Global Provisioned** | Follows closely after Global Standard—provides reserved throughput with global routing |
| 3 | **Data Zone Standard** and **Data Zone Provisioned** | After Global Provisioned—data processing stays within a defined geographic boundary |
| 4 | **Standard** and **Provisioned** | Last—regional-only, as older models retire and capacity is reallocated |

> [!TIP]
> For a full comparison of deployment types, see [Deployment type comparison](../../foundry-models/concepts/deployment-types.md).

## Lifecycle and availability variations

Several factors affect how the standard lifecycle applies to your deployments, including the region you operate in, the cloud environment you use, and security requirements.

### Regional availability

- Not all model and version combinations are available in all regions.
- Typically, more specialized models—for example, audio, image, and video generation—are only available as Data Zone or Global deployment types.
- Successive model versions might not be available in the same regions. A newer version can appear in some regions before upgrades are scheduled in others.
- Microsoft can limit new customers in specific regions to maintain service quality for existing customers.

### Azure Government clouds

- Global Standard deployments aren't available in government clouds.
- Not all models or versions available in commercial clouds are available in government clouds.
- Government clouds typically support only one version of a given model at a time, with a **30-day overlap** when a new version becomes available.

For more information, see [Foundry Models sold directly by Azure (government)](/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-gov), [Model versions](/azure/foundry/foundry-models/concepts/model-versions-gov), and [Deployment types](/azure/foundry/foundry-models/concepts/deployment-types-gov) in Azure Government.

### Security-driven retirements

If a model is found to have compliance or security issues, Microsoft reserves the right to invoke an **emergency retirement** with shortened notice. Refer to the Azure terms of service for details.

## Lifecycle timeline commitments

Microsoft makes specific commitments about how long model versions stay available and when replacements appear, so you can plan migrations with confidence.

### Generally Available (GA) replacement model overlap commitments

We commit to meaningful overlap between a retiring GA model and its replacement so customers can test, evaluate, and migrate with confidence.

:::image type="content" source="../media/concepts/general-availability-lifecycle-and-replacement-transition-timeframes.png" alt-text="Screenshot of the general availability model lifecycle showing model overlap and replacement transition timeframes." lightbox="../media/concepts/general-availability-lifecycle-and-replacement-transition-timeframes.png":::

| Phase | Pattern |
|-------|---------|
| **GA launch** | Each model launches per its own deployment type and region availability matrix. Retirement date (18 months out) is set programmatically and available via the [Models API](/rest/api/aiservices/accountmanagement/models). |
| **Deprecated (existing customers only)** | At 12 months from launch, existing customers can continue to create and manage deployments. New customers can't access the model. |
| **Replacement available in global standard** | Customers can use and test the replacement model in global standard approximately 90 days before retirement. |
| **Replacement available in provisioned regions** | Replacement model becomes available to test in provisioned regions where the predecessor is retiring approximately 30 days before retirement, giving provisioned customers a manual migration window. |
| **Model version retired** | At 18 months from launch, all inference returns `410 Gone`. |

> [!TIP]
> **Why 90–120 days?** The official replacement model is selected and declared approximately 90–120 days before the retiring model's retirement date—not sooner. Given the rapid pace of improvement in generative AI, declaring a replacement too early risks directing customers to a model that is no longer the best available option by the time they need to migrate.

### Preview model lifecycle

Preview models have a fundamentally different lifecycle than GA models. They launch with a "not sooner than" retirement date (typically 90 days out), but are sometimes extended beyond that initial window, until a suitable replacement preview or GA model version is available. When a retirement decision is made, customers are **force-upgraded** to a replacement (a newer preview version or the GA model) or the model is **retired with no replacement**. There's no option to remain on a retiring preview model—all preview deployments are either upgraded or terminated.

> [!NOTE]
> Preview models aren't recommended for production workloads.

:::image type="content" source="../media/concepts/preview-lifecycle-and-replacement-transition-timeframes.png" alt-text="Screenshot of the preview lifecycle of models, showing model overlap and replacement transition timeframes." lightbox="../media/concepts/preview-lifecycle-and-replacement-transition-timeframes.png":::

| Outcome | What happens |
|---------|-------------|
| **Upgrade to newer Preview** | Existing preview deployments are force-upgraded to a newer preview version. Customers get at least **30 days notice**. The cycle repeats until a GA version is available. |
| **Upgrade to GA** | When the GA model launches, preview deployments are force-upgraded to the GA version. Customers get at least **30 days notice**. The GA model then follows the standard 18-month GA lifecycle. |
| **No replacement (rare)** | If no replacement exists, customers get **30 days notice** before the model retires and inference returns `410 Gone`. |

## Automatic upgrades

For **Global Standard**, **Data Zone Standard**, and **Standard** deployment types, Microsoft manages automatic upgrades when a model version is retired:

- Auto-upgrades are scheduled on a **rolling, region-by-region** basis.
- The upgrade schedule is published in advance in the [Model Retirement Schedule](../concepts/model-retirements.md).
- Upgrades can occur even if the new model version isn't yet separately available in that region, or for that SKU—the upgrade process will make it available.

> [!IMPORTANT]
> **Provisioned deployments are NOT auto-upgraded.** Provisioned customers must manually migrate to the replacement model.
>
> Use the [Models API](/rest/api/aiservices/accountmanagement/models) to programmatically check `lifecycleStatus`, `deprecation`, and per-SKU `deprecationDate` for any model at any time.

### Example: gpt-4o → gpt-5.1 upgrade

When gpt-4o versions `2024-05-13` and `2024-08-06` retired on **2026-03-31**, they were auto-upgraded to gpt-5.1 on the Standard SKU. Before the upgrade, gpt-5.1 had no Standard presence at all. After the upgrade, gpt-5.1 Standard was added to all eight regions that previously had those gpt-4o versions (centralus, eastus, eastus2, northcentralus, southcentralus, swedencentral, westus, westus3). Version `2024-11-20` was unaffected (retires 2026-10-01).

## Migration to a replacement model

When a model you use enters the Legacy or Deprecated stage, check the "Suggested Replacement" column in the [Model Retirement Schedule](../concepts/model-retirements.md) and follow the steps in [Working with models](/azure/foundry/openai/how-to/working-with-models) to deploy, test, and migrate to the replacement.

## Notifications

GA models have their retirement date set programmatically at launch to 18 months out—there's no separate "announcement." Legacy and Deprecated transitions follow the published timeline and are visible in real time via the [Models API](/rest/api/aiservices/accountmanagement/models).

### When you receive active notifications

| Event | Timing | Applies to |
|-------|--------|-----------|
| **GA model retirement notice** | At least **60 days** before retirement | All GA models. Sent to subscription owners with active deployments. |
| **Preview model retirement notice** | At least **30 days** before retirement | Preview models. Preview deployments can be auto-upgraded to the replacement if a replacement model is available and applicable (for example, doesn't require a different API contract). |

### How you're notified

| Channel | Details |
|---------|---------|
| **Email** | Sent automatically to subscription owners with active deployments. |
| **Azure Service Health** | Health advisories appear for affected subscriptions. Go to [Service Health > Health advisories](https://portal.azure.com/#blade/Microsoft_Azure_Health/AzureHealthBrowseBlade/healthAdvisories), filter by `Azure OpenAI Service`, and create an alert rule for email, text messages, or webhook notifications. |

### Programmatic methods to check model lifecycle and deprecation

Customers can check lifecycle and deprecation fields on any model using the [Models API](/rest/api/aiservices/accountmanagement/models) (subscription-scoped, all models in a region):

```http
GET https://management.azure.com/subscriptions/{sub}/providers/Microsoft.CognitiveServices/locations/{location}/models?api-version=2024-10-01
```

Fields: `lifecycleStatus`, `deprecation.inference`, `deprecation.fineTune`, per-SKU `deprecationDate` (ISO dates).

## Fine-tuned models

Fine-tuned models retire in two phases: training and deployment.

Unless explicitly stated, training retires no earlier than the base model retirement date. After a model is retired for training, it's no longer available for fine-tuning but any previously trained models remain available for deployment.

At deployment retirement, inference and deployment return error responses.

| Model | Version | Training retirement date | Deployment retirement date |
|-------|---------|--------------------------|----------------------------|
| gpt-4o | 2024-08-06 | No earlier than 2027-04-01<sup>1</sup> | 2027-10-01 |
| gpt-4o-mini | 2024-07-18 | No earlier than 2027-04-01<sup>1</sup> | 2027-10-01 |
| gpt-4.1 | 2025-04-14 | No earlier than 2027-04-14<sup>1</sup> | 2027-10-14 |
| gpt-4.1-mini | 2025-04-14 | No earlier than 2027-04-14<sup>1</sup> | 2027-10-14 |
| gpt-4.1-nano | 2025-04-14 | No earlier than 2027-04-14<sup>1</sup> | 2027-10-14 |
| o4-mini | 2025-04-16 | Base model retirement | One year after training retirement |

<sup>1</sup> For existing customers only. Otherwise, training retirement occurs at base model retirement.

## Frequently asked questions

| Question | Answer | Learn more |
|----------|--------|------------|
| **What's the difference between a model family, version, and variant?** | A *model family* is a generation of models (for example, GPT-4o, GPT-5). A *model version* is a dated release within a family (for example, gpt-4o 2024-05-13 vs. 2024-08-06). A *model variant* is a size/capability tier within the same family (for example, GPT-5, GPT-5-mini, GPT-5-nano). | [Model versions](/azure/foundry/foundry-models/concepts/model-versions) |
| **Can I control when my Standard deployment auto-upgrades?** | Yes. Set the `versionUpgradeOption` property on your deployment to one of three values: `OnceNewDefaultVersionAvailable` (upgrade when a new default is set), `OnceCurrentVersionExpired` (upgrade only at retirement), or `NoAutoUpgrade` (never auto-upgrade—deployment stops working at retirement). You can configure this setting via REST API, Azure PowerShell, or the Foundry portal. | [Working with models—upgrade configuration](/azure/foundry/openai/how-to/working-with-models#model-deployment-upgrade-configuration) |
| **How do I migrate a Provisioned deployment?** | Provisioned deployments aren't auto-upgraded. You have two options: *In-place migration* (Azure handles traffic migration over a 20–30 minute window with no downtime) or *Side-by-side (multi-deployment) migration* (you create a new deployment, test, switch traffic, and delete the old one). | [Managing models on provisioned deployment types](/azure/foundry/openai/how-to/working-with-models#managing-models-on-provisioned-deployment-types) |
| **Will my quota carry over to the replacement model?** | For Standard auto-upgrades, yes—quota is handled automatically. For Provisioned deployments, you must ensure quota is available for the target model before migrating. PTU capacity is model-agnostic and fungible across provisioned managed deployments. | [Provisioned throughput—quota](/azure/foundry/openai/concepts/provisioned-throughput) |
| **Can I get an exception to extend a model's retirement date?** | No. Retirement dates aren't extendable. Plan your migration using the timelines published in the [Model Retirement Schedule](../concepts/model-retirements.md) and the [Models API](/rest/api/aiservices/accountmanagement/models). | N/A |
| **What tools can help me evaluate a replacement model?** | Use the model leaderboard in the [Foundry portal](https://ai.azure.com/explore/models) to compare benchmarks, the model comparison feature when deploying, and [Evaluations](/azure/foundry/openai/concepts/model-retirements?tabs=text#preparation-for-model-retirements-and-version-upgrades) for custom workload testing. Apply prompt engineering and fine-tuning as needed to match prior accuracy. | [Preparation for model retirements](/azure/foundry/openai/concepts/model-retirements?tabs=text#preparation-for-model-retirements-and-version-upgrades) |
| **Do embeddings models follow the same lifecycle?** | Embeddings models (text-embedding-3-large, text-embedding-3-small, text-embedding-ada-002) have extended timelines and are handled differently from inference models. Check the [Model Retirement Schedule](../concepts/model-retirements.md) for specific dates. | [Model retirements—embeddings](/azure/foundry/openai/concepts/model-retirements) |
| **How do Priority Processing and Batch deployments upgrade?** | Priority Processing follows the same upgrade process as Standard deployments (auto-upgrade supported). Batch deployments follow the side-by-side (multi-deployment) migration approach—deploy the new model, resubmit jobs, then retire the old deployment. | [Working with models](/azure/foundry/openai/how-to/working-with-models) |
| **I can't find "Microsoft Foundry" in Azure Service Health—how do I set up alerts?** | Select `Azure OpenAI Service` as the service name when configuring Service Health alerts. There's no separate "Microsoft Foundry" service in Service Health. | [Set up Service Health alerts](/azure/service-health/alerts-activity-log-service-notifications-portal) |

## Related content

- [Model Retirement Schedule](../concepts/model-retirements.md) for specific dates for all current, deprecated, and retired models
- [Models API reference](/rest/api/aiservices/accountmanagement/models) to programmatically query `lifecycleStatus`, `deprecation`, and per-SKU `deprecationDate` for any model
- [Model versions in Microsoft Foundry Models](../../foundry-models/concepts/model-versions.md) for how version upgrades work
- [Getting started with model evaluation](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/how-to-evaluate-amp-upgrade-model-versions-in-the-azure-openai/ba-p/4218880)
- [Managing models on provisioned deployment types](/azure/foundry/openai/how-to/working-with-models#managing-models-on-provisioned-deployment-types)
- [Set up Service Health alerts](/azure/service-health/alerts-activity-log-service-notifications-portal)