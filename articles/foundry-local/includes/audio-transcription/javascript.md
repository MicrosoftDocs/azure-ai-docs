---
title: Include file
description: Include file
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/15/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [Node.js](https://nodejs.org/en/download/) version 20 or later installed.

## Samples repository

The complete sample code for this article is available in the [foundry-samples GitHub repository](https://github.com/microsoft-foundry/foundry-samples). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
cd foundry-samples/samples/javascript/foundry-local/audio-transcription-example
```

## Install packages

[!INCLUDE [project-setup](../javascript-project-setup.md)]

## Transcribe an audio file

Copy and paste the following code into a JavaScript file named `app.js`:

:::code language="javascript" source="~/foundry-local-main/samples/javascript/foundry-local/audio-transcription-example/app.js" id="complete_code":::

The sample includes a `Recording.mp3` file. To transcribe a different audio file, pass the file path as an argument.

To run the application, use the following command in your terminal:

```bash
node app.js
```

To transcribe a custom audio file:

```bash
node app.js path/to/audio.mp3
```
