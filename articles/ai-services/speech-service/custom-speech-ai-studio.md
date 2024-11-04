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

Custom speech projects contain models, training and testing datasets, and deployment endpoints. Each project is specific to a [locale](language-support.md?tabs=stt). For example, you might create a project for English in the United States.

## Create a project in AI Studio

To create a custom speech project, follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customspeech).
1. Select the subscription and Speech resource to work with. 

    > [!IMPORTANT]
    > If you will train a custom model with audio data, choose a Speech resource region with dedicated hardware for training audio data. See footnotes in the [regions](regions.md#speech-service) table for more information.

1. Select **Custom speech** > **Create a new project**. 
1. Follow the instructions provided by the wizard to create your project. 

Select the new project by name or select **Go to project**. You'll see these menu items in the left panel: **Speech datasets**, **Train custom models**, **Test models**, and **Deploy models**. 


## Related content
 
