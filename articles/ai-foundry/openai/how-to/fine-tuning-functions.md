---
title: Fine-tuning function calls with Azure OpenAI in Microsoft Foundry Models
description: Learn how to improve tool calling performance with Azure OpenAI fine-tuning
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/11/2026
author: ssalgadodev
ms.author: ssalgado
monikerRange: 'foundry-classic || foundry'
---


# Fine-tuning and tool calling

Models that use the chat completions API support [tool calling](../how-to/function-calling.md). Functions defined in your chat completion calls don't always perform as expected. Fine-tuning your model with tool calling examples can improve model output:

| Benefit | Description |
|---------|-------------|
| Reduce prompt tokens | Get similarly formatted responses even when the full function definition isn't present. |
| Improve accuracy | Get more accurate and consistent outputs. |

> [!NOTE]
> `function_call` and `functions` have been deprecated in favor of `tools`.
> Use the `tools` parameter instead.


## Tool calling (recommended)
### Constructing a training file

When constructing a training file of tool calling examples, take a function definition like this:

```json
{
    "messages": [
        { "role": "user", "content": "What is the weather in San Francisco?" },
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_id",
                    "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "arguments": "{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"
                    }
                }
            ]
        }
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and country/region, eg. San Francisco, USA"
                        },
                        "format": { "type": "string", "enum": ["celsius", "fahrenheit"] }
                    },
                    "required": ["location", "format"]
                }
            }
        }
    ]
}
```

And express the information as a single line within your `.jsonl` training file as below:

```jsonl
{"messages":[{"role":"user","content":"What is the weather in San Francisco?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"}}]}],"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country/region, eg. San Francisco, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
```

As with all fine-tuning training, your example file requires at least 10 examples.

### Optimize for cost

To use fewer prompt tokens after fine-tuning on full function definitions, experiment with the following strategies:

| Strategy | Description |
|----------|-------------|
| Omit descriptions | Remove the `description` field from function and parameters. |
| Omit parameters | Remove the entire `properties` field from the `parameters` object. |
| Omit function entirely | Remove the entire function object from the functions array. |

### Optimize for quality

To improve the quality of tool calling output, keep the function definitions in your fine-tuning training dataset and subsequent chat completion calls identical.

### Customize model responses to function outputs

You can also fine-tune on tool calling examples to improve the model's response to function outputs. Include examples consisting of function response messages and assistant response messages where the function response is interpreted and put into context by the assistant.

```json
{
    "messages": [
        {"role": "user", "content": "What is the weather in San Francisco?"},
        {"role": "assistant", "tool_calls": [{"id": "call_id", "type": "function", "function": {"name": "get_current_weather", "arguments": "{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"}}]}
        {"role": "tool", "tool_call_id": "call_id", "content": "21.0"},
        {"role": "assistant", "content": "It is 21 degrees celsius in San Francisco, CA"}
    ],
    "tools": [] // same as before
}
```

As with the example before, this example is artificially expanded for readability. The actual entry in the `.jsonl` training file would be a single line:

```jsonl
{"messages":[{"role":"user","content":"What is the weather in San Francisco?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"}}]},{"role":"tool","tool_call_id":"call_id","content":"21.0"},{"role":"assistant","content":"It is 21 degrees celsius in San Francisco, CA"}],"tools":[]}
```

### Constructing a training file

When constructing a training file of function calling examples, take a function definition like this:

```json
{
    "messages": [
        {"role": "user", "content": "What is the weather in San Francisco?"},
        {"role": "assistant", "function_call": {"name": "get_current_weather", "arguments": "{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"}
    ],
    "functions": [{
        "name": "get_current_weather",
        "description": "Get the current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city and country, eg. San Francisco, USA"},
                "format": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["location", "format"]
        }
    }]
}
```

And express the information as a single line within your `.jsonl` training file as below:

```jsonl
{"messages": [{"role": "user", "content": "What is the weather in San Francisco?"}, {"role": "assistant", "function_call": {"name": "get_current_weather", "arguments": "{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"}}], "functions": [{"name": "get_current_weather", "description": "Get the current weather", "parameters": {"type": "object", "properties": {"location": {"type": "string", "description": "The city and country/region, eg. San Francisco, USA"}, "format": {"type": "string", "enum": ["celsius", "fahrenheit"]}}, "required": ["location", "format"]}}]}
```

As with all fine-tuning training, your example file requires at least 10 examples.

### Optimize for cost

To use fewer prompt tokens after fine-tuning on full function definitions, experiment with the following strategies:

| Strategy | Description |
|----------|-------------|
| Omit descriptions | Remove the `description` field from function and parameters. |
| Omit parameters | Remove the entire `properties` field from the `parameters` object. |
| Omit function entirely | Remove the entire function object from the functions array. |

### Optimize for quality

To improve the quality of function calling output, keep the function definitions in your fine-tuning training dataset and subsequent chat completion calls identical.

### Customize model responses to function outputs

You can also fine-tune on function calling examples to improve the model's response to function outputs. Include examples consisting of function response messages and assistant response messages where the function response is interpreted and put into context by the assistant.

```json
{
    "messages": [
        {"role": "user", "content": "What is the weather in San Francisco?"},
        {"role": "assistant", "function_call": {"name": "get_current_weather", "arguments": "{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"}}
        {"role": "function", "name": "get_current_weather", "content": "21.0"},
        {"role": "assistant", "content": "It is 21 degrees celsius in San Francisco, CA"}
    ],
    "functions": [...] // same as before
}
```

As with the example before, this example is artificially expanded for readability. The actual entry in the `.jsonl` training file would be a single line:

```jsonl
{"messages": [{"role": "user", "content": "What is the weather in San Francisco?"}, {"role": "assistant", "function_call": {"name": "get_current_weather", "arguments": "{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"}}, {"role": "function", "name": "get_current_weather", "content": "21.0"}, {"role": "assistant", "content": "It is 21 degrees celsius in San Francisco, CA"}], "functions": []}
```


## Next steps

* [Function calling fine-tuning scenarios](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/fine-tuning-with-function-calling-on-azure-openai-service/ba-p/4065968).
* Explore the fine-tuning capabilities in the [Azure OpenAI fine-tuning tutorial](../tutorials/fine-tune.md).
* Review fine-tuning [model regional availability](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models).
