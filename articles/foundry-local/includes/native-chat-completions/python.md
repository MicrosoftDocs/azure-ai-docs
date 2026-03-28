---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 07/17/2025
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [Python 3.11](https://www.python.org/downloads/) or later installed.

## Set up project

[!INCLUDE [project-setup](../python-project-setup.md)]

## Use native chat completions API    

The following example demonstrates how to use the native chat completions API in Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration`.
1. Gets a `Model` object from the model catalog using an alias.
   
   > [!NOTE]
   > Foundry Local automatically selects the best variant for the model based on the available hardware of the host machine.

1. Downloads and loads the model variant.
1. Uses the native chat completions API to generate a streaming response.
1. Unloads the model.

Copy and paste the following code into a Python file named `app.py`:

```python
import asyncio
from foundry_local_sdk import Configuration, FoundryLocalManager


async def main():
    # Initialize the Foundry Local SDK
    config = Configuration(app_name="app-name")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # Get a model using an alias
    model = manager.catalog.get_model("qwen2.5-0.5b")

    # Download the model (skips download if already cached)
    model.download(lambda progress: print(f"\rDownloading model: {progress:.2f}%", end="", flush=True))
    print()

    # Load the model
    model.load()

    # Get a chat client
    client = model.get_chat_client()

    # Create a chat message
    messages = [
        {"role": "user", "content": "Why is the sky blue?"}
    ]

    # Stream the response
    for chunk in client.complete_streaming_chat(messages):
        content = chunk.choices[0].message.content
        if content:
            print(content, end="", flush=True)
    print()

    # Tidy up - unload the model
    model.unload()


if __name__ == "__main__":
    asyncio.run(main())
```

Run the code by using the following command:

```bash
python app.py
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'foundry_local_sdk'`**: Install the SDK by running `pip install foundry-local-sdk`.
- **`Model not found`**: Run the optional model listing snippet to find an alias available on your device, then update the alias passed to `get_model`.
- **Slow first run**: Model downloads can take time the first time you run the app.
