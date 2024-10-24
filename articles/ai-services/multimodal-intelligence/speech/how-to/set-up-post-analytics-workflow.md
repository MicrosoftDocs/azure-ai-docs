---
title: Azure AI Multimodal Intelligence set up a post-call analytics workflow
titleSuffix: Azure AI services
description: Learn how to set up a post-call analytics workflow
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure
ms.topic: overview
ms.date: 10/24/2024
---

# Set up a post-call analytics workflow in Azure AI Studio

> [!IMPORTANT]
>
> * Azure AI Multimodal Intelligence is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes may change or have constrained capabilities, prior to General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).


Azure AI Multimodal Intelligence in [Azure AI Studio](https://ai.azure.com/) is a feature that allows you to extract insights from audio files using customizable extraction schemas. You can use Multimodal Intelligence to generate summaries, detect roles, extract information, and more from the conversation transcripts of your audio files.

Post-call analytics is a process that uses AI, natural language processing (NLP), and speech analytics to review customer-agent interactions after a call ends. It can help you gain insights, measure performance, and improve customer experiences.

In this article, you learn how to create a post call analytics workflow with an Multimodal Intelligence project using the following resources:

* An AI Studio hub and connected Azure Blob Storage account.

* An Azure AI services connection for the hub.

* An Multimodal Intelligence project in the hub.

## Prerequisites

* To get started, you need an active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free 12-month subscription**](https://azure.microsoft.com/free/).
* Once you have your Azure subscription, you need an [**Azure AI services multi-services resource**](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices) created in one of the supported regions. The following regions support Multimodal Intelligence speech capabilities:

     * West US

     * East US

     * West Europe

     * Sweden Central

     * SouthEast Asia

     * Australia East

* An audio file (less than 2 hours long and less than 200 MB in size) in one of the formats and codecs supported. Multimodal Intelligence speech capabilities supports multiple audio formats and codecs, such as:

* `WAV`
* `MP3`
* `OPUS/OGG`
* `FLAC`
* `WMA`
* `AAC`
* `ALAW` in `WAV` container
* `MULAW` in `WAV` container
* `AMR`
* `WebM`
* `M4A`
* `SPEEX`

## Create an AI Studio hub

You deploy and manage your Azure AI Studio projects in hubs. Here's how to create a new hub:

1. Navigate to the Home page in [Azure AI studio](https://ai.azure.com/) and sign in with your Azure account.

1. Select **All hubs** from the left pane and then select **➕New hub**.


    :::image type="content" source="../../media/ai-studio/hub/create-new.png" alt-text="Screenshot of the create a new hub button." lightbox="../../media/ai-studio/create-new-hub.png":::

1. In the **Create a new hub** dialog window, enter a name for your hub and select **Next**. Leave the default **Connect Azure AI Services** option selected. A new Azure AI services connection is created for the hub.


    :::image type="content" source="../../media/ai-studio/hub/create-new-connection.png" alt-text="Screenshot of the create a new hub dialog window." lightbox="../../media/ai-studio/create-new-connection.png":::

1. Review your entries then select **Create**.

    :::image type="content" source="../../media/ai-studio/hub/create-new-review.png" alt-text="Screenshot of the review and finish dialog window." lightbox="../../media/ai-studio/create-new-hub-review.png":::

1. You can review the progress of the hub creation in the deployment wizard. The deployment may take a few minutes to complete.

## Create a speech analytics project in your AI Studio hub


A speech analytics project is a specialized project in Azure AI Studio that primarily has resources and tools for speech analytics. You see it listed among your other projects int he studio. When you create a speech analytics project, you also create a generative AI project. The generative AI project is where you customize the prompt flow deployment.

Follow these steps to create a speech analytics project in your hub:

Navigate to the Home page and select AI Services from the left pane. Then select **Speech analytics** from the list of features.

    :::image type="content" source="../../media/ai-studio/speech-analytics/choose-project.png" alt-text="Screenshot of the Speech analytics selection tab.":::

1. On the Speech analytics page, select **➕New speech analytics project**.

    :::image type="content" source="../../media/ai-studio/speech-analytics/start-new-project.png" alt-text="Screenshot of the start new speech analytics project window." lightbox="../../media/ai-studio/speech-analytics/start-new-project.png":::

1. **Scenario**. In the **Create a speech analytics project** dialog window, select **Post-call analytics**, and then select **Next**.

    :::image type="content" source="../../media/ai-studio/speech-analytics/create-project-scenario.png" alt-text="Screenshot the Scenario window." lightbox="../../media/ai-studio/speech-analytics/create-project-scenario.png":::

1. **Project details**. Enter a **Project name**, select the **Hub** that you previously created from the dropdown list, and then select **Next**.

    :::image type="content" source="../../media/ai-studio/speech-analytics/create-project-details.png" alt-text="Screenshot the Project details window." lightbox="../../media/ai-studio/speech-analytics/create-project-details.png":::

1. **Data settings**. Leave the default settings selected for the data location. Optionally, you can select **Show advanced settings** to view the names of the storage containers that you use later during prompt flow. Select **Next**.

    :::image type="content" source="../../media/ai-studio/speech-analytics/create-project-data-settings.png" alt-text="Screenshot the Data settings window." lightbox="../../media/ai-studio/speech-analytics/create-project-data-settings.png":::

1. **Speech settings**. Leave the default setting selected for the Azure AI services connection. This setting is used to connect to the GPT chat model deployment that you created earlier.

   * Select the spoken language in the audio file corresponding to the transcription that you want to analyze. Select *English (United States)* if you're using our [**sample audio file on GitHub**](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/call-center/sampledata/Call1_separated_16k_health_insurance.wav).

      :::image type="content" source="../../media/ai-studio/speech-analytics/create-project-speech-settings.png" alt-text="Screenshot the speech settings window." lightbox="../../media/ai-studio/speech-analytics/create-project-speech-settings.png":::

   * In the same **Speech settings** dialog window, you can select **Show advanced settings** to view the Azure AI Speech features that can be enabled for your speech analytics project. You can enable features such as language identification, profanity filter mode, and more. Speech analytics supports a subset of the batch transcription API request options.

      >[!NOTE]
      > Make sure that you select **20231129 Batch Transcription** from the **Speech to text model** dropdown menu.

       :::image type="content" source="../../media/ai-studio/speech-analytics/create-project-advanced-settings.png" alt-text="Screenshot the advanced settings window." lightbox="../../media/ai-studio/speech-analytics/create-project-advanced-settings.png":::

   * After you complete your selections, select **Next**.

1. **Analytics settings**. Select the Azure OpenAI model deployment that you created earlier. Leave the default settings selected for the generative AI project, prompt flow, and custom connection. Then select **Next**.

   :::image type="content" source="../../media/ai-studio/speech-analytics/create-project-analytics-settings.png" alt-text="Screenshot the analytics settings window." lightbox="../../media/ai-studio/speech-analytics/create-project-analytics-settings.png":::

1. **Review**. After you review the settings for the speech analytics project, select **Create project**.

   :::image type="content" source="../../media/ai-studio/speech-analytics/create-project-review-settings.png" alt-text="Screenshot the review settings window." lightbox="../../media/ai-studio/speech-analytics/create-project-review-settings.png":::

1. You can view the progress of the speech analytics project creation in the deployment wizard window. The deployment may take up to 10 minutes to complete.


1. After the setup is complete, the speech analytics project opens on the overview page.

## Analyze the transcript of an audio file

The transcription is what you analyze with the prompt flow in AI Studio. You can upload an audio file in AI Studio and get a transcript of the audio file. Then speech analytics processes the transcript and generates analytics results based on the prompt flow that the wizard created and deployed for you:

1. Navigate to the hub that you previously created. You can find and select the hub via the **Home** → **All resources** page.

1. On the Hub overview page, select the speech analytics project (not the generative AI project) that you previously created.

1. Navigate to the Upload and monitor page and select **Upload data**.

   :::image type="content" source="../../media/ai-studio/speech-analytics/upload-monitor-data.png" alt-text="Screenshot the upload and monitor data window." lightbox="../../media/ai-studio/speech-analytics/upload-monitor-data.png":::

1. In the **Upload data** dialog window, select the audio file that you want to analyze. You can use the [**sample *.wav* file**](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/call-center/sampledata/Call1_separated_16k_health_insurance.wav) in our GitHub repo.

## Monitor analytics results in AI Studio

You can monitor the analytics results in the Speech analytics project in AI Studio:

1. Navigate to the **Upload and monitor** page to see the status of processing the audio file that you uploaded.

   :::image type="content" source="../../media/ai-studio/speech-analytics/monitor-analytics-results.png" alt-text="Screenshot the monitor analytics results window." lightbox="../../media/ai-studio/speech-analytics/monitor-analytics-results.png":::

1. You can also access the transcription in your transcription container in the Azure portal. The wizard created the storage container during the speech analytics project creation process.

That's it! You successfully created a speech analytics project in AI Studio and used prompt flow to generate analytics results from the transcripts of your audio files.