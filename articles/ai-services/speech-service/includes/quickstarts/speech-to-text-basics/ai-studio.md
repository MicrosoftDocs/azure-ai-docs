---
author: eric-urban
ms.service: azure-ai-speech
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: include
ms.date: 5/21/2024
ms.author: eur
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

In this quickstart, you try real-time speech to text in [Azure AI Foundry](https://ai.azure.com). 

## Prerequisites

[!INCLUDE [Prerequisites](../../../../includes/quickstarts/ai-studio-prerequisites.md)]

## Try real-time speech to text

1. Go to your AI Foundry project. If you need to create a project, see [Create an AI Foundry project](../../../../../ai-studio/how-to/create-projects.md).
1. Select **Playgrounds** from the left pane and then select a playground to use. In this example, select **Try the Speech playground**.

    :::image type="content" source="../../../../../ai-studio/media/ai-services/playgrounds/azure-ai-services-playgrounds.png" alt-text="Screenshot of the project level playgrounds that you can use." lightbox="../../../../../ai-studio/media/ai-services/playgrounds/azure-ai-services-playgrounds.png":::

1. Optionally, you can select a different connection to use in the playground. In the Speech playground, you can connect to Azure AI Services multi-service resources or Speech service resources. 

    :::image type="content" source="../../../../../ai-studio/media/ai-services/playgrounds/speech-playground.png" alt-text="Screenshot of the Speech playground in a project." lightbox="../../../../../ai-studio/media/ai-services/playgrounds/speech-playground.png":::

1. Select **Real-time transcription**.
1. Select **Show advanced options** to configure speech to text options such as: 

    - **Language identification**: Used to identify languages spoken in audio when compared against a list of supported languages. For more information about language identification options such as at-start and continuous recognition, see [Language identification](../../../language-identification.md).
    - **Speaker diarization**: Used to identify and separate speakers in audio. Diarization distinguishes between the different speakers who participate in the conversation. The Speech service provides information about which speaker was speaking a particular part of transcribed speech. For more information about speaker diarization, see the [real-time speech to text with speaker diarization](../../../get-started-stt-diarization.md) quickstart.
    - **Custom endpoint**: Use a deployed model from custom speech to improve recognition accuracy. To use Microsoft's baseline model, leave this set to None. For more information about custom speech, see [Custom Speech](../../../custom-speech-overview.md).
    - **Output format**: Choose between simple and detailed output formats. Simple output includes display format and timestamps. Detailed output includes more formats (such as display, lexical, ITN, and masked ITN), timestamps, and N-best lists. 
    - **Phrase list**: Improve transcription accuracy by providing a list of known phrases, such as names of people or specific locations. Use commas or semicolons to separate each value in the phrase list. For more information about phrase lists, see [Phrase lists](../../../improve-accuracy-phrase-list.md).

1. Select an audio file to upload, or record audio in real-time. In this example, we use the `Call1_separated_16k_health_insurance.wav` file that's available in the [Speech SDK repository on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/raw/master/scenarios/call-center/sampledata/Call1_separated_16k_health_insurance.wav). You can download the file or use your own audio file.

    :::image type="content" source="../../../media/ai-studio/real-time-speech-to-text-audio.png" alt-text="Screenshot of the option to select an audio file or speak into a microphone." lightbox="../../../media/ai-studio/real-time-speech-to-text-audio.png":::

1. You can view the real-time transcription at the bottom of the page.

    :::image type="content" source="../../../media/ai-studio/real-time-speech-to-text-results.png" alt-text="Screenshot of the real-time transcription results in Azure AI Foundry." lightbox="../../../media/ai-studio/real-time-speech-to-text-results.png":::

1. You can select the **JSON** tab to see the JSON output of the transcription. Properties include `Offset`, `Duration`, `RecognitionStatus`, `Display`, `Lexical`, `ITN`, and more.

    :::image type="content" source="../../../media/ai-studio/real-time-speech-to-text-results-json.png" alt-text="Screenshot of the real-time transcription results in JSON format in Azure AI Foundry." lightbox="../../../media/ai-studio/real-time-speech-to-text-results-json.png":::
