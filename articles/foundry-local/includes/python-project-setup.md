---
title: include file
description: include file
author: samuel100
ms.author: samkemp
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 07/17/2025
ms.custom: include file
ai-usage: ai-assisted
---

Use Foundry Local in your Python project by following these steps:

1. Create a new Python project and virtual environment:
    ```bash
    mkdir app-name
    cd app-name
    python -m venv .venv
    ```
1. Activate the virtual environment:

    ### [macOS/Linux](#tab/macos-linux)

    ```bash
    source .venv/bin/activate
    ```

    ### [Windows](#tab/windows)

    ```bash
    .venv\Scripts\activate
    ```

    ---

1. Install the Foundry Local SDK package:
    ```bash
    pip install foundry-local-sdk
    ```
