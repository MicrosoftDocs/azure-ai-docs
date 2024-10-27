---
title: Use the Azure AI model inference endpoint
titleSuffix: Azure AI studio
description: Learn about to use the Azure AI model inference endpoint and how to configure it.
ms.service: azure-ai-studio
ms.topic: conceptual
author: sdgilley
manager: scottpolly
ms.date: 10/24/2024
ms.author: sgilley
ms.reviewer: fasantia
ms.custom: ignite-2024, github-universe-2024
---

# Use the Azure AI model inference endpoint

Azure AI inference service in Azure AI services allow customers to consume the most powerful models from flagship model providers using a single endpoint and credentials. This means that you can switch between models and consume them from your application without changing a single line of code.

The article explains how models are organized inside of the service and how to use the inference endpoint to invoke them.

## Deployments

Azure AI model inference service make models available using the **deployment** concept. **Deployments** are a way to give a model a name under certain configurations. Then, you can invoke such model configuration by indicating its name on your requests.

Deployments capture:

> [!div class="checklist"]
> * A model name
> * A model version
> * A provisioning/capacity type<sup>1</sup>
> * A content filtering configuration<sup>1</sup>
> * A rate limiting configuration<sup>1</sup>

<sup>1</sup> Configurations may vary depending on the model you have selected.

An Azure AI services resource can have as many model deployments as needed and they don't incur in cost unless inference is performed for those models. Deployments are Azure resources and hence they are subject to Azure policies.

To learn more about how to create deployments see [Add and configure model deployments](../how-to/create-model-deployments.md).

## Azure AI inference endpoint

The Azure AI inference endpoint allow customers to use a single endpoint with the same authentication and schema to generate inference for the deployed models in the resource. This endpoint follows the [Azure AI model inference API](../../reference/reference-model-inference-api.md) which is supported by all the models in Azure AI model inference service.

You can see the endpoint URL and credentials in the **Overview** section:

:::image type="content" source="../../media/ai-services/overview/overview-endpoint-and-key.png" alt-text="An screenshot showing how to get the URL and key associated with the resource." lightbox="../../media/ai-services/overview/overview-endpoint-and-key.png":::

### Routing

The inference endpoint routes requests to a given deployment by matching the parameter `name` inside of the request to the name of the deployment. This means that *deployments work as an alias of a given model under certain configurations*. This flexibility allow you to deploy a given model multiple times in the service but under different configurations if needed.

:::image type="content" source="../../media/ai-services/endpoint/endpoint-routing.png" alt-text="An illustration showing how routing works for a Meta-llama-3.2-8b-instruct model by indicating such name in the parameter 'model' inside of the payload request." lightbox="../../media/ai-services/endpoint/endpoint-routing.png":::

For example, if you create a deployment named `Mistral-large`, then such deployment can be invoked as:

[!INCLUDE [code-create-chat-completion](../../includes/ai-services/code-create-chat-completion.md)]

> [!TIP]
> Deployment routing is not case sensitive.

### Supported languages and SDKs

All models deployed in Azure AI model inference service support the [Azure AI model inference API](https://aka.ms/aistudio/modelinference) and its associated family of SDKs, which are available in the following languages:

| Language   | Documentation | Package | Examples |
|------------|---------|-----|-------|
| C#         | [Reference](https://aka.ms/azsdk/azure-ai-inference/csharp/reference) | [azure-ai-inference (NuGet)](https://www.nuget.org/packages/Azure.AI.Inference/) | [C# examples](https://aka.ms/azsdk/azure-ai-inference/csharp/samples)       |
| Java       | [Reference](https://aka.ms/azsdk/azure-ai-inference/java/reference) | [azure-ai-inference (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-inference/) | [Java examples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-inference/src/samples) |
| JavaScript | [Reference](https://aka.ms/AAp1kxa) | [@azure/ai-inference (npm)](https://www.npmjs.com/package/@azure/ai-inference) | [JavaScript examples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples) |
| Python     | [Reference](https://aka.ms/azsdk/azure-ai-inference/python/reference) | [azure-ai-inference (PyPi)](https://pypi.org/project/azure-ai-inference/) | [Python examples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples) |

## Azure OpenAI inference endpoint

Azure OpenAI models also support the Azure OpenAI API. This API exposes the full capabilities of OpenAI models and support additional features like assistants, threads, files, and batch inference.

Azure OpenAI inference endpoints are used per-deployment and they have they own URL that is associated with only one deployment. However, the same authentication mechanism can be used to consume it. Learn more in the reference page for [Azure OpenAI API](../../../ai-services/openai/reference.md)

:::image type="content" source="../../media/ai-services/endpoint/endpoint-openai.png" alt-text="An illustration showing how Azure OpenAI deployments contain a single URL for each deployment." lightbox="../../media/ai-services/endpoint/endpoint-openai.png":::

Each deployment has a URL that is the concatenations of the **Azure OpenAI** base URL and the route `/deployments/<model-deployment-name>`.

> [!IMPORTANT]
> There is no routing mechanism for the Azure OpenAI endpoint, as each URL is exclusive for each model deployment.

### Supported languages and SDKs

The Azure OpenAI endpoint is supported by the **OpenAI SDK (`AzureOpenAI` class)** and **Azure OpenAI SDKs**, which are available in multiple languages:

| Language   | Source code | Package | Examples |
|------------|---------|-----|-------|
| C#         | [Source code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/openai/Azure.AI.OpenAI) | [Azure.AI.OpenAI (NuGet)](https://www.nuget.org/packages/Azure.AI.OpenAI/) | [C# examples](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/openai/Azure.AI.OpenAI/tests/Samples)       |
| Go         | [Source code](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/ai/azopenai) | [azopenai (Go)](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai)| [Go examples](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai#pkg-examples) |
| Java       | [Source code](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai) | [azure-ai-openai (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-openai/) | [Java examples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai/src/samples) |
| JavaScript | [Source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai) | [@azure/openai (npm)](https://www.npmjs.com/package/@azure/openai) | [JavaScript examples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples/) |
| Python     | [Source code](https://github.com/openai/openai-python) | [openai (PyPi)](https://pypi.org/project/openai/) | [Python examples](https://github.com/openai/openai-cookbook) |

## Next steps

- [Deployment types](deployment-types.md)