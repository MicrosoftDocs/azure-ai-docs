---
title: 'Tutorial: AutoML- train no-code classification models'
titleSuffix: Azure Machine Learning
description: In this tutorial, train a classification model without writing a single line of code using Azure Machine Learning Automated ML in the studio UI.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: automl
ms.topic: tutorial
author: s-polly
ms.author: scottpolly
ms.reviewer: sooryar
ms.date: 10/15/2025
ms.custom: automl, build-2023
#Customer intent: As a non-coding data scientist, I want to use automated machine learning techniques so that I can build a classification model.
---

# Tutorial: Train a classification model with no-code AutoML in the Azure Machine Learning studio

In this tutorial, you learn how to train a classification model with no-code automated machine learning (AutoML) using Azure Machine Learning in the Azure Machine Learning studio. This classification model predicts whether a client subscribes to a fixed term deposit with a financial institution.

With Automated ML, you can automate away time intensive tasks. Automated machine learning rapidly iterates over many combinations of algorithms and hyperparameters to help you find the best model based on a success metric of your choosing.

You don't write any code in this tutorial. You use the studio interface to perform training. You learn how to do the following tasks:

> [!div class="checklist"]
> - Create an Azure Machine Learning workspace
> - Run an automated machine learning experiment
> - Explore model details
> - Deploy the recommended model

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- Download the [**bank+marketing.zip**](https://archive.ics.uci.edu/static/public/222/bank+marketing.zip) data file. We will use the **bank-full.csv** file. The **y** column indicates if a customer subscribed to a fixed term deposit, which is later identified as the target column for predictions in this tutorial.

  > [!NOTE]
  > This Bank Marketing dataset is made available under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/legalcode). This dataset is   available as part the [UCI Machine Learning Database](https://archive.ics.uci.edu/ml/datasets/bank+marketing).
  >
  > Moro, S., P. Rita, and P. Cortez. 2014. Bank Marketing. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306.

## Create a workspace

An Azure Machine Learning workspace is a foundational resource in the cloud that you use to experiment, train, and deploy machine learning models. It ties your Azure subscription and resource group to an easily consumed object in the service.

Complete the following steps to create a workspace and continue the tutorial.

1. Sign in to [Azure Machine Learning studio](https://ml.azure.com).

1. Select **Create workspace**.

1. Provide the following information to configure your new workspace:

   | Field | Description |
   |:---|:--- |
   |  Workspace name | Enter a unique name that identifies your workspace. Names must be unique across the resource group. Use a name that's easy to recall and to differentiate from workspaces created by others. The workspace name is case-insensitive. |
   | Subscription | Select the Azure subscription that you want to use. |
   | Resource group | Use an existing resource group in your subscription or enter a name to create a new resource group. A resource group holds related resources for an Azure solution. You need *contributor* or *owner* role to use an existing resource group. For more information, see [Manage access to an Azure Machine Learning workspace](how-to-assign-roles.md). |
   | Region | Select the Azure region closest to your users and the data resources to create your workspace. |

1. Select **Create** to create the workspace.

For more information on Azure resources, see [Create the workspace](quickstart-create-resources.md#create-the-workspace).

For other ways to create a workspace in Azure, [Manage Azure Machine Learning workspaces in the portal or with the Python SDK (v2)](how-to-manage-workspace.md).

## Create an Automated Machine Learning job

Complete the following experiment set-up and run steps by using the Azure Machine Learning studio at https://ml.azure.com. Machine Learning Studio is a consolidated web interface that includes machine learning tools to perform data science scenarios for data science practitioners of all skill levels. The studio isn't supported on Internet Explorer browsers.

1. Select your subscription and the workspace you created.

1. In the navigation pane, select **Authoring** > **Automated ML**.

   Because this tutorial is your first automated ML experiment, you see an empty list and links to documentation.

   :::image type="content" source="./media/tutorial-first-experiment-automated-ml/get-started.png" alt-text="Screenshot shows the Automated ML page where you can create a new Automated ML job." lightbox="./media/tutorial-first-experiment-automated-ml/get-started.png":::

1. Select **New Automated ML job**.

1. In **Training method**, select **Train automatically**, then select **Start configuring job**.

1. In **Basic settings**, select **Create new**, then for **Experiment name**, enter *my-1st-automl-experiment*.

1. Select **Next** to load your dataset.

## Create and load a dataset as a data asset

Before you configure your experiment, upload the data file to your workspace in the form of an Azure Machine Learning data asset. For this tutorial, you can think of a data asset as your dataset for the Automated ML job. Doing so allows you to ensure that your data is formatted appropriately for your experiment.

1. In **Task type & data**, for **Select task type**, choose **Classification**.

1. Under **Select data**, choose **Create**.

   1. In the **Data type** form, give your data asset a name and provide an optional description.
   1. For **Type**, select **Tabular**. The automated ML interface currently only supports TabularDatasets.
   1. Select **Next**.
   1. In the **Data source** form, select **From local files**. Select **Next**.
   1. In **Destination storage type**, select the default datastore that was automatically set up during your workspace creation: **workspaceblobstore**. You upload your data file to this location to make it available to your workspace.
   1. Select **Next**.
   1. In **File or folder selection**, select **Upload files or folder** > **Upload files**.
   1. Choose the *bankmarketing_train.csv* file on your local computer. You downloaded this file as a [prerequisite](https://archive.ics.uci.edu/static/public/222/bank+marketing.zip).
   1. Select **Next**.

      When the upload finishes, the **Data preview** area is populated based on the file type.

   1. In the **Settings** form, review the values for your data. Then select **Next**.

      | Field | Description | Value for tutorial |
      |:---|:---|:---|
      | File format | Defines the layout and type of data stored in a file.| Delimited |
      | Delimiter | One or more characters for specifying the boundary between&nbsp; separate, independent regions in plain text or other data streams. | Semicolon |
      | Encoding | Identifies what bit to character schema table to use to read your dataset. | UTF-8 |
      | Column headers | Indicates how the headers of the dataset, if any, are treated. | All files have same headers |
      | Skip rows | Indicates how many, if any, rows are skipped in the dataset. | None |

   1. The **Schema** form allows for further configuration of your data for this experiment. For this example, select the toggle switch for the **day_of_week**, so as to not include it. Select **Next**.

       :::image type="content" source="./media/tutorial-first-experiment-automated-ml/configure-schema-tab.png" alt-text="Screenshot shows the Schema form where you can exlcued columns from your data.":::

   1. In the **Review** form, verify your information, and then select **Create**.

1. Select your dataset from the list.

1. Review the data by selecting the data asset and looking at the **preview** tab. Ensure that it doesn't include **day_of_week** and select **Close**.

1. Select  **Next** to proceed to task settings.

## Configure job

After you load and configure your data, you can set up your experiment. This setup includes experiment design tasks such as, selecting the size of your compute environment and specifying what column you want to predict.

1. Populate the **Task settings** form as follows:

   1. Select **y (String)** as the target column, which is what you want to predict. This column indicates whether the client subscribed to a term deposit or not.
   1. Select **View additional configuration settings** and populate the fields as follows. These settings are to better control the training job. Otherwise, defaults are applied based on experiment selection and data.

      | Additional&nbsp;configurations | Description | Value&nbsp;for&nbsp;tutorial |
      |:------|:---------|:---|
      | Primary metric| Evaluation metric used to measure the machine learning algorithm. | AUCWeighted |
      | Explain best model | Automatically shows explainability on the best model created by automated ML.| Enable |
      | Blocked models | Algorithms you want to exclude from the training job | None |

   1. Select **Save**.

1. Under **Validate and test**:

    1. For **Validation type**, select **k-fold cross-validation**.
    1. For **Number of cross validations**, select **2**.

1. Select **Next**.
1. Select **compute cluster** as your compute type.

   A compute target is a local or cloud-based resource environment used to run your training script or host your service deployment. For this experiment, you can either try a cloud-based serverless compute (preview) or create your own cloud-based compute.

   > [!NOTE]
   > To use serverless compute, [enable the preview feature](./how-to-use-serverless-compute.md#how-to-use-serverless-compute), select **Serverless**, and skip this procedure.

1. To create your own compute target, in **Select compute type**, select **Compute cluster** to configure your compute target.

1. Populate the **Virtual Machine** form to set up your compute. Select **New**.

   | Field | Description | Value for tutorial |
   |:----|:---|:---|
   | Location | Your region that you'd like to run the machine from |West US 2
   | Virtual&nbsp;machine&nbsp;tier |Select what priority your experiment should have| Dedicated
   | Virtual&nbsp;machine&nbsp;type| Select the virtual machine type for your compute.|CPU (Central Processing Unit)
   | Virtual&nbsp;machine&nbsp;size| Select the virtual machine size for your compute. A list of recommended sizes is provided based on your data and experiment type. |Standard_DS12_V2

1. Select **Next** to go to the **Advanced Settings** form.

   :::image type="content" source="./media/tutorial-first-experiment-automated-ml/compute-settings.png" alt-text="Screenshot shows the Advanced Settings page, where you enter values for your compute cluster." lightbox="./media/tutorial-first-experiment-automated-ml/compute-settings.png":::

   | Field | Description | Value for tutorial |
   |:----|:---|:---|
   | Compute name | A unique name that identifies your compute context. | automl-compute |
   | Min / Max nodes| To profile data, you must specify 1 or more nodes. | Min nodes: 1<br>Max nodes: 6 |
   | Idle seconds before scale down | Idle time before  the cluster is automatically scaled down to the minimum node count.|120 (default) |
   | Advanced settings | Settings to configure and authorize a virtual network for your experiment.| None |

1. Select **Create**.

   Creating a compute can take minutes to complete.

1. After creation, select your new compute target from the list. Select **Next**.

1. Select **Submit training job** to run the experiment. The **Overview** screen opens with the **Status** at the top as the experiment preparation begins. This status updates as the experiment progresses. Notifications also appear in the studio to inform you of the status of your experiment.

>[!IMPORTANT]
> Preparation takes **10-15 minutes** to prepare the experiment run. Once running, it takes **2-3 minutes more for each iteration**.
>
> In production, you'd likely walk away for a bit. But for this tutorial, you can start exploring the tested algorithms on the **Models** tab as they complete while the others continue to run.

## Explore models

Navigate to the **Models + child jobs** tab to see the algorithms (models) tested. By default, the job orders the models by metric score as they complete. For this tutorial, the model that scores the highest based on the chosen **AUCWeighted** metric is at the top of the list.

While you wait for all of the experiment models to finish, select the **Algorithm name** of a completed model to explore its performance details. Select the **Overview** and the **Metrics** tabs for information about the job.

The following animation views the selected model's properties, metrics, and performance charts.

:::image type="content" source="./media/tutorial-first-experiment-automated-ml/run-detail.gif" alt-text="Animation that shows different views available for a child job." lightbox="./media/tutorial-first-experiment-automated-ml/run-detail.gif":::

## View model explanations

While you wait for the models to complete, you can also take a look at model explanations and see which data features (raw or engineered) influenced a particular model's predictions.

These model explanations can be generated on demand. The model explanations dashboard that's part of the **Explanations (preview)** tab summarizes these explanations.

To generate model explanations:

1. In the navigation links at the top of the page, select the job name to go back to the **Models** screen.
1. Select the **Models + child jobs** tab.
1. For this tutorial, select the first **MaxAbsScaler, LightGBM** model.
1. Select **Explain model**. On the right, the **Explain model** pane appears.
1. Select your compute type and then select the instance or cluster: **automl-compute** that you created previously. This compute starts a child job to generate the model explanations.
1. Select **Create**. A green success message appears.

   > [!NOTE]
   > The explainability job takes about 2-5 minutes to complete.

1. Select **Explanations (preview)**. This tab populates after the explainability run completes.
1. On the left, expand the pane. Under **Features**, select the row that says **raw**.
1. Select the **Aggregate feature importance** tab. This chart shows which data features influenced the predictions of the selected model.

   :::image type="content" source="media/tutorial-first-experiment-automated-ml/model-explanation-dashboard.png" alt-text="Screenshot shows the Model explanation dashboard, displaying an aggregate feature importance chart." lightbox="media/tutorial-first-experiment-automated-ml/model-explanation-dashboard.png":::

   In this example, the *duration* appears to have the most influence on the predictions of this model.

## Deploy the best model

The automated machine learning interface allows you to deploy the best model as a web service. *Deployment* is the integration of the model so it can predict on new data and identify potential areas of opportunity. For this experiment, deployment to a web service means that the financial institution now has an iterative and scalable web solution for identifying potential fixed term deposit customers.

Check to see whether your experiment run is complete. To do so, navigate back to the parent job page by selecting the job name at the top of your screen. A **Completed** status is shown on the top left of the screen.

After the experiment run is complete, the **Details** page is populated with a **Best model summary** section. In this experiment context, **VotingEnsemble** is considered the best model, based on the **AUCWeighted** metric.

Deploy this model. Deployment takes about 20 minutes to complete. The deployment process entails several steps including registering the model, generating resources, and configuring them for the web service.

1. Select **VotingEnsemble** to open the model-specific page.

1. Select **Deploy** > **Web service**.

1. Populate the **Deploy a model** pane as follows:

   | Field | Value |
   |:----|:----|
   | Name | my-automl-deploy |
   | Description | My first automated machine learning experiment deployment |
   | Compute type | Select Azure Container Instance |
   | Enable authentication | Disable. |
   | Use custom deployment assets | Disable. Allows for the default driver file (scoring script) and environment file to be autogenerated. |

   For this example, use the defaults provided in the **Advanced** menu.

1. Select **Deploy**.

   A green success message appears at the top of the **Job** screen. In the **Model summary** pane, a status message appears under **Deploy status**. Select **Refresh** periodically to check the deployment status.

You have an operational web service to generate predictions.

Proceed to the [Related content](#related-content) to learn more about how to consume your new web service, and test your predictions using Power BI built in Azure Machine Learning support.

## Clean up resources

Deployment files are larger than data and experiment files, so they cost more to store. If you want to keep your workspace and experiment files, delete only the deployment files to minimize costs to your account. If you don't plan to use any of the files, delete the entire resource group.

### Delete the deployment instance

Delete just the deployment instance from Azure Machine Learning at https:\//ml.azure.com/.

1. Go to [Azure Machine Learning](https://ml.azure.com/). Navigate to your workspace and under the **Assets** pane, select **Endpoints**.

1. Select the deployment you want to delete and select **Delete**.

1. Select **Proceed**.

### Delete the resource group

[!INCLUDE [aml-delete-resource-group](includes/aml-delete-resource-group.md)]

## Related content

In this automated machine learning tutorial, you used Azure Machine Learning's automated ML interface to create and deploy a classification model. For more information and next steps, see these resources:

- Learn more about [automated machine learning](concept-automated-ml.md).
- Learn about classification metrics and charts: [Evaluate automated machine learning experiment results](how-to-understand-automated-ml.md) article.
- Learn more about [how to set up AutoML for NLP](how-to-auto-train-nlp-models.md).

Also try automated machine learning for these other model types:

- For a no-code example of forecasting, see [Tutorial: Forecast demand with no-code automated machine learning in the Azure Machine Learning studio](tutorial-automated-ml-forecast.md).
- For a code first example of an object detection model, see the [Tutorial: Train an object detection model with AutoML and Python](tutorial-auto-train-image-models.md).
