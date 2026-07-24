---
title: Embedded Speech - Speech service
titleSuffix: Foundry Tools
description: Embedded Speech is designed for on-device scenarios where cloud connectivity is intermittent or unavailable.
author: PatrickFarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.custom: devx-track-extended-java
ms.topic: how-to
ms.date: 07/01/2026
ms.author: pafarley
zone_pivot_groups: programming-languages-speech-services-embedded
ai-usage: ai-assisted
---

# What is embedded speech?

Embedded Speech is designed for on-device [speech to text](speech-to-text.md) and [text to speech](text-to-speech.md) scenarios where cloud connectivity is intermittent or unavailable. For example, you can use embedded speech in industrial equipment, a voice enabled air conditioning unit, or a car that might travel out of range. You can also develop hybrid cloud and offline solutions. For scenarios where your devices must be in a secure environment like a bank or government entity, you should first consider [disconnected containers](../containers/disconnected-containers.md).

> [!IMPORTANT]
> Microsoft limits access to embedded speech. You can apply for access through the Azure Speech in Foundry Tools [embedded speech limited access review](https://aka.ms/csgate-embedded-speech). For more information, see [Limited access for embedded speech](/azure/ai-foundry/responsible-ai/speech-service/embedded-speech/limited-access-embedded-speech).

## Platform requirements

Embedded speech is included with the Speech SDK (version 1.24.1 and higher) for C#, C++, and Java, and with the Speech SDK for Python (version 1.51.0 and higher). Refer to the general [Speech SDK installation requirements](quickstarts/setup-platform.md#platform-requirements) for programming language and target platform specific details.

Embedded speech with the Speech SDK for Python is supported on Windows (x64, Arm64), Linux (x64, Arm64), and macOS (x64, Arm64). Python doesn't support embedded speech on Android.

Embedded speech with the Speech SDK for Go (version 1.51.0 and higher) is supported on Linux (x64, Arm64, Arm32). Go doesn't support embedded speech on Android.

The following are general estimates of memory consumption with embedded speech. The final numbers depend on feature configuration.
* Speech recognition or translation: Total size of the files of a model + 200 MB.
* Speech synthesis: 100-200 MB depending on the locale.

**Choose your target environment**

# [Android](#tab/android-target)

Requires Android 8.0 (API level 26) or higher on Arm64 (`arm64-v8a`) or Arm32 (`armeabi-v7a`) hardware.

# [Linux](#tab/linux-target)

Requires Linux on x64, Arm64, or Arm32 hardware with [supported Linux distributions](quickstarts/setup-platform.md?tabs=linux).

Embedded TTS with neural voices isn't supported on Linux Arm32.

# [macOS](#tab/macos-target)

Requires 10.14 or newer on x64 or Arm64 hardware.

# [Windows](#tab/windows-target)

Requires Windows 11 or newer on x64 or Arm64 hardware.

The latest [Microsoft Visual C++ Redistributable for Visual Studio 2015-2022](/cpp/windows/latest-supported-vc-redist?view=msvc-170&preserve-view=true) must be installed regardless of the programming language used with the Speech SDK.

The Speech SDK for Java doesn't support Windows on Arm64.

---


## Limitations

- Only the C#, C++, Java, Python, and Go SDKs support embedded speech. The other Speech SDKs, Speech CLI, and REST APIs don't support embedded speech.
- The Speech SDK for Python and the Speech SDK for Go don't support hybrid speech (`HybridSpeechConfig`). Use the C#, C++, or Java SDK for hybrid scenarios.
- Embedded speech recognition only supports mono 16 bit, 8-kHz or 16-kHz PCM-encoded WAV audio formats.
- Embedded neural voices support 16 or 24 kHz RIFF/RAW.

## Embedded speech SDK packages

::: zone pivot="programming-language-csharp"

For C# embedded applications, install following Speech SDK for C# packages:

|Package  |Description  |
| --------- | --------- |
|[Microsoft.CognitiveServices.Speech](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech)|Required to use the Speech SDK|
| [Microsoft.CognitiveServices.Speech.Extension.Embedded.SR](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech.Extension.Embedded.SR) | Required for embedded speech recognition |
| [Microsoft.CognitiveServices.Speech.Extension.Embedded.TTS](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech.Extension.Embedded.TTS) | Required for embedded speech synthesis |
| [Microsoft.CognitiveServices.Speech.Extension.ONNX.Runtime](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech.Extension.ONNX.Runtime) | Required for embedded speech recognition and synthesis |
| [Microsoft.CognitiveServices.Speech.Extension.Telemetry](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech.Extension.Telemetry) | Required for embedded speech recognition and synthesis |

::: zone-end

::: zone pivot="programming-language-cpp"

For C++ embedded applications, install following Speech SDK for C++ packages:

|Package  |Description  |
| --------- | --------- |
|[Microsoft.CognitiveServices.Speech](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech)|Required to use the Speech SDK|
| [Microsoft.CognitiveServices.Speech.Extension.Embedded.SR](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech.Extension.Embedded.SR) | Required for embedded speech recognition |
| [Microsoft.CognitiveServices.Speech.Extension.Embedded.TTS](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech.Extension.Embedded.TTS) | Required for embedded speech synthesis |
| [Microsoft.CognitiveServices.Speech.Extension.ONNX.Runtime](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech.Extension.ONNX.Runtime) | Required for embedded speech recognition and synthesis |
| [Microsoft.CognitiveServices.Speech.Extension.Telemetry](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech.Extension.Telemetry) | Required for embedded speech recognition and synthesis |


::: zone-end

::: zone pivot="programming-language-java"

**Choose your target environment**

# [Java Runtime](#tab/jre)

For Java embedded applications, add [client-sdk-embedded](https://mvnrepository.com/artifact/com.microsoft.cognitiveservices.speech/client-sdk-embedded) (`.jar`) as a dependency. This package supports cloud, embedded, and hybrid speech.

> [!IMPORTANT]
> Don't add [client-sdk](https://mvnrepository.com/artifact/com.microsoft.cognitiveservices.speech/client-sdk) in the same project, since it supports only cloud speech services.

Follow these steps to install the Speech SDK for Java using Apache Maven:

1. Install [Apache Maven](https://maven.apache.org/install.html).
1. Open a command prompt where you want the new project, and create a new `pom.xml` file.
1. Copy the following XML content into `pom.xml`:
    ```xml
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>
        <groupId>com.microsoft.cognitiveservices.speech.samples</groupId>
        <artifactId>quickstart-eclipse</artifactId>
        <version>1.0.0-SNAPSHOT</version>
        <build>
            <sourceDirectory>src</sourceDirectory>
            <plugins>
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.7.0</version>
                <configuration>
                <source>1.8</source>
                <target>1.8</target>
                </configuration>
            </plugin>
            </plugins>
        </build>
        <dependencies>
            <dependency>
            <groupId>com.microsoft.cognitiveservices.speech</groupId>
            <artifactId>client-sdk-embedded</artifactId>
            <version>1.43.0</version>
            </dependency>
        </dependencies>
    </project>
    ```
1. Run the following Maven command to install the Speech SDK and dependencies.
    ```console
    mvn clean dependency:copy-dependencies
    ```

# [Android](#tab/android)

For Java embedded applications, add [client-sdk-embedded](https://mvnrepository.com/artifact/com.microsoft.cognitiveservices.speech/client-sdk-embedded) (`.aar`) as a dependency. This package supports cloud, embedded, and hybrid speech.

> [!IMPORTANT]
> Don't add [client-sdk](https://mvnrepository.com/artifact/com.microsoft.cognitiveservices.speech/client-sdk) in the same project, since it supports only cloud speech services.

Be sure to use the `@aar` suffix when the dependency is specified in `build.gradle`. Here's an example:

```
dependencies {
    implementation 'com.microsoft.cognitiveservices.speech:client-sdk-embedded:1.43.0@aar'
}
```
::: zone-end

::: zone pivot="programming-language-python"

For Python embedded applications, install the embedded variant of the Speech SDK for Python, which includes the on-device inference runtime:

```console
pip install azure-cognitiveservices-speech-embedded
```

> [!IMPORTANT]
> The embedded package (`azure-cognitiveservices-speech-embedded`) is a superset of the cloud-only package (`azure-cognitiveservices-speech`). It exposes the same `azure.cognitiveservices.speech` import namespace and supports all cloud scenarios in addition to embedded ones. Install only one of the two packages.

::: zone-end


::: zone pivot="programming-language-go"

The Speech SDK for Go is a `cgo` binding, so embedded speech requires the native Speech SDK libraries at build time and run time. Download the embedded variant of the native Speech SDK package for Linux, which includes the on-device runtime extensions:

1. Choose a directory for the Speech SDK files and set the `SPEECHSDK_ROOT` environment variable to point to it:

    ```console
    export SPEECHSDK_ROOT="$HOME/speechsdk-embedded"
    mkdir -p "$SPEECHSDK_ROOT"
    ```

1. Download and extract the embedded Speech SDK binaries:

    ```console
    wget -O SpeechSDK-Embedded-Linux.tar.gz https://aka.ms/csspeech/linuxembeddedbinary
    tar --strip 1 -xzf SpeechSDK-Embedded-Linux.tar.gz -C "$SPEECHSDK_ROOT"
    ```

    The embedded package is a superset of the standard (cloud-only) package. It includes the core library (`Microsoft.CognitiveServices.Speech.core`), the embedded recognition and synthesis runtime extensions, and their ONNX runtime dependency. Install only the embedded package, not both.

1. Point `cgo` at the native headers and libraries, and add the library folder to the loader path. Replace `<architecture>` with the processor architecture of your CPU: `x64`, `arm64`, or `arm32`.

    ```console
    export CGO_CFLAGS="-I$SPEECHSDK_ROOT/include/c_api"
    export CGO_LDFLAGS="-L$SPEECHSDK_ROOT/lib/<architecture> -lMicrosoft.CognitiveServices.Speech.core"
    export LD_LIBRARY_PATH="$SPEECHSDK_ROOT/lib/<architecture>:$LD_LIBRARY_PATH"
    ```

1. Add the Speech SDK for Go module to your project:

    ```console
    go get github.com/Microsoft/cognitive-services-speech-sdk-go
    ```

::: zone-end


## Models and voices

For embedded speech, you need to download the speech recognition models for [speech to text](speech-to-text.md) and voices for [text to speech](text-to-speech.md). Instructions are provided upon successful completion of the [limited access review](https://aka.ms/csgate-embedded-speech) process.

The following [speech to text](speech-to-text.md) models are available: da-DK, de-DE, en-AU, en-CA, en-GB, en-IE, en-IN, en-NZ, en-US, es-ES, es-MX, fr-CA, fr-FR, it-IT, ja-JP, ko-KR, pt-BR, pt-PT, zh-CN, zh-HK, and zh-TW.

All text to speech locales [here](language-support.md?tabs=tts) (except fa-IR, Persian (Iran)) are available out of box with either 1 selected female and/or 1 selected male voices. We welcome your input to help us gauge demand for more languages and voices.

## Embedded speech configuration

For cloud connected applications, as shown in most Speech SDK samples, you use the `SpeechConfig` object with an API key and endpoint. For embedded speech, you don't use a Foundry resource for Speech. Instead of a cloud resource, you use the [models and voices](#models-and-voices) that you download to your local device.

Use the `EmbeddedSpeechConfig` object to set the location of the models or voices. If your application is used for both speech to text and text to speech, you can use the same `EmbeddedSpeechConfig` object to set the location of the models and voices.

::: zone pivot="programming-language-csharp"

```csharp
// Provide the location of the models and voices.
List<string> paths = new List<string>();
paths.Add("C:\\dev\\embedded-speech\\stt-models");
paths.Add("C:\\dev\\embedded-speech\\tts-voices");
var embeddedSpeechConfig = EmbeddedSpeechConfig.FromPaths(paths.ToArray());

// For speech to text
embeddedSpeechConfig.SetSpeechRecognitionModel(
    "Microsoft Speech Recognizer en-US FP Model V8",
    Environment.GetEnvironmentVariable("EMBEDDED_SPEECH_MODEL_LICENSE"));

// For text to speech
embeddedSpeechConfig.SetSpeechSynthesisVoice(
    "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)",
    Environment.GetEnvironmentVariable("EMBEDDED_SPEECH_MODEL_LICENSE"));
embeddedSpeechConfig.SetSpeechSynthesisOutputFormat(SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm);
```
::: zone-end

::: zone pivot="programming-language-cpp"

> [!TIP]
> The `GetEnvironmentVariable` function is defined in the [speech to text quickstart](get-started-speech-to-text.md) and [text to speech quickstart](get-started-text-to-speech.md).

```cpp
// Provide the location of the models and voices.
vector<string> paths;
paths.push_back("C:\\dev\\embedded-speech\\stt-models");
paths.push_back("C:\\dev\\embedded-speech\\tts-voices");
auto embeddedSpeechConfig = EmbeddedSpeechConfig::FromPaths(paths);

// For speech to text
embeddedSpeechConfig->SetSpeechRecognitionModel((
    "Microsoft Speech Recognizer en-US FP Model V8",
    GetEnvironmentVariable("EMBEDDED_SPEECH_MODEL_LICENSE"));

// For text to speech
embeddedSpeechConfig->SetSpeechSynthesisVoice(
    "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)",
    GetEnvironmentVariable("EMBEDDED_SPEECH_MODEL_LICENSE"));
embeddedSpeechConfig->SetSpeechSynthesisOutputFormat(SpeechSynthesisOutputFormat::Riff24Khz16BitMonoPcm);
```

::: zone-end

::: zone pivot="programming-language-java"

```java
// Provide the location of the models and voices.
List<String> paths = new ArrayList<>();
paths.add("C:\\dev\\embedded-speech\\stt-models");
paths.add("C:\\dev\\embedded-speech\\tts-voices");
var embeddedSpeechConfig = EmbeddedSpeechConfig.fromPaths(paths);

// For speech to text
embeddedSpeechConfig.setSpeechRecognitionModel(
    "Microsoft Speech Recognizer en-US FP Model V8",
    System.getenv("EMBEDDED_SPEECH_MODEL_LICENSE"));

// For text to speech
embeddedSpeechConfig.setSpeechSynthesisVoice(
    "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)",
    System.getenv("EMBEDDED_SPEECH_MODEL_LICENSE"));
embeddedSpeechConfig.setSpeechSynthesisOutputFormat(SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm);
```

::: zone-end

::: zone pivot="programming-language-python"

```python
import os
import azure.cognitiveservices.speech as speechsdk

# Provide the location of the models and voices.
paths = [
    "C:\\dev\\embedded-speech\\stt-models",
    "C:\\dev\\embedded-speech\\tts-voices",
]
embedded_speech_config = speechsdk.EmbeddedSpeechConfig.from_paths(paths)

# For speech to text
embedded_speech_config.set_speech_recognition_model(
    "Microsoft Speech Recognizer en-US FP Model V8",
    os.environ.get("EMBEDDED_SPEECH_MODEL_LICENSE"))

# For text to speech
embedded_speech_config.set_speech_synthesis_voice(
    "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)",
    os.environ.get("EMBEDDED_SPEECH_MODEL_LICENSE"))
embedded_speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
```

> [!TIP]
> If there's only one model or voice path, you can also use `speechsdk.EmbeddedSpeechConfig.from_path(path)`.

::: zone-end


::: zone pivot="programming-language-go"

```go
import (
    "os"

    "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
)

// Provide the location of the models and voices.
paths := []string{
    "/dev/embedded-speech/stt-models",
    "/dev/embedded-speech/tts-voices",
}
embeddedSpeechConfig, err := speech.NewEmbeddedSpeechConfigFromPaths(paths)
if err != nil {
    // Handle the error.
}
defer embeddedSpeechConfig.Close()

// For speech to text
embeddedSpeechConfig.SetSpeechRecognitionModel(
    "Microsoft Speech Recognizer en-US FP Model V8",
    os.Getenv("EMBEDDED_SPEECH_MODEL_LICENSE"))

// For text to speech
embeddedSpeechConfig.SetSpeechSynthesisVoice(
    "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)",
    os.Getenv("EMBEDDED_SPEECH_MODEL_LICENSE"))
```

> [!TIP]
> If there's only one model or voice path, you can also use `speech.NewEmbeddedSpeechConfigFromPath(path)`. The embedded config wraps a regular `SpeechConfig`, so pass `embeddedSpeechConfig.GetSpeechConfig()` to the existing recognizer and synthesizer factory functions, such as `NewSpeechRecognizerFromConfig`.

::: zone-end


## Embedded speech code samples

::: zone pivot="programming-language-csharp"

You can find ready to use embedded speech samples at [GitHub](https://aka.ms/embedded-speech-samples). For remarks on projects from scratch, see samples specific documentation:

- [C# (.NET 8.0)](https://aka.ms/embedded-speech-samples-csharp)
- [C# (.NET MAUI)](https://aka.ms/embedded-speech-samples-csharp-maui)
::: zone-end

::: zone pivot="programming-language-cpp"

You can find ready to use embedded speech samples at [GitHub](https://aka.ms/embedded-speech-samples). For remarks on projects from scratch, see samples specific documentation:
- [C++](https://aka.ms/embedded-speech-samples-cpp)
::: zone-end

::: zone pivot="programming-language-java"

You can find ready to use embedded speech samples at [GitHub](https://aka.ms/embedded-speech-samples). For remarks on projects from scratch, see samples specific documentation:
- [Java (JRE)](https://aka.ms/embedded-speech-samples-java)
- [Java for Android](https://aka.ms/embedded-speech-samples-java-android)
::: zone-end

::: zone pivot="programming-language-python"

You can find ready-to-use embedded speech samples at [GitHub](https://aka.ms/embedded-speech-samples). For remarks on projects from scratch, see the samples specific documentation:
- [Python](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/python/embedded-speech)
::: zone-end

::: zone pivot="programming-language-go"

You can find ready-to-use embedded speech samples for speech recognition, synthesis, and translation at [GitHub](https://github.com/microsoft/cognitive-services-speech-sdk-go/tree/master/samples/embedded). For prerequisites, native library setup, model and voice installation, and build flags, see the [embedded samples guide](https://github.com/microsoft/cognitive-services-speech-sdk-go/blob/master/samples/embedded/README.md).
::: zone-end

## Hybrid speech

Hybrid speech with the `HybridSpeechConfig` object uses the cloud speech service by default and embedded speech as a fallback in case cloud connectivity is limited or slow.

With hybrid speech configuration for [speech to text](speech-to-text.md) (recognition models), embedded speech is used when connection to the cloud service fails after repeated attempts. Recognition might continue using the cloud service again if the connection is later resumed.

With hybrid speech configuration for [text to speech](text-to-speech.md) (voices), embedded and cloud synthesis are run in parallel and the final result is selected based on response speed. The best result is evaluated again on each new synthesis request.

> [!NOTE]
> The Speech SDK for Python and the Speech SDK for Go don't support hybrid speech. Use the C#, C++, or Java SDK for hybrid scenarios.

## Cloud speech

For cloud speech, you use the `SpeechConfig` object, as shown in the [speech to text quickstart](get-started-speech-to-text.md) and [text to speech quickstart](get-started-text-to-speech.md). To run the quickstarts for embedded speech, you can replace `SpeechConfig` with `EmbeddedSpeechConfig` or `HybridSpeechConfig`. Most of the other speech recognition and synthesis code are the same, whether using cloud, embedded, or hybrid configuration.

## Embedded voices capabilities

For embedded voices, it's essential to note that certain [Speech synthesis markup language (SSML)](./speech-synthesis-markup.md) tags might not be currently supported due to differences in the model structure. For detailed information regarding the unsupported SSML tags, refer to the following table.

| Level 1 | Level 2 | Sub values | Support in embedded NTTS |
|---------|---------|---------|---------|
| audio           | src       |                                                       | No                       |
| bookmark        |           |                                                       | Yes                      |
| break           | strength  |                                                       | Yes                       |
|                 | time      |                                                       | Yes                       |
| silence         | type      | Leading, Tailing, Comma-exact, etc.                   | No                       |
|                 | value     |                                                       | No                       |
| emphasis        | level     |                                                       | No                       |
| lang            |           |                                                       | No                       |
| lexicon         | uri       |                                                       | Yes                      |
| math            |           |                                                       | No                       |
| msttsaudioduration | value   |                                                       | No                       |
| msttsbackgroundaudio | src    |                                                       | No                       |
|                 | volume    |                                                       | No                       |
|                 | fadein    |                                                       | No                       |
|                 | fadeout   |                                                       | No                       |
| msttsexpress-as | style     |                                                       | Yes<sup>1</sup>          |
|                 | styledegree |                                                     | No                       |
|                 | role      |                                                       | No                       |
| msttssilence    |           |                                                       | No                       |
| msttsviseme     | type      | redlips_front, FacialExpression                       | No                       |
| p               |           |                                                       | Yes                      |
| phoneme         | alphabet  | ipa, sapi, ups, etc.                                  | Yes                      |
|                 | ph        |                                                       | Yes                      |
| prosody         | contour   | Sentences level support, word level only en-US and zh-CN | Yes                      |
|                 | pitch     |                                                       | Yes                      |
|                 | range     |                                                       | Yes                      |
|                 | rate      |                                                       | Yes                      |
|                 | volume    |                                                       | Yes                      |
| s               |           |                                                       | Yes                      |
| say-as          | interpret-as | characters, spell-out, number_digit, date, etc.     | Yes                      |
|                 | format    |                                                       | Yes                      |
|                 | detail    |                                                       | Yes                      |
| sub             | alias     |                                                       | Yes                      |
| speak           |           |                                                       | Yes                      |
| voice           |           |                                                       | No                       |

<sup>1</sup> The [`msttsexpress-as`](./speech-synthesis-markup-voice.md#use-speaking-styles-paralinguistics-and-roles) style is supported only for the `en-US-JennyNeural` voice.

## Related content

- [Read about text to speech on devices for disconnected and hybrid scenarios](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/azure-neural-tts-now-available-on-devices-for-disconnected-and-hybrid-scenarios/3716797)
- [Limited Access to embedded Speech](/azure/ai-foundry/responsible-ai/speech-service/embedded-speech/limited-access-embedded-speech)
