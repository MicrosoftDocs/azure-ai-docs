---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 7/17/2025
ms.author: pafarley
---

[!INCLUDE [Header](../../common/javascript.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

## Set up

1. Create a new folder `synthesis-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir synthesis-quickstart && cd synthesis-quickstart
    ```
    
1. Create the `package.json` with the following command:

    ```shell
    npm init -y
    ```

1. Install the Speech SDK for JavaScript with:

    ```console
    npm install microsoft-cognitiveservices-speech-sdk
    ```

### Retrieve resource information

[!INCLUDE [Environment variables](../../common/environment-variables.md)]

## Synthesize speech to a file

To translate speech from a file:

1. Create a new file named *synthesis.js* with the following content:

    ```javascript
    import { createInterface } from "readline";
    import { SpeechConfig, AudioConfig, SpeechSynthesizer, ResultReason } from "microsoft-cognitiveservices-speech-sdk";
    function synthesizeSpeech() {
        const audioFile = "YourAudioFile.wav";
        // This example requires environment variables named "ENDPOINT" and "SPEECH_KEY"
        const speechConfig = SpeechConfig.fromEndpoint(new URL(ENDPOINT), process.env.SPEECH_KEY);
        const audioConfig = AudioConfig.fromAudioFileOutput(audioFile);
        // The language of the voice that speaks.
        speechConfig.speechSynthesisVoiceName = "en-US-Ava:DragonHDLatestNeural";
        // Create the speech synthesizer.
        const synthesizer = new SpeechSynthesizer(speechConfig, audioConfig);
        const rl = createInterface({
            input: process.stdin,
            output: process.stdout
        });
        rl.question("Enter some text that you want to speak >\n> ", function (text) {
            rl.close();
            // Start the synthesizer and wait for a result.
            synthesizer.speakTextAsync(text, function (result) {
                if (result.reason === ResultReason.SynthesizingAudioCompleted) {
                    console.log("synthesis finished.");
                }
                else {
                    console.error("Speech synthesis canceled, " + result.errorDetails +
                        "\nDid you set the speech resource key and region values?");
                }
                synthesizer.close();
            }, function (err) {
                console.trace("err - " + err);
                synthesizer.close();
            });
            console.log("Now synthesizing to: " + audioFile);
        });
    }
    synthesizeSpeech();
    ```

    In *synthesis.js*, optionally you can rename *YourAudioFile.wav* to another output file name.

    To change the speech synthesis language, replace `en-US-Ava:DragonHDLatestNeural` with another [supported voice](~/articles/ai-services/speech-service/language-support.md#standard-voices).

    All neural voices are multilingual and fluent in their own language and English. For example, if the input text in English is *I'm excited to try text to speech* and you set `es-ES-Ximena:DragonHDLatestNeural`, the text is spoken in English with a Spanish accent. If the voice doesn't speak the language of the input text, the Speech service doesn't output synthesized audio.

1. Run your console application to start speech synthesis to a file:

   ```console
   node synthesis.js
   ```

## Output

You should see the following output in the console. Follow the prompt to enter text that you want to synthesize:

```console
Enter some text that you want to speak >
> I'm excited to try text to speech
Now synthesizing to: YourAudioFile.wav
synthesis finished.
```

## Remarks

### More speech synthesis options

This quickstart uses the `SpeakTextAsync` operation to synthesize a short block of text that you enter. You can also use long-form text from a file and get finer control over voice styles, prosody, and other settings.

- See [how to synthesize speech](~/articles/ai-services/speech-service/how-to-speech-synthesis.md) and [Speech Synthesis Markup Language (SSML) overview](~/articles/ai-services/speech-service/speech-synthesis-markup.md) for information about speech synthesis from a file and finer control over voice styles, prosody, and other settings.
- See [batch synthesis API for text to speech](~/articles/ai-services/speech-service/batch-synthesis.md) for information about synthesizing long-form text to speech.

### OpenAI text to speech voices in Azure Speech in Foundry Tools

OpenAI text to speech voices are also supported. See [OpenAI text to speech voices in Azure Speech](../../../openai-voices.md) and [multilingual voices](../../../language-support.md?tabs=tts#multilingual-voices). You can replace `en-US-Ava:DragonHDLatestNeural` with a supported OpenAI voice name such as `en-US-FableMultilingualNeural`.

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
