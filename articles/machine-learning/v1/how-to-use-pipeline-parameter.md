---
title: Use Pipeline Parameters to Build Versatile Pipelines
titleSuffix: Azure Machine Learning
description: Use pipeline parameters in the Azure Machine Learning designer.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.author: lagayhar
author: lgayhardt
ms.reviewer: keli19
ms.date: 06/12/2025
ms.topic: how-to
ms.custom: UpdateFrequency5, designer

#customer intent: As a machine learning engineer, I want to use pipleline parameters so that I can dynamically set parameter values at runtime.
---

# Use pipeline parameters in the designer to build versatile pipelines

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

This article describes how to use pipeline parameters to build flexible pipelines in the Azure Machine Learning designer. Pipeline parameters enable you to dynamically set values at runtime so you can encapsulate pipeline logic and reuse assets.

Pipeline parameters are especially useful when you resubmit a pipeline job, [retrain models](how-to-retrain-designer.md), or [perform batch predictions](how-to-run-batch-predictions-designer.md).

In this article, you learn how to do the following:

> [!div class="checklist"]
> * Create pipeline parameters.
> * Delete and manage pipeline parameters.
> * Supply pipeline paramenters when you trigger pipeline jobs.

## Prerequisites

* An Azure Machine Learning workspace. See [Create workspace resources](../quickstart-create-resources.md).

* For a guided introduction to the designer, complete the [designer tutorial](tutorial-designer-automobile-price-train-score.md). 

> [!IMPORTANT]
> If you don't see the UI elements mentioned in this article, such as buttons in studio or designer, you might not have the right level of permissions for the workspace. Contact your Azure subscription administrator to verify that you're granted the correct level of access. For more information, see [Manage users and roles](../how-to-assign-roles.md).

## Create a pipeline parameter

There are three ways to create a pipeline parameter in the designer:
- Create a pipeline parameter in the settings panel and bind it to a component.
- Promote a component parameter to a pipeline parameter.
- Promote a dataset to a pipeline parameter.

> [!NOTE]
> Pipeline parameters support only basic data types, like `int`, `float`, and `string`.

### Option 1: Create a pipeline parameter in the settings panel

In this section, you create a pipeline parameter in the settings panel.

In this example, you create a pipeline parameter that defines how a pipeline fills in missing data by using the **Clean missing data** component.

1. Next to the name of your pipeline draft, select the gear button to open the **Settings** panel.

1. In the **Pipeline parameters** section, select the **+** button.

1. Enter a name for the parameter and a default value. 

   For example, enter `replace-missing-value` as parameter name and `0` as the default value.

   :::image type="content" source="media/how-to-use-pipeline-parameter/create-pipeline-parameter.png" alt-text="Screenshot that shows how to create a pipeline parameter." lightbox ="media/how-to-use-pipeline-parameter/create-pipeline-parameter.png":::

After you create a pipeline parameter, you must [attach it to the component parameter](#attach-component-parameter-to-pipeline-parameter) that you want to dynamically set.

### Option 2: Promote a component parameter

The easiest way to create a pipeline parameter for a component value is to promote a component parameter. Use the following steps to promote a component parameter to a pipeline parameter:

1. Select the component you want to attach a pipeline parameter to.
1. In the component detail pane, hover over the parameter you want to specify.
1. Select the ellipsis button (**...**) that appears.
1. Select **Add to pipeline parameter**.

   :::image type="content" source="media/how-to-use-pipeline-parameter/promote-module-para-to-pipeline-para.png" alt-text="Screenshot that shows how to promote a component parameter to a pipeline parameter." lightbox ="media/how-to-use-pipeline-parameter/promote-module-para-to-pipeline-para.png":::

1. Enter a parameter name and a default value.
1. Select **Save**.

You can now specify new values for this parameter anytime you submit the pipeline.

### Option 3: Promote a dataset to a pipeline parameter

If you want to submit your pipeline with variable datasets, you need to promote your dataset to a pipeline parameter:

1. Select the dataset you want to turn into a pipeline parameter.

1. In the details pane of the dataset, select **Set as pipeline parameter**.

   :::image type="content" source="media/how-to-use-pipeline-parameter/set-dataset-as-pipeline-parameter.png" alt-text="Screenshot that shows how to set dataset as pipeline parameter." lightbox ="media/how-to-use-pipeline-parameter/set-dataset-as-pipeline-parameter.png":::

You can now specify a different dataset by using the pipeline parameter the next time you run the pipeline.

## Attach a component parameter to or detach a component pipeline from a pipeline parameter 

In this section, you learn how to attach a component parameter to a pipeline parameter and how to detach a component parameter from a pipeline parameter.

### Attach component parameter to pipeline parameter

You can attach the component parameters of duplicated components to the same pipeline parameter if you want to alter the value one time when you trigger the pipeline job.

In the following example, the **Clean Missing Data** component is duplicated. For each **Clean Missing Data** component, attach a **Replacement value** to the pipeline parameter **replace-missing-value**:

1. Select the **Clean Missing Data** component.

1. In the component detail pane, to the right of the canvas, set the **Cleaning mode** to **Custom substitution value**.

1. Hover over the **Replacement value** field.

1. Select the ellipsis button (**...**) that appears.

1. Select the pipeline parameter `replace-missing-value`.

   :::image type="content" source="media/how-to-use-pipeline-parameter/attach-replace-value-to-pipeline-parameter.png" alt-text="Screenshot that shows how to attach a pipeline parameter." lightbox ="media/how-to-use-pipeline-parameter/attach-replace-value-to-pipeline-parameter.png":::

You have successfully attached the **Replacement value** field to your pipeline parameter. 

### Detach a component parameter from a pipeline parameter

When you detach a **Replacement value** from a pipeline parameter, it's not actionable.

You can detach a component parameter from a pipeline parameter by selecting the ellipsis button (**...**) next to the component parameter and then selecting **Detach from pipeline parameter**.

:::image type="content" source="media/how-to-use-pipeline-parameter/non-actionable-module-parameter.png" alt-text="Screenshot that shows how to detach a component parameter." lightbox ="media/how-to-use-pipeline-parameter/non-actionable-module-parameter.png":::

## Update and delete pipeline parameters

In this section, you learn how to update and delete pipeline parameters.

### Update pipeline parameters

Complete the following steps to update a component pipeline parameter:

1. At the top of the canvas, select the gear icon.
1. In the **Pipeline parameters** section, you can view and update the name and default value for all of your pipeline parameters.

### Delete a dataset pipeline parameter

Complete the following steps to delete a dataset pipeline parameter:

1. Select the dataset component.
1. Clear the **Set as pipeline parameter** option.

### Delete component pipeline parameters

Complete the following steps to delete a component pipeline parameter:

1. At the top of the canvas, select the gear icon.

1. Select the ellipsis button (**...**) next to the pipeline parameter.

    This view displays components that the pipeline parameter is attached to.

    :::image type="content" source="media/how-to-use-pipeline-parameter/delete-pipeline-parameter2.png" alt-text="Screenshot that shows the current pipeline parameter applied to a component." lightbox ="media/how-to-use-pipeline-parameter/delete-pipeline-parameter2.png":::

1. Select **Delete parameter**.

    > [!NOTE]
    > Deleting a pipeline parameter causes all attached component parameters to be detached. The values of detached component parameters will keep current pipeline parameter values.

## Supply pipeline parameters when you trigger a pipeline job

In this section, you learn how to supply pipeline paramaters when you submit a pipeline job.

### Resubmit a pipeline job

After you submit a pipeline with pipeline parameters, you can resubmit the job with different parameters:

1. Go to pipeline detail page. In the **Pipeline run overview** pane, you can check current pipeline parameters and values.
1. Select **Resubmit**.
1. In the **Set up pipleine run** window, specify your new pipeline parameters. 

 :::image type="content" source="media/how-to-use-pipeline-parameter/resubmit-pipeline-run.png" alt-text="Screenshot that shows how to resubmit a pipeline with pipeline parameters." lightbox ="media/how-to-use-pipeline-parameter/resubmit-pipeline-run.png":::

### Use published pipelines

You can also publish a pipeline to use its pipeline parameters. A *published pipeline* is a pipeline that has been deployed to a compute resource. Client applications can invoke the pipeline via a REST endpoint.

Published endpoints are especially useful for retraining and batch prediction scenarios. For more information, see [How to retrain models in the designer](how-to-retrain-designer.md) or [Run batch predictions in the designer](how-to-run-batch-predictions-designer.md).

## Next steps

In this article, you learned how to create pipeline parameters in the designer. Next, see how you can use pipeline parameters to [retrain models](how-to-retrain-designer.md) or perform [batch predictions](how-to-run-batch-predictions-designer.md).

You can also learn how to [use pipelines programmatically with the SDK v1](how-to-deploy-pipelines.md?view=azureml-api-1&preserve-view=true).
