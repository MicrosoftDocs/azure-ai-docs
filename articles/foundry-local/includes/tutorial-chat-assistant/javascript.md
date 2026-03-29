---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

[!INCLUDE [JavaScript project setup](../javascript-project-setup.md)]

## Browse the catalog and select a model

The Foundry Local SDK provides a model catalog that lists all available models. In this step, you initialize the SDK and select a model for your chat assistant.

1. Create a file called `index.js`.

1. Add the following code to initialize the SDK and select a model:

    ```javascript
    import { FoundryLocalManager } from 'foundry-local-sdk';
    import * as readline from 'readline';

    // Initialize the Foundry Local SDK
    const manager = FoundryLocalManager.create({
        appName: 'chat-assistant',
        logLevel: 'info'
    });

    // Select a model from the catalog
    const model = await manager.catalog.getModel('phi-3.5-mini');

    // Download the model (skips if already cached)
    await model.download((progress) => {
        process.stdout.write(`\rDownloading model: ${progress.toFixed(2)}%`);
    });
    console.log('\nModel downloaded.');

    // Load the model into memory
    await model.load();
    console.log('Model loaded and ready.');
    ```

    The `getModel` method accepts a model alias, which is a short friendly name that maps to a specific model in the catalog. The `download` method fetches the model weights to your local cache, and `load` makes the model ready for inference.

## Define a system prompt

A system prompt sets the assistant's personality and behavior. It's the first message in the conversation history and the model references it throughout the conversation.

Add a system prompt to shape how the assistant responds:

```javascript
// Start the conversation with a system prompt
const messages = [
    {
        role: 'system',
        content: 'You are a helpful, friendly assistant. Keep your responses ' +
                 'concise and conversational. If you don\'t know something, say so.'
    }
];
```

> [!TIP]
> Experiment with different system prompts to change the assistant's behavior. For example, you can instruct it to respond as a pirate, a teacher, or a domain expert.

## Implement multi-turn conversation

A chat assistant needs to maintain context across multiple exchanges. You achieve this by keeping a list of all messages (system, user, and assistant) and sending the full list with each request. The model uses this history to generate contextually relevant responses.

Add a conversation loop that:

- Reads user input from the console.
- Appends the user message to the history.
- Sends the complete history to the model.
- Appends the assistant's response to the history for the next turn.

```javascript
// Create a chat client
const chatClient = model.createChatClient();

// Set up readline for console input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const askQuestion = (prompt) => new Promise((resolve) => rl.question(prompt, resolve));

console.log('\nChat assistant ready! Type \'quit\' to exit.\n');

while (true) {
    const userInput = await askQuestion('You: ');
    if (userInput.trim().toLowerCase() === 'quit' ||
        userInput.trim().toLowerCase() === 'exit') {
        break;
    }

    // Add the user's message to conversation history
    messages.push({ role: 'user', content: userInput });

    // Send the full conversation history and get a response
    const response = await chatClient.completeChat(messages);
    const assistantMessage = response.choices[0]?.message?.content;

    // Add the assistant's response to conversation history
    messages.push({ role: 'assistant', content: assistantMessage });

    console.log(`Assistant: ${assistantMessage}\n`);
}
```

Each call to `completeChat` receives the full message history. This is how the model "remembers" previous turns — it doesn't store state between calls.

## Add streaming responses

Streaming prints each token as it's generated, which makes the assistant feel more responsive. Replace the `completeChat` call with `completeStreamingChat` to stream the response token by token.

Update the conversation loop to use streaming:

```javascript
while (true) {
    const userInput = await askQuestion('You: ');
    if (userInput.trim().toLowerCase() === 'quit' ||
        userInput.trim().toLowerCase() === 'exit') {
        break;
    }

    // Add the user's message to conversation history
    messages.push({ role: 'user', content: userInput });

    // Stream the response token by token
    process.stdout.write('Assistant: ');
    let fullResponse = '';
    await chatClient.completeStreamingChat(messages, (chunk) => {
        const content = chunk.choices?.[0]?.message?.content;
        if (content) {
            process.stdout.write(content);
            fullResponse += content;
        }
    });
    console.log('\n');

    // Add the complete response to conversation history
    messages.push({ role: 'assistant', content: fullResponse });
}
```

The streaming version accumulates the full response so it can be added to the conversation history after the stream completes.

## Complete code

Create a file named `index.js` and add the following complete code:

```javascript
import { FoundryLocalManager } from 'foundry-local-sdk';
import * as readline from 'readline';

// Initialize the Foundry Local SDK
const manager = FoundryLocalManager.create({
    appName: 'chat-assistant',
    logLevel: 'info'
});

// Select and load a model from the catalog
const model = await manager.catalog.getModel('phi-3.5-mini');

await model.download((progress) => {
    process.stdout.write(`\rDownloading model: ${progress.toFixed(2)}%`);
});
console.log('\nModel downloaded.');

await model.load();
console.log('Model loaded and ready.');

// Create a chat client
const chatClient = model.createChatClient();

// Start the conversation with a system prompt
const messages = [
    {
        role: 'system',
        content: 'You are a helpful, friendly assistant. Keep your responses ' +
                 'concise and conversational. If you don\'t know something, say so.'
    }
];

// Set up readline for console input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const askQuestion = (prompt) => new Promise((resolve) => rl.question(prompt, resolve));

console.log('\nChat assistant ready! Type \'quit\' to exit.\n');

while (true) {
    const userInput = await askQuestion('You: ');
    if (userInput.trim().toLowerCase() === 'quit' ||
        userInput.trim().toLowerCase() === 'exit') {
        break;
    }

    // Add the user's message to conversation history
    messages.push({ role: 'user', content: userInput });

    // Stream the response token by token
    process.stdout.write('Assistant: ');
    let fullResponse = '';
    await chatClient.completeStreamingChat(messages, (chunk) => {
        const content = chunk.choices?.[0]?.message?.content;
        if (content) {
            process.stdout.write(content);
            fullResponse += content;
        }
    });
    console.log('\n');

    // Add the complete response to conversation history
    messages.push({ role: 'assistant', content: fullResponse });
}

// Clean up - unload the model
await model.unload();
console.log('Model unloaded. Goodbye!');
rl.close();
```

## Run the application

Run the chat assistant:

```bash
node index.js
```

You see output similar to:

```
Downloading model: 100.00%
Model downloaded.
Model loaded and ready.

Chat assistant ready! Type 'quit' to exit.

You: What is the capital of France?
Assistant: The capital of France is Paris! It's known for landmarks like the Eiffel Tower,
the Louvre Museum, and Notre-Dame Cathedral.

You: What's it famous for besides those?
Assistant: Beyond those iconic landmarks, Paris is famous for its café culture, world-class
cuisine, fashion industry, and the Seine River. It's also home to the Musée d'Orsay
and the Palace of Versailles is just outside the city.

You: quit
Model unloaded. Goodbye!
```

Notice how the assistant remembers context from previous turns — when you ask "What's it famous for besides those?", it knows you're still talking about Paris.
