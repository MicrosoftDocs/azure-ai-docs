---
title: Disclosure design patterns for text to speech avatar
titleSuffix: Foundry Tools
description: Design patterns and best practices for avatar disclosure.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 11/16/2023
---

# Disclosure design patterns for text to speech avatar

[!INCLUDE [non-english-translation](../../includes/non-english-translation.md)]

## Overview

There's a spectrum of disclosure design patterns you can apply to your text to speech avatar experience. There is [explicit disclosure](#explicit-disclosure), which means communicating the origins of the text to speech avatar outright, and [Implicit disclosure](#implicit-disclosure), which includes cues and interaction patterns that benefit avatar experiences. 

|Category | Examples |
|--------------|-------------|
| Explicit disclosure patterns   | <ul><li>[Transparent Introduction](#transparent-introduction)</li><li>[Verbal Transparent Introduction](#verbal-transparent-introduction)</li> <li> [Explicit Byline](#explicit-byline)</li><li>  <li>[Parental Disclosure](#parental-disclosure)</li><li> [Providing opportunities to learn more about how the avatar was made](#providing-opportunities-to-learn-more-about-how-the-avatar-was-made)</li></ul> |
|Implicit disclosure patterns | <ul><li>[Capability Disclosure](#capability-disclosure)</li><li>[Implicit Cues and Feedback](#implicit-cues-and-feedback)</li><li> [Conversational Transparency](#conversational-transparency)</li></ul> |


Because all text to speech avatars require High Disclosure, we recommend using at least one explicit pattern paired with implicit cues up front to help users build accurate associations.

Some other conditions may also apply to your scenario. You can refer to the design patterns in the following table. 

| If your text to speech avatar experience… | Recommendations | Design patterns |
| --- | --- | --- |
| Has a high level of engagement | Build for the long term and offer multiple entry points to disclosure along the user journey. It is highly recommended to have an onboarding experience.  | <ul><li>[Transparent Introduction](#transparent-introduction)</li><li>[Explicit byline](#explicit-byline)</li><li>[Capability Disclosure](#capability-disclosure)</li></ul> |
| Includes children as the primary intended audience  | Target parents as the primary disclosure audience and ensure that they can effectively communicate disclosure to children. | <ul><li> [Parental Disclosure](#parental-disclosure)</li><li>[Verbal Transparent Introduction](#verbal-transparent-introduction)</li><li> [Implicit Disclosure](#implicit-disclosure)</li><li> [Conversational Transparency](#conversational-transparency) </li></ul> |
| Includes blind users or people with low vision as the primary intended audience  | Be inclusive of all users and ensure that any form of visual disclosure has associated alternative text or sound effects. Adhere to accessibility standards for contrast ratio and display size. Use auditory cues to communicate disclosure.   | <ul><li>[Verbal Transparent Introduction](#verbal-transparent-introduction) </li><li>[Conversational Transparency](#conversational-transparency)</li><li>[Accessibility Standards](https://www.microsoft.com/accessibility)</li></ul> |
| Potentially includes multiple users/listeners (e.g., personal assistant in multiple household)  | Be mindful of various user contexts and levels of understanding and offer multiple opportunities for disclosure in the user journey.   | <ul><li>[Transparent Introduction (Return User)](#transparent-introduction)</li><li> [Providing opportunities to learn more about how the avatar was made](#providing-opportunities-to-learn-more-about-how-the-avatar-was-made)</li><li> [Conversational Transparency](#conversational-transparency) </li></ul> |

## Explicit disclosure

It's best to use at least one of the following explicit patterns to clearly state the synthetic nature of a text to speech avatar. 

### Transparent introduction 

Before the avatar experience begins, introduce the digital assistant by being fully transparent about the origins of its image, voice, and its capabilities. The optimal moment to use this pattern is when onboarding a new user or when introducing new features to a returning user. Implementing implicit cues during an introduction helps users form a mental model about the synthetic nature of the digital agent.

#### First-time user experience

![A diagram of transparent introduction during first run experience.](media\transparent-intro-first-avatar.png) </br>
*The text to speech avatar is introduced while onboarding a new user.*

Recommendations
- Describe that the human image is artificial (e.g. "digital") 
- Describe what the agent is capable of doing 
- Explicitly state the avatar and voice's origins 
- Offer an entry point to learn more about the synthetic technology 

#### Returning user experience

If a user skips the onboarding experience, continue to offer entry points to the Transparent Introduction experience until the user triggers the avatar for the first time. 

![A diagram of Transparent introduction during return user experience.](media\transparent-intro-return-avatar.png)
<br/>*Provide a consistent entry point to the text to speech avatar experience. Allow the user to return to the onboarding experience when they trigger the avatar for the first time at any point in the user journey.*


### Verbal transparent introduction

A spoken prompt stating the origins of the digital assistant's image and voice is explicit enough on its own to achieve disclosure.

![A diagram of Verbally spoken transparent introduction.](media\verbal-transparent.png)

### Explicit byline

Use this pattern if the user will be interacting with a video player or interactive component to trigger the avatar.

![A diagram of explicit byline in a news media scenario.](media\explicit-byline-2.png) <br/>
*An explicit byline is the attribution of where image and voice came from.*

Recommendations
- Offer entry point to learn more about the synthesized technology


### Parental Disclosure

In addition to complying with COPPA regulations, provide disclosure to parents if your primary intended audience is young children. For sensitive uses, consider gating the experience until an adult has acknowledged the use of the synthetic voice. Encourage parents to communicate the message to their children.

![A screenshot of Disclosure for parents.](media\parent-disclosure-avatar.png)<br/>
*A transparent introduction optimized for parents ensures that an adult was made aware of the synthetic nature of the avatar before a child interacts with it.*

Recommendations
- Target parents as the primary audience for disclosure 
- Encourage parents to communicate disclosure to their children 
- Offer entry points to learn more about the synthesized technology 
- Gate the experience by asking parents a simple "safeguard" question to show they have read the disclosure 


### Providing opportunities to learn more about how the avatar was made

Offer context-sensitive entry points to a page, pop-up, or external site that provides more information about the text to speech avatar technology. For example, you could surface a link to learn more during onboarding or when the user prompts for more information during conversation.

![A screenshot of entry point to learn more](media\learn-more-entry-point-avatar.png)<br/>
*Example of an entry point to offer the opportunity to learn more about the synthesized technology.*

Once a user requests more information about the synthetic avatar and voice, the primary goal is to educate them about the origins of the synthetic technology and to be transparent about it.

![A screenshot of providing users more information about synthetic voice.](media\learn-more.png)<br/>
*More information can be offered in an external help site.*

Recommendations
- Simplify complex concepts and avoid using legalese and technical jargon 
- Don't bury this content in privacy and terms of use statements 
- Keep content concise and use imagery when available 

## Implicit disclosure

Consistency is the key to achieving disclosure implicitly throughout the user journey. Consistent use of visual and auditory cues across devices and modes of interaction can help build associations between implicit patterns and explicit disclosure.

![A diagram of Consistency of implicit cues.](media\consistency.png)

### Implicit cues and feedback

Anthropomorphism can manifest in different ways, from the actual visual representation of the agent, to the voice, sounds, patterns of light, bouncing shapes, or even the vibration of a device. When defining your persona, leverage implicit cues and feedback patterns rather than aim for a very human-like avatar. This is one way to minimize the need for more explicit disclosure.

![A diagram of Visual cues and feedback.](media\visual-affordances.png)<br/>
*These cues help anthropomorphize the agent without being too human-like. They can also become effective disclosure mechanisms on their own when used consistently over time.*

Consider the different modes of interactions of your experience when incorporating the following types of cues:

|Category| Examples|
|--|--|
| Visual Cues  | <ul><li>Avatar</li><li>Responsive real-time cues (e.g., animations)</li><li> Non-screen cues (e.g., lights and patterns on a device)</li></ul> |
|Auditory Cues   | <ul><li>Sonicon (e.g., a brief distinctive sound, series of musical notes)</li></ul> |
|Haptic Cues |  <ul><li>Vibration</li></ul> | 

### Capability disclosure

Disclosure can be achieved implicitly by setting accurate expectations for what the digital assistant is capable of. Provide sample commands so that users can learn how to interact with the digital assistant and offer contextual help to learn more about the text to speech avatar during the early stages of the experience.

![A screenshot of Example of default responses to a conversation that you can craft.](media\capability-disclosure.png)<br/>

### Conversational Transparency

When conversations fall in unexpected paths, consider crafting default responses that can help reset expectations, reinforce transparency, and steer users towards successful paths. There are opportunities to use explicit disclosure in conversation as well.

For example, when asked a question that hard to be answered by AI, the avatar can say, “Sorry, I can’t help you with that, perhaps a real human can. Would you like me to connect you to customer service?”


## Additional resources

- [Microsoft Bot Guidelines](https://www.microsoft.com/research/uploads/prod/2018/11/Bot_Guidelines_Nov_2018.pdf)
- [Microsoft Windows UWP Speech Design Guidelines](/windows/uwp/design/input/speech-interactions)
- [Microsoft Windows Mixed Reality Voice Commanding Guidelines](/windows/mixed-reality/voice-design#top-things-users-should-know-about-speech-in-mixed-reality)

## See also

* [Disclosure for voice and avatar talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent)
* [Guidelines for responsible deployment of synthetic voice technology](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)
* [How to disclose](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines)
