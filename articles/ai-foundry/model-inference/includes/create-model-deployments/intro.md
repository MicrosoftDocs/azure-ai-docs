---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 1/21/2025
ms.topic: include
---

You can decide and configure which models are available for inference in your Azure AI Foundry resource. When a given model is configured, you can then generate predictions from it by indicating its model name or deployment name on your requests. No further changes are required in your code to use it.

In this article, you'll learn how to add a new model to Azure AI Foundry.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Azure AI Foundry Models](../../how-to/quickstart-github-models.md) if that's your case.

* An Azure AI Foundry resource (formerly known as Azure AI Services). For more information, see [Create and configure all the resources for Azure AI Foundry Models](../../how-to/quickstart-create-resources.md).

* [Models from Partners and Community](../../concepts/models.md#models-from-partners-and-community) require access to **Azure Marketplace**. Ensure you have the [permissions required to subscribe to model offerings](../../how-to/configure-marketplace.md). [Models Sold Directly by Azure](../../concepts/models.md#models-sold-directly-by-azure) don't have this requirement.