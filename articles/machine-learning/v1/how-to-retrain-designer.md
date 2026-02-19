---
title: Use Pipeline Inputs to Retrain Models in Designer
titleSuffix: Azure Machine Learning
description: Learn how to retrain models by using published pipelines and pipeline inputs in Azure Machine Learning designer.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.author: scottpolly
author: lgayhardt
ms.reviewer: jturuk
ms.date: 06/11/2025
ms.topic: how-to
ms.custom: UpdateFrequency5, designer
---

# Use pipeline inputs to retrain models in the designer

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

In this how-to article, you learn how to use Azure Machine Learning designer to retrain a machine learning model using pipeline inputs. You can use published pipelines to automate your workflow and set inputs to train your model on new data. Pipeline inputs let you reuse existing pipelines for different jobs.  

In this article, you learn how to:

> [!div class="checklist"]
> * Train a machine learning model.
> * Create a pipeline input.
> * Publish your training pipeline.
> * Retrain your model with new inputs.

## Prerequisites

* An Azure Machine Learning workspace
* Complete part 1 of this how-to series, [Transform data in the designer](how-to-designer-transform-data.md)

> [!IMPORTANT]
> If you don't see graphical elements mentioned in this document, such as buttons in studio or designer, you might not have the right level of permissions to the workspace. Contact your Azure subscription administrator to verify that you have been granted the correct level of access. For more information, see [Manage users and roles](../how-to-assign-roles.md).

This article also assumes that you have some knowledge of building pipelines in the designer. For a guided introduction, complete the [tutorial](tutorial-designer-automobile-price-train-score.md). 

### Sample pipeline

The pipeline used in this article is an altered version of the [Income prediction](samples-designer.md#classification) sample pipeline. The pipeline uses the [Import Data](../algorithm-module-reference/import-data.md) component instead of the sample dataset to show you how to train models using your own data.

If you're using the pipeline that you built in part one of this series, add the other components in the following example.

:::image type="content" source="./media/how-to-retrain-designer/modified-sample-pipeline.png" alt-text="Screenshot that shows the modified sample pipeline with a box highlighting the Import Data component." lightbox="./media/how-to-retrain-designer/modified-sample-pipeline.png":::

## Create a pipeline input

Pipeline inputs are used to build versatile pipelines that can be resubmitted later with varying values. You can create pipeline inputs to dynamically set variables at runtime. Some common scenarios involve updating datasets or hyper-parameters for retraining.

Pipeline inputs can be added to data source or component parameters in a pipeline. When the pipeline is resubmitted, the values of these inputs can be specified.

For this example, you change the training data path from a fixed value to an input, so that you can retrain your model on different data. You can also add other component parameters as pipeline inputs according to your use case.

1. Double-click the **Import Data** component.

    > [!NOTE]
    > This example uses the **Import Data** component to access data in a registered datastore. However, you can follow similar steps if you use alternative data access patterns.

1. In the component detail pane, select your data source.

1. Enter the path to your data. You can also select **Browse path** to browse your file tree. 

1. Mouseover the **Path** field, and select the ellipses above the **Path** field that appear.

1. Select **Add to pipeline input**.

1. Provide an input name and a value.

   :::image type="content" source="media/how-to-retrain-designer/add-pipeline-input.png" alt-text="Screenshot that shows how to create a pipeline parameter." lightbox="media/how-to-retrain-designer/add-pipeline-input.png":::

1. Select **Save**.

   > [!NOTE]
   > You can also detach a component parameter from pipeline input in the component detail pane, similar to adding pipeline inputs.
   >
   > You can inspect and edit your pipeline inputs by selecting the **Settings** gear icon next to the title of your pipeline draft. 
   >    - After detaching, you can delete the pipeline input in the **Settings** pane.
   >    - You can also add a pipeline input in the **Settings** pane, and then apply it on some component parameter.

1. Submit the pipeline job.

## Publish a training pipeline

Publish a pipeline to a pipeline endpoint to easily reuse your pipelines in the future. A pipeline endpoint creates a REST endpoint to invoke pipeline in the future. In this example, your pipeline endpoint lets you reuse your pipeline to retrain a model on different data.

1. Select **Publish** above the designer canvas.

1. Select or create a pipeline endpoint.

   > [!NOTE]
   > You can publish multiple pipelines to a single endpoint. Each pipeline in a given endpoint is given a version number, which you can specify when you call the pipeline endpoint.

1. Select **Publish**.

## Retrain your model

Now that you have a published training pipeline, you can use it to retrain your model on new data. You can submit jobs from a pipeline endpoint from the studio workspace or programmatically.

### Submit jobs by using the studio portal

Use the following steps to submit a parameterized pipeline endpoint job from the studio portal:

1. Select **Endpoints** on the sidebar menu.

1. Select the **Pipeline endpoints** tab. Then, select your pipeline endpoint.

1. Select the **Published pipelines** tab. Then, select the pipeline version that you want to run.

1. Select **Submit**.

1. In the setup dialog box, you can specify the parameter values for the job. For this example, update the data path to train your model using a non-US dataset.

:::image type="content" source="./media/how-to-retrain-designer/published-pipeline-run.png" alt-text="Screenshot that shows how to set up a parameterized pipeline job in the designer." lightbox="./media/how-to-retrain-designer/published-pipeline-run.png":::

### Submit jobs by using code

You can find the REST endpoint of a published pipeline in the overview panel. By calling the endpoint, you can retrain the published pipeline.

To make a REST call, you need an OAuth 2.0 bearer-type authentication header. For information about setting up authentication to your workspace and making a parameterized REST call, see [Use REST to manage resources](../how-to-manage-rest.md).

## Related content

- [Tutorial: Train a no-code regression model using designer](tutorial-designer-automobile-price-train-score.md)

- [Publish machine learning pipelines](how-to-deploy-pipelines.md)
