---
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.topic: include
ms.date: 05/02/2025
ms.author: jburchel
reviewer: maanavdalal
ms.reviewer: maanavd
author: jonburchel
---

## Prerequisites

- Python 3.9 or later installed. You can download Python from the [official Python website](https://www.python.org/downloads/).

## Install pip packages

Install the following Python packages:

```bash
pip install openai
pip install foundry-local-sdk
```

> [!TIP]
> We recommend using a virtual environment to avoid package conflicts. You can create a virtual environment using either `venv` or `conda`.

## Use OpenAI SDK with Foundry Local

The following example demonstrates how to use the OpenAI SDK with Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration` that includes the web service configuration. The web service is an OpenAI compliant endpoint.
1. Gets a `Model` object from the model catalog using an alias. Note: Foundry Local will select the best variant for the model automatically based on the available hardware of the host machine.
1. Downloads and loads the model variant.
1. Starts the web service.
1. Uses the OpenAI SDK to call the local Foundry web service.
1. Tidies up by stopping the web service and unloading the model.

Copy-and-paste the following code into a Python file named `app.py`:

```python
import openai
from foundry_local.foundry_local_manager import FoundryLocalManager
from foundry_local.configuration import Configuration, ConfigurationKeys

def main():
    # Initialize Foundry Local Manager with configuration
    endpoint_url = "http://127.0.0.1:5464"
    config = Configuration(
        {
            ConfigurationKeys.AppName: "hello-foundry-local",
            ConfigurationKeys.WebServiceUrls: endpoint_url
        }
    )
    FoundryLocalManager.initialize(config)
    mgr = FoundryLocalManager.instance
    
    # get the model from the catalog
    model = mgr.catalog.get_model("qwen2.5-0.5b")
    
    # download and load the model
    model.download()
    model.load()
    
    # Start the web service to handle requests
    mgr.start_web_service()

    client = openai.OpenAI(
        base_url=endpoint_url + "/v1",
        api_key="notneeded"  # API key is not required for local usage
    )
    # Set the model to use and generate a response
    response = client.chat.completions.create(
        model=model.id,
        messages=[{"role": "user", "content": "What is the golden ratio?"}]
    )
    print(response.choices[0].message.content)
    
    # Tidy up - unload model and stop web service
    model.unload()
    mgr.stop_web_service()

if __name__ == "__main__":
    main()
```

Run the code using the following command:

```bash
python app.py
```

### Streaming Response

If you want to receive a streaming response, you can modify the code as follows:

```python
import openai
from foundry_local import FoundryLocalManager

# By using an alias, the most suitable model will be downloaded
# to your end-user's device.
alias = "qwen2.5-0.5b"

# Create a FoundryLocalManager instance. This will start the Foundry
# Local service if it is not already running and load the specified model.
manager = FoundryLocalManager(alias)

# The remaining code us es the OpenAI Python SDK to interact with the local model.

# Configure the client to use the local Foundry service
client = openai.OpenAI(
    base_url=manager.endpoint,
    api_key=manager.api_key  # API key is not required for local usage
)

# Set the model to use and generate a streaming response
stream = client.chat.completions.create(
    model=manager.get_model_info(alias).id,
    messages=[{"role": "user", "content": "What is the golden ratio?"}],
    stream=True
)

# Print the streaming response
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

You can run the code using the same command as before:

```bash
python app.py
```

## Use `requests` with Foundry Local

```python
# Install with: pip install requests
import requests
import json
from foundry_local import FoundryLocalManager

# By using an alias, the most suitable model will be downloaded
# to your end-user's device.
alias = "qwen2.5-0.5b"

# Create a FoundryLocalManager instance. This will start the Foundry
# Local service if it is not already running and load the specified model.
manager = FoundryLocalManager(alias)

url = manager.endpoint + "/chat/completions"

payload = {
    "model": manager.get_model_info(alias).id,
    "messages": [
        {"role": "user", "content": "What is the golden ratio?"}
    ]
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.json()["choices"][0]["message"]["content"])
```
