---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 1/21/2025
ms.topic: include
---

[!INCLUDE [Feature preview](../../../includes/feature-preview.md)]

You can decide and configure which models are available for inference in the inference endpoint. When a given model is configured, you can then generate predictions from it by indicating its model name or deployment name on your requests. No further changes are required in your code to use it.

In this article, you'll learn how to add a new model to Azure AI model inference in Azure AI Foundry.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Azure AI model inference](../../how-to/quickstart-github-models.md) if that's your case.

* An Azure AI services resource.