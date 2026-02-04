---
author: s-polly
ms.service: azure-machine-learning
ms.topic: include
ms.date: 02/10/2025
ms.author: scottpolly
---

* An Azure Machine Learning workspace. For instructions for creating a workspace, see [Create the workspace](../quickstart-create-resources.md#create-the-workspace).

* The Azure CLI and the `ml` extension or the Azure Machine Learning Python SDK v2:

    # [Azure CLI](#tab/cli)

    To install the Azure CLI and the `ml` extension, see [Install and set up the CLI (v2)](../how-to-configure-cli.md).

    The examples in this article assume that you use a Bash shell or a compatible shell. For example, you can use a shell on a Linux system or [Windows Subsystem for Linux](/windows/wsl/about). 

    # [Python SDK](#tab/python)

    * Python 3.10 or later.

    To install the Python SDK v2, use the following command:

    ```bash
    pip install azure-ai-ml azure-identity
    ```

    To update an existing installation of the SDK to the latest version, use the following command:

    ```bash
    pip install --upgrade azure-ai-ml azure-identity
    ```

    For more information, see [Azure Machine Learning Package client library for Python](https://aka.ms/sdk-v2-install).

    ---