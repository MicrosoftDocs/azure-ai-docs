---
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-openai
ms.topic: include
ms.date: 3/20/2025
---

## Deploy a model for real-time audio

[!INCLUDE [Deploy model](realtime-deploy-model.md)]

## Use the GPT-4o real-time audio

To chat with your deployed `gpt-4o-mini-realtime-preview` model in the [Azure AI Foundry](https://ai.azure.com) **Real-time audio** playground, follow these steps:

1. Go to the [Azure AI Foundry portal](https://ai.azure.com) and select your project that has your deployed `gpt-4o-mini-realtime-preview` model.
1. Select **Playgrounds** from the left pane.
1. Select **Audio playground** > **Try the Audio playground**. 

    > [!NOTE]
    > The **Chat playground** doesn't support the `gpt-4o-mini-realtime-preview` model. Use the **Audio playground** as described in this section.

1. Select your deployed `gpt-4o-mini-realtime-preview` model from the **Deployment** dropdown.

    :::image type="content" source="../media/how-to/real-time/real-time-playground.png" alt-text="Screenshot of the audio playground with the deployed model selected." lightbox="../media/how-to/real-time/real-time-playground.png":::

1. Optionally, you can edit contents in the **Give the model instructions and context** text box. Give the model instructions about how it should behave and any context it should reference when generating a response. You can describe the assistant's personality, tell it what it should and shouldn't answer, and tell it how to format responses.
1. Optionally, change settings such as threshold, prefix padding, and silence duration.
1. Select **Start listening** to start the session. You can speak into the microphone to start a chat.
1. You can interrupt the chat at any time by speaking. You can end the chat by selecting the **Stop listening** button.
