---
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.topic: include
ms.date: 05/02/2025
ms.author: jburchel
ms.reviewer: maanavd
reviewer: maanavdalal
author: jonburchel
ai-usage: ai-assisted
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

Create a new Python file named `translation_app.py` in your favorite IDE and add the following code:

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from foundry_local import FoundryLocalManager

# By using an alias, the most suitable model will be downloaded
# to your end-user's device.
# TIP: You can find a list of available models by running the
# following command: `foundry model list`.
alias = "qwen2.5-0.5b"

# Create a FoundryLocalManager instance. This will start the Foundry
# Local service if it is not already running and load the specified model.
manager = FoundryLocalManager(alias)

# Configure ChatOpenAI to use your locally-running model
llm = ChatOpenAI(
    model=manager.get_model_info(alias).id,
    base_url=manager.endpoint,
    api_key=manager.api_key,
    temperature=0.6,
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

#### References

- Reference: [Foundry Local SDK reference](../../reference/reference-sdk.md)
- Reference: [Get started with Foundry Local](../../get-started.md)

> [!NOTE]
> One of key benefits of Foundry Local is that it **automatically** selects the most suitable model **variant** for the user's hardware. For example, if the user has a GPU, it downloads the GPU version of the model. If the user has an NPU (Neural Processing Unit), it downloads the NPU version. If the user doesn't have either a GPU or NPU, it downloads the CPU version of the model.

## Run the application

To run the application, open a terminal and navigate to the directory where you saved the `translation_app.py` file. Then, run the following command:

```bash
python translation_app.py
```

You're done when you see a `Response:` line with the translated text.

You should see output similar to:

```text
Translating 'I love to code.' to French...
Response: <translated text>
```
