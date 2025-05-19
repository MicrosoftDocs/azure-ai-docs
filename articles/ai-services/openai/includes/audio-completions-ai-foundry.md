---
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-openai
ms.topic: include
ms.date: 1/7/2025
---

[!INCLUDE [Audio completions introduction](audio-completions-intro.md)]

## Deploy a model for audio generation

[!INCLUDE [Deploy model](audio-completions-deploy-model.md)]

## Use GPT-4o audio generation

To chat with your deployed `gpt-4o-mini-audio-preview` model in the **Chat** playground of [Azure AI Foundry portal](https://ai.azure.com), follow these steps:

1. Go to the [Azure OpenAI in Azure AI Foundry Models page](https://ai.azure.com/resource/overview) in Azure AI Foundry portal. Make sure you're signed in with the Azure subscription that has your Azure OpenAI in Azure AI Foundry Models resource and the deployed `gpt-4o-mini-audio-preview` model.
1. Select the **Chat** playground from under **Resource playground** in the left pane.
1. Select your deployed `gpt-4o-mini-audio-preview` model from the **Deployment** dropdown. 
1. Start chatting with the model and listen to the audio responses.

    :::image type="content" source="../media/quickstarts/audio-completions-chat-playground.png" alt-text="Screenshot of the Chat playground page." lightbox="../media/quickstarts/audio-completions-chat-playground.png":::

    You can:
    - Record audio prompts.
    - Attach audio files to the chat.
    - Enter text prompts.
