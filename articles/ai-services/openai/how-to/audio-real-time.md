---
title: 'How to use GPT-4o real-time audio with Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Learn how to use GPT-4o real-time audio with Azure OpenAI Service.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 10/1/2024
author: eric-urban
ms.author: eur
ms.custom: references_regions
recommendations: false
---

# GPT-4o real-time audio

Azure OpenAI GPT-4o audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. The GPT-4o audio `realtime` API is designed to handle real-time, low-latency conversational interactions, making it a great fit for use cases involving live interactions between a user and a model, such as customer support agents, voice assistants, and real-time translators.

Most users of this API need to deliver and receive audio from an end-user in real time, including applications that use WebRTC or a telephony system. The real-time API isn't designed to connect directly to end user devices and relies on client integrations to terminate end user audio streams. 

## Supported models

Currently only `gpt-4o-realtime-preview` version: `2024-10-01-preview` supports real-time audio.

The `gpt-4o-realtime-preview` model is available for global deployments in [East US 2 and Sweden Central regions](../concepts/models.md#global-standard-model-availability).

> [!IMPORTANT]
> The system stores your prompts and completions as described in the "Data Use and Access for Abuse Monitoring" section of the service-specific Product Terms for Azure OpenAI Service, except that the Limited Exception does not apply. Abuse monitoring will be turned on for use of the `gpt-4o-realtime-preview` API even for customers who otherwise are approved for modified abuse monitoring.

## API support

Support for real-time audio was first added in API version `2024-10-01-preview`. 

> [!NOTE]
> For more information about the API and architecture, see the [Azure OpenAI GPT-4o real-time audio repository on GitHub](https://github.com/azure-samples/aoai-realtime-audio-sdk).

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- An Azure OpenAI resource created in a [supported region](#supported-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

## Deploy a model for real-time audio

Before you can use GPT-4o real-time audio, you need a deployment of the `gpt-4o-realtime-preview` model in a supported region as described in the [supported models](#supported-models) section.

You can deploy the model from the Azure OpenAI model catalog or from your project in AI Studio. Follow these steps to deploy a `gpt-4o-realtime-preview` model from the [AI Studio model catalog](../../../ai-studio/how-to/model-catalog-overview.md):

1. Sign in to [AI Studio](https://ai.azure.com) and go to the **Home** page.
1. Select **Model catalog** from the left sidebar.
1. Search for and select the `gpt-4o-realtime-preview` model from the Azure OpenAI collection.
1. Select **Deploy** to open the deployment window. 
1. Select the subscription that you want to use.
1. Select **Customize** from the **Deployment details** section.
1. Enter a deployment name and select an Azure OpenAI resource.
1. Select `2024-10-01` from the **Model version** dropdown.
1. Modify other default settings depending on your requirements.
1. Select **Deploy**. You land on the deployment details page. 

Now that you have a deployment of the `gpt-4o-realtime-preview` model, you can use the playground to interact with the model in real time. Select **Early access playground** from the list of playgrounds in the left pane.

## Use the GPT-4o real-time audio API

> [!TIP]
> A playground for GPT-4o real-time audio is coming soon to [Azure AI Studio](https://ai.azure.com). You can already use the API directly in your application.

Right now, the fastest way to get started with GPT-4o real-time audio is to download the sample code from the [Azure OpenAI GPT-4o real-time audio repository on GitHub](https://github.com/azure-samples/aoai-realtime-audio-sdk).

The JavaScript web sample demonstrates how to use the GPT-4o real-time audio API to interact with the model in real time. The sample code includes a simple web interface that captures audio from the user's microphone and sends it to the model for processing. The model responds with text and audio, which the sample code renders in the web interface.
 
1. Clone the repository to your local machine:
    
    ```bash
    git clone https://github.com/Azure-Samples/aoai-realtime-audio-sdk.git
    ```

1. Go to the `javascript/samples/web` folder in your preferred code editor.

    ```bash
    cd .\javascript\samples\web\
    ```

1. If you don't have Node.js installed, download and install the [LTS version of Node.js](https://nodejs.org/).

1. Run `npm install` to download a few dependency packages. For more information, see the `package.json` file in the same `web` folder.

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

## Related content

* Learn more about Azure OpenAI [deployment types](./deployment-types.md)
* Learn more about Azure OpenAI [quotas and limits](../quotas-limits.md)
