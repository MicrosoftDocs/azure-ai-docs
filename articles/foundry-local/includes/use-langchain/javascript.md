---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.topic: include
ms.date: 05/02/2025
ms.author: jburchel
ms.reviewer: maanavd
reviewer: maanavdalal
author: jonburchel
ai-usage: ai-assisted
---

## Prerequisites

Before starting this tutorial, you need:

- **Node.js 20 or later** installed on your computer. You can download Node.js from the [official website](https://nodejs.org/).

## Set up project

[!INCLUDE [project-setup](../javascript-project-setup.md)]

### Install LangChain packages

You also need to install the following Node.js packages:

```bash
npm install @langchain/openai @langchain/core
```

## Create a translation application

Create a new JavaScript file named `translation_app.js` in your favorite IDE and add the following code:

```javascript
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { FoundryLocalManager } from 'foundry-local-sdk';

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
model.selectVariant('qwen2.5-0.5b-instruct-generic-cpu:4');

// Download the model
console.log(`\nDownloading model ${modelAlias}...`);
await model.download();
console.log('✓ Model downloaded');

// Load the model
console.log(`\nLoading model ${modelAlias}...`);
await model.load();
console.log('✓ Model loaded');

// Start the web service
console.log('\nStarting web service...');
manager.startWebService();
console.log('✓ Web service started');


// Configure ChatOpenAI to use your locally-running model
const llm = new ChatOpenAI({
    model: model.id,
    configuration: {
        baseURL: endpointUrl + '/v1',
        apiKey: 'notneeded'
    },
    temperature: 0.6,
    streaming: false
});

// Create a translation prompt template
const prompt = ChatPromptTemplate.fromMessages([
    {
        role: "system",
        content: "You are a helpful assistant that translates {input_language} to {output_language}."
    },
    {
        role: "user",
        content: "{input}"
    }
]);

// Build a simple chain by connecting the prompt to the language model
const chain = prompt.pipe(llm);

const input = "I love to code.";
console.log(`Translating '${input}' to French...`);

// Run the chain with your inputs
await chain.invoke({
    input_language: "English",
    output_language: "French",
    input: input
}).then(aiMsg => {
    // Print the result content
    console.log(`Response: ${aiMsg.content}`);
}).catch(err => {
    console.error("Error:", err);
});

// Tidy up
console.log('Unloading model and stopping web service...');
await model.unload();
manager.stopWebService();
console.log(`✓ Model unloaded and web service stopped`);
```

### Run the application

To run the application, open a terminal and navigate to the directory where you saved the `translation_app.js` file. Then, run the following command:

```bash
node translation_app.js
```

You're done when you see a `Response:` line with the translated text.

You should see output similar to:

```text
Translating 'I love to code.' to French...
Response: J'aime le coder
```
