---
title: Supported Models in Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn about the models that you can use with Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 12/04/2025
ms.custom: azure-ai-agents, references_regions
monikerRange: 'foundry-classic || foundry'
---

# Supported models in Foundry Agent Service

[!INCLUDE [version-banner](../../includes/version-banner.md)]

In this article, you learn about the diverse set of Azure OpenAI models that agents use in Microsoft Foundry Agent Service. These models have various capabilities and price points.

Microsoft Foundry offers two main types of deployments:

- *Standard* includes a global deployment option that routes traffic globally to provide higher throughput.
- *Provisioned* also includes a global deployment option. You can purchase and deploy provisioned throughput units across the Azure global infrastructure.

All deployments can perform the same inference operations. However, the billing, scale, and performance are substantially different. To learn more about Azure OpenAI deployment types, see [Deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md).

## Available models

Foundry Agent Service supports the following Azure OpenAI models in the listed regions.

Keep in mind that model availability varies by region and cloud. Certain tools and capabilities require the latest models. The following models are available in the REST API and SDKs.

::: moniker range="foundry-classic"
> [!NOTE]
>
> - [Hub-based projects](../../what-is-azure-ai-foundry.md#types-of-projects) are limited to the following models: gpt-4o, gpt-4o-mini, gpt-4, gpt-35-turbo.
> - [Spillover traffic management](../../openai/how-to/spillover-traffic-management.md) for [provisioned throughput](../../openai/concepts/provisioned-throughput.md) is compatible with agents.
> - For information on Class A subnet support, see the [setup guide on GitHub](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/15-private-network-standard-agent-setup).
> - The [file search tool](../how-to/tools/file-search.md) is currently unavailable in the Italy North and Brazil South regions.
> - The gpt-5 models can use only the [code interpreter](../how-to/tools/code-interpreter.md) and [file search](../how-to/tools/file-search.md) tools.
> - [Registration](https://aka.ms/openai/gpt-5/2025-08-07) is required to use the gpt-5 models. Access is granted according to Microsoft's eligibility criteria.
::: moniker-end

::: moniker range="foundry"
> [!NOTE]
>
> - [Spillover traffic management](../../openai/how-to/spillover-traffic-management.md) for [provisioned throughput](../../openai/concepts/provisioned-throughput.md) is compatible with agents.
> - For information on Class A subnet support, see the [setup guide on GitHub](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/15-private-network-standard-agent-setup).
> - The [file search tool](../how-to/tools/file-search.md) is currently unavailable in the Italy North and Brazil South regions.
> - The gpt-5 models are available for the [code interpreter](../how-to/tools/code-interpreter.md) and [file search](../how-to/tools/file-search.md) tools.
> - [Registration](https://aka.ms/openai/gpt-5/2025-08-07) is required to use the gpt-5 models. Access is granted according to Microsoft's eligibility criteria.
::: moniker-end

# [Global standard](#tab/global-standard)

| Region         | gpt-5, 2025-08-07 | gpt-5-mini, 2025-08-07 | gpt-5-nano, 2025-08-07 | gpt-5-chat, 2025-08-07 | gpt-4.1, 2025-04-14 | gpt-4.1-nano, 2025-04-14 | gpt-4.1-mini, 2025-04-14 | gpt-4o, 2024-05-13 | gpt-4o, 2024-08-06 | gpt-4o, 2024-11-20 | gpt-4o-mini, 2024-07-18 | gpt-4, 0613 | gpt-4, turbo-2024-04-09 |
|:-------------------|:-------------------------:|:------------------------------:|:------------------------------:|:------------------------------:|:---------------------------:|:--------------------------------:|:--------------------------------:|:--------------------------:|:--------------------------:|:--------------------------:|:-------------------------------:|:-------------------:|:-------------------------------:|
| `australiaeast`      | ✅                        | ✅                              |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `brazilsouth`        |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | -                   | ✅                              |
| `canadaeast`         |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `eastus`             | ✅                        | ✅                              |                                |                                | ✅                          |                                | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `eastus2`            | ✅                        | ✅                              | ✅                             |        ✅                        | ✅                          | ✅                               | ✅                               | ✅                          | ✅                         | ✅                          | ✅                              | ✅                   | ✅                              |
| `francecentral`      |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `germanywestcentral` |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `italynorth`         |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | -                          | -                          | ✅                         | ✅                               | -                   | -                               |
| `japaneast`          | ✅                        | ✅                              |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `norwayeast`         |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `southafricanorth`   |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | -                   | ✅                              |
| `southcentralus`     |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `southindia`         | ✅                        | ✅                              |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `swedencentral`      | ✅                        | ✅                              | ✅                             |      ✅                          | ✅                          | ✅                               | ✅                               | ✅                          | ✅                         | ✅                          | ✅                              | ✅                   | ✅                              |
| `switzerlandnorth`   | ✅                        | ✅                              |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `uksouth`            | ✅                        | ✅                              |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `westeurope`         |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | -                   | ✅                              |
| `westus`             |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| `westus3`            |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |

# [Global provisioned managed](#tab/ptu-global)

| Region     | gpt-5, 2025-08-07 | gpt-5-mini, 2025-08-07 | gpt-4.1, 2025-04-14 | gpt-4.1-nano, 2025-04-14 | gpt-4.1-mini, 2025-04-14 | gpt-4o, 2024-05-13 | gpt-4o, 2024-08-06 | gpt-4o, 2024-11-20 | gpt-4o-mini, 2024-07-18 |
|:-------------------|:--------------------------:|:------------------------------:|:---------------------------:|:--------------------------------:|:--------------------------------:|:--------------------------:|:--------------------------:|:--------------------------:|:-------------------------------:|
| `australiaeast`      | ✅                        | ✅                             | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `brazilsouth`        | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `canadaeast`         | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `eastus`             | ✅                        |  ✅                            | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `eastus2`            | ✅                        | ✅                             | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `francecentral`      | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `germanywestcentral` | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `italynorth`         | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `japaneast`          | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `norwayeast`         | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `polandcentral`      | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `southafricanorth`   | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `southcentralus`     | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `southeastasia`      | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `southindia`         | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `swedencentral`      | ✅                        |  ✅                            | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `switzerlandnorth`   | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `uksouth`            | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `westeurope`         | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `westus`             | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| `westus3`            | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |

# [Standard](#tab/standard)

| Region           | o3-deep-research, 2025-06-26 | gpt-4o, 2024-05-13 | gpt-4o, 2024-08-06 | gpt-4o, 2024-11-20 | gpt-4o-mini, 2024-07-18 | gpt-4, 0613 | gpt-4, turbo-2024-04-09 | gpt-4-32k, 0613 | gpt-35-turbo, 1106 | gpt-35-turbo, 0125 |
|------------------|------------------------------|--------------------|--------------------|--------------------|-------------------------|-------------|-------------------------|-----------------|--------------------|--------------------|
| `australiaeast`    | -                            | -                  | -                  | ✅                  | -                       | ✅           | -                       | ✅               | ✅                  | ✅                  |  
| `canadaeast`       | -                            | -                  | -                  | ✅                  | -                       | ✅           | -                       | ✅               | ✅                  | ✅                  |  
| `eastus`           | -                            | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | -               | -                  | ✅                  |
| `eastus2`          | -                            | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | -               | -                  | ✅                  |
| `francecentral`    | -                            | -                  | -                  | ✅                  | -                       | ✅           | -                       | ✅               | ✅                  | ✅                  |
| `japaneast`        | -                            | -                  | -                  | ✅                  | -                       | -           | -                       | -               | -                  | ✅                  |
| `norwayeast`       | ✅                            | -                  | -                  | ✅                  | -                       | -           | -                       | -               | -                  | -                  |  
| `southcentralus`   | ✅                           | ✅                | ✅                 | ✅                  | ✅                     | ✅          | ✅                      | -             | -                  | ✅                |
| `southindia`       | -                            | -                  | -                  | ✅                  | -                       | -           | -                       | -               | ✅                  | ✅                  |  
| `swedencentral`    | -                            | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| `switzerlandnorth` | -                            | -                  | -                  | ✅                  | -                       | ✅           | -                       | ✅               | -                  | ✅                  |  
| `uksouth`          | -                            | -                  | -                  | ✅                  | -                       | -           | -                       | -               | ✅                  | ✅                  |  
| `westeurope`       | -                            | -                  | -                  | -                    | -                       | -            | -                      | -              | -                     | ✅                  |  
| `westus`           | ✅                            | ✅                  | ✅                  | ✅                  | ✅                       | -           | ✅                       | -               | ✅                  | ✅                  |
| `westus3`          | -                            | ✅                  | ✅                  | ✅                  | ✅                       | -           | ✅                       | -               | -                  | ✅                  |

# [Provisioned managed](#tab/ptu)

| Region           | gpt-5, 2025-08-07 | gpt-5-mini, 2025-08-07 | gpt-4.1, 2025-04-14 | gpt-4.1-nano, 2025-04-14 | gpt-4.1-mini, 2025-04-14 | gpt-4o, 2024-05-13 | gpt-4o, 2024-08-06 | gpt-4o, 2024-11-20 | gpt-4o-mini, 2024-07-18 | gpt-4, 0613 | gpt-4, turbo-2024-04-09 | gpt-4-32k, 0613 | gpt-35-turbo, 1106 | gpt-35-turbo, 0125 |
|------------------|-------------------|------------------------|---------------------|--------------------------|--------------------------|--------------------|--------------------|--------------------|--------------------------|-----------|-----------------------|-----------------|--------------------|--------------------|
| `australiaeast`    | -                | -                      | ✅                   | -                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| `brazilsouth`      | -                | -                      | -                   | -                        | -                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | -                  |
| `canadaeast`       | -                | -                      | -                   | -                        | -                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | -                  |  
| `eastus`           | ✅                | -                    | ✅                   | ✅                        |✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |
| `eastus2`          | ✅                | ✅                    | ✅                   | ✅                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |
| `francecentral`    | -                | -                      | -                   | -                        | -                        | ✅                  | ✅                  | -                  | ✅                       | ✅           | -                       | ✅               | -                  | ✅                  |
| `germanywestcentral`| -               | -                      | -                   | -                        | -                        | ✅                  | ✅                  | ✅                  |  -                      |✅             | -                      | ✅                | ✅                | -              |
| `japaneast`        | -                | -                      | ✅                 | -                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | -           | ✅                       | -               | -                  | ✅                  |
| `southafricanorth` | -                | -                      | -                   | -                        | -                        | ✅                  | -                   | -                    | -                        | ✅          | ✅                      | ✅               | ✅                 | -                     |
| `southcentralus`   | ✅                | -                      | ✅                   | ✅                     | ✅                        | -                   | ✅                  | ✅                  | ✅                       | ✅          | ✅                      | ✅                 | ✅                | ✅                  |
| `southeastasia`    | -                | -                      | -                   | -                        | -                        | -                   | ✅                  | ✅                  | ✅                       | -           | -                       | -               | -                  | -                  |
| `southindia`       | -                | -                      | -                   | -                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | -                       | ✅               | ✅                  | ✅                  |  
| `swedencentral`    | -                | -                    | ✅                  | ✅                      | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| `switzerlandnorth` | -                | -                      | -                   | -                        | -                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| `uksouth`          | -                | -                      | ✅                  | -                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| `westeurope`       | -                | -                      | -                   | -                        | -                        | -                   | -                    | ✅                  | -                        | -             | -                         | -                | -                   | -                    |
| `westus`           | ✅                | -                      | ✅                   | ✅                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |
| `westus3`          | ✅                | -                    | ✅                   | ✅                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |

---

## Other model collections

The following lists of Foundry Models are also available for your agents to use.

[!INCLUDE [agent-service-models-support-list](../includes/agent-service-models-support-list.md)]

## View all agent-supported models in the Foundry portal

[!INCLUDE [agent-service-view-models-in portal](../includes/agent-service-view-models-in-portal.md)]

## Related content

- [Create a new agent](../quickstart.md)
