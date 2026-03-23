---
title: Region availability for models in standard deployments
titleSuffix: Azure Machine Learning
description: Learn about the regions where each model is available for deployment in standard deployments.
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: reference
ms.date: 03/23/2026
ms.reviewer: jturuk
ms.author: scottpolly
author: s-polly
ms.collection: ce-skilling-ai-copilot 
ms.custom: 
 - build-2024
 - serverless
 - references_regions
---

# Region availability for models in standard deployments

In this article, you learn about which regions are available for each of the models supporting standard deployments.

You can deploy certain models in the model catalog as a standard deployment. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. This deployment option doesn't require quota from your subscription.

> [!NOTE]
> Standard deployments are one of several serverless deployment types available in Microsoft Foundry. For information about all deployment types, including Global Standard and Data Zone options, see [Deployment types for Microsoft Foundry Models](../foundry/foundry-models/concepts/deployment-types.md).

## Region availability

Model providers make standard deployments available only to users whose Azure subscription belongs to a billing account in a country/region where the model provider makes the offer available (see "offer availability region" in the table in the next section). If the offer is available in the relevant region, the user must have a Hub/Project in the Azure region where the model is available for deployment or fine-tuning, as applicable (see "Hub/Project Region" columns in the following tables).


[!INCLUDE [region-availability-maas](../foundry-classic/includes/region-availability-maas.md)]


## Alternatives to region availability

If most of your infrastructure is in a particular region and you want to take advantage of models available only as standard deployments, you can create a workspace on the supported region and then consume the endpoint from another region. 

To learn how to configure an existing standard deployment in a different workspace than the one where it was deployed, see [Consume standard deployments from a different workspace](how-to-connect-models-serverless.md).

## Related content

- [Explore Microsoft Foundry Models in Azure Machine Learning](foundry-models-overview.md)
- [Deploy models as standard deployments](how-to-deploy-models-serverless.md).


