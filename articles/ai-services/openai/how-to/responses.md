---
title: Azure OpenAI Responses API
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI's new stateful Responses API.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/21/2025
author: mrbullwinkle    
ms.author: mbullwin
ms.custom: references_regions
---

# Azure OpenAI Responses API (Preview)

The Responses API is a new stateful API from Azure OpenAI. It brings together the best capabilities from the chat completions and assistants API in one unified experience. The Responses API also adds support for the new `computer-use-preview` model which powers the [Computer use](../how-to/computer-use.md) capability.

## Responses API

### API support

`2025-03-01-preview` or later

### Region Availability

The responses API is currently available in the following regions:

- australiaeast
- eastus
- eastus2
- francecentral
- japaneast
- norwayeast
- southindia
- swedencentral
- uaenorth
- uksouth
- westus
- westus3

### Model support

- `gpt-4o` (Versions: `2024-11-20`, `2024-08-06`, `2024-05-13`)
- `gpt-4o-mini` (Version: `2024-07-18`)
- `computer-use-preview`
- `gpt-4.1` (Version: `2025-04-14`)
- `gpt-4.1-nano` (Version: `2025-04-14`)
- `gpt-4.1-mini` (Version: `2025-04-14`)
- `gpt-image-1` (Version: `2025-04-15`)
- `o3` (Version: `2025-04-16`)
- `o4-mini` (Version: `2025-04-16`)

Not every model is available in the regions supported by the responses API. Check the [models page](../concepts/models.md) for model region availability.

> [!NOTE]
> Not currently supported:
> - Structured outputs
> - image_url pointing to an internet address
> - The web search tool
> - Fine-tuned models
>
> There is also a known issue with vision performance when using the Responses API, particularly with OCR tasks. As a temporary workaround set image detail to `high`. This article will be updated once this issue is resolved and as any additional feature support is added.


### Reference documentation

- [Responses API reference documentation](/azure/ai-services/openai/reference-preview?#responses-api---create)

## Getting started with the responses API

To access the responses API commands, you need to upgrade your version of the OpenAI library.

```cmd
pip install --upgrade openai
```

## Generate a text response

# [Python (Microsoft Entra ID)](#tab/python-secure)

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

response = client.responses.create(
    model="gpt-4o", # replace with your model deployment name 
    input="This is a test."
    #truncation="auto" required when using computer-use-preview model.

)
```

# [Python (API Key)](#tab/python-key)

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2025-03-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

response = client.responses.create(
    model="gpt-4o", # replace with your model deployment name 
    input="This is a test."
    #truncation="auto" required when using computer-use-preview model.

)
```

# [REST API](#tab/rest-api)

### Microsoft Entra ID

```bash
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/responses?api-version=2025-03-01-preview" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
     "model": "gpt-4o",
     "input": "This is a test"
    }'
```

### API Key

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/responses?api-version=2025-03-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "gpt-4o",
     "input": "This is a test"
    }'
```

# [Output](#tab/output)

**Output:**

```json
{
  "id": "resp_67cb32528d6881909eb2859a55e18a85",
  "created_at": 1741369938.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-4o-2024-08-06",
  "object": "response",
  "output": [
    {
      "id": "msg_67cb3252cfac8190865744873aada798",
      "content": [
        {
          "annotations": [],
          "text": "Great! How can I help you today?",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": null,
      "type": "message"
    }
  ],
  "output_text": "Great! How can I help you today?",
  "parallel_tool_calls": null,
  "temperature": 1.0,
  "tool_choice": null,
  "tools": [],
  "top_p": 1.0,
  "max_output_tokens": null,
  "previous_response_id": null,
  "reasoning": null,
  "status": "completed",
  "text": null,
  "truncation": null,
  "usage": {
    "input_tokens": 20,
    "output_tokens": 11,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 31
  },
  "user": null,
  "reasoning_effort": null
}
```

---

## Retrieve a response

To retrieve a response from a previous call to the responses API.

# [Python (Microsoft Entra ID)](#tab/python-secure)

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

response = client.responses.retrieve("resp_67cb61fa3a448190bcf2c42d96f0d1a8")

print(response.model_dump_json(indent=2))
```

# [Python (API Key)](#tab/python-key)

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2025-03-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

response = client.responses.retrieve("resp_67cb61fa3a448190bcf2c42d96f0d1a8")
```

# [REST API](#tab/rest-api)

### Microsoft Entra ID

```bash
curl -X GET "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/responses/{response_id}?api-version=2025-03-01-preview" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" 
```

### API Key

```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/responses/{response_id}?api-version=2025-03-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
```

# [Output](#tab/output)

```json
{
  "id": "resp_67cb61fa3a448190bcf2c42d96f0d1a8",
  "created_at": 1741382138.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-4o-2024-08-06",
  "object": "response",
  "output": [
    {
      "id": "msg_67cb61fa95588190baf22ffbdbbaaa9d",
      "content": [
        {
          "annotations": [],
          "text": "Hello! How can I assist you today?",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": null,
      "type": "message"
    }
  ],
  "parallel_tool_calls": null,
  "temperature": 1.0,
  "tool_choice": null,
  "tools": [],
  "top_p": 1.0,
  "max_output_tokens": null,
  "previous_response_id": null,
  "reasoning": null,
  "status": "completed",
  "text": null,
  "truncation": null,
  "usage": {
    "input_tokens": 20,
    "output_tokens": 11,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 31
  },
  "user": null,
  "reasoning_effort": null
}
```

---

## Delete response

By default response data is retained for 30 days. To delete a response, you can use `response.delete"("{response_id})`

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

response = client.responses.delete("resp_67cb61fa3a448190bcf2c42d96f0d1a8")

print(response)
```

## Chaining responses together

You can chain responses together by passing the `response.id` from the previous response to the `previous_response_id` parameter.

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

response = client.responses.create(
    model="gpt-4o",  # replace with your model deployment name
    input="Define and explain the concept of catastrophic forgetting?"
)

second_response = client.responses.create(
    model="gpt-4o",  # replace with your model deployment name
    previous_response_id=response.id,
    input=[{"role": "user", "content": "Explain this at a level that could be understood by a college freshman"}]
)
print(second_response.model_dump_json(indent=2)) 
```

Note from the output that even though we never shared the first input question with the `second_response` API call, by passing the `previous_response_id` the model has full context of previous question and response to answer the new question.

**Output:**

```json
{
  "id": "resp_67cbc9705fc08190bbe455c5ba3d6daf",
  "created_at": 1741408624.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-4o-2024-08-06",
  "object": "response",
  "output": [
    {
      "id": "msg_67cbc970fd0881908353a4298996b3f6",
      "content": [
        {
          "annotations": [],
          "text": "Sure! Imagine you are studying for exams in different subjects like math, history, and biology. You spend a lot of time studying math first and get really good at it. But then, you switch to studying history. If you spend all your time and focus on history, you might forget some of the math concepts you learned earlier because your brain fills up with all the new history facts. \n\nIn the world of artificial intelligence (AI) and machine learning, a similar thing can happen with computers. We use special programs called neural networks to help computers learn things, sort of like how our brain works. But when a neural network learns a new task, it can forget what it learned before. This is what we call \"catastrophic forgetting.\"\n\nSo, if a neural network learned how to recognize cats in pictures, and then you teach it how to recognize dogs, it might get really good at recognizing dogs but suddenly become worse at recognizing cats. This happens because the process of learning new information can overwrite or mess with the old information in its \"memory.\"\n\nScientists and engineers are working on ways to help computers remember everything they learn, even as they keep learning new things, just like students have to remember math, history, and biology all at the same time for their exams. They use different techniques to make sure the neural network doesn’t forget the important stuff it learned before, even when it gets new information.",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": null,
      "type": "message"
    }
  ],
  "parallel_tool_calls": null,
  "temperature": 1.0,
  "tool_choice": null,
  "tools": [],
  "top_p": 1.0,
  "max_output_tokens": null,
  "previous_response_id": "resp_67cbc96babbc8190b0f69aedc655f173",
  "reasoning": null,
  "status": "completed",
  "text": null,
  "truncation": null,
  "usage": {
    "input_tokens": 405,
    "output_tokens": 285,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 690
  },
  "user": null,
  "reasoning_effort": null
}
```

### Chaining responses manually

Alternatively you can manually chain responses together using the method below:

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)


inputs = [{"type": "message", "role": "user", "content": "Define and explain the concept of catastrophic forgetting?"}] 
  
response = client.responses.create(  
    model="gpt-4o",  # replace with your model deployment name  
    input=inputs  
)  
  
inputs += response.output

inputs.append({"role": "user", "type": "message", "content": "Explain this at a level that could be understood by a college freshman"}) 
               

second_response = client.responses.create(  
    model="gpt-4o",  
    input=inputs
)  
      
print(second_response.model_dump_json(indent=2))  
```

## Streaming

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider = token_provider,
  api_version = "2025-04-01-preview" 
)

response = client.responses.create(
    input = "This is a test",
    model = "o4-mini", # replace with model deployment name
    stream = True
)

for event in response:
    if event.type == 'response.output_text.delta':
        print(event.delta, end='')

```


## Function calling

The responses API supports function calling.

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

response = client.responses.create(  
    model="gpt-4o",  # replace with your model deployment name  
    tools=[  
        {  
            "type": "function",  
            "name": "get_weather",  
            "description": "Get the weather for a location",  
            "parameters": {  
                "type": "object",  
                "properties": {  
                    "location": {"type": "string"},  
                },  
                "required": ["location"],  
            },  
        }  
    ],  
    input=[{"role": "user", "content": "What's the weather in San Francisco?"}],  
)  

print(response.model_dump_json(indent=2))  
  
# To provide output to tools, add a response for each tool call to an array passed  
# to the next response as `input`  
input = []  
for output in response.output:  
    if output.type == "function_call":  
        match output.name:  
            case "get_weather":  
                input.append(  
                    {  
                        "type": "function_call_output",  
                        "call_id": output.call_id,  
                        "output": '{"temperature": "70 degrees"}',  
                    }  
                )  
            case _:  
                raise ValueError(f"Unknown function call: {output.name}")  
  
second_response = client.responses.create(  
    model="gpt-4o",  
    previous_response_id=response.id,  
    input=input  
)  

print(second_response.model_dump_json(indent=2)) 

```

## List input items

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

response = client.responses.input_items.list("resp_67d856fcfba0819081fd3cffee2aa1c0")

print(response.model_dump_json(indent=2))
```

**Output:**

```json
{
  "data": [
    {
      "id": "msg_67d856fcfc1c8190ad3102fc01994c5f",
      "content": [
        {
          "text": "This is a test.",
          "type": "input_text"
        }
      ],
      "role": "user",
      "status": "completed",
      "type": "message"
    }
  ],
  "has_more": false,
  "object": "list",
  "first_id": "msg_67d856fcfc1c8190ad3102fc01994c5f",
  "last_id": "msg_67d856fcfc1c8190ad3102fc01994c5f"
}
```

## Image input

There is a known issue with image url based image input. Currently only base64 encoded images are supported.

### Image url

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "what is in this image?" },
                {
                    "type": "input_image",
                    "image_url": "<image_URL>"
                }
            ]
        }
    ]
)

print(response)

```

### Base64 encoded image

```python
import base64
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Path to your image
image_path = "path_to_your_image.jpg"

# Getting the Base64 string
base64_image = encode_image(image_path)

response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "what is in this image?" },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ]
)

print(response)
```

## Reasoning models

For examples of how to use reasoning models with the responses API see the [reasoning models guide](./reasoning.md#reasoning-summary).

## Computer use

In this section, we provide a simple example script that integrates Azure OpenAI's `computer-use-preview` model with [Playwright](https://playwright.dev/) to automate basic browser interactions. Combining the model with [Playwright](https://playwright.dev/) allows the model to see the browser screen, make decisions, and perform actions like clicking, typing, and navigating websites. You should exercise caution when running this example code. This code is designed to be run locally but should only be executed in a test environment. Use a human to confirm decisions and don't give the model access to sensitive data.

:::image type="content" source="../media/computer-use-preview.gif" alt-text="Animated gif of computer-use-preview model integrated with playwright." lightbox="../media/computer-use-preview.gif":::

First you'll need to install the Python library for [Playwright](https://playwright.dev/).

```cmd
pip install playwright
```

Once the package is installed, you'll also need to run

```cmd
playwright install
```

### Imports and configuration

First, we import the necessary libraries and define our configuration parameters. Since we're using `asyncio` we'll be executing this code outside of Jupyter notebooks. We'll walk through the code first in chunks and then demonstrate how to use it.

```python
import os
import asyncio
import base64
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from playwright.async_api import async_playwright, TimeoutError

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)


# Configuration

AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
MODEL = "computer-use-preview" # Set to model deployment name
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
API_VERSION = "2025-03-01-preview" #Use this API version or later
ITERATIONS = 5 # Max number of iterations before returning control to human supervisor
```

### Key mapping for browser interaction

Next, we set up mappings for special keys that the model might need to pass to Playwright. Ultimately the model is never performing actions itself, it passes representations of commands and you have to provide the final integration layer that can take those commands and execute them in your chosen environment.

This isn't an exhaustive list of possible key mappings. You can expand this list as needed. This dictionary is specific to integrating the model with Playwright. If you were integrating the model with an alternate library to provide API access to your operating systems keyboard/mouse you would need to provide a mapping specific to that library.

```python
# Key mapping for special keys in Playwright
KEY_MAPPING = {
    "/": "Slash", "\\": "Backslash", "alt": "Alt", "arrowdown": "ArrowDown",
    "arrowleft": "ArrowLeft", "arrowright": "ArrowRight", "arrowup": "ArrowUp",
    "backspace": "Backspace", "ctrl": "Control", "delete": "Delete", 
    "enter": "Enter", "esc": "Escape", "shift": "Shift", "space": " ",
    "tab": "Tab", "win": "Meta", "cmd": "Meta", "super": "Meta", "option": "Alt"
}
```

This dictionary translates user-friendly key names to the format expected by Playwright's keyboard API.

### Coordinate validation function

To make sure that any mouse actions that are passed from the model stay within the browser window boundaries we'll add the following utility function:

```python
def validate_coordinates(x, y):
    """Ensure coordinates are within display bounds."""
    return max(0, min(x, DISPLAY_WIDTH)), max(0, min(y, DISPLAY_HEIGHT))
```

This simple utility attempts to prevent out-of-bounds errors by clamping coordinates to the window dimensions.

### Action handling

The core of our browser automation is the action handler that processes various types of user interactions and convert them into actions within the browser.

```python
async def handle_action(page, action):
    """Handle different action types from the model."""
    action_type = action.type
    
    if action_type == "drag":
        print("Drag action is not supported in this implementation. Skipping.")
        return
        
    elif action_type == "click":
        button = getattr(action, "button", "left")
        # Validate coordinates
        x, y = validate_coordinates(action.x, action.y)
        
        print(f"\tAction: click at ({x}, {y}) with button '{button}'")
        
        if button == "back":
            await page.go_back()
        elif button == "forward":
            await page.go_forward()
        elif button == "wheel":
            await page.mouse.wheel(x, y)
        else:
            button_type = {"left": "left", "right": "right", "middle": "middle"}.get(button, "left")
            await page.mouse.click(x, y, button=button_type)
            try:
                await page.wait_for_load_state("domcontentloaded", timeout=3000)
            except TimeoutError:
                pass
        
    elif action_type == "double_click":
        # Validate coordinates
        x, y = validate_coordinates(action.x, action.y)
        
        print(f"\tAction: double click at ({x}, {y})")
        await page.mouse.dblclick(x, y)
        
    elif action_type == "scroll":
        scroll_x = getattr(action, "scroll_x", 0)
        scroll_y = getattr(action, "scroll_y", 0)
        # Validate coordinates
        x, y = validate_coordinates(action.x, action.y)
        
        print(f"\tAction: scroll at ({x}, {y}) with offsets ({scroll_x}, {scroll_y})")
        await page.mouse.move(x, y)
        await page.evaluate(f"window.scrollBy({{left: {scroll_x}, top: {scroll_y}, behavior: 'smooth'}});")
        
    elif action_type == "keypress":
        keys = getattr(action, "keys", [])
        print(f"\tAction: keypress {keys}")
        mapped_keys = [KEY_MAPPING.get(key.lower(), key) for key in keys]
        
        if len(mapped_keys) > 1:
            # For key combinations (like Ctrl+C)
            for key in mapped_keys:
                await page.keyboard.down(key)
            await asyncio.sleep(0.1)
            for key in reversed(mapped_keys):
                await page.keyboard.up(key)
        else:
            for key in mapped_keys:
                await page.keyboard.press(key)
                
    elif action_type == "type":
        text = getattr(action, "text", "")
        print(f"\tAction: type text: {text}")
        await page.keyboard.type(text, delay=20)
        
    elif action_type == "wait":
        ms = getattr(action, "ms", 1000)
        print(f"\tAction: wait {ms}ms")
        await asyncio.sleep(ms / 1000)
        
    elif action_type == "screenshot":
        print("\tAction: screenshot")
        
    else:
        print(f"\tUnrecognized action: {action_type}")
```

This function attempts to handle various types of actions. We need to translate between the commands that the `computer-use-preview` will generate and the Playwright library which will execute the actions. For more information refer to the reference documentation for `ComputerAction`.

- [Click](/azure/ai-services/openai/reference-preview#click)
- [DoubleClick](/azure/ai-services/openai/reference-preview#doubleclick)
- [Drag](/azure/ai-services/openai/reference-preview#drag)
- [KeyPress](/azure/ai-services/openai/reference-preview#keypress)
- [Move](/azure/ai-services/openai/reference-preview#move)
- [Screenshot](/azure/ai-services/openai/reference-preview#screenshot)
- [Scroll](/azure/ai-services/openai/reference-preview#scroll)
- [Type](/azure/ai-services/openai/reference-preview#type)
- [Wait](/azure/ai-services/openai/reference-preview#wait)

### Screenshot capture

In order for the model to be able to see what it's interacting with the model needs a way to capture screenshots. For this code we're using Playwright to capture the screenshots and we're limiting the view to just the content in the browser window. The screenshot won't include the url bar or other aspects of the browser GUI. If you need the model to see outside the main browser window you could augment the model by creating your own screenshot function. 

```python
async def take_screenshot(page):
    """Take a screenshot and return base64 encoding with caching for failures."""
    global last_successful_screenshot
    
    try:
        screenshot_bytes = await page.screenshot(full_page=False)
        last_successful_screenshot = base64.b64encode(screenshot_bytes).decode("utf-8")
        return last_successful_screenshot
    except Exception as e:
        print(f"Screenshot failed: {e}")
        print(f"Using cached screenshot from previous successful capture")
        if last_successful_screenshot:
            return last_successful_screenshot
```

This function captures the current browser state as an image and returns it as a base64-encoded string, ready to be sent to the model. We'll constantly do this in a loop after each step allowing the model to see if the command it tried to execute was successful or not, which then allows it to adjust based on the contents of the screenshot. We could let the model decide if it needs to take a screenshot, but for simplicity we will force a screenshot to be taken for each iteration.

### Model response processing

This function processes the model's responses and executes the requested actions:

```python
async def process_model_response(client, response, page, max_iterations=ITERATIONS):
    """Process the model's response and execute actions."""
    for iteration in range(max_iterations):
        if not hasattr(response, 'output') or not response.output:
            print("No output from model.")
            break
        
        # Safely access response id
        response_id = getattr(response, 'id', 'unknown')
        print(f"\nIteration {iteration + 1} - Response ID: {response_id}\n")
        
        # Print text responses and reasoning
        for item in response.output:
            # Handle text output
            if hasattr(item, 'type') and item.type == "text":
                print(f"\nModel message: {item.text}\n")
                
            # Handle reasoning output
            if hasattr(item, 'type') and item.type == "reasoning":
                # Extract meaningful content from the reasoning
                meaningful_content = []
                
                if hasattr(item, 'summary') and item.summary:
                    for summary in item.summary:
                        # Handle different potential formats of summary content
                        if isinstance(summary, str) and summary.strip():
                            meaningful_content.append(summary)
                        elif hasattr(summary, 'text') and summary.text.strip():
                            meaningful_content.append(summary.text)
                
                # Only print reasoning section if there's actual content
                if meaningful_content:
                    print("=== Model Reasoning ===")
                    for idx, content in enumerate(meaningful_content, 1):
                        print(f"{content}")
                    print("=====================\n")
        
        # Extract computer calls
        computer_calls = [item for item in response.output 
                         if hasattr(item, 'type') and item.type == "computer_call"]
        
        if not computer_calls:
            print("No computer call found in response. Reverting control to human operator")
            break
        
        computer_call = computer_calls[0]
        if not hasattr(computer_call, 'call_id') or not hasattr(computer_call, 'action'):
            print("Computer call is missing required attributes.")
            break
        
        call_id = computer_call.call_id
        action = computer_call.action
        
        # Handle safety checks
        acknowledged_checks = []
        if hasattr(computer_call, 'pending_safety_checks') and computer_call.pending_safety_checks:
            pending_checks = computer_call.pending_safety_checks
            print("\nSafety checks required:")
            for check in pending_checks:
                print(f"- {check.code}: {check.message}")
            
            if input("\nDo you want to proceed? (y/n): ").lower() != 'y':
                print("Operation cancelled by user.")
                break
            
            acknowledged_checks = pending_checks
        
        # Execute the action
        try:
           await page.bring_to_front()
           await handle_action(page, action)
           
           # Check if a new page was created after the action
           if action.type in ["click"]:
               await asyncio.sleep(1.5)
               # Get all pages in the context
               all_pages = page.context.pages
               # If we have multiple pages, check if there's a newer one
               if len(all_pages) > 1:
                   newest_page = all_pages[-1]  # Last page is usually the newest
                   if newest_page != page and newest_page.url not in ["about:blank", ""]:
                       print(f"\tSwitching to new tab: {newest_page.url}")
                       page = newest_page  # Update our page reference
           elif action.type != "wait":
               await asyncio.sleep(0.5)
               
        except Exception as e:
           print(f"Error handling action {action.type}: {e}")
           import traceback
           traceback.print_exc()    

        # Take a screenshot after the action
        screenshot_base64 = await take_screenshot(page)

        print("\tNew screenshot taken")
        
        # Prepare input for the next request
        input_content = [{
            "type": "computer_call_output",
            "call_id": call_id,
            "output": {
                "type": "input_image",
                "image_url": f"data:image/png;base64,{screenshot_base64}"
            }
        }]
        
        # Add acknowledged safety checks if any
        if acknowledged_checks:
            acknowledged_checks_dicts = []
            for check in acknowledged_checks:
                acknowledged_checks_dicts.append({
                    "id": check.id,
                    "code": check.code,
                    "message": check.message
                })
            input_content[0]["acknowledged_safety_checks"] = acknowledged_checks_dicts
        
        # Add current URL for context
        try:
            current_url = page.url
            if current_url and current_url != "about:blank":
                input_content[0]["current_url"] = current_url
                print(f"\tCurrent URL: {current_url}")
        except Exception as e:
            print(f"Error getting URL: {e}")
        
        # Send the screenshot back for the next step
        try:
            response = client.responses.create(
                model=MODEL,
                previous_response_id=response_id,
                tools=[{
                    "type": "computer_use_preview",
                    "display_width": DISPLAY_WIDTH,
                    "display_height": DISPLAY_HEIGHT,
                    "environment": "browser"
                }],
                input=input_content,
                truncation="auto"
            )

            print("\tModel processing screenshot")
        except Exception as e:
            print(f"Error in API call: {e}")
            import traceback
            traceback.print_exc()
            break
    
    if iteration >= max_iterations - 1:
        print("Reached maximum number of iterations. Stopping.")
```

In this section we have added code that:

- Extracts and displays text and reasoning from the model.
- Processes computer action calls.
- Handles potential safety checks requiring user confirmation.
- Executes the requested action.
- Captures a new screenshot.
- Sends the updated state back to the model and defines the [`ComputerTool`](/azure/ai-services/openai/reference-preview#computertool).
- Repeats this process for multiple iterations.

### Main function

The main function coordinates the entire process:

```python
    # Initialize OpenAI client
    client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        azure_ad_token_provider=token_provider,
        api_version=API_VERSION
    )
    
    # Initialize Playwright
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
            args=[f"--window-size={DISPLAY_WIDTH},{DISPLAY_HEIGHT}", "--disable-extensions"]
        )
        
        context = await browser.new_context(
            viewport={"width": DISPLAY_WIDTH, "height": DISPLAY_HEIGHT},
            accept_downloads=True
        )
        
        page = await context.new_page()
        
        # Navigate to starting page
        await page.goto("https://www.bing.com", wait_until="domcontentloaded")
        print("Browser initialized to Bing.com")
        
        # Main interaction loop
        try:
            while True:
                print("\n" + "="*50)
                user_input = input("Enter a task to perform (or 'exit' to quit): ")
                
                if user_input.lower() in ('exit', 'quit'):
                    break
                
                if not user_input.strip():
                    continue
                
                # Take initial screenshot
                screenshot_base64 = await take_screenshot(page)
                print("\nTake initial screenshot")
                
                # Initial request to the model
                response = client.responses.create(
                    model=MODEL,
                    tools=[{
                        "type": "computer_use_preview",
                        "display_width": DISPLAY_WIDTH,
                        "display_height": DISPLAY_HEIGHT,
                        "environment": "browser"
                    }],
                    instructions = "You are an AI agent with the ability to control a browser. You can control the keyboard and mouse. You take a screenshot after each action to check if your action was successful. Once you have completed the requested task you should stop running and pass back control to your human operator.",
                    input=[{
                        "role": "user",
                        "content": [{
                            "type": "input_text",
                            "text": user_input
                        }, {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{screenshot_base64}"
                        }]
                    }],
                    reasoning={"generate_summary": "concise"},
                    truncation="auto"
                )
                print("\nSending model initial screenshot and instructions")

                # Process model actions
                await process_model_response(client, response, page)
                
        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Close browser
            await context.close()
            await browser.close()
            print("Browser closed.")

if __name__ == "__main__":
    asyncio.run(main())
```

The main function:

- Initializes the AzureOpenAI client.
- Sets up the Playwright browser.
- Starts at Bing.com.
- Enters a loop to accept user tasks.
- Captures the initial state.
- Sends the task and screenshot to the model.
- Processes the model's response.
- Repeats until the user exits.
- Ensures the browser is properly closed.

### Complete script

> [!CAUTION]
> This code is experimental and for demonstration purposes only. It's only intended to illustrate the basic flow of the responses API and the `computer-use-preview` model. While you can execute this code on your local computer, we strongly recommend running this code on a low privilege virtual machine with no access to sensitive data. This code is for basic testing purposes only.

```python
import os
import asyncio
import base64
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from playwright.async_api import async_playwright, TimeoutError


token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

# Configuration

AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
MODEL = "computer-use-preview"
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
API_VERSION = "2025-03-01-preview"
ITERATIONS = 5 # Max number of iterations before forcing the model to return control to the human supervisor

# Key mapping for special keys in Playwright
KEY_MAPPING = {
    "/": "Slash", "\\": "Backslash", "alt": "Alt", "arrowdown": "ArrowDown",
    "arrowleft": "ArrowLeft", "arrowright": "ArrowRight", "arrowup": "ArrowUp",
    "backspace": "Backspace", "ctrl": "Control", "delete": "Delete", 
    "enter": "Enter", "esc": "Escape", "shift": "Shift", "space": " ",
    "tab": "Tab", "win": "Meta", "cmd": "Meta", "super": "Meta", "option": "Alt"
}

def validate_coordinates(x, y):
    """Ensure coordinates are within display bounds."""
    return max(0, min(x, DISPLAY_WIDTH)), max(0, min(y, DISPLAY_HEIGHT))

async def handle_action(page, action):
    """Handle different action types from the model."""
    action_type = action.type
    
    if action_type == "drag":
        print("Drag action is not supported in this implementation. Skipping.")
        return
        
    elif action_type == "click":
        button = getattr(action, "button", "left")
        # Validate coordinates
        x, y = validate_coordinates(action.x, action.y)
        
        print(f"\tAction: click at ({x}, {y}) with button '{button}'")
        
        if button == "back":
            await page.go_back()
        elif button == "forward":
            await page.go_forward()
        elif button == "wheel":
            await page.mouse.wheel(x, y)
        else:
            button_type = {"left": "left", "right": "right", "middle": "middle"}.get(button, "left")
            await page.mouse.click(x, y, button=button_type)
            try:
                await page.wait_for_load_state("domcontentloaded", timeout=3000)
            except TimeoutError:
                pass
        
    elif action_type == "double_click":
        # Validate coordinates
        x, y = validate_coordinates(action.x, action.y)
        
        print(f"\tAction: double click at ({x}, {y})")
        await page.mouse.dblclick(x, y)
        
    elif action_type == "scroll":
        scroll_x = getattr(action, "scroll_x", 0)
        scroll_y = getattr(action, "scroll_y", 0)
        # Validate coordinates
        x, y = validate_coordinates(action.x, action.y)
        
        print(f"\tAction: scroll at ({x}, {y}) with offsets ({scroll_x}, {scroll_y})")
        await page.mouse.move(x, y)
        await page.evaluate(f"window.scrollBy({{left: {scroll_x}, top: {scroll_y}, behavior: 'smooth'}});")
        
    elif action_type == "keypress":
        keys = getattr(action, "keys", [])
        print(f"\tAction: keypress {keys}")
        mapped_keys = [KEY_MAPPING.get(key.lower(), key) for key in keys]
        
        if len(mapped_keys) > 1:
            # For key combinations (like Ctrl+C)
            for key in mapped_keys:
                await page.keyboard.down(key)
            await asyncio.sleep(0.1)
            for key in reversed(mapped_keys):
                await page.keyboard.up(key)
        else:
            for key in mapped_keys:
                await page.keyboard.press(key)
                
    elif action_type == "type":
        text = getattr(action, "text", "")
        print(f"\tAction: type text: {text}")
        await page.keyboard.type(text, delay=20)
        
    elif action_type == "wait":
        ms = getattr(action, "ms", 1000)
        print(f"\tAction: wait {ms}ms")
        await asyncio.sleep(ms / 1000)
        
    elif action_type == "screenshot":
        print("\tAction: screenshot")
        
    else:
        print(f"\tUnrecognized action: {action_type}")

async def take_screenshot(page):
    """Take a screenshot and return base64 encoding with caching for failures."""
    global last_successful_screenshot
    
    try:
        screenshot_bytes = await page.screenshot(full_page=False)
        last_successful_screenshot = base64.b64encode(screenshot_bytes).decode("utf-8")
        return last_successful_screenshot
    except Exception as e:
        print(f"Screenshot failed: {e}")
        print(f"Using cached screenshot from previous successful capture")
        if last_successful_screenshot:
            return last_successful_screenshot


async def process_model_response(client, response, page, max_iterations=ITERATIONS):
    """Process the model's response and execute actions."""
    for iteration in range(max_iterations):
        if not hasattr(response, 'output') or not response.output:
            print("No output from model.")
            break
        
        # Safely access response id
        response_id = getattr(response, 'id', 'unknown')
        print(f"\nIteration {iteration + 1} - Response ID: {response_id}\n")
        
        # Print text responses and reasoning
        for item in response.output:
            # Handle text output
            if hasattr(item, 'type') and item.type == "text":
                print(f"\nModel message: {item.text}\n")
                
            # Handle reasoning output
            if hasattr(item, 'type') and item.type == "reasoning":
                # Extract meaningful content from the reasoning
                meaningful_content = []
                
                if hasattr(item, 'summary') and item.summary:
                    for summary in item.summary:
                        # Handle different potential formats of summary content
                        if isinstance(summary, str) and summary.strip():
                            meaningful_content.append(summary)
                        elif hasattr(summary, 'text') and summary.text.strip():
                            meaningful_content.append(summary.text)
                
                # Only print reasoning section if there's actual content
                if meaningful_content:
                    print("=== Model Reasoning ===")
                    for idx, content in enumerate(meaningful_content, 1):
                        print(f"{content}")
                    print("=====================\n")
        
        # Extract computer calls
        computer_calls = [item for item in response.output 
                         if hasattr(item, 'type') and item.type == "computer_call"]
        
        if not computer_calls:
            print("No computer call found in response. Reverting control to human supervisor")
            break
        
        computer_call = computer_calls[0]
        if not hasattr(computer_call, 'call_id') or not hasattr(computer_call, 'action'):
            print("Computer call is missing required attributes.")
            break
        
        call_id = computer_call.call_id
        action = computer_call.action
        
        # Handle safety checks
        acknowledged_checks = []
        if hasattr(computer_call, 'pending_safety_checks') and computer_call.pending_safety_checks:
            pending_checks = computer_call.pending_safety_checks
            print("\nSafety checks required:")
            for check in pending_checks:
                print(f"- {check.code}: {check.message}")
            
            if input("\nDo you want to proceed? (y/n): ").lower() != 'y':
                print("Operation cancelled by user.")
                break
            
            acknowledged_checks = pending_checks
        
        # Execute the action
        try:
           await page.bring_to_front()
           await handle_action(page, action)
           
           # Check if a new page was created after the action
           if action.type in ["click"]:
               await asyncio.sleep(1.5)
               # Get all pages in the context
               all_pages = page.context.pages
               # If we have multiple pages, check if there's a newer one
               if len(all_pages) > 1:
                   newest_page = all_pages[-1]  # Last page is usually the newest
                   if newest_page != page and newest_page.url not in ["about:blank", ""]:
                       print(f"\tSwitching to new tab: {newest_page.url}")
                       page = newest_page  # Update our page reference
           elif action.type != "wait":
               await asyncio.sleep(0.5)
               
        except Exception as e:
           print(f"Error handling action {action.type}: {e}")
           import traceback
           traceback.print_exc()    

        # Take a screenshot after the action
        screenshot_base64 = await take_screenshot(page)

        print("\tNew screenshot taken")
        
        # Prepare input for the next request
        input_content = [{
            "type": "computer_call_output",
            "call_id": call_id,
            "output": {
                "type": "input_image",
                "image_url": f"data:image/png;base64,{screenshot_base64}"
            }
        }]
        
        # Add acknowledged safety checks if any
        if acknowledged_checks:
            acknowledged_checks_dicts = []
            for check in acknowledged_checks:
                acknowledged_checks_dicts.append({
                    "id": check.id,
                    "code": check.code,
                    "message": check.message
                })
            input_content[0]["acknowledged_safety_checks"] = acknowledged_checks_dicts
        
        # Add current URL for context
        try:
            current_url = page.url
            if current_url and current_url != "about:blank":
                input_content[0]["current_url"] = current_url
                print(f"\tCurrent URL: {current_url}")
        except Exception as e:
            print(f"Error getting URL: {e}")
        
        # Send the screenshot back for the next step
        try:
            response = client.responses.create(
                model=MODEL,
                previous_response_id=response_id,
                tools=[{
                    "type": "computer_use_preview",
                    "display_width": DISPLAY_WIDTH,
                    "display_height": DISPLAY_HEIGHT,
                    "environment": "browser"
                }],
                input=input_content,
                truncation="auto"
            )

            print("\tModel processing screenshot")
        except Exception as e:
            print(f"Error in API call: {e}")
            import traceback
            traceback.print_exc()
            break
    
    if iteration >= max_iterations - 1:
        print("Reached maximum number of iterations. Stopping.")
        
async def main():    
    # Initialize OpenAI client
    client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        azure_ad_token_provider=token_provider,
        api_version=API_VERSION
    )
    
    # Initialize Playwright
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
            args=[f"--window-size={DISPLAY_WIDTH},{DISPLAY_HEIGHT}", "--disable-extensions"]
        )
        
        context = await browser.new_context(
            viewport={"width": DISPLAY_WIDTH, "height": DISPLAY_HEIGHT},
            accept_downloads=True
        )
        
        page = await context.new_page()
        
        # Navigate to starting page
        await page.goto("https://www.bing.com", wait_until="domcontentloaded")
        print("Browser initialized to Bing.com")
        
        # Main interaction loop
        try:
            while True:
                print("\n" + "="*50)
                user_input = input("Enter a task to perform (or 'exit' to quit): ")
                
                if user_input.lower() in ('exit', 'quit'):
                    break
                
                if not user_input.strip():
                    continue
                
                # Take initial screenshot
                screenshot_base64 = await take_screenshot(page)
                print("\nTake initial screenshot")
                
                # Initial request to the model
                response = client.responses.create(
                    model=MODEL,
                    tools=[{
                        "type": "computer_use_preview",
                        "display_width": DISPLAY_WIDTH,
                        "display_height": DISPLAY_HEIGHT,
                        "environment": "browser"
                    }],
                    instructions = "You are an AI agent with the ability to control a browser. You can control the keyboard and mouse. You take a screenshot after each action to check if your action was successful. Once you have completed the requested task you should stop running and pass back control to your human supervisor.",
                    input=[{
                        "role": "user",
                        "content": [{
                            "type": "input_text",
                            "text": user_input
                        }, {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{screenshot_base64}"
                        }]
                    }],
                    reasoning={"generate_summary": "concise"},
                    truncation="auto"
                )
                print("\nSending model initial screenshot and instructions")

                # Process model actions
                await process_model_response(client, response, page)
                
        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Close browser
            await context.close()
            await browser.close()
            print("Browser closed.")

if __name__ == "__main__":
    asyncio.run(main())
```
