---
title: Use Pipeline Inputs to Build Versatile Pipelines
titleSuffix: Azure Machine Learning
description: Use pipeline inputs in the Azure Machine Learning designer.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.author: lagayhar
author: lgayhardt
ms.reviewer: keli19
ms.date: 06/12/2025
ms.topic: how-to
ms.custom: UpdateFrequency5, designer

#customer intent: As a machine learning engineer, I want to use pipleline inputs so that I can dynamically set parameter values at runtime.
---

# Use pipeline inputs in the designer to build versatile pipelines

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

This article describes how to use pipeline inputs to build flexible pipelines in the Azure Machine Learning designer. Pipeline inputs enable you to dynamically set values at runtime so you can encapsulate pipeline logic and reuse assets.

Pipeline inputs are especially useful when you resubmit a pipeline job, [retrain models](how-to-retrain-designer.md), or [perform batch predictions](how-to-run-batch-predictions-designer.md).

In this article, you learn how to do the following:

> [!div class="checklist"]
> * Create pipeline inputs.
> * Delete and manage pipeline inputs.
> * Supply pipeline inputs when you trigger pipeline jobs.

## Prerequisites

* An Azure Machine Learning workspace. See [Create workspace resources](../quickstart-create-resources.md).

* A pipeline draft. 

* For a guided introduction to the designer, complete the [designer tutorial](tutorial-designer-automobile-price-train-score.md). 

> [!IMPORTANT]
> If you don't see the UI elements mentioned in this article, such as buttons in studio or designer, you might not have the right level of permissions for the workspace. Contact your Azure subscription administrator to verify that you're granted the correct level of access. For more information, see [Manage users and roles](../how-to-assign-roles.md).

## Create a pipeline parameter

There are three ways to create a pipeline input in the designer:
- Create a pipeline input in the settings panel and bind it to a component.
- Promote a component input to a pipeline input.
- Promote a dataset to a pipeline input.

> [!NOTE]
> Pipeline inputs support only basic data types, like `int`, `float`, and `string`.

### Option 1: Create a pipeline input in the settings panel

In this section, you create a pipeline input in the settings panel.

In this example, you create a pipeline input that defines how a pipeline fills in missing data with the **Clean missing data** component.

1. In your pipeline draft, select **Piepleline interface**.

1. In the **Pipeline interface** section, select the **+** button and then select an input type, for example, `Double`. 

1. Enter a name for the input and a default value. 

   For example, enter `minimum-missing-value-ratio-2` as input name and `0.1` as the default value.

   :::image type="content" source="media/how-to-use-pipeline-parameter/create-pipeline-parameter.png" alt-text="Screenshot that shows how to create a pipeline input." lightbox ="media/how-to-use-pipeline-parameter/create-pipeline-parameter.png":::

1. Select **Save**.

After you create a pipeline input, you must [attach it to the component input](#attach-a-component-parameter-to-a-pipeline-parameter) that you want to dynamically set.

### Option 2: Promote a component input

The easiest way to create a pipeline input for a component value is to promote a component input. Use the following steps to promote a component input to a pipeline input:

1. Double-click the component you want to attach a pipeline input to.
1. Select the ellipsis button (**...**) next to the input that you want to specify.
1. Select **Add to pipeline input**.

   :::image type="content" source="media/how-to-use-pipeline-parameter/promote-module-para-to-pipeline-para.png" alt-text="Screenshot that shows how to promote a component input to a pipeline input." lightbox ="media/how-to-use-pipeline-parameter/promote-module-para-to-pipeline-para.png":::

1. Enter a input name and a default value.
1. Select **Save**.

You can now specify new values for this input anytime you submit the pipeline.

### Option 3: Promote a dataset to a pipeline input

If you want to submit your pipeline with variable datasets, you need to promote your dataset to a pipeline input:

1. Select the dataset you want to turn into a pipeline input.

1. In the details pane of the dataset, select **Set as pipeline input**.

   :::image type="content" source="media/how-to-use-pipeline-parameter/set-dataset-as-pipeline-parameter.png" alt-text="Screenshot that shows how to set dataset as pipeline input." lightbox ="media/how-to-use-pipeline-parameter/set-dataset-as-pipeline-parameter.png":::

1. Select **Save**.

You can now specify a different dataset by using the pipeline input the next time you run the pipeline.

## Attach a component input to or detach a component pipeline from a pipeline input 

In this section, you learn how to attach a component input to a pipeline input and how to detach a component input from a pipeline input.

### Attach a component input to a pipeline input

You can attach the component inputs of duplicated components to the same pipeline input if you want to alter the value one time when you trigger the pipeline job.

In the following example, the **Clean Missing Data** component is duplicated. For each **Clean Missing Data** component, attach a **Minimum missing value ratio** to the pipeline input **minimum-missing-value-ratio-2**:

1. Double-click the **Clean Missing Data** component.

1. Select the ellipsis button (**...**) above the **Minimum missing value reatio** box.

1. Select the pipeline input `minimum-missing-value-ratio-2`.

   :::image type="content" source="media/how-to-use-pipeline-parameter/attach-replace-value-to-pipeline-parameter.png" alt-text="Screenshot that shows how to attach a pipeline input." lightbox ="media/how-to-use-pipeline-parameter/attach-replace-value-to-pipeline-parameter.png":::

1. Select **Save**.

You have successfully attached the **Minimum missing value ratio** field to your pipeline input. 

### Detach a component input from a pipeline input

When you detach a component input from a pipeline input, it's not actionable.

You can detach a component input from a pipeline input by selecting the ellipsis button (**...**) next to the component input and then selecting **Detach from pipeline input**.

:::image type="content" source="media/how-to-use-pipeline-parameter/non-actionable-module-parameter.png" alt-text="Screenshot that shows how to detach a component input." lightbox ="media/how-to-use-pipeline-parameter/non-actionable-module-parameter.png":::

## Update and delete pipeline inputs

In this section, you learn how to update and delete pipeline inputs.

### Update pipeline inputs

Complete the following steps to update a component pipeline input:

1. To the right of the canvas, select **Pipeline interface**.
1. You can view and update the names and default values for all of your pipeline inputs.

### Delete a dataset pipeline input

Complete the following steps to delete a dataset pipeline input:

1. Double-click the dataset component.
1. Clear the **Set as pipeline input** checkbox.
1. Select **Save**.

### Delete component pipeline inputs

Complete the following steps to delete a component pipeline input:

1. To the right of the canvas, select **Pipeline interface**.

1. Select the recycle bin icon next to the pipeline input.

    :::image type="content" source="media/how-to-use-pipeline-parameter/delete-pipeline-parameter2.png" alt-text="Screenshot that shows the current pipeline input applied to a component." lightbox ="media/how-to-use-pipeline-parameter/delete-pipeline-parameter2.png":::

1. Confirm the deletion in the resulting pop-up window.

    > [!NOTE]
    > Deleting a pipeline input causes all attached component inputs to be detached. The values of detached component inputs will keep current pipeline input values.

## Supply pipeline inputs when you trigger a pipeline job

In this section, you learn how to supply pipeline paramaters when you submit a pipeline job.

### Resubmit a pipeline job

After you submit a pipeline with pipeline inputs, you can resubmit the job with different inputs:

1. Go to pipeline detail page. In the **Pipeline run overview** pane, you can check current pipeline inputs and values.
1. Select **Resubmit**.
1. In the **Set up pipleine job** window, specify your new pipeline inputs. 

   :::image type="content" source="media/how-to-use-pipeline-parameter/resubmit-pipeline-run.png" alt-text="Screenshot that shows how to resubmit a pipeline with pipeline inputs." lightbox ="media/how-to-use-pipeline-parameter/resubmit-pipeline-run.png":::

### Use published pipelines

You can also publish a pipeline to use its pipeline inputs. A *published pipeline* is a pipeline that has been deployed to a compute resource. Client applications can invoke the pipeline via a REST endpoint.

Published endpoints are especially useful for retraining and batch prediction scenarios. For more information, see [How to retrain models in the designer](how-to-retrain-designer.md) or [Run batch predictions in the designer](how-to-run-batch-predictions-designer.md).

## Next steps

In this article, you learned how to create pipeline inputs in the designer. Next, see how you can use pipeline inputs to [retrain models](how-to-retrain-designer.md) or perform [batch predictions](how-to-run-batch-predictions-designer.md).

You can also learn how to [use pipelines programmatically with the SDK v1](how-to-deploy-pipelines.md?view=azureml-api-1&preserve-view=true).
