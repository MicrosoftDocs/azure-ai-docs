---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 7/16/2025
ms.author: pafarley
---

[!INCLUDE [Header](../../common/javascript.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

You also need a *.wav* audio file on your local machine. You can use your own *.wav* file (up to 30 seconds) or download the [https://crbn.us/whatstheweatherlike.wav](https://crbn.us/whatstheweatherlike.wav) sample file.

## Setup

1. Create a new folder `transcription-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir transcription-quickstart && cd transcription-quickstart
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

## Recognize speech from a file

To transcribe speech from a file:

1. Create a new file named *transcription.ts* with the following content:

    ```typescript
    import { readFileSync } from "fs";
    import { 
        SpeechConfig, 
        AudioConfig, 
        SpeechRecognizer, 
        ResultReason, 
        CancellationDetails, 
        CancellationReason,
        SpeechRecognitionResult 
    } from "microsoft-cognitiveservices-speech-sdk";
    
    // This example requires environment variables named "ENDPOINT" and "SPEECH_KEY"
    const speechConfig: SpeechConfig = SpeechConfig.fromEndpoint(new URL(process.env.ENDPOINT!), process.env.SPEECH_KEY!);
    speechConfig.speechRecognitionLanguage = "en-US";
    
    function fromFile(): void {
        const audioConfig: AudioConfig = AudioConfig.fromWavFileInput(readFileSync("YourAudioFile.wav"));
        const speechRecognizer: SpeechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
    
        speechRecognizer.recognizeOnceAsync((result: SpeechRecognitionResult) => {
            switch (result.reason) {
                case ResultReason.RecognizedSpeech:
                    console.log(`RECOGNIZED: Text=${result.text}`);
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
                        console.log("CANCELED: Did you set the speech resource key and region values?");
                    }
                    break;
            }
            speechRecognizer.close();
        });
    }
    
    fromFile();
    ```

    In *transcription.ts*, replace *YourAudioFile.wav* with your own *.wav* file. This example only recognizes speech from a *.wav* file. For information about other audio formats, see [How to use compressed input audio](~/articles/ai-services/speech-service/how-to-use-codec-compressed-audio-input-streams.md). This example supports up to 30 seconds of audio.

    To change the speech recognition language, replace `en-US` with another [supported language](~/articles/ai-services/speech-service/language-support.md). For example, use `es-ES` for Spanish (Spain). If you don't specify a language, the default is `en-US`. For details about how to identify one of multiple languages that might be spoken, see [Language identification](~/articles/ai-services/speech-service/language-identification.md).

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
   node transcription.js
   ```

Wait a few moments to get the response.

## Output

The speech from the audio file should be output as text:

```output
RECOGNIZED: Text=I'm excited to try speech to text.
```

## Remarks

This example uses the `recognizeOnceAsync` operation to transcribe utterances of up to 30 seconds, or until silence is detected. For information about continuous recognition for longer audio, including multi-lingual conversations, see [How to recognize speech](~/articles/ai-services/speech-service/how-to-recognize-speech.md).

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
