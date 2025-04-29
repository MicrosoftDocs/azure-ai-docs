---
title: Supported models in Azure AI Foundry Agent Service
titleSuffix: Azure AI services
description: Learn about the models you can use with Azure AI Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 04/15/2025
ms.custom: azure-ai-agents
---

# Models supported by Azure AI Foundry Agent Service

Agents are powered by a diverse set of models with different capabilities and price points. Model availability varies by region and cloud. Certain tools and capabilities require the latest models. The following models are available in the REST API and SDKs. 

## Azure OpenAI models

Azure OpenAI provides customers with choices on the hosting structure that fits their business and usage patterns. The service offers two main types of deployment: 

- **Standard** is offered with a global deployment option, routing traffic globally to provide higher throughput.
- **Provisioned** is also offered with a global deployment option, allowing customers to purchase and deploy provisioned throughput units across Azure global infrastructure.

All deployments can perform the exact same inference operations, however the billing, scale, and performance are substantially different. To learn more about Azure OpenAI deployment types see our [deployment types guide](../../openai/how-to/deployment-types.md).

Azure AI Foundry Agent Service supports the following Azure OpenAI models in the listed regions.

> [!NOTE]
> The following table is for pay-as-you-go. For information on Provisioned Throughput Unit (PTU) availability, see [provisioned throughput](../../openai/concepts/provisioned-throughput.md) in the Azure OpenAI documentation. `GlobalStandard` customers also have access to [global standard models](../../openai/concepts/models.md#global-standard-model-availability). 

| **Region**    | **gpt-4o**, **2024-11-20** | **gpt-4o**, **2024-05-13** | **gpt-4o**, **2024-08-06** | **gpt-4o-mini**, **2024-07-18** | **gpt-4**, **0613** | **gpt-4**, **1106-Preview** | **gpt-4**, **0125-Preview** | **gpt-4**, **turbo-2024-04-09** | **gpt-4-32k**, **0613** | **gpt-35-turbo**, **0613** | **gpt-35-turbo**, **1106** | **gpt-35-turbo**, **0125** | **gpt-35-turbo-16k**, **0613** |
|:--------------|:--------------------------:|:--------------------------:|:--------------------------:|:-------------------------------:|:-------------------:|:---------------------------:|:---------------------------:|:-------------------------------:|:--------------------------:|:--------------------------:|:--------------------------:|:------------------------------:|
| australiaeast  |  | - | - | - | ✅ | ✅ | -| - | ✅ | ✅ | ✅ | ✅ | ✅ |
| eastus       | | ✅                         | ✅                          | ✅                            | -                   | -                           | ✅                          | ✅                              | -                       | ✅                          | -                          | ✅                         | ✅                              |
| eastus2   | | ✅ | ✅ | ✅ | -  | ✅ | - | ✅ | - | ✅ | - | ✅ | ✅ | 
| francecentral | | -                          | -                          | -                               | ✅                  | ✅                           | -                           | -                               | ✅ | ✅                         | ✅                          | -                          | ✅                             |
| japaneast    | ✅  | -                          | -                          | -                               | -                   | -                           | -                           | -                               | -                      | ✅                         | -                          | ✅                         | ✅                              |
| norwayeast   | |-  |  - |  - | -  | ✅ | -  |-  | -  | -  | -  | -  | - |
| polandcentral  |  - | -  | - | -  | - | - | - | - | - | - | - | - | - |
| southindia   | | - | - | - | - | ✅ | - | - | - | - | ✅ | ✅ | - |
| swedencentral  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ | ✅ | ✅ | ✅ | - | ✅ |
| switzerlandnorth  |  - | -  | - | -  | ✅ | - | - | - | ✅ | - | - | ✅ | ✅ |
| uaenorth   | | - | - | - | - | - | - | - | - | - | - | - | - |
| uksouth     |  | -                          | -                          | -                               | -                   | ✅                          | ✅                           | -                               | -                       | ✅                          | ✅                         | ✅                          | ✅                             |
| westus      |  | ✅                         | ✅                          | ✅                            | -                   | ✅                          | -                           | ✅                               | - | -                          | ✅                         | ✅                          | -                              |
| westus3  |  | ✅ | ✅ | ✅ | - | ✅ | - | ✅ | - | - | - | ✅ | - |


## Non-Microsoft models

The Azure AI Foundry Agent Service also supports the following models from the Azure AI Foundry model catalog.

* Meta-Llama-405B-Instruct
* Cohere-command-r-plus
* Cohere-command-r

To use these models, you can use [Azure AI Foundry portal](https://ai.azure.com/) to make a deployment, and then reference the deployment name in your agent. For example:

```python
agent = project_client.agents.create_agent( model="llama-3", name="my-agent", instructions="You are a helpful agent" ) 
```

## Next steps

[Create a new Agent project](../quickstart.md)
