---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 09/29/2025
ms.topic: include
---

You can decide and configure which models are available for inference in your Microsoft Foundry resource. When you configure a model, you can generate predictions from it by specifying its model name or deployment name in your requests. You don't need to make any other changes in your code to use the model.

In this article, you learn how to add a new model to a Foundry Models endpoint.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Foundry Models](../../how-to/quickstart-github-models.md) if that's your case.

* A Foundry project. This kind of project is managed under a Foundry resource (formerly known as Azure AI Services resource). If you don't have a Foundry project, see [Create a project for Foundry (Foundry projects)](../../../how-to/create-projects.md).


* [Foundry Models from partners and community](../../concepts/models-from-partners.md) require access to **Azure Marketplace**. Ensure you have the [permissions required to subscribe to model offerings](../../how-to/configure-marketplace.md). [Foundry Models sold directly by Azure](../../concepts/models-sold-directly-by-azure.md) don't have this requirement.