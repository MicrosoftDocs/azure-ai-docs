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


## Samples repository

The complete sample code for this article is available in the [Foundry Local GitHub repository](https://github.com/microsoft/Foundry-Local). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft/Foundry-Local.git
cd Foundry-Local/samples/python/web-server
```

## Install packages

[!INCLUDE [project-setup](../python-project-setup.md)]

> [!TIP]
> We recommend using a virtual environment to avoid package conflicts. You can create a virtual environment using either `venv` or `conda`.

## Use OpenAI SDK with Foundry Local

Copy-and-paste the following code into a Python file named `app.py`:

:::code language="python" source="~/foundry-local-main/samples/python/web-server/src/app.py" id="complete_code":::

Reference: [Foundry Local SDK reference](../../reference/reference-sdk-current.md)
Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

Run the code using the following command:

```bash
python app.py
```

You should see a streaming response printed in your terminal. On the first run, Foundry Local might download execution providers and the model, which can take a few minutes.
