---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 01/30/2024
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
    import { readFileSync, createReadStream } from "fs";
    import { SpeechConfig, AudioConfig, ConversationTranscriber, AudioInputStream } from "microsoft-cognitiveservices-speech-sdk";
    // This example requires environment variables named "ENDPOINT" and "SPEECH_KEY"
    const speechConfig = SpeechConfig.fromEndpoint(new URL(process.env.ENDPOINT), process.env.SPEECH_KEY);
    function fromFile() {
        const filename = "katiesteve.wav";
        const audioConfig = AudioConfig.fromWavFileInput(readFileSync(filename));
        const conversationTranscriber = new ConversationTranscriber(speechConfig, audioConfig);
        const pushStream = AudioInputStream.createPushStream();
        createReadStream(filename).on('data', function (chunk) {
            pushStream.write(chunk.slice());
        }).on('end', function () {
            pushStream.close();
        });
        console.log("Transcribing from: " + filename);
        conversationTranscriber.sessionStarted = function (s, e) {
            console.log("SessionStarted event");
            console.log("SessionId:" + e.sessionId);
        };
        conversationTranscriber.sessionStopped = function (s, e) {
            console.log("SessionStopped event");
            console.log("SessionId:" + e.sessionId);
            conversationTranscriber.stopTranscribingAsync();
        };
        conversationTranscriber.canceled = function (s, e) {
            console.log("Canceled event");
            console.log(e.errorDetails);
            conversationTranscriber.stopTranscribingAsync();
        };
        conversationTranscriber.transcribed = function (s, e) {
            console.log("TRANSCRIBED: Text=" + e.result.text + " Speaker ID=" + e.result.speakerId);
        };
        // Start conversation transcription
        conversationTranscriber.startTranscribingAsync(function () { }, function (err) {
            console.trace("err - starting transcription: " + err);
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
