---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 1/21/2024
ms.author: eur
ms.custom: devx-track-csharp
---

[!INCLUDE [Header](../../common/csharp.md)]

[!INCLUDE [Introduction](intro.md)]

## Sensitive data and environment variables

The example source code in this article depends on environment variables for storing sensitive data, such as the Speech resource's key and region. The `Program` class contains two `static readonly string` values that are assigned from the host machine's environment variables: `SPEECH__SUBSCRIPTION__KEY` and `SPEECH__SERVICE__REGION`. Both of these fields are at the class scope, so they're accessible within method bodies of the class: 

```csharp
public class Program
{
    static readonly string SPEECH__SUBSCRIPTION__KEY =
        Environment.GetEnvironmentVariable(nameof(SPEECH__SUBSCRIPTION__KEY));
    
    static readonly string SPEECH__SERVICE__REGION =
        Environment.GetEnvironmentVariable(nameof(SPEECH__SERVICE__REGION));

    static Task Main() => Task.CompletedTask;
}
```

For more information on environment variables, see [Environment variables and application configuration](../../../../cognitive-services-environment-variables.md).

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

## Create a speech translation configuration

To call the Speech service by using the Speech SDK, you need to create a [`SpeechTranslationConfig`][speechtranslationconfig] instance. This class includes information about your subscription, like your key and associated region, endpoint, host, or authorization token.

> [!TIP]
> Regardless of whether you're performing speech recognition, speech synthesis, translation, or intent recognition, you'll always create a configuration.

You can initialize `SpeechTranslationConfig` in a few ways:

* With a subscription: pass in a key and the associated region.
* With an endpoint: pass in a Speech service endpoint. A key or authorization token is optional.
* With a host: pass in a host address. A key or authorization token is optional.
* With an authorization token: pass in an authorization token and the associated region.

Let's look at how you create a `SpeechTranslationConfig` instance by using a key and region. Get the Speech resource key and region in the [Azure portal](https://portal.azure.com).

```csharp
public class Program
{
    static readonly string SPEECH__SUBSCRIPTION__KEY =
        Environment.GetEnvironmentVariable(nameof(SPEECH__SUBSCRIPTION__KEY));
    
    static readonly string SPEECH__SERVICE__REGION =
        Environment.GetEnvironmentVariable(nameof(SPEECH__SERVICE__REGION));

    static Task Main() => TranslateSpeechAsync();

    static async Task TranslateSpeechAsync()
    {
        var speechTranslationConfig =
            SpeechTranslationConfig.FromSubscription(SPEECH__SUBSCRIPTION__KEY, SPEECH__SERVICE__REGION);
    }
}
```

## Change the source language

One common task of speech translation is specifying the input (or source) language. The following example shows how you would change the input language to Italian. In your code, interact with the `SpeechTranslationConfig` instance by assigning it to the [`SpeechRecognitionLanguage`][recognitionlang] property:

```csharp
static async Task TranslateSpeechAsync()
{
    var speechTranslationConfig =
        SpeechTranslationConfig.FromSubscription(SPEECH__SUBSCRIPTION__KEY, SPEECH__SERVICE__REGION);

    // Source (input) language
    speechTranslationConfig.SpeechRecognitionLanguage = "it-IT";
}
```

The `SpeechRecognitionLanguage` property expects a language-locale format string. Refer to the [list of supported speech translation locales](../../../language-support.md?tabs=speech-translation).

## Add a translation language

Another common task of speech translation is to specify target translation languages. At least one is required, but multiples are supported. The following code snippet sets both French and German as translation language targets:

```csharp
static async Task TranslateSpeechAsync()
{
    var speechTranslationConfig =
        SpeechTranslationConfig.FromSubscription(SPEECH__SUBSCRIPTION__KEY, SPEECH__SERVICE__REGION);

    speechTranslationConfig.SpeechRecognitionLanguage = "it-IT";
    
    speechTranslationConfig.AddTargetLanguage("fr");
    speechTranslationConfig.AddTargetLanguage("de");
}
```

With every call to [`AddTargetLanguage`][addlang], a new target translation language is specified. In other words, when speech is recognized from the source language, each target translation is available as part of the resulting translation operation.

## Initialize a translation recognizer

After you created a [`SpeechTranslationConfig`][speechtranslationconfig] instance, the next step is to initialize [`TranslationRecognizer`][translationrecognizer]. When you initialize `TranslationRecognizer`, you need to pass it your `speechTranslationConfig` instance. The configuration object provides the credentials that the Speech service requires to validate your request.

If you're recognizing speech by using your device's default microphone, here's what the `TranslationRecognizer` instance should look like:

```csharp
static async Task TranslateSpeechAsync()
{
    var speechTranslationConfig =
        SpeechTranslationConfig.FromSubscription(SPEECH__SUBSCRIPTION__KEY, SPEECH__SERVICE__REGION);

    var fromLanguage = "en-US";
    var toLanguages = new List<string> { "it", "fr", "de" };
    speechTranslationConfig.SpeechRecognitionLanguage = fromLanguage;
    toLanguages.ForEach(speechTranslationConfig.AddTargetLanguage);

    using var translationRecognizer = new TranslationRecognizer(speechTranslationConfig);
}
```

If you want to specify the audio input device, then you need to create an [`AudioConfig`][audioconfig] class instance and provide the `audioConfig` parameter when initializing `TranslationRecognizer`.

> [!TIP]
> [Learn how to get the device ID for your audio input device](../../../how-to-select-audio-input-devices.md).

First, reference the `AudioConfig` object as follows:

```csharp
static async Task TranslateSpeechAsync()
{
    var speechTranslationConfig =
        SpeechTranslationConfig.FromSubscription(SPEECH__SUBSCRIPTION__KEY, SPEECH__SERVICE__REGION);
    
    var fromLanguage = "en-US";
    var toLanguages = new List<string> { "it", "fr", "de" };
    speechTranslationConfig.SpeechRecognitionLanguage = fromLanguage;
    toLanguages.ForEach(speechTranslationConfig.AddTargetLanguage);

    using var audioConfig = AudioConfig.FromDefaultMicrophoneInput();
    using var translationRecognizer = new TranslationRecognizer(speechTranslationConfig, audioConfig);
}
```

If you want to provide an audio file instead of using a microphone, you still need to provide an `audioConfig` parameter. However, when you create an `AudioConfig` class instance, instead of calling `FromDefaultMicrophoneInput`, you call `FromWavFileInput` and pass the `filename` parameter:

```csharp
static async Task TranslateSpeechAsync()
{
    var speechTranslationConfig =
        SpeechTranslationConfig.FromSubscription(SPEECH__SUBSCRIPTION__KEY, SPEECH__SERVICE__REGION);
    
    var fromLanguage = "en-US";
    var toLanguages = new List<string> { "it", "fr", "de" };
    speechTranslationConfig.SpeechRecognitionLanguage = fromLanguage;
    toLanguages.ForEach(speechTranslationConfig.AddTargetLanguage);

    using var audioConfig = AudioConfig.FromWavFileInput("YourAudioFile.wav");
    using var translationRecognizer = new TranslationRecognizer(speechTranslationConfig, audioConfig);
}
```

## Translate speech

To translate speech, the Speech SDK relies on a microphone or an audio file input. Speech recognition occurs before speech translation. After all objects are initialized, call the recognize-once function and get the result:

```csharp
static async Task TranslateSpeechAsync()
{
    var speechTranslationConfig =
        SpeechTranslationConfig.FromSubscription(SPEECH__SUBSCRIPTION__KEY, SPEECH__SERVICE__REGION);
    
    var fromLanguage = "en-US";
    var toLanguages = new List<string> { "it", "fr", "de" };
    speechTranslationConfig.SpeechRecognitionLanguage = fromLanguage;
    toLanguages.ForEach(speechTranslationConfig.AddTargetLanguage);

    using var translationRecognizer = new TranslationRecognizer(speechTranslationConfig);

    Console.Write($"Say something in '{fromLanguage}' and ");
    Console.WriteLine($"we'll translate into '{string.Join("', '", toLanguages)}'.\n");
    
    var result = await translationRecognizer.RecognizeOnceAsync();
    if (result.Reason == ResultReason.TranslatedSpeech)
    {
        Console.WriteLine($"Recognized: \"{result.Text}\":");
        foreach (var element in result.Translations)
        {
            Console.WriteLine($"    TRANSLATED into '{element.Key}': {element.Value}");
        }
    }
}
```

For more information about speech to text, see [the basics of speech recognition](../../../get-started-speech-to-text.md).

## Event based translation

The `TranslationRecognizer` object exposes a `Recognizing` event. The event fires several times and provides a mechanism to retrieve the intermediate translation results. 

> [!NOTE]
> Intermediate translation results aren't available when you use [multi-lingual speech translation](#multi-lingual-speech-translation-without-source-language-candidates).

The following example prints the intermediate translation results to the console:

```csharp
using (var audioInput = AudioConfig.FromWavFileInput(@"whatstheweatherlike.wav"))
{
    using (var translationRecognizer = new TranslationRecognizer(config, audioInput))
    {
        // Subscribes to events.
        translationRecognizer.Recognizing += (s, e) =>
        {
            Console.WriteLine($"RECOGNIZING in '{fromLanguage}': Text={e.Result.Text}");
            foreach (var element in e.Result.Translations)
            {
                Console.WriteLine($"    TRANSLATING into '{element.Key}': {element.Value}");
            }
        };

        translationRecognizer.Recognized += (s, e) => {
            if (e.Result.Reason == ResultReason.TranslatedSpeech)
            {
                Console.WriteLine($"RECOGNIZED in '{fromLanguage}': Text={e.Result.Text}");
                foreach (var element in e.Result.Translations)
                {
                    Console.WriteLine($"    TRANSLATED into '{element.Key}': {element.Value}");
                }
            }
            else if (e.Result.Reason == ResultReason.RecognizedSpeech)
            {
                Console.WriteLine($"RECOGNIZED: Text={e.Result.Text}");
                Console.WriteLine($"    Speech not translated.");
            }
            else if (e.Result.Reason == ResultReason.NoMatch)
            {
                Console.WriteLine($"NOMATCH: Speech could not be recognized.");
            }
        };

        // Starts continuous recognition. Uses StopContinuousRecognitionAsync() to stop recognition.
        Console.WriteLine("Start translation...");
        await translationRecognizer.StartContinuousRecognitionAsync().ConfigureAwait(false);

        // Waits for completion.
        // Use Task.WaitAny to keep the task rooted.
        Task.WaitAny(new[] { stopTranslation.Task });

        // Stops translation.
        await translationRecognizer.StopContinuousRecognitionAsync().ConfigureAwait(false);
    }
}
```

## Synthesize translations

After a successful speech recognition and translation, the result contains all the translations in a dictionary. The [`Translations`][translations] dictionary key is the target translation language, and the value is the translated text. Recognized speech can be translated and then synthesized in a different language (speech-to-speech).

### Event-based synthesis

The `TranslationRecognizer` object exposes a `Synthesizing` event. The event fires several times and provides a mechanism to retrieve the synthesized audio from the translation recognition result. If you're translating to multiple languages, see [Manual synthesis](#manual-synthesis). 

Specify the synthesis voice by assigning a [`VoiceName`][voicename] instance, and provide an event handler for the `Synthesizing` event to get the audio. The following example saves the translated audio as a .wav file.

> [!IMPORTANT]
> The event-based synthesis works only with a single translation. *Do not* add multiple target translation languages. Additionally, the `VoiceName` value should be the same language as the target translation language. For example, `"de"` could map to `"de-DE-Hedda"`.

```csharp
static async Task TranslateSpeechAsync()
{
    var speechTranslationConfig =
        SpeechTranslationConfig.FromSubscription(SPEECH__SUBSCRIPTION__KEY, SPEECH__SERVICE__REGION);
    
    var fromLanguage = "en-US";
    var toLanguage = "de";
    speechTranslationConfig.SpeechRecognitionLanguage = fromLanguage;
    speechTranslationConfig.AddTargetLanguage(toLanguage);

    speechTranslationConfig.VoiceName = "de-DE-Hedda";

    using var translationRecognizer = new TranslationRecognizer(speechTranslationConfig);

    translationRecognizer.Synthesizing += (_, e) =>
    {
        var audio = e.Result.GetAudio();
        Console.WriteLine($"Audio synthesized: {audio.Length:#,0} byte(s) {(audio.Length == 0 ? "(Complete)" : "")}");

        if (audio.Length > 0)
        {
            File.WriteAllBytes("YourAudioFile.wav", audio);
        }
    };

    Console.Write($"Say something in '{fromLanguage}' and ");
    Console.WriteLine($"we'll translate into '{toLanguage}'.\n");

    var result = await translationRecognizer.RecognizeOnceAsync();
    if (result.Reason == ResultReason.TranslatedSpeech)
    {
        Console.WriteLine($"Recognized: \"{result.Text}\"");
        Console.WriteLine($"Translated into '{toLanguage}': {result.Translations[toLanguage]}");
    }
}
```

### Manual synthesis

You can use the [`Translations`][translations] dictionary to synthesize audio from the translation text. Iterate through each translation and synthesize it. When you're creating a `SpeechSynthesizer` instance, the `SpeechConfig` object needs to have its [`SpeechSynthesisVoiceName`][speechsynthesisvoicename] property set to the desired voice. 

The following example translates to five languages. Each translation is then synthesized to an audio file in the corresponding neural language.

```csharp
static async Task TranslateSpeechAsync()
{
    var speechTranslationConfig =
        SpeechTranslationConfig.FromSubscription(SPEECH__SERVICE__KEY, SPEECH__SERVICE__REGION);

    var fromLanguage = "en-US";
    var toLanguages = new List<string> { "de", "en", "it", "pt", "zh-Hans" };
    speechTranslationConfig.SpeechRecognitionLanguage = fromLanguage;
    toLanguages.ForEach(speechTranslationConfig.AddTargetLanguage);

    using var translationRecognizer = new TranslationRecognizer(speechTranslationConfig);

    Console.Write($"Say something in '{fromLanguage}' and ");
    Console.WriteLine($"we'll translate into '{string.Join("', '", toLanguages)}'.\n");

    var result = await translationRecognizer.RecognizeOnceAsync();
    if (result.Reason == ResultReason.TranslatedSpeech)
    {
        var languageToVoiceMap = new Dictionary<string, string>
        {
            ["de"] = "de-DE-KatjaNeural",
            ["en"] = "en-US-AriaNeural",
            ["it"] = "it-IT-ElsaNeural",
            ["pt"] = "pt-BR-FranciscaNeural",
            ["zh-Hans"] = "zh-CN-XiaoxiaoNeural"
        };

        Console.WriteLine($"Recognized: \"{result.Text}\"");

        foreach (var (language, translation) in result.Translations)
        {
            Console.WriteLine($"Translated into '{language}': {translation}");

            var speechConfig =
                SpeechConfig.FromSubscription(
                    SPEECH__SERVICE__KEY, SPEECH__SERVICE__REGION);
            speechConfig.SpeechSynthesisVoiceName = languageToVoiceMap[language];

            using var audioConfig = AudioConfig.FromWavFileOutput($"{language}-translation.wav");
            using var speechSynthesizer = new SpeechSynthesizer(speechConfig, audioConfig);
            
            await speechSynthesizer.SpeakTextAsync(translation);
        }
    }
}
```

For more information about speech synthesis, see [the basics of speech synthesis](../../../get-started-text-to-speech.md).

## Multi-lingual translation with language identification

In many scenarios, you might not know which input languages to specify. Using [language identification](../../../language-identification.md?pivots=programming-language-csharp#run-speech-translation) you can detect up to 10 possible input languages and automatically translate to your target languages. 

The following example anticipates that `en-US` or `zh-CN` should be detected because they're defined in `AutoDetectSourceLanguageConfig`. Then, the speech is translated to `de` and `fr` as specified in the calls to `AddTargetLanguage()`.

```csharp
speechTranslationConfig.AddTargetLanguage("de");
speechTranslationConfig.AddTargetLanguage("fr");
var autoDetectSourceLanguageConfig = AutoDetectSourceLanguageConfig.FromLanguages(new string[] { "en-US", "zh-CN" });
var translationRecognizer = new TranslationRecognizer(speechTranslationConfig, autoDetectSourceLanguageConfig, audioConfig);
```

For a complete code sample, see [language identification](../../../language-identification.md?pivots=programming-language-csharp#run-speech-translation).


## Multi-lingual speech translation without source language candidates 

Multi-lingual speech translation implements a new level of speech translation technology that unlocks various capabilities, including having no specified input language, and handling language switches within the same session. These features enable a new level of speech translation powers that can be implemented into your products.

Currently when you use Language ID with speech translation, you must create the `SpeechTranslationConfig` object from the v2 endpoint. Replace the string "YourServiceRegion" with your Speech resource region (such as "westus"). Replace "YourSubscriptionKey" with your Speech resource key.

```csharp
var v2EndpointInString = String.Format("wss://{0}.stt.speech.microsoft.com/speech/universal/v2", "YourServiceRegion");
var v2EndpointUrl = new Uri(v2EndpointInString);
var speechTranslationConfig = SpeechTranslationConfig.FromEndpoint(v2EndpointUrl, "YourSubscriptionKey");
```

Specify the translation target languages. Replace with languages of your choice. You can add more lines.
```csharp
config.AddTargetLanguage("de");
config.AddTargetLanguage("fr");
```

A key differentiator with multi-lingual speech translation is that you do not need to specify the source language. This is because the service will automatically detect the source language. Create the `AutoDetectSourceLanguageConfig` object with the `fromOpenRange` method to let the service know that you want to use multi-lingual speech translation with no specified source language. 

```csharp
AutoDetectSourceLanguageConfig autoDetectSourceLanguageConfig = AutoDetectSourceLanguageConfig.fromOpenRange(); 
var translationRecognizer = new TranslationRecognizer(speechTranslationConfig, autoDetectSourceLanguageConfig, audioConfig);
```

For a complete code sample with the Speech SDK, see [speech translation samples on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/csharp/sharedcontent/console/translation_samples.cs#L714).

## Using custom translation in speech translation
The custom translation feature in speech translation seamlessly integrates with the Azure Custom Translation service, allowing you to achieve more accurate and tailored translations. As the integration directly harnesses the capabilities of the Azure custom translation service, you need to use a multi-service resource to ensure the correct functioning of the complete set of features. For detailed instructions, please consult the guide on [Create a multi-service resource for Azure AI services](/azure/ai-services/multi-service-resource?tabs=windows&pivots=azportal).

Additionally, for offline training of a custom translator and obtaining a "Category ID," please refer to the step-by-step script provided in the [Quickstart: Build, deploy, and use a custom model - Custom Translator](/azure/ai-services/translator/custom-translator/quickstart).

```csharp
// Creates an instance of a translation recognizer using speech translation configuration
// You should use the same subscription key, which you used to generate the custom model before.
// V2 endpoint is required for the “Custom Translation” feature. Example: "wss://westcentralus.stt.speech.microsoft.com/speech/universal/v2"

try (SpeechTranslationConfig config = SpeechTranslationConfig.fromEndpoint(URI.create(endpointUrl), speechSubscriptionKey)) {

            // Sets source and target language(s).
           ….

            // Set the category id
            config.setCustomModelCategoryId("yourCategoryId");

       ….
}
```

[speechtranslationconfig]: /dotnet/api/microsoft.cognitiveservices.speech.speechtranslationconfig
[audioconfig]: /dotnet/api/microsoft.cognitiveservices.speech.audio.audioconfig
[translationrecognizer]: /dotnet/api/microsoft.cognitiveservices.speech.translation.translationrecognizer
[recognitionlang]: /dotnet/api/microsoft.cognitiveservices.speech.speechconfig.speechrecognitionlanguage
[addlang]: /dotnet/api/microsoft.cognitiveservices.speech.speechtranslationconfig.addtargetlanguage
[translations]: /dotnet/api/microsoft.cognitiveservices.speech.translation.translationrecognitionresult.translations
[voicename]: /dotnet/api/microsoft.cognitiveservices.speech.speechtranslationconfig.voicename
[speechsynthesisvoicename]: /dotnet/api/microsoft.cognitiveservices.speech.speechconfig.speechsynthesisvoicename
