---
title: Speech containers overview - Speech service
titleSuffix: Foundry Tools
description: Use the Docker containers for the Speech service to perform speech recognition, transcription, generation, and more on-premises.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 12/19/2025
ms.author: pafarley
keywords: on-premises, Docker, container
# Customer intent: As a developer, I want to learn about the Speech containers available in the Microsoft Container Registry (MCR).
---

# Speech containers overview

By using containers, you can use a subset of the Speech service features in your own environment. With Speech containers, you can build a speech application architecture optimized for both robust cloud capabilities and edge locality. Containers are great for specific security and data governance requirements. 

## Available Speech containers

The following table lists the Speech containers available in the Microsoft Container Registry (MCR). The table also lists the features supported by each container and the latest version of the container. 

| Container | Features | Supported versions and locales |
|--|--|--|
| [Speech to text](speech-container-stt.md) | Transcribes continuous real-time speech or batch audio recordings with intermediate results.  | Latest: 5.1.0<br/><br/>For all supported versions and locales, see the [Microsoft Container Registry (MCR)](https://mcr.microsoft.com/product/azure-cognitive-services/speechservices/speech-to-text/tags) and [JSON tags](https://mcr.microsoft.com/v2/azure-cognitive-services/speechservices/speech-to-text/tags/list).|
| [Custom speech to text](speech-container-cstt.md) | Using a custom model from the [custom speech portal](https://speech.microsoft.com/customspeech), transcribes continuous real-time speech or batch audio recordings into text with intermediate results. | Latest: 5.1.0<br/><br/>For all supported versions and locales, see the [Microsoft Container Registry (MCR)](https://mcr.microsoft.com/product/azure-cognitive-services/speechservices/custom-speech-to-text/tags) and [JSON tags](https://mcr.microsoft.com/v2/azure-cognitive-services/speechservices/speech-to-text/tags/list). |
| [Speech language identification](speech-container-lid.md)<sup>1, 2</sup> | Detects the language spoken in audio files. | Latest preview: 1.18.0<br/><br/>For all supported versions and locales, see the [Microsoft Container Registry (MCR)](https://mcr.microsoft.com/product/azure-cognitive-services/speechservices/language-detection/tags) and [JSON tags](https://mcr.microsoft.com/v2/azure-cognitive-services/speechservices/language-detection/tags/list). |
| [Neural text to speech](speech-container-ntts.md) | Converts text to natural-sounding speech by using deep neural network technology, which allows for more natural synthesized speech. | Latest: 4.1.0<br/><br/>For all supported versions and locales, see the [Microsoft Container Registry (MCR)](https://mcr.microsoft.com/product/azure-cognitive-services/speechservices/neural-text-to-speech/tags) and [JSON tags](https://mcr.microsoft.com/v2/azure-cognitive-services/speechservices/neural-text-to-speech/tags/list). |

<sup>1</sup> The container is available in public preview. Containers in preview are still under development and don't meet Microsoft's stability and support requirements.

<sup>2</sup> Not available as a disconnected container.

## Request approval to run containers disconnected from the internet

To use the Speech containers in environments that are disconnected from the internet, you must submit a [request form](https://aka.ms/csdisconnectedcontainers) and wait for approval. For more information about applying and purchasing a commitment plan to use containers in disconnected environments, see [Use containers in disconnected environments](../containers/disconnected-containers.md) in the Foundry Tools documentation.

The form requests information about you, your company, and the user scenario for which you use the container. 

* On the form, you must use an email address associated with an Azure subscription ID.
* The Azure resource you use to run the container must be created with the approved Azure subscription ID.
* Check your email for updates on the status of your application from Microsoft.

After you submit the form, the Foundry Tools team reviews it and emails you with a decision within 10 business days.

## Billing information

The Speech containers send billing information to Azure by using a Foundry resource for Speech on your Azure account. 

> [!NOTE]
> Connected and disconnected container pricing and commitment tiers vary. For more information, see [Speech service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

Speech containers aren't licensed to run without being connected to Azure for metering. You must configure your container to always communicate billing information with the metering service. For more information, see [billing arguments](speech-container-howto.md#billing-arguments). 

## Container recipes and other container services

You can use container recipes to create containers that can be reused. Containers can be built with some or all configuration settings so that they aren't needed when the container is started. For container recipes see the following Foundry Tools articles:
- [Create containers for reuse](../containers/container-reuse-recipe.md)
- [Deploy and run container on Azure Container Instance](../containers/azure-container-instance-recipe.md)
- [Deploy a language detection container to Azure Kubernetes Service](../containers/azure-kubernetes-recipe.md)
- [Use Docker Compose to deploy multiple containers](../containers/docker-compose-recipe.md)

For information about other container services, see the following Foundry Tools articles:
- [Tutorial: Create a container image for deployment to Azure Container Instances](/azure/container-instances/container-instances-tutorial-prepare-app)
- [Quickstart: Create a private container registry using the Azure CLI](/azure/container-registry/container-registry-get-started-azure-cli)
- [Tutorial: Prepare an application for Azure Kubernetes Service (AKS)](/azure/aks/tutorial-kubernetes-prepare-app)

## Next step

* [Install and run Speech containers](speech-container-howto.md)


