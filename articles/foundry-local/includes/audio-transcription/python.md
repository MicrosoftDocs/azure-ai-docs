---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 07/17/2025
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [Python 3.11](https://www.python.org/downloads/) or later installed.

## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd python/audio-transcription
```

## Install packages

[!INCLUDE [project-setup](../python-project-setup.md)]

## Transcribe an audio file

Copy and paste the following code into a Python file named `app.py`:

:::code language="python" source="~/foundry-local-main/samples/python/audio-transcription/src/app.py" id="complete_code":::

The sample includes a `Recording.mp3` file. To transcribe a different audio file, pass the file path as an argument.

## Run the application

Run the code by using the following command:

```bash
python app.py
```

To transcribe a custom audio file:

```bash
python app.py path/to/audio.mp3
```
