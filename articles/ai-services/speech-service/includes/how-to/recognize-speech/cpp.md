---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 10/17/2024
ms.author: pafarley
---

[!INCLUDE [Header](../../common/cpp.md)]

[!INCLUDE [Introduction](intro.md)]

## Create a speech configuration instance

To call the Speech service using the Speech SDK, you need to create a [`SpeechConfig`](/cpp/cognitive-services/speech/speechconfig) instance. This class includes information about your Speech resource, like your key and associated region, endpoint, host, or authorization token.

1. Create a Foundry resource for Speech in the [Azure portal](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry). Get the Speech resource key and endpoint.
1. Create a `SpeechConfig` instance by using the following code. Replace `YourSpeechKey` and `YourSpeechEndpoint` with your Speech resource key and endpoint.

```cpp
using namespace std;
using namespace Microsoft::CognitiveServices::Speech;

auto speechConfig = SpeechConfig::FromEndpoint("YourServiceEndpoint", "YourSpeechResoureKey");
```

You can initialize `SpeechConfig` in a few other ways:

* Use an endpoint, and pass in a Speech service endpoint. A key or authorization token is optional.
* Use a host, and pass in a host address. A key or authorization token is optional.
* Use an authorization token with the associated region/location.

> [!NOTE]
> Regardless of whether you're performing speech recognition, speech synthesis, or translation, you always create a configuration.

## Recognize speech from a microphone

To recognize speech by using your device microphone, create an [`AudioConfig`](/cpp/cognitive-services/speech/audio-audioconfig) instance by using the `FromDefaultMicrophoneInput()` member function. Then initialize the[`SpeechRecognizer`](/cpp/cognitive-services/speech/speechrecognizer) object by passing `audioConfig` and `config`.

```cpp
using namespace Microsoft::CognitiveServices::Speech::Audio;

auto audioConfig = AudioConfig::FromDefaultMicrophoneInput();
auto speechRecognizer = SpeechRecognizer::FromConfig(config, audioConfig);

cout << "Speak into your microphone." << std::endl;
auto result = speechRecognizer->RecognizeOnceAsync().get();
cout << "RECOGNIZED: Text=" << result->Text << std::endl;
```

If you want to use a *specific* audio input device, you need to specify the device ID in `AudioConfig`. To learn how to get the device ID, see [Select an audio input device with the Speech SDK](../../../how-to-select-audio-input-devices.md).

## Recognize speech from a file

If you want to recognize speech from an audio file instead of using a microphone, you still need to create an `AudioConfig` instance. However, you don't call `FromDefaultMicrophoneInput()`. You call `FromWavFileInput()` and pass the file path:

```cpp
using namespace Microsoft::CognitiveServices::Speech::Audio;

auto audioConfig = AudioConfig::FromWavFileInput("YourAudioFile.wav");
auto speechRecognizer = SpeechRecognizer::FromConfig(config, audioConfig);

auto result = speechRecognizer->RecognizeOnceAsync().get();
cout << "RECOGNIZED: Text=" << result->Text << std::endl;
```

## Recognize speech by using the Recognizer class

The [Recognizer class](/cpp/cognitive-services/speech/speechrecognizer) for the Speech SDK for C++ exposes a few methods that you can use for speech recognition.

## Single-shot recognition

Single-shot recognition asynchronously recognizes a single utterance. The end of a single utterance is determined by listening for silence at the end or until a maximum of 15 seconds of audio is processed. Here's an example of asynchronous single-shot recognition via [`RecognizeOnceAsync`](/cpp/cognitive-services/speech/speechrecognizer#recognizeonceasync):

```cpp
auto result = speechRecognizer->RecognizeOnceAsync().get();
```

You need to write some code to handle the result. This sample evaluates [`result->Reason`](/cpp/cognitive-services/speech/recognitionresult#reason) and:

* Prints the recognition result: `ResultReason::RecognizedSpeech`.
* If there's no recognition match, it informs the user: `ResultReason::NoMatch`.
* If an error is encountered, it prints the error message: `ResultReason::Canceled`.

```cpp
switch (result->Reason)
{
    case ResultReason::RecognizedSpeech:
        cout << "We recognized: " << result->Text << std::endl;
        break;
    case ResultReason::NoMatch:
        cout << "NOMATCH: Speech could not be recognized." << std::endl;
        break;
    case ResultReason::Canceled:
        {
            auto cancellation = CancellationDetails::FromResult(result);
            cout << "CANCELED: Reason=" << (int)cancellation->Reason << std::endl;
    
            if (cancellation->Reason == CancellationReason::Error) {
                cout << "CANCELED: ErrorCode= " << (int)cancellation->ErrorCode << std::endl;
                cout << "CANCELED: ErrorDetails=" << cancellation->ErrorDetails << std::endl;
                cout << "CANCELED: Did you set the speech resource key and endpoint values?" << std::endl;
            }
        }
        break;
    default:
        break;
}
```

## Continuous recognition

Continuous recognition is a bit more involved than single-shot recognition. It requires you to subscribe to the `Recognizing`, `Recognized`, and `Canceled` events to get the recognition results. To stop recognition, you must call [StopContinuousRecognitionAsync](/cpp/cognitive-services/speech/speechrecognizer#stopcontinuousrecognitionasync). Here's an example of continuous recognition performed on an audio input file.

Start by defining the input and initializing [`SpeechRecognizer`](/cpp/cognitive-services/speech/speechrecognizer):

```cpp
auto audioConfig = AudioConfig::FromWavFileInput("YourAudioFile.wav");
auto speechRecognizer = SpeechRecognizer::FromConfig(config, audioConfig);
```

Next, create a variable to manage the state of speech recognition. Declare `promise<void>` because at the start of recognition, you can safely assume that it's not finished:

```cpp
promise<void> recognitionEnd;
```

Next, subscribe to the events that [`SpeechRecognizer`](/cpp/cognitive-services/speech/speechrecognizer) sends:

* [`Recognizing`](/cpp/cognitive-services/speech/asyncrecognizer#recognizing): Signal for events that contain intermediate recognition results.
* [`Recognized`](/cpp/cognitive-services/speech/asyncrecognizer#recognized): Signal for events that contain final recognition results, which indicate a successful recognition attempt.
* [`SessionStopped`](/cpp/cognitive-services/speech/asyncrecognizer#sessionstopped): Signal for events that indicate the end of a recognition session (operation).
* [`Canceled`](/cpp/cognitive-services/speech/asyncrecognizer#canceled): Signal for events that contain canceled recognition results. These results indicate a recognition attempt that was canceled as a result of a direct cancellation request. Alternatively, they indicate a transport or protocol failure.

```cpp
speechRecognizer->Recognizing.Connect([](const SpeechRecognitionEventArgs& e)
    {
        cout << "Recognizing:" << e.Result->Text << std::endl;
    });

speechRecognizer->Recognized.Connect([](const SpeechRecognitionEventArgs& e)
    {
        if (e.Result->Reason == ResultReason::RecognizedSpeech)
        {
            cout << "RECOGNIZED: Text=" << e.Result->Text 
                 << " (text could not be translated)" << std::endl;
        }
        else if (e.Result->Reason == ResultReason::NoMatch)
        {
            cout << "NOMATCH: Speech could not be recognized." << std::endl;
        }
    });

speechRecognizer->Canceled.Connect([&recognitionEnd](const SpeechRecognitionCanceledEventArgs& e)
    {
        cout << "CANCELED: Reason=" << (int)e.Reason << std::endl;
        if (e.Reason == CancellationReason::Error)
        {
            cout << "CANCELED: ErrorCode=" << (int)e.ErrorCode << "\n"
                 << "CANCELED: ErrorDetails=" << e.ErrorDetails << "\n"
                 << "CANCELED: Did you set the speech resource key and endpoint values?" << std::endl;

            recognitionEnd.set_value(); // Notify to stop recognition.
        }
    });

speechRecognizer->SessionStopped.Connect([&recognitionEnd](const SessionEventArgs& e)
    {
        cout << "Session stopped.";
        recognitionEnd.set_value(); // Notify to stop recognition.
    });
```

With everything set up, call [`StartContinuousRecognitionAsync`](/cpp/cognitive-services/speech/speechrecognizer#startcontinuousrecognitionasync) to start recognizing:

```cpp
// Starts continuous recognition. Uses StopContinuousRecognitionAsync() to stop recognition.
speechRecognizer->StartContinuousRecognitionAsync().get();

// Waits for recognition end.
recognitionEnd.get_future().get();

// Stops recognition.
speechRecognizer->StopContinuousRecognitionAsync().get();
```

## Change the source language

A common task for speech recognition is specifying the input (or source) language. The following example shows how to change the input language to German. In your code, find your [`SpeechConfig`](/cpp/cognitive-services/speech/speechconfig) instance and add this line directly below it:

```cpp
speechConfig->SetSpeechRecognitionLanguage("de-DE");
```

[`SetSpeechRecognitionLanguage`](/cpp/cognitive-services/speech/speechconfig#setspeechrecognitionlanguage) is a parameter that takes a string as an argument. For a list of supported locales, see [Language and voice support for the Speech service](../../../language-support.md).

## Language identification

You can use language identification with speech to text recognition when you need to identify the language in an audio source and then transcribe it to text.

For a complete code sample, see [Language identification](../../../language-identification.md?pivots=programming-language-cpp).

## Use a custom endpoint

With [custom speech](../../../custom-speech-overview.md), you can upload your own data, test and train a custom model, compare accuracy between models, and deploy a model to a custom endpoint. The following example shows how to set a custom endpoint.

```cpp
auto speechConfig = SpeechConfig::FromEndpoint("YourServiceEndpoint", "YourSpeechResoureKey");
speechConfig->SetEndpointId("YourEndpointId");
auto speechRecognizer = SpeechRecognizer::FromConfig(speechConfig);
```

## Run and use a container

Speech containers provide websocket-based query endpoint APIs that are accessed through the Speech SDK and Speech CLI. By default, the Speech SDK and Speech CLI use the public Speech service. To use the container, you need to change the initialization method. Use a container host URL instead of key and endpoint.

For more information about containers, see Host URLs in [Install and run Speech containers with Docker](../../../speech-container-howto.md#host-urls).


## Semantic segmentation

Semantic segmentation is a speech recognition segmentation strategy that's designed to mitigate issues associated with silence-based segmentation: 
- Under-segmentation: When users speak for a long time without pauses, they can see a long sequence of text without breaks ("wall of text"), which severely degrades their readability experience. 
- Over-segmentation: When a user pauses for a short time, the silence detection mechanism can segment incorrectly. 

Instead of only relying on silence timeouts, semantic segmentation mostly segments and returns final results when it detects sentence-ending punctuation (such as '.' or '?'). This improves the user experience with higher-quality, semantically complete segments and prevents long intermediate results. 

To use semantic segmentation, you need to set the following property on the `SpeechConfig` instance used to create a `SpeechRecognizer`:

```cpp
speechConfig->SetProperty(PropertyId::Speech_SegmentationStrategy, "Semantic");
```

Some of the limitations of semantic segmentation are as follows:
- You need the Speech SDK version 1.41 or later to use semantic segmentation.
- Semantic segmentation is only intended for use in [continuous recognition](#continuous-recognition). This includes scenarios such as dictation and captioning. It shouldn't be used in the single recognition mode or interactive scenarios. 
- Semantic segmentation isn't available for all languages and locales. 
- Semantic segmentation doesn't yet support confidence scores and NBest lists. As such, we don't recommend semantic segmentation if you're using confidence scores or NBest lists.
