---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd js/tutorial-chat-assistant
```

[!INCLUDE [JavaScript project setup](../javascript-project-setup.md)]

## Browse the catalog and select a model

The Foundry Local SDK provides a model catalog that lists all available models. In this step, you initialize the SDK and select a model for your chat assistant.

1. Create a file called `index.js`.

1. Add the following code to initialize the SDK and select a model:

    :::code language="javascript" source="~/foundry-local-main/samples/js/tutorial-chat-assistant/app.js" id="init":::

    The `getModel` method accepts a model alias, which is a short friendly name that maps to a specific model in the catalog. The `download` method fetches the model weights to your local cache, and `load` makes the model ready for inference.

## Define a system prompt

A system prompt sets the assistant's personality and behavior. It's the first message in the conversation history and the model references it throughout the conversation.

Add a system prompt to shape how the assistant responds:

:::code language="javascript" source="~/foundry-local-main/samples/js/tutorial-chat-assistant/app.js" id="system_prompt":::

> [!TIP]
> Experiment with different system prompts to change the assistant's behavior. For example, you can instruct it to respond as a pirate, a teacher, or a domain expert.

## Implement multi-turn conversation

A chat assistant needs to maintain context across multiple exchanges. You achieve this by keeping a list of all messages (system, user, and assistant) and sending the full list with each request. The model uses this history to generate contextually relevant responses.

Add a conversation loop that:

- Reads user input from the console.
- Appends the user message to the history.
- Sends the complete history to the model.
- Appends the assistant's response to the history for the next turn.

:::code language="javascript" source="~/foundry-local-main/samples/js/tutorial-chat-assistant/app.js" id="conversation_loop":::

Each call to `completeChat` receives the full message history. This is how the model "remembers" previous turns — it doesn't store state between calls.

## Add streaming responses

Streaming prints each token as it's generated, which makes the assistant feel more responsive. Replace the `completeChat` call with `completeStreamingChat` to stream the response token by token.

Update the conversation loop to use streaming:

:::code language="javascript" source="~/foundry-local-main/samples/js/tutorial-chat-assistant/app.js" id="streaming":::

The streaming version accumulates the full response so it can be added to the conversation history after the stream completes.

## Complete code

Create a file named `index.js` and add the following complete code:

:::code language="javascript" source="~/foundry-local-main/samples/js/tutorial-chat-assistant/app.js" id="complete_code":::

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

You: What is photosynthesis?
Assistant: Photosynthesis is the process plants use to convert sunlight, water, and carbon
dioxide into glucose and oxygen. It mainly happens in the leaves, inside structures
called chloroplasts.

You: Why is it important for other living things?
Assistant: It's essential because photosynthesis produces the oxygen that most living things
breathe. It also forms the base of the food chain — animals eat plants or eat other
animals that depend on plants for energy.

You: quit
Model unloaded. Goodbye!
```

Notice how the assistant remembers context from previous turns — when you ask "Why is it important for other living things?", it knows you're still talking about photosynthesis.
