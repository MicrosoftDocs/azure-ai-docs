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
cd cs/tutorial-tool-calling
```

## Install packages

[!INCLUDE [C# project setup](../csharp-project-setup.md)]

## Define tools

Tool calling lets the model request that your code runs a function and returns the result. You define the available tools as a list of JSON schemas that describe each function's name, purpose, and parameters.

1. Open `Program.cs` and add the following tool definitions:

    :::code language="csharp" source="~/foundry-local-main/samples/cs/tutorial-tool-calling/Program.cs" id="tool_definitions":::

    Each tool definition includes a `name`, a `description` that helps the model decide when to use it, and a `parameters` schema that describes the expected input.

1. Add the C# methods that implement each tool:

    :::code language="csharp" source="~/foundry-local-main/samples/cs/tutorial-tool-calling/Program.cs" id="tool_definitions":::

    The model doesn't run these functions directly. It returns a tool call request with the function name and arguments, and your code executes the function.

## Send a message that triggers tool use

Initialize the Foundry Local SDK, load a model, and send a message that the model can answer by calling a tool.

:::code language="csharp" source="~/foundry-local-main/samples/cs/tutorial-tool-calling/Program.cs" id="init":::

When the model determines that a tool is needed, the response contains `ToolCalls` instead of a regular text message. The next step shows how to detect and handle these calls.

## Execute the tool and return results

After the model responds with a tool call, you extract the function name and arguments, run the function, and send the result back.

:::code language="csharp" source="~/foundry-local-main/samples/cs/tutorial-tool-calling/Program.cs" id="tool_loop":::

The key steps in the tool calling loop are:

1. **Detect tool calls** — check `response.Choices[0].Message.ToolCalls`.
1. **Execute the function** — parse the arguments and call your local function.
1. **Return the result** — add a message with role `tool` and the matching `ToolCallId`.
1. **Get the final answer** — the model uses the tool result to generate a natural response.

## Handle the complete tool calling loop

Here's the complete application that combines tool definitions, SDK initialization, and the tool calling loop into a single runnable file.

Replace the contents of `Program.cs` with the following complete code:

:::code language="csharp" source="~/foundry-local-main/samples/cs/tutorial-tool-calling/Program.cs" id="complete_code":::

Run the tool-calling assistant:

```bash
dotnet run
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
