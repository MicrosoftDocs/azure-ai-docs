---
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: include
ms.date: 05/02/2025
ms.author: maanavdalal
author: maanavd
---

## Prerequisites

Before starting this tutorial, you need:

- **Foundry Local** installed on your computer. Read the [Get started with Foundry Local](../../get-started.md) guide for installation instructions.
- **Python 3.10 or later** installed on your computer. You can download Python from the [official website](https://www.python.org/downloads/).

## Install Python packages

You need to install the following Python packages:

```bash
pip install langchain[openai] 
pip install foundry-local-sdk
```

> [!TIP]
> We recommend using a virtual environment to avoid package conflicts. You can create a virtual environment using either `venv` or `conda`.


## Create a translation application

In this example, you create a translation application that translates text from one language to another using a local model. The application uses the Foundry Local Manager SDK to start the inference service, download the most suitable model for your hardware, and load it into memory.

In this example, you use the `phi-3-mini-4k` model, which is a lightweight model that can run on most machines. You can choose any other model that is compatible with Foundry Local.

> [!TIP]
> You can find a list of available models by running the following command: `foundry model list`.

Create a new Python file named `translation_app.py` in your favorite IDE and add the following code:

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from foundry_local import FoundryLocalManager

# By using an alias, the most suitable model will be downloaded 
# to your end-user's device.
alias = "phi-3-mini-4k"

# Create a FoundryLocalManager instance. This will start the Foundry 
# Local service if it is not already running and load the specified model.
manager = FoundryLocalManager(alias)

# Configure ChatOpenAI to use your locally-running model
llm = ChatOpenAI(
    model=manager.get_model_info(alias).id,
    base_url=manager.endpoint,
    api_key=manager.api_key,
    temperature=0.0,
    streaming=False
)

# Create a translation prompt template
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant that translates {input_language} to {output_language}."
    ),
    ("human", "{input}")
])

# Build a simple chain by connecting the prompt to the language model
chain = prompt | llm

input = "I love to code."
print(f"Translating '{input}' to French...")

# Run the chain with your inputs
ai_msg = chain.invoke({
    "input_language": "English",
    "output_language": "French",
    "input": input
})

# print the result content
print(f"Response: {ai_msg.content}")
```

You can change the `input` variable to any text you want to translate. The application translates the text from English to French using the local model.

### Explanation of the code

**`FoundryLocalManager`** is an class that manages the Foundry Local service and the models. By default `FoundryLocalManager` will initiate the following *bootstrap process* on the application user's machine for local inference:

1. *Starts the service*, if it is not already running.
1. *Downloads the model*, if it is not cached on the user's device.
1. *Loads the specified model into memory*.

The key inputs to LangChain's `ChatOpenAI` class can be set using the `FoundryLocalManager` instance. The `model` parameter is set to the model ID of the specified model, and the `base_url` and `api_key` parameters are set to the endpoint and API key of the Foundry Local service.

```python
llm = ChatOpenAI(
    model=manager.get_model_info(alias).id,
    base_url=manager.endpoint,
    api_key=manager.api_key,
    temperature=0.0,
    streaming=False
)
```

> [!NOTE]
> One of key benefits of Foundry Local is that it will **automatically** select the most suitable model **variant** for the user's hardware. For example, if the user has a GPU, it will download the GPU version of the model. If the user has an NPU, it will download the NPU version. If the user does not have either a GPU or NPU, it will download the CPU version of the model.
    
## Run the application

To run the application, open a terminal and navigate to the directory where you saved the `translation_app.py` file. Then, run the following command:

```bash
python translation_app.py
```

You should see output similar to the following:

```Plaintext
[foundry-local] | 2025-05-10 14:08:26 | INFO     | Foundry service is already running at http://localhost:5272
[foundry-local] | 2025-05-10 14:08:28 | INFO     | Model with alias 'phi-3-mini-4k' and ID 'Phi-3-mini-4k-instruct-generic-cpu' is already cached. Use force=True to download it again.
[foundry-local] | 2025-05-10 14:08:28 | INFO     | Loading model with alias 'phi-3-mini-4k' and ID 'Phi-3-mini-4k-instruct-generic-cpu'...
Translating 'I love to code.' to French...
Response:  J'aime coder.

This translation maintains the original meaning and sentiment of the English phrase "I love to code" into French.
```