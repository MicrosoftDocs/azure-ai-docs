---
title: How to use function calling with Azure OpenAI in Microsoft Foundry Models
titleSuffix: Azure OpenAI
description: Learn how to use function calling with OpenAI models.
author: mrbullwinkle #dereklegenzoff
ms.author: mbullwin #delegenz
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: devx-track-python
ms.topic: how-to
ms.date: 02/10/2026
manager: nitinme
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# How to use function calling with Azure OpenAI in Microsoft Foundry Models

If one or more functions are included in your request, the model determines if any of the functions should be called based on the context of the prompt. When the model determines thatodel a function should be called, it responds with a JSON object including the arguments for the function.

The models formulate API calls and structure data outputs, all based on the functions you specify. It's important to note that while the models can generate these calls, it's up to you to execute them, ensuring you remain in control.

At a high level, you can break down working with functions into three steps:

1. Call the chat completions API with your functions and the user’s input
2. Use the model’s response to call your API or function
3. Call the chat completions API again, including the response from your function to get a final response

## Prerequisites

- An Azure OpenAI model deployed 
- For Microsoft Entra ID authentication:
    - A custom subdomain configured. For more information, see [Custom subdomain names](../../../ai-services/cognitive-services-custom-subdomains.md).
    - Packages: `pip install openai azure-identity`.


## Single tool/function calling example

First demonstrate a toy function call that can check the time in three hardcoded locations with a single tool/function defined. We have added print statements to help make the code execution easier to follow:

# [Microsoft Entra ID](#tab/python-secure)

```python
import os
import json
from openai import OpenAI
from datetime import datetime
from zoneinfo import ZoneInfo
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

# Define the deployment you want to use for your chat completions API calls

deployment_name = "<YOUR_DEPLOYMENT_NAME_HERE>"

# Simplified timezone data
TIMEZONE_DATA = {
    "tokyo": "Asia/Tokyo",
    "san francisco": "America/Los_Angeles",
    "paris": "Europe/Paris"
}

def get_current_time(location):
    """Get the current time for a given location"""
    print(f"get_current_time called with location: {location}")  
    location_lower = location.lower()
    
    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            print(f"Timezone found for {key}")  
            current_time = datetime.now(ZoneInfo(timezone)).strftime("%I:%M %p")
            return json.dumps({
                "location": location,
                "current_time": current_time
            })
    
    print(f"No timezone data found for {location_lower}")  
    return json.dumps({"location": location, "current_time": "unknown"})

def run_conversation():
    # Initial user message
    messages = [{"role": "user", "content": "What's the current time in San Francisco"}] # Single function call
    #messages = [{"role": "user", "content": "What's the current time in San Francisco, Tokyo, and Paris?"}] # Parallel function call with a single tool/function defined

    # Define the function for the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                    },
                    "required": ["location"],
                },
            }
        }
    ]

    # First API call: Ask the model to use the function
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process the model's response
    response_message = response.choices[0].message
    messages.append(response_message)

    print("Model's response:")  
    print(response_message)  

    # Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "get_current_time":
                function_args = json.loads(tool_call.function.arguments)
                print(f"Function arguments: {function_args}")  
                time_response = get_current_time(
                    location=function_args.get("location")
                )
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "get_current_time",
                    "content": time_response,
                })
    else:
        print("No tool calls were made by the model.")  

    # Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
    )

    return final_response.choices[0].message.content

# Run the conversation and print the result
print(run_conversation())
```

# [API Key](#tab/python-api-key)

```python
import os
import json
from openai import OpenAI
from datetime import datetime
from zoneinfo import ZoneInfo

# Initialize the Azure OpenAI client
client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

# Define the deployment you want to use for your chat completions API calls

deployment_name = "<YOUR_DEPLOYMENT_NAME_HERE>"

# Simplified timezone data
TIMEZONE_DATA = {
    "tokyo": "Asia/Tokyo",
    "san francisco": "America/Los_Angeles",
    "paris": "Europe/Paris"
}

def get_current_time(location):
    """Get the current time for a given location"""
    print(f"get_current_time called with location: {location}")  
    location_lower = location.lower()
    
    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            print(f"Timezone found for {key}")  
            current_time = datetime.now(ZoneInfo(timezone)).strftime("%I:%M %p")
            return json.dumps({
                "location": location,
                "current_time": current_time
            })
    
    print(f"No timezone data found for {location_lower}")  
    return json.dumps({"location": location, "current_time": "unknown"})

def run_conversation():
    # Initial user message
    messages = [{"role": "user", "content": "What's the current time in San Francisco"}] # Single function call
    #messages = [{"role": "user", "content": "What's the current time in San Francisco, Tokyo, and Paris?"}] # Parallel function call with a single tool/function defined

    # Define the function for the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                    },
                    "required": ["location"],
                },
            }
        }
    ]

    # First API call: Ask the model to use the function
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process the model's response
    response_message = response.choices[0].message
    messages.append(response_message)

    print("Model's response:")  
    print(response_message)  

    # Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "get_current_time":
                function_args = json.loads(tool_call.function.arguments)
                print(f"Function arguments: {function_args}")  
                time_response = get_current_time(
                    location=function_args.get("location")
                )
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "get_current_time",
                    "content": time_response,
                })
    else:
        print("No tool calls were made by the model.")  

    # Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
    )

    return final_response.choices[0].message.content

# Run the conversation and print the result
print(run_conversation())

```

---

**Output:**

```output
Model's response:
ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_pOsKdUlqvdyttYB67MOj434b', function=Function(arguments='{"location":"San Francisco"}', name='get_current_time'), type='function')])
Function arguments: {'location': 'San Francisco'}
get_current_time called with location: San Francisco
Timezone found for san francisco
The current time in San Francisco is 09:24 AM.
```

If we're using a model deployment that supports parallel function calls we could convert this into a parallel function calling example by changing the messages array to ask for the time in multiple locations instead of one.

To accomplish this swap the comments in these two lines:

```python
    messages = [{"role": "user", "content": "What's the current time in San Francisco"}] # Single function call
    #messages = [{"role": "user", "content": "What's the current time in San Francisco, Tokyo, and Paris?"}] # Parallel function call with a single tool/function defined
```

To look like this, and run the code again:

```python
    #messages = [{"role": "user", "content": "What's the current time in San Francisco"}] # Single function call
    messages = [{"role": "user", "content": "What's the current time in San Francisco, Tokyo, and Paris?"}] # Parallel function call with a single tool/function defined
```

This generates the following output:

**Output:**

```output
Model's response:
ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_IjcAVz9JOv5BXwUx1jd076C1', function=Function(arguments='{"location": "San Francisco"}', name='get_current_time'), type='function'), ChatCompletionMessageToolCall(id='call_XIPQYTCtKIaNCCPTdvwjkaSN', function=Function(arguments='{"location": "Tokyo"}', name='get_current_time'), type='function'), ChatCompletionMessageToolCall(id='call_OHIB5aJzO8HGqanmsdzfytvp', function=Function(arguments='{"location": "Paris"}', name='get_current_time'), type='function')])
Function arguments: {'location': 'San Francisco'}
get_current_time called with location: San Francisco
Timezone found for san francisco
Function arguments: {'location': 'Tokyo'}
get_current_time called with location: Tokyo
Timezone found for tokyo
Function arguments: {'location': 'Paris'}
get_current_time called with location: Paris
Timezone found for paris
As of now, the current times are:

- **San Francisco:** 11:15 AM
- **Tokyo:** 03:15 AM (next day)
- **Paris:** 08:15 PM
```


Parallel function calls allow you to perform multiple function calls together, allowing for parallel execution and retrieval of results. This reduces the number of calls to the API that need to be made and can improve overall performance.

For example in our simple time app we retrieved multiple times at the same time. This resulted in a chat completion message with three function calls in the `tool_calls` array, each with a unique `id`. If you wanted to respond to these function calls, you would add three new messages to the conversation, each containing the result of one function call, with a `tool_call_id` referencing the `id` from `tool_calls`.


To force the model to call a specific function, set `tool_choice` to a named tool object, for example: `tool_choice={"type": "function", "function": {"name": "get_current_time"}}`. To force a user-facing message, set `tool_choice="none"`.

> [!NOTE]
> The default behavior (`tool_choice: "auto"`) is for the model to decide on its own if it should call a function and if so which function to call.

## Parallel function calling with multiple functions

Now we demonstrate another toy function calling example this time with two different tools/functions defined.

# [Microsoft Entra ID](#tab/python-secure)

```python
import os
import json
from openai import OpenAI
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

# Provide the model deployment name you want to use for this example

deployment_name = "YOUR_DEPLOYMENT_NAME_HERE" 

# Simplified weather data
WEATHER_DATA = {
    "tokyo": {"temperature": "10", "unit": "celsius"},
    "san francisco": {"temperature": "72", "unit": "fahrenheit"},
    "paris": {"temperature": "22", "unit": "celsius"}
}

# Simplified timezone data
TIMEZONE_DATA = {
    "tokyo": "Asia/Tokyo",
    "san francisco": "America/Los_Angeles",
    "paris": "Europe/Paris"
}

def get_current_weather(location, unit=None):
    """Get the current weather for a given location"""
    location_lower = location.lower()
    print(f"get_current_weather called with location: {location}, unit: {unit}")  
    
    for key in WEATHER_DATA:
        if key in location_lower:
            print(f"Weather data found for {key}")  
            weather = WEATHER_DATA[key]
            return json.dumps({
                "location": location,
                "temperature": weather["temperature"],
                "unit": unit if unit else weather["unit"]
            })
    
    print(f"No weather data found for {location_lower}")  
    return json.dumps({"location": location, "temperature": "unknown"})

def get_current_time(location):
    """Get the current time for a given location"""
    print(f"get_current_time called with location: {location}")  
    location_lower = location.lower()
    
    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            print(f"Timezone found for {key}")  
            current_time = datetime.now(ZoneInfo(timezone)).strftime("%I:%M %p")
            return json.dumps({
                "location": location,
                "current_time": current_time
            })
    
    print(f"No timezone data found for {location_lower}")  
    return json.dumps({"location": location, "current_time": "unknown"})

def run_conversation():
    # Initial user message
    messages = [{"role": "user", "content": "What's the weather and current time in San Francisco, Tokyo, and Paris?"}]

    # Define the functions for the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                    },
                    "required": ["location"],
                },
            }
        }
    ]

    # First API call: Ask the model to use the functions
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process the model's response
    response_message = response.choices[0].message
    messages.append(response_message)

    print("Model's response:")  
    print(response_message)  

    # Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            print(f"Function call: {function_name}")  
            print(f"Function arguments: {function_args}")  
            
            if function_name == "get_current_weather":
                function_response = get_current_weather(
                    location=function_args.get("location"),
                    unit=function_args.get("unit")
                )
            elif function_name == "get_current_time":
                function_response = get_current_time(
                    location=function_args.get("location")
                )
            else:
                function_response = json.dumps({"error": "Unknown function"})
            
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })
    else:
        print("No tool calls were made by the model.")  

    # Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
    )

    return final_response.choices[0].message.content

# Run the conversation and print the result
print(run_conversation())
```

# [API Key](#tab/python-api-key)

```python
import os
import json
from openai import OpenAI
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Initialize the Azure OpenAI client
client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

# Provide the model deployment name you want to use for this example

deployment_name = "YOUR_DEPLOYMENT_NAME_HERE" 

# Simplified weather data
WEATHER_DATA = {
    "tokyo": {"temperature": "10", "unit": "celsius"},
    "san francisco": {"temperature": "72", "unit": "fahrenheit"},
    "paris": {"temperature": "22", "unit": "celsius"}
}

# Simplified timezone data
TIMEZONE_DATA = {
    "tokyo": "Asia/Tokyo",
    "san francisco": "America/Los_Angeles",
    "paris": "Europe/Paris"
}

def get_current_weather(location, unit=None):
    """Get the current weather for a given location"""
    location_lower = location.lower()
    print(f"get_current_weather called with location: {location}, unit: {unit}")  
    
    for key in WEATHER_DATA:
        if key in location_lower:
            print(f"Weather data found for {key}")  
            weather = WEATHER_DATA[key]
            return json.dumps({
                "location": location,
                "temperature": weather["temperature"],
                "unit": unit if unit else weather["unit"]
            })
    
    print(f"No weather data found for {location_lower}")  
    return json.dumps({"location": location, "temperature": "unknown"})

def get_current_time(location):
    """Get the current time for a given location"""
    print(f"get_current_time called with location: {location}")  
    location_lower = location.lower()
    
    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            print(f"Timezone found for {key}")  
            current_time = datetime.now(ZoneInfo(timezone)).strftime("%I:%M %p")
            return json.dumps({
                "location": location,
                "current_time": current_time
            })
    
    print(f"No timezone data found for {location_lower}")  
    return json.dumps({"location": location, "current_time": "unknown"})

def run_conversation():
    # Initial user message
    messages = [{"role": "user", "content": "What's the weather and current time in San Francisco, Tokyo, and Paris?"}]

    # Define the functions for the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                    },
                    "required": ["location"],
                },
            }
        }
    ]

    # First API call: Ask the model to use the functions
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process the model's response
    response_message = response.choices[0].message
    messages.append(response_message)

    print("Model's response:")  
    print(response_message)  

    # Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            print(f"Function call: {function_name}")  
            print(f"Function arguments: {function_args}")  
            
            if function_name == "get_current_weather":
                function_response = get_current_weather(
                    location=function_args.get("location"),
                    unit=function_args.get("unit")
                )
            elif function_name == "get_current_time":
                function_response = get_current_time(
                    location=function_args.get("location")
                )
            else:
                function_response = json.dumps({"error": "Unknown function"})
            
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })
    else:
        print("No tool calls were made by the model.")  

    # Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
    )

    return final_response.choices[0].message.content

# Run the conversation and print the result
print(run_conversation())
```

---

**Output**

```Output
Model's response:
ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_djHAeQP0DFEVZ2qptrO0CYC4', function=Function(arguments='{"location": "San Francisco", "unit": "celsius"}', name='get_current_weather'), type='function'), ChatCompletionMessageToolCall(id='call_q2f1HPKKUUj81yUa3ITLOZFs', function=Function(arguments='{"location": "Tokyo", "unit": "celsius"}', name='get_current_weather'), type='function'), ChatCompletionMessageToolCall(id='call_6TEY5Imtr17PaB4UhWDaPxiX', function=Function(arguments='{"location": "Paris", "unit": "celsius"}', name='get_current_weather'), type='function'), ChatCompletionMessageToolCall(id='call_vpzJ3jElpKZXA9abdbVMoauu', function=Function(arguments='{"location": "San Francisco"}', name='get_current_time'), type='function'), ChatCompletionMessageToolCall(id='call_1ag0MCIsEjlwbpAqIXJbZcQj', function=Function(arguments='{"location": "Tokyo"}', name='get_current_time'), type='function'), ChatCompletionMessageToolCall(id='call_ukOu3kfYOZR8lpxGRpdkhhdD', function=Function(arguments='{"location": "Paris"}', name='get_current_time'), type='function')])
Function call: get_current_weather
Function arguments: {'location': 'San Francisco', 'unit': 'celsius'}
get_current_weather called with location: San Francisco, unit: celsius
Weather data found for san francisco
Function call: get_current_weather
Function arguments: {'location': 'Tokyo', 'unit': 'celsius'}
get_current_weather called with location: Tokyo, unit: celsius
Weather data found for tokyo
Function call: get_current_weather
Function arguments: {'location': 'Paris', 'unit': 'celsius'}
get_current_weather called with location: Paris, unit: celsius
Weather data found for paris
Function call: get_current_time
Function arguments: {'location': 'San Francisco'}
get_current_time called with location: San Francisco
Timezone found for san francisco
Function call: get_current_time
Function arguments: {'location': 'Tokyo'}
get_current_time called with location: Tokyo
Timezone found for tokyo
Function call: get_current_time
Function arguments: {'location': 'Paris'}
get_current_time called with location: Paris
Timezone found for paris
Here's the current information for the three cities:

### San Francisco
- **Time:** 09:13 AM
- **Weather:** 72°C (quite warm!)

### Tokyo
- **Time:** 01:13 AM (next day)
- **Weather:** 10°C

### Paris
- **Time:** 06:13 PM
- **Weather:** 22°C

Is there anything else you need?
```

> [!IMPORTANT]
> The JSON response might not always be valid so you need to add additional logic to your code to be able to handle errors. For some use cases you may find you need to use fine-tuning to improve [function calling performance](./fine-tuning-functions.md).

## Prompt engineering with functions

When you define a function as part of your request, the details are injected into the system message using specific syntax that the model has been trained on. This means that functions consume tokens in your prompt and that you can apply prompt engineering techniques to optimize the performance of your function calls. The model uses the full context of the prompt to determine if a function should be called including function definition, the system message, and the user messages.

#### Improving quality and reliability

If the model isn't calling your function when or how you expect, there are a few things you can try to improve the quality.

##### Provide more details in your function definition

It's important that you provide a meaningful `description` of the function and provide descriptions for any parameter that might not be obvious to the model. For example, in the description for the `location` parameter, you could include extra details and examples on the format of the location.
```json
"location": {
    "type": "string",
    "description": "The location of the hotel. The location should include the city and the state's abbreviation (i.e. Seattle, WA or Miami, FL)"
},
```

##### Provide more context in the system message

The system message can also be used to provide more context to the model. For example, if you have a function called `search_hotels` you could include a system message like the following to instruct the model to call the function when a user asks for help with finding a hotel.
```json 
{"role": "system", "content": "You're an AI assistant designed to help users search for hotels. When a user asks for help finding a hotel, you should call the search_hotels function."}
```

##### Instruct the model to ask clarifying questions

In some cases, you want to instruct the model to ask clarifying questions to prevent making assumptions about what values to use with functions. For example, with `search_hotels` you would want the model to ask for clarification if the user request didn't include details on `location`. To instruct the model to ask a clarifying question, you could include content like the next example in your system message.
```json
{"role": "system", "content": "Don't make assumptions about what values to use with functions. Ask for clarification if a user request is ambiguous."}
```

#### Reducing errors

Another area where prompt engineering can be valuable is in reducing errors in function calls. The models are trained to generate function calls matching the schema that you define, but the models produce a function call that doesn't match the schema you defined or try to call a function that you didn't include. 

If you find the model is generating function calls that weren't provided, try including a sentence in the system message that says `"Only use the functions you have been provided with."`.

## Using function calling responsibly
Like any AI system, using function calling to integrate language models with other tools and systems presents potential risks. It’s important to understand the risks that function calling could present and take measures to ensure you use the capabilities responsibly.

Here are a few tips to help you use functions safely and securely:
*	**Validate Function Calls**: Always verify the function calls generated by the model. This includes checking the parameters, the function being called, and ensuring that the call aligns with the intended action.
*	**Use Trusted Data and Tools**: Only use data from trusted and verified sources. Untrusted data in a function’s output could be used to instruct the model to write function calls in a way other than you intended.
*	**Follow the Principle of Least Privilege**: Grant only the minimum access necessary for the function to perform its job. This reduces the potential impact if a function is misused or exploited. For example, if you’re using function calls to query a database, you should only give your application read-only access to the database. You also shouldn’t depend solely on excluding capabilities in the function definition as a security control.
*	**Consider Real-World Impact**: Be aware of the real-world impact of function calls that you plan to execute, especially those that trigger actions such as executing code, updating databases, or sending notifications.
*	**Implement User Confirmation Steps**: Particularly for functions that take actions, we recommend including a step where the user confirms the action before execution.

To learn more about our recommendations on how to use Azure OpenAI models responsibly, see the [Overview of Responsible AI practices for Azure OpenAI models](/azure/ai-foundry/responsible-ai/openai/overview).

> [!IMPORTANT]
> The `functions` and `function_call` parameters have been deprecated with the release of the [`2023-12-01-preview`](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2023-12-01-preview/inference.json) version of the API. The replacement for `functions` is the [`tools`](../reference.md#chat-completions) parameter. The replacement for `function_call` is the [`tool_choice`](../reference.md#chat-completions) parameter.

## Function calling support

### Parallel function calling

* `gpt-4` (`2024-04-09`)
* `gpt-4o` (`2024-05-13`)
* `gpt-4o` (`2024-08-06`)
* `gpt-4o` (`2024-11-20`)
* `gpt-4o-mini` (`2024-07-18`)
* `gpt-4.1` (`2025-04-14`)
* `gpt-4.1-mini` (`2025-04-14`)
* `gpt-5` (`2025-08-07`)
* `gpt-5-mini` (`2025-08-07`)
* `gpt-5-nano` (`2025-08-07`)
* `gpt-5-codex` (`2025-09-11`)
* `gpt-5.1` (`2025-11-13`)
* `gpt-5.1-chat` (`2025-11-13`)
* `gpt-5.1-codex` (`2025-11-13`)
* `gpt-5.1-codex-mini` (`2025-11-13`)
* `gpt-5.1-codex-max` (`2025-12-04`)
* `gpt-5.2` (`2025-12-11`)
* `gpt-5.2-chat` (`2025-12-11`)
* `gpt-5.2-codex` (`2026-01-14`)

Support for parallel function was first added in API version [`2023-12-01-preview`](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2023-12-01-preview/inference.json)

### Basic function calling with tools

* All the models that support parallel function calling
* `gpt-5-pro` (`2025-10-06`)
* `codex-mini` (`2025-05-16`)
* `o3-pro` (`2025-06-10`)
* `o4-mini` (`2025-04-16`)
* `o3` (`2025-04-16`)
* `gpt-4.1-nano` (`2025-04-14`)
* `o3-mini` (`2025-01-31`)
* `o1` (`2024-12-17`)

> [!NOTE]
> The `tool_choice` parameter is now supported with `o3-mini` and `o1`. For more information, see the [reasoning models guide](./reasoning.md).

> [!IMPORTANT]
> Tool/function descriptions are currently limited to 1,024 characters with Azure OpenAI. We'll update this article if this limit is changed.


## Next steps

* [Learn more about Azure OpenAI](../../foundry-models/concepts/models-sold-directly-by-azure.md).
* For more examples on working with functions, check out the [Azure OpenAI Samples GitHub repository](https://aka.ms/oai/functions-samples)

