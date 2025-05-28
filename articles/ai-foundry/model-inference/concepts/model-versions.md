---
title: Model versions in Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn about model versions in Foundry Models. 
ms.service: azure-ai-model-inference
ms.topic: conceptual
ms.custom: ignite-2024, github-universe-2024 
ms.date: 05/19/2025
manager: nitinme
author: santiagxf
ms.author: fasantia
recommendations: false
---

# Model versions in Azure AI Foundry Models

Azure AI Foundry Models are committed to providing the best generative AI models for customers. As part of this commitment, Azure AI Foundry Models regularly releases new model versions to incorporate the latest features and improvements from key model providers in the industry.

## How model versions work

We want to make it easy for customers to stay up to date as models improve. Customers can choose to start with a particular version and stay on it or to automatically update as new versions are released.

We distinguish two different versions when working with models:

* The version of the model itself.
* The version of the API used to consume a model deployment.

The version of a model is decided when you deploy it. You can choose an update policy, which can include the following options:

* Deployments set with a specific version or without offering an upgrade policy require a manual upgrade if a new version is released. When the model is retired, those deployments stop working.

* Deployments set to **Auto-update to default** automatically update to use the new default version.

* Deployments set to **Upgrade when expired** automatically update when its current version is retired.

> [!NOTE]
> Update policies are configured per deployment and **vary** by model and provider.

The API version indicated the contract that you use to interface with the model in code. When using REST APIs, you indicate the API version using the query parameter `api-version`. Azure SDKs versions are usually paired with specific APIs versions but you can indicate the API version you want to use. A given model deployment might support multiple API versions. The release of a new model version might not require you to upgrade to a new API version, as is the case when there's an update to the model's weights.

## Azure OpenAI model updates

Azure works closely with OpenAI to release new model versions. When a new version of a model is released, you can immediately test it in new deployments. Azure publishes when new versions of models are released, and notifies customers at least two weeks before a new version becomes the default version of the model. Azure also maintains the previous major version of the model until its retirement date, so you can switch back to it if desired.

### What you need to know about Azure OpenAI model version upgrades

As a customer of Azure OpenAI models, you might notice some changes in the model behavior and compatibility after a version upgrade.  These changes might affect your applications and workflows that rely on the models.  Here are some tips to help you prepare for version upgrades and minimize the impact:

* Read [what's new](../../../ai-services/openai/whats-new.md) and [models](../../../ai-services/openai/concepts/models.md) to understand the changes and new features.
* Read the documentation on [model deployments](../../../ai-services/openai/how-to/create-resource.md) and [version upgrades](../../../ai-services/openai/how-to/working-with-models.md) to understand how to work with model versions.
* Test your applications and workflows with the new model version after release.
* Update your code and configuration to use the new features and capabilities of the new model version.

## Partners model updates

Azure works closely with model providers to release new model versions. When a new version of a model is released, you can immediately test it in new deployments. Azure also maintains the previous major version of the model until its retirement date, so you can switch back to it if desired.

New model versions might result in a new model ID being published. For example, `Llama-3.3-70B-Instruct`, `Meta-Llama-3.1-70B-Instruct`, and `Meta-Llama-3-70B-Instruct`. In some cases, all the model versions might be available in the same API version. In other cases, you might also need to adjust the API version used to consume the model in case the API contract has changed from one model to another.

## Related content

- [Learn more about working with Azure OpenAI models](../../../ai-services/openai/how-to/working-with-models.md)