---
title: Build, train, and deploy a custom text classification model
titleSuffix: Foundry Tools
description: Prepare data, define a schema, label data, train, evaluate, deploy, and query a custom text classification model in Microsoft Foundry.
author: laujan
manager: mcleans
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 06/24/2026
ms.author: lajanuar
ms.custom: language-service-custom-classification
---

# Build, train, and deploy a custom text classification model

This article walks you through the complete custom text classification lifecycle in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs): prepare your data and define a schema, label your data, train and evaluate a model, deploy it, and send prediction requests. Each stage links to the relevant concepts and reference content if you want to go deeper.

For an end-to-end introduction with a sample project, see the [custom text classification quickstart](../quickstart.md). For the broader process, see the [project development lifecycle](../overview.md#project-development-lifecycle).

## Prerequisites

* **An active Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **A project created with a configured Azure blob storage account**. For more information, *see* [Create a custom text classification project](create-project.md).
* **Text data that's [uploaded](#data-preparation) to your storage account**.

## Prepare your data and define a schema

The schema defines the classes that you need your model to classify your text into at runtime. Defining the schema is the first step in the [project development lifecycle](../overview.md#project-development-lifecycle).

### Schema design

* **Review and identify**: Review documents in your dataset to be familiar with their structure and content, then identify how you want to classify your data.

    For example, if you're classifying support tickets, you might need the following classes: *Sign in issue*, *hardware issue*, *connectivity issue*, and *new equipment request*.

* **Avoid ambiguity in classes**: Ambiguity arises when the classes you specify share similar meaning to one another. The more ambiguous your schema is, the more labeled data you might need to differentiate between different classes.

    For example, if you're classifying food recipes, they might be similar to an extent. To differentiate between *dessert recipe* and *main dish recipe*, you might need to label more examples to help your model distinguish between the two classes. Avoiding ambiguity saves time and yields better results.

* **Out of scope data**: When using your model in production, consider adding an *out of scope* class to your schema if you expect documents that don't belong to any of your classes. Then add a few documents to your dataset to be labeled as *out of scope*. The model can learn to recognize irrelevant documents, and predict their labels accordingly.

### Data selection

The quality of the data you use to train your model greatly affects model performance.

* Use real-life data that reflects your domain's problem space to effectively train your model. You can use synthetic data to accelerate the initial model training process, but it likely differs from your real-life data and makes your model less effective when used.

* Balance your data distribution as much as possible without deviating far from the distribution in real life.

* Use diverse data whenever possible to avoid overfitting your model. Less diversity in training data might lead to your model learning spurious correlations that don't exist in real-life data.

* Avoid duplicate documents in your data. Duplicate data negatively affects the training process, model metrics, and model performance.

* Consider where your data comes from. If you collect data from one person, department, or part of your scenario, you're likely missing diversity that might be important for your model to learn about.

> [!NOTE]
> If your documents are in multiple languages, select the **multiple languages** option during [project creation](../quickstart.md) and set the **language** option to the language for most of your documents.

### Data preparation

As a prerequisite for creating a custom text classification project, upload your training data to a blob container in your storage account. You can create and upload training documents from Azure directly, or through using the Azure Storage Explorer tool. Using the Azure Storage Explorer tool allows you to upload more data quickly.

* [Create and upload documents from Azure](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container)
* [Create and upload documents using Azure Storage Explorer](/azure/vs-azure-tools-storage-explorer-blobs)

You can only use `.txt` documents for custom text. If your data is in another format, use the [CLUtils parse command](https://github.com/microsoft/CognitiveServicesLanguageUtilities/blob/main/CustomTextAnalytics.CLUtils/Solution/CogSLanguageUtilities.ViewLayer.CliCommands/Commands/ParseCommand/README.md) to change your file format.

### Test set

When you define the testing set, make sure to include example documents that aren't present in the training set. Defining the testing set is an important step to calculate the [model performance](#view-model-details). Also, make sure that the testing set includes documents that represent all classes used in your project.

## Label your data

Before training your model, label your documents with the classes you want to categorize them into. Data labeling is a crucial step in the development lifecycle. Use this data in the next step when training your model so that your model can learn from the labeled data. If you already labeled your data, you can directly [import](create-project.md) it into your project. Make sure your data follows the [accepted data format](../concepts/data-formats.md).

### Data labeling guidelines

After [preparing your data, designing your schema](#schema-design), and [creating your project](create-project.md), label your data. Labeling your data is important so your model knows which documents are associated with the classes you need. When you label your data or import labeled data, the labels are stored in the JSON file in your storage container that you connected to this project.

As you label your data, keep in mind:

* In general, more labeled data leads to better results, provided the data is labeled accurately.

* There's no fixed number of labels that can guarantee your model performs the best. Model performance depends on possible ambiguity in your [schema](#schema-design), and the quality of your labeled data. Nevertheless, we recommend 50 labeled documents per class.

### Label your data in Foundry

Use the following steps to label your data:

1. Go to your project page in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs).

1. From the left side menu, select **Data labeling**. You can find a list of all documents in your storage container.

    >[!TIP]
    > Use the filters in the top menu to view the unlabeled files so that you can start labeling them.
    > Use the filters to view the documents that are labeled with a specific class.

1. Change to a single file view from the left side in the top menu or select a specific file to start labeling. You can find a list of all `.txt` files available in your projects to the left. Use the **Back** and **Next** buttons from the bottom of the page to navigate through your documents.

    > [!NOTE]
    > If you enabled multiple languages for your project, you see a **Language** dropdown in the top menu, which you use to select the language of each document.

1. In the right side pane, **Add class** to your project so you can start labeling your data with them.

1. Start labeling your files based on your project type:

    * **Multilabel classification**: your file can be labeled with multiple classes. Select all applicable check boxes next to the classes you want to label this document with.

        :::image type="content" source="../media/multiple.png" alt-text="A screenshot showing the multiple label classification tag page." lightbox="../media/multiple.png":::

    * **Single label classification**: your file can only be labeled with one class. Select one of the buttons next to the class you want to label the document with.

        :::image type="content" source="../media/single.png" alt-text="A screenshot showing the single label classification tag page" lightbox="../media/single.png":::

    To ensure complete labeling, use the [auto labeling feature](use-autolabeling.md).

1. In the right side pane under the **Labels** pivot you can find all the classes in your project and the count of labeled instances per each.

1. In the bottom section of the right side pane you can add the current file you're viewing to the training set or the testing set. By default all the documents are added to your training set. Learn more about [training and testing sets](#data-splitting) and how they're used for model training and evaluation.

    > [!TIP]
    > If you're planning on using **Automatic** data splitting, use the default option of assigning all the documents into your training set.

1. Under the **Distribution** pivot you can view the distribution across training and testing sets. You have two options for viewing:
   * *Total instances* where you can view count of all labeled instances of a specific class.
   * *documents with at least one label* where each document is counted if it contains at least one labeled instance of this class.

1. While you're labeling, your changes sync periodically. If they aren't saved yet, you see a warning at the top of your page. If you want to save manually, select **Save labels** button at the bottom of the page.

To remove a label, uncheck the button next to the class.

To delete a class, select the icon next to the class you want to remove. Deleting a class removes all its labeled instances from your dataset.

## Train your model

Training is the process where the model learns from your labeled data. After training is completed, you can [view the model's performance](#view-model-details) to determine if you need to improve your model.

To train a model, start a training job. Only successfully completed jobs create a usable model. Training jobs expire after seven days. After this period, you can't retrieve the job details. If your training job completed successfully and a model was created, the job expiration isn't affected. You can only have one training job running at a time, and you can't start other jobs in the same project.

Depending on the dataset size and the complexity of your schema, training times can vary from a few minutes up to several hours.

### Data splitting

Before you start the training process, labeled documents in your project are divided into a training set and a testing set. Each one of them serves a different function. The **training set** is used in training the model and where the model learns the class/classes assigned to each document. The **testing set** is a blind set that isn't introduced to the model during training but only during evaluation. After the model is trained successfully, it can make predictions from the documents in the testing set. Based on these predictions, the model's [evaluation metrics](../concepts/evaluation-metrics.md) are calculated. Make sure that all your classes are adequately represented in both the training and testing set.

Custom text classification supports two methods for data splitting:

* **Automatically splitting the testing set from training data**: The system splits your labeled data between the training and testing sets, according to the percentages you choose. The system attempts to have a representation of all classes in your training set. The recommended percentage split is 80% for training and 20% for testing.

 > [!NOTE]
 > If you choose the **Automatically splitting the testing set from training data** option, only the data assigned to training set is split according to the percentages provided.

* **Use a manual split of training and testing data**: This method enables you to define which labeled documents should belong to which set. This step is only enabled if you added documents to your testing set during [data labeling](#label-your-data).

### Train your model

# [Foundry](#tab/ai-foundry)

To start training your model from within the [Foundry](https://ai.azure.com/?cid=learnDocs):

1. Select **Training jobs** from the left navigation menu.
1. Select **Start a training job** from the top menu.
1. To train a new model, select **Train a new model** and enter a new model name. Otherwise, to replace an existing model with a model trained on the new data, select **Overwrite an existing model** and then select an existing model.
1. Select the data splitting method: either **Automatically splitting the testing set from training data** or **Use a manual split of training and testing data**.
1. Select the **Train** button.
1. Choose the training job ID from the list. A panel appears that details the training progress, job status, and other details for this job.

> [!NOTE]
>
> * Only successfully completed training jobs generate models.
> * Training can take from a few minutes to a few hours based on the size of your training data.
> * You can only have one training job running at a time. You can't start other training jobs within the same project until the running job is completed.

# [REST APIs](#tab/rest-api)

### Start training job

[!INCLUDE [train model](../includes/rest-api/train-model.md)]

### Get training job status

Training could take some time depending on the size of your training data and complexity of your schema. You can use the following request to keep polling the status of the training job until it successfully completes.

[!INCLUDE [get training model status](../includes/rest-api/get-training-status.md)]

### Cancel training job

[!INCLUDE [Cancel training](../includes/rest-api/cancel-training.md)]

---

## View model details

After your model finishes training, you can view the model performance and see the predicted classes for the documents in the test set.

> [!NOTE]
> If you use the **Automatically split the testing set from training data** option, you might get different model evaluation results each time you train a new model. This difference happens because the test set is randomly selected from the data. To ensure the evaluation uses the same test set every time you train a model, use the **Use a manual split of training and testing data** option when starting a training job. Also, define your **Test** documents when [labeling data](#label-your-data).

### Single label classification

[!INCLUDE [Model evaluation](../includes/rest-api/model-evaluation-single-label.md)]

### Multi label classification

[!INCLUDE [Model evaluation](../includes/rest-api/model-evaluation-multi-label.md)]

### Load or export model data

[!INCLUDE [Load export model](../includes/rest-api/load-export-model.md)]

### Delete model

[!INCLUDE [Delete model](../includes/rest-api/delete-model.md)]

As you review how your model performs, learn about the [evaluation metrics](../concepts/evaluation-metrics.md) that are used.

## Deploy your model

When you're satisfied with how your model performs, it's ready to deploy. You can use it to classify text. Deploying a model makes it available for use through the [prediction API](https://aka.ms/ct-runtime-swagger).

After you review your model's performance and decide it can be used in your environment, assign it to a deployment so you can query it. Create a deployment named `production` to which you assign the best model you built so far and use it in your system. You can create another deployment called `staging` to which you can assign the model you're currently working on to test it. You can have a maximum of 10 deployments in your project.

### Submit deployment job

[!INCLUDE [deploy model](../includes/rest-api/deploy-model.md)]

### Get deployment job status

[!INCLUDE [get deployment status](../includes/rest-api/get-deployment-status.md)]

### Swap deployments

You can swap deployments after testing a model assigned to one deployment, and want to assign it to another. Swapping deployments involves taking the model assigned to the first deployment, and assigning it to the second deployment. Then taking the model assigned to second deployment and assign it to the first deployment. This step could be used to swap your `production` and `staging` deployments when you want to take the model assigned to `staging` and assign it to `production`.

[!INCLUDE [Swap deployments](../includes/rest-api/swap-deployment.md)]

### Delete deployment

[!INCLUDE [Delete deployment](../includes/rest-api/delete-deployment.md)]

### Assign deployment resources

You can [deploy your project to multiple regions](../../concepts/custom-features/multi-region-deployment.md) by assigning different language resources that exist in different regions.

[!INCLUDE [Assign resource](../includes/rest-api/assign-resources.md)]

### Unassign deployment resources

When you unassign or remove a deployment resource from a project, you also delete all the deployments previously deployed to that resource region.

[!INCLUDE [Unassign resource](../includes/rest-api/unassign-resources.md)]

## Send prediction requests

After you successfully deploy a model, you can query the deployment to classify text based on the model you assigned to the deployment. You can query the deployment programmatically through the [prediction API](/rest/api/language/analyze-text/analyze-text/analyze-text?view=rest-language-analyze-text-2025-11-01&tabs=HTTP&preserve-view=true) or through the client libraries (Azure SDK).

First, you need to get your resource key and endpoint:

1. Go to your resource overview page in the [Azure portal](https://portal.azure.com/#home).

1. From the menu on the left side, select **Keys and Endpoint**. Use the endpoint and key for the API requests.

    :::image type="content" source="../media/key-endpoint-page.png" alt-text="A screenshot showing the key and endpoint page in the Azure portal." lightbox="../media/key-endpoint-page.png":::

### Submit a custom text classification task

[!INCLUDE [submit a text classification task using the REST API](../includes/rest-api/submit-task.md)]

### Get task results

[!INCLUDE [get custom NER task results](../includes/rest-api/get-results.md)]

### Use the client libraries (Azure SDK)

To use the client libraries provided by the Azure SDK to send requests to your model, first get your resource key and endpoint:

[!INCLUDE [Get keys and endpoint Azure portal](../includes/get-keys-endpoint-azure.md)]

1. Download and install the client library package for your language of choice:

    |Language  |Package version  |
    |---------|---------|
    |.NET     | [5.2.0-beta.3](https://www.nuget.org/packages/Azure.AI.TextAnalytics/5.2.0-beta.3)        |
    |Java     | [5.2.0-beta.3](https://mvnrepository.com/artifact/com.azure/azure-ai-textanalytics/5.2.0-beta.3)        |
    |JavaScript     |  [6.0.0-beta.1](https://www.npmjs.com/package/@azure/ai-text-analytics/v/6.0.0-beta.1)       |
    |Python     | [5.2.0b4](https://pypi.org/project/azure-ai-textanalytics/5.2.0b4/)         |

1. After you install the client library, use the following samples on GitHub to start calling the API.

    Single label classification:
    * [C#](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/textanalytics/Azure.AI.TextAnalytics/samples/Sample9_SingleLabelClassify.md)
    * [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/textanalytics/azure-ai-textanalytics/src/samples/java/com/azure/ai/textanalytics/lro/SingleLabelClassifyDocument.java)
    * [JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/%40azure/ai-text-analytics_6.0.0-beta.1/sdk/textanalytics/ai-text-analytics/samples/v5/javascript/customText.js)
    * [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/textanalytics/azure-ai-textanalytics/samples/sample_single_label_classify.py)

    Multi label classification:
    * [C#](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/textanalytics/Azure.AI.TextAnalytics/samples/Sample10_MultiLabelClassify.md)
    * [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/textanalytics/azure-ai-textanalytics/src/samples/java/com/azure/ai/textanalytics/lro/MultiLabelClassifyDocument.java)
    * [JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/%40azure/ai-text-analytics_6.0.0-beta.1/sdk/textanalytics/ai-text-analytics/samples/v5/javascript/customText.js)
    * [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/textanalytics/azure-ai-textanalytics/samples/sample_multi_label_classify.py)

1. See the following reference documentation on the client, and return object:

    * [C#](/dotnet/api/azure.ai.textanalytics?view=azure-dotnet-preview&preserve-view=true)
    * [Java](/java/api/overview/azure/ai-textanalytics-readme?view=azure-java-preview&preserve-view=true)
    * [JavaScript](/javascript/api/overview/azure/ai-text-analytics-readme?view=azure-node-preview&preserve-view=true)
    * [Python](/python/api/azure-ai-textanalytics/azure.ai.textanalytics?view=azure-python-preview&preserve-view=true)

## Related content

* [Custom text classification overview](../overview.md)
* [Custom text classification quickstart](../quickstart.md)
* [Evaluation metrics](../concepts/evaluation-metrics.md)
</content>
