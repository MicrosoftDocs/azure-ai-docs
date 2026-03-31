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

## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd rust/audio-transcription-example
```

## Install packages

[!INCLUDE [project-setup](../rust-project-setup.md)]

## Transcribe an audio file

Replace the contents of `main.rs` with the following code:

:::code language="rust" source="~/foundry-local-main/samples/rust/audio-transcription-example/src/main.rs" id="complete_code":::

The sample includes a `Recording.mp3` file. To transcribe a different audio file, pass the file path as an argument.

## Run the application

Run the code by using the following command:

```bash
cargo run
```

To transcribe a custom audio file:

```bash
cargo run -- path/to/audio.mp3
```
