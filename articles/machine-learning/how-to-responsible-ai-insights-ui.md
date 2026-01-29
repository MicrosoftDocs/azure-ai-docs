---
title: Generate Responsible AI insights in the studio UI
titleSuffix: Azure Machine Learning
description: Learn how to generate Responsible AI insights with no-code experience in the Azure Machine Learning studio UI.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: responsible-ai
ms.topic:  how-to
ms.reviewer: None
ms.author: lagayhar
author: lgayhardt
ms.date: 01/13/2026
ms.custom: responsible-ml
#customer intent: As a data scientist, I need to know how to create a Responsible AI dashboard using the Azure Machine Learning studio so that I can implement responsible AI principles.
---

# Generate Responsible AI insights in the studio UI

In this article, you create a Responsible AI dashboard and scorecard (preview) with a no-code experience in the [Azure Machine Learning studio UI](https://ml.azure.com/).

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

To access the dashboard generation page and generate a Responsible AI dashboard, do the following steps:

1. [Register your model](how-to-manage-models.md) in Azure Machine Learning so that you can access the no-code experience.
1. On the left pane of Azure Machine Learning studio, select the **Models** tab.
1. Select the registered model that you want to create Responsible AI insights for, and then select the **Details** tab.
1. Select **Create Responsible AI dashboard (preview)**.

    :::image type="content" source="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard.png" alt-text="Screenshot of the page details pane with 'Create Responsible AI dashboard (preview)' tab highlighted." lightbox="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard.png":::

To learn more supported model types and limitations in the Responsible AI dashboard, see [supported scenarios and limitations](concept-responsible-ai-dashboard.md#supported-scenarios-and-limitations).

The dashboard generation page provides an interface for entering all the necessary parameters to create your Responsible AI dashboard without having to touch code. The experience takes place entirely in the Azure Machine Learning studio UI. The studio presents a guided flow and instructional text to help contextualize the variety of choices about which Responsible AI components you'd like to populate your dashboard with.

The generation process is divided into six sections:

1. Training datasets
1. Test dataset
1. Modeling task
1. Dashboard components
1. Component parameters
1. Experiment configuration

## Select your datasets

In the first two sections, you select the train and test datasets that you used when you trained your model to generate model-debugging insights. For components like causal analysis, which doesn't require a model, you use the train dataset to train the causal model to generate the causal insights.

> [!NOTE]
> Only tabular dataset formats in ML Table are supported.

1. **Select a dataset for training**: In the list of registered datasets in the Azure Machine Learning workspace, select the dataset you want to use to generate Responsible AI insights for components, such as model explanations and error analysis.  

   :::image type="content" source="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-train-dataset.png" alt-text="Screenshot of the train dataset tab." lightbox="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-train-dataset.png":::

1. **Select a dataset for testing**: In the list of registered datasets, select the dataset you want to use to populate your Responsible AI dashboard visualizations.

   :::image type="content" source="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-test-dataset.png" alt-text="Screenshot of the test dataset tab." lightbox="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-test-dataset.png":::

1. If the train or test dataset you want to use isn't listed, select **Create** to upload it.

## Select your modeling task

After you pick your datasets, select your modeling task type, as shown in the following image:

:::image type="content" source="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-modeling-task.png" alt-text="Screenshot of the modeling task tab." lightbox="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-modeling-task.png":::

## Select your dashboard components

The Responsible AI dashboard offers two profiles for recommended sets of tools that you can generate:

- **Model debugging**: Understand and debug erroneous data cohorts in your machine learning model by using error analysis, counterfactual what-if examples, and model explainability.
- **Real-life interventions**: Understand and debug erroneous data cohorts in your machine learning model by using causal analysis.

  > [!NOTE]
  > Multi-class classification doesn't support the real-life interventions analysis profile.

:::image type="content" source="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-dashboard-components.png" alt-text="Screenshot of the dashboard components tab, showing the 'Model debugging' and 'Real-life interventions' profiles." lightbox="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-dashboard-components.png":::

1. Select the profile you want to use.
1. Select **Next**.

## Configure parameters for dashboard components

After you select a profile, the **Component parameters for model debugging** configuration pane for the corresponding components appears.

:::image type="content" source="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-component-parameter-debugging.png" alt-text="Screenshot of the component parameter tab, showing the 'Component parameters for model debugging' configuration pane." lightbox="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-component-parameter-debugging.png":::

Component parameters for model debugging:

1. **Target feature (required)**: Specify the feature that your model was trained to predict.
1. **Categorical features**: Indicate which features are categorical to properly render them as categorical values in the dashboard UI. This field is preloaded for you based on your dataset metadata.
1. **Generate error tree and heat map**: Toggle on and off to generate an error analysis component for your Responsible AI dashboard.
1. **Features for error heat map**: Select up to two features that you want to pregenerate an error heatmap for. 
1. **Advanced configuration**: Specify other parameters, such as **Maximum depth of error tree**, **Number of leaves in error tree**, and **Minimum number of samples in each leaf node**.
1. **Generate counterfactual what-if examples**: Toggle on and off to generate a counterfactual what-if component for your Responsible AI dashboard.
1. **Number of counterfactuals (required)**: Specify the number of counterfactual examples that you want to generate per data point. A minimum of 10 should be generated to enable a bar chart view of the features that were most perturbed, on average, to achieve the desired prediction.
1. **Range of value predictions (required)**: Specify for regression scenarios the range that you want counterfactual examples to have prediction values in. For binary classification scenarios, the range is set to generate counterfactuals for the opposite class of each data point. For multi-classification scenarios, use the dropdown list to specify which class you want each data point to be predicted as.
1. **Specify which features to perturb**: By default, all features are perturbed. However, if you want only specific features to be perturbed, select **Specify which features to perturb for generating counterfactual explanations** to display a pane with features to select.

    When you select **Specify which features to perturb**, you can specify the range you want to allow perturbations in. For example, for the feature YOE (Years of experience), specify that counterfactuals should have feature values ranging from only 10 to 21 instead of the default values of 5 to 21.

    :::image type="content" source="./media/how-to-responsible-ai-insights-ui/model-debug-counterfactuals.png" alt-text="Screenshot of the page, showing a pane of features you can specify to perturb." lightbox="./media/how-to-responsible-ai-insights-ui/model-debug-counterfactuals.png":::

1. **Generate explanations**: Toggle on and off to generate a model explanation component for your Responsible AI dashboard. No configuration is necessary, because a default opaque box mimic explainer generates feature importances.

Alternatively, if you select the **Real-life interventions** profile, you see the following screen generate a causal analysis. This approach helps you understand the causal effects of features you want to "treat" on a certain outcome you want to optimize.

:::image type="content" source="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-component-parameter-real-life-intervention.png" alt-text="Screenshot of the page, showing the 'Component parameters for real-life interventions' pane." lightbox="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-component-parameter-real-life-intervention.png":::

Component parameters for real-life interventions use causal analysis. Do the following steps:

1. **Target feature (required)**: Choose the outcome you want the causal effects to be calculated for.
1. **Treatment features (required)**: Choose one or more features that you're interested in changing ("treating") to optimize the target outcome.
1. **Categorical features**: Indicate which features are categorical to properly render them as categorical values in the dashboard UI. This field is preloaded for you based on your dataset metadata.
1. **Advanced settings**: Specify other parameters for your causal analysis, such as heterogeneous features and which causal model you want to be used. *Heterogeneous features* are features used to understand causal segmentation in your analysis, in addition to your treatment features.

## Configure your experiment

Finally, configure your experiment to kick off a job to generate your Responsible AI dashboard.

:::image type="content" source="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-experiment-config.png" alt-text="Screenshot of the Experiment configuration tab, showing the 'Training job or experiment configuration' pane." lightbox="./media/how-to-responsible-ai-insights-ui/create-responsible-ai-dashboard-ui-experiment-config.png":::

On the **Training job** or **Experiment configuration** pane, do the following steps:

1. **Name**: Give your dashboard a unique name so that you can differentiate it when you're viewing the list of dashboards for a given model.
1. **Experiment name**: Select an existing experiment to run the job in, or create a new experiment.
1. **Existing experiment**: Select an existing experiment.
1. **Select compute type**: Specify which compute type you want to use to run your job.
1. **Select compute**: Select the compute you want to use. If there are no existing compute resources, select the plus sign (**+**), create a new compute resource, and then refresh the list.
1. **Description**: Add a longer description of your Responsible AI dashboard.
1. **Tags**: Add any tags to this Responsible AI dashboard.

After you finish configuring your experiment, select **Create** to start generating your Responsible AI dashboard. The job page redirects you to the experiment page to track the progress of your job with a link to the resulting Responsible AI dashboard.

To learn how to view and use your Responsible AI dashboard see, [Use the Responsible AI dashboard in Azure Machine Learning studio](how-to-responsible-ai-dashboard.md).

## How to generate Responsible AI scorecard (preview)

After you create a dashboard, you can use a no-code UI in Azure Machine Learning studio to customize and generate a Responsible AI scorecard. This approach enables you to share key insights for responsible deployment of your model, such as fairness and feature importance, with nontechnical and technical stakeholders. Similar to creating a dashboard, you can use the following steps to access the scorecard generation page:

- Navigate to the **Models** tab from the left pane in Azure Machine Learning studio.
- Select the registered model you'd like to create a scorecard for and select the **Responsible AI** tab.
- From the top panel, select **Create Responsible AI insights (preview)** and then **Generate new PDF scorecard**.

The dashboard generation page allows you to customize your PDF scorecard without having to touch code. The experience takes place entirely in the Azure Machine Learning studio, which helps contextualize the variety of choices of UI. This approach uses a guided flow and instructional text to help you choose the components you'd like to populate your scorecard with. The page is divided into seven steps, with an eighth step (fairness assessment) that appear only for models with categorical features:

1. PDF scorecard summary
2. Model performance
3. Tool selection
4. Data analysis (previously called data explorer)
5. Causal analysis
6. Interpretability
7. Experiment configuration
8. Fairness assessment (only if categorical features exist)

### Configuring your scorecard

1. Enter a descriptive title for your scorecard. You can also enter an optional description about the model's functionality, data it was trained and evaluated on, architecture type, and more.

   :::image type="content" source="./media/how-to-responsible-ai-insights-ui/scorecard-summary.png" alt-text="Screenshot of the dashboard generation page on scorecard summary configuration." lightbox="./media/how-to-responsible-ai-insights-ui/scorecard-summary.png":::

1. *The Model performance* section allows you to incorporate into your scorecard industry-standard model evaluation metrics, while enabling you to set desired target values for your selected metrics. Select your desired performance metrics (up to three) and target values using the dropdown lists.

   :::image type="content" source="./media/how-to-responsible-ai-insights-ui/scorecard-performance.png" alt-text="Screenshot of the dashboard generation page on scorecard model performance configuration." lightbox="./media/how-to-responsible-ai-insights-ui/scorecard-performance.png":::

1. *The Tool selection* step allows you to choose which subsequent components you would like to include in your scorecard. Select **Include in scorecard** to include all components, or select each component individually. To learn more about components, select the information icon ("i" in a circle) next to a component.

   :::image type="content" source="./media/how-to-responsible-ai-insights-ui/scorecard-selection.png" alt-text="Screenshot of the dashboard generation page on scorecard tool selection configuration." lightbox="./media/how-to-responsible-ai-insights-ui/scorecard-selection.png":::

1. *The Data analysis* section (previously called data explorer) enables cohort analysis. Here, you can identify issues of over- and under-representation explore how data is clustered in the dataset, and how model predictions affect specific data cohorts. Select features in the dropdown list as features of interest to identify your model performance on their underlying cohorts.

   :::image type="content" source="./media/how-to-responsible-ai-insights-ui/scorecard-explorer.png" alt-text="Screenshot of the dashboard generation page on scorecard data analysis configuration." lightbox="./media/how-to-responsible-ai-insights-ui/scorecard-explorer.png":::

1. *The Fairness assessment* section can help with assessing which groups of people predictions of a machine learning model might negatively affect. There are two fields in this section.

   - **Sensitive features**: identify your sensitive attributes of choice (for example, age, gender) by prioritizing up to 20 subgroups you would like to explore and compare.

   - **Fairness metric**: select a fairness metric that's appropriate for your setting, for example, difference in accuracy or error rate ratio. Identify your desired target values on your selected fairness metrics. Your selected fairness metric paired with your selection of difference or ratio by using the toggle, capture the difference or ratio between the extreme values across the subgroups. (max - min or max/min).

   :::image type="content" source="./media/how-to-responsible-ai-insights-ui/scorecard-fairness.png" alt-text="Screenshot of the dashboard generation page on scorecard fairness assessment configuration." lightbox="./media/how-to-responsible-ai-insights-ui/scorecard-fairness.png":::

   > [!NOTE]
   > The Fairness assessment is currently only available for categorical sensitive attributes such as gender.

1. *The Causal analysis* section answers real-world "what if" questions about how changes of treatments would affect a real-world outcome. If the causal component is activated in the Responsible AI dashboard for which you're generating a scorecard, no more configuration is needed.

   :::image type="content" source="./media/how-to-responsible-ai-insights-ui/scorecard-causal.png" alt-text="Screenshot of the dashboard generation page on scorecard causal analysis configuration." lightbox="./media/how-to-responsible-ai-insights-ui/scorecard-causal.png":::

1. *The Interpretability* section generates human-understandable descriptions for predictions made by of your machine learning model. Using model explanations, you can understand the reasoning behind decisions made by your model. Select a number (K) to see the top K important features impacting your overall model predictions. The default value for K is 10.

   :::image type="content" source="./media/how-to-responsible-ai-insights-ui/scorecard-interpretability.png" alt-text="Screenshot of the dashboard generation page on scorecard feature importance configuration." lightbox="./media/how-to-responsible-ai-insights-ui/scorecard-interpretability.png":::

1. Configure your experiment to kick off a job to generate your scorecard. These configurations are the same as the ones for your Responsible AI dashboard.

   :::image type="content" source="./media/how-to-responsible-ai-insights-ui/scorecard-experiment.png" alt-text="Screenshot of the dashboard generation page on scorecard experiment configuration." lightbox="./media/how-to-responsible-ai-insights-ui/scorecard-experiment.png":::

1. Finally, review your configurations and select **Create** to start your job!

   :::image type="content" source="./media/how-to-responsible-ai-insights-ui/scorecard-review.png" alt-text="Screenshot of the dashboard generation page on scorecard configuration review." lightbox="./media/how-to-responsible-ai-insights-ui/scorecard-review.png":::

   After you start the job, it redirects you to the experiment page to track the progress of the job. To learn how to view and use your Responsible AI scorecard, see [Use Responsible AI scorecard (preview)](how-to-responsible-ai-scorecard.md).

## Related content

- After you generate your Responsible AI dashboard, [view how to access and use it in Azure Machine Learning studio](how-to-responsible-ai-dashboard.md).
- Learn more about the  [concepts and techniques behind the Responsible AI dashboard](concept-responsible-ai-dashboard.md).
- Learn more about how to [collect data responsibly](concept-sourcing-human-data.md).
- Learn more about how to use the Responsible AI dashboard and scorecard to debug data and models and inform better decision-making in this [tech community blog post](https://www.microsoft.com/ai/ai-lab-responsible-ai-dashboard).
- Learn about how the Responsible AI dashboard and scorecard were used by the UK National Health Service (NHS) in a [real life customer story](https://aka.ms/NHSCustomerStory).
