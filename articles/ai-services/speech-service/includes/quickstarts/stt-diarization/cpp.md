---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 7/16/2025
ms.author: pafarley
---

[!INCLUDE [Header](../../common/cpp.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites-resourcekey-endpoint.md)]

## Set up the environment

The Speech SDK is available as a [NuGet package](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech) and implements .NET Standard 2.0. You install the Speech SDK later in this guide, but first check the [SDK installation guide](../../../quickstarts/setup-platform.md?pivots=programming-language-cpp) for any more requirements.

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables-resourcekey-endpoint.md)]

## Implement diarization from file with conversation transcription

Follow these steps to create a console application and install the Speech SDK.

1. Create a new C++ console project in [Visual Studio Community 2022](https://visualstudio.microsoft.com/downloads/) named `ConversationTranscription`.

1. Select **Tools** > **Nuget Package Manager** > **Package Manager Console**. In the **Package Manager Console**, run this command:

    ```console
    Install-Package Microsoft.CognitiveServices.Speech
    ```

1. Replace the contents of `ConversationTranscription.cpp` with the following code.

    ```cpp
    #include <iostream> 
    #include <stdlib.h>
    #include <speechapi_cxx.h>
    #include <future>

    using namespace Microsoft::CognitiveServices::Speech;
    using namespace Microsoft::CognitiveServices::Speech::Audio;
    using namespace Microsoft::CognitiveServices::Speech::Transcription;

    std::string GetEnvironmentVariable(const char* name);

    int main()
    {
        // This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
        auto speechKey = GetEnvironmentVariable("SPEECH_KEY");
        auto endpoint = GetEnvironmentVariable("ENDPOINT");

        if (std::string(speechKey).empty() || std::string(endpoint).empty()) {
            std::cout << "Please set both SPEECH_KEY and ENDPOINT environment variables." << std::endl;
            return -1;
        }

        auto speechConfig = SpeechConfig::FromEndpoint(endpoint, speechKey);
        speechConfig->SetProperty(PropertyId::SpeechServiceResponse_DiarizeIntermediateResults, "true"); 

        speechConfig->SetSpeechRecognitionLanguage("en-US");

        auto audioConfig = AudioConfig::FromWavFileInput("katiesteve.wav");
        auto conversationTranscriber = ConversationTranscriber::FromConfig(speechConfig, audioConfig);

        // promise for synchronization of recognition end.
        std::promise<void> recognitionEnd;

        // Subscribes to events.
        conversationTranscriber->Transcribing.Connect([](const ConversationTranscriptionEventArgs& e)
            {
                std::cout << "TRANSCRIBING:" << e.Result->Text << std::endl;
                std::cout << "Speaker ID=" << e.Result->SpeakerId << std::endl;
            });

        conversationTranscriber->Transcribed.Connect([](const ConversationTranscriptionEventArgs& e)
            {
                if (e.Result->Reason == ResultReason::RecognizedSpeech)
                {
                    std::cout << "\n" << "TRANSCRIBED: Text=" << e.Result->Text << std::endl;
                    std::cout << "Speaker ID=" << e.Result->SpeakerId << "\n" << std::endl;
                }
                else if (e.Result->Reason == ResultReason::NoMatch)
                {
                    std::cout << "NOMATCH: Speech could not be transcribed." << std::endl;
                }
            });

        conversationTranscriber->Canceled.Connect([&recognitionEnd](const ConversationTranscriptionCanceledEventArgs& e)
            {
                auto cancellation = CancellationDetails::FromResult(e.Result);
                std::cout << "CANCELED: Reason=" << (int)cancellation->Reason << std::endl;

                if (cancellation->Reason == CancellationReason::Error)
                {
                    std::cout << "CANCELED: ErrorCode=" << (int)cancellation->ErrorCode << std::endl;
                    std::cout << "CANCELED: ErrorDetails=" << cancellation->ErrorDetails << std::endl;
                    std::cout << "CANCELED: Did you set the speech resource key and endpoint values?" << std::endl;
                }
                else if (cancellation->Reason == CancellationReason::EndOfStream)
                {
                    std::cout << "CANCELED: Reach the end of the file." << std::endl;
                }
            });

        conversationTranscriber->SessionStopped.Connect([&recognitionEnd](const SessionEventArgs& e)
            {
                std::cout << "Session stopped.";
                recognitionEnd.set_value(); // Notify to stop recognition.
            });

        conversationTranscriber->StartTranscribingAsync().wait();

        // Waits for recognition end.
        recognitionEnd.get_future().wait();

        conversationTranscriber->StopTranscribingAsync().wait();
    }

    std::string GetEnvironmentVariable(const char* name)
    {
    #if defined(_MSC_VER)
        size_t requiredSize = 0;
        (void)getenv_s(&requiredSize, nullptr, 0, name);
        if (requiredSize == 0)
        {
            return "";
        }
        auto buffer = std::make_unique<char[]>(requiredSize);
        (void)getenv_s(&requiredSize, buffer.get(), requiredSize, name);
        return buffer.get();
    #else
        auto value = getenv(name);
        return value ? value : "";
    #endif
    }
    ```

1. Get the [sample audio file](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/sampledata/audiofiles/katiesteve.wav) or use your own `.wav` file. Replace `katiesteve.wav` with the path and name of your `.wav` file.

   The application recognizes speech from multiple participants in the conversation. Your audio file should contain multiple speakers.

1. To change the speech recognition language, replace `en-US` with another [supported language](/azure/cognitive-services/speech-service/supported-languages). For example, `es-ES` for Spanish (Spain). The default language is `en-US` if you don't specify a language. For details about how to identify one of multiple languages that might be spoken, see [language identification](/azure/cognitive-services/speech-service/language-identification).

1. To start conversation transcription, [Build and run](/cpp/build/vscpp-step-2-build) your application:

   > [!IMPORTANT]
   > Make sure that you set the `SPEECH_KEY` and `ENDPOINT` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

The transcribed conversation should be output as text:

```output
TRANSCRIBING:good morning
Speaker ID=Unknown
TRANSCRIBING:good morning steve
Speaker ID=Unknown
TRANSCRIBING:good morning steve how are you doing
Speaker ID=Guest-1
TRANSCRIBING:good morning steve how are you doing today
Speaker ID=Guest-1

TRANSCRIBED: Text=Good morning, Steve. How are you doing today?
Speaker ID=Guest-1

TRANSCRIBING:good
Speaker ID=Unknown
TRANSCRIBING:good morning
Speaker ID=Unknown
TRANSCRIBING:good morning kat
Speaker ID=Unknown
TRANSCRIBING:good morning katie i hope you're having a
Speaker ID=Guest-2
TRANSCRIBING:good morning katie i hope you're having a great start to your day
Speaker ID=Guest-2

TRANSCRIBED: Text=Good morning, Katie. I hope you're having a great start to your day.
Speaker ID=Guest-2

TRANSCRIBING:have you
Speaker ID=Unknown
TRANSCRIBING:have you tried
Speaker ID=Unknown
TRANSCRIBING:have you tried the latest
Speaker ID=Unknown
TRANSCRIBING:have you tried the latest real
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization in
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization in microsoft
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization in microsoft speech
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization in microsoft speech service
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization in microsoft speech service which
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization in microsoft speech service which can
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization in microsoft speech service which can tell you
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization in microsoft speech service which can tell you who said
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization in microsoft speech service which can tell you who said what
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization in microsoft speech service which can tell you who said what in
Speaker ID=Guest-1
TRANSCRIBING:have you tried the latest real time diarization in microsoft speech service which can tell you who said what in real time
Speaker ID=Guest-1

TRANSCRIBED: Text=Have you tried the latest real time diarization in Microsoft Speech Service which can tell you who said what in real time?
Speaker ID=Guest-1

TRANSCRIBING:not yet
Speaker ID=Unknown
TRANSCRIBING:not yet i
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch trans
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization function
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces di
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to di
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to diarize
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to diarize in real
Speaker ID=Guest-2
TRANSCRIBING:not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to diarize in real time
Speaker ID=Guest-2

TRANSCRIBED: Text=Not yet. I've been using the batch transcription with diarization functionality, but it produces diarization results after the whole audio is processed. Is the new feature able to diarize in real time?
Speaker ID=Guest-2

TRANSCRIBING:absolutely
Speaker ID=Unknown
TRANSCRIBING:absolutely i
Speaker ID=Unknown
TRANSCRIBING:absolutely i recom
Speaker ID=Guest-1
TRANSCRIBING:absolutely i recommend
Speaker ID=Guest-1
TRANSCRIBING:absolutely i recommend you
Speaker ID=Guest-1
TRANSCRIBING:absolutely i recommend you give it a try
Speaker ID=Guest-1

TRANSCRIBED: Text=Absolutely, I recommend you give it a try.
Speaker ID=Guest-1

TRANSCRIBING:that's exc
Speaker ID=Unknown
TRANSCRIBING:that's exciting
Speaker ID=Unknown
TRANSCRIBING:that's exciting let me
Speaker ID=Guest-2
TRANSCRIBING:that's exciting let me try
Speaker ID=Guest-2
TRANSCRIBING:that's exciting let me try it right now
Speaker ID=Guest-2

TRANSCRIBED: Text=That's exciting. Let me try it right now.
Speaker ID=Guest-2
```

Speakers are identified as Guest-1, Guest-2, and so on, depending on the number of speakers in the conversation.

> [!NOTE]
> You might see `Speaker ID=Unknown` in some of the early intermediate results when the speaker isn't yet identified. Without intermediate diarization results (if you don't set the `PropertyId::SpeechServiceResponse_DiarizeIntermediateResults` property to "true"), the speaker ID is always "Unknown."

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]

