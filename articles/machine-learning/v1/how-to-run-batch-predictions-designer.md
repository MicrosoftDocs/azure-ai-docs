---
title: Run Batch Predictions Using Designer
titleSuffix: Azure Machine Learning
description: Learn how to create a batch prediction pipeline. Deploy the pipeline as a parameterized web service, and trigger it from any HTTP library.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.author: scottpolly
author: lgayhardt
ms.reviewer: jturuk
ms.date: 06/16/2025
ms.topic: how-to
ms.custom:
  - UpdateFrequency5
  - designer
  - sfi-image-nochange
---

# Run batch predictions using Azure Machine Learning designer

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

In this article, you learn how to use the designer to create a batch prediction pipeline. Batch prediction lets you continuously score large datasets on demand by using a web service that can be triggered from any HTTP library.

In this how-to guide, you learn to do the following tasks:

> [!div class="checklist"]
> * Create and publish a batch inference pipeline.
> * Consume a pipeline endpoint.
> * Manage endpoint versions.

To learn how to set up batch scoring services using the SDK, see [Tutorial: Build an Azure Machine Learning pipeline for image classification](../tutorial-pipeline-python-sdk.md).

## Prerequisites

This how-to assumes you already have a training pipeline. For a guided introduction to the designer, complete [part one of the designer tutorial](tutorial-designer-automobile-price-train-score.md).

> [!IMPORTANT]
> If you don't see graphical elements mentioned in this document, such as buttons in studio or designer, you might not have the right level of permissions to the workspace. Contact your Azure subscription administrator to verify that you have been granted the correct level of access. For more information, see [Manage users and roles](../how-to-assign-roles.md).

## Create a batch inference pipeline

Your training pipeline must be run at least once to be able to create an inferencing pipeline.

1. Sign in to the Machine Learning studio, then select **Designer**.

1. Select the training pipeline that trains the model you want to use to make prediction.

1. Submit the pipeline.

    :::image type="content" source="./media/how-to-run-batch-predictions-designer/run-training-pipeline.png" alt-text="Screenshot showing the set up pipeline job with the experiment drop-down and submit button highlighted." lightbox= "./media/how-to-run-batch-predictions-designer/run-training-pipeline.png":::

You can select the job detail link to go to the job detail page, and after the training pipeline job completes, you can create a batch inference pipeline.

1. Select **Jobs** in the sidebar menu and choose your job. Above the canvas, select the dropdown **Create inference pipeline**. Select **Batch inference pipeline**.

    > [!NOTE]
    > Currently auto-generating inference pipeline only works for training pipeline built purely by the designer built-in components.

    :::image type="content" source="./media/how-to-run-batch-predictions-designer/create-batch-inference.png" alt-text="Screenshot of the create inference pipeline drop-down with batch inference pipeline highlighted." lightbox= "./media/how-to-run-batch-predictions-designer/create-batch-inference.png":::
    
    It creates a batch inference pipeline draft for you. The batch inference pipeline draft uses the trained model as **MD-** node and transformation as **TD-** node from the training pipeline job.

    You can also modify this inference pipeline draft to better handle your input data for batch inference.

     :::image type="content" source="./media/how-to-run-batch-predictions-designer/batch-inference-draft.png" alt-text="Screenshot showing a batch inference pipeline draft." lightbox= "./media/how-to-run-batch-predictions-designer/batch-inference-draft.png":::

### Add a pipeline input

To create predictions on new data, you can either manually connect a different dataset in this pipeline draft view or create an input parameter for your dataset. Inputs let you change the behavior of the batch inferencing process at runtime.

In this section, you create a pipeline input to specify a different dataset to make predictions on.

1. Double-click the dataset component.

1. A pane appears to the right of the canvas. At the bottom of the pane, select **Set as pipeline input**.

    Enter a name for the input, or accept the default value.

     :::image type="content" source="./media/how-to-run-batch-predictions-designer/create-pipeline-parameter.png" alt-text="Screenshot of cleaned dataset tab with set as pipeline input checked." lightbox= "./media/how-to-run-batch-predictions-designer/create-pipeline-parameter.png":::

1. Submit the batch inference pipeline.

## Publish your batch inference pipeline

Now you're ready to deploy the inference pipeline. This deploys the pipeline and makes it available for others to use.

1. On the job detail page, select the **Publish** button in the ribbon menu.

1. In the dialog that appears, select **Create new**.

1. Provide an endpoint name and optional description.

    Near the bottom of the dialog, you can see the input you configured with a default value of the dataset ID used during training.

1. Select **Publish**.

    :::image type="content" source="./media/how-to-run-batch-predictions-designer/publish-inference-pipeline.png" alt-text="Screenshot of set up published pipeline." lightbox= "./media/how-to-run-batch-predictions-designer/publish-inference-pipeline.png":::

## Consume an endpoint

Now, you have a published pipeline with a dataset parameter. The pipeline uses the trained model created in the training pipeline to score the dataset you provide as a parameter.

### Submit a pipeline job

In this section, you set up a manual pipeline job and alter the pipeline parameter to score new data.

1. After the deployment is complete, select **Pipelines** in the sidebar menu.

1. Select the **Pipeline endpoints** tab.

1. Select the name of the endpoint you created.

    :::image type="content" source="./media/how-to-run-batch-predictions-designer/manage-endpoints.png" alt-text="Screenshot of the pipeline endpoint tab." :::

1. Select **Published pipelines**.

    This screen shows all published pipelines published under this endpoint.

1. Select the pipeline you published.

    The pipeline details page shows you a detailed job history and connection string information for your pipeline.

1. Select **Submit** to create a manual run of the pipeline.

    :::image type="content" source="./media/how-to-run-batch-predictions-designer/submit-manual-run.png" alt-text="Screenshot of set up pipeline job with parameters highlighted." lightbox= "./media/how-to-run-batch-predictions-designer/submit-manual-run.png" :::

1. Change the parameter to use a different dataset.

1. Select **Submit** to run the pipeline.

### Use the REST endpoint

You can find information on how to consume pipeline endpoints and published pipeline in the **Endpoints** section.

You can find the REST endpoint of a pipeline endpoint in the job overview panel. By calling the endpoint, you're consuming its default published pipeline.

You can also consume a published pipeline in the **Published pipelines** page. Select a published pipeline and you can find the REST endpoint of it in the **Published pipeline overview** panel to the right of the graph. 

To make a REST call, you need an OAuth 2.0 bearer-type authentication header. See the following [tutorial section](../tutorial-pipeline-batch-scoring-classification.md#publish-and-run-from-a-rest-endpoint) for more detail on setting up authentication to your workspace and making a parameterized REST call.

## Versioning endpoints

The designer assigns a version to each subsequent pipeline that you publish to an endpoint. You can specify the pipeline version that you want to execute as a parameter in your REST call. If you don't specify a version number, the designer uses the default pipeline.

When you publish a pipeline, you can choose to make it the new default pipeline for that endpoint.

:::image type="content" source="./media/how-to-run-batch-predictions-designer/set-default-pipeline.png" alt-text="Screenshot of set up published pipeline with set as default pipeline for this endpoint checked." :::

You can also set a new default pipeline in the **Published pipelines** tab of your endpoint.

## Update pipeline endpoint

If you make some modifications in your training pipeline, you might want to update the newly trained model to the pipeline endpoint.

1. After your modified training pipeline completes successfully, go to the job detail page.

1. Right-click the **Train Model** component and select **Register data**.

    :::image type="content" source="./media/how-to-run-batch-predictions-designer/register-train-model-as-dataset.png" alt-text="Screenshot of the train model component options with register data highlighted." lightbox= "./media/how-to-run-batch-predictions-designer/register-train-model-as-dataset.png" :::

    Input a name and select a **File** type.

    :::image type="content" source="./media/how-to-run-batch-predictions-designer/register-train-model-as-dataset-2.png" alt-text="Screenshot of register as data asset with new data asset selected." lightbox= "./media/how-to-run-batch-predictions-designer/register-train-model-as-dataset-2.png" :::

1. Find the previous batch inference pipeline draft, or **Clone** the published pipeline into a new draft.

1. Replace the **MD-** node in the inference pipeline draft with the registered data in the preceding step.

    :::image type="content" source="./media/how-to-run-batch-predictions-designer/update-inference-pipeline-draft.png" alt-text="Screenshot of updating the inference pipeline draft with the registered data." :::

1. Updating data transformation node **TD-** is the same as the trained model.

1. Submit the inference pipeline with the updated model and transformation, and publish again.

## Related content

* [Tutorial: Train a no-code regression model using designer](tutorial-designer-automobile-price-train-score.md)
* [Publish machine learning pipelines](how-to-deploy-pipelines.md?view=azureml-api-1&preserve-view=true)
