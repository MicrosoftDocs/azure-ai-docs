---
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-openai
ms.topic: include
ms.date: 5/29/2025
---

[!INCLUDE [Video generation introduction](video-generation-intro.md)]

## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>. We recommend using Python 3.10 or later, but having at least Python 3.8 is required. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- An Azure OpenAI resource created in one of the supported regions. For more information about region availability, see the [models and versions documentation](/azure/ai-services/openai/concepts/models#video-generation-models).
- Then, you need to deploy a `sora` model with your Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

## Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `video-generation-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir video-generation-quickstart && cd video-generation-quickstart
    ```
    
1. Create a virtual environment. If you already have Python 3.10 or higher installed, you can create a virtual environment using the following commands:
    
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
    
    Activating the Python environment means that when you run ```python``` or ```pip``` from the command line, you then use the Python interpreter contained in the ```.venv``` folder of your application. You can use the ```deactivate``` command to exit the python virtual environment, and can later reactivate it when needed.

    > [!TIP]
    > We recommend that you create and activate a new Python environment to use to install the packages you need for this tutorial. Don't install packages into your global python installation. You should always use a virtual or conda environment when installing python packages, otherwise you can break your global installation of Python.

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the `azure-identity` package with:

    ```console
    pip install azure-identity
    ```


## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]


## Generate video with Sora
You can generate a video with the Sora model by creating a video generation job, polling for its status, and retrieving the generated video. The following code shows how to do this via the REST API using Python.

## [Microsoft Entra ID](#tab/keyless)

1. Create the `sora-quickstart.py` file with the following code:

    ```python
    import requests
    import base64 
    import os
    from azure.identity import DefaultAzureCredential
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    
    # Keyless authentication
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    
    api_version = '2025-01-01-preview'
    url = f"{endpoint}/openai/deployments/gpt-4o-mini-audio-preview/chat/completions?api-version={api_version}"
    headers= { "Authorization": f"Bearer {token.token}", "Content-Type": "application/json" }
    ```

1. Run the Python file.

    ```shell
    python sora-quickstart.py
    ```

## [API key](#tab/api-key)

1. Create the `sora-quickstart.py` file with the following code:

    ```python
    import requests
    import base64 
    import os
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    api_key = os.environ['AZURE_OPENAI_API_KEY']
    
    api_version = '2025-01-01-preview'
    url = f"{endpoint}/openai/deployments/gpt-4o-mini-audio-preview/chat/completions?api-version={api_version}"
    headers= { "api-key": api_key, "Content-Type": "application/json" }
    ```

1. Run the Python file.

    ```shell
    python sora-quickstart.py
    ```

---

Wait a few moments to get the response.

### Output


