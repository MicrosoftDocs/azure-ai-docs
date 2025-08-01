---
title: Supported models in Azure AI Foundry Agent Service
titleSuffix: Azure AI Foundry
description: Learn about the models you can use with Azure AI Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 07/14/2025
ms.custom: azure-ai-agents, references_regions
---

# Models supported by Azure AI Foundry Agent Service

Agents are powered by a diverse set of models with different capabilities and price points. Model availability varies by region and cloud. Certain tools and capabilities require the latest models. The following models are available in the REST API and SDKs. 

## Azure OpenAI models

Azure OpenAI provides customers with choices on the hosting structure that fits their business and usage patterns. The service offers two main types of deployment: 

- **Standard** is offered with a global deployment option, routing traffic globally to provide higher throughput.
- **Provisioned** is also offered with a global deployment option, allowing customers to purchase and deploy provisioned throughput units across Azure global infrastructure.

All deployments can perform the exact same inference operations, however the billing, scale, and performance are substantially different. To learn more about Azure OpenAI deployment types see [deployment types guide](../../openai/how-to/deployment-types.md).

Azure AI Foundry Agent Service supports the following Azure OpenAI models in the listed regions.

> [!NOTE]
> * The following table is for serverless API deployment availability. For information on Provisioned Throughput Unit (PTU) availability, see [provisioned throughput](../../openai/concepts/provisioned-throughput.md) in the Azure OpenAI documentation. `GlobalStandard` customers also have access to [global standard models](../../openai/concepts/models.md#global-standard-model-availability). 
> * [Hub based projects](../../what-is-azure-ai-foundry.md#project-types) are limited to the following models: gpt-4o, gpt-4o-mini, gpt-4, gpt-35-turbo

| REGION           | o3-deep-research, 2025-06-26 | gpt-4o, 2024-05-13 | gpt-4o, 2024-08-06 | gpt-4o, 2024-11-20 | gpt-4o-mini, 2024-07-18 | gpt-4, 0613 | gpt-4, turbo-2024-04-09 | gpt-4-32k, 0613 | gpt-35-turbo, 1106 | gpt-35-turbo, 0125 |
|------------------|------------------------------|--------------------|--------------------|--------------------|-------------------------|-------------|-------------------------|-----------------|--------------------|--------------------|
| australiaeast    |                              |                    |                    | X                  |                         | X           |                         | X               | X                  | X                  |  
| canadaeast       |                              |                    |                    | X                  |                         | X           |                         | X               | X                  | X                  |  
| eastus           |                              | X                  | X                  | X                  | X                       | X           | X                       |                 |                    | X                  |
| eastus2          |                              | X                  | X                  | X                  | X                       | X           | X                       |                 |                    | X                  |
| francecentral    |                              |                    |                    | X                  |                         | X           |                         | X               | X                  | X                  |
| japaneast        |                              |                    |                    | X                  |                         |             |                         |                 |                    | X                  |
| norwayeast       | X                            |                    |                    | X                  |                         |             |                         |                 |                    |                    |  
| southindia       |                              |                    |                    | X                  |                         |             |                         |                 | X                  |                    |  
| swedencentral    |                              | X                  | X                  | X                  | X                       | X           | X                       | X               | X                  | X                  |  
| switzerlandnorth |                              |                    |                    | X                  |                         | X           |                         | X               |                    | X                  |  
| uksouth          |                              |                    |                    | X                  |                         |             |                         |                 | X                  | X                  |  
| westus           | X                            | X                  | X                  | X                  | X                       |             | X                       |                 | X                  |                    |
| westus3          |                              | X                  | X                  | X                  | X                       |             | X                       |                 |                    |                    |


## Next steps

[Create a new Agent project](../quickstart.md)
