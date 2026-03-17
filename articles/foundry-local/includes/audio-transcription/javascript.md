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
- A local audio file in a supported format (for example, MP3, WAV, FLAC).

## Samples repository

You can find the sample in this article in the [Foundry Local SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Create project

[!INCLUDE [project-setup](../javascript-project-setup.md)]

## Transcribe an audio file
The following example demonstrates how to use the native audio transcription API in Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration` object.
1. Gets a `Model` object from the model catalog using an alias. Foundry Local automatically selects the best variant for the model based on the available hardware of the host machine.
1. Downloads and loads the model variant.
1. Uses the native audio transcription API to generate a response.
1. Unloads the model.

Copy and paste the following code into a JavaScript file named `app.js`:

```javascript
import { FoundryLocalManager } from 'foundry-local-sdk';

// Initialize the Foundry Local SDK
console.log('Initializing Foundry Local SDK...');

const manager = FoundryLocalManager.create({
    appName: 'foundry_local_samples',
    logLevel: 'info'
});
console.log('✓ SDK initialized successfully');

// Get the model object
const modelAlias = 'whisper-tiny'; // Using an available model from the list above
let model = await manager.catalog.getModel(modelAlias);
console.log(`Using model: ${model.id}`);

// Download the model
console.log(`\nDownloading model ${modelAlias}...`);
await model.download((progress) => {
    process.stdout.write(`\rDownloading... ${progress.toFixed(2)}%`);
});
console.log('\n✓ Model downloaded');

// Load the model
console.log(`\nLoading model ${modelAlias}...`);
await model.load();
console.log('✓ Model loaded');

// Create audio client
console.log('\nCreating audio client...');
const audioClient = model.createAudioClient();
console.log('✓ Audio client created');

// Example audio transcription
console.log('\nTesting audio transcription...');
const transcription = await audioClient.transcribe('./Recording.mp3');

console.log('\nAudio transcription result:');
console.log(transcription.text);

// Unload the model
console.log('Unloading model...');
await model.unload();
console.log(`✓ Model unloaded`);
```

## Run the application
To run the application, use the following command in your terminal:

```bash
node app.js
```