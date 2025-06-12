---
title: Supported models in Azure AI Foundry Agent Service
titleSuffix: Azure AI Foundry
description: Learn about the models you can use with Azure AI Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 06/03/2025
ms.custom: azure-ai-agents
---

# Models supported by Azure AI Foundry Agent Service

Agents are powered by a diverse set of models with different capabilities and price points. Model availability varies by region and cloud. Certain tools and capabilities require the latest models. The following models are available in the REST API and SDKs. 

## Azure OpenAI models

Azure OpenAI provides customers with choices on the hosting structure that fits their business and usage patterns. The service offers two main types of deployment: 

- **Standard** is offered with a global deployment option, routing traffic globally to provide higher throughput.
- **Provisioned** is also offered with a global deployment option, allowing customers to purchase and deploy provisioned throughput units across Azure global infrastructure.

All deployments can perform the exact same inference operations, however the billing, scale, and performance are substantially different. To learn more about Azure OpenAI deployment types see [deployment types guide](/azure/ai-services/agents/ai-services/openai/how-to/deployment-types).

Azure AI Foundry Agent Service supports the following Azure OpenAI models in the listed regions.

> [!NOTE]
> * The following table is for standard deployment availability. For information on Provisioned Throughput Unit (PTU) availability, see [provisioned throughput](/azure/ai-services/agents/ai-services/openai/concepts/provisioned-throughput) in the Azure OpenAI documentation. `GlobalStandard` customers also have access to [global standard models](/azure/ai-services/agents/ai-services/openai/concepts/modelsglobal-standard-model-availability). 
> * [Hub based projects](/azure/ai-services/agents/ai-foundry/what-is-azure-ai-foundryproject-types) are limited to the following models: gpt-4o, gpt-4o-mini, gpt-4, gpt-35-turbo

| REGION           | o1 | o3-mini | gpt-4.1, 2025-04-14 | gpt-4.1-mini, 2025-04-14 | gpt-4.1-nano, 2025-04-14 | gpt-4o, 2024-05-13 | gpt-4o, 2024-08-06 | gpt-4o, 2024-11-20 | gpt-4o-mini, 2024-07-18 | gpt-4, 0613 | gpt-4, turbo-2024-04-09 | gpt-4-32k, 0613 | gpt-35-turbo, 1106 | gpt-35-turbo, 0125 |
|------------------|----|---------|---------------------|--------------------------|--------------------------|--------------------|--------------------|--------------------|-------------------------|-------------|-------------------------|-----------------|--------------------|--------------------|
| australiaeast    |    |         |                     |                          |                          |                    |                    | X                  |                         | X           |                         | X               | X                  | X                  |
| canadaeast       |    |         |                     |                          |                          |                    |                    | X                  |                         | X           |                         | X               | X                  | X                  |
| eastus           |    |         |                     |                          |                          | X                  | X                  | X                  | X                       | X           | X                       |                 |                    | X                  |
| eastus2          |    |         |                     |                          |                          | X                  | X                  | X                  | X                       | X           | X                       |                 |                    | X                  |
| francecentral    |    |         |                     |                          |                          |                    |                    | X                  |                         | X           |                         | X               | X                  | X                  |
| japaneast        |    |         |                     |                          |                          |                    |                    | X                  |                         |             |                         |                 |                    | X                  |
| koreacentral     |    |         |                     |                          |                          |                    |                    |                    |                         |             |                         |                 |                    |                    |
| norwayeast       |    |         |                     |                          |                          |                    |                    | X                  |                         |             |                         |                 |                    |                    |
| polandcentral    |    |         |                     |                          |                          |                    |                    |                    |                         |             |                         |                 |                    |                    |
| southindia       |    |         |                     |                          |                          |                    |                    | X                  |                         |             |                         |                 | X                  |                    |
| swedencentral    |    |         |                     |                          |                          | X                  | X                  | X                  | X                       | X           | X                       | X               | X                  | X                  |
| switzerlandnorth |    |         |                     |                          |                          |                    |                    | X                  |                         | X           |                         | X               |                    | X                  |
| uaenorth         |    |         |                     |                          |                          |                    |                    |                    |                         |             |                         |                 |                    |                    |
| uksouth          |    |         |                     |                          |                          |                    |                    | X                  |                         |             |                         |                 | X                  | X                  |
| westus           |    |         |                     |                          |                          | X                  | X                  | X                  | X                       |             | X                       |                 | X                  |                    |
| westus3          |    |         |                     |                          |                          | X                  | X                  | X                  | X                       |             | X                       |                 |                    |                    |

## Non-Microsoft models

The Azure AI Foundry Agent Service also supports the following models from the Azure AI Foundry model catalog.

* Meta-Llama-405B-Instruct

To use these models, you can use [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) to make a deployment, and then reference the deployment name in your agent. For example:

```python
agent = project_client.agents.create_agent( model="llama-3", name="my-agent", instructions="You are a helpful agent" ) 
```
## Azure AI Foundry models

### Models with tool-calling 

To best support agentic scenarios, we recommend using models that support tool-calling. The Azure AI Foundry Agent Service currently supports all agent-compatible models from the Azure AI Foundry model catalog. 

To use these models, use the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) to make a model deployment, then reference the deployment name in your agent. For example: 

`agent = project_client.agents.create_agent( model="llama-3", name="my-agent", instructions="You are a helpful agent")`

> [!NOTE]
> This option should only be used for open-source models (for example, Cepstral, Mistral, Llama) and not for OpenAI models, which are natively supported in the service. This option should also only be used for models that support tool-calling. 

### Models without tool-calling 

Though tool-calling support is a core capability for agentic scenarios, we now provide the ability to use models that don’t support tool-calling in our API and SDK. This option can be helpful when you have specific use-cases that don’t require tool-calling. 

The following steps will allow you to utilize any chat-completion model that is available through a [serverless API](/azure/ai-foundry/how-to/model-catalog-overview): 

 

1. Deploy your desired model through serverless API. Model will show up on your **Models + Endpoints** page. 

1. Click on model name to see model details, where you'll find your model's target URI and key. 

1. Create a new Serverless connection on **Connected Resources** page, using the target URI and key. 

The model can now be referenced in your code (`Target URI` + `@` + `Model Name`), for example: 

`Model=https://Phi-4-mejco.eastus.models.ai.azure.com/@Phi-4-mejco`

## Next steps

[Create a new Agent project](../quickstart.md)
