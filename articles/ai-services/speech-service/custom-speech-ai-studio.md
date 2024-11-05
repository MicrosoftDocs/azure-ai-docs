---
title: Customize a speech model with fine-tuning in AI Studio
titleSuffix: Azure AI services
description: Learn about how to customize a speech model with fine-tuning in AI Studio.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 9/19/2024
ms.author: eur
zone_pivot_groups: speech-studio-cli-rest
#Customer intent: As a developer, I want to learn how to customize a speech model with fine-tuning in AI Studio so that I can deploy a custom model.
---

# Customize a speech model with fine-tuning in AI Studio

With custom speech, you can enhance speech recognition accuracy for your applications by using a custom model for real-time speech to text, speech translation, and batch transcription. The base model, trained with Microsoft-owned data, handles common spoken language well, but a custom model can improve domain-specific vocabulary and audio conditions by providing text and audio data for training. Additionally, you can train the model with structured text for custom pronunciations, display text formatting, and profanity filtering.

> [!TIP]
> You can bring your custom speech projects and trained models from Speech Studio to AI Studio. In AI Studio, you can pick up where you left off by connecting to your existing Speech resource. For more information about connecting to an existing Speech resource, see [Connect to an existing Speech resource](../../ai-studio/ai-services/connect-ai-services.md#connect-azure-ai-services-after-you-create-a-project).


## Create a project in AI Studio

Custom speech projects contain models, training and testing datasets, and deployment endpoints. Each project is specific to a [locale](language-support.md?tabs=stt). For example, you might create a project for English in the United States.

To create a custom speech project, follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select the subscription and Speech resource to work with. 

    > [!IMPORTANT]
    > If you will train a custom model with audio data, choose a Speech resource region with dedicated hardware for training audio data. See footnotes in the [regions](regions.md#speech-service) table for more information.

1. Select **Custom speech** > **Create a new project**. 
1. Follow the instructions provided by the wizard to create your project. 

Select the new project by name or select **Go to project**. You'll see these menu items in the left panel: **Speech datasets**, **Train custom models**, **Test models**, and **Deploy models**. 


## Related content

- [Custom speech overview](./custom-speech-overview.md)
