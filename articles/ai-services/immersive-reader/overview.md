---
title: What is Azure AI Immersive Reader?
titleSuffix: Azure AI services
description: Learn how you can use Immersive Reader to help people with learning differences or help new readers and language learners improve reading comprehension.
author: rwallerms
manager: nitinme

ms.service: azure-ai-immersive-reader
ms.topic: overview
ms.date: 02/12/2024
ms.author: rwaller
keywords: readers, language learners, display pictures, improve reading, read content, translate
#Customer intent: As a developer, I want to learn more about the Immersive Reader, which is a new offering in Azure AI services, so that I can embed this package of content into a document to accommodate users with reading differences.
---

# What is Azure AI Immersive Reader?

[Immersive Reader](https://www.onenote.com/learningtools), part of [Azure AI services](../../ai-services/what-are-ai-services.md), is an inclusively designed tool that implements proven techniques to improve reading comprehension for new readers, language learners, and people with learning differences such as dyslexia. With the Immersive Reader client library, you can leverage the same technology used in Microsoft Word and Microsoft OneNote to improve your web applications.

This documentation contains the following types of articles:  

* **[Quickstart guides](quickstarts/client-libraries.md)** provide instructions to help you get started making requests to the service.
* **[How-to guides](how-to-create-immersive-reader.md)** contain instructions for using the service in more specific or customized ways.

## Use Immersive Reader to improve reading accessibility

Immersive Reader is designed to make reading easier and more accessible for everyone. Take a look at a few of Immersive Reader's core features.

### Isolate content for improved readability

Immersive Reader isolates content to improve readability.

:::image type="content" source="media/immersive-reader.png" alt-text="Screenshot of Immersive Reader that shows how it isolates content for improved readability.":::

### Display pictures for common words

Immersive Reader displays pictures for commonly used terms.

:::image type="content" source="media/picture-dictionary.png" alt-text="Screenshot of Immersive Reader's picture dictionary displaying a picture of a tool for the word tool.":::

### Highlight parts of speech

Immersive Reader can help learners understand parts of speech and grammar by highlighting verbs, nouns, pronouns, and more.

:::image type="content" source="media/parts-of-speech.png" alt-text="Screenshot of Immersive Reader highlighting parts of speech using different colors.":::

### Read content aloud

Speech synthesis, or text to speech, is baked into the Immersive Reader service. Readers can select text to be read aloud.

:::image type="content" source="media/read-aloud.png" alt-text="Screenshot of Immersive Reader's text-to-speech feature that reads text aloud.":::

### Translate content in real-time

Immersive Reader can translate text into many languages in real time, which helps to improve comprehension for readers learning a new language.

:::image type="content" source="media/translation.png" alt-text="Screenshot of Immersive Reader's language translation feature.":::

### Split words into syllables

With Immersive Reader, you can break words into syllables to improve readability or to sound out new words.

:::image type="content" source="media/syllabification.png" alt-text="Screenshot of Immersive Reader breaking words into syllables.":::

## How does Immersive Reader work?

Immersive Reader is a standalone web application. When it's invoked, the Immersive Reader client library displays on top of your existing web application in an `iframe`. When your web application calls the Immersive Reader service, you specify the content to show the reader. The Immersive Reader client library handles the creation and styling of the `iframe` and communication with the Immersive Reader backend service. The Immersive Reader service processes the content for parts of speech, text to speech, translation, and more.

## Data privacy for Immersive reader

Immersive reader doesn't store any customer data.

## Next step

The Immersive Reader client library is available in C#, JavaScript, Java (Android), Kotlin (Android), and Swift (iOS). Get started with:

* [Quickstart: Use the Immersive Reader client library](quickstarts/client-libraries.md)
