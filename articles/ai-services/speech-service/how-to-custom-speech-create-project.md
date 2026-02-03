---
title: Customize speech models with fine-tuning
titleSuffix: Foundry Tools
description: Learn about how to customize speech models with fine-tuning. 
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 11/18/2025
ms.author: pafarley
zone_pivot_groups: foundry-speech-studio
#Customer intent: As a developer, I want to learn how to customize speech models with fine-tuning so that I can train and deploy a custom model.
---

# Customize speech models with fine-tuning

With custom speech, you can enhance speech recognition accuracy for your applications by using a custom model for real-time speech to text, speech translation, and batch transcription. 

> [!TIP]
> Bring your custom speech models from [Speech Studio](https://speech.microsoft.com) to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). In Microsoft Foundry portal, you can pick up where you left off by connecting to your existing Speech resource. For more information about connecting to an existing Speech resource, see [Connect to an existing Speech resource](../../ai-studio/ai-services/how-to/connect-ai-services.md).

You create a custom speech model by fine-tuning an Azure Speech in Foundry Tools base model with your own data. You can upload your data, test and train a custom model, compare accuracy between models, and deploy a model to a custom endpoint.

This article shows you how to use fine-tuning to create a custom speech model. For more information about custom speech, see the [custom speech overview](./custom-speech-overview.md) documentation.

> [!TIP]
> You can bring your custom speech models from [Speech Studio](https://speech.microsoft.com) to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). In Microsoft Foundry, you can pick up where you left off by connecting to your existing Speech resource. For more information about connecting to an existing Speech resource, see [Connect to an existing Speech resource](../../ai-services/connect-services-foundry-portal.md).

## Start fine-tuning

Custom speech fine-tuning includes models, training and testing datasets, and deployment endpoints. Each project is specific to a [locale](language-support.md?tabs=stt). For example, you might fine-tune for English in the United States.

::: zone pivot="ai-foundry-portal"

In the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs), you can fine-tune some Foundry Tools models. For example, you can fine-tune a model for custom speech. Each custom model is specific to a [locale](language-support.md?tabs=stt). For example, you might fine-tune a model for English in the United States.

1. Go to your project in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). If you need to create a project, see [Create a Microsoft Foundry project](../../ai-foundry/how-to/create-projects.md).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning** > **+ Fine-tune**.

    :::image type="content" source="./media/custom-speech/ai-foundry/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to select fine-tuning of Foundry Tools models." lightbox="./media/custom-speech/ai-foundry/fine-tune-azure-ai-services.png":::
 
1. In the wizard, select **Custom Speech (speech to text fine-tuning)** for custom speech. Then select **Next**.

1. Enter the language, name, and description for the fine-tuning job. Then select **Create**.

## Continue fine-tuning

Go to the Azure Speech documentation to learn how to continue fine-tuning your custom speech model:
* [Upload training and testing datasets](./how-to-custom-speech-upload-data.md)
* [Train a model](how-to-custom-speech-train-model.md)
* [Test model quantitatively](how-to-custom-speech-evaluate-data.md) and [test model qualitatively](./how-to-custom-speech-inspect-data.md)
* [Deploy a model](how-to-custom-speech-deploy-model.md)

## View fine-tuned models

After fine-tuning, you can access your custom speech models and deployments from the **Fine-tuning** page. 

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning**.

    :::image type="content" source="./media/custom-speech/ai-foundry/fine-tune-succeeded-list.png" alt-text="Screenshot of the page where you can view fine-tuned Foundry Tools models." lightbox="./media/custom-speech/ai-foundry/fine-tune-succeeded-list.png":::

::: zone-end

::: zone pivot="speech-studio"

After you create a custom speech project, you can access your custom speech models and deployments from the **Custom speech** page.

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select the subscription and Speech resource to work with. 

    > [!IMPORTANT]
    > If you train a custom model with audio data, select a service resource in a region with dedicated hardware for training audio data. See footnotes in the [regions](regions.md#regions) table for more information.

1. Select **Custom speech** > **Create a new project**. 
1. Follow the instructions provided by the wizard to create your project. 

Select the new project by name or select **Go to project**. Then you should see these menu items in the left panel: **Speech datasets**, **Train custom models**, **Test models**, and **Deploy models**. 

::: zone-end


## Get the project ID for the REST API

::: zone pivot="ai-foundry-portal"

When you use the speech to text REST API for custom speech, you need to set the `project` property to the ID of your custom speech project. You need to set the `project` property so that you can manage fine-tuning in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). 

> [!IMPORTANT]
> The project ID for custom speech isn't the same as the ID of the Microsoft Foundry project.

You can find the project ID in the URL after you select or start fine-tuning a custom speech model. 

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning**.
1. Select the custom model that you want to check from the **Model name** column.
1. Inspect the URL in your browser. The project ID is part of the URL. For example, the project ID is `00001111-aaaa-2222-bbbb-3333cccc4444` in the following URL: 

    ```https
    https://ai.azure.com/build/models/aiservices/speech/customspeech/00001111-aaaa-2222-bbbb-3333cccc4444/<REDACTED_FOR_BREVITY>
    ```

::: zone-end

::: zone pivot="speech-studio"

When you use the speech to text REST API for custom speech, you need to set the `project` property to the ID of your custom speech project. You need to set the `project` property so that you can manage fine-tuning in the [Speech Studio](https://aka.ms/speechstudio/customspeech). 

To get the project ID for a custom speech project in [Speech Studio](https://aka.ms/speechstudio/customspeech):

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech) and select the **Custom speech** tile.
1. Select your custom speech project. 
1. Inspect the URL in your browser. The project ID is part of the URL. For example, the project ID is `00001111-aaaa-2222-bbbb-3333cccc4444` in the following URL:

    ```https
    https://speech.microsoft.com/portal/<Your-Resource-ID>/customspeech/a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1
    ```

::: zone-end

## Related content

* [Training and testing datasets](./how-to-custom-speech-test-and-train.md)
* [Train a model](how-to-custom-speech-train-model.md)
* [Test model quantitatively](how-to-custom-speech-evaluate-data.md)
