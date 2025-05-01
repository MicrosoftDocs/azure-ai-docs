---
author: eric-urban
ms.service: azure-ai-speech
ms.custom: linux-related-content
ms.topic: include
ms.date: 02/02/2024
ms.author: eur
---

The Speech SDK for Python is compatible with Windows, Linux, and macOS.

# [Windows](#tab/windows)

On Windows, you must use the 64-bit target architecture. Windows 10 or later is required.

Install the [Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017, 2019, and 2022](/cpp/windows/latest-supported-vc-redist?view=msvc-170&preserve-view=true) for your platform. Installing this package for the first time might require a restart.

> [!IMPORTANT]
> Make sure that packages of the same target architecture are installed. For example, if you install the x64 redistributable package, install the x64 Python package.

# [Linux](#tab/linux)

The Speech SDK for Python supports the following distributions on the x64 and ARM64 architectures:

- Ubuntu 20.04/22.04/24.04
- Debian 11/12
- Amazon Linux 2023
- Azure Linux 3.0

[!INCLUDE [Linux distributions](linux-distributions.md)]

# [macOS](#tab/macos)

A macOS version 10.14 or later is required.

---

Install a version of [Python from 3.8 or later](https://www.python.org/downloads/).

- To check your installation, open a terminal and run the command `python --version`. If Python installed properly, you get a response like `Python 3.8.10`.

- If you're using macOS or Linux, you might need to run the command `python3 --version` instead.

  To enable use of `python` instead of `python3`, run `alias python='python3'` to set up an alias. The Speech SDK quickstart samples specify `python` usage.
