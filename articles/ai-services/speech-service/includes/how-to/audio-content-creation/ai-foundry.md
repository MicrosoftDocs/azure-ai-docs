---
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 8/5/2025
---

## Prerequisites

- An active Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Permission to create resources in your subscription.
- A Microsoft Foundry project. For more information, see [Create a Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects).

## Use the audio content creation tool

The following diagram displays the process for fine-tuning the text to speech outputs. 

:::image type="content" source="../../../media/audio-content-creation/audio-content-creation-diagram.jpg" alt-text="Diagram of the sequence of steps for fine-tuning text to speech outputs." lightbox="../../../media/audio-content-creation/audio-content-creation-diagram.jpg":::

### Access the tool

To access the audio content creation tool in Microsoft Foundry, follow these steps:

1. Go to your project in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). 
1. Select **Playgrounds** from the left pane.
1. In the **Speech playground** tile, select **Try the Speech playground**.
1. Select **Text to speech** > **Audio content creation**. You might need to scroll to find the tile. 

   :::image type="content" source="../../../media/voice-live/foundry-portal/capabilities-by-scenario.png" alt-text="Screenshot of filtering Speech service capabilities by scenario." lightbox="../../../media/voice-live/foundry-portal/capabilities-by-scenario.png":::

### Workflow overview

Once you have access to the tool, follow this general workflow:

1. [Create an audio tuning file](#create-an-audio-tuning-file) by using plain text or SSML scripts. Enter or upload your content into audio content creation.
1. Choose the voice and the language for your script content. Audio content creation includes all of the [standard text to speech voices](../../../language-support.md?tabs=tts). You can use standard voices or a custom voice.

   > [!NOTE]
   > Custom voice access is [limited](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access) based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).

1. Select the content you want to preview, and then select **Play** (via the triangle icon) to preview the default synthesis output. 

   If you make any changes to the text, select the **Stop** icon, and then select **Play** again to regenerate the audio with changed scripts. 

   Improve the output by adjusting pronunciation, break, pitch, rate, intonation, voice style, and more. For a complete list of options, see [Speech Synthesis Markup Language](../../../speech-synthesis-markup.md). 

1. Save and [export your tuned audio](#export-tuned-audio). 

   When you save the tuning track in the system, you can continue to work and iterate on the output. When you're satisfied with the output, you can create an audio creation task with the export feature. You can observe the status of the export task and download the output for use with your apps and products.

## Create an audio tuning file

You can get your content into the audio content creation tool in either of two ways:

### Option 1: Create a new audio tuning file

1. Select **New** > **Text file** to create a new audio tuning file.

1. Enter or paste your content into the editing window. The allowable number of characters for each file is 20,000 or fewer. If your script contains more than 20,000 characters, you can use Option 2 to automatically split your content into multiple files.

1. Select **Save**.

### Option 2: Upload an audio tuning file

1. Select **Upload** > **Text file** to import one or more text files. Both plain text and SSML are supported. 

   If your script file is more than 20,000 characters, split the content by paragraphs, by characters, or by regular expressions.

1. When you upload your text files, make sure that they meet these requirements:

   | Property | Description |
   |----------|---------------|
   | File format | Plain text (.txt) or SSML text (.txt)<br/><br/>Zip files aren't supported. |
   | Encoding format | UTF-8 |
   | File name | Each file must have a unique name. Duplicate files aren't supported. |
   | Text length | Character limit is 20,000. If your files exceed the limit, split them according to the instructions in the tool. |
   | SSML restrictions | Each SSML file can contain only a single piece of SSML. |
      

   Here's a plain text example:

   ```txt
   Welcome to use audio content creation to customize audio output for your products.
   ```

   Here's an SSML example:

   ```xml
   <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" version="1.0" xml:lang="en-US">
      <voice name="en-US-AvaMultilingualNeural">
      Welcome to use audio content creation <break time="10ms" />to customize audio output for your products.
      </voice>
   </speak>
   ```

## Export tuned audio

After you review your audio output and are satisfied with your tuning and adjustment, you can export the audio.

1. Select **Export** to create an audio creation task. 

   We recommend **Export to Audio library** to easily store, find, and search audio output in the cloud. You can better integrate with your applications through Azure blob storage. You can also download the audio to your local disk directly.
   
1. Choose the output format for your tuned audio. The **supported audio formats and sample rates** are listed in the following table:

    | Format | 8 kHz sample rate | 16 kHz sample rate | 24 kHz sample rate | 48 kHz sample rate |
    |--- |--- |--- |--- |--- |
    | wav | riff-8khz-16bit-mono-pcm | riff-16khz-16bit-mono-pcm | riff-24khz-16bit-mono-pcm |riff-48khz-16bit-mono-pcm |
    | mp3 | N/A | audio-16khz-128kbitrate-mono-mp3 | audio-24khz-160kbitrate-mono-mp3 |audio-48khz-192kbitrate-mono-mp3 |
    
1. To view the status of the task, select the **Task list** tab. 

   If the task fails, see the detailed information page for a full report.

1. When the task is complete, your audio is available for download on the **Audio library** pane.

1. Select the file you want to download and **Download**. 

Now you're ready to use your custom tuned audio in your apps or products.
   