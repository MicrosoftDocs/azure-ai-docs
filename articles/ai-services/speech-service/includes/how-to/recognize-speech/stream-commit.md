---
author: KunCong
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 09/26/2026
ms.author: kuncong
ai-usage: ai-assisted
---

## Commit an explicit audio boundary (preview)

When you stream audio to Azure Speech Service, the service automatically segments the audio and generates transcription results accordingly. However, in certain scenarios, such as turn-based voice agents, you might need to explicitly define boundaries in the transcription stream. You can now achieve this goal by using the `Commit()` method of `PushAudioInputStream`.

Using an explicit audio boundary requires Speech SDK version 1.52 or later. It also requires the service property `setfeature=forcecommit` to be enabled.

During public preview, the following limitations apply:

- Only PCM, A-law, μ-law, and G.711 audio formats are supported. Other compressed audio formats aren't supported.
- Microsoft Audio Stack (MAS) isn't supported.

::: zone pivot="programming-language-csharp"

Create a `PushAudioInputStream` and use it with `SpeechRecognizer`. 

```csharp
var config = SpeechConfig.FromEndpoint(new Uri(endpoint), subscriptionKey);
config.SpeechRecognitionLanguage = "en-US";
config.SetServiceProperty("setfeature", "forcecommit", ServicePropertyChannel.UriQueryParameter);
var pushStream = AudioInputStream.CreatePushStream();
var audioInput = AudioConfig.FromStreamInput(pushStream);
var recognizer = new SpeechRecognizer(config, audioInput);
```

Use `PushAudioInputStream.Commit()` to commit audio boundary. A token is returned.

```csharp
// writing audio
pushStream.Write(audioBytes);

// ...

// commit audio boundary
var token = pushStream.Commit();

```

Use `SpeechRecognitionResult.CommitToken` to identify the result from `Recognized` event that matches the commit.

```csharp
recognizer.Recognized += (s, e) =>
{
    var token = e.Result.CommitToken;
    var tokenText = token != 0 ? $" commit_token={token}" : "";
    Console.WriteLine($"RECOGNIZED: Reason={e.Result.Reason} Text={e.Result.Text}{tokenText}");
};
```

You can find the complete sample in `RecognitionWithPushStreamCommitAsync` in Speech SDK samples [on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/csharp/sharedcontent/console/speech_recognition_samples.cs).


::: zone-end

::: zone pivot="programming-language-cpp"

Create a `PushAudioInputStream` and use it with `SpeechRecognizer`. 

```cpp
auto config = SpeechConfig::FromEndpoint(endpoint, subscriptionKey);
config->SetSpeechRecognitionLanguage("en-US");
config->SetServiceProperty("setfeature", "forcecommit", ServicePropertyChannel::UriQueryParameter);
auto pushStream = AudioInputStream::CreatePushStream();
auto recognizer = SpeechRecognizer::FromConfig(config, AudioConfig::FromStreamInput(pushStream));
```

Use `PushAudioInputStream::Commit()` to commit audio boundary. A token is returned.

```cpp
// vector<uint8_t> audioBytes(3200);
// ... read audio into audioBytes
// writing audio
pushStream->Write(audioBytes.data(),static_cast<uint32_t>(audioBytes.size()));

// ...

// commit audio boundary
uint32_t token = pushStream->Commit();

```

Use `SpeechRecognitionResult::CommitToken()` to identify the result from `Recognized` event that matches the commit.

```cpp
recognizer->Recognized.Connect([&](const SpeechRecognitionEventArgs& e)
{
    cout << "RECOGNIZED: Reason=" << (int)e.Result->Reason << " Text=" << e.Result->Text;
    // NoMatch can acknowledge a commit; naturally segmented results have token 0.
    if (e.Result->CommitToken() != 0)
    {
        uint32_t acknowledgedToken = e.Result->CommitToken();
        cout << " commit_token=" << acknowledgedToken;
    }
    cout << endl;
});
```

You can find the complete sample in `SpeechRecognitionWithPushStreamCommit` in Speech SDK samples [on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/cpp/windows/console/samples/speech_recognition_samples.cpp).


::: zone-end

::: zone pivot="programming-language-java"

Create a `PushAudioInputStream` and use it with `SpeechRecognizer`. 

```java
SpeechConfig config = SpeechConfig.fromEndpoint(new URI(endpoint), subscriptionKey);
config.setSpeechRecognitionLanguage("en-US");
config.setServiceProperty("setfeature", "forcecommit", ServicePropertyChannel.UriQueryParameter);
PushAudioInputStream pushStream = AudioInputStream.createPushStream();
AudioConfig audioInput = AudioConfig.fromStreamInput(pushStream);
SpeechRecognizer recognizer = new SpeechRecognizer(config, audioInput);
```

Use `PushAudioInputStream.commit()` to commit audio boundary. A token is returned.

```java
// writing audio
pushStream.write(audioBytes);

// ...

// commit audio boundary
int token = pushStream.commit();

```

Use `SpeechRecognitionResult.getCommitToken()` to identify the result from `recognized` event that matches the commit.

```java
recognizer.recognized.addEventListener((s, e) -> {
    int acknowledgedToken = e.getResult().getCommitToken();
    String tokenText = acknowledgedToken != 0 ? " commit_token=" + acknowledgedToken : "";
    System.out.println("RECOGNIZED: Reason=" + e.getResult().getReason()
        + " Text=" + e.getResult().getText() + tokenText);
});
```

You can find the complete sample in `recognitionWithPushStreamCommitAsync` in Speech SDK samples [on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/java/jre/console/src/com/microsoft/cognitiveservices/speech/samples/console/SpeechRecognitionSamples.java).


::: zone-end

::: zone pivot="programming-language-python"

Create a `PushAudioInputStream` and use it with `SpeechRecognizer`. 

```python
speech_config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=speech_endpoint)
speech_config.speech_recognition_language = "en-US"

speech_config.set_service_property(
    "setfeature", "forcecommit", speechsdk.ServicePropertyChannel.UriQueryParameter)

pushStream = speechsdk.audio.PushAudioInputStream()
audio_config = speechsdk.audio.AudioConfig(stream=pushStream)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
```

Use `PushAudioInputStream.commit()` to commit audio boundary. A token is returned.

```python
# writing audio
pushStream.write(audio)

# ...

# commit audio boundary
token = pushStream.commit()
```

Use `SpeechRecognitionResult.commit_token` to identify the result from `recognized` event that matches the commit.

```python
def recognized_cb(evt):
    result = evt.result
    commit_info = " commit_token={}".format(result.commit_token) if result.commit_token != 0 else ""
    print("RECOGNIZED: reason={} text={}{}".format(result.reason, result.text, commit_info))

speech_recognizer.recognized.connect(recognized_cb)
```

You can find the complete sample in `speech_recognition_with_push_stream_commit` in Speech SDK samples [on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/python/console/speech_sample.py).

::: zone-end