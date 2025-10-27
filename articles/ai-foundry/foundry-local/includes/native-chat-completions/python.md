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
pip install foundry-local-sdk
pip install openai
```

> [!TIP]
> We recommend using a virtual environment to avoid package conflicts. You can create a virtual environment using either `venv` or `conda`.

Foundry Local SDK supports the OpenAI input/output messaging format and therefore you can use the OpenAI Python SDK to create the chat messages.

## Use Foundry Local native chat completions API

The following example demonstrates how to use the Foundry Local native chat completions API. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration`.
1. Gets a `Model` object from the model catalog using an alias. Note: Foundry Local will select the best variant for the model automatically based on the available hardware of the host machine.
1. Downloads and loads the model variant.
1. Uses the Foundry Local native chat completions API to generate a response.
1. Tidies up by unloading the model.

Copy-and-paste the following code into a Python file named `app.py`:

```python
from foundry_local.foundry_local_manager import FoundryLocalManager
from foundry_local.configuration import Configuration, ConfigurationKeys
from openai.types.chat.chat_completion_message_param import ChatCompletionUserMessageParam
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

def main():
    
    config = Configuration(
        {
            ConfigurationKeys.AppName: "hello-foundry-local"
        }
    )
    FoundryLocalManager.initialize(config)
    mgr = FoundryLocalManager.instance
    
    model = mgr.catalog.get_model("qwen2.5-0.5b")
    model.select_variant("qwen2.5-0.5b-instruct-generic-cpu:3")
    model.download()
    model.load()
    client = model.get_chat_client()

    # Create a chat completion request
    messages = [ChatCompletionUserMessageParam(role="user", content="Why is the sky blue?")]
    
    def print_chunk(chunk: ChatCompletionChunk):
        print(chunk.choices[0].message['content'], end='', flush=True)

    client.complete_streaming_chat(
        messages,
        user_callback=print_chunk
    )
    
    model.unload()

if __name__ == "__main__":
    main()
```

Run the code using the following command:

```bash
python app.py
```
