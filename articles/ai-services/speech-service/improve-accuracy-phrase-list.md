---
title: Improve recognition accuracy with phrase list
description: Phrase lists can be used to customize speech recognition results based on context. 
author: PatrickFarley
ms.author: pafarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.custom: devx-track-extended-java, devx-track-js, devx-track-python
ms.topic: how-to
ms.date: 10/21/2025
zone_pivot_groups: programming-languages-set-two-with-js-spx
#Customer intent: As a developer using speech to text, I want to learn how to improve recognition accuracy with phrase list.
---

# Improve recognition accuracy with phrase list

A phrase list is a list of words or phrases provided ahead of time to help improve their recognition. Adding a phrase to a phrase list increases its importance, thus making it more likely to be recognized.
You can add phrase list in real-time transcription and fast transcription.

Examples of phrases include:
* Names
* Geographical locations
* Homonyms
* Words or acronyms unique to your industry or organization

Phrase lists are simple and lightweight:
- **Just-in-time**: A phrase list is provided just before starting the speech recognition, eliminating the need to train a custom model. 
- **Lightweight**: You don't need a large data set. Provide a word or phrase to boost its recognition.

For supported phrase list locales, see [Language and voice support for the Speech service](language-support.md?tabs=phraselist).

You can use phrase lists with the [Speech Studio](speech-studio-overview.md), [Speech SDK](quickstarts/setup-platform.md), or [Speech Command Line Interface (CLI)](spx-overview.md). It's supported with [Real-time transcription](./how-to-recognize-speech.md) and [Fast transcription API](./fast-transcription-create.md). The [Batch transcription API](batch-transcription.md) doesn't support phrase lists.

You can use phrase lists with both standard and [custom speech](custom-speech-overview.md). There are some situations where training a custom model that includes phrases is likely the best option to improve accuracy. For example, in the following cases you would use custom speech: 
- If you need to use a large list of phrases. A phrase list shouldn't have more than 500 phrases. 
- If you need a phrase list for languages that aren't currently supported.

## Phrase list weight

When using the Speech SDK with Real-time transcription, you can control the weight of phrase list phrases relative to the default dictionary. This setting determines how much influence the phrase list has on speech-to-text results.

The phrase list weight can be set within a range of `0.0` to `2.0`:
- **0.0**: Disables the phrase list
- **1.0**: Default weight (standard influence)
- **2.0**: Maximum weight (highest influence)

A higher weight increases the likelihood that phrases from your list are recognized over alternatives in the default dictionary. This setting applies to the complete list.

## Try it in Speech Studio

You can use [Speech Studio](speech-studio-overview.md) to test how phrase list would help improve recognition for your audio. To implement a phrase list with your application in production, you use the Speech SDK or Speech CLI. 

For example, let's say that you want the Speech service to recognize this sentence:
"Hi Rehaan, I'm Jessie from Contoso bank."

You might find that a phrase is incorrectly recognized as:
"Hi **everyone**, I'm **Jesse** from **can't do so bank**."

In the previous scenario, you would want to add "Rehaan", "Jessie", and "Contoso" to your phrase list. Then the names should be recognized correctly. 

Now try Speech Studio to see how phrase list can improve recognition accuracy.

> [!NOTE]
> You can be prompted to select your Azure subscription and Speech resource, and then acknowledge billing for your region. 

1. Go to **Real-time Speech to text** in [Speech Studio](https://aka.ms/speechstudio/speechtotexttool). 
1. You test speech recognition by uploading an audio file or recording audio with a microphone. For example, select **record audio with a microphone** and then say "Hi Rehaan, I'm Jessie from Contoso bank. " Then select the red button to stop recording. 
1. You should see the transcription result in the **Test results** text box. If "Rehaan", "Jessie", or "Contoso" were recognized incorrectly, you can add the terms to a phrase list in the next step.
1. Select **Show advanced options** and turn on **Phrase list**. 
1. Enter "Contoso;Jessie;Rehaan" in the phrase list text box. Multiple phrases need to be separated by a semicolon.
    :::image type="content" source="./media/custom-speech/phrase-list-after-zoom.png" alt-text="Screenshot of a phrase list applied in Speech Studio." lightbox="./media/custom-speech/phrase-list-after-full.png":::
1. Use the microphone to test recognition again. Otherwise you can select the retry arrow next to your audio file to rerun your audio. The terms "Rehaan", "Jessie", or "Contoso" should be recognized. 

## Implement phrase list in real-time transcription

::: zone pivot="programming-language-csharp"
With the [Speech SDK](speech-sdk.md) you can add phrases individually and then run speech recognition. 

```csharp
var phraseList = PhraseListGrammar.FromRecognizer(recognizer);
phraseList.AddPhrase("Contoso");
phraseList.AddPhrase("Jessie");
phraseList.AddPhrase("Rehaan");
phraselist.SetWeight(weight);
```
::: zone-end

::: zone pivot="programming-language-cpp"
With the [Speech SDK](speech-sdk.md) you can add phrases individually and then run speech recognition. 

```cpp
auto phraseListGrammar = PhraseListGrammar::FromRecognizer(recognizer);
phraseListGrammar->AddPhrase("Contoso");
phraseListGrammar->AddPhrase("Jessie");
phraseListGrammar->AddPhrase("Rehaan");
phraselist->SetWeight(weight);
```
::: zone-end

::: zone pivot="programming-language-java"
With the [Speech SDK](speech-sdk.md) you can add phrases individually and then run speech recognition. 

```java
PhraseListGrammar phraseList = PhraseListGrammar.fromRecognizer(recognizer);
phraseList.addPhrase("Contoso");
phraseList.addPhrase("Jessie");
phraseList.addPhrase("Rehaan");
phraseList.setWeight(weight);
```
::: zone-end

::: zone pivot="programming-language-javascript"
With the [Speech SDK](speech-sdk.md) you can add phrases individually and then run speech recognition. 

```javascript
const phraseList = sdk.PhraseListGrammar.fromRecognizer(recognizer);
phraseList.addPhrase("Contoso");
phraseList.addPhrase("Jessie");
phraseList.addPhrase("Rehaan");
phraseList.setWeight(weight);
```
::: zone-end

::: zone pivot="programming-language-python"
With the [Speech SDK](speech-sdk.md) you can add phrases individually and then run speech recognition. 

```Python
phrase_list_grammar = speechsdk.PhraseListGrammar.from_recognizer(reco)
phrase_list_grammar.addPhrase("Contoso")
phrase_list_grammar.addPhrase("Jessie")
phrase_list_grammar.addPhrase("Rehaan")
phraseList.setWeight(weight)
```
::: zone-end

::: zone pivot="programmer-tool-spx"
With the [Speech CLI](spx-overview.md) you can include a phrase list in-line or with a text file along with the recognize command.


# [Terminal](#tab/terminal)

Try recognition from a microphone or an audio file. 

```console
spx recognize --microphone --phrases "Contoso;Jessie;Rehaan;"
spx recognize --file "your\path\to\audio.wav" --phrases "Contoso;Jessie;Rehaan;"
```

You can also add a phrase list using a text file that contains one phrase per line.

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

You can also add a phrase list using a text file that contains one phrase per line.

```powershell
spx --% recognize --microphone --phrases @phrases.txt
spx --% recognize --file "your\path\to\audio.wav" --phrases @phrases.txt
```

***

::: zone-end

Allowed characters include locale-specific letters and digits, white space characters, and special characters such as +, \-, $, :, (, ), {, }, \_, ., ?, @, \\, ’, &, \#, %, \^, \*, \`, \<, \>, ;, \/. Other special characters are removed internally from the phrase.

## Implement phrase list in fast transcription
You can add a list of phrases in fast transcription via [Speech-to-text REST API](/rest/api/speechtotext/transcriptions/transcribe)

```azurecli-interactive
curl --location 'https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
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
