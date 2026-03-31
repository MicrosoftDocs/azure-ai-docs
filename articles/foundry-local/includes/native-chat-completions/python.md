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


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

```bash
cd Foundry-Local/samples/python/native-chat-completions
```

## Install packages

[!INCLUDE [project-setup](../python-project-setup.md)]

## Use native chat completions API    

Copy and paste the following code into a Python file named `app.py`:

:::code language="python" source="~/foundry-local-main/samples/python/native-chat-completions/src/app.py" id="complete_code":::

Run the code by using the following command:

```bash
python app.py
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'foundry_local_sdk'`**: Install the SDK by running `pip install foundry-local-sdk`.
- **`Model not found`**: Run the optional model listing snippet to find an alias available on your device, then update the alias passed to `get_model`.
- **Slow first run**: Model downloads can take time the first time you run the app.
