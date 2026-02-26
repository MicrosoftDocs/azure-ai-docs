---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 1/21/2025
---

[REST API Spec](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/stable/2024-10-21/inference.json) |

[!INCLUDE [Audio completions introduction](audio-completions-intro.md)]

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
    from azure.identity import DefaultAzureCredential
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    
    # Keyless authentication
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    
    api_version = '2025-01-01-preview'
    url = f"{endpoint}/openai/deployments/gpt-4o-mini-audio-preview/chat/completions?api-version={api_version}"
    headers= { "Authorization": f"Bearer {token.token}", "Content-Type": "application/json" }
    body = {
      "modalities": ["audio", "text"],
      "model": "gpt-4o-mini-audio-preview",
      "audio": {
          "format": "wav",
          "voice": "alloy"
      },
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Is a golden retriever a good family dog?"
            }
          ]
        }
      ]
    }
    
    # Make the audio chat completions request
    completion = requests.post(url, headers=headers, json=body)
    audio_data = completion.json()['choices'][0]['message']['audio']['data']
    
    # Write the output audio data to a file
    wav_bytes = base64.b64decode(audio_data)
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
    import requests
    import base64 
    import os 
    from openai import AzureOpenAI 
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    api_key = os.environ['AZURE_OPENAI_API_KEY']
    
    api_version = '2025-01-01-preview'
    url = f"{endpoint}/openai/deployments/gpt-4o-mini-audio-preview/chat/completions?api-version={api_version}"
    headers= { "api-key": api_key, "Content-Type": "application/json" }
    body = {
      "modalities": ["audio", "text"],
      "model": "gpt-4o-mini-audio-preview",
      "audio": {
          "format": "wav",
          "voice": "alloy"
      },
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Is a golden retriever a good family dog?"
            }
          ]
        }
      ]
    }
    
    # Make the audio chat completions request
    completion = requests.post(url, headers=headers, json=body)
    audio_data = completion.json()['choices'][0]['message']['audio']['data']
    
    # Write the output audio data to a file 
    wav_bytes = base64.b64decode(audio_data)
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

## Generate audio and text from audio input

## [Microsoft Entra ID](#tab/keyless)

1. Create the `from-audio.py` file with the following code:

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
    
    # Read and encode audio file  
    with open('dog.wav', 'rb') as wav_reader: 
      encoded_string = base64.b64encode(wav_reader.read()).decode('utf-8') 
    
    api_version = '2025-01-01-preview'
    url = f"{endpoint}/openai/deployments/gpt-4o-mini-audio-preview/chat/completions?api-version={api_version}"
    headers= { "Authorization": f"Bearer {token.token}", "Content-Type": "application/json" }
    body = {
      "modalities": ["audio", "text"],
      "model": "gpt-4o-mini-audio-preview",
      "audio": {
          "format": "wav",
          "voice": "alloy"
      },
      "messages": [
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
    }
    
    completion = requests.post(url, headers=headers, json=body)
    
    print(completion.json()['choices'][0]['message']['audio']['transcript'])
    
    # Write the output audio data to a file
    audio_data = completion.json()['choices'][0]['message']['audio']['data'] 
    wav_bytes = base64.b64decode(audio_data)
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
    import requests
    import base64
    import os
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    api_key = os.environ['AZURE_OPENAI_API_KEY']
    
    # Read and encode audio file  
    with open('dog.wav', 'rb') as wav_reader: 
      encoded_string = base64.b64encode(wav_reader.read()).decode('utf-8') 
    
    api_version = '2025-01-01-preview'
    url = f"{endpoint}/openai/deployments/gpt-4o-mini-audio-preview/chat/completions?api-version={api_version}"
    headers= { "api-key": api_key, "Content-Type": "application/json" }
    body = {
      "modalities": ["audio", "text"],
      "model": "gpt-4o-mini-audio-preview",
      "audio": {
          "format": "wav",
          "voice": "alloy"
      },
      "messages": [
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
    }
    
    completion = requests.post(url, headers=headers, json=body)
    
    print(completion.json()['choices'][0]['message']['audio']['transcript'])
    
    # Write the output audio data to a file
    audio_data = completion.json()['choices'][0]['message']['audio']['data'] 
    wav_bytes = base64.b64decode(audio_data)
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


## Generate audio and use multi-turn chat completions

## [Microsoft Entra ID](#tab/keyless)

1. Create the `multi-turn.py` file with the following code:

    ```python
    import requests
    import base64 
    import os 
    from openai import AzureOpenAI 
    from azure.identity import DefaultAzureCredential
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    
    # Keyless authentication
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    
    api_version = '2025-01-01-preview'
    url = f"{endpoint}/openai/deployments/gpt-4o-mini-audio-preview/chat/completions?api-version={api_version}"
    headers= { "Authorization": f"Bearer {token.token}", "Content-Type": "application/json" }
    
    # Read and encode audio file  
    with open('dog.wav', 'rb') as wav_reader: 
      encoded_string = base64.b64encode(wav_reader.read()).decode('utf-8') 
    
    # Initialize messages with the first turn's user input 
    messages = [
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
        }] 
    
    body = {
      "modalities": ["audio", "text"],
      "model": "gpt-4o-mini-audio-preview",
      "audio": {
          "format": "wav",
          "voice": "alloy"
      },
      "messages": messages
    }
    
    # Get the first turn's response, including generated audio 
    completion = requests.post(url, headers=headers, json=body)
    
    print("Get the first turn's response:")
    print(completion.json()['choices'][0]['message']['audio']['transcript']) 
    
    print("Add a history message referencing the first turn's audio by ID:")
    print(completion.json()['choices'][0]['message']['audio']['id'])
    
    # Add a history message referencing the first turn's audio by ID 
    messages.append({ 
        "role": "assistant", 
        "audio": { "id": completion.json()['choices'][0]['message']['audio']['id'] } 
    }) 
    
    # Add the next turn's user message 
    messages.append({ 
        "role": "user", 
        "content": "Very briefly, summarize the favorability." 
    }) 
    
    body = {
      "model": "gpt-4o-mini-audio-preview",
      "messages": messages
    }
    
    # Send the follow-up request with the accumulated messages
    completion = requests.post(url, headers=headers, json=body) 
    
    print("Very briefly, summarize the favorability.")
    print(completion.json()['choices'][0]['message']['content'])
    ```

1. Run the Python file.

    ```shell
    python multi-turn.py
    ```

## [API key](#tab/api-key)

1. Create the `multi-turn.py` file with the following code:

    ```python
    import requests
    import base64 
    import os 
    from openai import AzureOpenAI 
    
    # Set environment variables or edit the corresponding values here.
    endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    api_key = os.environ['AZURE_OPENAI_API_KEY']
    
    api_version = '2025-01-01-preview'
    url = f"{endpoint}/openai/deployments/gpt-4o-mini-audio-preview/chat/completions?api-version={api_version}"
    headers= { "api-key": api_key, "Content-Type": "application/json" }
    
    # Read and encode audio file  
    with open('dog.wav', 'rb') as wav_reader: 
      encoded_string = base64.b64encode(wav_reader.read()).decode('utf-8') 
    
    # Initialize messages with the first turn's user input 
    messages = [
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
        }] 
    
    body = {
      "modalities": ["audio", "text"],
      "model": "gpt-4o-mini-audio-preview",
      "audio": {
          "format": "wav",
          "voice": "alloy"
      },
      "messages": messages
    }
    
    
    # Get the first turn's response, including generated audio 
    completion = requests.post(url, headers=headers, json=body)
    
    print("Get the first turn's response:")
    print(completion.json()['choices'][0]['message']['audio']['transcript']) 
    
    print("Add a history message referencing the first turn's audio by ID:")
    print(completion.json()['choices'][0]['message']['audio']['id'])
    
    # Add a history message referencing the first turn's audio by ID 
    messages.append({ 
        "role": "assistant", 
        "audio": { "id": completion.json()['choices'][0]['message']['audio']['id'] } 
    }) 
    
    # Add the next turn's user message 
    messages.append({ 
        "role": "user", 
        "content": "Very briefly, summarize the favorability." 
    }) 
    
    body = {
      "model": "gpt-4o-mini-audio-preview",
      "messages": messages
    }
    
    # Send the follow-up request with the accumulated messages
    completion = requests.post(url, headers=headers, json=body) 
    
    print("Very briefly, summarize the favorability.")
    print(completion.json()['choices'][0]['message']['content'])
    ```

1. Run the Python file.

    ```shell
    python multi-turn.py
    ```

---

Wait a few moments to get the response.

### Output for multi-turn chat completions

The script generates a transcript of the summary of the spoken audio input. Then, it makes a multi-turn chat completion to briefly summarize the spoken audio input. 
