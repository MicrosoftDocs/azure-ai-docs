---
title: Train a Foundry Tools custom translation model
titleSuffix: Foundry Tools
description: How to train a custom translation model in Microsoft Foundry.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 11/18/2025
ms.author: lajanuar
ms.topic: how-to
---

# Train a Foundry Tools custom translation model

A custom translation model provides translations for a specific language pair. The outcome of a successful training is a model. To train a custom translation model, three mutually exclusive document types are required: training, tuning, and testing. If only training data is provided when queuing a training, custom translation automatically assembles tuning and testing data. It uses a random subset of sentences from your training documents, and exclude these sentences from the training data itself. A minimum of 10,000 parallel training sentences are required to train a full model.

## Create your custom translation model

Here are the steps to create a custom translation model:

1. Follow [Upload data](upload-data.md), then continue here.

1. After the data is processed, select the **Train model** from the left menu.

   :::image type="content" source="../media/fine-tune-train-model-1.png" alt-text="Screenshot depicting the train model blade.":::

1. Type the **Model name**.

1. Select **Training type**.

   >[!NOTE]
   >Full training displays all uploaded document types. Dictionary-only displays dictionary documents only.

1. Select **Next**.

   :::image type="content" source="../media/fine-tune-train-model-2.png" alt-text="Screenshot illustrating train model blade.":::

1. Select the data you want to use for training and review the training cost associated with the selected number of sentences.

   :::image type="content" source="../media/fine-tune-train-model-3.png" alt-text="Screenshot depicting a view of the train model blade.":::

1. Select **Next**

1. Review and select **Train model**.

   :::image type="content" source="../media/fine-tune-train-model-4.png" alt-text="Screenshot illustrating the train model blade.":::

## When to select dictionary-only training

For better results, we recommended letting the system learn from your training data. However, when you don't have enough parallel sentences to meet the 10,000 minimum requirements, and sentences and compound nouns must be rendered as-is, use dictionary-only training. Your model typically completes training faster than with full training. The resulting models use the baseline models for translation along with the dictionaries you added. You don't see `BLEU` scores and test report.

> [!NOTE] 
>Custom translation doesn't sentence-align dictionary files. Therefore, it's important that there are an equal number of source and target phrases/sentences in your dictionary documents and that they're precisely aligned. If not, the document upload fails.

## Model details

1. After successful model training, select the **Train model** from the left menu, then select the model name.

1. Select the **Model Name** to review training date/time, total training time, number of sentences used for training, tuning, testing, dictionary, and whether the system generated the test and tuning sets. You use `Category ID` to make translation requests.

1. Evaluate the model [`BLEU` score](../beginners-guide.md#what-is-a-bleu-score). Review the test set: the **BLEU score** is the custom translation model score and the **Baseline BLEU** is the pretrained baseline model used for customization. A higher **BLEU score** means higher translation quality using the custom translation model.

   :::image type="content" source="../media/fine-tune-model-detail.png" alt-text="Screenshot illustrating the model details.":::

## Duplicate model

1. Select the **Train model** from the left menu.

1. Hover over the model name and check the selection button.

1. Select **Duplicate model**.

1. Fill in **New model name**.

1. Keep **Train immediately** checked if no more data is needed and ready to train, otherwise, check **Save as draft**.

1. Select **Duplicate**.

   > [!NOTE]
   >
   > If you save the model as `Draft`, **Model details** is updated with the model name in `Draft` status.
   >
   > To add more documents, select the model name and select **Manage data** from the left menu. 
   > Follow [Upload data](upload-data.md)

   :::image type="content" source="../media/fine-tune-duplicate-model.png" alt-text="Screenshot illustrating the duplicate model blade.":::

## Next steps

> [!div class="nextstepaction"]
> [Learn how to Test model](test-model.md)
