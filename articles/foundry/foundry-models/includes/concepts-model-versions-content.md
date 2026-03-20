---
title: include file
description: include file
author: scottpolly
ms.author: scottpolly
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/19/2026
ms.custom: include
---

Microsoft Foundry Models regularly release new model versions that incorporate the latest features and improvements from model providers. This article explains how model versioning works, what update policies are available for your deployments, and how Azure OpenAI and partner model versions are managed.

After reading this article, you'll know which upgrade policy to choose when you deploy a model, how Azure manages version upgrades automatically, and how partner model versioning differs from Azure OpenAI model versioning.

## How model versions work

You can choose to start with a particular model version and stay on it, or automatically update as new versions are released.

There are two different versions to consider when working with models:

* The version of the model itself.
* The version of the API used to consume a model deployment.


### Model version

> [!NOTE]
> The following upgrade guidance only applies to Standard deployment types. For guidance on updating or migrating provisioned deployment types, review the [model management documentation](../../openai/how-to/working-with-models.md).

You configure update policies when you deploy a model in the [Foundry portal](https://ai.azure.com). You can also change the policy later in the deployment settings. Update policies are configured per deployment and *vary* by model and provider. 

Version upgrade policies include the following options:

* Deployments set to **Opt out of automatic model version upgrades** require a manual upgrade if a new version is released. When the model is retired, those deployments stop working.
* Deployments set to **Upgrade once new default version becomes available** automatically update to use the new default version.
* Deployments set to **Once the current version expires** automatically update when their current version is retired.

For example, a deployment of `gpt-4o` might target version `2024-08-06`. When version `2024-11-20` becomes available, deployments set to auto-update switch to the new version automatically.

To check the current version of a deployment, use either of the following methods:

* **Foundry portal**: Go to your deployment in the Foundry portal, then open the **Details** tab to see the current model version.
* **REST API**: Query the deployments endpoint for your resource. The response includes the model version for each deployment.

### Version of the API used to consume a model deployment

The API version indicates the contract that you use to interface with the model in code. When using REST APIs, you indicate the API version using the query parameter `api-version`. Azure SDK versions are usually paired with specific API versions, but you can specify the API version you want to use.

A given model deployment might support multiple API versions. The release of a new model version doesn't always require you to upgrade to a new API version, as is the case when there's an update to the model's weights. Azure maintains the previous major version of a model until its retirement date, so you can switch back to it if needed.

## Azure OpenAI model upgrades

Azure works closely with OpenAI to release new model versions. When a new version of a model is released, you can immediately test it in new deployments. Azure publishes when new versions of models are released, and notifies customers at least two weeks before a new version becomes the default version of the model. Azure also maintains the previous major version of the model until its retirement date, so customers can switch back to it if desired.

### Prepare for Azure OpenAI model version upgrades

As a customer of Azure OpenAI models, you might notice some changes in the model behavior and compatibility after a version upgrade.  These changes might affect your applications and workflows that rely on the models.  Here are some tips to help you prepare for version upgrades and minimize the impact:

* Read [what's new](../../../foundry-classic/openai/whats-new.md) and [models](../concepts/models-sold-directly-by-azure.md) to understand the changes and new features.
* Read the documentation on [Deploy Foundry Models](../how-to/deploy-foundry-models.md) and [version upgrades](../../openai/how-to/working-with-models.md) to understand how to work with model versions.
* Test your applications and workflows with the new model version after release.
* Update your code and configuration to use the new features and capabilities of the new model version.

### Will a model upgrade happen if the new model version is not yet available in that region?

Yes, even in cases where the latest model version is not yet available in a region, Azure automatically upgrades deployments during the scheduled upgrade window. Our engineering team begins rollout of the new model version starting on the announced upgrade date. For example, if `gpt-35-turbo-0125` is not yet available in Japan East, Azure engineering team deploys `gpt-35-turbo-0125` to Japan East to upgrade older model versions as part of the default model version upgrade process. 

## Partner model upgrades

Azure works closely with model providers to release new model versions. When a new version of a model is released, you can immediately test it in new deployments.

New model versions might result in a new model ID being published. For example, `Meta-Llama-3-70B-Instruct` and `Meta-Llama-3.1-70B-Instruct` were both retired in favor of `Llama-3.3-70B-Instruct`. Each generation uses a different model ID. In some cases, all model versions might be available in the same API version. In other cases, you might also need to adjust the API version used to consume the model, because the API contract may have changed from one model to another.

## What happens when models are retired

When a model version reaches its retirement date, what happens next depends on the upgrade policy configured for that deployment:

* **Opt out of automatic model version upgrades**: The deployment stops accepting requests and returns errors after the model is retired. Update the deployment to a supported model version before the retirement date to avoid service interruption.
* **Upgrade once new default version becomes available**: The deployment automatically updates to the current default version. No action is required.
* **Once the current version expires**: The deployment automatically updates to the next available version when the current version expires.

Azure notifies you of upcoming retirements through email to subscription owners and contributors, Azure Service Health alerts, and the upcoming retirement tables in [Model deprecation and retirement for Microsoft Foundry Models](../../concepts/model-lifecycle-retirement.md).

## Related content

- [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md)
- [Foundry Models from partners and community](../concepts/models-from-partners.md)
- [Model deprecation and retirement for Microsoft Foundry Models](../../concepts/model-lifecycle-retirement.md)
- [Deploy Foundry Models](../how-to/deploy-foundry-models.md)
- [Deployment types in Foundry Models](../concepts/deployment-types.md)
