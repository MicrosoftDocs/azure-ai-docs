---
title: Build an app with Langchain
titleSuffix: Foundry Local
description: Learn how to build a Langchain application with Foundry local
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

# Build a Chat application with Langchain

This tutorial guides you through setting up a chat application using Foundry Local and Open Web UI. By the end, you'll have a fully functional chat interface running locally on your device.

## Prerequisites

Before beginning this tutorial, make sure you have:

- **Foundry Local** [installed](../get-started.md) on your machine.
- **At least one model loaded** using the `foundry model load` command, for example:
  ```bash
  foundry model load phi4-cpu
  ```
- Install Langchain by running following command

```bash
pip install langchain[openai]
```

## Create Langchain application

Azure Foundry Local supports the OpenAI Chat Completion API and can be seamlessly integrated with the LangChain framework. Here is an example chain:

```python
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# no key needed
if not os.environ.get("OPENAI_API_KEY"):
   os.environ["OPENAI_API_KEY"] = "no_key"

# base url pointing to Azure Founry Local
llm = ChatOpenAI(model="Phi-4-mini-cpu-int4-rtn-block-32-acc-level-4-onnx",
                   base_url="http://localhost:5272/v1/",
                   temperature=0.0, streaming=False)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that translates {input_language} to {output_language}.",
        ),
        ("human", "{input}"),
    ]
)

# simple chain
chain = prompt | llm
ai_msg = chain.invoke(
    {
        "input_language": "English",
        "output_language": "French",
        "input": "I love programming.",
    }
)

print(ai_msg)
```

That's it! You're now running Langchain with locally hosted model

## Next steps

- Try [different models](../how-to/manage.md) to compare performance and capabilities
