---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: include
ms.date: 01/06/2026
ms.author: jburchel
reviewer: maanavdalal
ms.reviewer: maanavd
author: jonburchel
ai-usage: ai-assisted
---

## Prerequisites

- Python 3.11 or later installed. You can download Python from the [official Python website](https://www.python.org/downloads/).

## Install pip packages

Install the following Python packages:

```bash
pip install openai foundry-local-sdk requests
```

> [!TIP]
> We recommend using a virtual environment to avoid package conflicts. You can create a virtual environment using either `venv` or `conda`.

## Use OpenAI SDK with Foundry Local

The following example demonstrates how to use the OpenAI SDK with Foundry Local. The code initializes the Foundry Local service, loads a model, and generates a response using the OpenAI SDK.

Copy-and-paste the following code into a Python file named `app.py`:

```python
import openai
from foundry_local_sdk import Configuration, FoundryLocalManager

# By using an alias, the most suitable model is downloaded
# to your end-user's device.
alias = "qwen2.5-0.5b"

# Initialize the Foundry Local SDK with web service configuration
config = Configuration(
    app_name="app-name",
    web={"urls": "http://localhost:5000"},
)
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# Get and prepare the model
model = manager.catalog.get_model(alias)
model.download(lambda progress: print(f"\rDownloading: {progress:.2f}%", end="", flush=True))
print()
model.load()

# Start the web service
manager.start_web_service()

# Configure the client to use the local Foundry service
client = openai.OpenAI(
    base_url=f"{manager.urls[0].rstrip('/')}/v1",
    api_key="local"
)

# Set the model to use and generate a response
response = client.chat.completions.create(
    model=model.id,
    messages=[{"role": "user", "content": "What is the golden ratio?"}]
)
print(response.choices[0].message.content)
```

Reference: [Foundry Local SDK reference](../../reference/reference-sdk-current.md)
Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

Run the code using the following command:

```bash
python app.py
```

You should see a text response printed in your terminal. On the first run, Foundry Local might download execution providers and the model, which can take a few minutes.

### Streaming Response

If you want to receive a streaming response, you can modify the code as follows:

```python
import openai
from foundry_local_sdk import Configuration, FoundryLocalManager

# By using an alias, the most suitable model is downloaded
# to your end-user's device.
alias = "qwen2.5-0.5b"

# Initialize the Foundry Local SDK with web service configuration
config = Configuration(
    app_name="app-name",
    web={"urls": "http://localhost:5000"},
)
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# Get and prepare the model
model = manager.catalog.get_model(alias)
model.download(lambda progress: print(f"\rDownloading: {progress:.2f}%", end="", flush=True))
print()
model.load()

# Start the web service
manager.start_web_service()

# Configure the client to use the local Foundry service
client = openai.OpenAI(
    base_url=f"{manager.urls[0].rstrip('/')}/v1",
    api_key="local"
)

# Set the model to use and generate a streaming response
stream = client.chat.completions.create(
    model=model.id,
    messages=[{"role": "user", "content": "What is the golden ratio?"}],
    stream=True
)

# Print the streaming response
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

You can run the code using the same command as before:

```bash
python app.py
```

You should see tokens stream to your terminal.

## Use `requests` with Foundry Local

```python
import requests
import json
from foundry_local_sdk import Configuration, FoundryLocalManager

# By using an alias, the most suitable model is downloaded
# to your end-user's device.
alias = "qwen2.5-0.5b"

# Initialize the Foundry Local SDK with web service configuration
config = Configuration(
    app_name="app-name",
    web={"urls": "http://localhost:5000"},
)
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# Get and prepare the model
model = manager.catalog.get_model(alias)
model.download(lambda progress: print(f"\rDownloading: {progress:.2f}%", end="", flush=True))
print()
model.load()

# Start the web service
manager.start_web_service()

url = f"{manager.urls[0].rstrip('/')}/v1/chat/completions"

payload = {
    "model": model.id,
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

Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)
