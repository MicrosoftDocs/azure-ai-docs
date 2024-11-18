---
title: Supported models in Azure AI Agent Service
titleSuffix: Azure AI services
description: Learn about the models you can use with Azure AI Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure
ms.topic: conceptual
ms.date: 11/13/2024
recommendations: false
---

# Models supported by Azure AI Agent Service

Agents are powered by a diverse set of models with different capabilities and price points. Model availability varies by region and cloud. Certain tools and capabilities require the latest models. The following models are available in the API, SDK, and Azure AI Foundry. The following table is for pay-as-you-go. For information on Provisioned Throughput Unit (PTU) availability, see [provisioned throughput](../../openai/concepts/provisioned-throughput.md) in the OpenAI documentation. You can use [global standard models](../../openai/concepts/models.md#global-standard-model-availability) if they're supported in the regions listed here. 

| Region | `gpt-35-turbo (0613)` | `gpt-35-turbo (1106)`| `fine tuned gpt-3.5-turbo-0125` | `gpt-4 (0613)` | `gpt-4 (1106)` | `gpt-4 (0125)` | `gpt-4o (2024-05-13)` | `gpt-4o-mini (2024-07-18)` |
|-----|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Australia East | ✅ | ✅ | | ✅ |✅ | | | |
| East US  | ✅ | | | | | ✅ | ✅ |✅|
| East US 2 | ✅ |  | ✅ | ✅ |✅ | |✅| |
| France Central  | ✅ | ✅ | | ✅ |✅ |  | | |
| Japan East | ✅ |  | | | | | | |
| Norway East | |  | | | ✅ |  | | |
| Sweden Central | ✅ |✅ | ✅ |✅ |✅| |✅| |
| UK South | ✅  | ✅ | | | ✅ | ✅ |  | |
| West US |  | ✅ | | | ✅ | |✅| |
| West US 3 |  |  | | |✅ | |✅| |

## Additional models

In addition to the supported Azure OpenAI models, you can also use the following 3rd party models with Azure AI Agent Service. 

* Llama 3.1-405B-instruct

## Next steps

[Create a new Agent project](../quickstart.md)