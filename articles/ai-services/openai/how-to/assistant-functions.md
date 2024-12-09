---
title: 'How to use Azure OpenAI Assistants function calling'
titleSuffix: Azure OpenAI
description: Learn how to use Assistants function calling
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 09/04/2024
author: aahill
ms.author: aahi
recommendations: false

---

# Azure OpenAI Assistants function calling

The Assistants API supports function calling, which allows you to describe the structure of functions to an Assistant and then return the functions that need to be called along with their arguments.

[!INCLUDE [Assistants v2 note](../includes/assistants-v2-note.md)]

## Function calling support

### Supported models

The [models page](../concepts/models.md#assistants-preview) contains the most up-to-date information on regions/models where Assistants are supported.

To use all features of function calling including parallel functions, you need to use a model that was released after November 6th 2023.

### API Versions

API versions starting with `2024-02-15-preview`.

## Example function definition

> [!NOTE]
> * We've added support for the `tool_choice` parameter which can be used to force the use of a specific tool (like `file_search`, `code_interpreter`, or a `function`) in a particular run. 
> * Runs expire ten minutes after creation. Be sure to submit your tool outputs before this expiration.
> * You can also perform function calling [with Azure Logic apps](./assistants-logic-apps.md)

# [Python 1.x](#tab/python)

```python
from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-07-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

assistant = client.beta.assistants.create(
  name="Weather Bot",
  instructions="You are a weather bot. Use the provided functions to answer questions.",
  model="gpt-4", #Replace with model deployment name
  tools=[{
      "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get the weather in location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "The city name, for example San Francisco"}
        },
        "required": ["location"]
      }
    }
  }]
)
```

# [REST](#tab/rest)

> [!NOTE]
> With Azure OpenAI the `model` parameter requires model deployment name. If your model deployment name is different than the underlying model name then you would adjust your code to ` "model": "{your-custom-model-deployment-name}"`.

```console
curl https://YOUR_RESOURCE_NAME.openai.azure.com/openai/assistants?api-version=2024-07-01-preview \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are a weather bot. Use the provided functions to answer questions.",
    tools=[{
      "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get the weather in location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "The city name, for example San Francisco"}
        },
        "required": ["location"]
      }
    }
  }],
    "model": "gpt-4-1106-preview"
  }'
```

---

## Reading the functions

When you initiate a **Run** with a user Message that triggers the function, the **Run** will enter a pending status. After it processes, the run will enter a requires_action state that you can verify by retrieving the **Run**.

```json
{
  "id": "run_abc123",
  "object": "thread.run",
  "assistant_id": "asst_abc123",
  "thread_id": "thread_abc123",
  "status": "requires_action",
  "required_action": {
    "type": "submit_tool_outputs",
    "submit_tool_outputs": {
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "get_weather",
            "arguments": "{\"location\":\"Seattle\"}"
          }
        },
      ]
    }
  },
...
```

## Submitting function outputs

You can then complete the **Run** by submitting the tool output from the function(s) you call. Pass the `tool_call_id` referenced in the `required_action` object to match output to each function call.


# [Python 1.x](#tab/python)

```python

# Example function
def get_weather():
    return "It's 80 degrees F and slightly cloudy."

# Define the list to store tool outputs
tool_outputs = []
 
# Loop through each tool in the required action section
for tool in run.required_action.submit_tool_outputs.tool_calls:
  # get data from the weather function
  if tool.function.name == "get_weather":
    weather = get_weather()
    tool_outputs.append({
      "tool_call_id": tool.id,
      "output": weather
    })
 
# Submit all tool outputs at once after collecting them in a list
if tool_outputs:
  try:
    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
      thread_id=thread.id,
      run_id=run.id,
      tool_outputs=tool_outputs
    )
    print("Tool outputs submitted successfully.")
  except Exception as e:
    print("Failed to submit tool outputs:", e)
else:
  print("No tool outputs to submit.")
 
if run.status == 'completed':
  print("run status: ", run.status)
  messages = client.beta.threads.messages.list(thread_id=thread.id)
  print(messages.to_json(indent=2))

else:
  print("run status: ", run.status)
  print (run.last_error.message)
```

# [REST](#tab/rest)

In the following example, replace `output` with the output of the function you want to use.
 
```console
curl https://YOUR_RESOURCE_NAME.openai.azure.com/openai/threads/thread_abc123/runs/run_123/submit_tool_outputs?api-version=2024-07-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: 851c6e0b83744d8c8fc2a07eab098376" \
  -d '{
    "tool_outputs": [{
      "tool_call_id": "call_123",
      "output": "{\"60 degrees F and raining\"}"
    }]
  }'
```

---

After you submit tool outputs, the **Run** will enter the `queued` state before it continues execution.

## See also

* [Assistants API Reference](../assistants-reference.md)
* Learn more about how to use Assistants with our [How-to guide on Assistants](../how-to/assistant.md).
* [Azure OpenAI Assistants API samples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/Assistants)
