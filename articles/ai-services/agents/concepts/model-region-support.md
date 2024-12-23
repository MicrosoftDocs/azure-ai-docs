---
title: Supported models in Azure AI Agent Service
titleSuffix: Azure AI services
description: Learn about the models you can use with Azure AI Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 12/11/2024
ms.custom: azure-ai-agents
---

# Models supported by Azure AI Agent Service

Agents are powered by a diverse set of models with different capabilities and price points. Model availability varies by region and cloud. Certain tools and capabilities require the latest models. The following models are available in the available SDKs. The following table is for pay-as-you-go. For information on Provisioned Throughput Unit (PTU) availability, see [provisioned throughput](../../openai/concepts/provisioned-throughput.md) in the Azure OpenAI documentation. You can use [global standard models](../../openai/concepts/models.md#global-standard-model-availability) if they're supported in the regions listed here. 

## Azure OpenAI models

Azure AI Agent Service supports the same models as the chat completions API in Azure OpenAI, in the following regions.

| **Region**    | **gpt-4o**, **2024-05-13** | **gpt-4o**, **2024-08-06** | **gpt-4o-mini**, **2024-07-18** | **gpt-4**, **0613** | **gpt-4**, **1106-Preview** | **gpt-4**, **0125-Preview** | **gpt-4**, **vision-preview** | **gpt-4**, **turbo-2024-04-09** | **gpt-4-32k**, **0613** | **gpt-35-turbo**, **0613** | **gpt-35-turbo**, **1106** | **gpt-35-turbo**, **0125** | **gpt-35-turbo-16k**, **0613** |
|:--------------|:--------------------------:|:--------------------------:|:-------------------------------:|:-------------------:|:---------------------------:|:---------------------------:|:-----------------------------:|:-------------------------------:|:--------------------------:|:--------------------------:|:--------------------------:|:------------------------------:|
| eastus        | ✅                         | ✅                          | ✅                            | -                   | -                           | ✅                          | -                             | ✅                              | -                       | ✅                          | -                          | ✅                         | ✅                              |
| francecentral | -                          | -                          | -                               | ✅                  | ✅                           | -                           | -                             | -                               | ✅ | ✅                         | ✅                          | -                          | ✅                             |
| japaneast     | -                          | -                          | -                               | -                   | -                           | -                           | ✅                            | -                               | -                      | ✅                         | -                          | ✅                         | ✅                              |
| uksouth       | -                          | -                          | -                               | -                   | ✅                          | ✅                           | -                             | -                               | -                       | ✅                          | ✅                         | ✅                          | ✅                             |
| westus        | ✅                         | ✅                          | ✅                            | -                   | ✅                          | -                           | ✅                            | ✅                               | - | -                          | ✅                         | ✅                          | -                              |


## More models

The Azure AI Agent Service also supports the following models from the Azure AI Foundry model catalog.

* Llama 3.1-70B-instruct
* Mistral-large-2407
* Cohere command R+

To use these models, you can use Azure AI Foundry portal to make a deployment, and then reference it in your agent. 

1. Go to the [Azure AI Foundry portal](https://ai.azure.com/) and select **Model catalog** in the left navigation menu, and scroll down to **Meta-Llama-3-70B-Instruct**. You can also find and use one of the models listed previously.  

1. Select **Deploy**. 

1. In the Deployment options screen that appears, select **Serverless API** with Azure AI Content Safety. 

    :::image type="content" source="../media/llama/llama-deployment.png" alt-text="An image of the llama model project selection screen.":::
 
1. Select your project and then select **Subscribe and deploy**. 

    :::image type="content" source="../media/llama/llama-deployment-2.png" alt-text="An image of the llama model deployment screen.":::

1. Add the serverless connection to your hub/project. The deployment name you choose is the one that you reference in your code.  

1. When calling agent creation API, set the `models` parameter to your deployment name. For example:

    # [Python](#tab/python)

    ```python
    agent = project_client.agents.create_agent( model="llama-3", name="my-agent", instructions="You are a helpful agent" ) 
    ```

    # [C#](#tab/csharp)

    ```csharp
    Response<Agent> agentResponse = await client.CreateAgentAsync(
            model: "llama-3",
            name: "My agent",
            instructions: "You are a helpful agent"
    ```
    ---


## Next steps

[Create a new Agent project](../quickstart.md)