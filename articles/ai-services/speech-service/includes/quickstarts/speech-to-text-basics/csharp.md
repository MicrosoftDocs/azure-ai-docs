---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 01/30/2024
ms.author: eur
---

[!INCLUDE [Header](../../common/csharp.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

## Set up the environment

The Speech SDK is available as a [NuGet package](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech) and implements .NET Standard 2.0. You install the Speech SDK later in this guide. For any other requirements, see [Install the Speech SDK](../../../quickstarts/setup-platform.md?pivots=programming-language-csharp).

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables.md)]

## Recognize speech from a microphone

> [!TIP]
> Try out the [Azure AI Speech Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-azureaispeech.azure-ai-speech-toolkit) to easily build and run samples on Visual Studio Code.

Follow these steps to create a console application and install the Speech SDK.

1. Open a command prompt window in the folder where you want the new project. Run this command to create a console application with the .NET CLI.

   ```dotnetcli
   dotnet new console
   ```

   This command creates the *Program.cs* file in your project directory.

1. Install the Speech SDK in your new project with the .NET CLI.

   ```dotnetcli
   dotnet add package Microsoft.CognitiveServices.Speech
   ```

1. Replace the contents of *Program.cs* with the following code:

   ```csharp
   using System;
   using System.IO;
   using System.Threading.Tasks;
   using Microsoft.CognitiveServices.Speech;
   using Microsoft.CognitiveServices.Speech.Audio;

   class Program 
   {
       // This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
       static string speechKey = Environment.GetEnvironmentVariable("SPEECH_KEY");
       static string speechRegion = Environment.GetEnvironmentVariable("SPEECH_REGION");

       static void OutputSpeechRecognitionResult(SpeechRecognitionResult speechRecognitionResult)
       {
           switch (speechRecognitionResult.Reason)
           {
               case ResultReason.RecognizedSpeech:
                   Console.WriteLine($"RECOGNIZED: Text={speechRecognitionResult.Text}");
                   break;
               case ResultReason.NoMatch:
                   Console.WriteLine($"NOMATCH: Speech could not be recognized.");
                   break;
               case ResultReason.Canceled:
                   var cancellation = CancellationDetails.FromResult(speechRecognitionResult);
                   Console.WriteLine($"CANCELED: Reason={cancellation.Reason}");

                   if (cancellation.Reason == CancellationReason.Error)
                   {
                       Console.WriteLine($"CANCELED: ErrorCode={cancellation.ErrorCode}");
                       Console.WriteLine($"CANCELED: ErrorDetails={cancellation.ErrorDetails}");
                       Console.WriteLine($"CANCELED: Did you set the speech resource key and region values?");
                   }
                   break;
           }
       }

       async static Task Main(string[] args)
       {
           var speechConfig = SpeechConfig.FromSubscription(speechKey, speechRegion);        
           speechConfig.SpeechRecognitionLanguage = "en-US";

           using var audioConfig = AudioConfig.FromDefaultMicrophoneInput();
           using var speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);

           Console.WriteLine("Speak into your microphone.");
           var speechRecognitionResult = await speechRecognizer.RecognizeOnceAsync();
           OutputSpeechRecognitionResult(speechRecognitionResult);
       }
   }
   ```

1. To change the speech recognition language, replace `en-US` with another [supported language](~/articles/ai-services/speech-service/language-support.md). For example, use `es-ES` for Spanish (Spain). If you don't specify a language, the default is `en-US`. For details about how to identify one of multiple languages that might be spoken, see [Language identification](~/articles/ai-services/speech-service/language-identification.md).

1. Run your new console application to start speech recognition from a microphone:

   ```console
   dotnet run
   ```

   > [!IMPORTANT]
   > Make sure that you set the `SPEECH_KEY` and `SPEECH_REGION` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

1. Speak into your microphone when prompted. What you speak should appear as text:

   ```output
   Speak into your microphone.
   RECOGNIZED: Text=I'm excited to try speech to text.
   ```

## Remarks

Here are some other considerations:

- This example uses the `RecognizeOnceAsync` operation to transcribe utterances of up to 30 seconds, or until silence is detected. For information about continuous recognition for longer audio, including multi-lingual conversations, see [How to recognize speech](~/articles/ai-services/speech-service/how-to-recognize-speech.md).
- To recognize speech from an audio file, use `FromWavFileInput` instead of `FromDefaultMicrophoneInput`:

   ```csharp
   using var audioConfig = AudioConfig.FromWavFileInput("YourAudioFile.wav");
   ```

- For compressed audio files such as MP4, install GStreamer and use `PullAudioInputStream` or `PushAudioInputStream`. For more information, see [How to use compressed input audio](~/articles/ai-services/speech-service/how-to-use-codec-compressed-audio-input-streams.md).

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
