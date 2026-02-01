---
manager: nitinme
author: goergenj
ms.author: jagoerge
ms.service: azure-ai-speech
ms.topic: include
ms.date: 01/13/2026
---

[Reference documentation](/python/api/overview/azure/ai-transcription-readme) | [Package (PyPi)](https://pypi.org/project/azure-ai-transcription/) | [GitHub Samples](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-transcription_1.0.0b2/sdk/cognitiveservices/azure-ai-transcription/samples)

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.9 or later version</a>. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- A [Microsoft Foundry resource](/azure/ai-services/multi-service-resource) created in one of the supported regions. For more information about region availability, see [Region support](/azure/ai-services/speech-service/regions?tabs=stt).
- A sample `.wav` audio file to transcribe.


### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Setup

1. Create a new folder named `transcription-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir transcription-quickstart && cd transcription-quickstart
    ```

1. Create and activate a virtual Python environment to install the packages you need for this tutorial. We recommend you always use a virtual or conda environment when installing Python packages. Otherwise, you can break your global installation of Python. If you already have Python 3.9 or higher installed, create a virtual environment by using the following commands:

    # [Windows](#tab/windows)

    ```powershell
    py -3 -m venv .venv
    .venv\Scripts\Activate.ps1
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

    When you activate the Python environment, running `python` or `pip` from the command line uses the Python interpreter in the `.venv` folder of your application. Use the `deactivate` command to exit the Python virtual environment. You can reactivate it later when needed.


1. Create a file named **requirements.txt**. Add the following packages to the file:

    ```txt
    azure-ai-transcription
    azure-identity
    ```

1. Install the packages:

    ```bash
    pip install -r requirements.txt
    ```

## Retrieve resource information

You need to retrieve your resource endpoint and API key for authentication.

1. Sign in to [Foundry portal](https://ai.azure.com).
1. Select **Management center** from the left menu. Under **Connected resources**, select your Speech or multi-service resource.
1. Select **Keys and Endpoint**.
1. Copy the **Endpoint** and **Key** values. Use these values to set environment variables.

1. Set the following environment variables:

    # [Windows](#tab/windows)

    ```powershell
    $env:AZURE_SPEECH_ENDPOINT="<your-speech-endpoint>"
    $env:AZURE_SPEECH_API_KEY="<your-api-key>"
    ```

    # [Linux](#tab/linux)

    ```bash
    export AZURE_SPEECH_ENDPOINT="<your-speech-endpoint>"
    export AZURE_SPEECH_API_KEY="<your-api-key>"
    ```

    # [macOS](#tab/macos)

    ```bash
    export AZURE_SPEECH_ENDPOINT="<your-speech-endpoint>"
    export AZURE_SPEECH_API_KEY="<your-api-key>"
    ```

    ---

> [!NOTE]
> For Microsoft Entra ID authentication (recommended for production), install `azure-identity` and configure authentication as described in the [Microsoft Entra ID prerequisites](#microsoft-entra-id-prerequisites) section.

## Code

1. Create a file named `transcribe_audio_file.py` with the following code:

    ```python
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.transcription import TranscriptionClient
    from azure.ai.transcription.models import TranscriptionContent, TranscriptionOptions

    # Get configuration from environment variables
    endpoint = os.environ["AZURE_SPEECH_ENDPOINT"]
    api_key = os.environ["AZURE_SPEECH_API_KEY"]

    # Create the transcription client
    client = TranscriptionClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

    # Path to your audio file (replace with your own file path)
    audio_file_path = "<path-to-your-audio-file.wav>"

    # Open and read the audio file
    with open(audio_file_path, "rb") as audio_file:
        # Create transcription options
        options = TranscriptionOptions(locales=["en-US"])  # Specify the language

        # Create the request content
        request_content = TranscriptionContent(definition=options, audio=audio_file)

        # Transcribe the audio
        result = client.transcribe(request_content)

        # Print the transcription result
        print(f"Transcription: {result.combined_phrases[0].text}")

        # Print detailed phrase information
        if result.phrases:
            print("\nDetailed phrases:")
            for phrase in result.phrases:
                print(
                    f"  [{phrase.offset_milliseconds}ms - "
                    f"{phrase.offset_milliseconds + phrase.duration_milliseconds}ms]: "
                    f"{phrase.text}"
                )
    ```

    Reference: [TranscriptionClient](/python/api/azure-ai-transcription/azure.ai.transcription.transcriptionclient) | [TranscriptionContent](/python/api/azure-ai-transcription/azure.ai.transcription.models.transcriptioncontent) | [TranscriptionOptions](/python/api/azure-ai-transcription/azure.ai.transcription.models.transcriptionoptions) | [AzureKeyCredential](/python/api/azure-core/azure.core.credentials.azurekeycredential)

1. Replace `<path-to-your-audio-file.wav>` with the path to your audio file. The service supports WAV, MP3, FLAC, OGG, and other common audio formats.

1. Run the Python script:

    ```bash
    python transcribe_audio_file.py
    ```

## Output

The script prints the transcription result to the console:

```output
Transcription: Hi there! This is a sample voice recording created for speech synthesis testing. The quick brown fox jumps over the lazy dog. Just a fun way to include every letter of the alphabet. Numbers, like 1, 2, 3, are spoken clearly. Let's see how well this voice captures tone, timing, and natural rhythm. This audio is provided by samplefiles.com.

Detailed phrases:
  [40ms - 4880ms]: Hi there! This is a sample voice recording created for speech synthesis testing.
  [5440ms - 8400ms]: The quick brown fox jumps over the lazy dog.
  [9040ms - 12240ms]: Just a fun way to include every letter of the alphabet.
  [12720ms - 16720ms]: Numbers, like 1, 2, 3, are spoken clearly.
  [17200ms - 22000ms]: Let's see how well this voice captures tone, timing, and natural rhythm.
  [22480ms - 25920ms]: This audio is provided by samplefiles.com.
```

