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


1. Install the OpenAI Python client library with:

    ```console
    pip install openai[realtime]
    ```
    
    > [!NOTE]
    > This library is maintained by OpenAI. Refer to the [release history](https://github.com/openai/openai-python/releases) to track the latest updates to the library.

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the `azure-identity` package with:

    ```console
    pip install azure-identity
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

> [!CAUTION]
> To use the recommended keyless authentication with the SDK, make sure that the `AZURE_OPENAI_API_KEY` environment variable isn't set. 

## Text in audio out

## [Microsoft Entra ID](#tab/keyless)

1. Create the `text-in-audio-out.py` file with the following code:

    ```python
    import os
    import base64
    import asyncio
    from openai import AsyncAzureOpenAI
    from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
    
    async def main() -> None:
        """
        When prompted for user input, type a message and hit enter to send it to the model.
        Enter "q" to quit the conversation.
        """
    
        credential = DefaultAzureCredential()
        token_provider=get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
        client = AsyncAzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            azure_ad_token_provider=token_provider,
            api_version="2025-04-01-preview",
        )
        async with client.beta.realtime.connect(
            model="gpt-4o-realtime-preview",  # name of your deployment
        ) as connection:
            await connection.session.update(session={"modalities": ["text", "audio"]})  
            while True:
                user_input = input("Enter a message: ")
                if user_input == "q":
                    break
    
                await connection.conversation.item.create(
                    item={
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": user_input}],
                    }
                )
                await connection.response.create()
                async for event in connection:
                    if event.type == "response.text.delta":
                        print(event.delta, flush=True, end="")
                    elif event.type == "response.audio.delta":
                        
                        audio_data = base64.b64decode(event.delta)
                        print(f"Received {len(audio_data)} bytes of audio data.")
                    elif event.type == "response.audio_transcript.delta":
                        print(f"Received text delta: {event.delta}")
                    elif event.type == "response.text.done":
                        print()
                    elif event.type == "response.done":
                        break
    
        await credential.close()
    
    asyncio.run(main())
    ```

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the Python file.

    ```shell
    python text-in-audio-out.py
    ```

1. When prompted for user input, type a message and hit enter to send it to the model. Enter "q" to quit the conversation.

## [API key](#tab/api-key)

1. Create the `text-in-audio-out.py` file with the following code:

    ```python
    import os
    import base64
    import asyncio
    from openai import AsyncAzureOpenAI
    from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
    
    async def main() -> None:
        """
        When prompted for user input, type a message and hit enter to send it to the model.
        Enter "q" to quit the conversation.
        """
    
        client = AsyncAzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2025-04-01-preview",
        )
        async with client.beta.realtime.connect(
            model="gpt-4o-realtime-preview",  # deployment name of your model
        ) as connection:
            await connection.session.update(session={"modalities": ["text", "audio"]})  
            while True:
                user_input = input("Enter a message: ")
                if user_input == "q":
                    break
    
                await connection.conversation.item.create(
                    item={
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": user_input}],
                    }
                )
                await connection.response.create()
                async for event in connection:
                    if event.type == "response.text.delta":
                        print(event.delta, flush=True, end="")
                    elif event.type == "response.audio.delta":
                        
                        audio_data = base64.b64decode(event.delta)
                        print(f"Received {len(audio_data)} bytes of audio data.")
                    elif event.type == "response.audio_transcript.delta":
                        print(f"Received text delta: {event.delta}")
                    elif event.type == "response.text.done":
                        print()
                    elif event.type == "response.done":
                        break
        
    asyncio.run(main())
    ```

1. Run the Python file.

    ```shell
    python text-in-audio-out.py
    ```

1. When prompted for user input, type a message and hit enter to send it to the model. Enter "q" to quit the conversation.
---

Wait a few moments to get the response.

## Output

The script gets a response from the model and prints the transcript and audio data received.

The output looks similar to the following:

```console
Enter a message: Please assist the user
Received text delta: Of
Received text delta:  course
Received text delta: !
Received text delta:  How
Received 4800 bytes of audio data.
Received 7200 bytes of audio data.
Received 12000 bytes of audio data.
Received text delta:  can
Received text delta:  I
Received text delta:  assist
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received text delta:  you
Received text delta:  today
Received text delta: ?
Received 12000 bytes of audio data.
Received 24000 bytes of audio data.
Received 36000 bytes of audio data.
Enter a message: q
```
