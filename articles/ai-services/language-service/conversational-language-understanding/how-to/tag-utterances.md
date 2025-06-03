---
title: How to tag utterances in Conversational Language Understanding
titleSuffix: Azure AI services
description: Use this article to tag your utterances in Conversational Language Understanding projects
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 05/20/2025
ms.author: lajanuar
ms.custom: language-service-clu
---

# Label your utterances in AI Foundry

Once you [build a schema](build-schema.md) for your fine-tuning task, you should add training utterances to your project. The utterances should be similar to what your users use when interacting with the project. When you add an utterance, you have to assign which intent it belongs to. After the utterance is added, label the words within your utterance that you want to extract as entities.

Data labeling is a crucial step in the conversational language understanding `CLU` trained development lifecycle; this data are used in the next step when training your model so that your model can learn from the labeled data. If you already labeled utterances, you can directly [import it into your project](create-project.md#import-project), IF your data follows the [accepted data format](../concepts/data-formats.md). See [create fine-tuning task](create-project.md#import-project) to learn more about importing labeled data. Labeled data informs the model how to interpret text and is used for training and evaluation.

   > [!TIP]
  > Use the `Quick Deploy` option to implement custom `CLU` intent routing, powered by your own `LLM` model deployment without adding or labeling any training data.

## Prerequisites

Before you can label your data, you need:

* A successfully [created project](create-project.md).

For more information, see the [conversational language understanding development lifecycle](../overview.md#project-development-lifecycle).

## Data labeling guidelines

After [building your schema](build-schema.md) and [creating your project](create-project.md), you need to label your data. Labeling your data is important so your model knows which sentences and words are associated with the intents and entities in your project. Spend time labeling your utterances - introducing and refining the data that is used in training your models.

As you add utterances and label them, keep in mind:

* The machine learning models generalize based on the labeled examples you provide it; the more examples you provide, the more data points the model has to make better generalizations.

* The precision, consistency, and completeness of your labeled data are key factors to determining model performance.

    * **Label precisely**: Label each intent and entity to its right type always. Only include what you want classified and extracted, avoid unnecessary data in your labels.
    * **Label consistently**:  The same entity should have the same label across all the utterances.
    * **Label completely**: Provide varied utterances for every intent. Label all the instances of the entity in all your utterances.

[!INCLUDE [Label data best practices](../includes/label-data-best-practices.md)]

* For [Multilingual projects](../language-support.md#multi-lingual-option), adding utterances in other languages increases the model's performance in these languages, but avoid duplicating your data across all the languages you would like to support. For example, to improve a calender bot's performance with users, a developer might add examples mostly in English, and a few in Spanish or French as well. They might add utterances such as:

  * "_Set a meeting with **Matt** and **Kevin** **tomorrow** at **12 PM**._" (English)
  * "_Reply as **tentative** to the **weekly update** meeting._" (English)
  * "_Cancelar mi **próxima** reunión_." (Spanish)

## How to label your utterances

Use the following steps to label your utterances:

1. Go to your project page in [AI Foundry](https://ai.azure.com/?cid=learnDocs).

1. From the left side menu, select `Manage data`. In this page, you can start adding your utterances and labeling them. You can also upload your utterances directly by clicking on `Upload utterance file` from the top menu. Make sure it follows the [accepted format](../concepts/data-formats.md#utterance-file-format).

1. From the top pivots, you can change the view to be `training set` or `testing set`. Learn more about [training and testing sets](train-model.md#data-splitting) and how they're used for model training and evaluation.

    :::image type="content" source="../media/tag-utterances.png" alt-text="A screenshot of the page for tagging utterances in Language Studio." lightbox="../media/tag-utterances.png":::

    > [!TIP]
    > If you're planning on using `Automatically split the testing set from training data` splitting, add all your utterances to the training set.


1.  From the `Select intent` dropdown menu, select one of the intents, the language of the utterance (for multilingual projects), and the utterance itself. Press enter key in the utterance's text box and add the utterance.

1. You have two options to label entities in an utterance:

    |Option |Description  |
    |---------|---------|
    |Label using a brush     | Select the brush icon next to an entity in the right pane, then highlight the text in the utterance you want to label.           |
    |Label using inline menu     | Highlight the word you want to label as an entity, and a menu appears. Select the entity you want to label these words with. |

1. In the right side pane, under the `Labels` pivot, you can find all the entity types in your project and the count of labeled instances per each.

1. Under the `Distribution` pivot, you can view the distribution across training and testing sets. You have two options for viewing:
    * *Total instances per labeled entity* where you can view count of all labeled instances of a specific entity.
    * *Unique utterances per labeled entity* where each utterance is counted if it contains at least one labeled instance of this entity.
    * *Utterances per intent* where you can view count of utterances per intent.

    :::image type="content" source="../media/label-distribution.png" alt-text="A screenshot showing entity distribution in Language Studio." lightbox="../media/label-distribution.png":::


  > [!NOTE]
  > List, regex, and prebuilt components aren't shown in the data labeling page, and all labels here only apply to the **learned component**.

To remove a label:
  1. From within your utterance, select the entity you want to remove a label from.
  1. Scroll through the menu that appears, and select **Remove label**.

To delete an entity:
  1. Select the garbage bin icon next to the entity you want to edit in the right side pane. Then select **Delete** to confirm.

## Suggest utterances with Azure OpenAI

In `CLU`, use Azure OpenAI to suggest utterances to add to your project using generative language models. We recommended that you use an AI Foundry resource while using `CLU`, so you don't need to connect multiple resources. In order to use the AI Foundry resource, you need to provide your AI Foundry resource with elevated access. To do so, access the Azure portal. Within your Azure AI resource, provide access as a *Cognitive Services User* to itself. This step ensures that all parts of your resource are communicating correctly.

### Connect with separate Language and Azure OpenAI Resources

You first need to get access and create a resource in Azure OpenAI. Next, create a connection to the Azure OpenAI resource within the same AI Foundry project in the `Management center` in the left panel of the Azure AI Foundry page. You then need to create a deployment for the AOAI models within the connected AOAI resource. Follow the prerequisite steps [here](../../../openai/how-to/create-resource.md) to create a new resource.

Before you get started, the suggested utterances feature is only available if your Language resource is in the following regions:
* East US
* South Central US
* West Europe

In the Data Labeling page:

1. Select the `Suggest utterances` button. A pane opens up on the right side prompting you to select your Azure OpenAI resource and deployment.
1. On selection of an Azure OpenAI resource, select `Connect`, which allows your Language resource to have direct access to your Azure OpenAI resource. It assigns your Language resource the role of `Cognitive Services User` to your Azure OpenAI resource, which allows your current Language resource to have access to Azure OpenAI's service. If the connection fails, the following [steps](#add-required-configurations-to-azure-openai-resource) enable you to manually add the correct role to your Azure OpenAI resource.
1. Once the resource is connected, select the deployment. The recommended model for the Azure OpenAI deployment is `gpt-35-turbo-instruct`.
1. Select the intent you'd like to get suggestions for. Make sure the intent you selected has at least five saved utterances to be enabled for utterance suggestions. The suggestions provided by Azure OpenAI are based on the `most recent utterances` you added for that intent.
1. Select `Generate utterances`. Once complete, the suggested utterances  show up with a dotted line around it, with the note *Generated by AI*. Those suggestions need to be accepted or rejected. Accepting a suggestion simply adds it to your project, as if you had added it yourself. Rejecting it deletes the suggestion entirely. Only accepted utterances are part of your project and used for training or testing. You can accept or reject by clicking on the green check or red cancel buttons beside each utterance. You can also use the `Accept all` and `Reject all` buttons in the toolbar.

    :::image type="content" source="../media/suggest-utterances.png" alt-text="A screenshot showing suggested utterances." lightbox="../media/suggest-utterances.png":::

Using this feature entails a charge to your Azure OpenAI resource for a similar number of tokens to the suggested utterances generated. Details for Azure OpenAI's pricing can be found [here](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

### Add required configurations to Azure OpenAI resource

Enable identity management for your Language resource using the following options:

#### [Azure portal](#tab/portal)

Your Language resource must have identity management, to enable it using the [Azure portal](https://portal.azure.com):

1. Go to your Language resource.
1. From left hand menu, under `Resource Management` section, select `Identity`.
1. From `System assigned` tab, make sure to set `Status` to `On`.

#### [Language Studio](#tab/studio)

Your Language resource must have identity management, to enable it using [Language Studio](https://aka.ms/languageStudio):

1. Select the settings icon in the top right corner of the screen.
1. Select *`Resources`.
1. Select the check box `Managed Identity` for your Language resource.

---

After enabling managed identity, assign the role `Cognitive Services User` to your Azure OpenAI resource using the managed identity of your Language resource.

  1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your Azure OpenAI resource.
  1. Select the `Access Control (IAM)` tab.
  1. Select `Add` > Add role assignment.
  1. Select `Job function roles` and select `Next`.
  1. Select `Cognitive Services User` from the list of roles and select `Next`.
  1. Select Assign access to "Managed identity" and select `Select members`.
  1. Under `Managed identity` select `Language`.
  1. Search for your resource and select it. Then select `Next` and complete the process.
  1. Review the details and select `Review + Assign`.

     :::image type="content" source="../media/add-role-azure-openai.gif" alt-text="Multiple screenshots showing the steps to add the required role to your Azure OpenAI resource." lightbox="../media/add-role-azure-openai.gif":::

After a few minutes, refresh the AI Foundry, and you can successfully connect to Azure OpenAI.

## Next Steps
* [Train Model](./train-model.md)
