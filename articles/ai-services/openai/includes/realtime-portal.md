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

1. Go to the [Azure OpenAI in Azure AI Foundry Models page](https://ai.azure.com/resource/overview) in Azure AI Foundry portal. Make sure you're signed in with the Azure subscription that has your Azure OpenAI in Azure AI Foundry Models resource and the deployed `gpt-4o-mini-realtime-preview` model.
1. Select the **Real-time audio** playground from under **Playgrounds** in the left pane.
1. Select your deployed `gpt-4o-mini-realtime-preview` model from the **Deployment** dropdown. 
1. Select **Enable microphone** to allow the browser to access your microphone. If you already granted permission, you can skip this step.

    :::image type="content" source="../media/how-to/real-time/real-time-playground.png" alt-text="Screenshot of the real-time audio playground with the deployed model selected." lightbox="../media/how-to/real-time/real-time-playground.png":::

1. Optionally, you can edit contents in the **Give the model instructions and context** text box. Give the model instructions about how it should behave and any context it should reference when generating a response. You can describe the assistant's personality, tell it what it should and shouldn't answer, and tell it how to format responses.
1. Optionally, change settings such as threshold, prefix padding, and silence duration.
1. Select **Start listening** to start the session. You can speak into the microphone to start a chat.

    :::image type="content" source="../media/how-to/real-time/real-time-playground-start-listening.png" alt-text="Screenshot of the real-time audio playground with the start listening button and microphone access enabled." lightbox="../media/how-to/real-time/real-time-playground-start-listening.png":::

1. You can interrupt the chat at any time by speaking. You can end the chat by selecting the **Stop listening** button.
