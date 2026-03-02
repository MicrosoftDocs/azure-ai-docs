---
title: What is the Speech CLI? - Azure Speech in Foundry Tools
titleSuffix: Foundry Tools
description: Learn about the Speech CLI, a command-line tool for using Azure Speech in Foundry Tools without writing code. Run speech recognition, synthesis, and translation from the command line.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 02/25/2026
ms.author: pafarley
#Customer intent: As a developer, I want to learn about the Speech CLI, a command-line tool for using Speech service without having to write any code.
---

# What is the Azure Speech in Foundry Tools CLI?

The Speech CLI is a command-line tool for using Azure Speech in Foundry Tools without writing code. The Speech CLI requires minimal setup, and you can start experimenting with key features of the Speech service right away. Within minutes, run simple test workflows like batch speech recognition from a directory of files, or text to speech on a collection of strings from a file. Beyond simple workflows, the Speech CLI is production-ready. Scale it up to run larger processes by using automated `.bat` or shell scripts.

Most features in the Speech SDK are available in the Speech CLI, and some advanced features and customizations are simplified. Consider the following guidance when choosing between the Speech CLI and the Speech SDK.

Use the Speech CLI when:
* You want to experiment with Speech service features with minimal setup and no code.
* You have relatively simple requirements for a production application that uses the Speech service.

Use the Speech SDK when:
* You want to integrate Speech service functionality within a specific language or platform (for example, C#, Python, or C++).
* You have complex requirements that might require advanced service requests.
* You're developing custom behavior, including response streaming.

## Core features

* **Speech recognition**: Convert speech to text from audio files or directly from a microphone, or transcribe a recorded conversation.

* **Speech synthesis**: Convert text to speech from text files or directly from the command line. Customize speech output characteristics by using [Speech Synthesis Markup Language (SSML) configurations](speech-synthesis-markup.md).

* **Speech translation**: Translate audio in a source language to text or audio in a target language.

* **Azure compute**: Send Speech CLI commands to run on an Azure remote compute resource by using `spx webjob`.

## Get started

To get started with the Speech CLI, see the [quickstart](spx-basics.md). The article shows you how to run basic commands and gives you slightly more advanced commands for running batch operations for speech to text and text to speech. After reading the basics article, you have enough understanding of the syntax to write custom commands or automate simple Speech service operations.

## Next steps

- [Get started with the Azure Speech CLI](spx-basics.md)
- [Speech CLI configuration options](./spx-data-store-configuration.md)
- [Speech CLI batch operations](./spx-batch-operations.md)
