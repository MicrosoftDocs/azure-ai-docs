---
title: Organize & track training jobs (preview)
titleSuffix: Azure Machine Learning 
description: Learn how to organize and track your machine learning experiment jobs with the Azure Machine Learning studio. 
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.custom: build-2023, dev-focus
ms.author: scottpolly
author: s-polly
ms.reviewer: jturuk
ms.date: 03/30/2026
ms.topic: how-to
ai-usage: ai-assisted
---

# Organize and track training jobs (preview)

Use the jobs list view in [Azure Machine Learning studio](https://ml.azure.com) to organize and track your jobs. When you select a job, you can view and analyze its details, such as metrics, parameters, logs, and outputs. This way, you can keep track of your ML job history and ensure a transparent and reproducible ML development process.

This article shows how to complete the following tasks:

* Edit job display name.
* Select and pin columns.
* Sort jobs.
* Filter jobs.
* Perform batch actions on jobs.
* Tag jobs.

> [!TIP]
> * The Azure Machine Learning CLI v1 reached end of support on September 30, 2025, and SDK v1 is deprecated (end of support June 30, 2026). For v1 information, see [How to track, monitor, and analyze jobs (v1)](./v1/how-to-track-monitor-analyze-runs.md). To migrate, see [Upgrade to v2](how-to-migrate-from-v1.md).
> * For information on monitoring training jobs from the CLI or SDK v2, see [Track experiments with MLflow and CLI v2](how-to-use-mlflow-cli-runs.md).
> * For information on monitoring the Azure Machine Learning service and associated Azure services, see [How to monitor Azure Machine Learning](monitor-azure-machine-learning.md).
> * If you're looking for information on monitoring models deployed to online endpoints, see [Monitor online endpoints](how-to-monitor-online-endpoints.md).

> [!IMPORTANT]
> Items marked (preview) in this article are currently in public preview.
> The preview version is provided without a service level agreement, and it's not recommended for production workloads. Certain features might not be supported or might have constrained capabilities.
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## Prerequisites

You need the following items:

* [!INCLUDE [prereq-workspace](includes/prereq-workspace.md)]

* Run one or more jobs in your workspace to have results available in the dashboard. If you don't have any jobs yet, complete [Tutorial: Train a model in Azure Machine Learning](tutorial-train-model.md).

* Enable this preview feature through the preview panel.

    :::image type="content" source="media/how-to-visualize-jobs/enable-preview.png" alt-text="Screenshot shows enabling the preview feature.":::

## View jobs list

* Select **Jobs** in the left side navigation panel.
* Select either **All experiments** to view all the jobs in an experiment or select **All jobs** to view all the jobs submitted in the workspace.
* Select **List view** at the top to switch into **List view**.

## Job display name

The job display name is an optional and customizable name that you provide for your job. You can edit this name directly in your jobs list view by selecting the pencil icon when you move your mouse over a job name.

Customizing the name helps you organize and label your training jobs.

## Select and pin columns

Add, remove, reorder, and pin columns to customize your jobs list.  Select **Columns** to open the column options pane.

In column options, select columns to add or remove from the table. Drag columns to reorder how they appear in the table. Pin any column to the left of the table, so you can view your important column information, such as display name and metric value, while scrolling horizontally.  

## Sort jobs

Sort your jobs list by your metric values (such as accuracy, loss, or F1 score) to identify the best performing job that meets your criteria.

To sort by multiple columns, hold the Shift key and select the column headers you want to sort. Multiple sorts help you rank your training results according to your criteria. 
 
At any point, manage your sorting preferences for your table in column options under **Columns** to add or remove columns and change sorting order. 

## Filter jobs

Filter your jobs list by selecting **Filters**. You can use quick filters for **Status** and **Created by**, or add custom filters to any column, including metrics.

Select **Add filter** to search or select a column of your preference.

Upon choosing your column, select what type of filter you want and the value. Apply changes and see the jobs list page update accordingly.

You can remove the filter you applied from the job list if you no longer want it.  To edit your filters, simply navigate back to **Filters** to do so.  

## Perform actions on multiple jobs

Select multiple jobs in your jobs list and perform an action, such as cancel or delete, on them together.  

## Tag jobs

Tag your experiments with custom labels that help you group and filter them later. To add tags to multiple jobs, select the jobs and then select the **Add tags** button at the top of the table.

## Custom view

To view your jobs in the studio:

1. Go to the **Jobs** tab.

1. Select **All experiments** to view all the jobs in an experiment, or select **All jobs** to view all the jobs submitted in the workspace.

    In the **All jobs** page, filter the jobs list by tags, experiments, compute target, and more to better organize and scope your work.  

1. Customize the page by selecting jobs to compare, adding charts, or applying filters. Save these changes as a **Custom View** so you can easily return to your work. Users with workspace permissions can edit or view the custom view. To enhance collaboration, select **Share view** to share the custom view with team members.

## Next steps

* To learn how to visualize and analyze your experimentation results, see [visualize training results](how-to-visualize-jobs.md).
* To learn how to log metrics for your experiments, see [Log metrics during training jobs](how-to-log-view-metrics.md).
* To learn how to monitor resources and logs from Azure Machine Learning, see [Monitoring Azure Machine Learning](monitor-azure-machine-learning.md).
