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

With custom speech, you can enhance speech recognition accuracy for your applications by using a custom model for real-time speech to text, speech translation, and batch transcription. The base model, trained with Microsoft-owned data, handles common spoken language well, but a custom model can improve domain-specific vocabulary and audio conditions by providing text and audio data for training. Additionally, you can train the model with structured text for custom pronunciations, display text formatting, and profanity filtering.

> [!TIP]
> You can bring your custom speech models from [Speech Studio](https://speech.microsoft.com) to the [Azure AI Foundry portal](https://ai.azure.com). In Azure AI Foundry, you can pick up where you left off by connecting to your existing Speech resource. For more information about connecting to an existing Speech resource, see [Connect to an existing Speech resource](../../ai-studio/ai-services/how-to/connect-ai-services.md#connect-azure-ai-services-after-you-create-a-project).

## Start fine-tuning

Custom speech fine-tuning includes models, training and testing datasets, and deployment endpoints. Each project is specific to a [locale](language-support.md?tabs=stt). For example, you might fine-tune for English in the United States.

::: zone pivot="ai-foundry-portal"

In [Azure AI Foundry portal](https://ai.azure.com), you create a custom speech model by fine-tuning an Azure AI Speech base model with your own data. You can upload your data, test and train a custom model, compare accuracy between models, and deploy a model to a custom endpoint.

This article shows you how to use fine-tuning in Azure AI Foundry portal to create a custom speech model. For more information about custom speech, see the [custom speech overview](./custom-speech-overview.md) documentation.


## Start fine-tuning a model with your data

In Azure AI Foundry, you can fine-tune some Azure AI services models. For example, you can fine-tune a model for custom speech. Each custom model is specific to a [locale](language-support.md?tabs=stt). For example, you might fine-tune a model for English in the United States.

1. Go to your Azure AI Foundry project. If you need to create a project, see [Create an Azure AI Foundry project](../../ai-studio/how-to/create-projects.md).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning** > **+ Fine-tune**.

    :::image type="content" source="../../ai-studio/media/ai-services/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to select fine-tuning of Azure AI Services models." lightbox="../../ai-studio/media/ai-services/fine-tune-azure-ai-services.png":::
 
1. In the wizard, select **Speech to text (speech recognition)** for custom speech. Then select **Next**.
1. Select the connected service resource that you want to use for fine-tuning. Then select **Next**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-select-connection.png" alt-text="Screenshot of the page to select the connected service resource that you want to use for fine-tuning." lightbox="./media/ai-studio/custom-speech/new-fine-tune-select-connection.png":::

    In this example, we can choose from the following options:
    - **AI Service**: The Azure AI Services multi-service resource that [came with the Azure AI Foundry project](../../ai-studio/ai-services/how-to/connect-ai-services.md#connect-azure-ai-services-when-you-create-a-project-for-the-first-time).
    - **Speech Service**: An Azure AI Speech resource that was [connected after the project was created](../../ai-studio/ai-services/how-to/connect-ai-services.md#connect-azure-ai-services-after-you-create-a-project). 

1. Enter a name and description for the fine-tuning job. Then select **Next**.
1. From the new left menu in the fine-tuning page, select **Manage data** and then select **Add data**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-add-data.png" alt-text="Screenshot of the page with an option to add data to the custom speech project." lightbox="./media/ai-studio/custom-speech/new-fine-tune-add-data.png":::

1. In the **Add data** wizard, select the type of training data you want to add. In this example, we select **Audio + human-labeled transcript**. Then select **Next**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-add-data-select-type.png" alt-text="Screenshot of the page with an option to select the type of training data you want to add." lightbox="./media/ai-studio/custom-speech/new-fine-tune-add-data-select-type.png":::

1. On the **Upload your data** page, select local files, Azure Blob Storage, or other shared web locations. Then select **Next**.
1. Enter a name and description for the data. Then select **Next**.
1. Review the data and select **Upload**. You're taken back to the **Manage data** page. The status of the data is **Processing**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-add-data-status-processing.png" alt-text="Screenshot of the page that shows the status of the data as processing." lightbox="./media/ai-studio/custom-speech/new-fine-tune-add-data-status-processing.png":::

## Train a custom model from your data

1. After the data is processed, select **Train model** from the left menu. Then select **+ Train model**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-train-model.png" alt-text="Screenshot of the page with an option to start training for a custom speech model." lightbox="./media/ai-studio/custom-speech/new-fine-tune-train-model.png":::

1. In the **Train a new model** wizard, select the base model that you want to fine-tune. Then select **Next**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-train-model-select-base.png" alt-text="Screenshot of the page with an option to select the base model that you want to fine-tune." lightbox="./media/ai-studio/custom-speech/new-fine-tune-train-model-select-base.png":::

1. Select the data that you want to use for training. Then select **Next**.
1. Enter a name and description for the model. Then select **Next**.
1. Review the settings and select **Train a new model**. You're taken back to the **Train model** page. The status of the data is **Processing**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-train-model-status-processing.png" alt-text="Screenshot of the page that shows the status of the training as processing." lightbox="./media/ai-studio/custom-speech/new-fine-tune-train-model-status-processing.png":::

## Test the custom model

1. After the model is trained, select **Test models** from the left menu. Then select **+ Create test**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-test-model.png" alt-text="Screenshot of the page with an option to test your custom speech model." lightbox="./media/ai-studio/custom-speech/new-fine-tune-test-model.png":::

1. In the **Create a new test** wizard, select the test type. In this example, we select **Evaluate accuracy (Audio + transcript data)**. Then select **Next**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-test-model-select-type.png" alt-text="Screenshot of the page with an option to select the test type." lightbox="./media/ai-studio/custom-speech/new-fine-tune-test-model-select-type.png":::

1. Select the data that you want to use for testing. Then select **Next**.
1. Select up to two models to evaluate and compare accuracy. In this example, we select the model that we trained and the base model. Then select **Next**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-test-model-select-models.png" alt-text="Screenshot of the page with an option to select up to two models to evaluate and compare accuracy." lightbox="./media/ai-studio/custom-speech/new-fine-tune-test-model-select-models.png":::

1. Enter a name and description for the test. Then select **Next**.
1. Review the settings and select **Create test**. You're taken back to the **Test models** page. The status of the data is **Processing**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-test-model-status-processing.png" alt-text="Screenshot of the page that shows the status of the test as processing." lightbox="./media/ai-studio/custom-speech/new-fine-tune-test-model-status-processing.png":::

1. When the test status is **Succeeded**, you can view the results. Select the test to view the results.


## Deploy the custom model

1. After you're satisfied with the test results, select **Deploy models** from the left menu. Then select **+ Deploy model**.

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-deploy-model.png" alt-text="Screenshot of the page with an option to deploy the custom speech model." lightbox="./media/ai-studio/custom-speech/new-fine-tune-deploy-model.png":::

1. In the **Deploy a new model** wizard, select the model that you want to deploy. 

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-deploy-model-select-and-deploy.png" alt-text="Screenshot of the page with an option to select the model that you want to deploy." lightbox="./media/ai-studio/custom-speech/new-fine-tune-deploy-model-select-and-deploy.png":::

1. Enter a name and description for the deployment. Select the box to agree to the terms of use. Then select **Deploy**.

1. After the deployment status is **Succeeded**, you can view the deployment details. Select the deployment to view the details like the endpoint ID. 

    :::image type="content" source="./media/ai-studio/custom-speech/new-fine-tune-deploy-model-status-succeeded.png" alt-text="Screenshot of the page with an option to select the deployment to view the details like the endpoint ID." lightbox="./media/ai-studio/custom-speech/new-fine-tune-deploy-model-status-succeeded.png":::

## View fine-tuned models

You can access your custom speech models and deployments from the **Fine-tuning** page. 

1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning**.

    :::image type="content" source="./media/ai-studio/custom-speech/fine-tune-succeeded-list.png" alt-text="Screenshot of the page where you can view fine-tuned AI services models." lightbox="./media/ai-studio/custom-speech/fine-tune-succeeded-list.png":::

::: zone-end

::: zone pivot="speech-studio"

To create a custom speech project, follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select the subscription and Speech resource to work with. 

    > [!IMPORTANT]
    > If you will train a custom model with audio data, choose a region with dedicated hardware for training audio data. See footnotes in the [regions](regions.md#regions) table for more information.

1. Select **Custom speech** > **Create a new project**. 
1. Follow the instructions provided by the wizard to create your project. 

Select the new project by name or select **Go to project**. You'll see these menu items in the left panel: **Speech datasets**, **Train custom models**, **Test models**, and **Deploy models**. 

::: zone-end


## Choose your model

There are a few approaches to using custom speech models:
- The base model provides accurate speech recognition out of the box for a range of [scenarios](overview.md#speech-scenarios). Base models are updated periodically to improve accuracy and quality. We recommend that if you use base models, use the latest default base models. If a required customization capability is only available with an older model, then you can choose an older base model. 
- A custom model augments the base model to include domain-specific vocabulary shared across all areas of the custom domain.
- Multiple custom models can be used when the custom domain has multiple areas, each with a specific vocabulary.

One recommended way to see if the base model suffices is to analyze the transcription produced from the base model and compare it with a human-generated transcript for the same audio. You can compare the transcripts and obtain a [word error rate (WER)](how-to-custom-speech-evaluate-data.md#evaluate-word-error-rate-wer) score. If the WER score is high, training a custom model to recognize the incorrectly identified words is recommended.

Multiple models are recommended if the vocabulary varies across the domain areas. For instance, Olympic commentators report on various events, each associated with its own vernacular. Because each Olympic event vocabulary differs significantly from others, building a custom model specific to an event increases accuracy by limiting the utterance data relative to that particular event. As a result, the model doesn't need to sift through unrelated data to make a match. Regardless, training still requires a decent variety of training data. Include audio from various commentators who have different accents, gender, age, etcetera. 

## Model stability and lifecycle

A base model or custom model deployed to an endpoint using custom speech is fixed until you decide to update it. The speech recognition accuracy and quality remain consistent, even when a new base model is released. This allows you to lock in the behavior of a specific model until you decide to use a newer model.

Whether you train your own model or use a snapshot of a base model, you can use the model for a limited time. For more information, see [Model and endpoint lifecycle](./how-to-custom-speech-model-and-endpoint-lifecycle.md).

## Next steps

* [Training and testing datasets](./how-to-custom-speech-test-and-train.md)
* [Test model quantitatively](how-to-custom-speech-evaluate-data.md)
* [Train a model](how-to-custom-speech-train-model.md)
