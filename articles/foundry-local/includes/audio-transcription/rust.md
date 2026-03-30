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

- [Rust and Cargo](https://www.rust-lang.org/tools/install) installed (Rust 1.70.0 or later).
- A local audio file to transcribe in a supported format (for example, MP3, WAV, or FLAC).

## Samples repository

You can find the sample in this article in the [Foundry Local SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Create project

[!INCLUDE [project-setup](../rust-project-setup.md)]

## Transcribe an audio file

The following example demonstrates how to use the native audio transcription API in Foundry Local. The code includes the following steps:

1. Creates a `FoundryLocalManager` instance with a `FoundryLocalConfig`.
1. Gets a `Model` object from the model catalog using an alias. Foundry Local automatically selects the best variant for the model based on the available hardware of the host machine.
1. Downloads and loads the model variant.
1. Uses the native audio transcription API to transcribe an audio file.
1. Unloads the model.

Replace the contents of `src/main.rs` with the following code:

:::code language="rust" source="~/foundry-local-main/samples/rust/audio-transcription-example/src/main.rs" id="complete_code":::

> [!NOTE]
> Replace `"Recording.mp3"` with the path to the audio file that you want to transcribe.

## Run the application

Run the code by using the following command:

```bash
cargo run
```
