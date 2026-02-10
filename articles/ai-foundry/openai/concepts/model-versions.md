---
title: Azure OpenAI in Microsoft Foundry Models model versions
titleSuffix: Azure OpenAI
description: Learn about model versions in Azure OpenAI. 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article 
ms.date: 11/26/2025
manager: nitinme
author: mrbullwinkle #ChrisHMSFT
ms.author: mbullwin #chrhoder
recommendations: false
---

# Azure OpenAI in Microsoft Foundry Models model versions

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Azure OpenAI is committed to providing the best generative AI models for customers. As part of this commitment, Azure OpenAI regularly releases new model versions to incorporate the latest features and improvements from OpenAI.

## How model versions work

We want to make it easy for customers to stay up to date as models improve. Customers can choose to start with a particular version and to automatically update as new versions are released.

> [!NOTE]
> The following upgrade guidance only applies to Standard deployment types. For guidance on updating or migrating provisioned deployment types, review the [model management documentation](../how-to/working-with-models.md).

When you deploy a model you can choose an update policy, which can include the following options:

* Deployments set to **Auto-update to default** automatically update to use the new default version.
* Deployments set to **Upgrade when expired** automatically update when its current version is retired.
* Deployments that are set to **No Auto Upgrade** stop working when the model is retired.

## How Azure updates OpenAI models

Azure works closely with OpenAI to release new model versions. When a new version of a model is released, a customer can immediately test it in new deployments. Azure publishes when new versions of models are released, and notifies customers at least two weeks before a new version becomes the default version of the model.   Azure also maintains the previous major version of the model until its retirement date, so customers can switch back to it if desired.

## What you need to know about Azure OpenAI model version upgrades

As a customer of Azure OpenAI models, you might notice some changes in the model behavior and compatibility after a version upgrade. These changes might affect your applications and workflows that rely on the models. Here are some tips to help you prepare for version upgrades:

* Read [what’s new](../whats-new.md) and [models](../../foundry-models/concepts/models-sold-directly-by-azure.md) to understand the changes and new features.
* Read the documentation on [model deployments](../how-to/create-resource.md) and [version upgrades](../how-to/working-with-models.md) to understand how to work with model versions.
* Test your applications and workflows with the new model version after release.
* Update your code and configuration to use the new features and capabilities of the new model version.

### Will a model upgrade happen if the new model version is not yet available in that region?

Yes, even in cases where the latest model version is not yet available in a region, we will automatically 
upgrade deployments during the scheduled upgrade window. Our engineering team will begin rollout of the new model version starting on the announced 
upgrade date. For example, if `gpt-35-turbo-0125` is not yet available in Japan East, we will deploy `gpt-35-turbo-0125` to Japan East to upgrade older model 
versions as part of the default model version upgrade process. 


## Next Steps

- [Learn more about working with Azure OpenAI models](../how-to/working-with-models.md)
- [Learn more about Azure OpenAI model regional availability](../../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Learn more about Azure OpenAI](../../foundry-models/concepts/models-sold-directly-by-azure.md)
