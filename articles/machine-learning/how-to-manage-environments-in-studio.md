---
title: Manage environments in the studio
titleSuffix: Azure Machine Learning
description: Learn how to create and manage environments in the Azure Machine Learning studio. Environments are used for training and inference.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
author: s-polly
ms.author: scottpolly
ms.reviewer: osiotugo
ms.date: 04/14/2025
ms.topic: how-to
ms.custom:
# Customer Intent: As a Data Scientist, I want to understand how to manage environments for training and inference in Azure Machine Learning studio.
---

# Manage software environments in Azure Machine Learning studio

This article explains how to create and manage [Azure Machine Learning environments](/python/api/azure-ai-ml/azure.ai.ml.entities.environment) in the Azure Machine Learning studio. Use the environments to track and reproduce your projects' software dependencies as they evolve.

The examples in this article show how to:

* Browse curated environments.
* Create an environment and specify package dependencies.
* Edit an existing environment specification and its properties.
* Rebuild an environment and view image build logs.

For a high-level overview of environments, see [What are Azure Machine Learning environments?](concept-environments.md) For more information, see [How to set up a development environment for Azure Machine Learning](how-to-configure-environment.md).

## Prerequisites

* An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* An [Azure Machine Learning workspace](quickstart-create-resources.md).

## Browse curated environments

Curated environments contain collections of Python packages and are available in your workspace by default. These environments are backed by cached Docker images, which reduce the job preparation cost and support training and inferencing scenarios.

> [!TIP]
> When you work with curated environments in the CLI or SDK, the curated environment names begin with `AzureML-`. When you use the Azure Machine Learning studio, the curated environments don't have this prefix. The reason for this difference is that the studio UI displays curated and custom environments on separate tabs, so the prefix isn't necessary. The CLI and SDK don't have this separation, so the prefix is used to differentiate between curated and custom environments.

Select an environment to see detailed information about its contents. For more information, see [Azure Machine Learning curated environments](resource-curated-environments.md).

## Create an environment

To create an environment:
1. Open your workspace in [Azure Machine Learning studio](https://ml.azure.com).
1. On the left side, select **Environments**.
1. Select the **Custom environments** tab.
1. Select the **Create** button.

Select one of the following options:
* Create a new docker [context](https://docs.docker.com/engine/reference/commandline/build/).
* Start from an existing environment.
* Upload an existing docker context.
* Use existing docker image with optional conda file.

:::image type="content" source="media/how-to-manage-environments-in-studio/create-page.png" alt-text="Screenshot of the environment creation wizard.":::

You can customize the configuration file, add tags and descriptions, and review the properties before creating the entity.

If a new environment is given the same name as an existing environment in the workspace, a new version of the existing one is created.

## View and edit environment details

1. Once an environment has been created, view its details by selecting the __Name__ from the __Custom environments__ tab.

    :::image type="content" source="media/how-to-manage-environments-in-studio/select-existing-environment.png" alt-text="Screenshot of the custom environments page." lightbox="media/how-to-manage-environments-in-studio/select-existing-environment.png":::

1. Use the __Version__ dropdown menu to select different versions of the environment. From the __Details__ tab, you can view metadata and the contents of the environment through its various dependencies. Select the pencil icons to edit fields such as __Description__ and __Tags__.

    :::image type="content" source="media/how-to-manage-environments-in-studio/environment-details.png" alt-text="Screenshot of the environment details tab." lightbox="media/how-to-manage-environments-in-studio/environment-details.png":::

3. Select the __Context__ tab to upload additional files or edit the existing Dockerfile. Use __Save and Build__ to save any changes and rebuild the context.

    Keep in mind that any changes to the Docker or Conda sections create a new version of the environment.

    :::image type="content" source="media/how-to-manage-environments-in-studio/environment-context.png" alt-text="Screenshot of the environment context tab." lightbox="media/how-to-manage-environments-in-studio/environment-context.png":::

## View logs

Select the **Build log** tab on the details page to view the logs of an environment version and the environment log analysis. Environment log analysis is a feature that provides insight and relevant troubleshooting documentation to explain environment definition issues or image build failures.

* The build log contains the bare output from an Azure Container Registry (ACR) task or an Image Build Compute job.
* Image build analysis is an analysis of the build log used to see the cause of the image build failure.
* Environment definition analysis provides information about the environment definition if it goes against best practices for reproducibility, supportability, or security.

For an overview of common build failures, see [Troubleshooting environment issues](https://aka.ms/azureml/environment/troubleshooting-guide).

If you have feedback on the environment log analysis, file a [GitHub issue](https://aka.ms/azureml/environment/log-analysis-feedback).

## Rebuild an environment

On the details page, select the **Rebuild** button to rebuild the environment. Any unpinned package versions in your configuration files might be updated to the most recent version with this action.

## Next step

> [!div class="nextstepaction"]
> [How to create and manage files in your workspace](how-to-manage-files.md)
