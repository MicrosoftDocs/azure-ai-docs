---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 01/30/2024
ms.author: eur
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

1. Install the Speech SDK for JavaScript with:

    ```console
    npm install microsoft-cognitiveservices-speech-sdk
    ```

### Retrieve resource information

[!INCLUDE [Environment variables](../../common/environment-variables.md)]

## Recognize speech from a file

To transcribe speech from a file:

1. Create a new file named *transcription.js* with the following content:

    ```javascript
    import { readFileSync } from "fs";
    import { SpeechConfig, AudioConfig, SpeechRecognizer, ResultReason, CancellationDetails, CancellationReason } from "microsoft-cognitiveservices-speech-sdk";
    // This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    const speechConfig = SpeechConfig.fromSubscription(process.env.SPEECH_KEY, process.env.SPEECH_REGION);
    speechConfig.speechRecognitionLanguage = "en-US";
    function fromFile() {
        const audioConfig = AudioConfig.fromWavFileInput(readFileSync("YourAudioFile.wav"));
        const speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
        speechRecognizer.recognizeOnceAsync((result) => {
            switch (result.reason) {
                case ResultReason.RecognizedSpeech:
                    console.log(`RECOGNIZED: Text=${result.text}`);
                    break;
                case ResultReason.NoMatch:
                    console.log("NOMATCH: Speech could not be recognized.");
                    break;
                case ResultReason.Canceled:
                    const cancellation = CancellationDetails.fromResult(result);
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

    In *transcription.js*, replace *YourAudioFile.wav* with your own *.wav* file. This example only recognizes speech from a *.wav* file. For information about other audio formats, see [How to use compressed input audio](~/articles/ai-services/speech-service/how-to-use-codec-compressed-audio-input-streams.md). This example supports up to 30 seconds of audio.

    To change the speech recognition language, replace `en-US` with another [supported language](~/articles/ai-services/speech-service/language-support.md). For example, use `es-ES` for Spanish (Spain). If you don't specify a language, the default is `en-US`. For details about how to identify one of multiple languages that might be spoken, see [Language identification](~/articles/ai-services/speech-service/language-identification.md).

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

> [!NOTE]
> Recognizing speech from a microphone is not supported in Node.js. It's supported only in a browser-based JavaScript environment. For more information, see the [React sample](https://github.com/Azure-Samples/AzureSpeechReactSample) and the [implementation of speech to text from a microphone](https://github.com/Azure-Samples/AzureSpeechReactSample/blob/main/src/App.js#L29) on GitHub.
> 
> The React sample shows design patterns for the exchange and management of authentication tokens. It also shows the capture of audio from a microphone or file for speech to text conversions.

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
