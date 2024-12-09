---
title: Manage training & deploy computes (studio)
titleSuffix: Azure Machine Learning
description: Use studio to manage training and deployment compute resources (compute targets) for machine learning.
services: machine-learning
author: sdgilley
ms.author: sgilley
ms.reviewer: vijetaj
ms.service: azure-machine-learning
ms.subservice: compute
ms.date: 09/17/2024
ms.topic: how-to
ms.custom: build-2023, FY25Q1-Linter
# customer intent: As a professional data scientist, I want to manage compute resources for model training and deployment in Azure Machine Learning studio.
---

# Manage compute resources for model training and deployment in studio

In this article, learn how to manage the compute resources you use for model training and deployment in Azure Machine studio. 

With Azure Machine Learning, you can train your model on various resources or environments, collectively referred to as _compute targets_). A compute target can be a local machine or a cloud resource, such as an Azure Machine Learning Compute, Azure HDInsight, or a remote virtual machine. 

You can also use [serverless compute](./how-to-use-serverless-compute.md) as a compute target. There's nothing for you to manage when you use serverless compute.

## Prerequisites

* If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/free/) today
* An [Azure Machine Learning workspace](quickstart-create-resources.md)

## View compute targets

To see all compute targets for your workspace, use the following steps:

1. Navigate to [Azure Machine Learning studio](https://ml.azure.com).
 
1. Under __Manage__, select __Compute__.

1. Select tabs at the top to show each type of compute target.

    :::image type="content" source="media/how-to-create-attach-studio/compute-targets.png" alt-text="Screenshot of view list of compute targets." lightbox="media/how-to-create-attach-studio/compute-targets.png":::

## Create compute instance and clusters

You can create compute instances and compute clusters in your workspace, using the Azure Machine Learning SDK, CLI, or studio:

* [Compute instance](how-to-create-compute-instance.md)
* [Compute cluster](how-to-create-attach-compute-cluster.md)

In addition, you can use the [VS Code extension](how-to-manage-resources-vscode.md#compute-clusters) to create compute instances and compute clusters in your workspace.

## Attach Kubernetes clusters

For information on configuring and attaching a Kubernetes cluster to your workspace, see [Configure Kubernetes cluster for Azure Machine Learning](how-to-attach-kubernetes-anywhere.md).

## <a name="other-compute-targets"></a>Attach other compute targets

To use VMs created outside the Azure Machine Learning workspace, you must first attach them to your workspace. Attaching the compute resource makes it available to your workspace. 

1. Navigate to [Azure Machine Learning studio](https://ml.azure.com).
 
1. Under __Manage__, select __Compute__.

1. In the tabs at the top, select **Attached compute** to attach a compute target for **training**. 

1. Select +New, then select the type of compute to attach. Not all compute types can be attached from Azure Machine Learning studio.

1. Fill out the form and provide values for the required properties.

    > [!NOTE]
    > Microsoft recommends that you use SSH keys, which are more secure than passwords. Passwords are vulnerable to brute force attacks. SSH keys rely on cryptographic signatures. For information on how to create SSH keys for use with Azure Virtual Machines, see the following documents:
    >
    > * [Create and use SSH keys on Linux or macOS](/azure/virtual-machines/linux/mac-create-ssh-keys)
    > * [Create and use SSH keys on Windows](/azure/virtual-machines/linux/ssh-from-windows)

1. Select __Attach__.


Detach your compute with the following steps:

1. In Azure Machine Learning studio, select __Compute__, __Attached compute__, and the compute you wish to remove.
1. Use the __Detach__ link to detach your compute.

## Connect with SSH access

[!INCLUDE [ssh-access](includes/machine-learning-ssh-access.md)]

## Related content

* Use the compute resource to [submit a training run](how-to-train-model.md).
* Once you have a trained model, learn [how and where to deploy models](how-to-deploy-online-endpoints.md).
* [Use Azure Machine Learning with Azure Virtual Networks](./how-to-network-security-overview.md)
