---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

[!INCLUDE [Rust project setup](../rust-project-setup.md)]

## Define tools

Tool calling lets the model request that your code runs a function and returns the result. You define the available tools as a list of JSON schemas that describe each function's name, purpose, and parameters.

1. Add the `serde_json` dependency for JSON handling:

    ```bash
    cargo add serde_json
    ```

1. Open `src/main.rs` and add the following tool definitions:

    ```rust
    use serde_json::json;

    // Define tools the model can call
    let tools = json!([
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description":
                    "Get the current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city or location"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "Temperature unit"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Perform a math calculation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description":
                                "The math expression to evaluate"
                        }
                    },
                    "required": ["expression"]
                }
            }
        }
    ]);
    ```

    Each tool definition includes a `name`, a `description` that helps the model decide when to use it, and a `parameters` schema that describes the expected input.

1. Add the Rust functions that implement each tool:

    ```rust
    fn execute_tool(
        name: &str,
        arguments: &serde_json::Value,
    ) -> serde_json::Value {
        match name {
            "get_weather" => {
                let location = arguments["location"]
                    .as_str()
                    .unwrap_or("unknown");
                let unit = arguments["unit"]
                    .as_str()
                    .unwrap_or("celsius");
                let temp = if unit == "celsius" { 22 } else { 72 };
                json!({
                    "location": location,
                    "temperature": temp,
                    "unit": unit,
                    "condition": "Sunny"
                })
            }
            "calculate" => {
                let expression = arguments["expression"]
                    .as_str()
                    .unwrap_or("");
                // Simple evaluation for basic arithmetic
                let is_valid = expression
                    .chars()
                    .all(|c| "0123456789+-*/(). ".contains(c));
                if !is_valid {
                    return json!({"error": "Invalid expression"});
                }
                // Use a basic parser for safe evaluation
                match eval_expression(expression) {
                    Ok(result) => json!({
                        "expression": expression,
                        "result": result
                    }),
                    Err(e) => json!({"error": e}),
                }
            }
            _ => json!({"error": format!("Unknown function: {}", name)}),
        }
    }

    fn eval_expression(expr: &str) -> Result<f64, String> {
        // Simple recursive-descent parser for basic arithmetic
        let expr = expr.replace(' ', "");
        let chars: Vec<char> = expr.chars().collect();
        let mut pos = 0;
        let result = parse_add(&chars, &mut pos)?;
        if pos < chars.len() {
            return Err("Unexpected character".to_string());
        }
        Ok(result)
    }

    fn parse_add(
        chars: &[char],
        pos: &mut usize,
    ) -> Result<f64, String> {
        let mut result = parse_mul(chars, pos)?;
        while *pos < chars.len()
            && (chars[*pos] == '+' || chars[*pos] == '-')
        {
            let op = chars[*pos];
            *pos += 1;
            let right = parse_mul(chars, pos)?;
            result = if op == '+' {
                result + right
            } else {
                result - right
            };
        }
        Ok(result)
    }

    fn parse_mul(
        chars: &[char],
        pos: &mut usize,
    ) -> Result<f64, String> {
        let mut result = parse_atom(chars, pos)?;
        while *pos < chars.len()
            && (chars[*pos] == '*' || chars[*pos] == '/')
        {
            let op = chars[*pos];
            *pos += 1;
            let right = parse_atom(chars, pos)?;
            result = if op == '*' {
                result * right
            } else {
                result / right
            };
        }
        Ok(result)
    }

    fn parse_atom(
        chars: &[char],
        pos: &mut usize,
    ) -> Result<f64, String> {
        if *pos < chars.len() && chars[*pos] == '(' {
            *pos += 1;
            let result = parse_add(chars, pos)?;
            if *pos < chars.len() && chars[*pos] == ')' {
                *pos += 1;
            }
            return Ok(result);
        }
        let start = *pos;
        while *pos < chars.len()
            && (chars[*pos].is_ascii_digit() || chars[*pos] == '.')
        {
            *pos += 1;
        }
        if start == *pos {
            return Err("Expected number".to_string());
        }
        let num_str: String = chars[start..*pos].iter().collect();
        num_str
            .parse::<f64>()
            .map_err(|e| e.to_string())
    }
    ```

    The model doesn't run these functions directly. It returns a tool call request with the function name and arguments, and your code executes the function.

## Send a message that triggers tool use

Initialize the Foundry Local SDK, load a model, and send a message that the model can answer by calling a tool.

```rust
use foundry_local_sdk::{
    ChatCompletionRequestMessage, ChatCompletionRequestSystemMessage,
    ChatCompletionRequestUserMessage, FoundryLocalConfig,
    FoundryLocalManager,
};
use std::io::Write;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize the Foundry Local SDK
    let manager = FoundryLocalManager::create(
        FoundryLocalConfig::new("tool-calling-app"),
    )?;

    // Select and load a model
    let model = manager.catalog().get_model("phi-3.5-mini").await?;

    model
        .download(Some(|progress: f32| {
            print!("\rDownloading model: {:.2}%", progress);
            std::io::stdout().flush().unwrap();
        }))
        .await?;
    println!();

    model.load().await?;
    println!("Model loaded and ready.\n");

    // Create a chat client
    let client = model
        .create_chat_client()
        .temperature(0.7)
        .max_tokens(512);

    // Start with a system prompt and a user message
    let mut messages: Vec<ChatCompletionRequestMessage> = vec![
        ChatCompletionRequestSystemMessage::new(
            "You are a helpful assistant with access to tools. \
             Use them when needed to answer questions accurately.",
        )
        .into(),
        ChatCompletionRequestUserMessage::new(
            "What's the weather like today?",
        )
        .into(),
    ];

    // Send the request with tools
    let response = client
        .complete_chat(&messages, Some(&tools))
        .await?;
    println!("Response received.");

    Ok(())
}
```

When the model determines that a tool is needed, the response contains `tool_calls` instead of a regular text message. The next step shows how to detect and handle these calls.

## Execute the tool and return results

After the model responds with a tool call, you extract the function name and arguments, run the function, and send the result back.

```rust
use foundry_local_sdk::ChatCompletionRequestToolMessage;

let choice = &response.choices[0].message;

// Check if the model wants to call a tool
if let Some(tool_calls) = &choice.tool_calls {
    // Add the assistant's response (with tool calls) to the history
    messages.push(choice.clone().into());

    for tool_call in tool_calls {
        let function_name = &tool_call.function.name;
        let arguments: serde_json::Value =
            serde_json::from_str(&tool_call.function.arguments)?;
        println!(
            "Tool call: {}({})",
            function_name, arguments
        );

        // Execute the function
        let result = execute_tool(function_name, &arguments);

        // Add the tool result to the conversation
        messages.push(
            ChatCompletionRequestToolMessage::new(
                result.to_string(),
                &tool_call.id,
            )
            .into(),
        );
    }

    // Send the updated conversation back to the model
    let final_response = client
        .complete_chat(&messages, Some(&tools))
        .await?;
    println!(
        "Assistant: {}",
        final_response.choices[0]
            .message
            .content
            .as_deref()
            .unwrap_or("")
    );
} else {
    // No tool call — the model responded directly
    println!(
        "Assistant: {}",
        choice.content.as_deref().unwrap_or("")
    );
}
```

The key steps in the tool calling loop are:

1. **Detect tool calls** — check `response.choices[0].message.tool_calls`.
1. **Execute the function** — parse the arguments and call your local function.
1. **Return the result** — add a message with role `tool` and the matching tool call ID.
1. **Get the final answer** — the model uses the tool result to generate a natural response.

## Handle the complete tool calling loop

Here's the complete application that combines tool definitions, SDK initialization, and the tool calling loop into a single runnable file.

Replace the contents of `src/main.rs` with the following complete code:

```rust
use foundry_local_sdk::{
    ChatCompletionRequestAssistantMessage,
    ChatCompletionRequestMessage,
    ChatCompletionRequestSystemMessage,
    ChatCompletionRequestToolMessage,
    ChatCompletionRequestUserMessage, FoundryLocalConfig,
    FoundryLocalManager,
};
use serde_json::json;
use std::io::{BufRead, Write};

// --- Tool implementations ---
fn execute_tool(
    name: &str,
    arguments: &serde_json::Value,
) -> serde_json::Value {
    match name {
        "get_weather" => {
            let location = arguments["location"]
                .as_str()
                .unwrap_or("unknown");
            let unit = arguments["unit"]
                .as_str()
                .unwrap_or("celsius");
            let temp = if unit == "celsius" { 22 } else { 72 };
            json!({
                "location": location,
                "temperature": temp,
                "unit": unit,
                "condition": "Sunny"
            })
        }
        "calculate" => {
            let expression = arguments["expression"]
                .as_str()
                .unwrap_or("");
            let is_valid = expression
                .chars()
                .all(|c| "0123456789+-*/(). ".contains(c));
            if !is_valid {
                return json!({"error": "Invalid expression"});
            }
            match eval_expression(expression) {
                Ok(result) => json!({
                    "expression": expression,
                    "result": result
                }),
                Err(e) => json!({"error": e}),
            }
        }
        _ => json!({"error": format!("Unknown function: {}", name)}),
    }
}

fn eval_expression(expr: &str) -> Result<f64, String> {
    let expr = expr.replace(' ', "");
    let chars: Vec<char> = expr.chars().collect();
    let mut pos = 0;
    let result = parse_add(&chars, &mut pos)?;
    if pos < chars.len() {
        return Err("Unexpected character".to_string());
    }
    Ok(result)
}

fn parse_add(
    chars: &[char],
    pos: &mut usize,
) -> Result<f64, String> {
    let mut result = parse_mul(chars, pos)?;
    while *pos < chars.len()
        && (chars[*pos] == '+' || chars[*pos] == '-')
    {
        let op = chars[*pos];
        *pos += 1;
        let right = parse_mul(chars, pos)?;
        result = if op == '+' {
            result + right
        } else {
            result - right
        };
    }
    Ok(result)
}

fn parse_mul(
    chars: &[char],
    pos: &mut usize,
) -> Result<f64, String> {
    let mut result = parse_atom(chars, pos)?;
    while *pos < chars.len()
        && (chars[*pos] == '*' || chars[*pos] == '/')
    {
        let op = chars[*pos];
        *pos += 1;
        let right = parse_atom(chars, pos)?;
        result = if op == '*' {
            result * right
        } else {
            result / right
        };
    }
    Ok(result)
}

fn parse_atom(
    chars: &[char],
    pos: &mut usize,
) -> Result<f64, String> {
    if *pos < chars.len() && chars[*pos] == '(' {
        *pos += 1;
        let result = parse_add(chars, pos)?;
        if *pos < chars.len() && chars[*pos] == ')' {
            *pos += 1;
        }
        return Ok(result);
    }
    let start = *pos;
    while *pos < chars.len()
        && (chars[*pos].is_ascii_digit() || chars[*pos] == '.')
    {
        *pos += 1;
    }
    if start == *pos {
        return Err("Expected number".to_string());
    }
    let num_str: String = chars[start..*pos].iter().collect();
    num_str.parse::<f64>().map_err(|e| e.to_string())
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // --- Tool definitions ---
    let tools = json!([
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description":
                    "Get the current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description":
                                "The city or location"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "Temperature unit"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Perform a math calculation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description":
                                "The math expression to evaluate"
                        }
                    },
                    "required": ["expression"]
                }
            }
        }
    ]);

    // Initialize the Foundry Local SDK
    let manager = FoundryLocalManager::create(
        FoundryLocalConfig::new("tool-calling-app"),
    )?;

    // Select and load a model
    let model = manager
        .catalog()
        .get_model("phi-3.5-mini")
        .await?;

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
    let client = model
        .create_chat_client()
        .temperature(0.7)
        .max_tokens(512);

    // Conversation with a system prompt
    let mut messages: Vec<ChatCompletionRequestMessage> = vec![
        ChatCompletionRequestSystemMessage::new(
            "You are a helpful assistant with access to tools. \
             Use them when needed to answer questions accurately.",
        )
        .into(),
    ];

    println!(
        "\nTool-calling assistant ready! Type 'quit' to exit.\n"
    );

    let stdin = std::io::stdin();
    loop {
        print!("You: ");
        std::io::stdout().flush()?;

        let mut input = String::new();
        stdin.lock().read_line(&mut input)?;
        let input = input.trim();

        if input.eq_ignore_ascii_case("quit")
            || input.eq_ignore_ascii_case("exit")
        {
            break;
        }

        messages.push(
            ChatCompletionRequestUserMessage::new(input).into(),
        );

        let mut response = client
            .complete_chat(&messages, Some(&tools))
            .await?;

        // Process tool calls in a loop
        while response.choices[0].message.tool_calls.is_some() {
            let tool_calls = response.choices[0]
                .message
                .tool_calls
                .as_ref()
                .unwrap();

            messages.push(
                response.choices[0].message.clone().into(),
            );

            for tool_call in tool_calls {
                let function_name = &tool_call.function.name;
                let arguments: serde_json::Value =
                    serde_json::from_str(
                        &tool_call.function.arguments,
                    )?;
                println!(
                    "  Tool call: {}({})",
                    function_name, arguments
                );

                let result =
                    execute_tool(function_name, &arguments);
                messages.push(
                    ChatCompletionRequestToolMessage::new(
                        result.to_string(),
                        &tool_call.id,
                    )
                    .into(),
                );
            }

            response = client
                .complete_chat(&messages, Some(&tools))
                .await?;
        }

        let answer = response.choices[0]
            .message
            .content
            .as_deref()
            .unwrap_or("");
        messages.push(
            ChatCompletionRequestAssistantMessage::new(
                answer.to_string(),
            )
            .into(),
        );
        println!("Assistant: {}\n", answer);
    }

    // Clean up
    model.unload().await?;
    println!("Model unloaded. Goodbye!");

    Ok(())
}
```

## Run the application

Run the tool-calling assistant:

```bash
cargo run
```

You see output similar to:

```
Downloading model: 100.00%
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
