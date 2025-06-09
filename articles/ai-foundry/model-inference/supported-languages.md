---
title: Supported programming languages for models in Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn about supported programming languages for models in Azure AI Foundry Models
author: msakande
manager: scottpolly
ms.service: azure-ai-model-inference
ms.custom: ignite-2024, github-universe-2024
ms.topic: concept-article
ms.date: 05/19/2025
ms.author: mopeakande
ms.reviewer: fasantia
reviewer: santiagxf
---

# Supported programming languages for Azure AI Inference SDK

All models deployed to Azure AI Foundry Models support the [Azure AI Model Inference API](https://aka.ms/azureai/modelinference) and its associated family of SDKs.

To use these SDKs, connect them to the [Azure AI model inference URI](how-to/inference.md#azure-openai-inference-endpoint) (usually in the form `https://<resource-name>.services.ai.azure.com/models`).

## Azure AI Inference package

The Azure AI Inference package allows you to consume all models deployed to the Azure AI Foundry resource and easily change among them. Azure AI Inference package is part of the Azure AI Foundry SDK.

| Language   | Documentation | Package | Examples |
|------------|---------|-----|-------|
| C#         | [Reference](https://aka.ms/azsdk/azure-ai-inference/csharp/reference) | [azure-ai-inference (NuGet)](https://www.nuget.org/packages/Azure.AI.Inference/) | [C# examples](https://aka.ms/azsdk/azure-ai-inference/csharp/samples)       |
| Java       | [Reference](https://aka.ms/azsdk/azure-ai-inference/java/reference) | [azure-ai-inference (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-inference/) | [Java examples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-inference/src/samples) |
| JavaScript | [Reference](/javascript/api/@azure-rest/ai-inference) | [@azure/ai-inference (npm)](https://www.npmjs.com/package/@azure/ai-inference) | [JavaScript examples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples) |
| Python     | [Reference](https://aka.ms/azsdk/azure-ai-inference/python/reference) | [azure-ai-inference (PyPi)](https://pypi.org/project/azure-ai-inference/) | [Python examples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples) |


## Integrations

| Framework   | Language   | Documentation | Package | Examples |
| ----------- |------------|---------|-----|-------|
| LangChain   | Python     | [Reference](https://python.langchain.com/docs/integrations/providers/microsoft) | [langchain-azure-ai (PyPi)](https://pypi.org/project/langchain-azure-ai/) | [Python examples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/langchain) |
| Llama-Index | Python     | [Reference](https://aka.ms/azsdk/azure-ai-inference/python/reference) | [llama-index-llms-azure-inference (PyPi)](https://pypi.org/project/llama-index-llms-azure-inference/) <br /> [llama-index-embeddings-azure-inference (PyPi)](https://pypi.org/project/llama-index-embeddings-azure-inference/) | [Python examples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/llama-index) |
| Semantic Kernel | Python     | [Reference](/semantic-kernel/overview) | [semantic-kernel[azure] (PyPi)](https://pypi.org/project/semantic-kernel/) | [Python examples](../../ai-studio/how-to/develop/semantic-kernel.md) |
| AutoGen     | Python     | [Reference](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.models.azure.html#autogen_ext.models.azure.AzureAIChatCompletionClient)  | [autogen-ext[azure] (PyPi)](https://pypi.org/project/autogen-ext/) | [Quickstart](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/quickstart.html) |


## Limitations

> [!WARNING]
> Cohere SDK and Mistral SDK aren't supported in Azure AI Foundry.

## Next steps

- To see what models are currently supported, check out the [Models](./concepts/models.md) section
