---
title: Hear and speak with chat models in the Azure AI Foundry portal chat playground
titleSuffix: Azure AI Foundry
description: Hear and speak with chat models in the Azure AI Foundry portal chat playground.
manager: nitinme
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: quickstart
ms.date: 2/12/2025
ms.reviewer: eur
ms.author: eur
author: eric-urban
---

# Quickstart: Hear and speak with chat models in the Azure AI Foundry portal chat playground

In the chat playground in Azure AI Foundry portal, you can use speech to text and text to speech features to interact with chat models. You can try the same model that you use for text-based chat in a speech-based chat. It's just another way to interact with the model.

In this quickstart, you use Azure OpenAI Service and Azure AI Speech to:

- Speak to the assistant via speech to text.
- Hear the assistant's response via text to speech.

The speech to text and text to speech features can be used together or separately in the Azure AI Foundry portal chat playground. You can use the playground to test your chat model before deploying it. 

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- An [Azure AI Foundry project](../how-to/create-projects.md).
- A deployed [Azure OpenAI](../how-to/deploy-models-openai.md) chat model. This guide is tested with a `gpt-4o-mini` model.

> [!NOTE]
> You must use a **[!INCLUDE [hub](../includes/hub-project-name.md)]** for the features mentioned in this article. A **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** is not supported. For more information, see [Project types](../what-is-azure-ai-foundry.md#project-types).

## Configure the chat playground

Before you can start a chat session, you need to configure the chat playground to use the speech to text and text to speech features.

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com).
1. Go to your Azure AI Foundry project. If you need to create a project, see [Create an Azure AI Foundry project](../how-to/create-projects.md).
1. Select **Playgrounds** from the left pane and then select a playground to use. In this example, select **Try the chat playground**.
1. Select your deployed chat model from the **Deployment** dropdown. 

    :::image type="content" source="../media/quickstarts/hear-speak/playground-config-deployment.png" alt-text="Screenshot of the chat playground with mode and deployment highlighted." lightbox="../media/quickstarts/hear-speak/playground-config-deployment.png":::

1. Select the **Chat capabilities** button with the gear icon. 

    :::image type="content" source="../media/quickstarts/hear-speak/playground-settings-select.png" alt-text="Screenshot of the chat playground with options to get to the chat capabilities settings." lightbox="../media/quickstarts/hear-speak/playground-settings-select.png":::

    > [!NOTE]
    > You should also see the options to select the microphone or speaker buttons. If you select either of these buttons, but didn't yet enable speech to text or text to speech, you're prompted to enable them in **Chat capabilities**. 

1. On the **Chat capabilities** page, select the box to acknowledge that usage of the speech feature incurs extra costs. For more information, see [Azure AI Speech pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

1. Select **Enable speech to text** and **Enable text to speech**.  

    :::image type="content" source="../media/quickstarts/hear-speak/playground-settings-enable-speech.png" alt-text="Screenshot of the chat capabilities page." lightbox="../media/quickstarts/hear-speak/playground-settings-enable-speech.png":::

1. Select the language locale and voice you want to use for speaking and hearing. The list of available voices depends on the locale that you select.

1. Optionally, you can try the voice before you return to the chat session. Enter some sample text and select **Play** to 

1. Select **Save**.
 

## Start a chat session

In this chat session, you use both speech to text and text to speech. You use the speech to text feature to speak to the assistant, and the text to speech feature to hear the assistant's response. 

1. Complete the steps in the [Configure the playground](#configure-the-chat-playground) section. To complete this quickstart, you need to enable the speech to text and text to speech features.
1. Select the microphone button and speak to the assistant. For example, you can say "Do you know where I can get an Xbox".

    :::image type="content" source="../media/quickstarts/hear-speak/chat-session-speaking.png" alt-text="Screenshot of the chat session with the enabled microphone icon and send button highlighted." lightbox="../media/quickstarts/hear-speak/chat-session-speaking.png":::


1. Select the send button (right arrow) to send your message to the assistant. The assistant's response is displayed in the chat session pane.

    > [!NOTE]
    > If the speaker button is turned on, you hear the assistant's response. If the speaker button is turned off, you don't hear the assistant's response, but the response is still displayed in the chat session pane.

1. You can change the system prompt to change the assistant's response format or style. 

    For example, enter:

    ```
    "You're an AI assistant that helps people find information. Answers shouldn't be longer than 20 words because you are on a phone. You could use 'um' or 'let me see' to make it more natural and add some disfluency."
    ```

    Say again: "Do you know where I can get an Xbox". The response is shown in the chat session pane. Since the speaker button is turned on, you also hear the response.

    :::image type="content" source="../media/quickstarts/hear-speak/chat-session-hear-response-natural.png" alt-text="Screenshot of the chat session with the system prompt edited." lightbox="../media/quickstarts/hear-speak/chat-session-hear-response-natural.png":::

## Clean up resources

To avoid incurring unnecessary Azure costs, you should delete the resources you created in this quickstart if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

## Next steps

- [Create a project in Azure AI Foundry portal](../how-to/create-projects.md)
- [Deploy an enterprise chat web app](../tutorials/deploy-chat-web-app.md)
- [Learn more about Azure AI Speech](../../ai-services/speech-service/overview.md)
