---
title: Supported programming languages for models in Azure AI services
titleSuffix: Azure AI services
description: Learn about supported programming languages for models in Azure AI services
author: santiagxf
manager: nitinme
ms.service: azure-ai-studio
ms.custom: ignite-2024, github-universe-2024
ms.topic: conceptual
ms.date: 10/18/2024
ms.author: fasantia
---

# Supported programming languages for models in Azure AI services

Models deployed in Azure AI services can be used with different SDKs and programming models. The following document describes which one to use:

> [!WARNING]
> Cohere SDK and Mistral SDK are not supported in the Azure AI model inference service in Azure AI services.

## All models

All models deployed in Azure AI services support the [Azure AI model inference API](https://aka.ms/aistudio/modelinference) and its associated family of SDKs.

| Language   | Documentation | Package | Examples |
|------------|---------|-----|-------|
| C#         | [Reference](https://aka.ms/azsdk/azure-ai-inference/csharp/reference) | [azure-ai-inference (NuGet)](https://www.nuget.org/packages/Azure.AI.Inference/) | [C# examples](https://aka.ms/azsdk/azure-ai-inference/csharp/samples)       |
| Java       | [Reference](https://aka.ms/azsdk/azure-ai-inference/java/reference) | [azure-ai-inference (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-inference/) | [Java examples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-inference/src/samples) |
| JavaScript | [Reference](https://aka.ms/AAp1kxa) | [@azure/ai-inference (npm)](https://www.npmjs.com/package/@azure/ai-inference) | [JavaScript examples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples) |
| Python     | [Reference](https://aka.ms/azsdk/azure-ai-inference/python/reference) | [azure-ai-inference (PyPi)](https://pypi.org/project/azure-ai-inference/) | [Python examples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples) |

## Azure OpenAI models

Azure OpenAI models can be consumed using the following SDKs and programming languages:

| Language   | Source code | Package | Examples |
|------------|---------|-----|-------|
| C#         | [Source code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/openai/Azure.AI.OpenAI) | [Azure.AI.OpenAI (NuGet)](https://www.nuget.org/packages/Azure.AI.OpenAI/) | [C# examples](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/openai/Azure.AI.OpenAI/tests/Samples)       |
| Go         | [Source code](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/ai/azopenai) | [azopenai (Go)](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai)| [Go examples](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai#pkg-examples) |
| Java       | [Source code](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai) | [azure-ai-openai (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-openai/) | [Java examples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai/src/samples) |
| JavaScript | [Source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai) | [@azure/openai (npm)](https://www.npmjs.com/package/@azure/openai) | [JavaScript examples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples/) |
| Python     | [Source code](https://github.com/openai/openai-python) | [openai (PyPi)](https://pypi.org/project/openai/) | [Python examples](https://github.com/openai/openai-cookbook) |

## Next steps

- To see what models are currently supported, check out the [Models](./concepts/models.md) section