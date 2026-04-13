---
title: Include file
description: Include file
author: msakande
ms.reviewer: sgilley
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

Microsoft Foundry Models enables you to access the most powerful models from leading model providers through a single endpoint and set of credentials. This capability lets you switch between models and use them in your application without changing any code.

This article explains how the Foundry services organize models and how to use the inference endpoint to access them.

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

## Deployments

Foundry uses **deployments** to make models available. **Deployments** give a model a name and set specific configurations. You can access a model by using its deployment name in your requests.

A deployment includes:

* A model name
* A model version
* A provisioning or capacity type<sup>1</sup>
* A content filtering configuration<sup>1</sup>
* A rate limiting configuration<sup>1</sup>

<sup>1</sup> These configurations can change depending on the selected model.

A Foundry resource can have many model deployments. You only pay for inference performed on model deployments. Deployments are Azure resources, so they're subject to Azure policies.

For more information about creating deployments, see [Add and configure model deployments](../how-to/create-model-deployments.md).
