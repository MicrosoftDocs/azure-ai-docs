---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
reviewer: patrickfarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 2/20/2026
---

In this article, you learn how to use Voice Live with [Microsoft Foundry Agent Service](/azure/ai-foundry/agents/overview) using the VoiceLive SDK for python. 

[!INCLUDE [Header](../../common/voice-live-python.md)] 

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

> [!NOTE]
> This document refers to the [Microsoft Foundry (new)](../../../../../ai-foundry/what-is-foundry.md#microsoft-foundry-portals) portal and the latest Foundry Agent Service version.

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.10 or later version</a>. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- The required language runtimes, global tools, and Visual Studio Code extensions as described in [Prepare your development environment](../../../../../ai-foundry/how-to/develop/install-cli-sdk.md).
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- A model deployed in Microsoft Foundry. If you don't have a model, first complete [Quickstart: Set up Microsoft Foundry resources](../../../../../ai-foundry/default/tutorials/quickstart-create-foundry-resources.md).
<!-- - A Microsoft Foundry agent created in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). For more information about creating an agent, see the [Create an agent quickstart](../../../../../ai-foundry/quickstarts/get-started-code.md). -->
- Assign the `Azure AI User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Prepare the environment

1. Create a new folder `voice-live-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir voice-live-quickstart && cd voice-live-quickstart
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
    > We recommend that you create and activate a new Python environment to use to install the packages you need for this tutorial. Don't install packages into your global Python installation. You should always use a virtual or conda environment when installing Python packages, otherwise you can break your global installation of Python.

1. Create a file named **requirements.txt**. Add the following packages to the file:

    ```txt
    azure-ai-projects>=2.0.0b3
    openai
    azure-ai-voicelive>=1.2.0b3
    pyaudio
    python-dotenv
    azure-identity
    ```

1. Install the packages:

    ```bash
    pip install -r requirements.txt
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

## Create an agent with Voice Live settings

1. Create a file **create_agent_with_voicelive.py** with the following code:

    ```python
    import os
    import json
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import PromptAgentDefinition
    
    load_dotenv()
    
    # Helper functions for Voice Live configuration chunking (512-char metadata limit)
    def chunk_config(config_json: str, limit: int = 512) -> dict:
        """Split config into chunked metadata entries."""
        metadata = {"microsoft.voice-live.configuration": config_json[:limit]}
        remaining = config_json[limit:]
        chunk_num = 1
        while remaining:
            metadata[f"microsoft.voice-live.configuration.{chunk_num}"] = remaining[:limit]
            remaining = remaining[limit:]
            chunk_num += 1
        return metadata
    
    def reassemble_config(metadata: dict) -> str:
        """Reassemble chunked Voice Live configuration."""
        config = metadata.get("microsoft.voice-live.configuration", "")
        chunk_num = 1
        while f"microsoft.voice-live.configuration.{chunk_num}" in metadata:
            config += metadata[f"microsoft.voice-live.configuration.{chunk_num}"]
            chunk_num += 1
        return config
    
    # Setup client
    project_client = AIProjectClient(
        endpoint=os.environ["PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )
    agent_name = os.environ["AGENT_NAME"]
    
    # Define Voice Live session settings
    voice_live_config = {
        "session": {
            "voice": {
                "name": "en-US-Ava:DragonHDLatestNeural",
                "type": "azure-standard",
                "temperature": 0.8
            },
            "input_audio_transcription": {
                "model": "azure-speech"
            },
            "turn_detection": {
                "type": "azure_semantic_vad",
                "end_of_utterance_detection": {
                    "model": "semantic_detection_v1_multilingual"
                }
            },
            "input_audio_noise_reduction": {"type": "azure_deep_noise_suppression"},
            "input_audio_echo_cancellation": {"type": "server_echo_cancellation"}
        }
    }
    
    # Create agent with Voice Live configuration in metadata
    agent = project_client.agents.create_version(
        agent_name=agent_name,
        definition=PromptAgentDefinition(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant that answers general questions",
        ),
        metadata=chunk_config(json.dumps(voice_live_config))
    )
    print(f"Agent created: {agent.name} (version {agent.version})")
    
    # Verify Voice Live configuration was stored correctly
    retrieved_agent = project_client.agents.get(agent_name=agent_name)
    stored_metadata = (retrieved_agent.versions or {}).get("latest", {}).get("metadata", {})
    stored_config = reassemble_config(stored_metadata)
    
    if stored_config:
        print("\nVoice Live configuration:")
        print(json.dumps(json.loads(stored_config), indent=2))
    else:
        print("\nVoice Live configuration not found in agent metadata.")
    ```

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the Python file.

    ```shell
    python create_agent_with_voicelive.py
    ```

## Talk with a voice agent

The sample code in this quickstart uses Microsoft Entra ID for authentication as the current integration only supports this authentication method.

1. Create the `voice-live-agents-quickstart.py` file with the following code:

    :::code language="python" source="./voice-live-with-agent-v2.py":::

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the Python file.

    ```shell
    python voice-live-agents-quickstart.py
    ```

1. You can start speaking with the agent and hear responses. You can interrupt the model by speaking. Enter "Ctrl+C" to quit the conversation.

## Output

The output of the script is printed to the console. You see messages indicating the status of the connection, audio stream, and playback. The audio is played back through your speakers or headphones.

```text
🎙️  Basic Voice Assistant with Azure VoiceLive SDK
==================================================

============================================================
🎤 VOICE ASSISTANT READY
Start speaking to begin conversation
Press Ctrl+C to exit
============================================================

🎤 Listening...
🤔 Processing...
👤 You said:  User Input:       Hello.
🎤 Ready for next input...
🤖 Agent responded with audio transcript:  Agent Audio Response:        Hello! I'm Tobi the agent. How can I assist you today?
🎤 Listening...
🤔 Processing...
👤 You said:  User Input:       What are the opening hours of the Eiffel Tower?
🎤 Ready for next input...
🤖 Agent responded with audio transcript:  Agent Audio Response:        The Eiffel Tower's opening hours can vary depending on the season and any special events or maintenance. Generally, the Eiffel Tower is open every day of the year, with the following typical hours:

- Mid-June to early September: 9:00 AM to 12:45 AM (last elevator ride up at 12:00 AM)
- Rest of the year: 9:30 AM to 11:45 PM (last elevator ride up at 11:00 PM)

These times can sometimes change, so it's always best to check the official Eiffel Tower website or contact them directly for the most up-to-date information before your visit.

Would you like me to help you find the official website or any other details about visiting the Eiffel Tower?

👋 Voice assistant shut down. Goodbye!
```

The script that you ran creates a log file named `<timestamp>_voicelive.log` in the `logs` folder.

```python
logging.basicConfig(
    filename=f'logs/{timestamp}_voicelive.log',
    filemode="w",
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    level=logging.INFO
)
```

The `voicelive.log` file contains information about the connection to the Voice Live API, including the request and response data. You can view the log file to see the details of the conversation.

```text
2026-02-10 18:40:19,183:__main__:INFO:Using Azure token credential
2026-02-10 18:40:19,184:__main__:INFO:Connecting to VoiceLive API with Foundry agent connection MyVoiceAgent for project my-voiceagent-project
2026-02-10 18:40:20,801:azure.identity.aio._internal.decorators:INFO:AzureCliCredential.get_token succeeded
2026-02-10 18:40:21,847:__main__:INFO:AudioProcessor initialized with 24kHz PCM16 mono audio
2026-02-10 18:40:21,847:__main__:INFO:Setting up voice conversation session...
2026-02-10 18:40:21,848:__main__:INFO:Session configuration sent
2026-02-10 18:40:22,174:__main__:INFO:Audio playback system ready
2026-02-10 18:40:22,174:__main__:INFO:Voice assistant ready! Start speaking...
2026-02-10 18:40:22,384:__main__:INFO:Session ready: sess_1m1zrSLJSPjJpzbEOyQpTL
2026-02-10 18:40:22,386:__main__:INFO:Sending proactive greeting request
2026-02-10 18:40:22,419:__main__:INFO:Started audio capture
2026-02-10 18:40:22,722:__main__:INFO:\U0001f916 Assistant response created
2026-02-10 18:40:26,054:__main__:INFO:\U0001f916 Assistant finished speaking
2026-02-10 18:40:26,074:__main__:INFO:\u2705 Response complete
2026-02-10 18:40:32,015:__main__:INFO:User started speaking - stopping playback
2026-02-10 18:40:32,866:__main__:INFO:\U0001f3a4 User stopped speaking
2026-02-10 18:40:32,972:__main__:INFO:\U0001f916 Assistant response created
2026-02-10 18:40:35,750:__main__:INFO:User started speaking - stopping playback
2026-02-10 18:40:35,751:__main__:INFO:\U0001f916 Assistant finished speaking
2026-02-10 18:40:36,171:__main__:INFO:\u2705 Response complete
2026-02-10 18:40:37,117:__main__:INFO:\U0001f3a4 User stopped speaking
2026-02-10 18:40:37,207:__main__:INFO:\U0001f916 Assistant response created
2026-02-10 18:40:41,016:__main__:INFO:\U0001f916 Assistant finished speaking
2026-02-10 18:40:41,023:__main__:INFO:\u2705 Response complete
2026-02-10 18:40:44,818:__main__:INFO:Stopped audio capture
2026-02-10 18:40:44,949:__main__:INFO:Stopped audio playback
2026-02-10 18:40:44,950:__main__:INFO:Audio processor cleaned up
```

Further a session log file is created in the `logs` folder with the name `<timestamp>_conversation.log`. This file contains detailed information about the session, including the request and response data.

```text
SessionID: sess_1m1zrSLJSPjJpzbEOyQpTL
Agent Name: VoiceAgentQuickstartTest
Agent Description: 
Agent ID: None
Thread ID: None
Voice Name: en-US-Ava:DragonHDLatestNeural
Voice Type: azure-standard
Voice Temperature: 0.8

User Input:	Hello.
Agent Audio Response:	Hello! I'm Tobi the agent. How can I assist you today?
User Input:	What are the opening hours of the Eiffel Tower?
Agent Audio Response:	The Eiffel Tower's opening hours can vary depending on the season and any special events or maintenance. Generally, the Eiffel Tower is open every day of the year, with the following typical hours:

- Mid-June to early September: 9:00 AM to 12:45 AM (last elevator ride up at 12:00 AM)
- Rest of the year: 9:30 AM to 11:45 PM (last elevator ride up at 11:00 PM)

These times can sometimes change, so it's always best to check the official Eiffel Tower website or contact them directly for the most up-to-date information before your visit.

Would you like me to help you find the official website or any other details about visiting the Eiffel Tower?
```

Here are the key differences between the [technical log](#technical-log) and the [conversation log](#conversation-log):

| Aspect | Conversation Log | Technical Log |
|--------|-------------|---------------|
| **Audience** | Business users, content reviewers | Developers, IT operations |
| **Content** | What was said in conversations | How the system is working |
| **Level** | Application/conversation level | System/infrastructure level |
| **Troubleshooting** | "What did the agent say?" | "Why did the connection fail?" |

**Example**: If your agent wasn't responding, you'd check:
- **voicelive.log** → "WebSocket connection failed" or "Audio stream error"
- **conversation.log** → "Did the user actually say anything?"

Both logs are complementary - conversation logs for conversation analysis and testing, technical logs for system diagnostics!

### Technical log
**Purpose**: Technical debugging and system monitoring

**Contents**:
- WebSocket connection events
- Audio stream status
- Error messages and stack traces
- System-level events (session.created, response.done, etc.)
- Network connectivity issues
- Audio processing diagnostics

**Format**: Structured logging with timestamps, log levels, and technical details

**Use Cases**:
- Debugging connection problems
- Monitoring system performance
- Troubleshooting audio issues
- Developer/operations analysis

### Conversation log
**Purpose**: Conversation transcript and user experience tracking

**Contents**:
- Agent and project identification
- Session configuration details
- **User transcripts**: "Tell me a story", "Stop"
- **Agent responses**: Full story text and follow-up responses
- Conversation flow and interactions

**Format**: Plain text, human-readable conversation format

**Use Cases**:
- Analyzing conversation quality
- Reviewing what was actually said
- Understanding user interactions and agent responses
- Business/content analysis
