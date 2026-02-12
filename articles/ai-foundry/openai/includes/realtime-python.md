---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 3/20/2025
---

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>. We recommend using Python 3.10 or later, but having at least Python 3.8 is required. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- An Azure OpenAI resource created in one of the supported regions. For more information about region availability, see the [models and versions documentation](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).
- Then, you need to deploy a `gpt-realtime`, `gpt-realtime-mini`, or `gpt-realtime-mini-2025-12-15` model with your Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

## Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services OpenAI User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Deploy a model for real-time audio

[!INCLUDE [Deploy model](realtime-deploy-model.md)]

## Set up

1. Create a new folder `realtime-audio-quickstart-py` and go to the quickstart folder with the following command:

    ```bash
    mkdir realtime-audio-quickstart-py && cd realtime-audio-quickstart-py
    ```
    
1. Create a virtual environment. If you already have Python 3.10 or higher installed, you can create a virtual environment using the following commands:
    
    # [Windows](#tab/windows)
    
    ```shell
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

    ```shell
    pip install openai[realtime]
    ```
    
    > [!NOTE]
    > This library is maintained by OpenAI. Refer to the [release history](https://github.com/openai/openai-python/releases) to track the latest updates to the library.

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the `azure-identity` package with:

    ```shell
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
    from openai import AsyncOpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    
    async def main() -> None:
        """
        When prompted for user input, type a message and hit enter to send it to the model.
        Enter "q" to quit the conversation.
        """
    
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
        token = token_provider()
    
        # The endpoint of your Azure OpenAI resource is required. You can set it in the AZURE_OPENAI_ENDPOINT
        # environment variable.
        # You can find it in the Microsoft Foundry portal in the Overview page of your Azure OpenAI resource.
        # Example: https://{your-resource}.openai.azure.com
        endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    
        # The deployment name of the model you want to use is required. You can set it in the AZURE_OPENAI_DEPLOYMENT_NAME
        # environment variable.
        # You can find it in the Foundry portal in the "Models + endpoints" page of your Azure OpenAI resource.
        # Example: gpt-realtime
        deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
    
        base_url = endpoint.replace("https://", "wss://").rstrip("/") + "/openai/v1"
    
        # The APIs are compatible with the OpenAI client library.
        # You can use the OpenAI client library to access the Azure OpenAI APIs.
        # Make sure to set the baseURL and apiKey to use the Azure OpenAI endpoint and token.
        client = AsyncOpenAI(
            websocket_base_url=base_url,
            api_key=token
        )
        async with client.realtime.connect(
            model=deployment_name,
        ) as connection:
            # after the connection is created, configure the session.
            await connection.session.update(session={
                "type": "realtime",
                "instructions": "You are a helpful assistant. You respond by voice and text.",
                "output_modalities": ["audio"],
                "audio": {
                    "input": {
                        "transcription": {
                            "model": "whisper-1",
                        },
                        "format": {
                            "type": "audio/pcm",
                            "rate": 24000,
                        },
                        "turn_detection": {
                            "type": "server_vad",
                            "threshold": 0.5,
                            "prefix_padding_ms": 300,
                            "silence_duration_ms": 200,
                            "create_response": True,
                        }
                    },
                    "output": {
                        "voice": "alloy",
                        "format": {
                            "type": "audio/pcm",
                            "rate": 24000,
                        }
                    }
                }
            })
    
            # After the session is configured, data can be sent to the session.
            while True:
                user_input = input("Enter a message: ")
                if user_input == "q":
                    print("Stopping the conversation.")
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
                    if event.type == "response.output_text.delta":
                        print(event.delta, flush=True, end="")
                    elif event.type == "session.created":
                        print(f"Session ID: {event.session.id}")
                    elif event.type == "response.output_audio.delta":
                        audio_data = base64.b64decode(event.delta)
                        print(f"Received {len(audio_data)} bytes of audio data.")
                    elif event.type == "response.output_audio_transcript.delta":
                        print(f"Received text delta: {event.delta}")
                    elif event.type == "response.output_text.done":
                        print()
                    elif event.type == "error":
                        print("Received an error event.")
                        print(f"Error code: {event.error.code}")
                        print(f"Error Event ID: {event.error.event_id}")
                        print(f"Error message: {event.error.message}")
                    elif event.type == "response.done":
                        break
    
        print("Conversation ended.")
        credential.close()
    
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
    from openai import AsyncOpenAI
    
    async def main() -> None:
        """
        When prompted for user input, type a message and hit enter to send it to the model.
        Enter "q" to quit the conversation.
        """
    
        # The endpoint of your Azure OpenAI resource is required. You can set it in the AZURE_OPENAI_ENDPOINT
        # environment variable.
        # You can find it in the Foundry portal in the Overview page of your Azure OpenAI resource.
        # Example: https://{your-resource}.openai.azure.com
        endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        base_url = endpoint.replace("https://", "wss://").rstrip("/") + "/openai/v1"
    
        # The deployment name of the model you want to use is required. You can set it in the AZURE_OPENAI_DEPLOYMENT_NAME
        # environment variable.
        # You can find it in the Foundry portal in the "Models + endpoints" page of your Azure OpenAI resource.
        # Example: gpt-realtime
        deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
        
        # API Key of your Azure OpenAI resource is required. You can set it in the AZURE_OPENAI_API_KEY
        # environment variable.
        # You can find it in the Foundry portal in the Overview page of your Azure OpenAI resource.
        token=os.environ["AZURE_OPENAI_API_KEY"]
    
        # The APIs are compatible with the OpenAI client library.
        # You can use the OpenAI client library to access the Azure OpenAI APIs.
        # Make sure to set the baseURL and apiKey to use the Azure OpenAI endpoint and token.
        client = AsyncOpenAI(
            websocket_base_url=base_url,
            api_key=token
        )
        async with client.realtime.connect(
            model=deployment_name,
        ) as connection:
            # after the connection is created, configure the session.
            await connection.session.update(session={
                "type": "realtime",
                "instructions": "You are a helpful assistant. You respond by voice and text.",
                "output_modalities": ["audio"],
                "audio": {
                    "input": {
                        "transcription": {
                            "model": "whisper-1",
                        },
                        "format": {
                            "type": "audio/pcm",
                            "rate": 24000,
                        },
                        "turn_detection": {
                            "type": "server_vad",
                            "threshold": 0.5,
                            "prefix_padding_ms": 300,
                            "silence_duration_ms": 200,
                            "create_response": True,
                        }
                    },
                    "output": {
                        "voice": "alloy",
                        "format": {
                            "type": "audio/pcm",
                            "rate": 24000,
                        }
                    }
                }
            })
    
            # After the session is configured, data can be sent to the session.
            while True:
                user_input = input("Enter a message: ")
                if user_input == "q":
                    print("Stopping the conversation.")
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
                    if event.type == "response.output_text.delta":
                        print(event.delta, flush=True, end="")
                    elif event.type == "session.created":
                        print(f"Session ID: {event.session.id}")
                    elif event.type == "response.output_audio.delta":
                        audio_data = base64.b64decode(event.delta)
                        print(f"Received {len(audio_data)} bytes of audio data.")
                    elif event.type == "response.output_audio_transcript.delta":
                        print(f"Received text delta: {event.delta}")
                    elif event.type == "response.output_text.done":
                        print()
                    elif event.type == "error":
                        print("Received an error event.")
                        print(f"Error code: {event.error.code}")
                        print(f"Error Event ID: {event.error.event_id}")
                        print(f"Error message: {event.error.message}")
                    elif event.type == "response.done":
                        break
    
        print("Conversation ended.")
    
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
Enter a message: How are you today?
Session ID: sess_CgAuonaqdlSNNDTdqBagI
Received text delta: I'm
Received text delta:  doing
Received text delta:  well
Received text delta: ,
Received 4800 bytes of audio data.
Received 7200 bytes of audio data.
Received 12000 bytes of audio data.
Received text delta:  thank
Received text delta:  you
Received text delta:  for
Received text delta:  asking
Received text delta: !
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received text delta:  How
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received text delta:  about
Received text delta:  you
Received text delta: —
Received text delta: how
Received text delta:  are
Received text delta:  you
Received text delta:  feeling
Received text delta:  today
Received text delta: ?
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 24000 bytes of audio data.
Enter a message: q
Stopping the conversation.
Conversation ended.
```
