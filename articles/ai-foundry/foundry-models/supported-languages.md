---
title: Supported programming languages for models in Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Learn how to choose the right programming languages and SDKs for deploying and using models in Microsoft Foundry Models.
author: msakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom: ignite-2024, github-universe-2024
ms.topic: concept-article
ms.date: 11/21/2025
ms.author: mopeakande
ms.reviewer: achand
reviewer: achandmsft
ai-usage: ai-assisted

#CustomerIntent: As a developer building AI applications with Microsoft Foundry Models, I want to know which programming languages and SDKs are supported for Microsoft Foundry Models so that I can choose the right tools for my application development.
---

# Supported programming languages for Azure AI Inference SDK

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

[!INCLUDE [migrate-model-inference-to-v1-openai](../includes/migrate-model-inference-to-v1-openai.md)]

All models deployed to Microsoft Foundry Models support the [Azure AI Model Inference API](https://aka.ms/azureai/modelinference) and its associated family of SDKs.

To use these SDKs, connect them to the [Azure AI model inference URI](./concepts/endpoints.md) (usually in the form `https://<resource-name>.services.ai.azure.com/models`).

## Azure AI Inference package

The Azure AI Inference package allows you to consume all models deployed to the Foundry resource and easily switch the model deployment from one to another. The Azure AI Inference package is part of the Microsoft Foundry SDK.

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

Foundry doesn't support the Cohere SDK or the Mistral SDK.

## Next step

- To see what models are currently supported, see [Foundry Models and capabilities](./concepts/models-sold-directly-by-azure.md).
