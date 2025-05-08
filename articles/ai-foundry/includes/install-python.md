---
title: include file
description: include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 08/29/2024
ms.custom: include, ignite-2024
---

First you need to create a new Python environment. DO NOT install packages into your global python installation. You should always use a virtual or conda environment when installing python packages, otherwise you can break your global install of Python.

### If needed, install Python

We recommend using Python 3.10 or later, but having at least Python 3.9 is required. If you don't have a suitable version of Python installed, follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.

### Create a virtual environment

If you already have Python 3.10 or higher installed,  create a virtual environment using the following commands:

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

Activating the Python environment means that when you run ```python``` or ```pip``` from the command line, you use the Python interpreter contained in the ```.venv``` folder of your application.

> [!NOTE]
> You can use the ```deactivate``` command to exit the python virtual environment, and can later reactivate it when needed.
