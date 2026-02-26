---
title: Disclosure design guidelines for avatars
titleSuffix: Foundry Tools
description: Introduction to disclosure design guidelines and assessing disclosure level for avatars.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 11/16/2023
---

# Disclosure design guidelines for avatars

[!INCLUDE [non-english-translation](../../includes/non-english-translation.md)]

Learn how to build and maintain trust with customers by being transparent about the synthetic nature of your avatar experience.

## What is disclosure?

Disclosure is a means of letting people know they're interacting with or watching an avatar that is synthetically generated. 

## Why is disclosure necessary?

The need to disclose the synthetic origins of a computer-generated avatar is relatively new. In the past, computer-generated humans were obviously that—no one would ever mistake them for a real person. Every day, however, the realism of synthetic human faces, bodies, and voices improves, and they become increasingly indistinguishable from videos of real humans.

## Goals

These are the principles to keep in mind when designing synthetic voice experiences: 

**Reinforce trust**: Design with the intention to fail the Turing Test without degrading the experience. Let the users in on the fact that they're interacting with a text to speech avatar while allowing them to engage seamlessly with the experience.

**Adapt to context of use**: Understand when, where, and how your users will interact with the text to speech avatar to provide the right type of disclosure at the right time. 

**Set clear expectations**: Allow users to easily discover and understand the capabilities of the agent. Offer opportunities to learn more about text to speech avatar technology upon request. 

**Embrace failure**: Use moments of failure to reinforce the capabilities of the agent. 

## How to use this guide

This guide helps you determine which disclosure patterns are best fit for your text to speech avatar experience. We then offer examples of how and when to use them. Each of these patterns is designed to maximize transparency with users about text to speech avatar while staying true to human-centered design.

Considering the vast body of design guidance on avatar watching or interacting experiences, we focus here specifically on: 
- [Disclosure assessment](#disclosure-assessment): A process to determine the type of disclosure recommended for your text to speech avatar experience 
- [How to disclose](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-patterns): Examples of disclosure patterns that can be applied to your text to speech avatar experience 
- [When to disclose](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-patterns#when-to-disclose): Optimal moments to disclose throughout the user journey

## Disclosure assessment

Consider your users' expectations about an interaction and the context in which they will experience the avatar. Unlike synthetic voices, synthetic avatars are more likely to be mistaken for real people, so clear disclosures are necessary to inform viewers that they are viewing and/or interacting with an avatar, not a real person.

### Determine disclosure level

The text to speech avatar is a photorealistic human image that has lip sync and facial expressions that can naturally match with a voice during speech, make gestures and natural-looking smiles, and nod its head. Combined with realistic sounding text to speech voices, it’s sometimes very hard to tell a text to speech avatar video from a video of a real speaking human. Interacting with or watching a custom avatar speaking in a custom neural voice from the same talent is likely to mislead an audience familiar with that individual, whom they may know or trust. So, we consider **all text to speech avatar features as in need of High Disclosure.**

## See also

* [Disclosure design patterns](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-patterns)
* [Disclosure for voice and avatar talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent)
* [Guidelines for responsible deployment of synthetic voice technology](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)
