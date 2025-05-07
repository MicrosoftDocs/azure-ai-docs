---
title: Customize speech models with fine-tuning
titleSuffix: Azure AI services
description: Learn about how to customize speech models with fine-tuning. 
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 2/25/2025
ms.author: eur
zone_pivot_groups: foundry-speech-studio
#Customer intent: As a developer, I want to learn how to customize speech models with fine-tuning so that I can train and deploy a custom model.
---

# Customize speech models with fine-tuning

With custom speech, you can enhance speech recognition accuracy for your applications by using a custom model for real-time speech to text, speech translation, and batch transcription. 

You create a custom speech model by fine-tuning an Azure AI Speech base model with your own data. You can upload your data, test and train a custom model, compare accuracy between models, and deploy a model to a custom endpoint.

This article shows you how to use fine-tuning to create a custom speech model. For more information about custom speech, see the [custom speech overview](./custom-speech-overview.md) documentation.

> [!TIP]
> You can bring your custom speech models from [Speech Studio](https://speech.microsoft.com) to the [Azure AI Foundry portal](https://ai.azure.com). In Azure AI Foundry, you can pick up where you left off by connecting to your existing Speech resource. For more information about connecting to an existing Speech resource, see [Connect to an existing Speech resource](../../ai-services/connect-services-ai-foundry-portal.md#connect-azure-ai-services-after-you-create-a-project).

## Start fine-tuning

Custom speech fine-tuning includes models, training and testing datasets, and deployment endpoints. Each project is specific to a [locale](language-support.md?tabs=stt). For example, you might fine-tune for English in the United States.

::: zone pivot="ai-foundry-portal"

In the [Azure AI Foundry portal](https://ai.azure.com), you can fine-tune some Azure AI services models. For example, you can fine-tune a model for custom speech. Each custom model is specific to a [locale](language-support.md?tabs=stt). For example, you might fine-tune a model for English in the United States.

1. Go to your project in the [Azure AI Foundry portal](https://ai.azure.com). If you need to create a project, see [Create an Azure AI Foundry project](../../ai-foundry/how-to/create-projects.md).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning** > **+ Fine-tune**.

    :::image type="content" source="./media/ai-foundry/custom-speech/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to select fine-tuning of Azure AI Services models." lightbox="./media/ai-foundry/custom-speech/fine-tune-azure-ai-services.png":::
 
1. In the wizard, select **Speech to text (speech recognition)** for custom speech. Then select **Next**.

1. Enter the language, name, and description for the fine-tuning job. Then select **Create**.

## Continue fine-tuning

Go to the Azure AI Speech documentation to learn how to continue fine-tuning your custom speech model:
* [Upload training and testing datasets](./how-to-custom-speech-upload-data.md)
* [Train a model](how-to-custom-speech-train-model.md)
* [Test model quantitatively](how-to-custom-speech-evaluate-data.md) and [test model qualitatively](./how-to-custom-speech-inspect-data.md)
* [Deploy a model](how-to-custom-speech-deploy-model.md)

::: zone-end

::: zone pivot="speech-studio"

To create a custom speech project in [Speech Studio](https://aka.ms/speechstudio/customspeech), follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select the subscription and Speech resource to work with. 

    > [!IMPORTANT]
    > If you train a custom model with audio data, select a service resource in a region with dedicated hardware for training audio data. See footnotes in the [regions](regions.md#regions) table for more information.

1. Select **Custom speech** > **Create a new project**. 
1. Follow the instructions provided by the wizard to create your project. 

Select the new project by name or select **Go to project**. Then you should see these menu items in the left panel: **Speech datasets**, **Train custom models**, **Test models**, and **Deploy models**. 

::: zone-end

## Related content

* [Training and testing datasets](./how-to-custom-speech-test-and-train.md)
* [Train a model](how-to-custom-speech-train-model.md)
* [Test model quantitatively](how-to-custom-speech-evaluate-data.md)
