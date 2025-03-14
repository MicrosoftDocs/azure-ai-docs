---
title: 'Computer Use (preview) in Azure OpenAI'
titleSuffix: Azure OpenAI
description: Learn about Computer Use in Azure OpenAI which allows AI to interact with computer applications.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 03/14/2025
author: aahill
ms.author: aahi
---

# Computer Use (preview) in Azure OpenAI

Use this article to learn how to work with Computer Use in Azure OpenAI. Computer Use is a specialized AI tool that uses a specialized model that can perform tasks by interacting with computer systems and applications through their UIs. With Computer Use, you can create an agent that can handle complex tasks and make decisions by interpreting visual elements and taking action based on on-screen content. 

Computer Use provides:

* **Autonomous navigation**: For example, opens applications, clicks buttons, fills out forms, and navigates multi-page workflows.
* **Dynamic adaptation**: Interprets UI changes and adjusts actions accordingly.
* **Cross-application task execution**: Operates across web-based and desktop applications.
* **Natural language interface**: Users can describe a task in plain language, and the Computer Use model determines the correct UI interactions to execute.   

## Request access

Access to Computer Use is limited. You will need to fill out the [access request form](https://aka.ms/oai/cuaaccess) before you can start using the model.

## Regional support

Computer Use is available in the following regions:
* `eastus2`
* `swedencentral`
* `southindia`

## Sending an API call to the Computer Use model using the responses API

The Computer Use tool is accessed through the responses API. The tool operates in a continuous loop that sends actions such as typing text or performing a click. Your code executes these actions on a computer, and sends screenshots of the outcome to the model. 

In this way, your code simulates the actions of a human using a computer interface, while the model uses the screenshots to understand the state of the environment and suggest next actions.

The following examples show a basic API call. 

> [!NOTE]
> You need an Azure OpenAI resource with a `computer-use-preview` model deployment in a [supported region](#regional-support).

## [Python](#tab/python)

To send requests, you will need to install the following Python packages.

```console
pip install openai
pip install azure-identity
```

```python
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

#from openai import OpenAI
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

client = AzureOpenAI(
    azure_ad_token_provider=token_provider,
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2025-03-01-preview"
)

response = client.responses.create(
    model="computer-use-preview",
    tools=[{
        "type": "computer-preview",
        "display_width": 1024,
        "display_height": 768,
        "environment": "browser" # other possible values: "mac", "windows", "ubuntu"
    }],
    input=[
        {
            "role": "user",
            "content": "Check the latest OpenAI news on bing.com."
        }
    ]
)

print(response.output)
```

### Output

```console
[
    ResponseComputerToolCall(
        id='comp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx', 
        action=ActionScreenshot(type='screenshot'), 
        call_id=None, 
        pending_safety_checks=None, 
        status=None, 
        type='computer_call'
    )
]
```

## [REST API](#tab/rest-api)

```bash
curl ${MY_ENDPOINT}/openai/responses?api-version=2025-03-01-preview \ 
  -H "Content-Type: application/json" \ 
  -H "api-key: $MY_API_KEY" \ 
  -d '{ 
    "model": "computer-use-preview", 
    "input": [ 
      { 
        "type": "message", 
        "role": "user", 
        "content": "Search Bing for the latest news in AI." 
      },
      "tools": [{
        "type": "computer-preview",
        "display_width": 1024,
        "display_height": 768,
        "environment": "browser" # other possible values: "mac", "windows", "ubuntu"
      }]
    ] 
  }' 
```

### Output

```json
{
  "id": "resp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "object": "response",
  "created_at": 1741716005,
  "status": "completed",
  "model": "computer-use-preview-2025-02-11",
  "previous_response_id": null,
  "output": [
    {
      "type": "computer_call",
      "id": "comp_xxxxxxxxxxxxxxxxxxxx",
      "action": {
        "type": "screenshot"
      }
    }
  ],
  "error": null,
  "tools": [
    {
      "type": "computer-preview",
      "environment": "browser",
      "display_width": 1024,
      "display_height": 768
    }
  ],
  "top_p": 1.0,
  "temperature": 1.0,
  "reasoning_effort": null,
  "usage": {
    "input_tokens": 510,
    "output_tokens": 7,
    "total_tokens": 517,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  },
  "metadata": {}
```

---

Once the initial API request is sent, you perform a loop where the specified action is performed in your application code, sending a screenshot with each turn so the model can evaluate the updated state of the environment.

## [Python](#tab/python)

```python

## response.output is the previous response from the model
computer_calls = [item for item in response.output if item.type == "computer_call"]
if not computer_calls:
    print("No computer call found. Output from model:")
    for item in response.output:
        print(item)

computer_call = computer_calls[0]
last_call_id = computer_call.call_id
action = computer_call.action

# Your application would now perform the action suggested by the model
# And create a screenshot of the updated state of the environment before sending another response

response_2 = client.responses.create(
    model="computer-use-preview",
    previous_response_id=response.id,
    tools=[{
        "type": "computer-preview",
        "display_width": 1024,
        "display_height": 768
        "environment": "browser" # other possible values: "mac", "windows", "ubuntu"
    }],
    input=[
        {
            "call_id": last_call_id,
            "type": "computer_call_output",
            "output": {
                "type": "input_image",
                # Image should be in base64
                "image_url": f"data:image/png;base64,{<base64_string>}"
            }
        }
    ]
)
```


## [REST API](#tab/rest-api)

```bash
curl ${MY_ENDPOINT}/openai/responses?api-version=2025-03-01-preview \ 
  -H "Content-Type: application/json" \ 
  -H "api-key: $MY_API_KEY" \ 
  -d '{ 
    "model": "computer-use-preview", 
    "input": [ 
      "tools": [{
        "type": "computer-preview",
        "display_width": 1024,
        "display_height": 768,
        "environment": "browser" # other possible values: "mac", "windows", "ubuntu"
      }], 
        {
        "call_id": last_call_id,
        "type": "computer_call_output",
        "output": {
            "type": "input_image",
            "image_url": "<base64_string>"
        }
      }
    ]
  }' 
```

---
## Understanding the Computer Use integration

When working with the Computer Use tool, you typically would perform the following to integrate it into your application.

1. Send a request to the model with that includes the computer use tool, and the display size and environment. You can also include a screenshot of the initial state of the environment in the first API request. 
1. Receive a response from the model. If the response has `action` items, those items contain suggested actions to make progress toward the specified goal. For example an action might be `screenshot` so the model can assess the current state with an updated screenshot, or `click` with X/Y coordinates indicating where the mouse should be moved.
1. Execute the action using your application code on your computer or browser environment.
1. After executing the action, capture the updated state of the environment as a screenshot.
1. Send a new request with the updated state as a `computer_call_output`, and repeat this loop until the model stops requesting actions or you decide to stop. 

## Handling conversation history

You can use the `previous_response_id` parameter to link the current request to the previous response. Using this parameter is recommended if you don't want to manage the conversation history.

If you don't use this parameter, you should make sure to include all the items returned in the response output of the previous request in your inputs array. This includes reasoning items if present.

## Safety checks

The API has safety checks to help protect against prompt injection and model mistakes. These checks include:

* **Malicious instruction detection**: The system evaluates the screenshot image and checks if it contains adversarial content that might change the model's behavior.
* **Irrelevant domain detection**: The system evaluates the `current_url` (if provided) and checks if the current domain is considered relevant given the conversation history.
* **Sensitive domain detection**: The system checks the `current_url` (if provided) and raises a warning when it detects the user is on a sensitive domain.

If one or more of the above checks is triggered, a safety check is raised when the model returns the next `computer_call`, with the `pending_safety_checks` parameter.

```json
"output": [
    {
        "type": "reasoning",
        "id": "rs_67cb...",
        "summary": [
            {
                "type": "summary_text",
                "text": "Exploring 'File' menu option."
            }
        ]
    },
    {
        "type": "computer_call",
        "id": "cu_67cb...",
        "call_id": "call_nEJ...",
        "action": {
            "type": "click",
            "button": "left",
            "x": 135,
            "y": 193
        },
        "pending_safety_checks": [
            {
                "id": "cu_sc_67cb...",
                "code": "malicious_instructions",
                "message": "We've detected instructions that may cause your application to perform malicious or unauthorized actions. Please acknowledge this warning if you'd like to proceed."
            }
        ],
        "status": "completed"
    }
]
```

You need to pass the safety checks back as `acknowledged_safety_checks` in the next request in order to proceed. 

```json
input=[
        {
            "type": "computer_call_output",
            "call_id": "<call_id>",
            "acknowledged_safety_checks": [
                {
                    "id": "<safety_check_id>",
                    "code": "malicious_instructions",
                    "message": "We've detected instructions that may cause your application to perform malicious or unauthorized actions. Please acknowledge this warning if you'd like to proceed."
                }
            ],
            "output": {
                "type": "computer_screenshot",
                "image_url": "<image_url>"
            }
        }
    ],
```

### Suggested safety check handling

In all cases where `pending_safety_checks` are returned, actions should be handed over to the end user to confirm proper model behavior and accuracy.

* `malicious_instructions` and `irrelevant_domain`: end users should review model actions and confirm that the model is behaving as intended.
* `sensitive_domain`: ensure an end user is actively monitoring the model actions on these sites. Exact implementation of this "watch mode" can vary by application, but a potential example could be collecting user impression data on the site to make sure there is active end user engagement with the application.
