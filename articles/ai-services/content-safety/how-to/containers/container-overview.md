---
title: Content safety containers overview - Azure AI Content Safety
titleSuffix: Azure AI services
description: Use the Docker containers for the content safety service to perform content safety operations on-premises.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: overview
ms.date: 09/16/2025
ms.author: pafarley
keywords: on-premises, Docker, container
---

# Content Safety containers overview (preview)

Containers let you use a subset of the Azure AI Content Safety features in your own environment. With content safety containers, you can build a content safety application architecture optimized for both robust cloud capabilities and edge locality. Containers help you meet specific security and data governance requirements. 

## Available containers

The following table lists the content safety containers available in the Microsoft Container Registry (MCR). The table also lists the features supported by each container and the latest version of the container.

| Container                            |  Features |
|--------------------------------------|----------|
|Analyze text|Scans text for sexual content, violence, hate, and self-harm with multiple severity levels.|
|Analyze image|Scans images for sexual content, violence, hate, and self-harm with multiple severity levels.|
|Prompt Shields for user prompts and documents |Detects and mitigates user prompt attacks and safeguards against attacks not directly supplied by the user or developer, such as external documents. |

The content safety container is available in public preview. Containers in preview are still under development and don't meet Microsoft's stability and support requirements.

## Request approval to run offline containers

To use the content safety containers in environments that are disconnected from the internet, you must submit a [request form](https://aka.ms/csdisconnectedcontainers) and wait for approval. For more information about applying and purchasing a commitment plan to use containers in disconnected environments, see [Use containers in disconnected environments](../../../../ai-services/containers/disconnected-containers.md) in the Azure AI services documentation.

The request form takes information about you, your company, and the user scenario for which you use the container. Make sure you meet the following requirements:

* On the form, you must use the email address associated with your Azure subscription ID.
* The Azure resource you use to run the container must be created with the approved Azure subscription ID.

After you submit the form, the Azure AI services team reviews it and emails you with a decision within 10 business days.

## Billing information

The content safety containers send billing information to Azure through the content safety resource in your Azure account.

Content safety containers aren't licensed to run without being connected to Azure for metering. You must configure your container to always communicate billing information with the metering service. For more information, see [Billing arguments](./install-run-container.md#billing-information). 

> [!NOTE]
> Connected and disconnected container pricing and commitment tiers vary. For more information, see [Content safety service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/content-safety/).

## Container recipes and other container services

You can use container recipes to create containers that can be reused. Containers can be built with some or all configuration settings so that they aren't needed when the container is started. For container recipes see the following Azure AI services articles:
- [Create containers for reuse](/azure/ai-services/containers/container-reuse-recipe)
- [Deploy and run containers on Azure Container Instance](/azure/ai-services/containers/azure-container-instance-recipe)
- [Deploy a language detection container to Azure Kubernetes Service](/azure/ai-services/containers/azure-kubernetes-recipe)
- [Use Docker Compose to deploy multiple containers](/azure/ai-services/containers/docker-compose-recipe)

For information about other container services, see the following Azure AI services articles:
- [Tutorial: Create a container image for deployment to Azure Container Instances](/azure/container-instances/container-instances-tutorial-prepare-app)
- [Quickstart: Create a private container registry using the Azure CLI](/azure/container-registry/container-registry-get-started-azure-cli)
- [Tutorial: Prepare an application for Azure Kubernetes Service (AKS)](/azure/aks/tutorial-kubernetes-prepare-app)

## Next steps

* [Install and run analyze text containers](./text-container.md)
* [Install and run analyze image containers](./image-container.md)


