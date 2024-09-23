---
title: Content safety containers overview - Azure AI Content Safety
titleSuffix: Azure AI services
description: Use the Docker containers for the content safety service to perform content safety check on-premises.
author: 
manager: 
ms.service: azure-ai-content-safety
ms.topic:
ms.date: 
ms.author:
keywords: on-premises, Docker, container
---

# Content Safety containers overview

By using containers, you can use a subset of the content safety service features in your own environment. With content safety containers, you can build a content safety application architecture optimized for both robust cloud capabilities and edge locality. Containers are great for specific security and data governance requirements. 

## Available content safety containers

The following table lists the content safety containers available in the Microsoft Container Registry (MCR). The table also lists the features supported by each container and the latest version of the container. 

| Container                            |  Features |
|--------------------------------------|----------|
|Analyze text|Scans text for sexual content, violence, hate, and self harm with multi-severity levels.|
|Analyze image|Scans images for sexual content, violence, hate, and self harm with multi-severity levels.|

The content safety container is available in public preview. Containers in preview are still under development and don't meet Microsoft's stability and support requirements.

## Request approval to run containers disconnected from the internet

To use the content safety containers in environments that are disconnected from the internet, you must submit a [request form](https://aka.ms/csdisconnectedcontainers) and wait for approval. For more information about applying and purchasing a commitment plan to use containers in disconnected environments, see [Use containers in disconnected environments](../../ai-services/containers/disconnected-containers.md) in the Azure AI services documentation.

The form requests information about you, your company, and the user scenario for which you use the container. 

* On the form, you must use an email address associated with an Azure subscription ID.
* The Azure resource you use to run the container must be created with the approved Azure subscription ID.
* Check your email for updates on the status of your application from Microsoft.

After you submit the form, the Azure AI services team reviews it and emails you with a decision within 10 business days.

## Billing

The content safety containers send billing information to Azure by using a content safety resource on your Azure account. 

> [!NOTE]
> Connected and disconnected container pricing and commitment tiers vary. For more information, see [content safety service pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/content-safety/).

Content safety containers aren't licensed to run without being connected to Azure for metering. You must configure your container to always communicate billing information with the metering service. For more information, see [billing arguments](content safety-container-howto.md#billing-arguments). 

## Container recipes and other container services

You can use container recipes to create containers that can be reused. Containers can be built with some or all configuration settings so that they aren't needed when the container is started. For container recipes see the following Azure AI services articles:
- [Create containers for reuse](../containers/container-reuse-recipe.md)
- [Deploy and run container on Azure Container Instance](../containers/azure-container-instance-recipe.md)
- [Deploy a language detection container to Azure Kubernetes Service](../containers/azure-kubernetes-recipe.md)
- [Use Docker Compose to deploy multiple containers](../containers/docker-compose-recipe.md)

For information about other container services, see the following Azure AI services articles:
- [Tutorial: Create a container image for deployment to Azure Container Instances](/azure/container-instances/container-instances-tutorial-prepare-app)
- [Quickstart: Create a private container registry using the Azure CLI](/azure/container-registry/container-registry-get-started-azure-cli)
- [Tutorial: Prepare an application for Azure Kubernetes Service (AKS)](/azure/aks/tutorial-kubernetes-prepare-app)

## Next steps

* [Install and run analyze text containers](./analyze-text-container.md)
[Install and run analyze image containers](./analyze-image-container.md)


