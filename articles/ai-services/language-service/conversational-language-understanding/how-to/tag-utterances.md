---
title: Tag Utterances in Conversational Language Understanding
titleSuffix: Foundry Tools
description: This article shows you how to tag your utterances in conversational language understanding projects.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-clu
---
# Label your utterances in Microsoft Foundry

After you [build a schema](build-schema.md) for your fine-tuning task, you add training utterances to your project. The utterances should be similar to what your users use when they interact with the project. When you add an utterance, you have to assign which intent it belongs to. After the utterance is added, label the words within your utterance that you want to extract as entities.

Data labeling is a crucial step in the conversational language understanding (CLU) trained development lifecycle. This data is used in the next step when you train your model so that your model can learn from the labeled data. If you already labeled utterances, you can directly [import them into your project](create-project.md#import-an-existing-foundry-project), if your data follows the [accepted data format](../concepts/data-formats.md). To learn more about importing labeled data, see [Create a CLU fine-tuning task](create-project.md#import-an-existing-foundry-project). Labeled data informs the model about how to interpret text and is used for training and evaluation.

> [!TIP]
> Use the **Quick Deploy** option to implement custom CLU intent routing, which is powered by your own large language model deployment without adding or labeling any training data.

## Prerequisites

* A successfully [created project](create-project.md).

For more information, see the [CLU development lifecycle](../overview.md#project-development-lifecycle).

## Data labeling guidelines

After you [build your schema](build-schema.md) and [create your project](create-project.md), you need to label your data. Labeling your data is important so that your model knows which sentences and words are associated with the intents and entities in your project. Spend time labeling your utterances to introduce and refine the data that's used in training your models.

As you add utterances and label them, keep in mind:

* The machine learning models generalize based on the labeled examples that you provide. The more examples that you provide, the more data points the model has to make better generalizations.
* The precision, consistency, and completeness of your labeled data are key factors to determining model performance:

    * **Label precisely:** Label each intent and entity to its right type always. Only include what you want classified and extracted. Avoid unnecessary data in your labels.
    * **Label consistently:** The same entity should have the same label across all the utterances.
    * **Label completely:** Provide varied utterances for every intent. Label all the instances of the entity in all your utterances.

[!INCLUDE [Label data best practices](../includes/label-data-best-practices.md)]

* For [multilingual projects](../language-support.md#multi-lingual-option), adding utterances in other languages increases the model's performance in these languages. Avoid duplicating your data across all the languages that you want to support. For example, to improve a calender bot's performance with users, a developer might add examples mostly in English and a few in Spanish or French. They might add utterances such as:

  * `Set a meeting with **Matt** and **Kevin** **tomorrow** at **12 PM**.` (English)
  * `Reply as **tentative** to the **weekly update** meeting.` (English)
  * `Cancelar mi **próxima** reunión.` (Spanish)

## Label your utterances

Use the following steps to label your utterances:

1. Go to your project page in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs).

1. On the left pane, select **Manage data**. On this page, you can add your utterances and label them. You can also upload your utterances directly by selecting **Upload utterance file** from the top menu. Make sure to follow the [accepted format](../concepts/data-formats.md#utterance-file-format).

1. By using the top tabs, you can change the view to **Training set** or **Testing set**. Learn more about [training and testing sets](train-model.md#data-splitting) and how they're used for model training and evaluation.

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

## Suggest utterances with Azure OpenAI

In CLU, use Azure OpenAI to suggest utterances to add to your project by using generative language models. We recommend that you use a Foundry resource while you use CLU so that you don't need to connect multiple resources. 

To use the Foundry resource, you need to provide your Foundry resource with elevated access. To do so, access the Azure portal. Within your Azure AI resource, provide access as a **Cognitive Services User** to itself. This step ensures that all parts of your resource are communicating correctly.

### Connect with separate Language and Azure OpenAI resources

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

### Add required configurations to Azure OpenAI resource

Enable identity management for your Language resource by using the following options.

#### [Azure portal](#tab/portal)

Your Language resource must have identity management. To enable it by using the [Azure portal](https://portal.azure.com):

1. Go to your Language resource.
1. On the left pane, under the **Resource Management** section, select **Identity**.
1. On the **System assigned** tab, set **Status** to **On**.

#### [Language Studio](#tab/studio)

Your Language resource must have identity management. To enable it by using [Language Studio](https://aka.ms/languageStudio):

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

## Related content

* [Train your conversational language understanding model](./train-model.md)
