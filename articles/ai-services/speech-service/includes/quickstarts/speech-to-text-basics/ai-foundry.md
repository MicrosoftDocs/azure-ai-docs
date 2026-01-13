---
author: PatrickFarley
ms.service: azure-ai-speech
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: include
ms.date: 4/14/2025
ms.author: pafarley
---

In this quickstart, you try real-time speech to text in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). 

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project. If you need to create a project, see [Create a Microsoft Foundry project](../../../../../ai-foundry/how-to/create-projects.md).

## Try real-time speech to text

#### [Foundry (new) portal](#tab/new-foundry)

1. [!INCLUDE [foundry-sign-in](../../../../../ai-foundry/default/includes/foundry-sign-in.md)]
1. Select **Build** from the top right menu.
1. Select **Models** on the left pane. 
1. The **AI Services** tab shows the Foundry models that can be used out of the box in the Foundry portal. Select **Azure Speech - Speech to text** to open the Speech to Text playground.
1. Optionally use the **Parameters** section to change the task, language, profanity policy, and other settings. You can also add special instructions for the LLM.
1. Use the **Upload files** section to select your audio file. Then select **Start**.
1. View the transcription output in the **Transcript** tab. Optionally view the raw API response output in the **JSON** tab.
1. Switch to the **Code** tab to get the sample code for using the speech to text feature in your application.

## Other Foundry (new) features


[!INCLUDE [speech-features-foundry](../../../../../ai-foundry/default/includes/speech-features-foundry.md)]

#### [Foundry (classic) portal](#tab/classic-foundry)

1. [!INCLUDE [classic-sign-in](../../../../../ai-foundry/includes/classic-sign-in.md)]
1. Select **Playgrounds** from the left pane and then select a playground to use. In this example, select **Try the Speech playground**.

    :::image type="content" source="../../../../../ai-services/media/ai-foundry/azure-ai-services-playgrounds.png" alt-text="Screenshot of the project level playgrounds that you can use." lightbox="../../../../../ai-services/media/ai-foundry/azure-ai-services-playgrounds.png":::

1. Select **Real-time transcription**.
1. Select **Show advanced options** to configure speech to text options such as: 

    - **Language identification**: Used to identify languages spoken in audio when compared against a list of supported languages. For more information about language identification options such as at-start and continuous recognition, see [Language identification](../../../language-identification.md).
    - **Speaker diarization**: Used to identify and separate speakers in audio. Diarization distinguishes between the different speakers who participate in the conversation. The Speech service provides information about which speaker was speaking a particular part of transcribed speech. For more information about speaker diarization, see the [real-time speech to text with speaker diarization](../../../get-started-stt-diarization.md) quickstart.
    - **Custom endpoint**: Use a deployed model from custom speech to improve recognition accuracy. To use Microsoft's baseline model, leave this set to None. For more information about custom speech, see [Custom Speech](../../../custom-speech-overview.md).
    - **Output format**: Choose between simple and detailed output formats. Simple output includes display format and timestamps. Detailed output includes more formats (such as display, lexical, ITN, and masked ITN), timestamps, and N-best lists. 
    - **Phrase list**: Improve transcription accuracy by providing a list of known phrases, such as names of people or specific locations. Use commas or semicolons to separate each value in the phrase list. For more information about phrase lists, see [Phrase lists](../../../improve-accuracy-phrase-list.md).

1. Select an audio file to upload, or record audio in real-time. In this example, we use the `Call1_separated_16k_health_insurance.wav` file that's available in the [Speech SDK repository on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/raw/master/scenarios/call-center/sampledata/Call1_separated_16k_health_insurance.wav). You can download the file or use your own audio file.

    :::image type="content" source="../../../media/ai-foundry/real-time-speech-to-text-audio.png" alt-text="Screenshot of the option to select an audio file or speak into a microphone." lightbox="../../../media/ai-foundry/real-time-speech-to-text-audio.png":::

1. You can view the real-time transcription at the bottom of the page.

    :::image type="content" source="../../../media/ai-foundry/real-time-speech-to-text-results.png" alt-text="Screenshot of the real-time transcription results in Microsoft Foundry." lightbox="../../../media/ai-foundry/real-time-speech-to-text-results.png":::

1. You can select the **JSON** tab to see the JSON output of the transcription. Properties include `Offset`, `Duration`, `RecognitionStatus`, `Display`, `Lexical`, `ITN`, and more.

    :::image type="content" source="../../../media/ai-foundry/real-time-speech-to-text-results-json.png" alt-text="Screenshot of the real-time transcription results in JSON format in Microsoft Foundry." lightbox="../../../media/ai-foundry/real-time-speech-to-text-results-json.png":::
