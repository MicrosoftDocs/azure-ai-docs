---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 07/17/2025
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [Rust and Cargo](https://www.rust-lang.org/tools/install) installed (Rust 1.70.0 or later).

## Samples repository

You can find the sample in this article in the [Foundry Local SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Set up project

[!INCLUDE [project-setup](../rust-project-setup.md)]

Add additional dependencies for HTTP and JSON:

```bash
cargo add anyhow reqwest --features reqwest/json
cargo add serde serde_json --features serde/derive
```

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

Replace the contents of `src/main.rs` with the following code:

```rust
use foundry_local_sdk::{FoundryLocalConfig, FoundryLocalManager};
use std::io::Write;

fn multiply_numbers(first: i64, second: i64) -> i64 {
    first * second
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize the Foundry Local SDK with web service
    let config = FoundryLocalConfig::new("app-name").with_web_urls("http://localhost:5000");
    let manager = FoundryLocalManager::create(config)?;

    // Get and load the model
    let model = manager.catalog().get_model("qwen2.5-0.5b").await?;
    model
        .download(Some(|progress: f32| {
            print!("\rDownloading model: {:.2}%", progress);
            std::io::stdout().flush().unwrap();
        }))
        .await?;
    println!();
    model.load().await?;

    // Start the web service
    manager.start_web_service().await?;
    let endpoint = manager.urls()[0].clone();

    // Use reqwest to call the OpenAI-compatible API
    let client = reqwest::Client::new();

    // First call - force the model to make a tool call
    let body = serde_json::json!({
        "model": model.id(),
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant. If necessary, you can use any provided tools to answer the question."},
            {"role": "user", "content": "What is the answer to 7 multiplied by 6?"}
        ],
        "tools": [{
            "type": "function",
            "function": {
                "name": "multiply_numbers",
                "description": "A tool for multiplying two numbers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first": {"type": "integer", "description": "The first number in the operation"},
                        "second": {"type": "integer", "description": "The second number in the operation"}
                    },
                    "required": ["first", "second"]
                }
            }
        }],
        "tool_choice": "required"
    });

    let response = client
        .post(format!("{}/v1/chat/completions", endpoint))
        .json(&body)
        .send()
        .await?
        .json::<serde_json::Value>()
        .await?;

    // Process tool calls
    let mut messages = vec![
        serde_json::json!({"role": "system", "content": "You are a helpful AI assistant. If necessary, you can use any provided tools to answer the question."}),
        serde_json::json!({"role": "user", "content": "What is the answer to 7 multiplied by 6?"}),
    ];

    if let Some(tool_calls) = response["choices"][0]["message"]["tool_calls"].as_array() {
        for tool_call in tool_calls {
            let name = tool_call["function"]["name"].as_str().unwrap_or_default();
            if name == "multiply_numbers" {
                let args: serde_json::Value =
                    serde_json::from_str(tool_call["function"]["arguments"].as_str().unwrap())?;
                let first = args["first"].as_i64().unwrap();
                let second = args["second"].as_i64().unwrap();

                println!("Invoking tool: {} with arguments {} and {}", name, first, second);
                let result = multiply_numbers(first, second);
                println!("Tool response: {}", result);

                messages.push(serde_json::json!({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result.to_string()
                }));
            }
        }
    }

    println!("Tool calls completed. Prompting model to continue conversation...\n");

    // Continue the conversation
    messages.push(serde_json::json!({"role": "system", "content": "Respond only with the answer generated by the tool."}));

    let body = serde_json::json!({
        "model": model.id(),
        "messages": messages,
        "tool_choice": "auto"
    });

    let response = client
        .post(format!("{}/v1/chat/completions", endpoint))
        .json(&body)
        .send()
        .await?
        .json::<serde_json::Value>()
        .await?;

    println!(
        "Chat completion response:\n{}",
        response["choices"][0]["message"]["content"]
    );

    // Tidy up
    manager.stop_web_service().await?;
    model.unload().await?;

    Ok(())
}
```

## Run the application

To run the application, execute the following command in your terminal:

```bash
cargo run
```
