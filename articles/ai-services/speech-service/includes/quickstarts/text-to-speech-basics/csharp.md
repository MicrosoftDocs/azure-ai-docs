---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 8/07/2024
ms.author: eur
---

[!INCLUDE [Header](../../common/csharp.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites-resourcekey-endpoint.md)]

## Set up the environment

The Speech SDK is available as a [NuGet package](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech) that implements .NET Standard 2.0. Install the Speech SDK later in this guide by using the console. For detailed installation instructions, see [Install the Speech SDK](../../../quickstarts/setup-platform.md?pivots=programming-language-csharp).

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables-resourcekey-endpoint.md)]

## Create the application

Follow these steps to create a console application and install the Speech SDK.

1. Open a command prompt window in the folder where you want the new project. Run this command to create a console application with the .NET CLI.

   ```dotnetcli
   dotnet new console
   ```

   The command creates a *Program.cs* file in the project directory.

1. Install the Speech SDK in your new project with the .NET CLI.

   ```dotnetcli
   dotnet add package Microsoft.CognitiveServices.Speech
   ```

1. Replace the contents of *Program.cs* with the following code.

    ```csharp
    using System;
    using System.IO;
    using System.Threading.Tasks;
    using Microsoft.CognitiveServices.Speech;
    using Microsoft.CognitiveServices.Speech.Audio;
        
    class Program 
    {
        // This example requires environment variables named "SPEECH_KEY" and "END_POINT"
        static string speechKey = Environment.GetEnvironmentVariable("SPEECH_KEY");
        static string endpoint = Environment.GetEnvironmentVariable("END_POINT");

        static void OutputSpeechSynthesisResult(SpeechSynthesisResult speechSynthesisResult, string text)
        {
            switch (speechSynthesisResult.Reason)
            {
                case ResultReason.SynthesizingAudioCompleted:
                    Console.WriteLine($"Speech synthesized for text: [{text}]");
                    break;
                case ResultReason.Canceled:
                    var cancellation = SpeechSynthesisCancellationDetails.FromResult(speechSynthesisResult);
                    Console.WriteLine($"CANCELED: Reason={cancellation.Reason}");
    
                    if (cancellation.Reason == CancellationReason.Error)
                    {
                        Console.WriteLine($"CANCELED: ErrorCode={cancellation.ErrorCode}");
                        Console.WriteLine($"CANCELED: ErrorDetails=[{cancellation.ErrorDetails}]");
                        Console.WriteLine($"CANCELED: Did you set the speech resource key and endpoint values?");
                    }
                    break;
                default:
                    break;
            }
        }
    
        async static Task Main(string[] args)
        {
            var speechConfig = SpeechConfig.FromEndpoint(speechKey, endpoint); 
    
            // The neural multilingual voice can speak different languages based on the input text.
            speechConfig.SpeechSynthesisVoiceName = "en-US-AvaMultilingualNeural"; 
    
            using (var speechSynthesizer = new SpeechSynthesizer(speechConfig))
            {
                // Get text from the console and synthesize to the default speaker.
                Console.WriteLine("Enter some text that you want to speak >");
                string text = Console.ReadLine();
    
                var speechSynthesisResult = await speechSynthesizer.SpeakTextAsync(text);
                OutputSpeechSynthesisResult(speechSynthesisResult, text);
            }
    
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
    ```

1. To change the speech synthesis language, replace `en-US-AvaMultilingualNeural` with another [supported voice](~/articles/ai-services/speech-service/language-support.md#standard-voices).

   All neural voices are multilingual and fluent in their own language and English. For example, if the input text in English is *I'm excited to try text to speech* and you set `es-ES-ElviraNeural` as the language, the text is spoken in English with a Spanish accent. If the voice doesn't speak the language of the input text, the Speech service doesn't output synthesized audio.

1. Run your new console application to start speech synthesis to the default speaker.

   ```console
   dotnet run
   ```

   > [!IMPORTANT]
   > Make sure that you set the `SPEECH_KEY` and `END_POINT` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

1. Enter some text that you want to speak. For example, type *I'm excited to try text to speech*. Select the **Enter** key to hear the synthesized speech.

   ```console
   Enter some text that you want to speak >
   I'm excited to try text to speech
   ```

## Remarks

### More speech synthesis options

This quickstart uses the `SpeakTextAsync` operation to synthesize a short block of text that you enter. You can also use long-form text from a file and get finer control over voice styles, prosody, and other settings.

- See [how to synthesize speech](~/articles/ai-services/speech-service/how-to-speech-synthesis.md) and [Speech Synthesis Markup Language (SSML) overview](~/articles/ai-services/speech-service/speech-synthesis-markup.md) for information about speech synthesis from a file and finer control over voice styles, prosody, and other settings.
- See [batch synthesis API for text to speech](~/articles/ai-services/speech-service/batch-synthesis.md) for information about synthesizing long-form text to speech.

### OpenAI text to speech voices in Azure AI Speech

OpenAI text to speech voices are also supported. See [OpenAI text to speech voices in Azure AI Speech](../../../openai-voices.md) and [multilingual voices](../../../language-support.md?tabs=tts#multilingual-voices). You can replace `en-US-AvaMultilingualNeural` with a supported OpenAI voice name such as `en-US-FableMultilingualNeural`.

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
