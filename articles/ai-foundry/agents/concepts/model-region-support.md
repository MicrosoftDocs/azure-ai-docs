---
title: Supported models in Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn about the models you can use with Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: conceptual
ms.date: 11/14/2025
ms.custom: azure-ai-agents, references_regions
monikerRange: 'foundry-classic || foundry'
---

# Models supported by Foundry Agent Service

In this article, you learn about the diverse set of Azure OpenAI models that power Agents in Microsoft Foundry Service. These models have different capabilities and price points.

> [!NOTE]
> If you'd like to see a selection of Foundry Models sold directly by Azure, along with their capabilities, see [Foundry Models sold directly by Azure](../../foundry-models/concepts/models-sold-directly-by-azure.md). 
Model availability varies by region and cloud. Certain tools and capabilities require the latest models. The following models are available in the REST API and SDKs. 

- **Standard** is offered with a global deployment option, routing traffic globally to provide higher throughput.
- **Provisioned** is also offered with a global deployment option, allowing customers to purchase and deploy provisioned throughput units across Azure global infrastructure.

All deployments can perform the exact same inference operations, however the billing, scale, and performance are substantially different. To learn more about Azure OpenAI deployment types see [deployment types guide](../../foundry-models/concepts/deployment-types.md).

## Available models

Foundry Agent Service supports the following Azure OpenAI models in the listed regions.

::: moniker range="foundry-classic"
> [!NOTE]
> * [Hub-based projects](../../what-is-azure-ai-foundry.md#types-of-projects) are limited to the following models: gpt-4o, gpt-4o-mini, gpt-4, gpt-35-turbo
> * [Spillover traffic management](../../openai/how-to/spillover-traffic-management.md) for [provisioned throughput](../../openai/concepts/provisioned-throughput.md) is compatible with agents
> * For information on class A subnet support, see the setup guide on [GitHub](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/15-private-network-standard-agent-setup).
> * The [file search tool](../how-to/tools/file-search.md) is currently unavailable in the following regions:
>     * Italy north
>     * Brazil south 
> * The gpt-5 models can only use the [code interpreter](../how-to/tools/code-interpreter.md) and [file search](../how-to/tools/file-search.md) tools 
>    * [Registration](https://aka.ms/openai/gpt-5/2025-08-07) is required to use the gpt-5 models. Access will be granted according to Microsoft's eligibility criteria.
::: moniker-end

::: moniker range="foundry"
> [!NOTE]
> * [Spillover traffic management](../../openai/how-to/spillover-traffic-management.md) for [provisioned throughput](../../openai/concepts/provisioned-throughput.md) is compatible with agents
> * For information on class A subnet support, see the setup guide on [GitHub](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/15-private-network-standard-agent-setup).
> * The [file search tool](../how-to/tools/file-search.md) is currently unavailable in the following regions:
>     * Italy north
>     * Brazil south 
> * The gpt-5 models are available for the [code interpreter](../how-to/tools/code-interpreter.md) and [file search](../how-to/tools/file-search.md) tools 
>    * [Registration](https://aka.ms/openai/gpt-5/2025-08-07) is required to use the gpt-5 models. Access will be granted according to Microsoft's eligibility criteria.
::: moniker-end

# [Global standard](#tab/global-standard)


| **Region**         | **gpt-5**, **2025-08-07** | **gpt-5-mini**, **2025-08-07** | **gpt-5-nano**, **2025-08-07** | **gpt-5-chat**, **2025-08-07** | **gpt-4.1**, **2025-04-14** | **gpt-4.1-nano**, **2025-04-14** | **gpt-4.1-mini**, **2025-04-14** | **gpt-4o**, **2024-05-13** | **gpt-4o**, **2024-08-06** | **gpt-4o**, **2024-11-20** | **gpt-4o-mini**, **2024-07-18** | **gpt-4**, **0613** | **gpt-4**, **turbo-2024-04-09** |
|:-------------------|:-------------------------:|:------------------------------:|:------------------------------:|:------------------------------:|:---------------------------:|:--------------------------------:|:--------------------------------:|:--------------------------:|:--------------------------:|:--------------------------:|:-------------------------------:|:-------------------:|:-------------------------------:|
| australiaeast      | ✅                        | ✅                              |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| brazilsouth        |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | -                   | ✅                              |
| canadaeast         |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| eastus             | ✅                        | ✅                              |                                |                                | ✅                          |                                | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| eastus2            | ✅                        | ✅                              | ✅                             |        ✅                        | ✅                          | ✅                               | ✅                               | ✅                          | ✅                         | ✅                          | ✅                              | ✅                   | ✅                              |
| francecentral      |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| germanywestcentral |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| italynorth         |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | -                          | -                          | ✅                         | ✅                               | -                   | -                               |
| japaneast          | ✅                        | ✅                              |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| norwayeast         |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| southafricanorth   |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | -                   | ✅                              |
| southcentralus     |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| southindia         | ✅                        | ✅                              |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| swedencentral      | ✅                        | ✅                              | ✅                             |      ✅                          | ✅                          | ✅                               | ✅                               | ✅                          | ✅                         | ✅                          | ✅                              | ✅                   | ✅                              |
| switzerlandnorth   | ✅                        | ✅                              |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| uksouth            | ✅                        | ✅                              |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| westeurope         |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | -                   | ✅                              |
| westus             |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |
| westus3            |                           |                                |                                |                                | ✅                          | ✅                               | ✅                               | ✅                         | ✅                          | ✅                         | ✅                               | ✅                  | ✅                               |

# [Global provisioned managed](#tab/ptu-global)

| **Region**     | **gpt-5**, **2025-08-07** | **gpt-5-mini**, **2025-08-07** | **gpt-4.1**, **2025-04-14** | **gpt-4.1-nano**, **2025-04-14** | **gpt-4.1-mini**, **2025-04-14** | **gpt-4o**, **2024-05-13** | **gpt-4o**, **2024-08-06** | **gpt-4o**, **2024-11-20** | **gpt-4o-mini**, **2024-07-18** |
|:-------------------|:--------------------------:|:------------------------------:|:---------------------------:|:--------------------------------:|:--------------------------------:|:--------------------------:|:--------------------------:|:--------------------------:|:-------------------------------:|
| australiaeast      | ✅                        | ✅                             | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| brazilsouth        | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| canadaeast         | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| eastus             | ✅                        |  ✅                            | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| eastus2            | ✅                        | ✅                             | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| francecentral      | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| germanywestcentral | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| italynorth         | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| japaneast          | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| norwayeast         | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| polandcentral      | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| southafricanorth   | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| southcentralus     | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| southeastasia      | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| southindia         | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| swedencentral      | ✅                        |  ✅                            | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| switzerlandnorth   | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| uksouth            | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| westeurope         | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| westus             | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |
| westus3            | ✅                        |                                | ✅                          | ✅                               | ✅                               | ✅                       | ✅                       | ✅                       | ✅                            |

# [Standard](#tab/standard)

| REGION           | o3-deep-research, 2025-06-26 | gpt-4o, 2024-05-13 | gpt-4o, 2024-08-06 | gpt-4o, 2024-11-20 | gpt-4o-mini, 2024-07-18 | gpt-4, 0613 | gpt-4, turbo-2024-04-09 | gpt-4-32k, 0613 | gpt-35-turbo, 1106 | gpt-35-turbo, 0125 |
|------------------|------------------------------|--------------------|--------------------|--------------------|-------------------------|-------------|-------------------------|-----------------|--------------------|--------------------|
| australiaeast    | -                            | -                  | -                  | ✅                  | -                       | ✅           | -                       | ✅               | ✅                  | ✅                  |  
| canadaeast       | -                            | -                  | -                  | ✅                  | -                       | ✅           | -                       | ✅               | ✅                  | ✅                  |  
| eastus           | -                            | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | -               | -                  | ✅                  |
| eastus2          | -                            | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | -               | -                  | ✅                  |
| francecentral    | -                            | -                  | -                  | ✅                  | -                       | ✅           | -                       | ✅               | ✅                  | ✅                  |
| japaneast        | -                            | -                  | -                  | ✅                  | -                       | -           | -                       | -               | -                  | ✅                  |
| norwayeast       | ✅                            | -                  | -                  | ✅                  | -                       | -           | -                       | -               | -                  | -                  |  
| southcentralus   | ✅                           | ✅                | ✅                 | ✅                  | ✅                     | ✅          | ✅                      | -             | -                  | ✅                |
| southindia       | -                            | -                  | -                  | ✅                  | -                       | -           | -                       | -               | ✅                  | ✅                  |  
| swedencentral    | -                            | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| switzerlandnorth | -                            | -                  | -                  | ✅                  | -                       | ✅           | -                       | ✅               | -                  | ✅                  |  
| uksouth          | -                            | -                  | -                  | ✅                  | -                       | -           | -                       | -               | ✅                  | ✅                  |  
| westeurope       | -                            | -                  | -                  | -                    | -                       | -            | -                      | -              | -                     | ✅                  |  
| westus           | ✅                            | ✅                  | ✅                  | ✅                  | ✅                       | -           | ✅                       | -               | ✅                  | ✅                  |
| westus3          | -                            | ✅                  | ✅                  | ✅                  | ✅                       | -           | ✅                       | -               | -                  | ✅                  |


# [Provisioned managed](#tab/ptu)

| REGION           | gpt-5, 2025-08-07 | gpt-5-mini, 2025-08-07 | gpt-4.1, 2025-04-14 | gpt-4.1-nano, 2025-04-14 | gpt-4.1-mini, 2025-04-14 | gpt-4o, 2024-05-13 | gpt-4o, 2024-08-06 | gpt-4o, 2024-11-20 | gpt-4o-mini, 2024-07-18 | gpt-4, 0613 | gpt-4, turbo-2024-04-09 | gpt-4-32k, 0613 | gpt-35-turbo, 1106 | gpt-35-turbo, 0125 |
|------------------|-------------------|------------------------|---------------------|--------------------------|--------------------------|--------------------|--------------------|--------------------|--------------------------|-----------|-----------------------|-----------------|--------------------|--------------------|
| australiaeast    | -                | -                      | ✅                   | -                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| brazilsouth      | -                | -                      | -                   | -                        | -                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | -                  |
| canadaeast       | -                | -                      | -                   | -                        | -                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | -                  |  
| eastus           | ✅                | -                    | ✅                   | ✅                        |✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |
| eastus2          | ✅                | ✅                    | ✅                   | ✅                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |
| francecentral    | -                | -                      | -                   | -                        | -                        | ✅                  | ✅                  | -                  | ✅                       | ✅           | -                       | ✅               | -                  | ✅                  |
| germanywestcentral| -               | -                      | -                   | -                        | -                        | ✅                  | ✅                  | ✅                  |  -                      |✅             | -                      | ✅                | ✅                | -              |
| japaneast        | -                | -                      | ✅                 | -                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | -           | ✅                       | -               | -                  | ✅                  |
| southafricanorth | -                | -                      | -                   | -                        | -                        | ✅                  | -                   | -                    | -                        | ✅          | ✅                      | ✅               | ✅                 | -                     |
| southcentralus   | ✅                | -                      | ✅                   | ✅                     | ✅                        | -                   | ✅                  | ✅                  | ✅                       | ✅          | ✅                      | ✅                 | ✅                | ✅                  | 
| southeastasia    | -                | -                      | -                   | -                        | -                        | -                   | ✅                  | ✅                  | ✅                       | -           | -                       | -               | -                  | -                  |                    
| southindia       | -                | -                      | -                   | -                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | -                       | ✅               | ✅                  | ✅                  |  
| swedencentral    | -                | -                    | ✅                  | ✅                      | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| switzerlandnorth | -                | -                      | -                   | -                        | -                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| uksouth          | -                | -                      | ✅                  | -                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| westeurope       | -                | -                      | -                   | -                        | -                        | -                   | -                    | ✅                  | -                        | -             | -                         | -                | -                   | -                    | 
| westus           | ✅                | -                      | ✅                   | ✅                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |
| westus3          | ✅                | -                    | ✅                   | ✅                        | ✅                        | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |

---

## Other model collections

The following [models sold directly by Azure](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-direct-others) are available for use by your agents:

- **MAI-DS-R1** — deterministic, precision-focused reasoning
- **grok-4** — frontier-scale reasoning for complex, multi-step problem solving 
- **grok-4-fast-reasoning** — accelerated agentic reasoning optimized for workflow automation
- **grok-4-fast-non-reasoning** — high-throughput, low-latency generation and system routing
- **grok-3** — strong reasoning for complex, system-level workflows
- **grok-3-mini** — lightweight model optimized for interactive, high-volume use cases 
- **Llama-3.3-70B-Instruct** — versatile model for enterprise Q&A, decision support, and system orchestration
- **Llama-4-Maverick-17B-128E-Instruct-FP8** — FP8-optimized model delivering fast, cost-efficient inference
- **DeepSeek-V3-0324** — multimodal understanding across text and images
- **DeepSeek-V3.1** — enhanced multimodal reasoning and grounded retrieval
- **DeepSeek-R1-0528** — advanced long-form and multi-step reasoning
- **gpt-oss-120b** — open-ecosystem model supporting transparency and reproducibility

The following [models from partners](../../foundry-models/concepts/models-from-partners.md) are available for use by your agents:

- **Claude-Opus-4-1** — frontier reasoning for the most complex problem-solving 
- **Claude-Sonnet-4-5** — balanced performance for multimodal and agentic workflows 
- **Claude-Haiku-4-5** — lightweight, high-speed generation for interactive scenarios

## Next step

[Create a new Agent project](../quickstart.md)
