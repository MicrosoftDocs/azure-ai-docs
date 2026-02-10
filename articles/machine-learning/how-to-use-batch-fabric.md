---
title: "Use Fabric to access model deployment batch endpoints (preview)"
titleSuffix: Azure Machine Learning
description: Use Fabric to consume Azure Machine Learning batch model deployments by pointing to the same Azure Data Lake storage account.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: how-to
author: s-polly
ms.author: scottpolly
ms.date: 02/03/2026
ms.reviewer: jturuk
ms.custom:
  - devplatv2
  - ignite-2023
  - sfi-image-nochange
#Customer intent: As a data science professional and Fabric user, I want to be able to configure Fabric to access Azure Machine Learning batch deployments, so I can access batch endpoints from both Azure Machine Learning and Fabric.
---

# Use Fabric to access model deployment batch endpoints

[!INCLUDE [ml v2](includes/machine-learning-dev-v2.md)]

In this article, you learn how to use Microsoft Fabric to access models deployed to Azure Machine Learning batch endpoints. This workflow also supports batch pipeline deployments from Fabric.

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

## Prerequisites

- A [Microsoft Fabric subscription](/fabric/enterprise/licenses) or [free Microsoft Fabric trial](/fabric/get-started/fabric-trial) with a [lakehouse created](/fabric/data-engineering/create-lakehouse).
- An Azure subscription with the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An [Azure Machine Learning workspace](how-to-manage-workspace.md) that has a model deployment to an Azure Data Lake Storage Gen 2 batch endpoint. Fabric supports only hierarchical storage accounts like Azure Data Lake Gen2. For more information, see [Deploy models for scoring in batch endpoints](how-to-use-batch-model-deployments.md).
- The [heart-unlabeled-0.csv](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/batch/deploy-models/heart-classifier-mlflow/data/heart-unlabeled-0.csv) sample dataset downloaded to use for scoring.

>[!IMPORTANT]
>The identity that invokes the batch deployment can grant access to the storage account, but the compute that runs the deployment must also have permission to mount the storage account. For more information, see [Access storage services](how-to-identity-based-service-authentication.md#access-storage-services).

## Architecture

Azure Machine Learning can't directly access data stored in Fabric [OneLake](/fabric/onelake/onelake-overview), but you can configure a [OneLake shortcut](/fabric/onelake/onelake-shortcuts) and an [Azure Machine Learning datastore](concept-data.md#datastore) to both access the same [Azure Data Lake storage account](/azure/storage/blobs/data-lake-storage-introduction). This workflow allows reading from and writing to the same underlying data without having to copy it.

The following diagram shows the data architecture.

:::image type="content" source="./media/how-to-use-batch-fabric/fabric-azureml-data-architecture.png" alt-text="A diagram showing how Azure Storage accounts are used to connect Fabric with Azure Machine Learning." border="false":::

## Configure data access

Create or identify a connection to the storage account that contains the batch endpoint data, so both Fabric OneLake and Azure Machine Learning can access the information. Fabric supports only hierarchical storage accounts like Azure Data Lake Gen2.

### Create a OneLake shortcut to the storage account

1. In **Fabric**, select your workspace from the left navigation pane.
1. Open the lakehouse you want to use.
1. In the **Explorer** pane, select the **More options** icon next to **Files**, and then select **New shortcut**.
   :::image type="content" source="./media/how-to-use-batch-fabric/fabric-lakehouse-new-shortcut.png" alt-text="A screenshot showing how to create a new shortcut in a lakehouse.":::
1. On the **New shortcut** screen, select the **Azure Data Lake Storage Gen2** option.
   :::image type="content" source="./media/how-to-use-batch-fabric/fabric-lakehouse-new-shortcut-type.png" alt-text="A screenshot showing how to create an Azure Data Lake Storage Gen2 shortcut." lightbox="media/how-to-use-batch-fabric/fabric-lakehouse-new-shortcut-type.png":::
1. On the **Connection settings** screen, select **New connection**, and then enter the URL for your Azure Data Lake Gen2 storage account.
1. In the **Connection credentials** section, provide the following information:
   - **Connection**: Select **Create new connection**.
   - **Connection name**: Keep the populated value.
   - **Authentication kind**: Select **Organizational account** to use the credentials of the connected user via OAuth 2.0. If you're not signed in, select **Sign in** to sign in.
1. Select **Next**.
   :::image type="content" source="./media/how-to-use-batch-fabric/fabric-lakehouse-new-shortcut-url.png" alt-text="A screenshot showing how to configure the URL of the shortcut.":::
1. On the next screen, select the storage account folder or folders to point the shortcut to, if applicable, and then select **Next**.
1. On the next screen, review the settings, and then select **Create**.

### Create a datastore pointing to the storage account

Create an Azure Machine Learning datastore that points to the storage account. Azure Machine Learning batch endpoints can write predictions only to blob storage accounts, so you select **Azure Blob Storage** rather than **Azure Data Lake Gen2** as the **Datastore type** for the batch endpoint. All Azure Data Lake storage accounts are also blob storage accounts.

1. In your Azure Machine Learning workspace in [Azure Machine Learning studio](https://ml.azure.com), select **Data** from the left navigation menu.
1. On the **Data** page, select the **Datastores** tab, and then select **Create**.
1. On the **Create datastore** screen, provide the following information:
   - **Datastore name**: Enter a name for the datastore.
   - **Datastore type**: Select **Azure Blob Storage**.
   - **Account selection method**: Select **Enter manually**.
   - **URL**: Enter the URL for your storage account and data container.
   - **Subscription ID**: Select your Azure subscription.
   - **Resource group of the storage resource**: Select the resource group of the storage account.
   - **Authentication type**: Select **Account key**.
   - **Account key**: Enter the access key of the storage account.
1. Select **Create**.
   :::image type="content" source="./media/how-to-use-batch-fabric/azureml-store-create-blob.png" alt-text="A screenshot showing how to configure the Azure Machine Learning data store." lightbox="media/how-to-use-batch-fabric/azureml-store-create-blob.png"::: 

## Upload sample dataset

In Fabric, upload the sample data for the batch endpoint to use as input.

1. Go to the shortcut you created in the Fabric lakehouse.
1. Select the **More actions** icon, select **New subfolder**, and create a new folder to store the sample dataset.
1. In the new folder, select **Get data** and then select **Upload files**.
   :::image type="content" source="./media/how-to-use-batch-fabric/fabric-lakehouse-get-data.png" alt-text="A screenshot showing how to upload data to an existing folder in OneLake.":::
1. Upload the sample dataset *heart-unlabeled-0.csv*.
   :::image type="content" source="./media/how-to-use-batch-fabric/fabric-lakehouse-upload-data.png" alt-text="A screenshot showing how to upload a file to OneLake.":::

The sample file is ready to be consumed. Note the path to the location where you saved it.

## Create a Fabric-to-batch inferencing pipeline

Create a Fabric-to-batch inferencing pipeline in your existing Fabric workspace that invokes the batch endpoint.

1. On the **Home** page of your Fabric workspace, select **New item**.
1. On the **New item** page, select **Pipeline**.
   :::image type="content" source="media/how-to-use-batch-fabric/fabric-select-data-pipeline.png" alt-text="A screenshot showing where to select the data pipeline option." lightbox="media/how-to-use-batch-fabric/fabric-select-data-pipeline.png":::
1. Name the pipeline and select **Create**.
1. Select the **Activities** tab at the top of the pipeline designer page.
1. Select the **More options** icon at the end of the tab, and then scroll down and select **Azure Machine Learning**.
   :::image type="content" source="./media/how-to-use-batch-fabric/fabric-pipeline-add-activity.png" alt-text="A screenshot showing how to add the Azure Machine Learning activity to a pipeline." lightbox="media/how-to-use-batch-fabric/fabric-pipeline-add-activity.png":::

### Create and configure the batch deployment connection

To configure the connection to the Azure Machine Learning workspace, complete the following steps.

1. On the lower designer pane, select the **Settings** tab.
1. Next to **Azure Machine Learning connection**, select the dropdown arrow and then select **Browse all** to add a new connection.
   :::image type="content" source="./media/how-to-use-batch-fabric/fabric-pipeline-add-connection.png" alt-text="A screenshot showing how to select Browse all to add a connection.":::
1. On the **Choose a data source to get started** screen, select **Azure Machine Learning** under **New sources**.
1. On the **Connect data source** screen, under **Connection settings**, enter the **Subscription ID**, **Resource group name**, and Azure Machine Learning **Workspace name** where your endpoint is deployed.
1. In the **Connection credentials** section, select **Create new connection** under **Connection**, and provide a connection name under **Connection name**.
1. For **Authentication kind**, select **Organizational account** to use the credentials of the connected user, or **Service principal** to use a service principal.
   >[!NOTE]
   >A service principal is recommended for production settings. For either choice, ensure that the identity associated with the connection has permission to call the batch endpoint you deployed.
1. For an organizational account, sign in if necessary. For a service principal connection, provide the **Tenant ID**, **Service principal client ID**, and **Service principal Key**.
1. Select **Connect**.
   :::image type="content" source="./media/how-to-use-batch-fabric/fabric-pipeline-add-connection-credentials.png" alt-text="A screenshot showing how to configure the connection.":::

The new connection appears in the designer **Settings** tab, and Fabric automatically populates the available batch endpoints in the selected workspace.

1. For **Batch endpoint**, select the batch endpoint you want to call. For this example, select a **heart-classifier** deployment endpoint.
1. For **Batch deployment**, select a specific deployment if needed.
   The **Batch deployment** section automatically populates with the available deployments under the endpoint. If you don't select a deployment, Fabric invokes the **Default** deployment under the endpoint, allowing the batch endpoint creator to decide which deployment to call. For most scenarios, keep this default behavior.
   :::image type="content" source="./media/how-to-use-batch-fabric/fabric-pipeline-configure-endpoint.png" alt-text="A screenshot showing how to select an endpoint once a connection is configured.":::

### Configure inputs and outputs for the batch endpoint

Configure inputs and outputs for the batch endpoint. *Inputs* to batch endpoints supply data and parameters needed to run the process. *Outputs* provide the paths to place the batch data.

The Azure Machine Learning batch pipeline in Fabric supports both [model deployments](how-to-use-batch-model-deployments.md) and [pipeline deployments](how-to-use-batch-pipeline-deployments.md). The number and type of inputs you provide depend on the deployment type. This example uses a model deployment that requires exactly one input and produces one output.

For more information on batch endpoint inputs and outputs, see [Understand inputs and outputs in batch endpoints](how-to-access-data-batch-endpoints-jobs.md#understand-inputs-and-outputs). 

#### Configure inputs

Configure the **Job inputs** section as follows:

1. Expand **Job inputs**, and select **New** to add a new input to your endpoint.
1. Name the input *input_data*. For your model deployment, you can use any name. For pipeline deployments, you must provide the exact name of the input that your model expects.
1. Select the caret next to the input to expand the **Name** and **Value** fields.
1. To indicate the type of input you're creating, enter *JobInputType* in the **Name** field.
1. To indicate that the input is a folder path, enter *UriFolder* in the **Value** field.
   >[!NOTE]
   >You need to use the type of input that your deployment expects. Other supported values for this field are *UriFile* for a file path or *Literal* for any literal value like a string or integer.
1. To add another property for this input, select the plus sign next to the property.
1. To indicate the path to the data, enter *Uri* in the **Name** field.
   > [!TIP]
   > If your input is of type *Literal*, enter *Value* in the **Name** field.
1. In the **Value** field, enter the path to the data, *azureml://datastores/trusted_blob/datasets/uci-heart-unlabeled-0*.

   This input path points to the storage account linked to both OneLake in Fabric and to Azure Machine Learning. You can also use a direct path to the storage account, such as *https://\<storage-account>.dfs.azure.com*. The path leads to the CSV files that contain the expected input data for the model deployed to the batch endpoint.

   :::image type="content" source="./media/how-to-use-batch-fabric/fabric-pipeline-configure-inputs.png" alt-text="A screenshot showing how to configure inputs in the endpoint.":::

If your endpoint requires more inputs, repeat the previous steps for each input.

#### Configure outputs

Configure the **Job outputs** section as follows:

1. Expand the **Job outputs** section, and select **New** to add a new output to your endpoint.
1. Name the output *output_data*. For your model deployment, you can use any name. For pipeline deployments, you must provide the exact name of the output that your model generates.
1. Select the caret next to the output to expand the **Name** and **Value** fields.
1. To indicate the type of output you're creating, enter *JobOutputType* in the **Name** field.
1. To indicate that the output is a file path, enter *UriFile* in the **Value** field. The other supported value for this field is *UriFolder*, for a folder path. *Literal* isn't supported for outputs.
1. To add another property for this output, select the plus sign next to the property.
1. To indicate the path to the data, enter *Uri* in the **Name** field.
1. Enter `@concat(@concat('azureml://datastores/trusted_blob/paths/endpoints', pipeline().RunId, 'predictions.csv')`, the path where the output should be placed, in the **Value** field.

   Azure Machine Learning batch endpoints support only datastore paths as outputs. Outputs must be unique to avoid conflicts, so you use a dynamic expression to construct the path.

   :::image type="content" source="./media/how-to-use-batch-fabric/fabric-pipeline-configure-outputs.png" alt-text="A screenshot showing how to configure outputs in the endpoint.":::

If your endpoint returns more outputs, repeat the previous steps for each output.

### Optionally configure job settings

You can also optionally configure job settings by expanding the **Job settings** section, selecting **New**, and adding any of the following properties.

#### For model deployments

| Name | Value |
|:----|:----|
|*MiniBatchSize*|The size of the batch.|
|*ComputeInstanceCount*|The number of compute instances to request from the deployment.|

#### For pipeline deployments

| Name | Value |
|:----|:----|
|*ContinueOnStepFailure*|Whether the pipeline should stop processing nodes after a failure.|
|*DefaultDatastore*|The default datastore to use for outputs.|
|*ForceRun*|Whether the pipeline should force all the components to run even if the output can be inferred from a previous run.|

Once configured, you can test the pipeline.

## Related content

* [Use low priority virtual machines in batch deployments](how-to-use-low-priority-batch.md)
* [Authorization on batch endpoints](how-to-authenticate-batch-endpoint.md)
* [Network isolation in batch endpoints](how-to-secure-batch-endpoint.md)
