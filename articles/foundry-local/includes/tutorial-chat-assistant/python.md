---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

[!INCLUDE [Python project setup](../python-project-setup.md)]

## Browse the catalog and select a model

The Foundry Local SDK provides a model catalog that lists all available models. In this step, you initialize the SDK and select a model for your chat assistant.

1. Create a file called `main.py`.

1. Add the following code to initialize the SDK and select a model:

    ```python
    from foundry_local_sdk import Configuration, FoundryLocalManager

    # Initialize the Foundry Local SDK
    config = Configuration(app_name="chat-assistant")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # Select a model from the catalog
    model = manager.catalog.get_model("phi-3.5-mini")

    # Download the model (skips if already cached)
    model.download(lambda progress: print(f"\rDownloading model: {progress:.2f}%", end="", flush=True))
    print()

    # Load the model into memory
    model.load()
    print("Model loaded and ready.")
    ```

    The `get_model` method accepts a model alias, which is a short friendly name that maps to a specific model in the catalog. The `download` method fetches the model weights to your local cache, and `load` makes the model ready for inference.

## Define a system prompt

A system prompt sets the assistant's personality and behavior. It's the first message in the conversation history and the model references it throughout the conversation.

Add a system prompt to shape how the assistant responds:

```python
# Start the conversation with a system prompt
messages = [
    {
        "role": "system",
        "content": "You are a helpful, friendly assistant. Keep your responses "
                   "concise and conversational. If you don't know something, say so."
    }
]
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

```python
# Get a chat client
client = model.get_chat_client()

print("\nChat assistant ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ("quit", "exit"):
        break

    # Add the user's message to conversation history
    messages.append({"role": "user", "content": user_input})

    # Send the full conversation history and get a response
    response = client.complete_chat(messages)
    assistant_message = response.choices[0].message.content

    # Add the assistant's response to conversation history
    messages.append({"role": "assistant", "content": assistant_message})

    print(f"Assistant: {assistant_message}\n")
```

Each call to `complete_chat` receives the full message history. This is how the model "remembers" previous turns — it doesn't store state between calls.

## Add streaming responses

Streaming prints each token as it's generated, which makes the assistant feel more responsive. Replace the `complete_chat` call with `complete_streaming_chat` to stream the response token by token.

Update the conversation loop to use streaming:

```python
while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ("quit", "exit"):
        break

    # Add the user's message to conversation history
    messages.append({"role": "user", "content": user_input})

    # Stream the response token by token
    print("Assistant: ", end="", flush=True)
    full_response = ""
    for chunk in client.complete_streaming_chat(messages):
        content = chunk.choices[0].message.content
        if content:
            print(content, end="", flush=True)
            full_response += content
    print("\n")

    # Add the complete response to conversation history
    messages.append({"role": "assistant", "content": full_response})
```

The streaming version accumulates the full response so it can be added to the conversation history after the stream completes.

## Complete code

Create a file named `main.py` and add the following complete code:

```python
import asyncio
from foundry_local_sdk import Configuration, FoundryLocalManager


async def main():
    # Initialize the Foundry Local SDK
    config = Configuration(app_name="chat-assistant")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # Select and load a model from the catalog
    model = manager.catalog.get_model("phi-3.5-mini")
    model.download(lambda progress: print(f"\rDownloading model: {progress:.2f}%", end="", flush=True))
    print()
    model.load()
    print("Model loaded and ready.")

    # Get a chat client
    client = model.get_chat_client()

    # Start the conversation with a system prompt
    messages = [
        {
            "role": "system",
            "content": "You are a helpful, friendly assistant. Keep your responses "
                       "concise and conversational. If you don't know something, say so."
        }
    ]

    print("\nChat assistant ready! Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            break

        # Add the user's message to conversation history
        messages.append({"role": "user", "content": user_input})

        # Stream the response token by token
        print("Assistant: ", end="", flush=True)
        full_response = ""
        for chunk in client.complete_streaming_chat(messages):
            content = chunk.choices[0].message.content
            if content:
                print(content, end="", flush=True)
                full_response += content
        print("\n")

        # Add the complete response to conversation history
        messages.append({"role": "assistant", "content": full_response})

    # Clean up - unload the model
    model.unload()
    print("Model unloaded. Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
```

## Run the application

Run the chat assistant:

```bash
python main.py
```

You see output similar to:

```
Downloading model: 100.00%
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
