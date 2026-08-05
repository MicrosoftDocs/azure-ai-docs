---
title: Include file
description: Include file
author: msakande
ms.author: mopeakande
reviewer: achandmsft
ms.reviewer: achand
ms.service: microsoft-foundry
ms.topic: include
ms.date: 07/31/2026
ms.custom: include
ai-usage: ai-assisted
---

Microsoft Foundry Models provides access to a wide variety of models from many providers through a single endpoint and set of credentials. This capability lets you switch between models and use them in your application without making code changes.

This article explains how the Foundry services organize models and how to use the inference endpoint to access them.

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
- A Microsoft Foundry resource. If you don't have one, [create a resource and deploy a model](../how-to/create-model-deployments.md).
- At least one [model deployment](../how-to/create-model-deployments.md) in your resource.
- The latest version of the OpenAI SDK for your language (Python, JavaScript, C#, or Java), or a REST client such as `curl`.
- To use keyless authentication, the required [Microsoft Entra ID role assignments](../how-to/configure-entra-id.md) on the resource.

## Deployments

Foundry uses **deployments** as aliases for model access. A deployment gives a model a name and a set of configurations. You access a model by using its deployment name in your requests.

A deployment defines:

* A model name
* A model version
* A provisioning or capacity type<sup>1</sup>
* A content filtering configuration<sup>1</sup>
* A rate limiting configuration<sup>1</sup>

<sup>1</sup> These configurations can change depending on the selected model.

A Foundry resource can have many model deployments. You only pay for inference performed on model deployments. Deployments are Azure resources, so they're subject to Azure policies.

For more information about creating deployments, see [Add and configure model deployments](../how-to/create-model-deployments.md).
