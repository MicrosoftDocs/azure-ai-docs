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

## Set up project

[!INCLUDE [project-setup](./../javascript-project-setup.md)]

## Understanding tool choice settings

When using tool calling with Foundry Local, the tool choice parameter controls whether and how the model invokes the tools you provide. It is sent as part of the chat completion request alongside your tool definitions.

Different models have different capabilities when it comes to tool calling, but in general you can expect the following behavior for each option:

| Option | Value | Behavior | Reliability |
|--------|-------|----------|-------------|
| **Auto** | `"auto"` | The model decides whether to call a tool or respond directly, based on the user's message and the available tool definitions. | Reliable across all tool-calling models |
| **None** | `"none"` | The model will not call any tools, even if tools are provided in the request. | Reliable across all tool-calling models |
| **Required** | `"required"` | The model must call at least one tool. It will not return a plain text response. | Best-effort — may be ignored by smaller models |
| **Specific function** | `{"type": "function", "function": {"name": "my_function"}}` | The model must call the specified function. | Best-effort — may be ignored by smaller models |

## Use chat completions with tool calling

Copy and paste the following code into a JavaScript file named `app.js`:

```javascript
import { OpenAI } from "openai";
import { FoundryLocalManager } from "foundry-local-sdk";

// By using an alias, the most suitable model will be downloaded 
// to your end-user's device.
// TIP: You can find a list of available models by running the 
// following command in your terminal: `foundry model list`.
const alias = "qwen2.5-0.5b";

function multiplyNumbers(first, second) {
  return first * second;
}

async function runToolCallingExample() {
  let manager = null;
  let model = null;

  try {
    console.log("Initializing Foundry Local SDK...");
    manager = FoundryLocalManager.create({
      appName: "FoundryLocalSample",
      webServiceUrls: "http://localhost:5000",
      logLevel: "info"
    });

    const catalog = manager.catalog;
    model = await catalog.getModel(alias);
    if (!model) {
      throw new Error(`Model ${alias} not found`);
    }

    // Download the model
    console.log(`\nDownloading model ${model.id}...`);
    await model.download((progress) => {
        process.stdout.write(`\rDownloading... ${progress.toFixed(2)}%`);
    });
    console.log('\n✓ Model downloaded');

    console.log(`Loading model ${model.id}...`);
    await model.load();
    console.log('✓ Model loaded');

    manager.startWebService();
    const endpoint = manager.urls[0];
    if (!endpoint) {
      throw new Error("Foundry Local web service did not return an endpoint.");
    }

    const openai = new OpenAI({
      baseURL: `${endpoint.replace(/\/$/, "")}/v1`,
      apiKey: "local"
    });

    // Prepare messages
    const messages = [
      {
        role: "system",
        content: "You are a helpful AI assistant. If necessary, you can use any provided tools to answer the question."
      },
      { role: "user", content: "What is the answer to 7 multiplied by 6?" }
    ];

    // Prepare tools
    const tools = [
      {
        type: "function",
        function: {
          name: "multiply_numbers",
          description: "A tool for multiplying two numbers.",
          parameters: {
            type: "object",
            properties: {
              first: {
                type: "integer",
                description: "The first number in the operation"
              },
              second: {
                type: "integer",
                description: "The second number in the operation"
              }
            },
            required: ["first", "second"]
          }
        }
      }
    ];

    // Start the conversation
    console.log("Chat completion response:");
    const toolCallResponses = [];

    const firstStream = await openai.chat.completions.create({
      model: model.id,
      messages,
      tools,
      tool_choice: "required", // force the model to make a tool call
      stream: true
    });

    for await (const chunk of firstStream) {
      const content = chunk.choices?.[0]?.delta?.content;
      if (content) {
        process.stdout.write(content);
      }

      if (chunk.choices?.[0]?.finish_reason === "tool_calls") {
        toolCallResponses.push(chunk);
      }
    }
    console.log();

    // Invoke tools called and append responses to the chat
    for (const chunk of toolCallResponses) {
      const toolCalls = chunk.choices?.[0]?.message?.tool_calls ?? chunk.choices?.[0]?.delta?.tool_calls ?? [];
      for (const toolCall of toolCalls) {
        if (toolCall.function?.name === "multiply_numbers") {
          const args = JSON.parse(toolCall.function.arguments || "{}");
          const first = args.first;
          const second = args.second;

          console.log(`\nInvoking tool: ${toolCall.function.name} with arguments ${first} and ${second}`);
          const result = multiplyNumbers(first, second);
          console.log(`Tool response: ${result}`);

          messages.push({
            role: "tool",
            tool_call_id: toolCall.id,
            content: result.toString()
          });
        }
      }
    }

    console.log("\nTool calls completed. Prompting model to continue conversation...\n");

    // Prompt the model to continue the conversation after the tool call
    messages.push({
      role: "system",
      content: "Respond only with the answer generated by the tool."
    });

    // Run the next turn of the conversation
    console.log("Chat completion response:");
    const secondStream = await openai.chat.completions.create({
      model: model.id,
      messages,
      tools,
      tool_choice: "auto", // now allow the model to decide whether to call more tools or respond with text
      stream: true
    });

    for await (const chunk of secondStream) {
      const content = chunk.choices?.[0]?.delta?.content;
      if (content) {
        process.stdout.write(content);
      }
    }

    console.log();
  } finally {
    if (model) {
      try {
        if (await model.isLoaded()) {
          await model.unload();
        }
      } catch (cleanupError) {
        console.warn("Cleanup warning while unloading model:", cleanupError);
      }
    }

    if (manager) {
      try {
        manager.stopWebService();
      } catch (cleanupError) {
        console.warn("Cleanup warning while stopping service:", cleanupError);
      }
    }
  }
}

await runToolCallingExample().catch((error) => {
  console.error("Error running sample:", error);
  process.exitCode = 1;
});
```

## Run the application

To run the application, execute the following command in your terminal:

```bash
node app.js
```
