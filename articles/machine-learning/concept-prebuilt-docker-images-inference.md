---
title: Prebuilt Docker images
titleSuffix: Azure Machine Learning
description: 'Prebuilt Docker images for inference (scoring) in Azure Machine Learning'
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.author: scottpolly
author: s-polly
ms.date: 09/24/2025
ms.topic: concept-article
ms.reviewer: jturuk
ms.custom: deploy, docker, prebuilt
ai-usage: ai-assisted
---

# Docker images for inference

Azure Machine Learning provides prebuilt Docker images for inference (scoring). These images include popular machine learning frameworks and commonly used Python packages. Extend an image to add more packages if needed.

## Why use prebuilt images

Using prebuilt images helps in several ways:

- Reduces model deployment latency
- Increases deployment success rate
- Avoids building container images during deployment
- Keeps the image small by containing only the required dependencies and minimal access rights

## List of prebuilt Docker images for inference

> [!IMPORTANT]
> The list in the following table includes only the inference Docker images that Azure Machine Learning **currently supports**.

* All images run as non-root users.
* Use the `latest` tag. Prebuilt images are published to the Microsoft Container Registry (MCR). To see available tags, go to the [MCR GitHub repository](https://github.com/microsoft/ContainerRegistry#browsing-mcr-content).
* If you need a specific tag, Azure Machine Learning supports tags that are up to *six months* older than `latest`.

**Inference minimal base images**

Framework version | CPU/GPU | Pre-installed packages | MCR path
--- | --- | --- | ---
NA | CPU | NA | `mcr.microsoft.com/azureml/minimal-ubuntu22.04-py39-cpu-inference:latest`
NA | GPU | NA | `mcr.microsoft.com/azureml/minimal-ubuntu22.04-py39-cuda11.8-gpu-inference:latest`
NA | CPU | NA | `mcr.microsoft.com/azureml/minimal-py312-inference:latest`

> [!NOTE]
> Azure Machine Learning supports [curated environments](resource-curated-environments.md). To browse curated environments in Studio, go to [Manage environments in Studio](how-to-manage-environments-in-studio.md#browse-curated-environments) and apply the filter `Tags: Inferencing`.

## Related content

* [GitHub examples of how to use inference prebuilt Docker images](https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/online/custom-container)
* Learn how to [deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md).
* Discover how to [use a custom container to deploy a model to an online endpoint](how-to-deploy-custom-container.md).
