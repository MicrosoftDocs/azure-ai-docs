---
title: Transform Data in the Designer
titleSuffix: Azure Machine Learning
description: Learn how to import and transform data in Azure Machine Learning designer to create your own datasets.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mldata
ms.reviewer: franksolomon
ms.author: keli19
author: likebupt
ms.date: 06/11/2025
ms.topic: how-to
ms.custom: UpdateFrequency5, designer
---

# Transform data in Azure Machine Learning designer

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

In this article, you learn how to transform and save datasets in the Azure Machine Learning designer, to prepare your own data for machine learning.

You'll use the sample [Adult Census Income Binary Classification](samples-designer.md#datasets) dataset to prepare two datasets. One dataset includes adult census information from only the United States, and another dataset includes census information from non-US adults.

In this article, you learn how to:

- Transform a dataset to prepare it for training.
- Export the resulting datasets to a datastore.
- View the results.

This how-to guide is a prerequisite for the [Use pipeline inputs to retrain models](how-to-retrain-designer.md) article. In that article, you learn how to use the transformed datasets to train multiple models with pipeline inputs.

> [!IMPORTANT]
> If you don't see graphical elements mentioned in this document, such as buttons in studio or designer, you might not have the right level of permissions to the workspace. Contact your Azure subscription administrator to verify that you have been granted the correct level of access. For more information, see [Manage users and roles](../how-to-assign-roles.md).

## Transform a dataset

In this section, you learn how to import the sample dataset, and split the data into US and non-US datasets. For more information, see [Import data into Azure Machine Learning designer](how-to-designer-import-data.md).

### Import data

Use these steps to import the sample dataset:

1. Sign in to [Azure Machine Learning studio](https://ml.azure.com), and select the workspace you want to use.

1. Select **Designer** from the sidebar menu. Under **Classic prebuilt**, choose **Create a new pipeline using classic prebuilt components**.

1. To the left of the pipeline canvas, in the **Component** tab, expand the **Sample data** node.

1. Drag and drop the **Adult Census Income Binary classification** dataset onto the canvas.

1. Right-select the **Adult Census Income** dataset component, and select **Preview data**.

1. Use the data preview window to explore the dataset. Take special note of the **native-country** column values.

### Split the data

Use the [Split Data component](../algorithm-module-reference/split-data.md) to identify and split rows that contain *United-States* in the **native-country** column.

1. To the left of the canvas, in the component tab, expand the **Data Transformation** section, and find the **Split Data** component.

1. Drag the **Split Data** component onto the canvas, and drop that component below the dataset component.

1. Connect the output of the dataset component to the input of the **Split Data** component.

1. Double-click the **Split Data** component to open the **Split Data** pane.

1. Set **Splitting mode** to **Regular Expression**.

1. Enter the **Regular Expression**: `\"native-country" United-States`.

    The **Regular expression** mode tests a single column for a value. Visit the related [algorithm component reference page](../algorithm-module-reference/split-data.md) for more information on the Split Data component.

Your pipeline should resemble this screenshot:

:::image type="content" source="./media/how-to-designer-transform-data/split-data.png" alt-text="Screenshot that shows how to configure the pipeline and the Split Data component." lightbox="./media/how-to-designer-transform-data/split-data.png":::

## Save the datasets

After you set up your pipeline to split the data, you must specify where to persist the datasets. For this example, use the **Export Data** component to save your dataset to a datastore. For more information about datastores, see [Connect to Azure storage services](how-to-access-data.md).

1. To the left of the canvas in the component palette, expand the **Data Input and Output** section, and find the **Export Data** component.

1. Drag and drop two **Export Data** components below the **Split Data** component.

1. Connect each output port of the **Split Data** component to a different **Export Data** component.

    Your pipeline should resemble the following:

    :::image type="content" source="media/how-to-designer-transform-data/export-data-pipeline.png" alt-text="Screenshot showing how to connect the Export Data components." lightbox="media/how-to-designer-transform-data/export-data-pipeline.png":::

1. Double-click the **Export Data** component connected to the *left*-most port of the **Split Data** component, to open the Export Data configuration pane.

    For the **Split Data** component, the output port order is important. The first output port contains the rows where the regular expression is true. In this case, the first port contains rows for US-based income, and the second port contains rows for non-US based income.

    - Set the following options:

        **Datastore type**: Azure Blob Storage

        **Datastore**: Select an existing datastore, or select *New datastore* to create a new one

        **Output path**: `/data/us-income`

        **File format**: csv

    > [!NOTE]
    > This article assumes that you have access to a datastore registered to the current Azure Machine Learning workspace. For datastore setup instructions, see [Connect to Azure storage services](how-to-connect-data-ui.md#create-datastores).

    You can create a datastore if you don't have one. For example purposes, this article saves the datasets to the default blob storage account associated with the workspace. It saves the datasets into the `azureml` container, in a new folder named `data`.

1. Double-click the **Export Data** component connected to the *right*-most port of the **Split Data** component, to open the Export Data configuration pane.

    - Set the following options:

        **Datastore type**: Azure Blob Storage

        **Datastore**: Select the earlier datastore

        **Output path**: `/data/non-us-income`

        **File format**: csv

1. Verify that the **Export Data** component connected to the left port of the **Split Data** has the **Path** `/data/us-income`.

1. Verify that the **Export Data** component connected to the right port has the **Path** `/data/non-us-income`.

    Your pipeline and settings should look like this:

    :::image type="content" source="media/how-to-designer-transform-data/us-income-export-data.png" alt-text="Screenshot showing how to configure the Export Data components." lightbox="media/how-to-designer-transform-data/us-income-export-data.png":::

### Submit the job

After you set up your pipeline to split and export the data, submit a pipeline job.

1. Select **Configure & Submit** at the top of the canvas.

1. Select the **Create new** option in the **Basics** pane of **Set up pipeline job** to create an experiment.

    Experiments logically group related pipeline jobs together. If you run this pipeline in the future, you should use the same experiment for logging and tracking purposes.

1. Provide a descriptive experiment name--for example, *split-census-data*.

1. In the **Runtime settings** pane, select or create a compute resource.

1. Select **Review + Submit**, and then select **Submit**.

## View results

After the pipeline finishes running, you can navigate to your Azure portal blob storage to view your results. You can also view the intermediary results of the **Split Data** component to confirm that your data split correctly.

1. Select **Jobs** from the sidebar menu, then choose your job.

1. Double-click the **Split Data** component.

1. In the component details pane to the right of the canvas, select the **Outputs + logs** tab.

1. Select the **Show data outputs** dropdown.

1. Select the visualize icon next to **Results dataset1**.

    :::image type="content" source="media/how-to-designer-transform-data/show-data-outputs.png" alt-text="Screenshot that shows the Split Data results dataset on the component details pane." lightbox="media/how-to-designer-transform-data/show-data-outputs.png":::

1. Verify that the **native-country** column contains only the value *United-States*.

1. Select the visualize icon ![visualize icon](media/how-to-designer-transform-data/visualize-icon.png) next to **Results dataset2**.

1. Verify that the **native-country** column doesn't contain the value *United-States*.

## Clean up resources

If you want to continue with [part two of this how-to guide](how-to-retrain-designer.md), skip this section.

[!INCLUDE [aml-ui-cleanup](../includes/aml-ui-cleanup.md)]

## Next step

Continue to the next part of this how-to series.

> [!div class="nextstepaction"]
> [Use pipeline inputs to retrain models](how-to-retrain-designer.md)
