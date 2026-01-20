---
title: About Azure Machine Learning environments
titleSuffix: Azure Machine Learning
description: Learn about machine learning environments, which enable reproducible, auditable, & portable machine learning dependency definitions for various compute targets.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: concept-article
author: s-polly
ms.author: scottpolly
ms.reviewer: osiotugo
ms.date: 10/30/2025
ms.custom: FY25Q1-Linter
# Customer Intent: As a data scientist, I want to understand what Azure Machine Learning environments are and how they can help me manage my machine learning dependencies.
---

# What are Azure Machine Learning environments?

Azure Machine Learning environments encapsulate the environment where your machine learning training or inferencing happens. They specify the Python packages and software settings for your training and scoring scripts. The Machine Learning workspace manages and versions these environments, enabling reproducible, auditable, and portable machine learning workflows across various compute targets. Use an `Environment` object to:

* Develop your training script.
* Reuse the same environment on Azure Machine Learning Compute for model training at scale.
* Deploy your model with that same environment.
* Revisit the environment in which an existing model was trained.

The following diagram illustrates how you can use a single `Environment` object in both your job configuration (for training) and your inference and deployment configuration (for web service deployments).

![Diagram of an environment in machine learning workflow](./media/concept-environments/ml-environment.png)

The environment, compute target, and training script together form the job configuration: the full specification of a training job.

## Types of environments

Environments fall into three categories: *curated*, *user-managed*, and *system-managed*.

Curated environments are provided by Azure Machine Learning and are available in your workspace by default. Use them as is. They contain collections of Python packages and settings to help you get started with various machine learning frameworks. These precreated environments also allow for faster deployment time. Azure Machine Learning hosts curated environments in the __AzureML registry__, which is a [machine learning registry](concept-machine-learning-registries-mlops.md) hosted by Microsoft. For a full list, see the [environments in AzureML registry](https://ml.azure.com/registries/azureml/environments).

In user-managed environments, you're responsible for setting up your environment and installing every package that your training script needs on the compute target. Also be sure to include any dependencies needed for model deployment. User managed environment can be BYOC (Bring Your Own Container) or Docker Build Context based that delegates image materialization to Azure Machine Learning. Similar to curated environments, you can share user-managed environments across workspaces by using a [machine learning registry](concept-machine-learning-registries-mlops.md) that you create and manage.

Use system-managed environments when you want [conda](https://conda.io/docs/) to manage the Python environment for you. A new conda environment is materialized from your conda specification on top of a base docker image.

## Create and manage environments

You can create environments from the Azure Machine Learning Python SDK, Azure Machine Learning CLI, Azure Machine Learning studio, and [VS Code extension](how-to-manage-resources-vscode.md#create-environment). Each client lets you customize the base image, Dockerfile, and Python layer if needed.

For specific code samples, see the "Create an environment" section of [How to use environments](how-to-manage-environments-v2.md#create-a-custom-environment). 

You can also manage environments through your workspace. With your workspace, you can:

* Register environments.
* Fetch environments from your workspace to use for training or deployment.
* Create a new instance of an environment by editing an existing one.
* View changes to your environments over time, which ensures reproducibility.
* Build Docker images automatically from your environments.

When you submit an experiment, the service automatically registers "anonymous" environments in your workspace. These environments aren't listed but you can use the version to retrieve them.

For code samples, see the "Manage environments" section of [How to use environments](how-to-manage-environments-v2.md#manage-environments).

## Environment building, caching, and reuse

Azure Machine Learning builds environment definitions into Docker images. It also caches the environments so you can reuse them in subsequent training jobs and service endpoint deployments. Running a training script remotely requires the creation of a Docker image. By default, Azure Machine Learning manages image build target on available workspace [serverless compute quota](how-to-use-serverless-compute.md) if no dedicated compute set for the workspace.

> [!NOTE]
> Any network restrictions in Azure Machine Learning workspace might require dedicated user managed image build compute setup. Please follow the steps to [secure workspace resources](how-to-secure-workspace-vnet.md).

### Submitting a job by using an environment

When you first submit a remote job by using an environment or create environment instance manually, Azure Machine Learning builds an image for the provided specification. The resulting image is cached in the container registry instance associated with the workspace. Curated environments are already cached in the Azure Machine Learning Registry. At the start of the job execution, the compute target retrieves the image from the relevant container registry.

### Building environments as Docker images

If the image for a particular environment definition doesn't already exist in the container registry instance associated with Azure Machine Learning workspace, the service builds a new image. For system managed environments, the image build process consists of two steps:

 1. Downloading a base image, and executing any Docker steps
 1. Building a conda environment according to conda dependencies specified in the environment definition.

For user managed environments, the service uses the provided docker context builds as is. In this case, you're responsible for installing any Python packages, by including them in your base image, or specifying custom Docker steps.

### Image caching and reuse

If you use the same environment definition for another job, Azure Machine Learning reuses the cached image from the container registry associated with your workspace.

To view the details of a cached image, check the Environments page in Azure Machine Learning studio or use [`MLClient.environments`](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-environments) to get and inspect the environment.

To determine whether to reuse a cached image or build a new one, Azure Machine Learning computes a [hash value](https://en.wikipedia.org/wiki/Hash_table) from the environment definition. It then compares the hash to the hashes of existing environments. The hash serves as a unique identifier for an environment and is based on the environment definition's:
 
 * Base image
 * Custom docker steps
 * Python packages

The environment name and version have no effect on the hash. If you rename your environment or create a new one with the same settings and packages as another environment, the hash value remains the same. However, environment definition changes like adding or removing a Python package or changing a package version change the resulting hash value. Changing the order of dependencies or channels in an environment changes the hash and requires a new image build. Similarly, any change to a curated environment results in the creation of a custom environment. 

> [!NOTE]
> You can't submit any local changes to a curated environment without changing the name of the environment. The prefixes "AzureML-" and "Microsoft" are reserved exclusively for curated environments, and your job submission fails if the name starts with either of them.

The environment's computed hash value is compared with the hashes in the workspace container registry. If there's a match, the cached image is pulled and used. Otherwise, an image build is triggered.

The following diagram shows three environment definitions. Two of them have different names and versions but identical base images and Python packages, which result in the same hash and corresponding cached image. The third environment has different Python packages and versions, leading to a different hash and cached image.

![Diagram of environment caching and Docker images](./media/concept-environments/environment-caching.png)

Actual cached images in your workspace container registry have names similar to `azureml/azureml_e9607b2514b066c851012848913ba19f` with the hash appearing at the end.

>[!IMPORTANT]
> * If you create an environment with an unpinned package dependency (for example, `numpy`), the environment uses the package version that was *available when the environment was created*. Any future environment that uses a matching definition uses the original version. 
>
>   To update the package, specify a version number to force an image rebuild. An example of this change is updating `numpy` to `numpy==1.18.1`. New dependencies, including nested ones, are installed, and they might break a previously working scenario.
>
> * Using an unpinned base image like `mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04` in your environment definition might result in rebuilding the image every time the `latest` tag is updated. This behavior helps the image receive the latest patches and system updates.

### Image patching

Microsoft patches the base images for known security vulnerabilities. Updates for supported images are released every two weeks, and the latest version of the image doesn't have unpatched vulnerabilities older than 30 days. Patched images are released with a new immutable tag, and the `:latest` tag is updated to the latest version of the patched image. 

You need to update associated Azure Machine Learning assets to use the newly patched image. For example, when working with a managed online endpoint, you need to redeploy your endpoint to use the patched image.

If you provide your own images, you're responsible for updating them and updating the Azure Machine Learning assets that use them.

For more information on the base images, see the following links:

* [Azure Machine Learning base images](https://github.com/Azure/AzureML-Containers) GitHub repository.
* [Use a custom container to deploy a model to an online endpoint](how-to-deploy-custom-container.md)
* [Managing environments and container images](concept-vulnerability-management.md#managing-environments-and-container-images)

## Related content

* Learn how to [create and use environments](how-to-use-environments.md) in Azure Machine Learning.
* See the Python SDK reference documentation for the [environment class](/python/api/azure-ai-ml/azure.ai.ml.entities.environment).
