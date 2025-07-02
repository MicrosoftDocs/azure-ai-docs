---
title: Region availability for models in serverless APIs
titleSuffix: Azure AI Foundry
description: Learn about the regions where each model is available for deployment in serverless APIs via Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 04/22/2025
ms.author: mopeakande
author: msakande
ms.reviewer: fasantia
reviewer: santiagxf
ms.custom: 
 - build-2024
 - serverless
 - references_regions
---

# Region availability for models in serverless APIs

In this article, you learn about which regions are available for each of the models supporting serverless API deployments.

[!INCLUDE [models-preview](../includes/models-preview.md)]

Certain models in the model catalog can be deployed as a serverless API. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. This deployment option doesn't require quota from your subscription.

## Region availability

Pay-as-you-go billing is available only to users whose Azure subscription belongs to a billing account in a country/region where the model provider has made the offer available (see "offer availability region" in the table in the next section). If the offer is available in the relevant region, the user then must have a Hub/Project in the Azure region where the model is available for deployment or fine-tuning, as applicable (see "Hub/Project Region" columns in the following tables).


[!INCLUDE [region-availability-maas](../includes/region-availability-maas.md)]


## Alternatives to region availability

If most of your infrastructure is in a particular region and you want to take advantage of models available only as serverless APIs, you can create a hub or project on the supported region and then consume the endpoint from another region. 

Read [Consume serverless APIs from a different hub or project](deploy-models-serverless-connect.md) to learn how to configure an existing serverless API deployment in a different hub or project than the one where it was deployed.

## Related content

- [Model Catalog and Collections](model-catalog-overview.md)
- [Deploy models as serverless API](deploy-models-serverless.md)


