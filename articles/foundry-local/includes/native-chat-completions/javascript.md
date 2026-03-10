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
- [Node.js 20](https://nodejs.org/en/download/) or later installed.

## Samples repository

You can find the sample in this article in the [Foundry Local SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Setup project

[!INCLUDE [project-setup](./../javascript-project-setup.md)]

## Use native chat completions API

The following example demonstrates how to use the native chat completions API in Foundry Local. The benefit of using the native chat completions API is there's no need for a REST web server running and therefore it provides a simplified deployment. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a configuration.
1. Gets a `Model` object from the model catalog using an alias.
1. Downloads and loads the model variant.
1. Uses the native chat completions API to generate a response.
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
const modelAlias = 'qwen2.5-0.5b'; // Using an available model from the list above
const model = await manager.catalog.getModel(modelAlias);

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

// Create chat client
console.log('\nCreating chat client...');
const chatClient = model.createChatClient();
console.log('✓ Chat client created');

// Example chat completion
console.log('\nTesting chat completion...');
const completion = await chatClient.completeChat([
    { role: 'user', content: 'Why is the sky blue?' }
]);

console.log('\nChat completion result:');
console.log(completion.choices[0]?.message?.content);

// Example streaming completion
console.log('\nTesting streaming completion...');
await chatClient.completeStreamingChat(
    [{ role: 'user', content: 'Write a short poem about programming.' }],
    (chunk) => {
        const content = chunk.choices?.[0]?.message?.content;
        if (content) {
            process.stdout.write(content);
        }
    }
);
console.log('\n');

// Unload the model
console.log('Unloading model...');
await model.unload();
console.log(`✓ Model unloaded`);
```

## Run the code

Run the code by using the following command:

```bash
node app.js
```