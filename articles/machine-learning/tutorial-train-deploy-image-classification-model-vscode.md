---
title: "Train Image Classification Model with VS Code Extension"
titleSuffix: Azure Machine Learning
description: Learn how to train a TensorFlow image classification model using the Azure Machine Learning Visual Studio Code extension.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: tutorial
author: s-polly
ms.author: scottpolly
ms.reviewer: tbombach
ms.date: 04/03/2025
ms.custom:
  - cliv2
  - build-2023
  - ignite-2023
#Customer intent: As a professional data scientist, I want to learn how to train an image classification model using TensorFlow and the Azure Machine Learning Visual Studio Code Extension.
---

# Tutorial: Train an image classification model by using the Azure Machine Learning Visual Studio Code extension (preview)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

This article explains how to train an image classification model to recognize hand-written numbers by using TensorFlow and the Azure Machine Learning Visual Studio Code extension.

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

In this tutorial, you learn the following tasks:

> [!div class="checklist"]
> * Understand the code
> * Create a workspace
> * Train a model

## Prerequisites

- An Azure subscription. If you don't have one, sign up for a [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). If you're using the free subscription, only CPU clusters are supported.
- [Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview), a lightweight, cross-platform code editor.
- Azure Machine Learning studio Visual Studio Code extension. For installation instructions, see [Setup Azure Machine Learning Visual Studio Code extension](./how-to-setup-vs-code.md).
- CLI (v2). For installation instructions, see [Install and set up the CLI (v2)](how-to-configure-cli.md)
- Clone the community-driven [Azure Machine Learning examples repository](https://github.com/Azure/azureml-examples):
    ```bash
    git clone https://github.com/Azure/azureml-examples.git
    ```

## Understand the code

The code for this tutorial uses TensorFlow to train an image classification machine learning model that categorizes handwritten digits from 0-9. It does so by creating a neural network that takes the pixel values of 28x28-pixel images as input, and then outputs a list of 10 probabilities, one for each of the digits being classified. The following sample shows what the data looks like.  

:::image type="content" source="media/tutorial-train-deploy-image-classification-model-vscode/digits.png" alt-text="Screenshot that shows a sample of MNIST digits.":::

## Create a workspace

To build an application in Azure Machine Learning, you first need to create a workspace. A workspace contains the resources to train models and also the trained models themselves. For more information, see [What is an Azure Machine Learning workspace?](./concept-workspace.md)

1. In Visual Studio Code, open the *azureml-examples/cli/jobs/single-step/tensorflow/mnist* directory from the examples repository.
1. On the Visual Studio Code activity bar, select the **Azure** icon to open the Azure Machine Learning view.
1. Under **Machine Learning**, right-click your subscription node and select **Create workspace**.

    :::image type="content" source="media/tutorial-train-deploy-image-classification-model-vscode/create-workspace.png" alt-text="Screenshot that shows the option to create a workspace.":::

1. A specification file appears. Configure the specification file with the following options and then save it.

    ```yml
    $schema: https://azuremlschemas.azureedge.net/latest/workspace.schema.json
    name: TeamWorkspace
    location: WestUS2
    display_name: team-ml-workspace
    description: A workspace for training machine learning models
    tags:
      purpose: training
      team: ml-team
    ```

    The specification file creates a workspace called `TeamWorkspace` in the `WestUS2` region. The rest of the options defined in the specification file provide friendly naming, descriptions, and tags for the workspace.

1. Right-click the specification file and select **AzureML: Execute YAML**. Creating a resource uses the configuration options defined in the YAML specification file and submits a job using the CLI (v2). At this point, a request to Azure is made to create a new workspace and dependent resources in your account. After a few minutes, the new workspace appears in your subscription node.
1. Set `TeamWorkspace` as your default workspace. Doing so places resources and jobs you create in the workspace by default. Select the **Set Azure Machine Learning Workspace** button on the Visual Studio Code status bar and follow the prompts to set `TeamWorkspace` as your default workspace.

For more information on workspaces, see [Manage Azure Machine Learning resources with the VS Code extension](how-to-manage-resources-vscode.md).

## Train the model

During the training process, a TensorFlow model is trained by processing the training data and learning patterns embedded within it for each of the respective digits being classified.

Like workspaces and compute targets, training jobs are defined using resource templates. For this sample, the specification is defined in the *job.yml* file, which is located in the *azureml-examples/cli/jobs/single-step/tensorflow/mnist* folder in the examples repository.

```yml
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
code: src
command: >
    python train.py
environment: azureml:AzureML-tensorflow-2.4-ubuntu18.04-py37-cuda11-gpu:48
resources:
   instance_type: Standard_NC12
   instance_count: 3
experiment_name: tensorflow-mnist-example
description: Train a basic neural network with TensorFlow on the MNIST dataset.
```

This specification file submits a training job called `tensorflow-mnist-example` to the recently created `gpu-cluster` computer target that runs the code in the *train.py* Python script. The environment used is one of the curated environments provided by Azure Machine Learning, which contains TensorFlow and other software dependencies required to run the training script. For more information on curated environments, see [Azure Machine Learning curated environments](resource-curated-environments.md).

To submit the training job:

1. Open the *job.yml* file.
1. Right-click the file in the text editor and select **AzureML: Execute YAML**.

At this point, a request is sent to Azure to run your experiment on the selected compute target in your workspace. This process takes several minutes. The amount of time to run the training job is impacted by several factors like the compute type and training data size. To track the progress of your experiment, right-click the current run node and select **View Job in Azure portal**.

When the dialog requesting to open an external website appears, select **Open**.

:::image type="content" source="media/tutorial-train-deploy-image-classification-model-vscode/track-experiment-progress.png" alt-text="Screenshot that shows the job's progress." lightbox="media/tutorial-train-deploy-image-classification-model-vscode/track-experiment-progress.png":::

When the model is done training, the status label next to the run node updates to *Completed*.

## Related content

* [Launch Visual Studio Code integrated with Azure Machine Learning](how-to-launch-vs-code-remote.md)
* [Get started with a Python tutorial](https://code.visualstudio.com/docs/Python/Python-tutorial)
* [Manage Azure Machine Learning resources with the VS Code extension](how-to-manage-resources-vscode.md)
* [Quickstart: Get started with Azure Machine Learning](tutorial-azure-ml-in-a-day.md)
