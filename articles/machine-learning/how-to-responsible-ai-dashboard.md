---
title: Use the Responsible AI dashboard in Azure Machine Learning studio
titleSuffix: Azure Machine Learning
description: Learn how to use the various tools and visualization charts in the Responsible AI dashboard in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: responsible-ai
ms.topic:  how-to
ms.reviewer: None
ms.author: lagayhar
author: lgayhardt
ms.date: 01/09/2026
ms.custom: responsible-ml
ai-usage: ai-assisted
#customer intent: As a data scientist, I need to understand the Responsible AI dashboard to use responsible AI practices in Azure Machine Learning.
---

# Use the Responsible AI dashboard in Azure Machine Learning studio

Link Responsible AI dashboards to your registered models. To view your Responsible AI dashboard, go to your model registry and select the registered model you generated a Responsible AI dashboard for. Then, select the **Responsible AI** tab to view a list of generated dashboards.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/view-responsible-ai-model-page.png" alt-text="Screenshot of the model details pane in Azure Machine Learning studio, with the 'Responsible AI' tab highlighted." lightbox="./media/how-to-responsible-ai-dashboard/view-responsible-ai-model-page.png":::

You can configure multiple dashboards and attach them to your registered model. Attach various combinations of components, such as interpretability, error analysis, and causal analysis, to each Responsible AI dashboard.

The following image shows a dashboard's customization and the components that were generated in it. In each dashboard, you can view or hide various components in the dashboard UI itself.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/view-responsible-ai-dashboard.png" alt-text="Screenshot of Responsible AI tab with a dashboard name highlighted." lightbox="./media/how-to-responsible-ai-dashboard/view-responsible-ai-dashboard.png":::

Select the name of the dashboard to open it into a full view in your browser. To return to your list of dashboards, select **Back to models details**.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/dashboard-full-view.png" alt-text="Screenshot of a Responsible AI dashboard with the 'Back to model details' button highlighted." lightbox="./media/how-to-responsible-ai-dashboard/dashboard-full-view.png":::

## Prerequisites

Before you open the Responsible AI dashboard, make sure you have:

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.
- [!INCLUDE [workspace and compute instance](includes/prerequisite-workspace-compute-instance.md)]
- A registered model with a generated Responsible AI dashboard. To create or update one, see [Generate Responsible AI insights in the studio UI](how-to-responsible-ai-insights-ui.md) or [Generate Responsible AI insights with the SDK or CLI](how-to-responsible-ai-insights-sdk-cli.md).
- Permissions in the workspace to view models and start compute instances. For example, **Contributor** or **Owner** at the workspace scope can start compute instances. For least-privilege access, combine **Reader** (to view assets) with **AzureML Compute Operator** (to manage compute). For more information, see [Manage access to Azure Machine Learning workspaces](/azure/machine-learning/how-to-assign-roles?view=azureml-api-2&preserve-view=true).
- Network access required by your organization to reach Azure Machine Learning studio and connect to a compute instance. If your workspace uses network isolation, for example, managed virtual network or virtual networks with private endpoints, make sure you allow required inbound and outbound traffic. For more information, see [Plan for network isolation in Azure Machine Learning](/azure/machine-learning/how-to-network-isolation-planning?view=azureml-api-2&preserve-view=true) and [Secure an Azure Machine Learning workspace with virtual networks](/azure/machine-learning/how-to-secure-workspace-vnet?view=azureml-api-2&preserve-view=true).

## Full functionality with an integrated compute resource

Some features of the Responsible AI dashboard require dynamic, on-the-fly, and real-time computation, such as what-if analysis. If you don't connect a compute resource to the dashboard, you might find some functionality missing. When you connect to a compute resource, you enable full functionality of your Responsible AI dashboard for the following components:

- **Error analysis**
    - Setting your global data cohort to any cohort of interest updates the error tree instead of disabling it.
    - Selecting other error or performance metrics is supported.
    - Selecting any subset of features for training the error tree map is supported.
    - Changing the minimum number of samples required per leaf node and error tree depth is supported.
    - Dynamically updating the heat map for up to two features is supported.
- **Feature importance**
    - An individual conditional expectation (ICE) plot in the individual feature importance tab is supported.
- **Counterfactual what-if**
    - Generating a new what-if counterfactual data point to understand the minimum change required for a desired outcome is supported.
- **Causal analysis**
    - Selecting any individual data point, perturbing its treatment features, and seeing the expected causal outcome of causal what-if is supported. This analysis is only for regression machine learning scenarios.

You can also find this information on the Responsible AI dashboard page by selecting the **Information** icon, as shown in the following image:

:::image type="content" source="./media/how-to-responsible-ai-dashboard/compute-view-full-functionality.png" alt-text="Screenshot of the 'Information' icon on the Responsible AI dashboard.":::

### Enable full functionality of the Responsible AI dashboard

To connect a compute instance and unlock real-time capabilities in the dashboard, complete the following steps:

1. Select a running compute instance in the **Compute** list at the top of the dashboard. If you don't have a running compute, create a new compute instance by selecting the plus sign (**+**) next to the dropdown list. Or you can select **Start compute** to start a stopped compute instance. Creating or starting a compute instance might take a few minutes.

   :::image type="content" source="./media/how-to-responsible-ai-dashboard/select-compute.png" alt-text="Screenshot of the 'Compute' dropdown list for selecting a running compute instance." lightbox="./media/how-to-responsible-ai-dashboard/select-compute.png":::
    
1. When a compute is in a *Running* state, your Responsible AI dashboard starts to connect to the compute instance. To achieve this connection, the dashboard creates a terminal process on the selected compute instance and starts a Responsible AI endpoint on the terminal. Select **View terminal outputs** to view the current terminal process.

   :::image type="content" source="./media/how-to-responsible-ai-dashboard/compute-connect-terminal.png" alt-text="Screenshot showing that the responsible AI dashboard is connecting to a compute resource." lightbox="./media/how-to-responsible-ai-dashboard/compute-connect-terminal.png":::

1. When your Responsible AI dashboard connects to the compute instance, you see a green message bar. The dashboard is now fully functional.

   :::image type="content" source="./media/how-to-responsible-ai-dashboard/compute-terminal-connected.png" alt-text="Screenshot showing that the dashboard is connected to the compute instance." lightbox="./media/how-to-responsible-ai-dashboard/compute-terminal-connected.png":::

1. If the process to connect the compute instance takes too long or the dashboard displays a red error message bar, it means there are problems with starting your Responsible AI endpoint. Select **View terminal outputs** and scroll down to the bottom to view the error message.

    :::image type="content" source="./media/how-to-responsible-ai-dashboard/compute-terminal-error.png" alt-text="Screenshot of an error connecting to a compute." lightbox="./media/how-to-responsible-ai-dashboard/compute-terminal-error.png":::

1. If you're having difficulty figuring out how to resolve the *failed to connect to compute instance* issue, select the **Smile** icon at the upper right. Submit feedback to us about any error or issue you encounter. You can include a screenshot and your email address in the feedback form.

## UI overview of the Responsible AI dashboard

The Responsible AI dashboard provides a rich set of visualizations and features to help you analyze your machine learning model and make data-driven business decisions. It includes:

- [Global controls](#global-controls)
- [Error analysis](#error-analysis)
- [Model overview and fairness metrics](#model-overview-and-fairness-metrics)
- [Data analysis](#data-analysis)
- [Feature importance (model explanations)](#feature-importances-model-explanations)
- [Counterfactual what-if](#counterfactual-what-if)
- [Causal analysis](#causal-analysis)

### Global controls

At the top of the dashboard, you can create *cohorts*, which are subgroups of data points that share specified characteristics. Use cohorts to focus your analysis of each component. The dashboard always shows the name of the cohort currently applied to the dashboard at the upper left. The default view in your dashboard is your whole dataset, titled **All data (default)**.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/view-dashboard-global-controls.png" alt-text="Screenshot of a responsible AI dashboard showing all data." lightbox = "./media/how-to-responsible-ai-dashboard/view-dashboard-global-controls.png":::

1. **Cohort settings**: View and modify the details of each cohort.
1. **Dashboard configuration**: View and modify the layout of the overall dashboard.
1. **Switch cohort**: Select a different cohort and view its statistics in a pop-up window.
1. **New cohort**: Create and add a new cohort to your dashboard.

To open a pane with a list of your cohorts, select **Cohort settings**. In this area, you can create, edit, duplicate, or delete cohorts.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/view-dashboard-cohort-settings.png" alt-text="Screenshot showing the cohort settings on the dashboard." lightbox ="./media/how-to-responsible-ai-dashboard/view-dashboard-cohort-settings.png":::

To open a new pane with options to filter the following values, select **New cohort** at the top of the dashboard or in the **Cohort settings**.

1. **Index**: Filter by the position of the data point in the full dataset.
1. **Dataset**: Filter by the value of a particular feature in the dataset.
1. **Predicted Y**: Filter by the prediction made by the model.
1. **True Y**: Filter by the actual value of the target feature.
1. **Error (regression)**: Filter by error (or **Classification Outcome (classification)**: Filter by type and accuracy of classification).
1. **Categorical Values**: Filter by a list of values that should be included.
1. **Numerical Values**: Filter by a Boolean operation over the values. For example, select data points where age < 64.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/view-dashboard-cohort-panel.png" alt-text="Screenshot of making multiple new cohorts." lightbox="./media/how-to-responsible-ai-dashboard/view-dashboard-cohort-panel.png":::

You can name your new dataset cohort, select **Add filter** to add each filter you want to use, and then do either of the following steps:

- Select **Save** to save the new cohort to your cohort list.
- Select **Save and switch** to save and switch the global cohort of the dashboard to the newly created cohort.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/view-dashboard-new-cohort.png" alt-text="Screenshot of making a new cohort in the dashboard." lightbox="./media/how-to-responsible-ai-dashboard/view-dashboard-new-cohort.png":::

To see a list of the components you configured on your dashboard, select **Dashboard configuration**. You can hide components on your dashboard by selecting the **Trash** icon, as shown in the following image:

:::image type="content" source="./media/how-to-responsible-ai-dashboard/dashboard-configuration.png" alt-text="Screenshot showing the dashboard configuration." lightbox="./media/how-to-responsible-ai-dashboard/dashboard-configuration.png":::

You can add components back to your dashboard by using the blue circular plus sign (**+**) icon in the divider between each component, as shown in the following image:

:::image type="content" source="./media/how-to-responsible-ai-dashboard/dashboard-add-component.png" alt-text="Screenshot of adding a component to the dashboard." lightbox="./media/how-to-responsible-ai-dashboard/dashboard-add-component.png":::

### Error analysis

The next sections describe how to interpret and use error tree maps and heat maps.

#### Error tree map

The first tab of the error analysis component is a tree map. It shows how model failure is distributed across various cohorts with a tree visualization. Select any node to see the prediction path on your features where an error was found.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/error-analysis-tree-map-selected.png" alt-text="Screenshot of the dashboard showing an error analysis on the tree map pane." lightbox="./media/how-to-responsible-ai-dashboard/error-analysis-tree-map-selected.png":::

1. **Heat map view**: Switches to heat map visualization of error distribution.
1. **Feature list**: Modify the features used in the heat map.
1. **Error coverage**: Shows the percentage of all error in the dataset concentrated in the selected node.
1. **Error (regression) or Error rate (classification)**: Shows the error or percentage of failures of all the data points in the selected node.
1. **Node**: Represents a cohort of the dataset, potentially with filters applied, and the number of errors out of the total number of data points in the cohort.
1. **Fill line**: Visualizes the distribution of data points into child cohorts based on filters, with the number of data points represented through line thickness.
1. **Selection information**: Contains information about the selected node.
1. **Save as a new cohort**: Creates a new cohort with the specified filters.
1. **Instances in the base cohort**: Shows the total number of points in the entire dataset and the number of correctly and incorrectly predicted points.
1. **Instances in the selected cohort**: Shows the total number of points in the selected node and the number of correctly and incorrectly predicted points.
1. **Prediction path (filters)**: Lists the filters placed over the full dataset to create this smaller cohort.

Select **Feature list** to open **Feature List**. You can retrain the error tree on specific features.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/error-analysis-feature-selection.png" alt-text="Screenshot of the dashboard side pane, which lists selectable features of an error analysis tree map." lightbox="./media/how-to-responsible-ai-dashboard/error-analysis-feature-selection.png":::

- **Search features**: Find specific features in the dataset.
- **Features**: Lists the name of the feature in the dataset.
- **Importances**: A guideline for how related the feature might be to the error. Calculated by using mutual information score between the feature and the error on the labels. Use this score to help you decide which features to choose in the error analysis.
- **Check mark**: Add or remove the feature from the tree map.
- **Maximum depth**: The maximum depth of the surrogate tree trained on errors.
- **Number of leaves**: The number of leaves of the surrogate tree trained on errors.
- **Minimum number of samples in one leaf**: The minimum amount of data required to create one leaf.

#### Error heat map

Select the **Heat map** tab to switch to a different view of the error in the dataset. You can select one or many heat map cells and create new cohorts. You can choose up to two features to create a heat map.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/error-analysis-heat-map.png" alt-text="Screenshot of the dashboard, showing an error analysis heat map and list of features to compare." lightbox="./media/how-to-responsible-ai-dashboard/error-analysis-heat-map.png":::

1. **Cells**: Shows the number of cells selected.
1. **Error coverage**: Shows the percentage of all errors concentrated in the selected cells.
1. **Error rate**: Shows the percentage of failures of all data points in the selected cells.
1. **Axis features**: Selects the intersection of features to display in the heat map.
1. **Cells**: Represents a cohort of the dataset, with filters applied, and the percentage of errors out of the total number of data points in the cohort. A blue outline indicates selected cells, and the darkness of red represents the concentration of failures.
1. **Prediction path (filters)**: Lists the filters placed over the full dataset for each selected cohort.

### Model overview and fairness metrics

The model overview component provides a comprehensive set of performance and fairness metrics for evaluating your model. It also provides key performance disparity metrics along specified features and dataset cohorts.  

#### Dataset cohorts

On the **Dataset cohorts** page, you can investigate your model by comparing the model performance of various user-specified dataset cohorts. You can access these cohorts through the **Cohort settings** icon at the top right of the dashboard.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/model-overview-dataset-cohorts.png" alt-text="Screenshot of the 'Model overview' pane, showing the 'Dataset cohorts' tab." lightbox="./media/how-to-responsible-ai-dashboard/model-overview-dataset-cohorts.png":::

1. **Help me choose metrics**: Select this icon for more information about what model performance metrics are available to be shown in the table. Adjust which metrics to view by using the multiselect list to select and deselect performance metrics. 
1. **Show heat map**: Toggle on and off to show or hide the heat map visualization in the table. The gradient of the heat map corresponds to the range normalized between the lowest value and the highest value in each column.  
1. **Table of metrics for each dataset cohort**: View columns of dataset cohorts, the sample size of each cohort, and the selected model performance metrics for each cohort.
1. **Bar chart visualizing individual metric**: View mean absolute error across the cohorts for easy comparison. 
1. **Choose metric (x-axis)**: Choose which metrics to view in the bar chart. 
1. **Choose cohorts (y-axis)**: Choose which cohorts to view in the bar chart. **Feature cohort** selection might be disabled unless you first specify the features you want on the **Feature cohort** tab of the component. 

Select **Help me choose metrics** to see model performance metrics and their definitions. This list can help you select the right metrics to view.

| Machine learning scenario | Metrics |
| --- | --- |
| Regression | Mean absolute error, Mean squared error, R-squared, Mean prediction. |
| Classification | Accuracy, Precision, Recall, F1 score, False positive rate, False negative rate, Selection rate. |

#### Feature cohorts

On the **Feature cohorts** page, you can investigate your model by comparing model performance across user-specified sensitive and nonsensitive features. For example, you can compare performance across various gender, race, and income level cohorts.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/model-overview-feature-cohorts.png" alt-text="Screenshot of the dashboard 'Model overview' page, showing the 'Feature cohorts' tab." lightbox="./media/how-to-responsible-ai-dashboard/model-overview-feature-cohorts.png":::

1. **Help me choose metrics**: Select this icon to see more information about what metrics are available to be shown in the table. Adjust which metrics to view by using the multiselect list to select and deselect performance metrics.
1. **Help me choose features**: Select this icon to see more information about what features are available to be shown in the table. The pane includes descriptors of each feature and their binning capability. Adjust which features to view by using the multiselect list to select and deselect them.

   :::image type="content" source="./media/how-to-responsible-ai-dashboard/model-overview-choose-features.png" alt-text="Screenshot of the dashboard 'Model overview' pane, showing how to choose features." lightbox="./media/how-to-responsible-ai-dashboard/model-overview-choose-features.png":::

1. **Show heat map**: Toggle on and off to see a heat map visualization. The gradient of the heat map corresponds to the range that's normalized between the lowest value and the highest value in each column.
1. **Table of metrics for each feature cohort**: A table with columns for feature cohorts (subcohort of your selected feature), sample size of each cohort, and the selected model performance metrics for each feature cohort.
1. **Fairness metrics/disparity metrics**: A table that corresponds to the metrics table and shows the maximum difference or maximum ratio in performance scores between any two feature cohorts.
1. **Bar chart visualizing individual metric**: View mean absolute error across the cohorts for easy comparison.
1. **Choose cohorts (y-axis)**: Choose which cohorts to view in the bar chart.

   Selecting **Choose cohorts** opens a pane with an option to either show a comparison of selected dataset cohorts or feature cohorts. The choice depends on what you select in the multiselect dropdown list. Select **Confirm** to save the changes to the bar chart view.  

   :::image type="content" source="./media/how-to-responsible-ai-dashboard/model-overview-choose-cohorts.png" alt-text="Screenshot of the dashboard 'Model overview' pane, showing how to choose cohorts." lightbox="./media/how-to-responsible-ai-dashboard/model-overview-choose-cohorts.png":::

1. **Choose metric (x-axis)**: Choose which metric to view in the bar chart.

### Data analysis

In the data analysis component, **Table view** shows a table view of your dataset for all features and rows.  

The **Chart view** shows aggregate and individual plots of data points. You can analyze data statistics along the x-axis and y-axis by using filters such as predicted outcome, dataset features, and error groups. This view helps you understand overrepresentation and underrepresentation in your dataset.  

:::image type="content" source="./media/how-to-responsible-ai-dashboard/data-analysis-table-view.png" alt-text="Screenshot of the dashboard, showing the data analysis." lightbox="./media/how-to-responsible-ai-dashboard/data-analysis-table-view.png":::

- **Select a dataset cohort to explore**: Specify which dataset cohort from your list of cohorts you want to view data statistics for.
- **X-axis**: Displays the type of value being plotted horizontally. Modify the values by selecting the button to open a side pane.
- **Y-axis**: Displays the type of value being plotted vertically. Modify the values by selecting the button to open a side pane.
- **Chart type**: Specifies the chart type. Choose between aggregate plots (bar charts) or individual data points (scatter plot).

   By selecting the **Individual data points** option under **Chart type**, you can shift to a disaggregated view of the data with the availability of a color axis.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/data-analysis-individual-datapoints.png" alt-text="Screenshot of the dashboard, showing the data analysis with the 'Individual data points' option selected." lightbox="./media/how-to-responsible-ai-dashboard/data-analysis-individual-datapoints.png":::

### Feature importances (model explanations)

By using the model explanation component, you can see which features were most important in your model's predictions. You can view what features affected your model's prediction overall on the **Aggregate feature importance** pane or view feature importances for individual data points on the **Individual feature importance** pane.

#### Aggregate feature importances (global explanations)

:::image type="content" source="./media/how-to-responsible-ai-dashboard/aggregate-feature-importance.png" alt-text="Screenshot of the dashboard, showing aggregate feature importances on the 'Feature importances' pane." lightbox="./media/how-to-responsible-ai-dashboard/aggregate-feature-importance.png":::

1. **Top k features**: Lists the most important global features for a prediction and you can change it by using a slider bar.
1. **Aggregate feature importance**: Visualizes the weight of each feature in influencing model decisions across all predictions.
1. **Sort by**: Select which cohort's importances to sort the aggregate feature importance graph by.
1. **Chart type**: Select between a bar plot view of average importances for each feature and a box plot of importances for all data.

   When you select one of the features in the bar plot, the dependence plot is populated, as shown in the following image. The dependence plot shows the relationship of the values of a feature to its corresponding feature importance values, which affect the model prediction.  

   :::image type="content" source="./media/how-to-responsible-ai-dashboard/aggregate-feature-importance-2.png" alt-text="Screenshot of the dashboard, showing a populated dependence plot on the 'Aggregate feature importances' pane." lightbox="./media/how-to-responsible-ai-dashboard/aggregate-feature-importance-2.png":::

1. **Feature importance of [feature] (regression) or Feature importance of [feature] on [predicted class] (classification)**: Plots the importance of a particular feature across the predictions. For regression scenarios, the importance values are in terms of the output, so positive feature importance means it contributed positively toward the output. The opposite applies to negative feature importance. For classification scenarios, positive feature importances mean that feature value is contributing toward the predicted class denoted in the y-axis title. Negative feature importance means it's contributing against the predicted class.
1. **View dependence plot for**: Selects the feature whose importances you want to plot.
1. **Select a dataset cohort**: Selects the cohort whose importances you want to plot.

#### Individual feature importances (local explanations)

The following image illustrates how features influence the predictions that are made on specific data points. You can choose up to five data points to compare feature importances for.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/individual-feature-importance.png" alt-text="Screenshot of the dashboard, showing the 'Individual feature importances' pane." lightbox="./media/how-to-responsible-ai-dashboard/individual-feature-importance.png":::

**Point selection table**: View your data points and select up to five points to display in the feature importance plot or the ICE plot.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/individual-feature-importance-bar-plot.png" alt-text="Screenshot of the dashboard, showing a bar plot on the 'Individual feature importances' pane." lightbox="./media/how-to-responsible-ai-dashboard/individual-feature-importance-bar-plot.png":::

**Feature importance plot**: A bar plot of the importance of each feature for the model's prediction on the selected data points.

1. **Top k features**: Specify the number of features to show importances for by using a slider.
1. **Sort by**: Select the point from the checked points whose feature importances are displayed in descending order on the feature importance plot.
1. **View absolute values**: Toggle on to sort the bar plot by the absolute values. This setting allows you to see the most impactful features regardless of their positive or negative direction.
1. **Bar plot**: Displays the importance of each feature in the dataset for the model prediction of the selected data points.

**Individual conditional expectation (ICE) plot**: Switches to the ICE plot, which shows model predictions across a range of values of a particular feature.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/individual-feature-importance-ice-plot.png" alt-text="Screenshot of the dashboard, showing an ICE plot on the 'Individual feature importances' pane." lightbox="./media/how-to-responsible-ai-dashboard/individual-feature-importance-ice-plot.png":::

- **Min (numerical features)**: Specifies the lower bound of the range of predictions in the ICE plot.
- **Max (numerical features)**: Specifies the upper bound of the range of predictions in the ICE plot.
- **Steps (numerical features)**: Specifies the number of points to show predictions for within the interval.
- **Feature values (categorical features)**: Specifies which categorical feature values to show predictions for.
- **Feature**: Specifies the feature to make predictions for.

### Counterfactual what-if

Counterfactual analysis provides a diverse set of *what-if* examples generated by changing the values of features minimally to produce the desired prediction class (classification) or range (regression).

:::image type="content" source="./media/how-to-responsible-ai-dashboard/counterfactuals.png" alt-text="Screenshot of the dashboard, showing counterfactuals." lightbox="./media/how-to-responsible-ai-dashboard/counterfactuals.png":::

1. **Point selection**: Selects the point to create a counterfactual for and display in the top-ranking features plot.

   :::image type="content" source="./media/how-to-responsible-ai-dashboard/counterfactuals-top-ranked-features.png" alt-text="Screenshot of the dashboard, showing a top ranked features plot." lightbox="./media/how-to-responsible-ai-dashboard/counterfactuals-top-ranked-features.png":::

   **Top ranked features plot**: Displays, in descending order of average frequency, the features to perturb to create a diverse set of counterfactuals of the desired class. Because there's a lack of accuracy with a lesser number of counterfactuals, you must generate at least 10 diverse counterfactuals per data point to enable this chart.

1. **Selected data point**: Performs the same action as the point selection in the table, except in a dropdown menu.
1. **Desired class for counterfactual(s)**: Specifies the class or range to generate counterfactuals for.
1. **Create what-if counterfactual**: Opens a pane for counterfactual what-if data point creation.

   Select the **Create what-if counterfactual** button to open a full window page.

   :::image type="content" source="./media/how-to-responsible-ai-dashboard/counterfactuals-examples.png" alt-text="Screenshot of the dashboard, showing what-if counterfactuals." lightbox="./media/how-to-responsible-ai-dashboard/counterfactuals-examples.png":::

1. **Search features**: Finds features to observe and change values.
1. **Sort counterfactual by ranked features**: Sorts counterfactual examples in order of perturbation effect. See also **Top ranked features plot**, discussed earlier.
1. **Counterfactual examples**: Lists feature values of example counterfactuals with the desired class or range. The first row is the original reference data point. Select **Set value** to set all the values of your own counterfactual data point in the bottom row with the values of the pregenerated counterfactual example.  
1. **Predicted value or class**: Lists the model prediction of a counterfactual's class given those changed features.
1. **Create your own counterfactual**: Allows you to perturb your own features to modify the counterfactual. Features that you change from the original feature value are denoted by the title being bolded, for example, **Employer** and **Programming language**. Select **See prediction delta** to view the difference in the new prediction value from the original data point.
1. **What-if counterfactual name**: Allows you to name the counterfactual uniquely.
1. **Save as new data point**: Saves the counterfactual you create.

### Causal analysis

The next sections describe how to read the causal analysis for your dataset on select user-specified treatments.

#### Aggregate causal effects

Select the **Aggregate causal effects** tab of the causal analysis component to display the average causal effects for predefined treatment features. These features are the ones that you want to treat to optimize your outcome.

> [!NOTE]
> The causal analysis component doesn't support global cohort functionality.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/aggregate-causal-effects.png" alt-text="Screenshot of the dashboard, showing causal analysis on the 'Aggregate causal effects' pane." lightbox="./media/how-to-responsible-ai-dashboard/aggregate-causal-effects.png":::

1. **Direct aggregate causal effect table**: Displays the causal effect of each feature aggregated on the entire dataset and associated confidence statistics.

   - **Continuous treatments**: On average in this sample, increasing this feature by one unit causes the probability of class to increase by X units, where X is the causal effect.
   - **Binary treatments**: On average in this sample, turning on this feature causes the probability of class to increase by X units, where X is the causal effect.

1. **Direct aggregate causal effect whisker plot**: Visualizes the causal effects and confidence intervals of the points in the table.

#### Individual causal effects and causal what-if

For a granular view of causal effects on an individual data point, switch to the **Individual causal what-if** tab.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/individual-causal-what-if.png" alt-text="Screenshot of the dashboard showing causal analysis on the individual causal what-if tab." lightbox="./media/how-to-responsible-ai-dashboard/individual-causal-what-if.png":::

1. **X-axis**: Selects the feature to plot on the x-axis.
1. **Y-axis**: Selects the feature to plot on the y-axis.
1. **Individual causal scatter plot**: Visualizes points in the table as a scatter plot to select data points for analyzing causal what-if and viewing the individual causal effects.
1. **Set new treatment value**:

   - **(numerical)**: Shows a slider to change the value of the numerical feature as a real-world intervention.
   - **(categorical)**: Shows a list to select the value of the categorical feature.

#### Treatment policy

Select the **Treatment policy** tab to switch to a view that helps determine real-world interventions and shows treatments to apply to achieve a particular outcome.

:::image type="content" source="./media/how-to-responsible-ai-dashboard/causal-treatment-policy.png" alt-text="Screenshot of the dashboard, showing causal analysis on the 'Treatment policy' pane." lightbox="./media/how-to-responsible-ai-dashboard/causal-treatment-policy.png":::

1. **Set treatment feature**: Selects a feature to change as a real-world intervention.

1. **Recommended global treatment policy**: Displays recommended interventions for data cohorts to improve the target feature value. Read the table from left to right, where the segmentation of the dataset is first in rows and then in columns. For example, for 658 individuals whose employer isn't Snapchat and whose programming language isn't JavaScript, the recommended treatment policy is to increase the number of GitHub repositories contributed to.

   **Average gains of alternative policies over always applying treatment**: Plots the target feature value in a bar chart of the average gain in your outcome for the recommended treatment policy versus always applying treatment.

   :::image type="content" source="./media/how-to-responsible-ai-dashboard/causal-treatment-policy-2.png" alt-text="Screenshot of the dashboard showing a bar chart of the average gains of alternative policies over always applying treatment on the treatment policy tab." lightbox="./media/how-to-responsible-ai-dashboard/causal-treatment-policy-2.png":::

   **Recommended individual treatment policy**:

   :::image type="content" source="./media/how-to-responsible-ai-dashboard/causal-treatment-policy-3.png" alt-text="Screenshot of the dashboard showing a recommended individual treatment policy table on the treatment policy tab." lightbox="./media/how-to-responsible-ai-dashboard/causal-treatment-policy-3.png":::

1. **Show top k data point samples ordered by causal effects for recommended treatment feature**: Selects the number of data points to show in the table.

1. **Recommended individual treatment policy table**: Lists, in descending order of causal effect, the data points whose target features would be most improved by an intervention.

## Related content

- Summarize and share your Responsible AI insights with the [Responsible AI scorecard as a PDF export](concept-responsible-ai-scorecard.md).
- Learn more about the [concepts and techniques behind the Responsible AI dashboard](concept-responsible-ai-dashboard.md).
- View [sample YAML and Python notebooks](https://aka.ms/RAIsamples) to generate a Responsible AI dashboard with YAML or Python.
- Explore the features of the Responsible AI dashboard through this [interactive AI lab web demo](https://www.microsoft.com/ai/ai-lab-responsible-ai-dashboard).
- Learn more about how you can use the Responsible AI dashboard and scorecard to debug data and models and inform better decision-making in this [tech community blog post](https://www.microsoft.com/ai/ai-lab-responsible-ai-dashboard).
- Learn about how the Responsible AI dashboard and scorecard were used by the UK National Health Service (NHS) in a [real-life customer story](https://aka.ms/NHSCustomerStory).
