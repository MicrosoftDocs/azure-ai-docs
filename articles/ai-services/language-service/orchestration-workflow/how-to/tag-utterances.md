---
title: How to tag utterances in an orchestration workflow project
titleSuffix: Foundry Tools
description: Use this article to tag utterances
author: laujan
manager: mcleans
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-orchestration
---
<!-- markdownlint-disable MD025 -->

# Tag utterances in an orchestration workflow project

Once you [build a schema](build-schema.md), add training and testing utterances to your project in Microsoft Foundry. The utterances should be similar to what your users use when interacting with the project. When you add an utterance, you have to assign which intent it belongs to.

Adding utterances is a crucial step in the project development lifecycle; this data is used in the next step when training your model so the model can learn from the added data. If you already have utterances, you can directly [import them into your project](create-project.md#import-an-orchestration-workflow-project-rest-api), but you need to make sure that your data follows the [accepted data format](../concepts/data-formats.md). Labeled data informs the model how to interpret text and is used for training and evaluation.

## Prerequisites

* A successfully [created project](create-project.md).

For more information, *see* [project development lifecycle](../overview.md#project-development-lifecycle).

## How to add utterances

Use the following steps to add utterances in Foundry:

1. Open your orchestration workflow project in Microsoft Foundry.

1. From the left navigation menu, select **Manage Data** and then **Add utterances**.

1. Use the **Training set** and **Testing set** views to manage your data. Learn more about [training and testing sets](train-model.md#data-splitting) and how they're used for model training and evaluation.

1. From the **Select intent** dropdown menu, select one of the intents. Type your utterance, then press `Enter` to add it. You can also upload utterances directly by selecting **Upload utterance file** from the top menu. Make sure the utterances follow the [accepted format](../concepts/data-formats.md#utterance-format).

   > [!Note]
   > If you're planning on using **Automatically split the testing set from training data**, add all your utterances to the training set.
   > You can add training utterances to **nonconnected** intents only.

   :::image type="content" source="../media/tag-utterances.png" alt-text="A screenshot of the page for tagging utterances in Microsoft Foundry." lightbox="../media/tag-utterances.png":::

1. Under **Distribution**, view the distribution across training and testing sets. You can also view utterances per intent:

* Utterances per nonconnected intent
* Utterances per connected intent

## Next Steps

* [Train Model](./train-model.md)
