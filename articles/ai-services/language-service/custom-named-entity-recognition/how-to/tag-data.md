---
title: How to label your data for Custom Named Entity Recognition (NER)
titleSuffix: Azure AI services
description: Learn how to label your data for use with Custom Named Entity Recognition (NER).
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/21/2024
ms.author: jboback
ms.custom: language-service-custom-ner
---

# Label your data in Language Studio

Before training your model you need to label your documents with the custom entities you want to extract. Data labeling is a crucial step in development lifecycle. In this step you can create the entity types you want to extract from your data and label these entities within your documents. This data will be used in the next step when training your model so that your model can learn from the labeled data. If you already have labeled data, you can directly [import](create-project.md#import-project) it into your project but you need to make sure that your data follows the [accepted data format](../concepts/data-formats.md). See [create project](create-project.md#import-project) to learn more about importing labeled data into your project.

Before creating a custom NER model, you need to have labeled data first. If your data isn't labeled already, you can label it in the [Language Studio](https://aka.ms/languageStudio). Labeled data informs the model how to interpret text, and is used for training and evaluation.

## Prerequisites

Before you can label your data, you need:

* A successfully [created project](create-project.md) with a configured Azure blob storage account
* Text data that [has been uploaded](design-schema.md#data-preparation) to your storage account.

See the [project development lifecycle](../overview.md#project-development-lifecycle) for more information.

## Data labeling guidelines

After [preparing your data, designing your schema](design-schema.md) and [creating your project](create-project.md), you will need to label your data. Labeling your data is important so your model knows which words will be associated with the entity types you need to extract. When you label your data in [Language Studio](https://aka.ms/languageStudio) (or import labeled data), these labels will be stored in the JSON document in your storage container that you have connected to this project. 

As you label your data, keep in mind:

* In general, more labeled data leads to better results, provided the data is labeled accurately.

* The precision, consistency and completeness of your labeled data are key factors to determining model performance. 

    * **Label precisely**: Label each entity to its right type always. Only include what you want extracted, avoid unnecessary data in your labels.
    * **Label consistently**:  The same entity should have the same label across all the documents.
    * **Label completely**: Label all the instances of the entity in all your documents. You can use the [auto labelling feature](use-autolabeling.md) to ensure complete labeling.

   > [!NOTE]
   > There is no fixed number of labels that can guarantee your model will perform the best. Model performance is dependent on possible ambiguity in your [schema](design-schema.md), and the quality of your labeled data. Nevertheless, we recommend having around 50 labeled instances per entity type.

## Label your data

Use the following steps to label your data:

1. Go to your project page in [Language Studio](https://aka.ms/languageStudio).

2. From the left side menu, select **Data labeling**. You can find a list of all documents in your storage container.

    <!--:::image type="content" source="../media/tagging-files-view.png" alt-text="A screenshot showing the Language Studio screen for labeling data." lightbox="../media/tagging-files-view.png":::-->

    >[!TIP]
    > You can use the filters in top menu to view the unlabeled documents so that you can start labeling them.
    > You can also use the filters to view the documents that are labeled with a specific entity type.

3. Change to a single document view from the left side in the top menu or select a specific document to start labeling. You can find a list of all `.txt` documents available in your project to the left. You can use the **Back** and **Next** button from the bottom of the page to navigate through your documents.

    > [!NOTE]
    > If you enabled multiple languages for your project, you will find a **Language** dropdown in the top menu, which lets you select the language of each document.

4. In the right side pane, **Add entity type** to your project so you can start labeling your data with them.

    <!--:::image type="content" source="../media/tag-1.png" alt-text="A screenshot showing complete data labeling." lightbox="../media/tag-1.png":::-->

6. You have two options to label your document:
    
    |Option |Description  |
    |---------|---------|
    |Label using a brush     | Select the brush icon next to an entity type in the right pane, then highlight the text in the document you want to annotate with this entity type.           |
    |Label using a menu    | Highlight the word you want to label as an entity, and a menu will appear. Select the entity type you want to assign for this entity.        |
    
    The below screenshot shows labeling using a brush.
    
    :::image type="content" source="../media/tag-options.png" alt-text="A screenshot showing the labeling options offered in Custom NER." lightbox="../media/tag-options.png":::
    
6. In the right side pane under the **Labels** pivot you can find all the entity types in your project and the count of labeled instances per each.

6. In the bottom section of the right side pane you can add the current document you are viewing to the training set or the testing set. By default all the documents are added to your training set. Learn more about [training and testing sets](train-model.md#data-splitting) and how they are used for model training and evaluation.

    > [!TIP]
    > If you are planning on using **Automatic** data splitting, use the default option of assigning all the documents into your training set.

7. Under the **Distribution** pivot you can view the distribution across training and testing sets. You have two options for viewing:
   * *Total instances* where you can view count of all labeled instances of a specific entity type.
   * *documents with at least one label* where each document is counted if it contains at least one labeled instance of this entity.
  
7. When you're labeling, your changes will be synced periodically, if they have not been saved yet you will find a warning at the top of your page. If you want to save manually, select **Save labels** button at the bottom of the page.

## Remove labels

To remove a label

1. Select the entity you want to remove a label from.
2. Scroll through the menu that appears, and select **Remove label**.

## Delete entities

To delete an entity, select the delete icon next to the entity you want to remove. Deleting an entity will remove all its labeled instances from your dataset.

## Next steps

After you've labeled your data, you can begin [training a model](train-model.md) that will learn based on your data.
