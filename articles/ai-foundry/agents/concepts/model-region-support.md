---
title: Azure OpenAI models and regions for Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Find supported Azure OpenAI models and regions for Microsoft Foundry Agent Service. Compare gpt-5, gpt-4o, and gpt-4 availability across global and regional deployments.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 02/02/2026
ms.custom: azure-ai-agents, references_regions, pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Azure OpenAI models and regions for Foundry Agent Service

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Azure OpenAI models power agents in Microsoft Foundry Agent Service. This article helps you choose a supported model and region combination for your deployment. Choosing the right model and region affects your agent's capabilities, latency, and cost.

To use these models, you need a [Microsoft Foundry project](../../what-is-foundry.md) with access to Foundry Agent Service.

Microsoft Foundry offers two main types of deployments:

- *Standard* includes a global deployment option that routes traffic across Azure's global infrastructure to maximize throughput and availability.
- *Provisioned* also includes a global deployment option. You can purchase and deploy provisioned throughput units (PTUs) across Azure's global infrastructure for predictable performance.

All deployments can perform the same inference operations. However, the billing, scale, and performance are substantially different. To learn more about Azure OpenAI deployment types, see [Deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md).

## How to use this page

Use the tables in this article to choose a supported combination of deployment type, model version, and Azure region.

- **Deployment type**: Use the tabs to select the deployment type you plan to use (standard or provisioned).
- **Region**: The **Region** column lists the Azure region where you deploy the model.
- **Availability markers**:
  - ✅: Supported.
  - Blank cells or `-`: Not supported.

## Choose a model

Select a model based on your agent's requirements:

- **gpt-5 family** (gpt-5, gpt-5-mini, gpt-5-nano, gpt-5-chat): Frontier-scale reasoning for complex, multi-step tasks. Registration is required for access.
- **gpt-4.1 family** (gpt-4.1, gpt-4.1-mini, gpt-4.1-nano): Cost-effective models for general-purpose agent workloads.
- **gpt-4o family** (gpt-4o, gpt-4o-mini): Multimodal capabilities with vision support.
- **gpt-4 and gpt-35-turbo**: Legacy models for backward compatibility.

> [!TIP]
> **Quick start**: For most new agents, deploy **gpt-4o, 2024-11-20** in **swedencentral** or **eastus2** using Global standard deployment. These regions have broad model availability and low latency for most scenarios.

## Available models

Foundry Agent Service supports the following Azure OpenAI models in the listed regions.

Keep in mind that model availability varies by region and cloud. Certain tools and capabilities require the latest models. The following models are available in the REST API and SDKs.

::: moniker range="foundry-classic"
> [!NOTE]
>
> - [Hub-based projects](../../what-is-foundry.md#types-of-projects) are limited to the following models: gpt-4o, gpt-4o-mini, gpt-4, and gpt-35-turbo.
> - [Spillover traffic management](../../openai/how-to/spillover-traffic-management.md) for [provisioned throughput](../../openai/concepts/provisioned-throughput.md) is compatible with agents.
> - For information on Class A subnet support, see the [setup guide on GitHub](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15-private-network-standard-agent-setup).
> - The [file search tool](../how-to/tools-classic/file-search.md) is currently unavailable in the Italy North and Brazil South regions.
> - The gpt-5 models can use only the [code interpreter](../how-to/tools-classic/code-interpreter.md) and [file search](../how-to/tools-classic/file-search.md) tools.
> - [Registration](https://aka.ms/openai/gpt-5/2025-08-07) is required to use the gpt-5 models. Access is granted according to Microsoft's eligibility criteria.
::: moniker-end

::: moniker range="foundry"
> [!NOTE]
>
> - [Spillover traffic management](../../openai/how-to/spillover-traffic-management.md) for [provisioned throughput](../../openai/concepts/provisioned-throughput.md) is compatible with agents.
> - For information on Class A subnet support, see the [setup guide on GitHub](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15-private-network-standard-agent-setup).
> - The [file search tool](../../default/agents/how-to/tools/file-search.md?view=foundry&preserve-view=true) is currently unavailable in the Italy North and Brazil South regions.
> - The gpt-5 models are available for the [code interpreter](../../default/agents/how-to/tools/code-interpreter.md?view=foundry&preserve-view=true) and [file search](../../default/agents/how-to/tools/file-search.md?view=foundry&preserve-view=true) tools.
> - [Registration](https://aka.ms/openai/gpt-5/2025-08-07) is required to use the gpt-5 models. Access is granted according to Microsoft's eligibility criteria.
::: moniker-end

# [Global standard](#tab/global-standard)

| Region | gpt-5.2 | gpt-5.1 | gpt-5 | gpt-5-mini | gpt-5-nano | gpt-5-chat | gpt-4.1 | gpt-4.1-nano | gpt-4.1-mini | gpt-4o (05-13) | gpt-4o (08-06) | gpt-4o (11-20) | gpt-4o-mini | gpt-4 | gpt-4-turbo |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| australiaeast | | ✅ | ✅ | ✅ | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| brazilsouth | | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | | ✅ |
| canadaeast | | ✅ | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| eastus | | | ✅ | ✅ | | | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| eastus2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| francecentral | | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| germanywestcentral | | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| italynorth | | | | | | | ✅ | ✅ | ✅ | | | ✅ | ✅ | | |
| japaneast | | ✅ | ✅ | ✅ | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| norwayeast | | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| southafricanorth | | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | | ✅ |
| southcentralus | ✅ | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| southindia | | | ✅ | ✅ | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| swedencentral | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| switzerlandnorth | | ✅ | ✅ | ✅ | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| uksouth | | ✅ | ✅ | ✅ | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| westeurope | | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | | ✅ |
| westus | | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| westus3 | | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

# [Global provisioned managed](#tab/ptu-global)

| Region | gpt-5.2 | gpt-5.1 | gpt-5 | gpt-5-mini | gpt-4.1 | gpt-4.1-nano | gpt-4.1-mini | gpt-4o (05-13) | gpt-4o (08-06) | gpt-4o (11-20) | gpt-4o-mini |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| australiaeast | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| brazilsouth | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| canadaeast | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| eastus | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| eastus2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| francecentral | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| germanywestcentral | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| italynorth | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| japaneast | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| norwayeast | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| polandcentral | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| southafricanorth | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| southcentralus | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| southeastasia | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| southindia | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| swedencentral | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| switzerlandnorth | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| uksouth | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| westeurope | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| westus | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| westus3 | | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

# [Standard](#tab/standard)

| Region | o3-deep-research | gpt-4o (05-13) | gpt-4o (08-06) | gpt-4o (11-20) | gpt-4o-mini | gpt-4 | gpt-4-turbo | gpt-4-32k | gpt-35-turbo (1106) | gpt-35-turbo (0125) |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| australiaeast | | | | ✅ | | ✅ | | ✅ | ✅ | ✅ |
| canadaeast | | | | ✅ | | ✅ | | ✅ | ✅ | ✅ |
| eastus | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | | | ✅ |
| eastus2 | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | | | ✅ |
| francecentral | | | | ✅ | | ✅ | | ✅ | ✅ | ✅ |
| japaneast | | | | ✅ | | | | | | ✅ |
| norwayeast | ✅ | | | ✅ | | | | | | |
| southcentralus | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | | | ✅ |
| southindia | | | | ✅ | | | | | ✅ | ✅ |
| swedencentral | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| switzerlandnorth | | | | ✅ | | ✅ | | ✅ | | ✅ |
| uksouth | | | | ✅ | | | | | ✅ | ✅ |
| westeurope | | | | | | | | | | ✅ |
| westus | ✅ | ✅ | ✅ | ✅ | ✅ | | ✅ | | ✅ | ✅ |
| westus3 | | ✅ | ✅ | ✅ | ✅ | | ✅ | | | ✅ |

# [Provisioned managed](#tab/ptu)

| Region | gpt-5 | gpt-5-mini | gpt-4.1 | gpt-4.1-nano | gpt-4.1-mini | gpt-4o (05-13) | gpt-4o (08-06) | gpt-4o (11-20) | gpt-4o-mini | gpt-4 | gpt-4-turbo | gpt-4-32k | gpt-35-turbo (1106) | gpt-35-turbo (0125) |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| australiaeast | | | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| brazilsouth | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | |
| canadaeast | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | |
| eastus | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| eastus2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| francecentral | | | | | | ✅ | ✅ | | ✅ | ✅ | | ✅ | | ✅ |
| germanywestcentral | | | | | | ✅ | ✅ | ✅ | | ✅ | | ✅ | ✅ | |
| japaneast | | | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | | ✅ | | | ✅ |
| southafricanorth | | | | | | ✅ | | | | ✅ | ✅ | ✅ | ✅ | |
| southcentralus | ✅ | | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| southeastasia | | | | | | | ✅ | ✅ | ✅ | | | | | |
| southindia | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ |
| swedencentral | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| switzerlandnorth | | | | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| uksouth | | | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| westeurope | | | | | | | | ✅ | | | | | | |
| westus | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| westus3 | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## Non-OpenAI models

In addition to Azure OpenAI models, you can use models sold directly by Azure. These models offer specialized capabilities for specific use cases, such as deterministic reasoning or high-throughput generation.

[!INCLUDE [agent-service-models-support-list](../includes/agent-service-models-support-list.md)]

## View all agent-supported models in the Foundry portal

[!INCLUDE [agent-service-view-models-in portal](../includes/agent-service-view-models-in-portal.md)]

## Verify model support

Model availability can change over time.

- To verify what you can deploy for your project and region, use the Foundry portal model experience described in the previous section.
- If you use provisioned throughput, make sure you have provisioned throughput units (PTUs) available in the target region. For background, see [Provisioned throughput](../../openai/concepts/provisioned-throughput.md).

## Troubleshooting

### A model or version isn't available in your region

- Confirm you selected the right tab for your deployment type.
- Try a different region that supports the model and version.
- If you're using gpt-5 models, make sure your subscription has access. Some models require registration.

### File search isn't available

- File search isn't available in Italy North and Brazil South. Choose a supported region, or use a different tool.

### Provisioned throughput deployment fails

- Confirm you have enough PTUs available in the region.
- Review [Provisioned throughput](../../openai/concepts/provisioned-throughput.md) and [Spillover traffic management](../../openai/how-to/spillover-traffic-management.md).

## Related content

- [Create a new agent](../quickstart.md)
- [Foundry Agent Service quotas and limits](../quotas-limits.md)
- [Deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md)
- [Feature availability across cloud regions](../../reference/region-support.md)
