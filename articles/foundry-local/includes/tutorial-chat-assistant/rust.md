---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

[!INCLUDE [Rust project setup](../rust-project-setup.md)]

## Browse the catalog and select a model

The Foundry Local SDK provides a model catalog that lists all available models. In this step, you initialize the SDK and select a model for your chat assistant.

1. Open `src/main.rs` and replace its contents with the following code to initialize the SDK and select a model:

    ```rust
    use foundry_local_sdk::{FoundryLocalConfig, FoundryLocalManager};
    use std::io::Write;

    #[tokio::main]
    async fn main() -> anyhow::Result<()> {
        // Initialize the Foundry Local SDK
        let manager = FoundryLocalManager::create(FoundryLocalConfig::new("chat-assistant"))?;

        // Select a model from the catalog
        let model = manager.catalog().get_model("phi-3.5-mini").await?;

        // Download the model (skips if already cached)
        model
            .download(Some(|progress: f32| {
                print!("\rDownloading model: {:.2}%", progress);
                std::io::stdout().flush().unwrap();
            }))
            .await?;
        println!();

        // Load the model into memory
        model.load().await?;
        println!("Model loaded and ready.");

        Ok(())
    }
    ```

    The `get_model` method accepts a model alias, which is a short friendly name that maps to a specific model in the catalog. The `download` method fetches the model weights to your local cache, and `load` makes the model ready for inference.

## Define a system prompt

A system prompt sets the assistant's personality and behavior. It's the first message in the conversation history and the model references it throughout the conversation.

Add a system prompt to shape how the assistant responds:

```rust
use foundry_local_sdk::{
    ChatCompletionRequestMessage, ChatCompletionRequestSystemMessage,
};

// Start the conversation with a system prompt
let mut messages: Vec<ChatCompletionRequestMessage> = vec![
    ChatCompletionRequestSystemMessage::new(
        "You are a helpful, friendly assistant. Keep your responses \
         concise and conversational. If you don't know something, say so."
    ).into(),
];
```

> [!TIP]
> Experiment with different system prompts to change the assistant's behavior. For example, you can instruct it to respond as a pirate, a teacher, or a domain expert.

## Implement multi-turn conversation

A chat assistant needs to maintain context across multiple exchanges. You achieve this by keeping a vector of all messages (system, user, and assistant) and sending the full list with each request. The model uses this history to generate contextually relevant responses.

Add a conversation loop that:

- Reads user input from the console.
- Appends the user message to the history.
- Sends the complete history to the model.
- Appends the assistant's response to the history for the next turn.

```rust
use foundry_local_sdk::{
    ChatCompletionRequestAssistantMessage, ChatCompletionRequestUserMessage,
};
use std::io::BufRead;

// Create a chat client
let client = model.create_chat_client().temperature(0.7).max_tokens(512);

println!("\nChat assistant ready! Type 'quit' to exit.\n");

let stdin = std::io::stdin();
loop {
    print!("You: ");
    std::io::stdout().flush()?;

    let mut input = String::new();
    stdin.lock().read_line(&mut input)?;
    let input = input.trim();

    if input.eq_ignore_ascii_case("quit") || input.eq_ignore_ascii_case("exit") {
        break;
    }

    // Add the user's message to conversation history
    messages.push(ChatCompletionRequestUserMessage::new(input).into());

    // Send the full conversation history and get a response
    let response = client.complete_chat(&messages, None).await?;
    let assistant_message = response.choices[0]
        .message
        .content
        .as_deref()
        .unwrap_or("");

    // Add the assistant's response to conversation history
    messages.push(
        ChatCompletionRequestAssistantMessage::new(assistant_message.to_string()).into(),
    );

    println!("Assistant: {}\n", assistant_message);
}
```

Each call to `complete_chat` receives the full message history. This is how the model "remembers" previous turns — it doesn't store state between calls.

## Add streaming responses

Streaming prints each token as it's generated, which makes the assistant feel more responsive. Replace the `complete_chat` call with `complete_streaming_chat` to stream the response token by token.

Update the conversation loop to use streaming:

```rust
use tokio_stream::StreamExt;

loop {
    print!("You: ");
    std::io::stdout().flush()?;

    let mut input = String::new();
    stdin.lock().read_line(&mut input)?;
    let input = input.trim();

    if input.eq_ignore_ascii_case("quit") || input.eq_ignore_ascii_case("exit") {
        break;
    }

    // Add the user's message to conversation history
    messages.push(ChatCompletionRequestUserMessage::new(input).into());

    // Stream the response token by token
    print!("Assistant: ");
    std::io::stdout().flush()?;
    let mut full_response = String::new();
    let mut stream = client.complete_streaming_chat(&messages, None).await?;
    while let Some(chunk) = stream.next().await {
        let chunk = chunk?;
        if let Some(content) = &chunk.choices[0].message.content {
            print!("{}", content);
            std::io::stdout().flush()?;
            full_response.push_str(content);
        }
    }
    println!("\n");

    // Add the complete response to conversation history
    messages.push(
        ChatCompletionRequestAssistantMessage::new(full_response).into(),
    );
}
```

The streaming version accumulates the full response so it can be added to the conversation history after the stream completes.

## Complete code

Replace the contents of `src/main.rs` with the following complete code:

```rust
use foundry_local_sdk::{
    ChatCompletionRequestAssistantMessage, ChatCompletionRequestMessage,
    ChatCompletionRequestSystemMessage, ChatCompletionRequestUserMessage,
    FoundryLocalConfig, FoundryLocalManager,
};
use std::io::{BufRead, Write};
use tokio_stream::StreamExt;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize the Foundry Local SDK
    let manager = FoundryLocalManager::create(FoundryLocalConfig::new("chat-assistant"))?;

    // Select and load a model from the catalog
    let model = manager.catalog().get_model("phi-3.5-mini").await?;

    model
        .download(Some(|progress: f32| {
            print!("\rDownloading model: {:.2}%", progress);
            std::io::stdout().flush().unwrap();
        }))
        .await?;
    println!();

    model.load().await?;
    println!("Model loaded and ready.");

    // Create a chat client
    let client = model.create_chat_client().temperature(0.7).max_tokens(512);

    // Start the conversation with a system prompt
    let mut messages: Vec<ChatCompletionRequestMessage> = vec![
        ChatCompletionRequestSystemMessage::new(
            "You are a helpful, friendly assistant. Keep your responses \
             concise and conversational. If you don't know something, say so.",
        )
        .into(),
    ];

    println!("\nChat assistant ready! Type 'quit' to exit.\n");

    let stdin = std::io::stdin();
    loop {
        print!("You: ");
        std::io::stdout().flush()?;

        let mut input = String::new();
        stdin.lock().read_line(&mut input)?;
        let input = input.trim();

        if input.eq_ignore_ascii_case("quit") || input.eq_ignore_ascii_case("exit") {
            break;
        }

        // Add the user's message to conversation history
        messages.push(ChatCompletionRequestUserMessage::new(input).into());

        // Stream the response token by token
        print!("Assistant: ");
        std::io::stdout().flush()?;
        let mut full_response = String::new();
        let mut stream = client.complete_streaming_chat(&messages, None).await?;
        while let Some(chunk) = stream.next().await {
            let chunk = chunk?;
            if let Some(content) = &chunk.choices[0].message.content {
                print!("{}", content);
                std::io::stdout().flush()?;
                full_response.push_str(content);
            }
        }
        println!("\n");

        // Add the complete response to conversation history
        messages.push(ChatCompletionRequestAssistantMessage::new(full_response).into());
    }

    // Clean up - unload the model
    model.unload().await?;
    println!("Model unloaded. Goodbye!");

    Ok(())
}
```

## Run the application

Run the chat assistant:

```bash
cargo run
```

You see output similar to:

```
Downloading model: 100.00%
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
