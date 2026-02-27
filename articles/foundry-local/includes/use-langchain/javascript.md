---
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

- **Foundry Local** installed on your computer. Read the [Get started with Foundry Local](../../get-started.md) guide for installation instructions.
- **Node.js 18 or later** installed on your computer. You can download Node.js from the [official website](https://nodejs.org/).

## Install Node.js packages

You need to install the following Node.js packages:

```bash
npm install @langchain/openai @langchain/core
npm install foundry-local-sdk
```

This example uses ES modules (`import`) and top-level `await`. If you haven't already, initialize a Node.js project and enable ES modules:

```bash
npm init -y
```

In your `package.json`, set:

```json
{
    "type": "module"
}
```

## Create a translation application

Create a new JavaScript file named `translation_app.js` in your favorite IDE and add the following code:

```javascript
import { FoundryLocalManager } from "foundry-local-sdk";
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";

// By using an alias, the most suitable model will be downloaded 
// to your end-user's device.
// TIP: You can find a list of available models by running the 
// following command in your terminal: `foundry model list`.
const alias = "phi-3-mini-4k";

// Create a FoundryLocalManager instance. This will start the Foundry 
// Local service if it is not already running.
const foundryLocalManager = new FoundryLocalManager()

// Initialize the manager with a model. This will download the model 
// if it is not already present on the user's device.
const modelInfo = await foundryLocalManager.init(alias)
console.log("Model Info:", modelInfo)

// Configure ChatOpenAI to use your locally-running model
const llm = new ChatOpenAI({
    model: modelInfo.id,
    configuration: {
        baseURL: foundryLocalManager.endpoint,
        apiKey: foundryLocalManager.apiKey
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
chain.invoke({
    input_language: "English",
    output_language: "French",
    input: input
}).then(aiMsg => {
    // Print the result content
    console.log(`Response: ${aiMsg.content}`);
}).catch(err => {
    console.error("Error:", err);
});
```

#### References

- Reference: [Foundry Local SDK reference](../../reference/reference-sdk.md)
- Reference: [Get started with Foundry Local](../../get-started.md)

> [!NOTE]
> One of the key benefits of Foundry Local is that it **automatically** selects the most suitable model **variant** for the user's hardware. For example, if the user has a GPU, it downloads the GPU version of the model. If the user has an NPU (Neural Processing Unit), it downloads the NPU version. If the user doesn't have either a GPU or NPU, it downloads the CPU version of the model.

## Run the application

To run the application, open a terminal and navigate to the directory where you saved the `translation_app.js` file. Then, run the following command:

```bash
node translation_app.js
```

You're done when you see a `Response:` line with the translated text.

You should see output similar to:

```text
Model Info: { ... }
Translating 'I love to code.' to French...
Response: <translated text>
```
