---
title: 'Computer Use (preview) in Azure OpenAI'
titleSuffix: Azure OpenAI
description: Learn about Computer Use in Azure OpenAI, which allows AI to interact with computer applications.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 11/26/2025
author: aahill
ms.author: aahi
---

# Computer Use (preview) in Azure OpenAI

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Use this article to learn how to work with Computer Use in Azure OpenAI. Computer Use is a specialized AI tool that uses a specialized model that can perform tasks by interacting with computer systems and applications through their UIs. With Computer Use, you can create an agent that can handle complex tasks and make decisions by interpreting visual elements and taking action based on on-screen content. 

Computer Use provides:

* **Autonomous navigation**: For example, opens applications, clicks buttons, fills out forms, and navigates multi-page workflows.
* **Dynamic adaptation**: Interprets UI changes and adjusts actions accordingly.
* **Cross-application task execution**: Operates across web-based and desktop applications.
* **Natural language interface**: Users can describe a task in plain language, and the Computer Use model determines the correct UI interactions to execute.   

## Request access

For access to the `computer-use-preview` model, registration is required and access will be granted based on Microsoft's eligibility criteria. Customers who have access to other limited access models will still need to request access for this model.

Request access: [computer-use-preview limited access model application](https://aka.ms/oai/cuaaccess)

Once access has been granted, you will need to create a deployment for the model.

## Regional support

Computer Use is available in the following regions:
* `eastus2`
* `swedencentral`
* `southindia`

## Sending an API call to the Computer Use model using the responses API

The Computer Use tool is accessed through the [responses API](./responses.md). The tool operates in a continuous loop that sends actions such as typing text or performing a click. Your code executes these actions on a computer, and sends screenshots of the outcome to the model. 

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
from openai import OpenAI

#from openai import OpenAI
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

response = client.responses.create(
    model="computer-use-preview", # set this to your model deployment name
    tools=[{
        "type": "computer_use_preview",
        "display_width": 1024,
        "display_height": 768,
        "environment": "browser" # other possible values: "mac", "windows", "ubuntu"
    }],
    input=[
        {
            "role": "user",
            "content": "Check the latest AI news on bing.com."
        }
    ],
    truncation="auto"
)

print(response.output)
```

### Output

```console
[
    ResponseComputerToolCall(
        id='cu_67d841873c1081908bfc88b90a8555e0', 
        action=ActionScreenshot(type='screenshot'), 
        call_id='call_wwEnfFDqQr1Z4Edk62Fyo7Nh', 
        pending_safety_checks=[], 
        status='completed', 
        type='computer_call'
    )
]
```

## [REST API](#tab/rest-api)

```bash
curl ${MY_ENDPOINT}/openai/v1/responses \ 
  -H "Content-Type: application/json" \ 
  -H "api-key: $MY_API_KEY" \ 
  -d '{ 
    "model": "computer-use-preview", 
    "input": [ 
      { 
        "type": "message", 
        "role": "user", 
        "content": "Check the latest AI news on bing.com." 
      }
    ],
    "tools": [{
        "type": "computer_use_preview",
        "display_width": 1024,
        "display_height": 768,
        "environment": "browser" 
    }],
    "truncation":"auto"
  }' 
```

### Output

```json
{
  "id": "resp_xxxxxxxxxxxxxxxxxxxxxxxx",
  "object": "response",
  "created_at": 1742227653,
  "status": "completed",
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "max_output_tokens": null,
  "model": "computer-use-preview",
  "output": [
    {
      "type": "computer_call",
      "id": "cu_xxxxxxxxxxxxxxxxxxxxxxxxxx",
      "call_id": "call_xxxxxxxxxxxxxxxxxxxxxxx",
      "action": {
        "type": "screenshot"
      },
      "pending_safety_checks": [],
      "status": "completed"
    }
  ],
  "parallel_tool_calls": true,
  "previous_response_id": null,
  "reasoning": {
    "effort": "medium",
    "generate_summary": null
  },
  "store": true,
  "temperature": 1.0,
  "text": {
    "format": {
      "type": "text"
    }
  },
  "tools": [
    {
      "type": "computer_use_preview",
      "display_height": 768,
      "display_width": 1024,
      "environment": "browser"
    }
  ],
  "top_p": 1.0,
  "truncation": "auto",
  "usage": {
    "input_tokens": 519,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 7,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 526
  },
  "user": null,
  "metadata": {}
}
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
        "type": "computer_use_preview",
        "display_width": 1024,
        "display_height": 768,
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
    ],
    truncation="auto"
)
```


## [REST API](#tab/rest-api)

```bash
curl ${MY_ENDPOINT}/openai/v1/responses \ 
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
    ],
    "truncation":"auto"
  }' 
```

---
## Understanding the Computer Use integration

When working with the Computer Use tool, you typically would perform the following to integrate it into your application.

1. Send a request to the model that includes a call to the computer use tool, and the display size and environment. You can also include a screenshot of the initial state of the environment in the first API request. 
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
"input":[
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

### Safety check handling

In all cases where `pending_safety_checks` are returned, actions should be handed over to the end user to confirm proper model behavior and accuracy.

* `malicious_instructions` and `irrelevant_domain`: end users should review model actions and confirm that the model is behaving as intended.
* `sensitive_domain`: ensure an end user is actively monitoring the model actions on these sites. Exact implementation of this "watch mode" can vary by application, but a potential example could be collecting user impression data on the site to make sure there is active end user engagement with the application.

## Playwright integration

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
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from playwright.async_api import async_playwright, TimeoutError

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)


# Configuration

BASE_URL = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
MODEL = "computer-use-preview" # Set to model deployment name
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
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

- [Click](/azure/ai-foundry/openai/reference-preview#click)
- [DoubleClick](/azure/ai-foundry/openai/reference-preview#doubleclick)
- [Drag](/azure/ai-foundry/openai/reference-preview#drag)
- [KeyPress](/azure/ai-foundry/openai/reference-preview#keypress)
- [Move](/azure/ai-foundry/openai/reference-preview#move)
- [Screenshot](/azure/ai-foundry/openai/reference-preview#screenshot)
- [Scroll](/azure/ai-foundry/openai/reference-preview#scroll)
- [Type](/azure/ai-foundry/openai/reference-preview#type)
- [Wait](/azure/ai-foundry/openai/reference-preview#wait)

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
- Sends the updated state back to the model and defines the [`ComputerTool`](/azure/ai-foundry/openai/reference-preview#computertool).
- Repeats this process for multiple iterations.

### Main function

The main function coordinates the entire process:

```python
    # Initialize OpenAI client
    client = OpenAI(
        base_url=BASE_URL,
        api_key=token_provider,
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

- Initializes the OpenAI client.
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
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from playwright.async_api import async_playwright, TimeoutError


token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

# Configuration

BASE_URL = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
MODEL = "computer-use-preview"
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
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
    client = OpenAI(
        base_url=BASE_URL,
        api_key=token_provider
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


## See also

* [Responses API](./responses.md)
    * [Computer Use with playwright](./responses.md#computer-use)
* [Computer Use Assistant sample on GitHub](https://github.com/Azure-Samples/computer-use-model)
