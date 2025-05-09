---
title: Build an application with LangChain
titleSuffix: Foundry Local
description: Learn how to build a LangChain application using Foundry Local
manager: scottpolly
keywords: Azure AI services, cognitive, AI models, local inference
ms.service: azure-ai-foundry
ms.topic: tutorial
ms.date: 02/20/2025
ms.reviewer: eneros
ms.author: eneros
author: eneros
ms.custom: build-2025
#customer intent: As a developer, I want to get started with Foundry Local so that I can run AI models locally.
---

# Build an application with LangChain

This tutorial shows you how to create an application using Foundry Local and LangChain. You'll learn how to integrate locally-hosted AI models with the popular LangChain framework.

## Prerequisites

Before starting this tutorial, you need:

- **Foundry Local** [installed](../get-started.md) on your computer
- **At least one model loaded** using the `foundry model load` command:
  ```bash
  foundry model load phi4-cpu
  ```
- **LangChain with OpenAI support** installed:

  ```bash
  pip install langchain[openai]
  ```

## Create a LangChain application

Foundry Local supports the OpenAI Chat Completion API, making it easy to integrate with LangChain. Here's how to build a simple translation application:

```python
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Set a placeholder API key (not actually used by Foundry Local)
if not os.environ.get("OPENAI_API_KEY"):
   os.environ["OPENAI_API_KEY"] = "no_key"

# Configure ChatOpenAI to use your locally-running model
llm = ChatOpenAI(
    model="Phi-4-mini-cpu-int4-rtn-block-32-acc-level-4-onnx",
    base_url="http://localhost:5272/v1/",
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

# Run the chain with your inputs
ai_msg = chain.invoke({
    "input_language": "English",
    "output_language": "French",
    "input": "I love programming."
})

# Display the result
print(ai_msg)
```

That's all you need! You're now running LangChain with a model hosted on your local device.

## Next steps

- Try [different models](../how-to/manage.md) to compare performance and capabilities
