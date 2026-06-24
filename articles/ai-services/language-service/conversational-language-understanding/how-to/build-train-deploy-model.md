---
title: Build, train, and deploy a conversational language understanding model
titleSuffix: Foundry Tools
description: Build a schema, label utterances, train, evaluate, deploy, and query a conversational language understanding model in Microsoft Foundry.
author: laujan
manager: mcleans
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 06/23/2026
ms.author: lajanuar
ms.custom: language-service-clu
---

# Build, train, and deploy a conversational language understanding model

This article walks you through the complete conversational language understanding (CLU) fine-tuning lifecycle in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs): build a schema, label your utterances, train and evaluate a model, deploy it, and send prediction requests. Each stage links to the relevant concepts and reference content if you want to go deeper.

For an end-to-end introduction with a preconfigured sample project, see the [CLU quickstart](../quickstart.md). For the broader process, see the [project development lifecycle](../overview.md#project-development-lifecycle).

## Prerequisites

* **An active Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Foundry Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](../../../openai/how-to/role-based-access-control.md#cognitive-services-contributor).

  [!INCLUDE [role-rename-note](../../../../foundry/includes/role-rename-note.md)]
* **A project created in the Microsoft Foundry**. For more information, *see* [Create a Foundry project](../../../../ai-foundry/how-to/create-projects.md) and [Create a fine-tuning task project](create-project.md).

## Build your fine-tuning schema

In conversational language understanding projects, the *schema* is the combination of intents and entities within your project. Schema design is a crucial part of your project's success. When you create a schema, think about which intents and entities should be included.

### Guidelines and recommendations

Consider the following guidelines when you choose intents for your project:

* **Create distinct, separable intents.** An intent is best described as an action that the user wants to perform. Identify all the different actions that your users might take when they interact with your project. Sending, calling, and canceling are all actions that are best represented as different intents. "Canceling an order" and "canceling an appointment" are similar, with the distinction being *what* they're canceling. Those two actions should be represented under the same intent, *cancel*.
* **Create entities to extract relevant pieces of information within your text.** Entities capture the information needed to fulfill your user's action. For example, *order* or *appointment* could be different things that a user is trying to cancel, and you should create an entity to capture that piece of information.

You can "send a message," "send an email," or "send a package." Creating an intent to capture each of those requirements won't scale over time, and you should use entities to identify *what* the user was sending. The combination of intents and entities should determine your conversation flow.

For example, consider a company where the bot developers identified the three most common actions that their users take when they use a calendar:

* Set up new meetings.
* Respond to meeting requests.
* Cancel meetings.

They might create an intent to represent each of these actions, along with entities to help complete them, such as:

* Meeting attendants
* Date
* Meeting durations

### Add intents

To build a project schema within [Foundry](https://ai.azure.com/?cid=learnDocs):

1. On the left pane, select **Define schema**.

1. Select the **Intents** or **Entities** tabs.

1. To create an intent, select **+ Add intent**. You're prompted to enter names and descriptions for as many intents as you want to create. Descriptions are required only for using the **Quick Deploy** option to help Azure OpenAI better understand the context of your intents.

1. Repeat the steps to develop intents that encompass all the actions that the user is likely to perform while interacting with the project.

   :::image type="content" source="../media/build-schema-page.png" alt-text="A screenshot that shows the schema creation page for conversation projects in Microsoft Foundry." lightbox="../media/build-schema-page.png":::

### Add entities

1. Select the **Entities** tab.

1. To add an entity, select **+ Add entity**. You're prompted to enter a name to create the entity.

1. After you create an entity, you can select the entity name to change the **Entity components** type. Multiple components like learned, list, regex, or prebuilt are used to define every entity. A learned component is added to all your entities after you label them in your utterances.

   :::image type="content" source="../media/entity-details.png" alt-text="A screenshot that shows the Entity components page for conversation projects in Microsoft Foundry." lightbox="../media/entity-details.png":::

1. You can also add a [list](../concepts/entity-components.md#list-component), [regex](../concepts/entity-components.md#regex-component), or [prebuilt](../concepts/entity-components.md#prebuilt-component) component to each entity.

#### Add a prebuilt component

To add a prebuilt component, select the prebuilt type from the dropdown menu in the **Entity options** section.

#### Add a list component

To add a list component, select **Add list**. You can add multiple lists to each entity:

1. Create a new list, and in the **List key** text box, enter the normalized value that was returned when any of the synonyms values were extracted.

1. Enter your synonyms and select Enter after each one. We recommend having a synonym list in multiple languages.

#### Add a regex component

To add a regex component, select **Add expression**. Name the regex key, and enter a regular expression that matches the entity to be extracted.

#### Define entity options

Select the **Entity Options** tab on the entity details page. When multiple components are defined for an entity, their predictions might overlap. When an overlap occurs, each entity's final prediction is determined based on the [entity option](../concepts/entity-components.md#entity-options) that you select in this step. Select the option that you want to apply to this entity, and then select **Save**.

After you create your entities, you can come back and edit them. You can edit entity components or delete them by selecting **Edit** or **Delete**.

## Label your utterances

After you build a schema for your fine-tuning task, you add training utterances to your project. The utterances should be similar to what your users use when they interact with the project. When you add an utterance, you assign which intent it belongs to. After the utterance is added, label the words within your utterance that you want to extract as entities.

Data labeling is a crucial step in the CLU trained development lifecycle. This data is used in the next step when you train your model so that your model can learn from the labeled data. If you already labeled utterances, you can directly [import them into your project](create-project.md#import-an-existing-foundry-project), if your data follows the [accepted data format](../concepts/data-formats.md). Labeled data informs the model about how to interpret text and is used for training and evaluation.

> [!TIP]
> Use the **Quick Deploy** option to implement custom CLU intent routing, which is powered by your own large language model deployment without adding or labeling any training data.

### Data labeling guidelines

Labeling your data is important so that your model knows which sentences and words are associated with the intents and entities in your project. Spend time labeling your utterances to introduce and refine the data that's used in training your models.

As you add utterances and label them, keep in mind:

* The machine learning models generalize based on the labeled examples that you provide. The more examples that you provide, the more data points the model has to make better generalizations.
* The precision, consistency, and completeness of your labeled data are key factors to determining model performance:

  * **Label precisely:** Label each intent and entity to its right type always. Only include what you want classified and extracted. Avoid unnecessary data in your labels.
  * **Label consistently:** The same entity should have the same label across all the utterances.
  * **Label completely:** Provide varied utterances for every intent. Label all the instances of the entity in all your utterances.

[!INCLUDE [Label data best practices](../includes/label-data-best-practices.md)]

* For [multilingual projects](../language-support.md#multi-lingual-option), adding utterances in other languages increases the model's performance in these languages. Avoid duplicating your data across all the languages that you want to support. For example, to improve a calendar bot's performance with users, a developer might add examples mostly in English and a few in Spanish or French. They might add utterances such as:

  * `Set a meeting with **Matt** and **Kevin** **tomorrow** at **12 PM**.` (English)
  * `Reply as **tentative** to the **weekly update** meeting.` (English)
  * `Cancelar mi **próxima** reunión.` (Spanish)

### Label your utterances in Foundry

Use the following steps to label your utterances:

1. Go to your project page in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs).

1. On the left pane, select **Manage data**. On this page, you can add your utterances and label them. You can also upload your utterances directly by selecting **Upload utterance file** from the top menu. Make sure to follow the [accepted format](../concepts/data-formats.md#utterance-file-format).

1. By using the top tabs, you can change the view to **Training set** or **Testing set**. Learn more about [training and testing sets](#data-splitting) and how they're used for model training and evaluation.

    :::image type="content" source="../media/tag-utterances.png" alt-text="A screenshot that shows the page for tagging utterances in Foundry." lightbox="../media/tag-utterances.png":::

    > [!TIP]
    > If you plan to use **Automatically split the testing set from training data** splitting, add all your utterances to the training set.

1. From the **Select intent** dropdown menu, select one of the intents, the language of the utterance (for multilingual projects), and the utterance itself. Press the Enter key in the utterance's text box and add the utterance.

1. You have two options to label entities in an utterance:

    |Option |Description  |
    |---------|---------|
    |Label by using a brush     | Select the brush icon next to an entity in the pane on the right, and then highlight the text in the utterance that you want to label.           |
    |Label by using inline menu     | Highlight the word that you want to label as an entity, and a menu appears. Select the entity that you want to label these words with. |

1. In the pane on the right, on the **Labels** tab, you can find all the entity types in your project and the count of labeled instances per each one.

1. On the **Distribution** tab, you can view the distribution across training and testing sets. You have these options for viewing:
    * **Total instances per labeled entity:** You can view the count of all labeled instances of a specific entity.
    * **Unique utterances per labeled entity:** Each utterance is counted if it contains at least one labeled instance of this entity.
    * **Utterances per intent:** You can view the count of utterances per intent.

    :::image type="content" source="../media/label-distribution.png" alt-text="A screenshot that shows entity distribution in Foundry." lightbox="../media/label-distribution.png":::

  > [!NOTE]
  > List, regex, and prebuilt components aren't shown on the data labeling page. All labels here apply to the learned component only.

To remove a label:

  1. From within your utterance, select the entity from which you want to remove a label.
  1. Scroll through the menu that appears, and select **Remove label**.

To delete an entity:

  1. Select the garbage bin icon next to the entity that you want to edit in the pane on the right.
  1. Select **Delete** to confirm.

### Suggest utterances with Azure OpenAI

In CLU, use Azure OpenAI to suggest utterances to add to your project by using generative language models. We recommend that you use a Foundry resource while you use CLU so that you don't need to connect multiple resources.

To use the Foundry resource, you need to provide your Foundry resource with elevated access. To do so, access the Azure portal. Within your Azure AI resource, provide access as a **Cognitive Services User** to itself. This step ensures that all parts of your resource are communicating correctly.

#### Connect with separate Language and Azure OpenAI resources

You first need to get access and create a resource in Azure OpenAI. Next, create a connection to the Azure OpenAI resource within the same Foundry project in the **Management center** on the left pane of the Foundry page. You then need to create a deployment for the Azure OpenAI models within the connected Azure OpenAI resource. To create a new resource, follow the steps in [Create and deploy an Azure OpenAI in Foundry Models resource](../../../../ai-foundry/openai/how-to/create-resource.md).

Before you get started, the suggested utterances feature is available only if your Language resource is in the following regions:

* East US
* South Central US
* West Europe

On the **Data labeling** page:

1. Select **Suggest utterances**. A pane opens and prompts you to select your Azure OpenAI resource and deployment.
1. After you select an Azure OpenAI resource, select **Connect** so that your Language resource has direct access to your Azure OpenAI resource. It assigns your Language resource the **Cognitive Services User** role to your Azure OpenAI resource. Now your current Language resource has access to Azure OpenAI. If the connection fails, follow [these steps](#add-required-configurations-to-azure-openai-resource) to manually add the correct role to your Azure OpenAI resource.
1. After the resource is connected, select the deployment. The model that we recommend for the Azure OpenAI deployment is `gpt-35-turbo-instruct`.
1. Select the intent for which you want to get suggestions. Make sure the intent that you selected has at least five saved utterances to be enabled for utterance suggestions. The suggestions provided by Azure OpenAI are based on the most recent utterances that you added for that intent.
1. Select **Generate utterances**.

   The suggested utterances show up with a dotted line around them and the note **Generated by AI**. Those suggestions must be accepted or rejected. Accepting a suggestion adds it to your project, as if you had added it yourself. Rejecting a suggestion deletes it entirely. Only accepted utterances are part of your project and used for training or testing.

    To accept or reject, select the green check mark or red cancel buttons beside each utterance. You can also use **Accept all** and **Reject all** on the toolbar.

    :::image type="content" source="../media/suggest-utterances.png" alt-text="A screenshot that shows suggested utterances." lightbox="../media/suggest-utterances.png":::

Use of this feature entails a charge to your Azure OpenAI resource for a similar number of tokens to the suggested utterances that are generated. For information on Azure OpenAI pricing, see [Azure OpenAI Service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

#### Add required configurations to Azure OpenAI resource

Enable identity management for your Language resource by using the following options.

##### [Azure portal](#tab/portal)

Your Language resource must have identity management. To enable it by using the [Azure portal](https://portal.azure.com):

1. Go to your Language resource.
1. On the left pane, under the **Resource Management** section, select **Identity**.
1. On the **System assigned** tab, set **Status** to **On**.

##### [Microsoft Foundry](#tab/foundry)

Your Language resource must have identity management. To enable it by using the [Microsoft Foundry](https://ai.azure.com/):

1. Select the settings icon in the upper-right corner of the screen.
1. Select **Resources**.
1. Select the **Managed Identity** check box for your Language resource.

---

After you enable managed identity, assign the **Cognitive Services User** role to your Azure OpenAI resource by using the managed identity of your Language resource.

  1. Sign in to the [Azure portal](https://portal.azure.com) and go to your Azure OpenAI resource.
  1. Select the **Access Control (IAM)** tab.
  1. Select **Add** > **Add role assignment**.
  1. Select **Job function roles** and select **Next**.
  1. Select **Cognitive Services User** from the list of roles, and select **Next**.
  1. Select **Assign access to: Managed identity** and choose **Select members**.
  1. Under **Managed identity**, select **Language**.
  1. Search for your resource and select it. Then select **Next** and complete the process.
  1. Review the details and select **Review + assign**.

     :::image type="content" source="../media/add-role-azure-openai.gif" alt-text="Multiple screenshots that show the steps to add the required role to your Azure OpenAI resource." lightbox="../media/add-role-azure-openai.gif":::

After a few minutes, refresh Foundry, and you can successfully connect to Azure OpenAI.

## Train your model

After you complete labeling your utterances, you can start training a model. Training is the process where the model learns from your labeled utterances. To train a model, start a training job. Only successfully completed jobs create a model. Training jobs expire after seven days, then you can no longer retrieve the job details. If your training job completed successfully and a model was created, the job doesn't expire. You can only have one training job running at a time, and you can't start other jobs in the same fine-tuning task.

> [!NOTE]
>
> When using the **Quick Deploy** option, CLU automatically creates an instant training job to set up your CLU intent router using your selected `LLM` deployment.

Model evaluation is triggered automatically after training is completed successfully. The evaluation process starts by using the trained model to run predictions on the utterances in the testing set, and compares the predicted results with the provided labels (which establishes a baseline of truth).

### Balance training data

When it comes to training data, try to keep your schema well-balanced. Including large quantities of one intent and few of another results in a model with bias towards particular intents.

To address this scenario, you might need to down sample your training set. Or you might need to add to it. To down sample, you can:

* Get rid of a certain percentage of the training data randomly.
* Analyze the dataset and remove overrepresented duplicate entries, which is a more systematic manner.

To add to the training set, in Microsoft Foundry, on the **Data labeling** tab, select **Suggest utterances**. CLU sends a call to [Azure OpenAI](../../../openai/overview.md) to generate similar utterances.

You should also look for unintentional patterns in the training set. For example, look to see if the training set for a particular intent is all lowercase or starts with a particular phrase. In such cases, the model you train might learn these unintended biases in the training set instead of being able to generalize.

We recommend that you introduce casing and punctuation diversity in the training set. If your model is expected to handle variations, be sure to have a training set that also reflects that diversity. For example, include some utterances in proper casing and some in all lowercase.

### Data splitting

Before you start the training process, labeled utterances in your project are divided into a training set and a testing set. Each one serves a different function:

* The **training set** is used in training the model, the set from which the model learns the labeled utterances.
* The **testing set** is a blind set that isn't introduced to the model during training but only during evaluation.

After the model is trained successfully, the model can be used to make predictions from the utterances in the testing set. These predictions are used to calculate [evaluation metrics](../concepts/evaluation-metrics.md). We recommend that you make sure that all your intents and entities are adequately represented in both the training and testing set.

CLU supports two methods for data splitting:

* **Automatically splitting the testing set from training data**: The system splits your tagged data between the training and testing sets, according to the percentages you choose. The recommended percentage split is 80% for training and 20% for testing.

 > [!NOTE]
 > If you choose the **Automatically splitting the testing set from training data** option, only the data assigned to a training set is split according to the percentages provided.

* **Use a manual split of training and testing data**: This method enables users to define which utterances should belong to which set. This step is only enabled if you added utterances to your testing set during labeling.

### Training modes

CLU supports two modes for training your models:

* **Standard training** uses fast machine learning algorithms to quickly train your models. This training level is currently only available for **English** and is disabled for any project that doesn't use English (US), or English (UK) as its primary language. This training option is free of charge. Standard training allows you to add utterances and test them quickly free of charge. The evaluation scores shown should guide you on where to make changes in your project and add more utterances. While standard training is best for testing and updating your model quickly, you should see better model quality when using advanced training. Once you iterate a few times and made incremental improvements, you can consider using advanced training to train another version of your model.

* **Advanced training** uses the latest in machine learning technology to customize models with your data. This training level is expected to show better performance scores for your models and enables you to use the [multilingual capabilities](../language-support.md#multi-lingual-option) of CLU as well. Advanced training is priced differently. See the [pricing information](https://azure.microsoft.com/pricing/details/cognitive-services/language-service) for details.

Use the evaluation scores to guide your decisions. There may be times where a specific example is predicted incorrectly in advanced training as opposed to when you used standard training mode. However, if the overall evaluation results are better using advanced training, then we recommend that you use that model as your final model. If that isn't the case and you aren't looking to use any multilingual capabilities, you can continue to use a model trained with standard mode.

> [!NOTE]
> You should expect to see a difference in behaviors in intent confidence scores between the training modes as each algorithm calibrates their scores differently.

### Start a training job

# [Foundry](#tab/ai-foundry)

1. Navigate to the [Foundry](https://ai.azure.com/).
1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.
1. Once signed in, you can create or access your existing projects within Foundry.
1. If you're not already at your project for this task, select it.
1. Select Fine-tuning from the left navigation pane.

   :::image type="content" source="../media/select-fine-tuning.png" alt-text="Screenshot of fine-tuning selector in the Foundry.":::

1. Select **the AI Service fine-tuning** tab and then **+ Fine-tune** button.

   :::image type="content" source="../media/fine-tune-button.png" alt-text="Screenshot of fine-tuning button in the Foundry.":::

1. From **Create service fine-tuning** window, choose the **Conversational language understanding** tab then select **Next**.

   :::image type="content" source="../media/select-project.png" alt-text="Screenshot of conversational language understanding tab in the Foundry.":::

1. In **Create CLU fine tuning task** window, select your **Connected service** from the drop-down menu, then complete the **Name** and **Language** fields. If you're using the free **Standard Training** mode, select **English** for the language field.

1. Select the  **Create** button. It may take a few minutes for the operation to complete.

1. From the immediate left navigation pane, choose **Train model**.

   :::image type="content" source="../media/train-fine-tuning-model.png" alt-text="Screenshot of the train model selection in the Foundry.":::

1. Next, select the **+ Train model** button from the main window.
1. In the **Train a new model** window, select one of the following:

   * **Create a new training model**. Enter a new **Model name**
   * **Overwrite an existing model name**. Replace an existing model trained on the new data.
1. Select **Your current training version**. The training version is the algorithm that determines how your model learns from your data. The machine learning used to train models is regularly updated. We recommend using the latest version for training, as it underwent thorough testing and provides the most balanced model predictions from your data.

   :::image type="content" source="../media/select-mode.png" alt-text="Screenshot of select a mode options in the Foundry." :::

1. Select **Next**.

1. Select one of the **Data splitting** methods presented in the **Train a new model** window:

   * **Automatically split the testing set from training data** enables the system to split your utterances between the training and testing sets, according to the specified percentages.
   * **Use a manual split of training and testing data** enables the system to use the training and testing sets that you assigned and labeled to create your custom model. *This option is only available if you added utterances to your testing set when you labeled your utterances*.

      :::image type="content" source="../media/data-splitting.png" alt-text="Screenshot of data splitting option in the Foundry.":::

1. Select **Next** and then select **Create**.

1. Choose the training job ID from the list. A panel appears that details the training progress, job status, and other details for this job.

> [!NOTE]
>
> * Only successfully completed training jobs generate models.
> * Training can take from a few minutes to a few hours based on the count of utterances.
> * You can only have one training job running at a time. You can't start other training jobs within the same project until the running job is completed.

# [REST APIs](#tab/rest-api)

#### Start training job

[!INCLUDE [train model](../includes/rest-api/train-model.md)]

#### Get training job status

Training could take some time depending on the size of your training data and complexity of your schema. You can use the following request to keep polling the status of the training job until it successfully completes.

[!INCLUDE [get training model status](../includes/rest-api/get-training-status.md)]

---

### Cancel a training job

# [Foundry](#tab/ai-foundry)

When you're done with your custom model, you can delete the deployment and model. You can also delete the training and validation files you uploaded to the service, if needed:

* To delete your custom model, on the left navigation pane select **My assets** → **Models + endpoints**. Choose the custom model to delete from the **Model deployments** tab, and then select **Delete**.
* To delete your training and validation files uploaded for training, on the left navigation pane select **Data + indexes**. Choose the file to delete, and then select **Delete**.

  :::image type="content" source="../media/my-assets.png" alt-text="Screenshot of my assets section in the Foundry.":::

# [REST APIs](#tab/rest-api)

[!INCLUDE [Cancel training](../includes/rest-api/cancel-training.md)]

---

## View model details

After model training is completed, you can view your model details and see how well it performs against the test set.

> [!NOTE]
> Using the **Automatically split the testing set from training data** option may result in different model evaluation result every time you train a new model, as the test set is selected randomly from your utterances. To make sure that the evaluation is calculated on the same test set every time you train a model, make sure to use the **Use a manual split of training and testing data** option when starting a training job and define your **Testing set** when you add your utterances.

### Model details

[!INCLUDE [Evaluate model](../includes/rest-api/model-evaluation.md)]

### Load or export model data

[!INCLUDE [Load export model](../includes/rest-api/load-export-model.md)]

### Delete model

[!INCLUDE [Delete model](../includes/rest-api/delete-model.md)]

As you review how your model performs, learn about the [evaluation metrics](../concepts/evaluation-metrics.md) that are used.

## Deploy your model

Once you're satisfied with how your model performs, it's ready to be deployed so you can query it for predictions from utterances. Deploying a model makes it available for use through the [prediction API](/rest/api/language/2023-04-01/conversation-analysis-runtime/analyze-conversation).

After you review the model's performance and decide it can be used in your environment, you need to assign it to a deployment to be able to query it. We recommend creating a deployment named `production` to which you assign the best model you built so far and use it in your system. You can create another deployment called `staging` to which you can assign the model you're currently working on to be able to test it. You can have a maximum of 10 deployments in your project.

### Submit deployment job

[!INCLUDE [deploy model](../includes/rest-api/deploy-model.md)]

### Get deployment job status

[!INCLUDE [get deployment status](../includes/rest-api/get-deployment-status.md)]

### Swap deployments

After you're done testing a model assigned to one deployment, you might want to assign it to another deployment. Swapping deployments involves:

* Taking the model assigned to the first deployment, and assigning it to the second deployment.
* Taking the model assigned to the second deployment and assigning it to the first deployment.

For example, you can swap your `production` and `staging` deployments when you want to take the model assigned to `staging` and assign it to `production`.

[!INCLUDE [Swap deployments](../includes/rest-api/swap-deployment.md)]

### Delete deployment

[!INCLUDE [Delete deployment](../includes/rest-api/delete-deployment.md)]

### Assign deployment resources

You can [deploy your project to multiple regions](../../concepts/custom-features/multi-region-deployment.md) by assigning different Language resources that exist in different regions.

[!INCLUDE [Assign resource](../includes/rest-api/assign-resources.md)]

### Unassign deployment resources

When unassigning or removing a deployment resource from a project, you also delete all the deployments that are deployed to the resource's region.

[!INCLUDE [Unassign resource](../includes/rest-api/unassign-resources.md)]

## Send prediction requests to a deployment

After the deployment is added successfully, you can query the deployment for intent and entities predictions from your utterance based on the model you assigned to the deployment. You can query the deployment programmatically through the [prediction API](https://aka.ms/ct-runtime-swagger) or through the client libraries (Azure SDK).

### Test the deployed model

Once your model is deployed, you can test it by sending prediction requests to evaluate its performance with real utterances. Testing helps you verify that the model accurately identifies intents and extracts entities as expected before integrating it into your production applications. You can test your deployment using either the REST API or the Azure SDK client libraries.

First you need to get your resource key and endpoint:

[!INCLUDE [Get keys and endpoint Azure portal](../includes/get-keys-endpoint-azure.md)]

### Query your model

[!INCLUDE [Query model](../includes/rest-api/query-model.md)]

You can also use the client libraries provided by the Azure SDK to send requests to your model.

> [!NOTE]
> The client library for conversational language understanding is only available for:
>
> * .NET
> * Python

1. Go to your resource overview page in the [Azure portal](https://portal.azure.com/#home)

1. From the menu on the left side, select **Keys and Endpoint**. Use endpoint for the API requests and you need the key for `Ocp-Apim-Subscription-Key` header.

    :::image type="content" source="../../custom-text-classification/media/get-endpoint-azure.png" alt-text="A screenshot showing a key and endpoint in the Azure portal." lightbox="../../custom-text-classification/media/get-endpoint-azure.png":::

1. Download and install the client library package for your language of choice:

    | Language | Package version |
    |--|--|
    | .NET | [1.0.0](https://www.nuget.org/packages/Azure.AI.Language.Conversations/1.0.0) |
    | Python | [1.0.0](https://pypi.org/project/azure-ai-language-conversations/1.0.0) |

1. After you install the client library, use the following samples on GitHub to start calling the API.

    * [C#](https://github.com/Azure/azure-sdk-for-net/tree/Azure.AI.Language.Conversations_1.0.0/sdk/cognitivelanguage/Azure.AI.Language.Conversations)
    * [Python](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-language-conversations_1.0.0/sdk/cognitivelanguage/azure-ai-language-conversations)

1. For more information, *see* the following reference documentation:

    * [C#](/dotnet/api/azure.ai.language.conversations)
    * [Python](/python/api/azure-ai-language-conversations/azure.ai.language.conversations.aio)

## Related content

* [Conversational language understanding overview](../overview.md)
* [CLU quickstart](../quickstart.md)
* [Evaluation metrics](../concepts/evaluation-metrics.md)
* [Build multi-turn CLU models with entity slot filling](build-multi-turn-model.md)
</content>
