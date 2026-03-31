---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/06/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [Node.js](https://nodejs.org/en/download/) version 20 or later installed.

## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd js/audio-transcription-example
```

## Install packages

[!INCLUDE [project-setup](../javascript-project-setup.md)]

## Transcribe an audio file
The following example demonstrates how to use the native audio transcription API in Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration` object.
1. Gets a `Model` object from the model catalog using an alias. Foundry Local automatically selects the best variant for the model based on the available hardware of the host machine.
1. Downloads and loads the model variant.
1. Uses the native audio transcription API to generate a response.
1. Unloads the model.

Copy and paste the following code into a JavaScript file named `app.js`:

:::code language="javascript" source="~/foundry-local-main/samples/js/audio-transcription-example/app.js" id="complete_code":::

The sample includes a `Recording.mp3` file. To transcribe a different audio file, pass the file path as an argument.

## Run the application
To run the application, use the following command in your terminal:

```bash
node app.js
```

To transcribe a custom audio file:

```bash
node app.js path/to/audio.mp3
```