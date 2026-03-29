---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

[!INCLUDE [JavaScript project setup](../javascript-project-setup.md)]

## Define tools

Tool calling lets the model request that your code runs a function and returns the result. You define the available tools as a list of JSON schemas that describe each function's name, purpose, and parameters.

1. Create a file called `index.js`.

1. Add the following tool definitions:

    ```javascript
    // Define tools the model can call
    const tools = [
        {
            type: 'function',
            function: {
                name: 'get_weather',
                description: 'Get the current weather for a location',
                parameters: {
                    type: 'object',
                    properties: {
                        location: {
                            type: 'string',
                            description: 'The city or location'
                        },
                        unit: {
                            type: 'string',
                            enum: ['celsius', 'fahrenheit'],
                            description: 'Temperature unit'
                        }
                    },
                    required: ['location']
                }
            }
        },
        {
            type: 'function',
            function: {
                name: 'calculate',
                description: 'Perform a math calculation',
                parameters: {
                    type: 'object',
                    properties: {
                        expression: {
                            type: 'string',
                            description:
                                'The math expression to evaluate'
                        }
                    },
                    required: ['expression']
                }
            }
        }
    ];
    ```

    Each tool definition includes a `name`, a `description` that helps the model decide when to use it, and a `parameters` schema that describes the expected input.

1. Add the JavaScript functions that implement each tool:

    ```javascript
    function getWeather(location, unit = 'celsius') {
        return {
            location,
            temperature: unit === 'celsius' ? 22 : 72,
            unit,
            condition: 'Sunny'
        };
    }

    function calculate(expression) {
        const allowed = /^[0-9+\-*/(). ]+$/;
        if (!allowed.test(expression)) {
            return { error: 'Invalid expression' };
        }
        try {
            const result = Function(
                `"use strict"; return (${expression})`
            )();
            return { expression, result };
        } catch (err) {
            return { error: err.message };
        }
    }

    // Map tool names to functions
    const toolFunctions = {
        get_weather: (args) => getWeather(args.location, args.unit),
        calculate: (args) => calculate(args.expression)
    };
    ```

    The model doesn't run these functions directly. It returns a tool call request with the function name and arguments, and your code executes the function.

## Send a message that triggers tool use

Initialize the Foundry Local SDK, load a model, and send a message that the model can answer by calling a tool.

```javascript
import { FoundryLocalManager } from 'foundry-local-sdk';

// Initialize the Foundry Local SDK
const manager = FoundryLocalManager.create({
    appName: 'tool-calling-app',
    logLevel: 'info'
});

// Select and load a model
const model = await manager.catalog.getModel('phi-3.5-mini');

await model.download((progress) => {
    process.stdout.write(
        `\rDownloading model: ${progress.toFixed(2)}%`
    );
});
console.log('\nModel downloaded.');

await model.load();
console.log('Model loaded and ready.\n');

// Create a chat client
const chatClient = model.createChatClient();

// Start with a system prompt and a user message
const messages = [
    {
        role: 'system',
        content:
            'You are a helpful assistant with access to tools. ' +
            'Use them when needed to answer questions accurately.'
    },
    { role: 'user', content: "What's the weather like today?" }
];

// Send the request with tools
const response = await chatClient.completeChat(messages, { tools });
console.log('Response received.');
```

When the model determines that a tool is needed, the response contains `tool_calls` instead of a regular text message. The next step shows how to detect and handle these calls.

## Execute the tool and return results

After the model responds with a tool call, you extract the function name and arguments, run the function, and send the result back.

```javascript
const choice = response.choices[0]?.message;

// Check if the model wants to call a tool
if (choice?.tool_calls?.length > 0) {
    // Add the assistant's response (with tool calls) to the history
    messages.push(choice);

    for (const toolCall of choice.tool_calls) {
        const functionName = toolCall.function.name;
        const args = JSON.parse(toolCall.function.arguments);
        console.log(`Tool call: ${functionName}(${JSON.stringify(args)})`);

        // Execute the function
        const result = toolFunctions[functionName](args);

        // Add the tool result to the conversation
        messages.push({
            role: 'tool',
            tool_call_id: toolCall.id,
            content: JSON.stringify(result)
        });
    }

    // Send the updated conversation back to the model
    const finalResponse = await chatClient.completeChat(
        messages, { tools }
    );
    console.log(
        `Assistant: ${finalResponse.choices[0]?.message?.content}`
    );
} else {
    // No tool call — the model responded directly
    console.log(`Assistant: ${choice?.content}`);
}
```

The key steps in the tool calling loop are:

1. **Detect tool calls** — check `response.choices[0]?.message?.tool_calls`.
1. **Execute the function** — parse the arguments and call your local function.
1. **Return the result** — add a message with role `tool` and the matching `tool_call_id`.
1. **Get the final answer** — the model uses the tool result to generate a natural response.

## Handle the complete tool calling loop

Here's the complete application that combines tool definitions, SDK initialization, and the tool calling loop into a single runnable file.

Create a file named `index.js` and add the following complete code:

```javascript
import { FoundryLocalManager } from 'foundry-local-sdk';
import * as readline from 'readline';

// --- Tool definitions ---
const tools = [
    {
        type: 'function',
        function: {
            name: 'get_weather',
            description: 'Get the current weather for a location',
            parameters: {
                type: 'object',
                properties: {
                    location: {
                        type: 'string',
                        description: 'The city or location'
                    },
                    unit: {
                        type: 'string',
                        enum: ['celsius', 'fahrenheit'],
                        description: 'Temperature unit'
                    }
                },
                required: ['location']
            }
        }
    },
    {
        type: 'function',
        function: {
            name: 'calculate',
            description: 'Perform a math calculation',
            parameters: {
                type: 'object',
                properties: {
                    expression: {
                        type: 'string',
                        description:
                            'The math expression to evaluate'
                    }
                },
                required: ['expression']
            }
        }
    }
];

// --- Tool implementations ---
function getWeather(location, unit = 'celsius') {
    return {
        location,
        temperature: unit === 'celsius' ? 22 : 72,
        unit,
        condition: 'Sunny'
    };
}

function calculate(expression) {
    const allowed = /^[0-9+\-*/(). ]+$/;
    if (!allowed.test(expression)) {
        return { error: 'Invalid expression' };
    }
    try {
        const result = Function(
            `"use strict"; return (${expression})`
        )();
        return { expression, result };
    } catch (err) {
        return { error: err.message };
    }
}

const toolFunctions = {
    get_weather: (args) => getWeather(args.location, args.unit),
    calculate: (args) => calculate(args.expression)
};

async function processToolCalls(messages, response, chatClient) {
    let choice = response.choices[0]?.message;

    while (choice?.tool_calls?.length > 0) {
        messages.push(choice);

        for (const toolCall of choice.tool_calls) {
            const functionName = toolCall.function.name;
            const args = JSON.parse(toolCall.function.arguments);
            console.log(
                `  Tool call: ${functionName}` +
                `(${JSON.stringify(args)})`
            );

            const result = toolFunctions[functionName](args);
            messages.push({
                role: 'tool',
                tool_call_id: toolCall.id,
                content: JSON.stringify(result)
            });
        }

        response = await chatClient.completeChat(
            messages, { tools }
        );
        choice = response.choices[0]?.message;
    }

    return choice?.content ?? '';
}

// --- Main application ---
const manager = FoundryLocalManager.create({
    appName: 'tool-calling-app',
    logLevel: 'info'
});

const model = await manager.catalog.getModel('phi-3.5-mini');

await model.download((progress) => {
    process.stdout.write(
        `\rDownloading model: ${progress.toFixed(2)}%`
    );
});
console.log('\nModel downloaded.');

await model.load();
console.log('Model loaded and ready.');

const chatClient = model.createChatClient();

const messages = [
    {
        role: 'system',
        content:
            'You are a helpful assistant with access to tools. ' +
            'Use them when needed to answer questions accurately.'
    }
];

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const askQuestion = (prompt) =>
    new Promise((resolve) => rl.question(prompt, resolve));

console.log(
    '\nTool-calling assistant ready! Type \'quit\' to exit.\n'
);

while (true) {
    const userInput = await askQuestion('You: ');
    if (
        userInput.trim().toLowerCase() === 'quit' ||
        userInput.trim().toLowerCase() === 'exit'
    ) {
        break;
    }

    messages.push({ role: 'user', content: userInput });

    const response = await chatClient.completeChat(
        messages, { tools }
    );
    const answer = await processToolCalls(
        messages, response, chatClient
    );

    messages.push({ role: 'assistant', content: answer });
    console.log(`Assistant: ${answer}\n`);
}

await model.unload();
console.log('Model unloaded. Goodbye!');
rl.close();
```

## Run the application

Run the tool-calling assistant:

```bash
node index.js
```

You see output similar to:

```
Downloading model: 100.00%
Model downloaded.
Model loaded and ready.

Tool-calling assistant ready! Type 'quit' to exit.

You: What's the weather like today?
  Tool call: get_weather({"location":"current location"})
Assistant: The weather today is sunny with a temperature of 22°C.

You: What is 245 * 38?
  Tool call: calculate({"expression":"245 * 38"})
Assistant: 245 multiplied by 38 equals 9,310.

You: quit
Model unloaded. Goodbye!
```

The model decides when to call a tool based on the user's message. For a weather question it calls `get_weather`, for math it calls `calculate`, and for general questions it responds directly without any tool calls.
