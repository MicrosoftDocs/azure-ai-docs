---
title: 'How to use GPT-4o Realtime API for speech and audio with Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Learn how to use GPT-4o Realtime API for speech and audio with Azure OpenAI Service.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 10/3/2024
author: eric-urban
ms.author: eur
ms.custom: references_regions
zone_pivot_groups: openai-studio-js
recommendations: false
---

# GPT-4o Realtime API for speech and audio (Preview)

Azure OpenAI GPT-4o Realtime API for speech and audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. The GPT-4o audio `realtime` API is designed to handle real-time, low-latency conversational interactions, making it a great fit for use cases involving live interactions between a user and a model, such as customer support agents, voice assistants, and real-time translators.

Most users of the Realtime API need to deliver and receive audio from an end-user in real time, including applications that use WebRTC or a telephony system. The Realtime API isn't designed to connect directly to end user devices and relies on client integrations to terminate end user audio streams. 

## Supported models

Currently only `gpt-4o-realtime-preview` version: `2024-10-01-preview` supports real-time audio.

The `gpt-4o-realtime-preview` model is available for global deployments in [East US 2 and Sweden Central regions](./concepts/models.md#global-standard-model-availability).

> [!IMPORTANT]
> The system stores your prompts and completions as described in the "Data Use and Access for Abuse Monitoring" section of the service-specific Product Terms for Azure OpenAI Service, except that the Limited Exception does not apply. Abuse monitoring will be turned on for use of the `gpt-4o-realtime-preview` API even for customers who otherwise are approved for modified abuse monitoring.

## API support

Support for the Realtime API was first added in API version `2024-10-01-preview`. 

> [!NOTE]
> For more information about the API and architecture, see the [Azure OpenAI GPT-4o real-time audio repository on GitHub](https://github.com/azure-samples/aoai-realtime-audio-sdk).

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- An Azure OpenAI resource created in a [supported region](#supported-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](./how-to/create-resource.md).

## Deploy a model for real-time audio

Before you can use GPT-4o real-time audio, you need a deployment of the `gpt-4o-realtime-preview` model in a supported region as described in the [supported models](#supported-models) section.

1. Go to the [AI Studio home page](https://ai.azure.com) and make sure you're signed in with the Azure subscription that has your Azure OpenAI Service resource (with or without model deployments.)
1. Select the **Real-time audio** playground from under **Resource playground** in the left pane.
1. Select **+ Create a deployment** to open the deployment window. 
1. Search for and select the `gpt-4o-realtime-preview` model and then select **Confirm**.
1. In the deployment wizard, make sure to select the `2024-10-01` model version.
1. Follow the wizard to deploy the model.

Now that you have a deployment of the `gpt-4o-realtime-preview` model, you can interact with it in real time in the AI Studio **Real-time audio** playground or Realtime API.

## Use the GPT-4o real-time audio

> [!TIP]
> Right now, the fastest way to get started development with the GPT-4o Realtime API is to download the sample code from the [Azure OpenAI GPT-4o real-time audio repository on GitHub](https://github.com/azure-samples/aoai-realtime-audio-sdk).

::: zone pivot="programming-language-ai-studio"

To chat with your deployed `gpt-4o-realtime-preview` model in the [Azure AI Studio](https://ai.azure.com) **Real-time audio** playground, follow these steps:

1. the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in AI Studio. Make sure you're signed in with the Azure subscription that has your Azure OpenAI Service resource and the deployed `gpt-4o-realtime-preview` model.
1. Select the **Real-time audio** playground from under **Resource playground** in the left pane.
1. Select your deployed `gpt-4o-realtime-preview` model from the **Deployment** dropdown. 
1. Select **Enable microphone** to allow the browser to access your microphone. If you already granted permission, you can skip this step.

    :::image type="content" source="./media/how-to/real-time/real-time-playground.png" alt-text="Screenshot of the real-time audio playground with the deployed model selected." lightbox="./media/how-to/real-time/real-time-playground.png":::

1. Optionally you can edit contents in the **Give the model instructions and context** text box. Give the model instructions about how it should behave and any context it should reference when generating a response. You can describe the assistant's personality, tell it what it should and shouldn't answer, and tell it how to format responses.
1. Optionally, change settings such as threshold, prefix padding, and silence duration.
1. Select **Start listening** to start the session. You can speak into the microphone to start a chat.

    :::image type="content" source="./media/how-to/real-time/real-time-playground-start-listening.png" alt-text="Screenshot of the real-time audio playground with the start listening button and microphone access enabled." lightbox="./media/how-to/real-time/real-time-playground-start-listening.png":::

1. You can interrupt the chat at any time by speaking. You can end the chat by selecting the **Stop listening** button.

::: zone-end

::: zone pivot="programming-language-javascript"

The JavaScript web sample demonstrates how to use the GPT-4o Realtime API to interact with the model in real time. The sample code includes a simple web interface that captures audio from the user's microphone and sends it to the model for processing. The model responds with text and audio, which the sample code renders in the web interface.

You can run the sample code locally on your machine by following these steps. Refer to the [repository on GitHub](https://github.com/azure-samples/aoai-realtime-audio-sdk) for the most up-to-date instructions.
1. If you don't have Node.js installed, download and install the [LTS version of Node.js](https://nodejs.org/).

1. Clone the repository to your local machine:
    
    ```bash
    git clone https://github.com/Azure-Samples/aoai-realtime-audio-sdk.git
    ```

1. Go to the `javascript/samples/web` folder in your preferred code editor.

    ```bash
    cd ./javascript/samples
    ```

1. Run `download-pkg.ps1` or `download-pkg.sh` to download the required packages. 

1. Go to the `web` folder from the `./javascript/samples` folder.

    ```bash
    cd ./web
    ```

1. Run `npm install` to install package dependencies.

1. Run `npm run dev` to start the web server, navigating any firewall permissions prompts as needed.
1. Go to any of the provided URIs from the console output (such as `http://localhost:5173/`) in a browser.
1. Enter the following information in the web interface:
    - **Endpoint**: The resource endpoint of an Azure OpenAI resource. You don't need to append the `/realtime` path. An example structure might be `https://my-azure-openai-resource-from-portal.openai.azure.com`.
    - **API Key**: A corresponding API key for the Azure OpenAI resource.
    - **Deployment**: The name of the `gpt-4o-realtime-preview` model that [you deployed in the previous section](#deploy-a-model-for-real-time-audio).
    - **System Message**: Optionally, you can provide a system message such as "You always talk like a friendly pirate."
    - **Temperature**: Optionally, you can provide a custom temperature.
    - **Voice**: Optionally, you can select a voice.
1. Select the **Record** button to start the session. Accept permissions to use your microphone if prompted.
1. You should see a `<< Session Started >>` message in the main output. Then you can speak into the microphone to start a chat.
1. You can interrupt the chat at any time by speaking. You can end the chat by selecting the **Stop** button.

::: zone-end

## Related content

* Learn more about Azure OpenAI [deployment types](./how-to/deployment-types.md)
* Learn more about Azure OpenAI [quotas and limits](quotas-limits.md)
