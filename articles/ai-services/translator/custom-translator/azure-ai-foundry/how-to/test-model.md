---
title: View your Foundry Tools custom translation test model details 
description: How to test your custom translation model BLEU score and evaluate translations
titleSuffix: Foundry Tools
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 11/18/2025
ms.author: lajanuar
ms.topic: how-to
---

# Test your Foundry Tools custom translation model

Once your Microsoft Foundry custom translation model is successfully trained, you can use translations to evaluate the quality of your model. In order to make an informed decision about whether to use our standard Azure Translator model or your custom translation model, you should evaluate the delta between your custom translation model [**BLEU score**](#bleu-score) and our standard Azure Translator model **Baseline BLEU**. If your model is trained within a narrow domain, and your training data is consistent with the test data, you can expect a high BLEU score.

## BLEU score

BLEU (Bilingual Evaluation Understudy) is an algorithm for evaluating the precision or accuracy of text that's machine translated from one language to another. Custom Translator uses the BLEU metric as one way of conveying translation accuracy.

A BLEU score is a number between zero and 100. A score of zero indicates a low-quality translation where nothing in the translation matched the reference. A score of 100 indicates a perfect translation that's identical to the reference. It's not necessary to attain a score of 100—a BLEU score between 40 and 60 indicates a high-quality translation.

[Read more](../concepts/bleu-score.md?WT.mc_id=aiml-43548-heboelma)

## Test quality of your model's translation

1. Select **Test model** from the left menu.

1. Select model **Name** then select **View test results**.

   :::image type="content" source="../media/fine-tune-test-model-1.png" alt-text="Screenshot illustrating test-model function.":::

1. Human evaluate translation from your custom translation model **New model** and the **Baseline model** (our pretrained baseline used for customization) against **Reference** (target translation from the test set).

   :::image type="content" source="../media/fine-tune-test-model-2.png" alt-text="Screenshot illustrating the test-model function.":::

1. If results are satisfactory, deploy the model, otherwise, iterate by adding more human curated training data until you find a winner model.

## Next steps

> [!div class="nextstepaction"]
> [Learn how to deploy model](deploy-model.md)
