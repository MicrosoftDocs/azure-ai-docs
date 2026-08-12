---
title: "include file"
description: "include file"
services: machine-learning
author: s-polly
ms.service: azure-machine-learning
ms.author: scottpolly
ms.custom: "include file"
ms.topic: "include"
ms.date: 06/29/2026
ai-usage: ai-assisted
---

1. Install the Azure Machine Learning SDK (v2) for Python, the authentication library, and Jupyter:

    ```bash
    pip install azure-ai-ml azure-identity notebook
    ```

    For more information, see [Install the Azure Machine Learning SDK for Python](https://aka.ms/sdk-v2-install).

1. Create an [Azure Machine Learning workspace](../how-to-manage-workspace.md).

1. Clone the [AzureML-Examples repository](https://github.com/Azure/azureml-examples).

    ```bash
    git clone https://github.com/Azure/azureml-examples.git --depth 1
    ```

1. Start the notebook server from the directory containing your clone.

    ```bash
    jupyter notebook
    ```