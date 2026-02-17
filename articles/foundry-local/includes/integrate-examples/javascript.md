---
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

- Foundry Local installed and running. For installation instructions, see [Get started with Foundry Local](../../get-started.md).
- [Node.js](https://nodejs.org/en/download/) version 18 or later installed.

## Install Node.js packages

You need to install the following Node.js packages:

```bash
npm install openai
npm install foundry-local-sdk
```

The Foundry Local SDK allows you to manage the Foundry Local service and models.

## Use OpenAI SDK with Foundry Local

The following example demonstrates how to use the OpenAI SDK with Foundry Local. The code initializes the Foundry Local service, loads a model, and generates a response using the OpenAI SDK.

Copy-and-paste the following code into a JavaScript file named `app.mjs`:

```javascript
import { OpenAI } from "openai";
import { FoundryLocalManager } from "foundry-local-sdk";

// By using an alias, the most suitable model will be downloaded
// to your end-user's device.
// TIP: You can find a list of available models by running the
// following command in your terminal: `foundry model list`.
const alias = "qwen2.5-0.5b";

// Create a FoundryLocalManager instance. This will start the Foundry
// Local service if it is not already running.
const foundryLocalManager = new FoundryLocalManager();

// Initialize the manager with a model. This will download the model
// if it is not already present on the user's device.
const modelInfo = await foundryLocalManager.init(alias);
console.log("Model Info:", modelInfo);

const openai = new OpenAI({
  baseURL: foundryLocalManager.endpoint,
  apiKey: foundryLocalManager.apiKey,
});

async function generateText() {
  const response = await openai.chat.completions.create({
    model: modelInfo.id,
    messages: [
      {
        role: "user",
        content: "What is the golden ratio?",
      },
    ],
  });

  console.log(response.choices[0].message.content);
}

generateText();
```

Reference: [Foundry Local SDK reference](../../reference/reference-sdk.md)
Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

Run the code using the following command:

```bash
node app.mjs
```

You should see a text response printed in your terminal. On the first run, Foundry Local might download execution providers and the model, which can take a few minutes.

### Streaming Responses

If you want to receive streaming responses, you can modify the code as follows:

```javascript
import { OpenAI } from "openai";
import { FoundryLocalManager } from "foundry-local-sdk";

// By using an alias, the most suitable model will be downloaded
// to your end-user's device.
// TIP: You can find a list of available models by running the
// following command in your terminal: `foundry model list`.
const alias = "qwen2.5-0.5b";

// Create a FoundryLocalManager instance. This will start the Foundry
// Local service if it is not already running.
const foundryLocalManager = new FoundryLocalManager();

// Initialize the manager with a model. This will download the model
// if it is not already present on the user's device.
const modelInfo = await foundryLocalManager.init(alias);
console.log("Model Info:", modelInfo);

const openai = new OpenAI({
  baseURL: foundryLocalManager.endpoint,
  apiKey: foundryLocalManager.apiKey,
});

async function streamCompletion() {
  const stream = await openai.chat.completions.create({
    model: modelInfo.id,
    messages: [{ role: "user", content: "What is the golden ratio?" }],
    stream: true,
  });

  for await (const chunk of stream) {
    if (chunk.choices[0]?.delta?.content) {
      process.stdout.write(chunk.choices[0].delta.content);
    }
  }
}

streamCompletion();
```

Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

Run the code using the following command:

```bash
node app.mjs
```

You should see tokens stream to your terminal.

## Use Fetch API with Foundry Local

If you prefer to use an HTTP client like `fetch`, you can do so as follows:

```javascript
import { FoundryLocalManager } from "foundry-local-sdk";

// By using an alias, the most suitable model will be downloaded
// to your end-user's device.
// TIP: You can find a list of available models by running the
// following command in your terminal: `foundry model list`.
const alias = "qwen2.5-0.5b";

// Create a FoundryLocalManager instance. This will start the Foundry
// Local service if it is not already running.
const foundryLocalManager = new FoundryLocalManager();

// Initialize the manager with a model. This will download the model
// if it is not already present on the user's device.
const modelInfo = await foundryLocalManager.init(alias);
console.log("Model Info:", modelInfo);

async function queryModel() {
  const response = await fetch(
    foundryLocalManager.endpoint + "/chat/completions",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: modelInfo.id,
        messages: [{ role: "user", content: "What is the golden ratio?" }],
      }),
    }
  );

  const data = await response.json();
  console.log(data.choices[0].message.content);
}

queryModel();
```

Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

### Streaming Responses

If you want to receive streaming responses using the Fetch API, you can modify the code as follows:

```javascript
import { FoundryLocalManager } from "foundry-local-sdk";

// By using an alias, the most suitable model will be downloaded
// to your end-user's device.
// TIP: You can find a list of available models by running the
// following command in your terminal: `foundry model list`.
const alias = "qwen2.5-0.5b";

// Create a FoundryLocalManager instance. This will start the Foundry
// Local service if it is not already running.
const foundryLocalManager = new FoundryLocalManager();

// Initialize the manager with a model. This will download the model
// if it is not already present on the user's device.
const modelInfo = await foundryLocalManager.init(alias);
console.log("Model Info:", modelInfo);

async function streamWithFetch() {
  const response = await fetch(
    foundryLocalManager.endpoint + "/chat/completions",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "text/event-stream",
      },
      body: JSON.stringify({
        model: modelInfo.id,
        messages: [{ role: "user", content: "what is the golden ratio?" }],
        stream: true,
      }),
    }
  );

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split("\n").filter((line) => line.trim() !== "");

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const data = line.substring(6);
        if (data === "[DONE]") continue;

        try {
          const json = JSON.parse(data);
          const content = json.choices[0]?.delta?.content || "";
          if (content) {
            // Print to console without line breaks, similar to process.stdout.write
            process.stdout.write(content);
          }
        } catch (e) {
          console.error("Error parsing JSON:", e);
        }
      }
    }
  }
}

// Call the function to start streaming
streamWithFetch();
```

Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

