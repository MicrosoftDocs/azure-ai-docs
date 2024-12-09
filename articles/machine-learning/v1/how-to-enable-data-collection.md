---
title: Collect data on your production models
titleSuffix: Azure Machine Learning
description: Learn how to collect data from an Azure Machine Learning model deployed on an Azure Kubernetes Service (AKS) cluster.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.reviewer: None
ms.author: sgilley
author: sdgilley
ms.date: 08/16/2022
ms.topic: how-to
ms.custom: UpdateFrequency5, data4ml, sdkv1
---
# Collect data from models in production

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

This article shows how to collect data from an Azure Machine Learning model deployed on an Azure Kubernetes Service (AKS) cluster. The collected data is then stored in Azure Blob storage.

Once collection is enabled, the data you collect helps you:

* [Monitor data drifts](how-to-monitor-datasets.md) on the production data you collect.

* Analyze collected data using [Power BI](#powerbi) or [Azure Databricks](#databricks)

* Make better decisions about when to retrain or optimize your model.

* Retrain your model with the collected data.

## Limitations

* The model data collection feature can only work with Ubuntu 18.04 image.

>[!IMPORTANT]
>
> As of 03/10/2023, the Ubuntu 18.04 image is now deprecated. **Support for Ubuntu 18.04 images will be dropped starting January 2023 when it reaches EOL on April 30, 2023.** 
>
> The MDC feature is incompatible with any other image than Ubuntu 18.04, which is no available after the Ubuntu 18.04 image is deprecated.
>
> mMore information you can refer to:
> * [openmpi3.1.2-ubuntu18.04 release-notes](https://github.com/Azure/AzureML-Containers/blob/master/base/cpu/openmpi3.1.2-ubuntu18.04/release-notes.md)
> * [data science virtual machine release notes](../data-science-virtual-machine/release-notes.md#september-20-2022)

>[!NOTE]
>
> The data collection feature is currently in preview, any preview features are not recommended for production workloads.

## What is collected and where it goes

The following data can be collected:

* Model input data from web services deployed in an AKS cluster. Voice audio, images, and video are *not* collected.
  
* Model predictions using production input data.

>[!NOTE]
> Preaggregation and precalculations on this data are not currently part of the collection service.

The output is saved in Blob storage. Because the data is added to Blob storage, you can choose your favorite tool to run the analysis.

The path to the output data in the blob follows this syntax:

```
/modeldata/<subscriptionid>/<resourcegroup>/<workspace>/<webservice>/<model>/<version>/<designation>/<year>/<month>/<day>/data.csv
# example: /modeldata/1a2b3c4d-5e6f-7g8h-9i10-j11k12l13m14/myresourcegrp/myWorkspace/aks-w-collv9/best_model/10/inputs/2018/12/31/data.csv
```

>[!NOTE]
> In versions of the Azure Machine Learning SDK for Python earlier than version 0.1.0a16, the `designation` argument is named `identifier`. If you developed your code with an earlier version, you need to update it accordingly.

## Prerequisites

- If you don't have an Azure subscription, create a
 [free account](https://azure.microsoft.com/free/) before you begin.

- An Azure Machine Learning workspace, a local directory containing your scripts, and the Azure Machine Learning SDK for Python must be installed. To learn how to install them, see [How to configure a development environment](how-to-configure-environment.md).

- You need a trained machine-learning model to be deployed to AKS. If you don't have a model, see the [Train image classification model](../tutorial-train-deploy-notebook.md) tutorial.

- You need an AKS cluster. For information on how to create one and deploy to it, see [Deploy machine learning models to Azure](how-to-deploy-and-where.md).

- [Set up your environment](how-to-configure-environment.md) and install the [Azure Machine Learning Monitoring SDK](/python/api/overview/azure/ml/install).

- Use a docker image based on Ubuntu 18.04, which is shipped with `libssl 1.0.0`, the essential dependency of [modeldatacollector](/python/api/azureml-monitoring/azureml.monitoring.modeldatacollector.modeldatacollector). You can refer to [prebuilt images](../concept-prebuilt-docker-images-inference.md).

## Enable data collection

You can enable [data collection](/python/api/azureml-monitoring/azureml.monitoring.modeldatacollector.modeldatacollector) regardless of the model you deploy through Azure Machine Learning or other tools.

To enable data collection, you need to:

1. Open the scoring file.

1. Add the following code at the top of the file:

   ```python 
   from azureml.monitoring import ModelDataCollector
   ```

1. Declare your data collection variables in your `init` function:

    ```python
    global inputs_dc, prediction_dc
    inputs_dc = ModelDataCollector("best_model", designation="inputs", feature_names=["feat1", "feat2", "feat3", "feat4", "feat5", "feat6"])
    prediction_dc = ModelDataCollector("best_model", designation="predictions", feature_names=["prediction1", "prediction2"])
    ```

    *CorrelationId* is an optional parameter. You don't need to use it if your model doesn't require it. Use of *CorrelationId* does help you more easily map with other data, such as *LoanNumber* or *CustomerId*.
    
    The *Identifier* parameter is later used for building the folder structure in your blob. You can use it to differentiate raw data from processed data.

1. Add the following lines of code to the `run(input_df)` function:

    ```python
    data = np.array(data)
    result = model.predict(data)
    inputs_dc.collect(data) #this call is saving our input data into Azure Blob
    prediction_dc.collect(result) #this call is saving our prediction data into Azure Blob
    ```

1. Data collection is *not* automatically set to **true** when you deploy a service in AKS. Update your configuration file, as in the following example:

    ```python
    aks_config = AksWebservice.deploy_configuration(collect_model_data=True)
    ```

    You can also enable Application Insights for service monitoring by changing this configuration:

    ```python
    aks_config = AksWebservice.deploy_configuration(collect_model_data=True, enable_app_insights=True)
    ```

1. To create a new image and deploy the machine learning model, see [Deploy machine learning models to Azure](how-to-deploy-and-where.md).

1. Add the 'Azure-Monitoring' pip package to the conda-dependencies of the web service environment:
  ```Python
    env = Environment('webserviceenv')
    env.python.conda_dependencies = CondaDependencies.create(conda_packages=['numpy'],pip_packages=['azureml-defaults','azureml-monitoring','inference-schema[numpy-support]'])
  ```


## Disable data collection

You can stop collecting data at any time. Use Python code to disable data collection.

  ```python 
  ## replace <service_name> with the name of the web service
  <service_name>.update(collect_model_data=False)
  ```

## Validate and analyze your data

You can choose a tool of your preference to analyze the data collected in your Blob storage.

### Quickly access your blob data

1. Sign in to [Azure portal](https://portal.azure.com).

1. Open your workspace.

1. Select **Storage**.

    :::image type="content" source="./media/how-to-enable-data-collection/StorageLocation.png" alt-text="Screenshot showing selection of the storage option." lightbox="./media/how-to-enable-data-collection/StorageLocation.png":::

1. Follow the path to the blob's output data with this syntax:

   ```
   /modeldata/<subscriptionid>/<resourcegroup>/<workspace>/<webservice>/<model>/<version>/<designation>/<year>/<month>/<day>/data.csv
   # example: /modeldata/1a2b3c4d-5e6f-7g8h-9i10-j11k12l13m14/myresourcegrp/myWorkspace/aks-w-collv9/best_model/10/inputs/2018/12/31/data.csv
   ```

### <a id="powerbi"></a> Analyze model data using Power BI

1. Download and open [Power BI Desktop](https://www.powerbi.com).

1. Select **Get Data** and select [**Azure Blob Storage**](/power-bi/desktop-data-sources).

    :::image type="content" source="./media/how-to-enable-data-collection/power-bi-blob.png" alt-text="Screenshot showing the Power BI blob setup." lightbox="./media/how-to-enable-data-collection/power-bi-blob.png":::

1. Add your storage account name and enter your storage key. You can find this information by selecting **Settings** > **Access keys** in your blob.

1. Select the **model data** container and select **Edit**.

    :::image type="content" source="./media/how-to-enable-data-collection/power-bi-navigator.png" alt-text="Screenshot showing the Power BI Navigator." lightbox="./media/how-to-enable-data-collection/power-bi-navigator.png":::

1. In the query editor, click under the **Name** column and add your storage account.

1. Enter your model path into the filter. If you want to look only into files from a specific year or month, just expand the filter path. For example, to look only into March data, use this filter path:

   /modeldata/\<subscriptionid>/\<resourcegroupname>/\<workspacename>/\<webservicename>/\<modelname>/\<modelversion>/\<designation>/\<year>/3

1. Filter the data that is relevant to you based on **Name** values. If you stored predictions and inputs, you need to create a query for each.

1. Select the downward double arrows next to the **Content** column heading to combine the files.

    :::image type="content" source="./media/how-to-enable-data-collection/power-bi-content.png" alt-text="Screenshot showing the Power BI Content." lightbox="./media/how-to-enable-data-collection/power-bi-content.png":::

1. Select **OK**. The data preloads.

    :::image type="content" source="./media/how-to-enable-data-collection/power-bi-combine.png" alt-text="Screenshot showing the Power BI Combine Files." lightbox="./media/how-to-enable-data-collection/power-bi-combine.png":::

1. Select **Close and Apply**.

1. If you added inputs and predictions, your tables are automatically ordered by **RequestId** values.

1. Start building your custom reports on your model data.

### <a id="databricks"></a> Analyze model data using Azure Databricks

1. Create an [Azure Databricks workspace](/azure/databricks/scenarios/quickstart-create-databricks-workspace-portal).

1. Go to your Databricks workspace.

1. In your Databricks workspace, select **Upload Data**.

    :::image type="content" source="./media/how-to-enable-data-collection/databricks-upload.png" alt-text="Screenshot showing selection of Databricks Upload Data option." lightbox="./media/how-to-enable-data-collection/databricks-upload.png":::

1. Select **Create New Table** and select **Other Data Sources** > **Azure Blob Storage** > **Create Table in Notebook**.

    :::image type="content" source="./media/how-to-enable-data-collection/databricks-table.png" alt-text="Screenshot showing Databricks table creation." lightbox="./media/how-to-enable-data-collection/databricks-table.png":::

1. Update the location of your data. Here is an example:

    ```
    file_location = "wasbs://mycontainer@storageaccountname.blob.core.windows.net/*/*/data.csv" 
    file_type = "csv"
    ```
    
    :::image type="content" source="./media/how-to-enable-data-collection/databricks-setup.png" alt-text="Screenshot showing the Databricks setup." lightbox="./media/how-to-enable-data-collection/databricks-setup.png":::

1. Follow the steps on the template to view and analyze your data.

## Next steps

[Detect data drift](how-to-monitor-datasets.md) on the data you have collected.
