---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.topic: include
ms.date: 01/06/2026
ms.author: jburchel
reviewer: maanavdalal
author: jonburchel
ms.reviewer: maanavd
ai-usage: ai-assisted
---

## Prerequisites

- [Node.js](https://nodejs.org/en/download/) version 20 or later installed.

## Set up project

[!INCLUDE [project-setup](./../javascript-project-setup.md)]


## Use OpenAI SDK with Foundry Local

Install the OpenAI SDK package:

```bash
npm install openai
```

The following example demonstrates how to use the OpenAI SDK with Foundry Local's optional web service that is compatible with the OpenAI API. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a configuration that includes the web service URL.
1. Gets a `Model` object from the model catalog using an alias.
1. Downloads and loads the model variant.
1. Starts the Foundry Local web service.
1. Uses the OpenAI SDK to generate a chat completion.
1. Unloads the model and stops the web service.

Copy-and-paste the following code into a JavaScript file named `app.js`:

```javascript
import { FoundryLocalManager } from 'foundry-local-sdk';
import { OpenAI } from 'openai';

// Initialize the Foundry Local SDK
console.log('Initializing Foundry Local SDK...');

const endpointUrl = 'http://localhost:5764';

const manager = FoundryLocalManager.create({
    appName: 'foundry_local_samples',
    logLevel: 'info',
    webServiceUrls: endpointUrl
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

// Start the web service
console.log('\nStarting web service...');
manager.startWebService();
console.log('✓ Web service started');

const openai = new OpenAI({
    baseURL: endpointUrl + '/v1',
    apiKey: 'notneeded',
});

// Example chat completion
console.log('\nTesting chat completion with OpenAI client...');
const response = await openai.chat.completions.create({
    model: model.id,
    messages: [
    {
        role: "user",
        content: "What is the golden ratio?",
    },
    ],
});

console.log(response.choices[0].message.content);

// Tidy up
console.log('Unloading model and stopping web service...');
await model.unload();
manager.stopWebService();
console.log(`✓ Model unloaded and web service stopped`);

```

## Use Fetch API with Foundry Local

If you prefer to use an HTTP client like `fetch`, you can do so as follows:

```javascript
import { FoundryLocalManager } from 'foundry-local-sdk';

// Initialize the Foundry Local SDK
console.log('Initializing Foundry Local SDK...');

const config = {
    appName: 'foundry_local_samples',
    logLevel: 'info',
    webServiceUrls: 'http://localhost:5764'
};

const manager = FoundryLocalManager.create(config);
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

// Start the web service
console.log('\nStarting web service...');
manager.startWebService();
console.log('✓ Web service started');
        
async function queryModel() {
  const response = await fetch(
    config.webServiceUrls + "/v1/chat/completions",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: model.id,
        messages: [{ role: "user", content: "What is the golden ratio?" }],
      }),
    }
  );

  const data = await response.json();
  console.log(data.choices[0].message.content);
}


await queryModel();

// Tidy up
console.log('Unloading model and stopping web service...');
await model.unload();
manager.stopWebService();
console.log(`✓ Model unloaded and web service stopped`);
```
