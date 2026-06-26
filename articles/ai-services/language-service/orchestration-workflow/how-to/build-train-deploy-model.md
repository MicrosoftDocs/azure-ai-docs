---
title: Build, train, and deploy an orchestration workflow model
titleSuffix: Foundry Tools
description: Build a schema, label utterances, train, evaluate, deploy, and query an orchestration workflow model in Microsoft Foundry.
author: laujan
manager: mcleans
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 06/24/2026
ms.author: lajanuar
ms.custom: language-service-orchestration
---

<!-- markdownlint-disable MD025 -->

# Build, train, and deploy an orchestration workflow model

This article walks you through the complete orchestration workflow lifecycle in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs): build your schema, label your utterances, train and evaluate a model, deploy it, and send prediction requests. Each stage links to the relevant concepts and reference content if you want to go deeper.

For the broader process, see the [project development lifecycle](../overview.md#project-development-lifecycle).

## Prerequisites

* An [orchestration workflow project](create-project.md) created with a configured Azure blob storage account.

## Build your schema

In orchestration workflow projects, the *schema* is the combination of intents within your project. Schema design is a crucial part of your project's success. When creating a schema, think about which intents to include in your project, and which connected service or model each intent routes to (a [conversational language understanding](../../conversational-language-understanding/overview.md) project, a [custom question answering](../../question-answering/overview.md) knowledge base, or a LUIS application).

### Guidelines and recommendations

Consider the following guidelines when building your schema:

* Build orchestration projects when you need to combine several language capabilities or connected services behind a single deployment.

* Orchestrate between projects that handle different domains. For example, an app that routes to a *Human resources* conversational language understanding project, an *IT support* knowledge base, and a LUIS application for *expense reports*.

* If you have an overlap of similar intents across domains, separate them into different connected domains so the orchestration model can route accurately.

* Add general intents, such as *Greeting*, *Confirm*, and *Reject*, to the orchestration project itself when they aren't specific to any connected domain.

* You can orchestrate to a Custom question answering knowledge base to answer general or frequently asked questions.

* When you find a misclassified utterance, add similar utterances to the correct intent to improve routing.

* Add test data that represents real user input to validate routing decisions.

## Label your utterances

After you build your schema, add training and testing utterances to your project in Microsoft Foundry. The utterances should be similar to what your users use when interacting with the project. When you add an utterance, you assign which intent it belongs to.

Adding utterances is a crucial step in the project development lifecycle; this data is used in the next step when training your model so the model can learn from the added data. If you already have utterances, you can directly [import them into your project](create-project.md#import-an-orchestration-workflow-project-rest-api), but you need to make sure that your data follows the [accepted data format](../concepts/data-formats.md). Labeled data informs the model how to interpret text and is used for training and evaluation.

### How to add utterances

Use the following steps to add utterances in Foundry:

1. Open your orchestration workflow project in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs).

1. From the left navigation menu, select **Manage Data** and then **Add utterances**.

1. Use the **Training set** and **Testing set** views to manage your data. For more information about [training and testing sets](#data-splitting) and how they're used for model training and evaluation, see the linked article.

1. From the **Select intent** dropdown menu, select one of the intents. Type your utterance, and then press `Enter` to add it. You can also upload utterances directly by selecting **Upload utterance file** from the top menu. Make sure the utterances follow the [accepted format](../concepts/data-formats.md#utterance-format).

   > [!Note]
   > If you plan to use **Automatically split the testing set from training data**, add all your utterances to the training set.
   > You can add training utterances to **nonconnected** intents only.

   :::image type="content" source="../media/tag-utterances.png" alt-text="A screenshot of the page for tagging utterances in Microsoft Foundry." lightbox="../media/tag-utterances.png":::

1. Under **Distribution**, view the distribution across training and testing sets. You can also view utterances per intent:

   * Utterances per nonconnected intent
   * Utterances per connected intent

## Train your model

Training is the process where the model learns from your labeled utterances. After training completes, you can [view model performance](#view-model-details).

To train a model, start a training job. Only successfully completed jobs create a model. Training jobs expire after seven days. After this time, you can't retrieve the job details. If your training job completes successfully and creates a model, the model isn't affected if the job expires. You can only have one training job running at a time, and you can't start other jobs in the same project.

Training times can range from a few seconds when dealing with simple projects, up to a couple of hours when you reach the [maximum limit](../service-limits.md) of utterances.

Model evaluation is triggered automatically after training completes successfully. The evaluation process starts by using the trained model to run predictions on the utterances in the testing set. It compares the predicted results with the provided labels, which establishes a baseline of truth. The results are returned so you can review the [model's performance](#view-model-details).

### Data splitting

Before you start the training process, the system divides labeled utterances in your project into a training set and a testing set. Each set serves a different function. The **training set** is used to train the model. The model learns the labeled utterances from this set. The **testing set** is a blind set that the model doesn't see during training but only during evaluation.

After the model trains successfully, you can use the model to make predictions from the utterances in the testing set. These predictions are used to calculate [evaluation metrics](../concepts/evaluation-metrics.md).

Ensure that all your intents are adequately represented in both the training and testing set.

The orchestration workflow supports two methods for data splitting:

* **Automatically splitting the testing set from training data**: The system splits your tagged data between the training and testing sets, according to the percentages you choose. The recommended percentage split is 80% for training and 20% for testing.

 > [!NOTE]
 > If you choose the **Automatically splitting the testing set from training data** option, only the data assigned to training set is split according to the percentages provided.

* **Use a manual split of training and testing data**: This method enables you to define which utterances belong to which set. This step is only enabled if you add utterances to your testing set during [labeling](#label-your-utterances).

> [!NOTE]
> You can only add utterances in the training dataset for non-connected intents.

### Train the model

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
> * Training can take from a few seconds to a couple of hours based on the size of your training data.
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

After your model finishes training, you can review the model's performance to determine whether to improve it before deploying.

> [!NOTE]
> Using the **Automatically split the testing set from training data** option may result in different model evaluation result every time you train a new model, as the test set is selected randomly from the utterances. To make sure that the evaluation is calculated on the same test set every time you train a model, make sure to use the **Use a manual split of training and testing data** option when starting a training job and define your **Testing set** utterances when [labeling](#label-your-utterances).

### Model details

[!INCLUDE [Model evaluation](../includes/rest-api/model-evaluation.md)]

### Load or export model data

[!INCLUDE [Load export model](../../conversational-language-understanding/includes/rest-api/load-export-model.md)]

### Delete model

[!INCLUDE [Delete model](../includes/rest-api/delete-model.md)]

As you review how your model performs, learn about the [evaluation metrics](../concepts/evaluation-metrics.md) that are used.

## Deploy your model

Once you're satisfied with how your model performs, it's ready to be deployed and used to predict intents. Deploying a model makes it available for use through the [prediction API](https://aka.ms/ct-runtime-swagger).

### Submit deployment job

[!INCLUDE [deploy model](../includes/rest-api/deploy-model.md)]

### Get deployment job status

[!INCLUDE [get deployment status](../includes/rest-api/get-deployment-status.md)]

### Swap deployments

You can swap deployments after testing a model assigned to one deployment, and want to assign it to another. Swapping deployments involves taking the model assigned to the first deployment, and assigning it to the second deployment. Then taking the model assigned to second deployment, and assigning it to the first deployment.

[!INCLUDE [Swap deployments](../includes/rest-api/swap-deployment.md)]

### Delete deployment

[!INCLUDE [Delete deployment](../includes/rest-api/delete-deployment.md)]

### Assign deployment resources

You can [deploy your project to multiple regions](../../concepts/custom-features/multi-region-deployment.md) by assigning different Language resources that exist in different regions.

[!INCLUDE [Assign resource](../../conversational-language-understanding/includes/rest-api/assign-resources.md)]

### Unassign deployment resources

When you unassign or remove a deployment resource from a project, you also delete all the deployments previously deployed to that resource region.

[!INCLUDE [Unassign resource](../../conversational-language-understanding/includes/rest-api/unassign-resources.md)]

## Send prediction requests

After the deployment is added successfully, you can query the deployment for intent and entities predictions from your utterance based on the model you assigned to the deployment. You can query the deployment programmatically through the [prediction API](https://aka.ms/ct-runtime-swagger) or through the client libraries (Azure SDK).

### Test deployed model

First you need to get your resource key and endpoint:

[!INCLUDE [Get keys and endpoint Azure portal](../includes/get-keys-endpoint-azure.md)]

### Query your model

[!INCLUDE [Query model](../includes/rest-api/query-model.md)]

### Use the client libraries (Azure SDK)

You can also use the client libraries provided by the Azure SDK to send requests to your model.

> [!NOTE]
> The client library for conversational language understanding is only available for .NET and Python.

1. Go to your resource overview page in the [Azure portal](https://portal.azure.com/#home)

1. From the menu on the left side, select **Keys and Endpoint**. Use endpoint for the API requests and you need the key for `Ocp-Apim-Subscription-Key` header.

    :::image type="content" source="../../custom-text-classification/media/get-endpoint-azure.png" alt-text="Screenshot showing how to get the Azure endpoint." lightbox="../../custom-text-classification/media/get-endpoint-azure.png":::

1. Download and install the client library package for your language of choice:

    |Language  |Package version  |
    |---------|---------|
    |.NET     | [1.0.0](https://www.nuget.org/packages/Azure.AI.Language.Conversations/1.0.0)        |
    |Python     | [1.0.0](https://pypi.org/project/azure-ai-language-conversations/1.0.0)         |

1. After you install the client library, use the following samples on GitHub to start calling the API.

    * [C#](https://github.com/Azure/azure-sdk-for-net/tree/Azure.AI.Language.Conversations_1.0.0/sdk/cognitivelanguage/Azure.AI.Language.Conversations)
    * [Python](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-language-conversations_1.0.0/sdk/cognitivelanguage/azure-ai-language-conversations)

1. See the following reference documentation for more information:

    * [C#](/dotnet/api/azure.ai.language.conversations)
    * [Python](/python/api/azure-ai-language-conversations/azure.ai.language.conversations.aio)

## Related content

* [Orchestration workflow overview](../overview.md)
* [Evaluation metrics](../concepts/evaluation-metrics.md)
