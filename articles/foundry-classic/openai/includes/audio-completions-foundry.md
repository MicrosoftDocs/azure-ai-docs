---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 1/7/2025
---

[!INCLUDE [Audio completions introduction](audio-completions-intro.md)]

## Deploy a model for audio generation

[!INCLUDE [Deploy model](audio-completions-deploy-model.md)]

## Use GPT-4o audio generation

To chat with your deployed `gpt-4o-mini-audio-preview` model in the **Chat** playground of [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs), follow these steps:

1. Go to the [Foundry portal](https://ai.azure.com/?cid=learnDocs) and select your project that has your deployed `gpt-4o-mini-audio-preview` model.
1. Go to your project in [Foundry](https://ai.azure.com/?cid=learnDocs). 
1. Select **Playgrounds** from the left pane.
1. Select **Audio playground** > **Try the Chat playground**. 

    > [!NOTE]
    > The **Audio playground** doesn't support the `gpt-4o-mini-audio-preview` model. Use the **Chat playground** as described in this section.

1. Select your deployed `gpt-4o-mini-audio-preview` model from the **Deployment** dropdown. 
1. Start chatting with the model and listen to the audio responses.

    :::image type="content" source="../media/quickstarts/audio-completions-chat-playground.png" alt-text="Screenshot of the Chat playground page." lightbox="../media/quickstarts/audio-completions-chat-playground.png":::

    You can:
    - Record audio prompts.
    - Attach audio files to the chat.
    - Enter text prompts.
