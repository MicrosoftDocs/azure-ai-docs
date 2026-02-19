---
title: include file
description: include file
author: PatrickFarley
reviewer: patrickfarley
ms.author: pafarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 12/19/2025
ms.custom: references_regions
---

In this article, you learn how to use video translation with Azure Speech in Foundry Tools in the [Speech Studio](https://aka.ms/speechstudio).

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a free account before you begin.
- A Speech resource [in a supported region](../../../regions.md?tabs=speech-translation). If you don't have a Speech resource, create one in the [Azure portal](https://portal.azure.com/).
- An [Azure Blob Storage](/azure/storage/blobs/storage-blobs-overview) account. 
- You need a video file in .mp4 format, less than 5 GB, and shorter than 4 hours. For testing purposes, you can use the sample video file provided by Microsoft at [https://ai.azure.com/speechassetscache/ttsvoice/VideoTranslation/PublicDoc/SampleData/es-ES-TryOutOriginal.mp4](https://ai.azure.com/speechassetscache/ttsvoice/VideoTranslation/PublicDoc/SampleData/es-ES-TryOutOriginal.mp4).
- Make sure video translation supports your [source and target language](../../../language-support.md?tabs=speech-translation#video-translation).

## Create a video translation project

To create a video translation project, follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio).
   
1. Select the subscription and Speech resource to work with. 

1. Select **Video translation**.

1. On the **Create and Manage Projects** page, select **Create a project**.

1. On the **New project** page, select a **Voice type**.

   :::image type="content" source="../../../media/video-translation/select-voice-type.png" alt-text="Screenshot of selecting a voice type on the new project page." lightbox="../../../media/video-translation/select-voice-type.png":::
   
   The voice type options are:
   - **Standard voice**: The service automatically selects the most suitable standard voice by matching the speaker's voice in the video with standard voices.
   - **Personal voice**: Use the personal voice that matches the voice of the speakers in the video. 

   > [!NOTE]
   > To use personal voice, you need to apply for [access](https://aka.ms/customneural). 
    
1. Upload your video file by dragging and dropping the video file or selecting the file manually. The video must be in .mp4 format, less than 5 GB, and shorter than 4 hours.
   
1. Provide the **Project name**, **Number of speakers**, **Language of the video**, and **Translate to** language.

1. Select the boxes to acknowledge the pricing information and code of conduct. 

1. Select **Next: Advanced settings** if you want to adjust the advanced settings. 

    :::image type="content" source="../../../media/video-translation/provide-video-information.png" alt-text="Screenshot of providing video information on the new project page." lightbox="../../../media/video-translation/provide-video-information.png":::

1. Optionally, you can adjust the following settings:

    - **Lexicon file**: This option allows you to add custom words or phrases that the system should recognize and pronounce correctly. You can create a lexicon file in the [audio content creation tool in the Speech Studio](https://aka.ms/speechstudio) and select it here. 
    - **Burn subtitles**: This option allows you to add subtitles to the video. The subtitle file can be in WebVTT or JSON format. You can download a sample WebVTT file for your reference by selecting **Download sample VTT file**.
   
    :::image type="content" source="../../../media/video-translation/provide-video-information-advanced.png" alt-text="Screenshot of providing lexicon and subtitle information while creating a new project." lightbox="../../../media/video-translation/provide-video-information-advanced.png":::

   If you want to use your own subtitle files, select **Subtitle** > **Upload your own**. You can choose to upload either the source subtitle file or the target subtitle file. 
   - Automatic subtitles: Results in both source and target language subtitles.
   - Upload source language subtitles: Results in both source and target language subtitles.
   - Upload target language subtitles: Results in only target language subtitles.

1. Select **Create**.

Once the upload to Azure Blob Storage is complete, you can check the processing status on the project tab.

After the project is created, you can select the project to review detailed settings and make adjustments according to your preferences.

## Check and adjust voice settings

On the project details page, you can see the **Translated** and **Original** tabs under **Video**. You can compare the original and translated videos by selecting the corresponding tab. The translated video is generated automatically, and you can play it to check the translation quality. 

To the right side of the video, you can view both the original script and the translated script. Hovering over each part of the original script triggers the video to automatically jump to the corresponding segment of the original video, while hovering over each part of the translated script triggers the video to jump to the corresponding translated segment.

You can also add or remove segments as needed. When you want to add a segment, ensure that the new segment timestamp doesn't overlap with the previous and next segment, and the segment end time should be larger than the start time. The correct format of timestamp should be `hh:mm:ss.ms`. Otherwise, you can't apply the changes.

You can adjust the time frame of the scripts directly using the audio waveform below the video. The adjustments will be applied after you select **Apply changes**. 

If you encounter segments with an "unidentified" voice name, it might be because the system couldn't accurately detect the voice, especially in situations where speaker voices overlap. In such cases, it's advisable to manually change the voice name.  

:::image type="content" source="../../../media/video-translation/voice-unidentified.png" alt-text="Screenshot of one segment with unidentified voice name." lightbox="../../../media/video-translation/voice-unidentified.png":::

If you want to adjust the voice, select **Voice settings** to make some changes. On the **Voice settings** page, you can adjust the voice type, gender, and the voice. Select the voice sample on the right of **Voice** to determine your voice selection. If you find there's missing voice, you can add the new voice name by selecting **Add speaker**. After changing the settings, select **Update**. 

:::image type="content" source="../../../media/video-translation/voice-settings.png" alt-text="Screenshot of adjusting voice settings on the voice settings page." lightbox="../../../media/video-translation/voice-settings.png":::

You can make multiple changes to the video, including adjusting the voice settings, adding or removing segments, and changing the time frame of the scripts. You're only charged after you select **Apply changes** to apply your changes. You can select **Save** to save work in progress without incurring any charges.

:::image type="content" source="../../../media/video-translation/apply-changes.png" alt-text="Screenshot of selecting apply changes button after making all changes." lightbox="../../../media/video-translation/apply-changes.png":::

## Translate to another language

You can keep the current translation project and translate the original video into another language.

1. Open your project.
1. Select **+ New language**. 
1. On the new **Translate** page that appears, choose a new translated language and voice type. Once the video is translated, a new project is automatically created. 

## Related content

- [Video translation overview](../../../video-translation-overview.md)