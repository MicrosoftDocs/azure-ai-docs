---
title: Use Designer to Deploy No-Code Models
titleSuffix: Azure Machine Learning
description: Learn how to deploy a machine learning model to predict car prices with the Azure Machine Learning designer.
ms.reviewer: None
author: lgayhardt
ms.author: lagayhar
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: tutorial
ms.date: 06/09/2025
ms.custom: UpdateFrequency5, designer
---

# Tutorial: Deploy a machine learning model using designer

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

In [part one of this tutorial](tutorial-designer-automobile-price-train-score.md), you trained a linear regression model that predicts car prices. In this second part, you use the Azure Machine Learning designer to deploy the model so that others can use it.

> [!NOTE]
> Designer supports two types of components: classic prebuilt components (v1) and custom components (v2). These two types of components are NOT compatible. 
>
>Classic prebuilt components are intended primarily for data processing and traditional machine learning tasks like regression and classification. This type of component continues to be supported but will not have any new components added. 
>
>Custom components allow you to wrap your own code as a component. It supports sharing components across workspaces and seamless authoring across Studio, CLI v2, and SDK v2 interfaces. 
>
>For new projects, we highly suggest that you use custom components, which are compatible with Azure Machine Learning V2 and will keep receiving new updates. 
>
>This article applies to classic prebuilt components and isn't compatible with CLI v2 and SDK v2.

In this tutorial, you learn how to:

> [!div class="checklist"]
> * Create a real-time inference pipeline.
> * Create an inferencing cluster.
> * Deploy the real-time endpoint.
> * Test the real-time endpoint.

## Prerequisites

Complete [part one of the tutorial](tutorial-designer-automobile-price-train-score.md) to learn how to train and score a machine learning model in the designer.

> [!IMPORTANT]
> If you don't see graphical elements mentioned in this document, such as buttons in studio or designer, you might not have the right level of permissions to the workspace. Contact your Azure subscription administrator to verify that you have been granted the correct level of access. For more information, see [Manage users and roles](../how-to-assign-roles.md).

## Create a real-time inference pipeline

To deploy your pipeline, you must first convert the training pipeline into a real-time inference pipeline. This process removes training components and adds web service inputs and outputs to handle requests.

> [!NOTE]
> The **Create inference pipeline** feature supports training pipelines that only contain the designer built-in components and that have a component like **Train Model** that outputs the trained model.

### Create a real-time inference pipeline

1. Select **Jobs** from the sidebar menu, then open the pipeline job that you created. On the detail page, above the pipeline canvas, select the ellipses **...** then choose **Create inference pipeline** > **Real-time inference pipeline**.

     :::image type="content" source="media/tutorial-designer-automobile-price-deploy/create-real-time-inference.png" alt-text="Screenshot of create inference pipeline in pipeline job detail page." lightbox="media/tutorial-designer-automobile-price-deploy/create-real-time-inference.png":::

    Your new pipeline now looks like this:

    :::image type="content" source="media/tutorial-designer-automobile-price-deploy/real-time-inference-pipeline.png" alt-text="Screenshot showing the expected configuration of the pipeline after preparing it for deployment." lightbox="media/tutorial-designer-automobile-price-deploy/real-time-inference-pipeline.png":::

    When you select **Create inference pipeline**, several things happen:

    * The trained model is stored as a **Dataset** component in the component palette. You can find it under **My Datasets**.
    * Training components like **Train Model** and **Split Data** are removed.
    * The saved trained model is added back into the pipeline.
    * **Web Service Input** and **Web Service Output** components are added. These components show where user data enters the pipeline and where data is returned.

    > [!NOTE]
    > By default, the **Web Service Input** expects the same data schema as the component output data that connects to the same downstream port. In this sample, **Web Service Input** and **Automobile price data (Raw)** connect to the same downstream component, so **Web Service Input** expects the same data schema as **Automobile price data (Raw)** and target variable column `price` is included in the schema.
    > However, when you score the data, you won't know the target variable values. In that case, you can remove the target variable column in the inference pipeline using the **Select Columns in Dataset** component. Make sure that the output of **Select Columns in Dataset** removing target variable column is connected to the same port as the output of the **Web Service Input** component.

1. Select **Configure & Submit**, and use the same compute target and experiment that you used in part one.

    If this is the first job, it might take up to 20 minutes for your pipeline to finish running. The default compute settings have a minimum node size of 0, which means that the designer must allocate resources after being idle. Repeated pipeline jobs take less time since the compute resources are already allocated. Additionally, the designer uses cached results for each component to further improve efficiency.

1. Go to the real-time inference pipeline job detail by selecting **Job detail** in the left pane.

1. Select **Deploy** in the job detail page.

     :::image type="content" source="./media/tutorial-designer-automobile-price-deploy/deploy-in-job-detail-page.png" alt-text="Screenshot showing deploying in job detail page." lightbox="./media/tutorial-designer-automobile-price-deploy/deploy-in-job-detail-page.png":::

## Create an inferencing cluster

In the dialog box that appears, you can select from any existing Azure Kubernetes Service (AKS) clusters to deploy your model to. If you don't have an AKS cluster, use the following steps to create one.

1. Go to the **Compute** page by selecting **Compute** in the sidebar menu.

1. On the navigation ribbon, select **Kubernetes Clusters**. Then select **+ New** > **AksCompute**.

    :::image type="content" source="./media/tutorial-designer-automobile-price-deploy/new-inference-cluster.png" alt-text="Screenshot showing how to get to the new inference cluster pane.":::

1. In the inference cluster pane, configure a new Kubernetes Service.

1. Select a nearby region that's available for the **Region**.

1. On the next screen, enter *aks-compute* for the **Compute name**.

1. Select **Create**.

    > [!NOTE]
    > It takes approximately 15 minutes to create a new AKS service. You can check the provisioning state on the **Inference Clusters** page.

## Deploy the real-time endpoint

After your AKS service finishes provisioning, return to the real-time inferencing pipeline to complete deployment.

1. Select **Deploy** above the canvas.

1. Select **Deploy new real-time endpoint**.

1. Select the AKS cluster you created.

     :::image type="content" source="./media/tutorial-designer-automobile-price-deploy/setup-endpoint.png" alt-text="Screenshot showing how to set up a new real-time endpoint.":::

    You can also change the **Advanced** settings for your real-time endpoint.

    |Advanced setting|Description|
    |---|---|
    |Enable Application Insights diagnostics and data collection| Allows Azure Application Insights to collect data from the deployed endpoints. <br> By default: false |
    |Scoring timeout| A timeout in milliseconds to enforce for scoring calls to the web service. <br> By default: 60000|
    |Auto scale enabled| Allows autoscaling for the web service.<br> By default: true|
    |Min replicas| The minimum number of containers to use when autoscaling this web service.<br> By default: 1|
    |Max replicas| The maximum number of containers to use when autoscaling this web service.<br> By default: 10|
    |Target utilization|The target utilization (as a percentage) that the autoscaler should attempt to maintain for this web service.<br> By default: 70|
    |Refresh period|How often (in seconds) the autoscaler attempts to scale this web service.<br> By default: 1|
    |CPU reserve capacity|The number of CPU cores to allocate for this web service.<br> By default: 0.1|
    |Memory reserve capacity|The amount of memory (in GB) to allocate for this web service.<br> By default: 0.5|

1. Select **Deploy**.

    A success notification from the notification center appears after deployment finishes. It might take a few minutes.

    :::image type="content" source="media/tutorial-designer-automobile-price-deploy/deploy-notification.png" alt-text="Screenshot showing deployment notification." lightbox="media/tutorial-designer-automobile-price-deploy/deploy-notification.png":::

> [!TIP]
> You can also deploy to Azure Container Instance if you select **Azure Container Instance** for **Compute type** in the real-time endpoint setting box.
> Azure Container Instance is used for testing or development. Use Azure Container Instance for low-scale CPU-based workloads that require less than 48 GB of RAM.

## Test the real-time endpoint

After deployment finishes, you can view your real-time endpoint by going to the **Endpoints** page.

1. Select **Endpoints** on the sidebar menu, then select the endpoint you deployed.

    - In the **Details** tab, you can see more information such as the REST URI, Swagger definition, status, and tags.

    - In the **Consume** tab, you can find sample consumption code, security keys, and set authentication methods.

    - In the **Deployment logs** tab, you can find the detailed deployment logs of your real-time endpoint.

1. To test your endpoint, go to the **Test** tab. From here, you can enter test data and select **Test** verify the output of your endpoint.

## Update the real-time endpoint

You can update the online endpoint with new model trained in the designer. On the online endpoint detail page, find your previous training pipeline job and inference pipeline job.

1. You can find and modify your training pipeline draft in the designer homepage.

    Or you can open the training pipeline job link and then clone it into a new pipeline draft to continue editing.

    :::image type="content" source="media/tutorial-designer-automobile-price-deploy/endpoint-train-job-link.png" alt-text="Screenshot showing training job link in endpoint detail page." lightbox="media/tutorial-designer-automobile-price-deploy/endpoint-train-job-link.png":::

1. After you submit the modified training pipeline, go to the job detail page.

1. When the job completes, right-click **Train Model** and select **Register data**.

     :::image type="content" source="media/how-to-run-batch-predictions-designer/register-train-model-as-dataset.png" alt-text="Screenshot showing register trained model as dataset." lightbox="media/how-to-run-batch-predictions-designer/register-train-model-as-dataset.png":::

    Input a name and select **File** type.

    :::image type="content" source="./media/how-to-run-batch-predictions-designer/register-train-model-as-dataset-2.png" alt-text="Screenshot of register as a data asset with new data asset selected." lightbox="./media/how-to-run-batch-predictions-designer/register-train-model-as-dataset-2.png":::

1. After the dataset registers successfully, open your inference pipeline draft, or clone the previous inference pipeline job into a new draft. In the inference pipeline draft, replace the previous trained model shown as **MD-xxxx** node connected to the **Score Model** component with the newly registered dataset.

    :::image type="content" source="media/tutorial-designer-automobile-price-deploy/modify-inference-pipeline.png" alt-text="Screenshot showing how to modify inference pipeline." lightbox="media/tutorial-designer-automobile-price-deploy/modify-inference-pipeline.png":::

1. If you need to update the data preprocessing part in your training pipeline, and would like to update that into the inference pipeline, the processing is similar to the preceding steps.

    You just need to register the transformation output of the transformation component as dataset.

    Then, manually replace the **TD-xxxx** component in the inference pipeline with the registered dataset.

    :::image type="content" source="media/tutorial-designer-automobile-price-deploy/replace-td-module.png" alt-text="Screenshot showing how to replace transformation component." lightbox="media/tutorial-designer-automobile-price-deploy/replace-td-module.png":::

1. After modifying your inference pipeline with the newly trained model or transformation, submit it. When the job is completed, deploy it to the existing online endpoint deployed previously.

    :::image type="content" source="./media/tutorial-designer-automobile-price-deploy/deploy-to-existing-endpoint.png" alt-text="Screenshot showing how to replace existing real-time endpoint." lightbox="./media/tutorial-designer-automobile-price-deploy/deploy-to-existing-endpoint.png":::

## Limitations

* Due to datastore access limitation, if your inference pipeline contains **Import Data** or **Export Data** components, they're autoremoved when deployed to a real-time endpoint.

* If you have datasets in the real-time inference pipeline and want to deploy to a real-time endpoint, currently this flow only supports datasets registered from **Blob** datastore. If you want to use datasets from other type datastores, you can use **Select Column** to connect with your initial dataset with settings of selecting all columns, register the outputs of **Select Column** as File dataset and then replace the initial dataset in the real-time inference pipeline with this newly registered dataset.

* If your inference graph contains **Enter Data Manually** component that isn't connected to the same port as **Web Service Input** component, the **Enter Data Manually** component isn't executed during HTTP call processing. A workaround is to register the outputs of that **Enter Data Manually** component as a dataset, then in the inference pipeline draft, replace the **Enter Data Manually** component with the registered dataset.

    :::image type="content" source="media/tutorial-designer-automobile-price-deploy/real-time-inference-pipeline-limitation.png" alt-text="Screenshot showing how to modify inference pipeline containing enter data manually component." lightbox="media/tutorial-designer-automobile-price-deploy/real-time-inference-pipeline-limitation.png":::

## Clean up resources

[!INCLUDE [aml-ui-cleanup](../includes/aml-ui-cleanup.md)]

## Related content

In this tutorial, you learned how to create, deploy, and consume a machine learning model in the designer. To learn more about how you can use the designer, see the following articles:

- [Example pipelines & datasets for Azure Machine Learning designer](samples-designer.md)
- [Use Azure Machine Learning studio in an Azure virtual network](../how-to-enable-studio-virtual-network.md)
