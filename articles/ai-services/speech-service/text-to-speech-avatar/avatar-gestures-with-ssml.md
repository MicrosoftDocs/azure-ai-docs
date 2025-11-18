---
title: Customize avatar gestures with SSML - Speech service
titleSuffix: Foundry Tools
description: Learn how to edit text to speech avatar gestures with SSML.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 08/07/2025
ms.author: pafarley
author: PatrickFarley
---

# Customize text to speech avatar gestures with SSML

The [Speech Synthesis Markup Language (SSML)](../speech-synthesis-markup-structure.md) with input text determines the structure, content, and other characteristics of the text to speech output. Most SSML tags also work in text to speech avatar. Furthermore, text to speech avatar batch mode provides avatar gesture insertion by using the SSML bookmark element with the format `<bookmark mark='gesture.*'/>`. 

A gesture starts at the insertion point in time. If the gesture takes more time than the audio, the gesture is cut at the point in time when the audio is finished.

## Bookmark example

The following example shows how to insert a gesture in the text to speech avatar batch synthesis with SSML.

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
<voice name="en-US-AvaMultilingualNeural">
Hello <bookmark mark='gesture.wave-left-1'/>, my name is Ava, nice to meet you!
</voice>
</speak>
```

In this example, the avatar starts waving their hand at the left after the word "Hello".

:::image type="content" source="./media/gesture.png" alt-text="Screenshot that shows the standard avatar waving their hand at the left." lightbox="./media/gesture.png":::

> [!NOTE]
> Gesture feature isn't currently supported when a voice sync for avatar is selected in a custom text to speech avatar.


## Next steps

* [What is text to speech avatar](what-is-text-to-speech-avatar.md)
* [Real-time synthesis](./real-time-synthesis-avatar.md)
* [Use batch synthesis for text to speech avatar](./batch-synthesis-avatar.md)