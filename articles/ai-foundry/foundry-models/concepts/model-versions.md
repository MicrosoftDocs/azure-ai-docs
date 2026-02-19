---
title: Model versions in Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Learn about model versions in Foundry Models.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: concept-article
ms.custom: ignite-2024, github-universe-2024, pilot-ai-workflow-jan-2026
ms.date: 02/11/2026
author: msakande
ms.author: mopeakande
recommendations: false
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
# customer intent: As a developer, I want to understand how model versions work in Microsoft Foundry Models so I can manage deployments and updates effectively.
---

# Model versions in Microsoft Foundry Models

Microsoft Foundry Models regularly release new model versions that incorporate the latest features and improvements from model providers. This article explains how model versioning works, what update policies are available for your deployments, and how Azure OpenAI and partner model versions are managed.

## How model versions work

You can choose to start with a particular model version and stay on it, or automatically update as new versions are released.

There are two different versions to consider when working with models:

* The version of the model itself.
* The version of the API used to consume a model deployment.

The version of a model is decided when you deploy it. You can choose an update policy, which can include the following options:

* Deployments set with a specific version or without offering an upgrade policy require a manual upgrade if a new version is released. When the model is retired, those deployments stop working.

* Deployments set to **Auto-update to default** automatically update to use the new default version.

* Deployments set to **Upgrade when expired** automatically update when its current version is retired.

> [!NOTE]
> Update policies are configured per deployment and **vary** by model and provider.

For example, a deployment of `gpt-4o` might target version `2024-08-06`. When version `2024-11-20` becomes available, deployments set to auto-update switch to the new version automatically.

You configure update policies when you deploy a model in the [Foundry portal](https://ai.azure.com). You can also change the policy later in the deployment settings. To check the current version of a deployment, open the deployment details in the Foundry portal or query the deployment via the REST API.

The API version indicates the contract that you use to interface with the model in code. When using REST APIs, you indicate the API version using the query parameter `api-version`. Azure SDK versions are usually paired with specific API versions, but you can specify the API version you want to use.

A given model deployment might support multiple API versions. The release of a new model version doesn't always require you to upgrade to a new API version, as is the case when there's an update to the model's weights. Azure maintains the previous major version of a model until its retirement date, so you can switch back to it if needed.

## Azure OpenAI model updates

Azure works closely with OpenAI to release new model versions. When a new version of a model is released, you can immediately test it in new deployments. Azure publishes when new versions of models are released, and notifies customers at least two weeks before a new version becomes the default version of the model.

### Prepare for Azure OpenAI model version upgrades

As a customer of Azure OpenAI models, you might notice some changes in the model behavior and compatibility after a version upgrade.  These changes might affect your applications and workflows that rely on the models.  Here are some tips to help you prepare for version upgrades and minimize the impact:

* Read [what's new](../../openai/whats-new.md) and [models](models-sold-directly-by-azure.md) to understand the changes and new features.
* Read the documentation on [model deployments](../../openai/how-to/create-resource.md) and [version upgrades](../../openai/how-to/working-with-models.md) to understand how to work with model versions.
* Test your applications and workflows with the new model version after release.
* Update your code and configuration to use the new features and capabilities of the new model version.

## Partner model updates

Azure works closely with model providers to release new model versions. When a new version of a model is released, you can immediately test it in new deployments.

New model versions might result in a new model ID being published. For example, `Llama-3.3-70B-Instruct`, `Meta-Llama-3.1-70B-Instruct`, and `Meta-Llama-3-70B-Instruct`. In some cases, all the model versions might be available in the same API version. In other cases, you might also need to adjust the API version used to consume the model in case the API contract has changed from one model to another.

## Related content

- [Working with Azure OpenAI models](../../openai/how-to/working-with-models.md)
- [Model deprecation and retirement for Microsoft Foundry Models](../../concepts/model-lifecycle-retirement.md)
- [Azure OpenAI in Microsoft Foundry model deprecations and retirements](../../openai/concepts/model-retirements.md)
- [Deploy Foundry Models](../how-to/deploy-foundry-models.md)
- [Deployment types in Foundry Models](deployment-types.md)
