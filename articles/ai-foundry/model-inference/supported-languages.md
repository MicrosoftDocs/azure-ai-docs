---
title: Supported programming languages for models in Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn about supported programming languages for models in Azure AI Foundry Models
author: santiagxf
manager: nitinme
ms.service: azure-ai-model-inference
ms.custom: ignite-2024, github-universe-2024
ms.topic: conceptual
ms.date: 1/21/2025
ms.author: fasantia
---

# Supported programming languages for models in Azure AI Foundry Models

Azure AI Foundry Models can be consumed with different SDKs and programming models. The following document describes which one to use:

## All models

All models deployed to Azure AI Foundry Models support the [Azure AI model inference API](https://aka.ms/azureai/modelinference) and its associated family of SDKs.

To use these SDKs, connect them to the [Azure AI model inference URI](concepts/endpoints.md#azure-ai-inference-endpoint) (usually in the form `https://<resource-name>.services.ai.azure.com/models`).

### Azure AI Inference package

The Azure AI Inference package allows you to consume all models deployed to the Azure AI Foundry resource and easily change among them. Azure AI Inference package is part of the Azure AI Foundry SDK.

| Language   | Documentation | Package | Examples |
|------------|---------|-----|-------|
| C#         | [Reference](https://aka.ms/azsdk/azure-ai-inference/csharp/reference) | [azure-ai-inference (NuGet)](https://www.nuget.org/packages/Azure.AI.Inference/) | [C# examples](https://aka.ms/azsdk/azure-ai-inference/csharp/samples)       |
| Java       | [Reference](https://aka.ms/azsdk/azure-ai-inference/java/reference) | [azure-ai-inference (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-inference/) | [Java examples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-inference/src/samples) |
| JavaScript | [Reference](/javascript/api/@azure-rest/ai-inference) | [@azure/ai-inference (npm)](https://www.npmjs.com/package/@azure/ai-inference) | [JavaScript examples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples) |
| Python     | [Reference](https://aka.ms/azsdk/azure-ai-inference/python/reference) | [azure-ai-inference (PyPi)](https://pypi.org/project/azure-ai-inference/) | [Python examples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples) |


### Integrations

| Framework   | Language   | Documentation | Package | Examples |
| ----------- |------------|---------|-----|-------|
| LangChain   | Python     | [Reference](https://python.langchain.com/docs/integrations/providers/microsoft) | [langchain-azure-ai (PyPi)](https://pypi.org/project/langchain-azure-ai/) | [Python examples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/langchain) |
| Llama-Index | Python     | [Reference](https://aka.ms/azsdk/azure-ai-inference/python/reference) | [llama-index-llms-azure-inference (PyPi)](https://pypi.org/project/llama-index-llms-azure-inference/) <br /> [llama-index-embeddings-azure-inference (PyPi)](https://pypi.org/project/llama-index-embeddings-azure-inference/) | [Python examples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/llama-index) |
| Semantic Kernel | Python     | [Reference](/semantic-kernel/overview) | [semantic-kernel[azure] (PyPi)](https://pypi.org/project/semantic-kernel/) | [Python examples](../../ai-studio/how-to/develop/semantic-kernel.md) |
| AutoGen     | Python     | [Reference](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.models.azure.html#autogen_ext.models.azure.AzureAIChatCompletionClient)  | [autogen-ext[azure] (PyPi)](https://pypi.org/project/autogen-ext/) | [Quickstart](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/quickstart.html) |


## Azure OpenAI models

Azure OpenAI models can be consumed using the following SDKs and programming languages.

To use these SDKs, connect them to the [Azure OpenAI service URI](concepts/endpoints.md#azure-openai-inference-endpoint) (usually in the form `https://<resource-name>.openai.azure.com`).

### OpenAI and Azure OpenAI SDK

| Language   | Source code | Package | Examples |
|------------|---------|-----|-------|
| C#         | [Source code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/openai/Azure.AI.OpenAI) | [Azure.AI.OpenAI (NuGet)](https://www.nuget.org/packages/Azure.AI.OpenAI/) | [C# examples](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/openai/Azure.AI.OpenAI/tests/Samples)       |
| Go         | [Source code](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/ai/azopenai) | [azopenai (Go)](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai)| [Go examples](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai#pkg-examples) |
| Java       | [Source code](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai) | [azure-ai-openai (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-openai/) | [Java examples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai/src/samples) |
| JavaScript | [Source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai) | [@azure/openai (npm)](https://www.npmjs.com/package/@azure/openai) | [JavaScript examples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples/) |
| Python     | [Source code](https://github.com/openai/openai-python) | [openai (PyPi)](https://pypi.org/project/openai/) | [Python examples](https://github.com/openai/openai-cookbook) |

### Integrations

| Framework   | Language   | Documentation | Package | Examples |
| ----------- |------------|---------|-----|-------|
| LangChain   | Python     | [Reference](https://python.langchain.com/docs/integrations/providers/microsoft) | [langchain-openai (PyPi)](https://pypi.org/project/langchain-openai/) | [Python examples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/langchain) |
| Llama-Index | Python     | [Reference](https://aka.ms/azsdk/azure-ai-inference/python/reference) | [llama-index-llms-openai (PyPi)](https://pypi.org/project/llama-index-llms-openai/) <br /> [llama-index-embeddings-openai (PyPi)](https://pypi.org/project/llama-index-embeddings-openai/) | [Python examples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/llama-index) |
| AutoGen     | Python     | [Reference](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.models.openai.html)  | [autogen-ext[openai] (PyPi)](https://pypi.org/project/autogen-ext/) | [Quickstart](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/quickstart.html) |

## Limitations

> [!WARNING]
> Cohere SDK and Mistral SDK aren't supported in Azure AI Foundry.

## Next steps

- To see what models are currently supported, check out the [Models](./concepts/models.md) section
