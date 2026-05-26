---
title: Include file
description: Include file
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/24/2026
ms.author: natke
author: natke
ai-usage: ai-assisted
---

## Prerequisites

- [Python 3.11](https://www.python.org/downloads/) or later installed.


## Samples repository

The complete sample code for this article is available in the [Foundry Local GitHub repository](https://github.com/microsoft/Foundry-Local). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft/Foundry-Local.git
cd Foundry-Local/samples/python/embeddings
```

## Install packages

[!INCLUDE [project-setup](../python-project-setup.md)]

## Generate text embeddings

Copy and paste the following code into a Python file named `app.py`:

:::code language="python" source="~/foundry-local-main/samples/python/embeddings/src/app.py" id="complete_code":::

Run the code by using the following command:

```bash
python app.py
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'foundry_local_sdk'`**: Install the SDK by running `pip install foundry-local-sdk`.
- **`Model not found`**: Run the optional model listing snippet to find an alias available on your device, then update the alias passed to `get_model`.
- **Slow first run**: Model downloads can take time the first time you run the app.
