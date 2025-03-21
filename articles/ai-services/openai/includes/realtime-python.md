---
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-openai
ms.topic: include
ms.date: 3/20/2025
---

## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>. We recommend using Python 3.10 or later, but having at least Python 3.8 is required. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- An Azure OpenAI resource created in one of the supported regions. For more information about region availability, see the [models and versions documentation](../concepts/models.md#global-standard-model-availability).
- Then, you need to deploy a `gpt-4o-mini-realtime-preview` model with your Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

## Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Deploy a model for real-time audio

[!INCLUDE [Deploy model](realtime-deploy-model.md)]

## Set up

1. Create a new folder `realtime-audio-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir realtime-audio-quickstart && cd realtime-audio-quickstart
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

1. Install the real-time audio client library for Python with:

    ```console
    pip install "https://github.com/Azure-Samples/aoai-realtime-audio-sdk/releases/download/py%2Fv0.5.3/rtclient-0.5.3.tar.gz"
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the `azure-identity` package with:

    ```console
    pip install azure-identity
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

## Text in audio out

## [Microsoft Entra ID](#tab/keyless)

1. Create the `text-in-audio-out.py` file with the following code:

    ```python
    import base64
    import asyncio
    from azure.identity.aio import DefaultAzureCredential
    from rtclient import (
        ResponseCreateMessage,
        RTLowLevelClient,
        ResponseCreateParams
    )
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"] or "https://<your-resource-name>.openai.azure.com/"
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] or "gpt-4o-mini-realtime-preview"
    
    async def text_in_audio_out():
        async with RTLowLevelClient(
            url=endpoint,
            azure_deployment=deployment,
            token_credential=DefaultAzureCredential(),
        ) as client:
            await client.send(
                ResponseCreateMessage(
                    response=ResponseCreateParams(
                        modalities={"audio", "text"}, 
                        instructions="Please assist the user."
                    )
                )
            )
            done = False
            while not done:
                message = await client.recv()
                match message.type:
                    case "response.done":
                        done = True
                    case "error":
                        done = True
                        print(message.error)
                    case "response.audio_transcript.delta":
                        print(f"Received text delta: {message.delta}")
                    case "response.audio.delta":
                        buffer = base64.b64decode(message.delta)
                        print(f"Received {len(buffer)} bytes of audio data.")
                    case _:
                        pass
    
    async def main():
        await text_in_audio_out()
    
    asyncio.run(main())
    ```

1. Run the Python file.

    ```shell
    python text-in-audio-out.py
    ```

## [API key](#tab/api-key)

1. Create the `text-in-audio-out.py` file with the following code:

    ```python
    import base64
    import asyncio
    from azure.core.credentials import AzureKeyCredential
    from rtclient import (
        ResponseCreateMessage,
        RTLowLevelClient,
        ResponseCreateParams
    )
    
    # Set environment variables or edit the corresponding values here.
    api_key = os.environ["AZURE_OPENAI_API_KEY"]    
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    deployment = "gpt-4o-mini-realtime-preview"
    
    async def text_in_audio_out():
        async with RTLowLevelClient(
            url=endpoint,
            azure_deployment=deployment,
            key_credential=AzureKeyCredential(api_key) 
        ) as client:
            await client.send(
                ResponseCreateMessage(
                    response=ResponseCreateParams(
                        modalities={"audio", "text"}, 
                        instructions="Please assist the user."
                    )
                )
            )
            done = False
            while not done:
                message = await client.recv()
                match message.type:
                    case "response.done":
                        done = True
                    case "error":
                        done = True
                        print(message.error)
                    case "response.audio_transcript.delta":
                        print(f"Received text delta: {message.delta}")
                    case "response.audio.delta":
                        buffer = base64.b64decode(message.delta)
                        print(f"Received {len(buffer)} bytes of audio data.")
                    case _:
                        pass
    
    async def main():
        await text_in_audio_out()
    
    asyncio.run(main())
    ```

1. Run the Python file.

    ```shell
    python text-in-audio-out.py
    ```

---

Wait a few moments to get the response.

## Output

The script gets a response from the model and prints the transcript and audio data received.

The output will look similar to the following:

```console
Received text delta: Hello
Received text delta: !
Received text delta:  How
Received 4800 bytes of audio data.
Received 7200 bytes of audio data.
Received text delta:  can
Received 12000 bytes of audio data.
Received text delta:  I
Received text delta:  assist
Received text delta:  you
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received text delta:  today
Received text delta: ?
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 28800 bytes of audio data.
```



