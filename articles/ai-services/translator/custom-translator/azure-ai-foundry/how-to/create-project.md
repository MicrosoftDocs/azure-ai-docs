---
title: Create a project - Custom translation
titleSuffix: Azure AI services
description: How to create and manage a project
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 05/19/2025
ms.author: lajanuar
ms.topic: how-to

---

# Start fine-tuning 

 Custom translation fine-tuning includes one or many language pairs, model training, tuning and testing datasets, and deployment endpoint.

## Create a project

In the [Azure AI Foundry portal](https://ai.azure.com/), you can fine-tune some Azure AI services models, e.g., Custom translation, Custom speech, etc. For Custom translation, you can fine-tune a model for a language pair, *say* English to French.

1. Go to your project in the [Azure AI Foundry portal](https://ai.azure.com/) portal. If you need to create a project, *see* [Create an Azure AI Foundry project](https://learn.microsoft.com/azure/ai-foundry/how-to/create-projects).

1. Select **Fine-tuning** from the left pane.

1. Select **AI Service Fine-tuning** > **+ Fine-tune**.

:::image type="content" source="../media/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to select fine-tuning of Azure AI Services models.":::

1. In the dialog, select **Translation** for custom translation. Then select **Next**.

:::image type="content" source="../media/fine-tune-select-translate.png" alt-text="Screenshot of the page to select Translate for custom translation models.":::

> [!NOTE]
> An Azure AI Service resouce is connected to your project.


## Next steps

> [!div class="nextstepaction"]
> [Learn how to create a language pair](how-to-custom-translation-create-language-pair.md)
