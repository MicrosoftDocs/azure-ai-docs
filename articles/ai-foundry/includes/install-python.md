---
title: include file
description: include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 12/18/2025
ms.custom: include, ignite-2024
---

First, create a new Python environment. Don't install packages into your global Python installation. Always use a virtual or conda environment when installing Python packages. Otherwise, you can break your global install of Python.

### If needed, install Python

Use Python 3.10 or later, but at least Python 3.9 is required. If you don't have a suitable version of Python installed, follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.

### Create a virtual environment

If you already have Python 3.10 or higher installed, create a virtual environment by using the following commands:

# [Windows](#tab/windows)

```bash
py -3 -m venv .venv
.venv\scripts\activate
```

# [Linux](#tab/linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

# [macOS](#tab/macos)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

When you activate the Python environment, running `python` or `pip` from the command line uses the Python interpreter in the `.venv` folder of your application.

> [!NOTE]
> Use the `deactivate` command to exit the Python virtual environment. You can reactivate it later when needed.
