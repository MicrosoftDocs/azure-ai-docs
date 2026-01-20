---
title: Open and custom models
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 09/05/2025
ms.author: mopeakande
author: msakande
---

## Open and custom models

The model catalog offers a larger selection of models from a wider range of providers. For these models, you can't use the option for [standard deployment in Microsoft Foundry resources](../../concepts/deployments-overview.md#standard-deployment-in-foundry-resources), where models are provided as APIs. Instead, to deploy these models, you might need to host them on your infrastructure, create an AI hub, and provide the underlying compute quota to host the models.

Furthermore, these models can be open-access or IP protected. In both cases, you have to deploy them in managed compute offerings in Foundry. To get started, see [How-to: Deploy to Managed compute](../../how-to/deploy-models-managed.md).