---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 1/21/2025
---

[Library source code](https://github.com/openai/openai-python/tree/main/src/openai) | [Package](https://github.com/openai/openai-python) | [Samples](https://github.com/openai/openai-python/tree/main/examples)

[!INCLUDE [Audio completions introduction](audio-completions-intro.md)]

Use this guide to get started generating audio with the Azure OpenAI SDK for Python.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>. We recommend using Python 3.10 or later, but having at least Python 3.8 is required. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- An Azure OpenAI resource created in one of the supported regions. For more information about region availability, see the [models and versions documentation](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).
- Then, you need to deploy a `gpt-4o-mini-audio-preview` model with your Azure OpenAI resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

## Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `audio-completions-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir audio-completions-quickstart && cd audio-completions-quickstart
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

1. Install the OpenAI client library for Python with:

    ```console
    pip install openai
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the `azure-identity` package with:

    ```console
    pip install azure-identity
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

## Generate audio from text input

## [Microsoft Entra ID](#tab/keyless)

1. Create the `to-audio.py` file with the following code:

    ```python
    import requests
    import base64 
    import os 
    from openai import AzureOpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    
    token_provider=get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    
    # Keyless authentication
    client=AzureOpenAI(
        azure_ad_token_provider=token_provider,
        azure_endpoint=endpoint,
        api_version="2025-01-01-preview"
    )
    
    # Make the audio chat completions request
    completion=client.chat.completions.create(
        model="gpt-4o-mini-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
        messages=[
            {
                "role": "user",
                "content": "Is a golden retriever a good family dog?"
            }
        ]
    )
    
    print(completion.choices[0])
    
    # Write the output audio data to a file
    wav_bytes=base64.b64decode(completion.choices[0].message.audio.data)
    with open("dog.wav", "wb") as f:
        f.write(wav_bytes)
    ```

1. Run the Python file.

    ```shell
    python to-audio.py
    ```

## [API key](#tab/api-key)

1. Create the `to-audio.py` file with the following code:

    ```python
    import base64 
    import os 
    from openai import AzureOpenAI 
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    api_key = os.environ['AZURE_OPENAI_API_KEY']
    
    client = AzureOpenAI(
        api_version="2025-01-01-preview",  
        api_key=api_key,
        azure_endpoint=endpoint
    )
    
    # Make the audio chat completions request
    completion = client.chat.completions.create(
        model="gpt-4o-mini-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
        messages=[
            {
                "role": "user",
                "content": "Is a golden retriever a good family dog?"
            }
        ]
    )
    
    print(completion.choices[0])
    
    # Write the output audio data to a file
    wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
    with open("dog.wav", "wb") as f:
        f.write(wav_bytes)
    ```

1. Run the Python file.

    ```shell
    python to-audio.py
    ```

---

Wait a few moments to get the response.

### Output for audio generation from text input

The script generates an audio file named _dog.wav_ in the same directory as the script. The audio file contains the spoken response to the prompt, "Is a golden retriever a good family dog?"

> [!TIP]
> Play the generated _dog.wav_ file to verify the audio was generated correctly. You can use any media player or double-click the file to open it in your default audio player.

## Generate audio and text from audio input

## [Microsoft Entra ID](#tab/keyless)

1. Create the `from-audio.py` file with the following code:

    ```python
    import base64
    import os
    from openai import AzureOpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    
    token_provider=get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    
    # Keyless authentication
    client=AzureOpenAI(
        azure_ad_token_provider=token_provider,
        azure_endpoint=endpoint,
        api_version="2025-01-01-preview"
    )
    
    # Read and encode audio file  
    with open('dog.wav', 'rb') as wav_reader: 
        encoded_string = base64.b64encode(wav_reader.read()).decode('utf-8') 
     
    # Make the audio chat completions request
    completion = client.chat.completions.create( 
        model="gpt-4o-mini-audio-preview", 
        modalities=["text", "audio"], 
        audio={"voice": "alloy", "format": "wav"}, 
        messages=[ 
            { 
                "role": "user", 
                "content": [ 
                    {  
                        "type": "text", 
                        "text": "Describe in detail the spoken audio input." 
                    }, 
                    { 
                        "type": "input_audio", 
                        "input_audio": { 
                            "data": encoded_string, 
                            "format": "wav" 
                        } 
                    } 
                ] 
            }, 
        ] 
    ) 
    
    print(completion.choices[0].message.audio.transcript)
    
    # Write the output audio data to a file
    wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
    with open("analysis.wav", "wb") as f:
        f.write(wav_bytes)
    ```

1. Run the Python file.

    ```shell
    python from-audio.py
    ```

## [API key](#tab/api-key)

1. Create the `from-audio.py` file with the following code:

    ```python
    import base64
    import os
    from openai import AzureOpenAI
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    api_key = os.environ['AZURE_OPENAI_API_KEY']
    
    client = AzureOpenAI(
        api_version="2025-01-01-preview",  
        api_key=api_key, 
        azure_endpoint=endpoint,
    )
    
    # Read and encode audio file  
    with open('dog.wav', 'rb') as wav_reader: 
        encoded_string = base64.b64encode(wav_reader.read()).decode('utf-8') 
     
    # Make the audio chat completions request
    completion = client.chat.completions.create( 
        model="gpt-4o-mini-audio-preview", 
        modalities=["text", "audio"], 
        audio={"voice": "alloy", "format": "wav"}, 
        messages=[ 
            { 
                "role": "user", 
                "content": [ 
                    {  
                        "type": "text", 
                        "text": "Describe in detail the spoken audio input." 
                    }, 
                    { 
                        "type": "input_audio", 
                        "input_audio": { 
                            "data": encoded_string, 
                            "format": "wav" 
                        } 
                    } 
                ] 
            }, 
        ] 
    ) 
    
    print(completion.choices[0].message.audio.transcript)
    
    # Write the output audio data to a file
    wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
    with open("analysis.wav", "wb") as f:
        f.write(wav_bytes)
    ```

1. Run the Python file.

    ```shell
    python from-audio.py
    ```

---

Wait a few moments to get the response.

### Output for audio and text generation from audio input

The script generates a transcript of the summary of the spoken audio input. It also generates an audio file named _analysis.wav_ in the same directory as the script. The audio file contains the spoken response to the prompt.

> [!TIP]
> Play the generated _analysis.wav_ file to hear the audio description of the input.


## Generate audio and use multi-turn chat completions

## [Microsoft Entra ID](#tab/keyless)

1. Create the `multi-turn.py` file with the following code:

    ```python
    import base64 
    import os 
    from openai import AzureOpenAI 
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    
    token_provider=get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    
    # Keyless authentication
    client=AzureOpenAI(
        azure_ad_token_provider=token_provider,
        azure_endpoint=endpoint,
        api_version="2025-01-01-preview"
    )
    
    # Read and encode audio file  
    with open('dog.wav', 'rb') as wav_reader: 
        encoded_string = base64.b64encode(wav_reader.read()).decode('utf-8') 
    
    # Initialize messages with the first turn's user input 
    messages = [
        { 
            "role": "user", 
            "content": [ 
                { "type": "text", "text": "Describe in detail the spoken audio input." }, 
                { "type": "input_audio", 
                    "input_audio": { 
                        "data": encoded_string, 
                        "format": "wav" 
                    } 
                } 
            ] 
        }] 
    
    # Get the first turn's response
    
    completion = client.chat.completions.create( 
        model="gpt-4o-mini-audio-preview", 
        modalities=["text", "audio"], 
        audio={"voice": "alloy", "format": "wav"}, 
        messages=messages
    ) 
    
    print("Get the first turn's response:")
    print(completion.choices[0].message.audio.transcript) 
    
    print("Add a history message referencing the first turn's audio by ID:")
    print(completion.choices[0].message.audio.id)
    
    # Add a history message referencing the first turn's audio by ID 
    messages.append({ 
        "role": "assistant", 
        "audio": { "id": completion.choices[0].message.audio.id } 
    }) 
    
    # Add the next turn's user message 
    messages.append({ 
        "role": "user", 
        "content": "Very briefly, summarize the favorability." 
    }) 
    
    # Send the follow-up request with the accumulated messages
    completion = client.chat.completions.create( 
        model="gpt-4o-mini-audio-preview", 
        messages=messages
    ) 
    
    print("Very briefly, summarize the favorability.")
    print(completion.choices[0].message.content)
    ```

1. Run the Python file.

    ```shell
    python multi-turn.py
    ```

## [API key](#tab/api-key)

1. Create the `multi-turn.py` file with the following code:

    ```python
    import base64 
    import os 
    from openai import AzureOpenAI 
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    api_key = os.environ['AZURE_OPENAI_API_KEY']
    
    client = AzureOpenAI(
        api_version="2025-01-01-preview",  
        api_key=api_key, 
        azure_endpoint=endpoint
    )
    
    # Read and encode audio file  
    with open('dog.wav', 'rb') as wav_reader: 
        encoded_string = base64.b64encode(wav_reader.read()).decode('utf-8') 
    
    # Initialize messages with the first turn's user input 
    messages = [
        { 
            "role": "user", 
            "content": [ 
                { "type": "text", "text": "Describe in detail the spoken audio input." }, 
                { "type": "input_audio", 
                    "input_audio": { 
                        "data": encoded_string, 
                        "format": "wav" 
                    } 
                } 
            ] 
        }] 
    
    # Get the first turn's response 
    
    completion = client.chat.completions.create( 
        model="gpt-4o-mini-audio-preview", 
        modalities=["text", "audio"], 
        audio={"voice": "alloy", "format": "wav"}, 
        messages=messages
    ) 
    
    print("Get the first turn's response:")
    print(completion.choices[0].message.audio.transcript) 
    
    print("Add a history message referencing the first turn's audio by ID:")
    print(completion.choices[0].message.audio.id)
    
    # Add a history message referencing the first turn's audio by ID 
    messages.append({ 
        "role": "assistant", 
        "audio": { "id": completion.choices[0].message.audio.id } 
    }) 
    
    # Add the next turn's user message 
    messages.append({ 
        "role": "user", 
        "content": "Very briefly, summarize the favorability." 
    }) 
    
    # Send the follow-up request with the accumulated messages 
    completion = client.chat.completions.create( 
        model="gpt-4o-mini-audio-preview", 
        messages=messages
    ) 
    
    print("Very briefly, summarize the favorability.")
    print(completion.choices[0].message.content)
    ```

1. Run the Python file.

    ```shell
    python multi-turn.py
    ```

---

Wait a few moments to get the response.

### Output for multi-turn chat completions

The script generates a transcript of the summary of the spoken audio input. Then, it makes a multi-turn chat completion to briefly summarize the spoken audio input.

> [!TIP]
> Review the console output to see the transcript and verify the multi-turn conversation completed successfully. 


