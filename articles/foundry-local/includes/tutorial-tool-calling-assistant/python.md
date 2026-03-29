---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

[!INCLUDE [Python project setup](../python-project-setup.md)]

## Define tools

Tool calling lets the model request that your code runs a function and returns the result. You define the available tools as a list of JSON schemas that describe each function's name, purpose, and parameters.

Create a file called `main.py` and add the following tool definitions:

```python
import json

# Define tools the model can call
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location",
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
                        "description": "The math expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]
```

Each tool definition includes a `name`, a `description` that helps the model decide when to use it, and a `parameters` schema that describes the expected input.

Next, add the Python functions that implement each tool:

```python
def get_weather(location, unit="celsius"):
    """Simulate a weather lookup."""
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "condition": "Sunny"
    }


def calculate(expression):
    """Evaluate a math expression safely."""
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return {"error": "Invalid expression"}
    try:
        result = eval(expression)  # Safe: only numeric chars allowed
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}


# Map tool names to functions
tool_functions = {
    "get_weather": get_weather,
    "calculate": calculate
}
```

The model doesn't run these functions directly. It returns a tool call request with the function name and arguments, and your code executes the function.

## Send a message that triggers tool use

Initialize the Foundry Local SDK, load a model, and send a message that the model can answer by calling a tool.

```python
import asyncio
from foundry_local_sdk import Configuration, FoundryLocalManager


async def main():
    # Initialize the Foundry Local SDK
    config = Configuration(app_name="tool-calling-app")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # Select and load a model
    model = manager.catalog.get_model("phi-3.5-mini")
    model.download(
        lambda progress: print(
            f"\rDownloading model: {progress:.2f}%", end="", flush=True
        )
    )
    print()
    model.load()
    print("Model loaded and ready.\n")

    # Get a chat client
    client = model.get_chat_client()

    # Start with a system prompt and a user message
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to tools. "
                       "Use them when needed to answer questions accurately."
        },
        {"role": "user", "content": "What's the weather like today?"}
    ]

    # Send the request with tools
    response = client.complete_chat(messages, tools=tools)
    print("Response received.")
```

When the model determines that a tool is needed, the response contains `tool_calls` instead of a regular text message. The next step shows how to detect and handle these calls.

## Execute the tool and return results

After the model responds with a tool call, you extract the function name and arguments, run the function, and send the result back.

```python
    choice = response.choices[0].message

    # Check if the model wants to call a tool
    if choice.tool_calls:
        # Add the assistant's response (with tool calls) to the history
        messages.append(choice)

        for tool_call in choice.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool call: {function_name}({arguments})")

            # Execute the function
            func = tool_functions[function_name]
            result = func(**arguments)

            # Add the tool result to the conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        # Send the updated conversation back to the model
        final_response = client.complete_chat(messages, tools=tools)
        print(f"Assistant: {final_response.choices[0].message.content}")
    else:
        # No tool call — the model responded directly
        print(f"Assistant: {choice.content}")
```

The key steps in the tool calling loop are:

1. **Detect tool calls** — check `response.choices[0].message.tool_calls`.
1. **Execute the function** — parse the arguments and call your local function.
1. **Return the result** — add a message with role `tool` and the matching `tool_call_id`.
1. **Get the final answer** — the model uses the tool result to generate a natural response.

## Handle the complete tool calling loop

Here's the complete application that combines tool definitions, SDK initialization, and the tool calling loop into a single runnable file.

Create a file named `main.py` and add the following complete code:

```python
import asyncio
import json
from foundry_local_sdk import Configuration, FoundryLocalManager


# --- Tool definitions ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location",
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
                        "description": (
                            "The math expression to evaluate"
                        )
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# --- Tool implementations ---
def get_weather(location, unit="celsius"):
    """Simulate a weather lookup."""
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "condition": "Sunny"
    }


def calculate(expression):
    """Evaluate a math expression safely."""
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return {"error": "Invalid expression"}
    try:
        result = eval(expression)
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}


tool_functions = {
    "get_weather": get_weather,
    "calculate": calculate
}


def process_tool_calls(messages, response, client):
    """Handle tool calls in a loop until the model produces a final answer."""
    choice = response.choices[0].message

    while choice.tool_calls:
        # Add the assistant message with tool call requests
        messages.append(choice)

        for tool_call in choice.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"  Tool call: {function_name}({arguments})")

            # Execute the function and add the result
            func = tool_functions[function_name]
            result = func(**arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        # Send the updated conversation back
        response = client.complete_chat(messages, tools=tools)
        choice = response.choices[0].message

    return choice.content


async def main():
    # Initialize the Foundry Local SDK
    config = Configuration(app_name="tool-calling-app")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # Select and load a model
    model = manager.catalog.get_model("phi-3.5-mini")
    model.download(
        lambda progress: print(
            f"\rDownloading model: {progress:.2f}%",
            end="",
            flush=True
        )
    )
    print()
    model.load()
    print("Model loaded and ready.")

    # Get a chat client
    client = model.get_chat_client()

    # Conversation with a system prompt
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to tools. "
                       "Use them when needed to answer questions accurately."
        }
    ]

    print("\nTool-calling assistant ready! Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            break

        messages.append({"role": "user", "content": user_input})

        response = client.complete_chat(messages, tools=tools)
        answer = process_tool_calls(messages, response, client)

        messages.append({"role": "assistant", "content": answer})
        print(f"Assistant: {answer}\n")

    # Clean up
    model.unload()
    print("Model unloaded. Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
```

## Run the application

Run the tool-calling assistant:

```bash
python main.py
```

You see output similar to:

```
Downloading model: 100.00%
Model loaded and ready.

Tool-calling assistant ready! Type 'quit' to exit.

You: What's the weather like today?
  Tool call: get_weather({'location': 'current location'})
Assistant: The weather today is sunny with a temperature of 22°C.

You: What is 245 * 38?
  Tool call: calculate({'expression': '245 * 38'})
Assistant: 245 multiplied by 38 equals 9,310.

You: quit
Model unloaded. Goodbye!
```

The model decides when to call a tool based on the user's message. For a weather question it calls `get_weather`, for math it calls `calculate`, and for general questions it responds directly without any tool calls.
