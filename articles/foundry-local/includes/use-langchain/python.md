---
title: Include file
description: Include file
ms.service: azure-ai-foundry
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

- **Python 3.11 or later** installed on your computer. You can download Python from the [official website](https://www.python.org/downloads/).

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

:::code language="python" source="~/foundry-local-main/samples/python/langchain-integration/src/app.py" id="complete_code":::

#### References

- Reference: [Foundry Local SDK reference](../../reference/reference-sdk-current.md)
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
