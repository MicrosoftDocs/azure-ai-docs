---
title: Supported models in Azure AI Foundry Agent Service
titleSuffix: Azure AI Foundry
description: Learn about the models you can use with Azure AI Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 08/14/2025
ms.custom: azure-ai-agents, references_regions
---

# Models supported by Azure AI Foundry Agent Service

Agents are powered by a diverse set of Azure OpenAI models with different capabilities and price points. Model availability varies by region and cloud. Certain tools and capabilities require the latest models. The following models are available in the REST API and SDKs. 

- **Standard** is offered with a global deployment option, routing traffic globally to provide higher throughput.
- **Provisioned** is also offered with a global deployment option, allowing customers to purchase and deploy provisioned throughput units across Azure global infrastructure.

All deployments can perform the exact same inference operations, however the billing, scale, and performance are substantially different. To learn more about Azure OpenAI deployment types see [deployment types guide](../../openai/how-to/deployment-types.md).

## Available models

Azure AI Foundry Agent Service supports the following Azure OpenAI models in the listed regions.

> [!NOTE]
> * [Hub-based projects](../../what-is-azure-ai-foundry.md#project-types) are limited to the following models: gpt-4o, gpt-4o-mini, gpt-4, gpt-35-turbo
> * For information on class A subnet support, see the setup guide on [GitHub](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/15-private-network-standard-agent-setup).
> * The [file search tool](../how-to/tools/file-search.md) is currently unavailable in the following regions:
>     * Italy north
>     * Brazil south 

# [Global standard](#tab/global-standard)


| **Region**       | **gpt-4o**, **2024-05-13** | **gpt-4o**, **2024-08-06** | **gpt-4o**, **2024-11-20** | **gpt-4o-mini**, **2024-07-18** | **gpt-4**, **0613** | **gpt-4**, **turbo-2024-04-09** |
|:-----------------|:--------------------------:|:--------------------------:|:--------------------------:|:-------------------------------:|:-------------------:|:-------------------------------:|
| australiaeast    | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| brazilsouth      | ✅                         | ✅                         | ✅                         | ✅                              | -                    | ✅                               |
| canadaeast       | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| eastus           | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| eastus2          | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| francecentral    | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| germanywestcentral| ✅                        | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| italynorth       |  -                          |  -                         | ✅                         | ✅                              |  -                   | -                               |
| japaneast        | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| norwayeast       | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| southcentralus   | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| southindia       | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| swedencentral    | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| switzerlandnorth | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| southafricanorth | ✅                         | ✅                         | ✅                         | ✅                              | -                    | ✅                              |
| uksouth          | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| westeurope       | ✅                         | ✅                         | ✅                         | ✅                              | -                   |  ✅                              |
| westus           | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |
| westus3          | ✅                         | ✅                         | ✅                         | ✅                              | ✅                  | ✅                              |

# [Global provisioned managed](#tab/ptu-global)

| **Region**     | **gpt-4o**, **2024-05-13** | **gpt-4o**, **2024-08-06** | **gpt-4o**, **2024-11-20** | **gpt-4o-mini**, **2024-07-18** |
|:-------------------|:--------------------------:|:--------------------------:|:--------------------------:|:-------------------------------:|
| australiaeast      | ✅                       | ✅                       | ✅                       | ✅                            |
| brazilsouth        | ✅                       | ✅                       | ✅                       | ✅                            |
| canadaeast         | ✅                       | ✅                       | ✅                       | ✅                            |
| eastus             | ✅                       | ✅                       | ✅                       | ✅                            |
| eastus2            | ✅                       | ✅                       | ✅                       | ✅                            |
| francecentral      | ✅                       | ✅                       | ✅                       | ✅                            |
| southafricanorth   | ✅                       | ✅                       | ✅                       | ✅                            |
| germanywestcentral|  ✅                       | ✅                       | ✅                       | ✅                            |
| italynorth         | ✅                       | ✅                       | ✅                       | ✅                            |
| japaneast          | ✅                       | ✅                       | ✅                       | ✅                            |
| southcentralus     | ✅                       | ✅                       | ✅                       | ✅                            |
| southeastasia      | ✅                       | ✅                       | ✅                       | ✅                            |
| southindia         | ✅                       | ✅                       | ✅                       | ✅                            |
| swedencentral      | ✅                       | ✅                       | ✅                       | ✅                            |
| switzerlandnorth   | ✅                       | ✅                       | ✅                       | ✅                            |
| uksouth            | ✅                       | ✅                       | ✅                       | ✅                            |
| westeurope         | ✅                       | ✅                       | ✅                       | ✅                            |
| westus             | ✅                       | ✅                       | ✅                       | ✅                            |
| westus3            | ✅                       | ✅                       | ✅                       | ✅                            |

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

| REGION           | gpt-4o, 2024-05-13 | gpt-4o, 2024-08-06 | gpt-4o, 2024-11-20 | gpt-4o-mini, 2024-07-18 | gpt-4, 0613 | gpt-4, turbo-2024-04-09 | gpt-4-32k, 0613 | gpt-35-turbo, 1106 | gpt-35-turbo, 0125 |
|------------------|--------------------|--------------------|--------------------|-------------------------|-------------|-------------------------|-----------------|--------------------|--------------------|
| australiaeast    | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| brazilsouth      | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | -                  |
| canadaeast       | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | -                  |  
| eastus           | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |
| eastus2          | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |
| francecentral    | ✅                  | ✅                  | -                  | ✅                       | ✅           | -                       | ✅               | -                  | ✅                  |
| germanywestcentral|  ✅                | ✅                  | ✅                  |  -                      |✅             | -                      | ✅                | ✅                |              |
| japaneast        | ✅                  | ✅                  | ✅                  | ✅                       | -           | ✅                       | -               | -                  | ✅                  |
| southafricanorth | ✅                  | -                   | -                    | -                        | ✅          | ✅                      | ✅               | ✅                 | -                     |
| southcentralus   | -                   | ✅                  | ✅                  | ✅                       | ✅          | ✅                      | ✅                 | ✅                | ✅                  | 
| southeastasia    | -                   | ✅                  | ✅                  | ✅                       | -           | -                       | -               | -                  | -                  |                    
| southindia       | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | -                       | ✅               | ✅                  | ✅                  |  
| swedencentral    | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| switzerlandnorth | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| uksouth          | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |  
| westus           | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |
| westus3          | ✅                  | ✅                  | ✅                  | ✅                       | ✅           | ✅                       | ✅               | ✅                  | ✅                  |

---

## Next steps

[Create a new Agent project](../quickstart.md)