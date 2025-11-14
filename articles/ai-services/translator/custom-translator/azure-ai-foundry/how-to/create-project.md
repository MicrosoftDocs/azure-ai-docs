---
title: Create a Foundry Tools fine-tuning project - custom translation
titleSuffix: Foundry Tools
description: How to create and manage a fine-tuning project
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 11/18/2025
ms.author: lajanuar
ms.topic: how-to

---

# Create a Foundry Tools fine-tuning project

Custom translation fine-tuning includes one or many language pairs, model training, tuning and testing datasets, and deployment endpoint. In the [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs), you can fine-tune some Foundry Tools models, for example, custom translation, Custom speech, etc. For custom translation, you can fine-tune a model for a language pair, *say* English to French.

1. Go to your project in the [Foundry](https://ai.azure.com/?cid=learnDocs) portal. If you need to create a project, *see* [Create a Foundry project](../../azure-ai-foundry/how-to/create-project.md).

1. Select **Fine-tuning** from the left pane.

1. Select **AI Service Fine-tuning** > **+ Fine-tune**.

:::image type="content" source="../media/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to select fine-tuning of Foundry Tools models.":::

1. In the dialog, select **Translation** for custom translation. Then select **Next**.

:::image type="content" source="../media/fine-tune-select-translate.png" alt-text="Screenshot of the page to select Translate for custom translation models.":::

> [!NOTE]
> A Foundry Tool resource is connected to your project.

## Next steps

> [!div class="nextstepaction"]
> [Learn how to create a language pair](create-language-pair.md)
