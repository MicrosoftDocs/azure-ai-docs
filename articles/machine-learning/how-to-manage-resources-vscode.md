---
title: Manage Resources with the VS Code Extension
titleSuffix: Azure Machine Learning
description: Learn how to create and manage Azure Machine Learning resources using the Azure Machine Learning Visual Studio Code extension.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: tbombach
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: how-to
ms.date: 03/31/2025
monikerRange: 'azureml-api-2 || azureml-api-1'
---

# Manage Azure Machine Learning resources with the VS Code extension (preview)

This article explains how to manage Azure Machine Learning resources by using the Visual Studio Code extension.

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

:::image type="content" source="media/how-to-manage-resources-vscode/azure-machine-learning-vscode-extension.png" alt-text="Screenshot that shows the Azure Machine Learning Visual Studio Code Extension.":::

## Prerequisites

- An Azure subscription. If you don't have one, sign up to try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Visual Studio Code. If you don't have it, see [Setting up Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview).
- The Azure Machine Learning extension. To learn how to set up the extension, see [Set up Visual Studio Code desktop with the Azure Machine Learning extension](how-to-setup-vs-code.md).

## Create resources

The quickest way to create resources is by using the extension's toolbar.

1. Open the Azure Machine Learning view from the activity bar.
1. Select your Azure subscription under **Machine Learning**.
1. Select **+** to choose your resource from the dropdown list.
1. Configure the specification file. The information required depends on the type of resource you want to create.
1. Select **AzureML: Execute YAML** from the menu bar, or by right-clicking the specification file.

Alternatively, you can create a resource by using the command palette:

1. Open the command palette by selecting **View > Command Palette**.
1. Enter `> Azure ML: Create <RESOURCE-TYPE>` into the text box. Replace `RESOURCE-TYPE` with the type of resource you want to create.
1. Configure the specification file.
1. Open the command palette by selecting **View > Command Palette**.
1. Enter `> Azure ML: Create Resource` into the text box.

## Version resources

Some resources, like environments and models, allow you to make changes to a resource and store the different versions.

To version a resource:

1. Use the existing specification file that created the resource or follow the create resources process to create a new specification file.
1. Increment the version number in the template.
1. Select **AzureML: Execute YAML** from the menu bar, or by right-clicking the specification file.

As long as the name of the updated resource is the same as the previous version, Azure Machine Learning picks up the changes and creates a new version.

## Workspaces

For more information, see [What is an Azure Machine Learning workspace?](concept-workspace.md)

### Create a workspace

1. In the Azure Machine Learning view, right-click your subscription node and select **Create workspace**.
1. A specification file appears. Configure the specification file.
1. Select **AzureML: Execute YAML** from the menu bar, or by right-clicking the specification file.

Alternatively, use the `> Azure ML: Create workspace` command in the command palette.

### Remove workspace

1. Expand the subscription node that contains your workspace.
1. Right-click the workspace you want to remove.
1. Select whether you want to remove:
    - **Only the workspace**: This option deletes *only* the workspace Azure resource. The resource group, storage accounts, and any other resources the workspace was attached to are still in Azure.
    - **With associated resources**: This option deletes the workspace *and* all resources associated with it.

Alternatively, use the `> Azure ML: Remove workspace` command in the command palette.

## Datastores

The extension currently supports datastores of the following types:

- Azure Blob
- Azure Data Lake Gen 1
- Azure Data Lake Gen 2
- Azure File

:::moniker range="azureml-api-2"
For more information, see [Datastore](concept-data.md#datastore).
:::moniker-end
:::moniker range="azureml-api-1"
For more information, see [Data concepts](concept-data.md).
:::moniker-end

### Create datastore

1. Expand the subscription node that contains your workspace.
1. Expand the workspace node you want to create the datastore under.
1. Right-click the **Datastores** node and select **Create datastore**.
1. Choose the datastore type.
1. A specification file appears. Configure the specification file.
1. Select **AzureML: Execute YAML** from the menu bar, or by right-clicking the specification file.

Alternatively, use the `> Azure ML: Create datastore` command in the command palette.

### Manage datastore

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Datastores** node inside your workspace.
1. Right-click the datastore you want to:
    - **Unregister datastore**: Removes datastore from your workspace.
    - **View datastore**: Display read-only datastore settings

Alternatively, use the `> Azure ML: Unregister datastore` and `> Azure ML: View datastore` commands respectively in the command palette.

:::moniker range="azureml-api-1"
## Datasets

The extension currently supports the following dataset types:

- *Tabular*: Allows you to materialize data into a DataFrame.
- *File*: A file or collection of files. Allows you to download or mount files to your compute.

For more information, see [Data in Azure Machine Learning v1](./concept-data.md)

### Create dataset

1. Expand the subscription node that contains your workspace.
1. Expand the workspace node you want to create the dataset under.
1. Right-click the **Datasets** node and select **Create dataset**.
1. A specification file appears. Configure the specification file.
1. Select **AzureML: Execute YAML** from the menu bar, or by right-clicking the specification file.

Alternatively, use the `> Azure ML: Create dataset` command in the command palette.

### Manage dataset

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Datasets** node.
1. Right-click the dataset you want to:
    - **View dataset properties**: Lets you view metadata associated with a specific dataset. If you have multiple versions of a dataset, you can choose to only view the dataset properties of a specific version by expanding the dataset node and performing the same steps described in this section on the version of interest.
    - **Preview dataset**: View your dataset directly in the VS Code Data Viewer. Note that this option is only available for tabular datasets.
    - **Unregister dataset**: Removes a dataset and all versions of it from your workspace.

Alternatively, use the `> Azure ML: View Dataset Properties` and `> Azure ML: Unregister Dataset` commands respectively in the command palette.
:::moniker-end

## Environments

For more information, see [What are Azure Machine Learning environments?](concept-environments.md)

### Create environment

1. Expand the subscription node that contains your workspace.
1. Expand the workspace node you want to create the datastore under.
1. Right-click the **Environments** node and select **Create environment**.
1. A specification file appears. Configure the specification file.
1. Select **AzureML: Execute YAML** from the menu bar, or by right-clicking the specification file.

Alternatively, use the `> Azure ML: Create environment` command in the command palette.

### View environment configurations

To view the dependencies and configurations for a specific environment in the extension:

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Environments** node.
1. Right-click the environment you want to view and select **View environment**.

Alternatively, use the `> Azure ML: View environment` command in the command palette.

:::moniker range="azureml-api-1"
## Experiments

For more information, see [experiments](concept-azure-machine-learning-architecture.md).
:::moniker-end
:::moniker range="azureml-api-2"
## Jobs
:::moniker-end

### Create job

The quickest way to create a job is by clicking the **Create job** icon in the extension's activity bar.

Using the resource nodes in the Azure Machine Learning view:

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Right-click the **Jobs** node in your workspace and select **Create job**.
1. Choose your job type.
1. A specification file appears. Configure the specification file.
1. Select **AzureML: Execute YAML** from the menu bar, or by right-clicking the specification file.

Alternatively, use the `> Azure ML: Create job` command in the command palette.

### View job

To view your job in Azure Machine Learning studio:

1. Expand the subscription node that contains your workspace.
1. Expand the **Jobs** node inside your workspace.
1. Right-click the job you want to view and select **View Job in Studio**.
1. A prompt appears asking you to open the job URL in Azure Machine Learning studio. Select **Open**.

Alternatively, use the `> Azure ML: View Experiment in Studio` command respectively in the command palette.

### Track job progress

As you're running your job, you might want to see its progress. To track the progress of a job in Azure Machine Learning studio from the extension:

1. Expand the subscription node that contains your workspace.
1. Expand the **Jobs** node inside your workspace.
1. Expand the job node you want to track progress for.
1. Right-click the job and select **View Job in Studio**.
1. A prompt appears asking you to open the job URL in Azure Machine Learning studio. Select **Open**.

### Download job logs & outputs

Once a job is complete, you might want to download the logs and assets such as the model generated as part of a job.

1. Expand the subscription node that contains your workspace.
1. Expand the **Jobs** node inside your workspace.
1. Expand the job node you want to download logs and outputs for.
1. Right-click the job:
    - To download the outputs, select **Download outputs**.
    - To download the logs, select **Download logs**.

Alternatively, use the `> Azure ML: Download outputs` and `> Azure ML: Download logs` commands respectively in the command palette.

## Compute instances

For more information, see [What is an Azure Machine Learning compute instance?](concept-compute-instance.md)

### Create compute instance

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Compute** node.
1. Right-click the **Compute instances** node in your workspace and select **Create compute instance**.
1. A specification file appears. Configure the specification file.
1. Select **AzureML: Execute YAML** from the menu bar, or by right-clicking the specification file.

Alternatively, use the `> Azure ML: Create compute instance` command in the command palette.

### Connect to compute instance

To use a compute instance as a development environment or remote Jupyter server, see [Connect to a compute instance](how-to-set-up-vs-code-remote.md?tabs=extension).

### Stop or restart compute instance

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Compute instances** node inside your **Compute** node.
1. Right-click the compute instance you want to stop or restart and select **Stop compute instance** or **Restart compute instance** respectively.

Alternatively, use the `> Azure ML: Stop compute instance` and `Restart compute instance` commands respectively in the command palette.

### View compute instance configuration

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Compute instances** node inside your **Compute** node.
1. Right-click the compute instance you want to inspect and select **View compute instance properties**.

Alternatively, use the `AzureML: View compute instance properties` command in the command palette.

### Delete compute instance

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Compute instances** node inside your **Compute** node.
1. Right-click the compute instance you want to delete and select **Delete compute instance**.

Alternatively, use the `AzureML: Delete compute instance` command in the command palette.

## Compute clusters

For more information, see [Training compute targets](concept-compute-target.md#training-compute-targets).

### Create compute cluster

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Compute** node.
1. Right-click the **Compute clusters** node in your workspace and select **Create compute cluster**.
1. A specification file appears. Configure the specification file.
1. Select **AzureML: Execute YAML** from the menu bar, or by right-clicking the specification file.

Alternatively, use the `> Azure ML: Create compute cluster` command in the command palette.

### View compute configuration

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Compute clusters** node inside your **Compute** node.
1. Right-click the compute you want to view and select **View compute properties**.

Alternatively, use the `> Azure ML: View compute properties` command in the command palette.

### Delete compute cluster

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Compute clusters** node inside your **Compute** node.
1. Right-click the compute you want to delete and select **Delete compute cluster**.

Alternatively, use the `> Azure ML: Delete compute cluster` command in the command palette.

## Inference clusters

For more information, see [Compute targets for inference](concept-compute-target.md#compute-targets-for-inference).

### Manage inference clusters

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Inference clusters** node inside your **Compute** node.
1. Right-click the compute you want to:
    - **View compute properties**: Displays read-only configuration data about your attached compute.
    - **Detach compute**: Detaches the compute from your workspace.

Alternatively, use the `> Azure ML: View compute properties` and `> Azure ML: Detach compute` commands respectively in the command palette.

### Delete inference clusters

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Attached computes** node inside your **Compute** node.
1. Right-click the compute you want to delete and select **Delete compute**.

Alternatively, use the `> Azure ML: Delete compute` command in the command palette.

## Attached compute

For more information, see [Unmanaged compute](concept-compute-target.md#unmanaged-compute).

### Manage attached compute

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Expand the **Attached computes** node inside your **Compute** node.
1. Right-click the compute you want to:
    - **View compute properties**: Displays read-only configuration data about your attached compute.
    - **Detach compute**: Detaches the compute from your workspace.

Alternatively, use the `> Azure ML: View compute properties` and `> Azure ML: Detach compute` commands respectively in the command palette.

## Models

:::moniker range="azureml-api-2"
For more information, see [Train models with Azure Machine Learning](concept-train-machine-learning-model.md).
:::moniker-end
:::moniker range="azureml-api-1"
For more information, see [Train models with Azure Machine Learning (v1)](./concept-train-machine-learning-model.md).
:::moniker-end

### Create model

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Right-click the **Models** node in your workspace and select **Create model**.
1. A specification file appears. Configure the specification file.
1. Right-click the specification file and select **AzureML: Execute YAML**.

Alternatively, use the `> Azure ML: Create model` command in the command palette.

### View model properties

1. Expand the subscription node that contains your workspace.
1. Expand the **Models** node inside your workspace.
1. Right-click the model whose properties you want to see and select **View model properties**. A file opens in the editor containing your model properties.

Alternatively, use the `> Azure ML: View model properties` command in the command palette.

### Download model

1. Expand the subscription node that contains your workspace.
1. Expand the **Models** node inside your workspace.
1. Right-click the model you want to download and select **Download model file**.

Alternatively, use the `> Azure ML: Download model file` command in the command palette.

### Delete a model

1. Expand the subscription node that contains your workspace.
1. Expand the **Models** node inside your workspace.
1. Right-click the model you want to delete and select **Delete model**.
1. A prompt appears confirming you want to remove the model. Select **Ok**.

Alternatively, use the `> Azure ML: Delete model` command in the command palette.

## Endpoints

:::moniker range="azureml-api-2"
For more information, see [Endpoints for inference in production](concept-endpoints.md).
:::moniker-end
:::moniker range="azureml-api-1"
For more information, see [How Azure Machine Learning works: Architecture and concepts](concept-azure-machine-learning-architecture.md).
:::moniker-end

### Create endpoint

1. Expand the subscription node that contains your workspace.
1. Expand your workspace node.
1. Right-click the **Models** node in your workspace and select **Create endpoint**.
1. Choose your endpoint type.
1. A specification file appears. Configure the specification file.
1. Select **AzureML: Execute YAML** from the menu bar, or by right-clicking the specification file.

Alternatively, use the `> Azure ML: Create endpoint` command in the command palette.

### Delete endpoint

1. Expand the subscription node that contains your workspace.
1. Expand the **Endpoints** node inside your workspace.
1. Right-click the deployment you want to remove and select **Delete endpoint**.
1. A prompt appears confirming you want to remove the service. Select **Ok**.

Alternatively, use the `> Azure ML: Delete online endpoint` command in the command palette.

### View endpoint properties

In addition to creating and deleting deployments, you can view and edit settings associated with the deployment.

1. Expand the subscription node that contains your workspace.
1. Expand the **Endpoints** node inside your workspace.
1. Right-click the deployment you want to manage, then select **View endpoint properties**.

Alternatively, use the `> Azure ML: View online endpoint properties` command in the command palette.

## Next step

> [!div class="nextstepaction"]
> [Tutorial: Train an image classification model](tutorial-train-deploy-image-classification-model-vscode.md)
