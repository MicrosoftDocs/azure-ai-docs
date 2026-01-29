---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 1/29/2026
ms.author: pafarley
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/csharp.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites-resourcekey-endpoint.md)]

## Set up the environment

The Speech SDK is available as a [NuGet package](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech) and implements .NET Standard 2.0. You install the Speech SDK later in this guide, but first check the [SDK installation guide](../../../quickstarts/setup-platform.md?pivots=programming-language-csharp) for any more requirements.

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables-resourcekey-endpoint.md)]

## Implement diarization from file with conversation transcription

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

1. Replace the contents of `Program.cs` with the following code.

    ```csharp
    using Microsoft.CognitiveServices.Speech;
    using Microsoft.CognitiveServices.Speech.Audio;
    using Microsoft.CognitiveServices.Speech.Transcription;
    
    class Program 
    {
        // This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
        static string speechKey = Environment.GetEnvironmentVariable("SPEECH_KEY");
        static string endpoint = Environment.GetEnvironmentVariable("ENDPOINT");
    
        async static Task Main(string[] args)
        {
            var filepath = "katiesteve.wav";
            var speechConfig = SpeechConfig.FromEndpoint(new Uri(endpoint), speechKey);        
            speechConfig.SpeechRecognitionLanguage = "en-US";
            speechConfig.SetProperty(PropertyId.SpeechServiceResponse_DiarizeIntermediateResults, "true"); 
    
            var stopRecognition = new TaskCompletionSource<int>(TaskCreationOptions.RunContinuationsAsynchronously);
    
            // Create an audio stream from a wav file or from the default microphone
            using (var audioConfig = AudioConfig.FromWavFileInput(filepath))
            {
                // Create a conversation transcriber using audio stream input
                using (var conversationTranscriber = new ConversationTranscriber(speechConfig, audioConfig))
                {
                    conversationTranscriber.Transcribing += (s, e) =>
                    {
                        Console.WriteLine($"TRANSCRIBING: Text={e.Result.Text} Speaker ID={e.Result.SpeakerId}");
                    };
    
                    conversationTranscriber.Transcribed += (s, e) =>
                    {
                        if (e.Result.Reason == ResultReason.RecognizedSpeech)
                        {
                            Console.WriteLine();
                            Console.WriteLine($"TRANSCRIBED: Text={e.Result.Text} Speaker ID={e.Result.SpeakerId}");
                            Console.WriteLine();
                        }
                        else if (e.Result.Reason == ResultReason.NoMatch)
                        {
                            Console.WriteLine($"NOMATCH: Speech could not be transcribed.");
                        }
                    };
    
                    conversationTranscriber.Canceled += (s, e) =>
                    {
                        Console.WriteLine($"CANCELED: Reason={e.Reason}");
    
                        if (e.Reason == CancellationReason.Error)
                        {
                            Console.WriteLine($"CANCELED: ErrorCode={e.ErrorCode}");
                            Console.WriteLine($"CANCELED: ErrorDetails={e.ErrorDetails}");
                            Console.WriteLine($"CANCELED: Did you set the speech resource key and endpoint values?");
                            stopRecognition.TrySetResult(0);
                        }
    
                        stopRecognition.TrySetResult(0);
                    };
    
                    conversationTranscriber.SessionStopped += (s, e) =>
                    {
                        Console.WriteLine("\n    Session stopped event.");
                        stopRecognition.TrySetResult(0);
                    };
    
                    await conversationTranscriber.StartTranscribingAsync();
    
                    // Waits for completion. Use Task.WaitAny to keep the task rooted.
                    Task.WaitAny(new[] { stopRecognition.Task });
    
                    await conversationTranscriber.StopTranscribingAsync();
                }
            }
        }
    }
    ```

1. Get the [sample audio file](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/sampledata/audiofiles/katiesteve.wav) or use your own `.wav` file. Replace `katiesteve.wav` with the path and name of your `.wav` file.

   The application recognizes speech from multiple participants in the conversation. Your audio file should contain multiple speakers.

1. To change the speech recognition language, replace `en-US` with another [supported language](/azure/cognitive-services/speech-service/supported-languages). For example, `es-ES` for Spanish (Spain). The default language is `en-US` if you don't specify a language. For details about how to identify one of multiple languages that might be spoken, see [language identification](/azure/cognitive-services/speech-service/language-identification).

1. Run your console application to start conversation transcription:

   ```dotnetcli
   dotnet run
   ```

> [!IMPORTANT]
> Make sure that you set the `SPEECH_KEY` and `ENDPOINT` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

The transcribed conversation should be output as text:

```output
TRANSCRIBING: Text=good morning steve Speaker ID=Unknown
TRANSCRIBING: Text=good morning steve how are Speaker ID=Guest-1
TRANSCRIBING: Text=good morning steve how are you doing today Speaker ID=Guest-1

TRANSCRIBED: Text=Good morning, Steve. How are you doing today? Speaker ID=Guest-1

TRANSCRIBING: Text=good morning katie Speaker ID=Unknown
TRANSCRIBING: Text=good morning katie i hope Speaker ID=Guest-2
TRANSCRIBING: Text=good morning katie i hope you're having a great Speaker ID=Guest-2
TRANSCRIBING: Text=good morning katie i hope you're having a great start to Speaker ID=Guest-2
TRANSCRIBING: Text=good morning katie i hope you're having a great start to your day Speaker ID=Guest-2

TRANSCRIBED: Text=Good morning, Katie. I hope you're having a great start to your day. Speaker ID=Guest-2

TRANSCRIBING: Text=have you tried Speaker ID=Unknown
TRANSCRIBING: Text=have you tried the latest Speaker ID=Unknown
TRANSCRIBING: Text=have you tried the latest real time Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can tell you Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said what Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said what in Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said what in real time Speaker ID=Guest-1

TRANSCRIBED: Text=Have you tried the latest real time diarization in Microsoft Speech Service which can tell you who said what in real time? Speaker ID=Guest-1

TRANSCRIBING: Text=not yet Speaker ID=Unknown
TRANSCRIBING: Text=not yet i Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch trans Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization Speaker ID=Guest-2  
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization function Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produc Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces di Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature Speaker ID=Guest-2  
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to di Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to diarize Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to diarize in real Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to diarize in real time Speaker ID=Guest-2

TRANSCRIBED: Text=Not yet. I've been using the batch transcription with diarization functionality, but it produces diarization results after the whole audio is processed. Is the new feature able to diarize in real time? Speaker ID=Guest-2

TRANSCRIBING: Text=absolutely Speaker ID=Unknown
TRANSCRIBING: Text=absolutely i Speaker ID=Unknown
TRANSCRIBING: Text=absolutely i recom Speaker ID=Guest-1
TRANSCRIBING: Text=absolutely i recommend Speaker ID=Guest-1
TRANSCRIBING: Text=absolutely i recommend you give it a try Speaker ID=Guest-1

TRANSCRIBED: Text=Absolutely, I recommend you give it a try. Speaker ID=Guest-1

TRANSCRIBING: Text=that's exc Speaker ID=Unknown
TRANSCRIBING: Text=that's exciting Speaker ID=Unknown
TRANSCRIBING: Text=that's exciting let me try Speaker ID=Guest-2
TRANSCRIBING: Text=that's exciting let me try it right now Speaker ID=Guest-2

TRANSCRIBED: Text=That's exciting. Let me try it right now. Speaker ID=Guest-2
```

Speakers are identified as Guest-1, Guest-2, and so on, depending on the number of speakers in the conversation. 

> [!NOTE]
> You might see `Speaker ID=Unknown` in some of the early intermediate results when the speaker isn't yet identified. Without intermediate diarization results (if you don't set the `PropertyId.SpeechServiceResponse_DiarizeIntermediateResults` property to "true"), the speaker ID is always "Unknown."

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
