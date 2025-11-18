---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 9/5/2024
ms.author: pafarley
---

In this how-to guide, you can use Azure Speech in Foundry Tools to converse with Azure OpenAI in Microsoft Foundry Models. The text recognized by the Speech service is sent to Azure OpenAI. The Speech service synthesizes speech from the text response from Azure OpenAI.

Speak into the microphone to start a conversation with Azure OpenAI.

- The Speech service recognizes your speech and converts it into text (speech to text).
- Your request as text is sent to Azure OpenAI.
- The Speech service text to speech feature synthesizes the response from Azure OpenAI to the default speaker.

Although the experience of this example is a back-and-forth exchange, Azure OpenAI doesn't remember the context of your conversation.

