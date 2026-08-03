---
title: Improve recognition accuracy with phrase list
description: Phrase lists can be used to customize speech recognition results based on context. 
author: PatrickFarley
ms.author: pafarley
ms.reviewer: pafarley
ms.service: azure-speech-foundry-tools
ms.custom: devx-track-extended-java, devx-track-go, devx-track-js, devx-track-python
ms.topic: how-to
ms.date: 06/02/2026
zone_pivot_groups: programming-languages-set-two-with-js-spx
#Customer intent: As a developer using speech to text, I want to learn how to improve recognition accuracy with phrase list.
ai-usage: ai-assisted
---

# Improve recognition accuracy with phrase list

A phrase list is a list of words or phrases you provide ahead of time to help improve their recognition. When you add a phrase to a phrase list, you increase its importance, so the system is more likely to recognize it.

> [!IMPORTANT]
> Phrase list is a **runtime recognition feature** applied at the endpoint level. It works with:
> - Real-time transcription (Speech SDK, Speech CLI, Speech Studio)
> - Fast transcription API
> - Voice Live API
>
> Phrase list works with both base and custom speech endpoints. It doesn't require model training and isn't available with batch transcription.

Examples of phrases include:
* Names
* Geographical locations
* Homonyms
* Words or acronyms unique to your industry or organization

Phrase lists are simple and lightweight:
- **Just-in-time**: You provide a phrase list just before starting the speech recognition, so you don't need to train a custom model.
- **Lightweight**: You don't need a large data set. Provide a word or phrase to boost its recognition.

You can use phrase lists with the [Speech Studio](speech-studio-overview.md), [Speech SDK](quickstarts/setup-platform.md), or [Speech Command Line Interface (CLI)](spx-overview.md). They're supported with [Real-time transcription](./how-to-recognize-speech.md) and [Fast transcription API](./fast-transcription-create.md). The [Batch transcription API](batch-transcription.md) doesn't support phrase lists.

You can use phrase lists with both base (standard) endpoints and [custom speech](custom-speech-overview.md) endpoints. You apply the phrase list at runtime and it doesn't require model training. Some situations call for training a custom model that includes phrases to improve accuracy. For example, use custom speech in the following cases:
- If you need to use a large list of phrases. A phrase list shouldn't have more than 500 phrases.

## Phrase list weight

When you use the Speech SDK with real-time transcription, you can control the weight of phrase list phrases relative to the default dictionary. This setting determines how much influence the phrase list has on speech-to-text results.

Set the phrase list weight within a range of `0.0` to `2.0`:
- **0.0**: Disables the phrase list
- **1.0**: Default weight (standard influence)
- **2.0**: Maximum weight (highest influence)

A higher weight increases the likelihood that phrases from your list are recognized over alternatives in the default dictionary. This setting applies to the complete list.

## Try it in Speech Studio

Use [Speech Studio](speech-studio-overview.md) to test how a phrase list improves recognition for your audio. To implement a phrase list with your application in production, use the Speech SDK or Speech CLI.

For example, suppose you want the Speech service to recognize this sentence:
"Hi Rehaan, I'm Jessie from Contoso bank."

You might find that a phrase is incorrectly recognized as:
"Hi **everyone**, I'm **Jesse** from **can't do so bank**."

In the previous scenario, you want to add "Rehaan", "Jessie", and "Contoso" to your phrase list. Then the names are recognized correctly.

Now try Speech Studio to see how a phrase list can improve recognition accuracy.

> [!NOTE]
> You might be prompted to select your Azure subscription and Speech resource, and then acknowledge billing for your region.

1. Go to **Real-time Speech to text** in [Speech Studio](https://aka.ms/speechstudio/speechtotexttool). 
1. Test speech recognition by uploading an audio file or recording audio by using a microphone. For example, select **record audio with a microphone** and then say "Hi Rehaan, I'm Jessie from Contoso bank. " Then select the red button to stop recording.
1. You see the transcription result in the **Test results** text box. If "Rehaan", "Jessie", or "Contoso" are recognized incorrectly, add the terms to a phrase list in the next step.
1. Select **Show advanced options** and turn on **Phrase list**. 
1. Enter "Contoso;Jessie;Rehaan" in the phrase list text box. Separate multiple phrases with a semicolon.
    :::image type="content" source="./media/custom-speech/phrase-list-after-zoom.png" alt-text="Screenshot of a phrase list applied in Speech Studio." lightbox="./media/custom-speech/phrase-list-after-full.png":::
1. Use the microphone to test recognition again. Otherwise, select the retry arrow next to your audio file to rerun your audio. The terms "Rehaan", "Jessie", or "Contoso" should be recognized.

## Implement phrase list in real-time transcription

::: zone pivot="programming-language-csharp"
By using the [Speech SDK](speech-sdk.md), you can add phrases one at a time and then run speech recognition.

```csharp
var phraseList = PhraseListGrammar.FromRecognizer(recognizer);
phraseList.AddPhrase("Contoso");
phraseList.AddPhrase("Jessie");
phraseList.AddPhrase("Rehaan");
phraselist.SetWeight(weight);
```
::: zone-end

::: zone pivot="programming-language-cpp"
By using the [Speech SDK](speech-sdk.md), you can add phrases one at a time and then run speech recognition.

```cpp
auto phraseListGrammar = PhraseListGrammar::FromRecognizer(recognizer);
phraseListGrammar->AddPhrase("Contoso");
phraseListGrammar->AddPhrase("Jessie");
phraseListGrammar->AddPhrase("Rehaan");
phraselist->SetWeight(weight);
```
::: zone-end

::: zone pivot="programming-language-java"
By using the [Speech SDK](speech-sdk.md), you can add phrases one at a time and then run speech recognition.

```java
PhraseListGrammar phraseList = PhraseListGrammar.fromRecognizer(recognizer);
phraseList.addPhrase("Contoso");
phraseList.addPhrase("Jessie");
phraseList.addPhrase("Rehaan");
phraseList.setWeight(weight);
```
::: zone-end

::: zone pivot="programming-language-javascript"
By using the [Speech SDK](speech-sdk.md), you can add phrases one at a time and then run speech recognition.

```javascript
const phraseList = sdk.PhraseListGrammar.fromRecognizer(recognizer);
phraseList.addPhrase("Contoso");
phraseList.addPhrase("Jessie");
phraseList.addPhrase("Rehaan");
phraseList.setWeight(weight);
```
::: zone-end

::: zone pivot="programming-language-python"
By using the [Speech SDK](speech-sdk.md), you can add phrases one at a time and then run speech recognition.

```Python
phrase_list_grammar = speechsdk.PhraseListGrammar.from_recognizer(reco)
phrase_list_grammar.addPhrase("Contoso")
phrase_list_grammar.addPhrase("Jessie")
phrase_list_grammar.addPhrase("Rehaan")
phraseList.setWeight(weight)
```
::: zone-end

::: zone pivot="programming-language-go"
By using the [Speech SDK](speech-sdk.md), you can add phrases one at a time and then run speech recognition.

```go
phraseListGrammar, err := speech.NewPhraseListGrammarFromRecognizer(recognizer)
if err != nil {
  // Handle error.
}
defer phraseListGrammar.Close()

phraseListGrammar.AddPhrase("Contoso")
phraseListGrammar.AddPhrase("Jessie")
phraseListGrammar.AddPhrase("Rehaan")
phraseListGrammar.SetWeight(weight)
```
::: zone-end

::: zone pivot="programmer-tool-spx"
By using the [Speech CLI](spx-overview.md), you can include a phrase list in-line or with a text file along with the `recognize` command.


# [Terminal](#tab/terminal)

Try recognition from a microphone or an audio file. 

```console
spx recognize --microphone --phrases "Contoso;Jessie;Rehaan;"
spx recognize --file "your\path\to\audio.wav" --phrases "Contoso;Jessie;Rehaan;"
```

You can also add a phrase list by using a text file that contains one phrase per line.

```console
spx recognize --microphone --phrases @phrases.txt
spx recognize --file "your\path\to\audio.wav" --phrases @phrases.txt
```

# [PowerShell](#tab/powershell)

Try recognition from a microphone or an audio file. 

```powershell
spx --% recognize --microphone --phrases "Contoso;Jessie;Rehaan;"
spx --% recognize --file "your\path\to\audio.wav" --phrases "Contoso;Jessie;Rehaan;"
```

You can also add a phrase list by using a text file that contains one phrase per line.

```powershell
spx --% recognize --microphone --phrases @phrases.txt
spx --% recognize --file "your\path\to\audio.wav" --phrases @phrases.txt
```

***

::: zone-end

Allowed characters include locale-specific letters and digits, white space characters, and special characters such as +, \-, $, :, (, ), {, }, \_, ., ?, @, \\, ’, &, \#, %, \^, \*, \`, \<, \>, ;, \/. The system removes other special characters from the phrase.

## Implement phrase list in fast transcription
You can add a list of phrases in fast transcription through the [Speech-to-text REST API](/rest/api/speechtotext/transcriptions/transcribe).

```azurecli-interactive
curl --location 'https://YourResourceName.cognitiveservices.azure.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Ocp-Apim-Subscription-Key: YourSpeechResourceKey' \
--form 'audio=@"YourAudioFile"' \
--form 'definition={
  "locales": ["en-US"],
  "phraseList": {
    "phrases": ["Contoso", "Jessie", "Rehaan"]
  }
}'
```

## Next steps

Learn more about options to improve recognition accuracy.

> [!div class="nextstepaction"]
> [Custom speech](custom-speech-overview.md)
