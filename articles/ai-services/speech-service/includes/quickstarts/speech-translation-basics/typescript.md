---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 1/29/2026
ms.author: pafarley
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/javascript.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

## Set up the environment

1. Create a new folder `translation-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir translation-quickstart && cd translation-quickstart
    ```
    
1. Create the `package.json` with the following command:

    ```shell
    npm init -y
    ```

1. Update the `package.json` to ECMAScript with the following command:
    ```shell
    npm pkg set type=module
    ```

1. Install the Speech SDK for JavaScript with:

    ```console
    npm install microsoft-cognitiveservices-speech-sdk
    ```

1. You need to install the Node.js type definitions to avoid TypeScript errors. Run the following command:

    ```shell
    npm install --save-dev @types/node
    ```

### Retrieve resource information

[!INCLUDE [Environment variables](../../common/environment-variables.md)]

## Translate speech from a file 

To translate speech from a file:

1. Create a new file named *translation.ts* with the following content:

    ```typescript
    import { readFileSync } from "fs";
    import { 
        SpeechTranslationConfig, 
        AudioConfig, 
        TranslationRecognizer, 
        ResultReason, 
        CancellationDetails, 
        CancellationReason,
        TranslationRecognitionResult 
    } from "microsoft-cognitiveservices-speech-sdk";
    
    // This example requires environment variables named "ENDPOINT" and "SPEECH_KEY"
    const speechTranslationConfig: SpeechTranslationConfig = SpeechTranslationConfig.fromEndpoint(new URL(process.env.ENDPOINT!), process.env.SPEECH_KEY!);
    speechTranslationConfig.speechRecognitionLanguage = "en-US";
    
    const language = "it";
    speechTranslationConfig.addTargetLanguage(language);
    
    function fromFile(): void {
        const audioConfig: AudioConfig = AudioConfig.fromWavFileInput(readFileSync("YourAudioFile.wav"));
        const translationRecognizer: TranslationRecognizer = new TranslationRecognizer(speechTranslationConfig, audioConfig);
    
        translationRecognizer.recognizeOnceAsync((result: TranslationRecognitionResult) => {
            switch (result.reason) {
                case ResultReason.TranslatedSpeech:
                    console.log(`RECOGNIZED: Text=${result.text}`);
                    console.log("Translated into [" + language + "]: " + result.translations.get(language));
    
                    break;
                case ResultReason.NoMatch:
                    console.log("NOMATCH: Speech could not be recognized.");
                    break;
                case ResultReason.Canceled:
                    const cancellation: CancellationDetails = CancellationDetails.fromResult(result);
                    console.log(`CANCELED: Reason=${cancellation.reason}`);
    
                    if (cancellation.reason === CancellationReason.Error) {
                        console.log(`CANCELED: ErrorCode=${cancellation.ErrorCode}`);
                        console.log(`CANCELED: ErrorDetails=${cancellation.errorDetails}`);
                        console.log("CANCELED: Did you set the speech resource key and endpoint values?");
                    }
                    break;
            }
            translationRecognizer.close();
        });
    }
    fromFile();
    ```

    - In `translation.ts`, replace `YourAudioFile.wav` with your own WAV file. This example only recognizes speech from a WAV file. For information about other audio formats, see [How to use compressed input audio](~/articles/ai-services/speech-service/how-to-use-codec-compressed-audio-input-streams.md). This example supports up to 30 seconds audio.

    - To change the speech recognition language, replace `en-US` with another [supported language](~/articles/ai-services/speech-service/language-support.md?tabs=stt#supported-languages). Specify the full locale with a dash (`-`) separator. For example, `es-ES` for Spanish (Spain). The default language is `en-US` if you don't specify a language. For details about how to identify one of multiple languages that might be spoken, see [language identification](~/articles/ai-services/speech-service/language-identification.md).

    - To change the translation target language, replace `it` with another [supported language](~/articles/ai-services/speech-service/language-support.md?tabs=speech-translation#supported-languages). With few exceptions you only specify the language code that precedes the locale dash (`-`) separator. For example, use `es` for Spanish (Spain) instead of `es-ES`. The default language is `en` if you don't specify a language.

1. Create the `tsconfig.json` file to transpile the TypeScript code and copy the following code for ECMAScript.

    ```json
    {
        "compilerOptions": {
          "module": "NodeNext",
          "target": "ES2022", // Supports top-level await
          "moduleResolution": "NodeNext",
          "skipLibCheck": true, // Avoid type errors from node_modules
          "strict": true // Enable strict type-checking options
        },
        "include": ["*.ts"]
    }
    ```

1. Transpile from TypeScript to JavaScript.

    ```shell
    tsc
    ```

    This command should produce no output if successful.

1. Run your new console application to start speech recognition from a file:

    ```console
    node translation.js
    ```

## Output 

The speech from the audio file should be output as translated text in the target language:

```console
RECOGNIZED: Text=I'm excited to try speech translation.
Translated into [it]: Sono entusiasta di provare la traduzione vocale.
```

## Remarks

Now that you've completed the quickstart, here are some additional considerations:

This example uses the `recognizeOnceAsync` operation to transcribe utterances of up to 30 seconds, or until silence is detected. For information about continuous recognition for longer audio, including multi-lingual conversations, see [How to translate speech](~/articles/ai-services/speech-service/how-to-translate-speech.md).

> [!NOTE]
> Recognizing speech from a microphone is not supported in Node.js. It's supported only in a browser-based JavaScript environment. 

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
