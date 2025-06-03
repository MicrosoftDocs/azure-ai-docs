---
title: Profanity filtering - Azure AI Translator
titleSuffix: Azure AI services
description: Use Azure AI Translator profanity filtering to determine the level of profanity translated in your text.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: conceptual
ms.date: 05/19/2025
ms.author: lajanuar
---

# Add profanity filtering with Azure AI Translator

In most cases, the Azure AI Translator service retains profanity that is present in the source in the translation. The degree of profanity and the context that makes words profane differ between cultures. As a result, the degree of profanity in the target language can be amplified or reduced.

If you want to avoid seeing profanity in the translation, even if profanity is present in the source text, use the profanity filtering option available in the `Translate()` method. This option allows you to choose whether you want the profanity deleted, marked with appropriate tags, or no action taken.

The `Translate()` method takes the "options" parameter, which contains the new element "ProfanityAction." The accepted values of ProfanityAction are "NoAction," "Marked," and "Deleted." For the value of "Marked," another optional element "ProfanityMarker" can take the values "Asterisk" (default) and "Tag."

## Accepted values and examples of ProfanityMarker and ProfanityAction

| ProfanityAction value | ProfanityMarker value | Action | Example: Source - Spanish| Example: Target - English|
|:--|:--|:--|:--|:--|
| NoAction|  | Default. Same as not setting the option. Profanity passes from source to target. | `Que coche de` \<insert-profane-word> | What a \<insert-profane-word> car  |
| Marked                | Asterisk              | Asterisks replace profane words (default).                               | `Que coche de` \<insert-profane-word> | What a *** car      |
| Marked                | Tag                   | Profane words are surrounded by XML tags \<profanity\>...\</profanity>.          | `Que coche de` \<insert-profane-word> | What a \<profanity> \<insert-profane-word> \</profanity> car |
| Deleted               |                       | Profane words are removed from the output without replacement.                   | `Que coche de` \<insert-profane-word> | What a car        |

In the above examples, **\<insert-profane-word>** is a placeholder for profane words.

## Next steps

> [!div class="nextstepaction"]
> [Apply profanity filtering with your Translator call](../../text-translation/reference/v3/translate.md)
