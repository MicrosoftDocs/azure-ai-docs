---
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-openai
ms.topic: include
ms.date: 7/31/2025
---

In this article, you learn how to use voice live with agents and Azure AI Speech using Python code. 

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>. We recommend using Python 3.10 or later, but having at least Python 3.8 is required. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- An [Azure AI Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live API overview documentation](../../../voice-live.md).

> [!TIP]
> To use voice live, you don't need to deploy an audio model with your Azure AI Foundry resource. Voice live is fully managed, and the model is automatically deployed for you. For more information about models availability, see the [voice live overview documentation](../../../voice-live.md).

## Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

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
    > We recommend that you create and activate a new Python environment to use to install the packages you need for this tutorial. Don't install packages into your global python installation. You should always use a virtual or conda environment when installing python packages, otherwise you can break your global installation of Python.

1. Create a file named **requirements.txt**. Add the following packages to the file:

    ```txt
    aiohttp==3.11.18
    azure-core==1.34.0
    azure-identity==1.22.0
    certifi==2025.4.26
    cffi==1.17.1
    cryptography==44.0.3
    numpy==2.2.5
    pycparser==2.22
    python-dotenv==1.1.0
    requests==2.32.3
    sounddevice==0.5.1
    typing_extensions==4.13.2
    urllib3==2.4.0
    websockets==15.0.1
    ```

1. Install the packages:

    ```bash
    pip install -r requirements.txt
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the `azure-identity` package with:

    ```console
    pip install azure-identity
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]


## Start a conversation

1. Create the `voice-live-agents-quickstart.py` file with the following code:

    ```python
    from __future__ import annotations

    import os
    import uuid
    import json
    import asyncio
    import base64
    import logging
    import threading
    import numpy as np
    import sounddevice as sd
    from datetime import datetime
    
    from collections import deque
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential
    from azure.core.credentials_async import AsyncTokenCredential
    from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
    from typing import Dict, Union, Literal, Set
    from typing_extensions import AsyncIterator, TypedDict, Required
    from websockets.asyncio.client import connect as ws_connect
    from websockets.asyncio.client import ClientConnection as AsyncWebsocket
    from websockets.asyncio.client import HeadersLike
    from websockets.typing import Data
    from websockets.exceptions import WebSocketException
    
    # This is the main function to run the Voice Live API client.
    
    async def main() -> None:
        # Set environment variables or edit the corresponding values here.
        endpoint = os.environ.get("AZURE_VOICE_LIVE_ENDPOINT") or "https://contoso-proj-agentic-foundry-res.cognitiveservices.azure.com/"
        api_version = os.environ.get("AZURE_VOICE_LIVE_API_VERSION") or "2025-05-01-preview"
        api_key = os.environ.get("AZURE_VOICE_LIVE_API_KEY") or "your_api_key"
        
        # Agent-specific configuration for Azure AI Foundry projects
        agent_id = os.environ.get("AI_FOUNDRY_AGENT_ID") or "your-agent-id"
        project_name = os.environ.get("AI_FOUNDRY_PROJECT_NAME") or "your-project-name"
    
        # For the recommended keyless authentication, get and
        # use the Microsoft Entra token instead of api_key:
        scopes = "https://ai.azure.com/.default"
        credential = DefaultAzureCredential()
        token = await credential.get_token(scopes)
    
        client = AsyncAzureVoiceLive(
            azure_endpoint = endpoint,
            api_version = api_version,
            token = token.token,
            #api_key = api_key,
        )
    
        print(f"Using agent: {agent_id}")
        print(f"Project name: {project_name}")
        
        # Log agent usage to conversation log
        await write_conversation_log(f'Using agent: {agent_id}')
        await write_conversation_log(f'Project name: {project_name}')
        
        async with client.connect_agent(
            project_name=project_name, 
            agent_id=agent_id, 
            agent_access_token=token.token, 
            debug=True
        ) as connection:
            session_update = {
                "type": "session.update",
                "session": {
                    "turn_detection": {
                        "type": "azure_semantic_vad",
                        "threshold": 0.3,
                        "prefix_padding_ms": 200,
                        "silence_duration_ms": 200,
                        "remove_filler_words": True,
                        "end_of_utterance_detection": {
                            "model": "semantic_detection_v1",
                            "threshold": 0.1,
                            "timeout": 4,
                        },
                    },
                    "input_audio_noise_reduction": {
                        "type": "azure_deep_noise_suppression"
                    },
                    "input_audio_echo_cancellation": {
                        "type": "server_echo_cancellation"
                    },
                    "voice": {
                        "name": "en-US-Aria:DragonHDLatestNeural",
                        "type": "azure-standard",
                        "temperature": 0.8,
                    },
                    "output_audio_timestamp_types": ["word"], 
                    "modalities": ["text", "audio"],
                },
                "event_id": ""
            }
            await connection.send(json.dumps(session_update))
            print("Session created: ", json.dumps(session_update))
            
            # Log session configuration
            await write_conversation_log(f'Session Config: {json.dumps(session_update)}')
    
            send_task = asyncio.create_task(listen_and_send_audio(connection))
            receive_task = asyncio.create_task(receive_audio_and_playback(connection))
            keyboard_task = asyncio.create_task(read_keyboard_and_quit())
    
            print("Starting the chat ...")
            await asyncio.wait([send_task, receive_task, keyboard_task], return_when=asyncio.FIRST_COMPLETED)
    
            send_task.cancel()
            receive_task.cancel()
            print("Chat done.")
    
    # --- End of Main Function ---
    
    logger = logging.getLogger(__name__)
    AUDIO_SAMPLE_RATE = 24000
    
    class AsyncVoiceLiveConnection:
        _connection: AsyncWebsocket
    
        def __init__(self, url: str, additional_headers: HeadersLike) -> None:
            self._url = url
            self._additional_headers = additional_headers
            self._connection = None
    
        async def __aenter__(self) -> AsyncVoiceLiveConnection:
            try:
                self._connection = await ws_connect(self._url, additional_headers=self._additional_headers)
            except WebSocketException as e:
                raise ValueError(f"Failed to establish a WebSocket connection: {e}")
            return self
    
        async def __aexit__(self, exc_type, exc_value, traceback) -> None:
            if self._connection:
                await self._connection.close()
                self._connection = None
    
        enter = __aenter__
        close = __aexit__
    
        async def __aiter__(self) -> AsyncIterator[Data]:
             async for data in self._connection:
                 yield data
    
        async def recv(self) -> Data:
            return await self._connection.recv()
    
        async def recv_bytes(self) -> bytes:
            return await self._connection.recv()
    
        async def send(self, message: Data) -> None:
            await self._connection.send(message)
    
    class AsyncAzureVoiceLive:
        def __init__(
            self,
            *,
            azure_endpoint: str | None = None,
            api_version: str | None = None,
            token: str | None = None,
            api_key: str | None = None,
        ) -> None:
    
            self._azure_endpoint = azure_endpoint
            self._api_version = api_version
            self._token = token
            self._api_key = api_key
            self._connection = None
    
        def connect(self, model: str) -> AsyncVoiceLiveConnection:
            if self._connection is not None:
                raise ValueError("Already connected to the Voice Live API.")
            if not model:
                raise ValueError("Model name is required.")
    
            url = f"{self._azure_endpoint.rstrip('/')}/voice-live/realtime?api-version={self._api_version}&model={model}"
            url = url.replace("https://", "wss://")
    
            auth_header = {"Authorization": f"Bearer {self._token}"} if self._token else {"api-key": self._api_key}
            request_id = uuid.uuid4()
            headers = {"x-ms-client-request-id": str(request_id), **auth_header}
    
            self._connection = AsyncVoiceLiveConnection(
                url,
                additional_headers=headers,
            )
            return self._connection
    
        def connect_agent(self, project_name: str, agent_id: str, agent_access_token: str, debug: bool = False) -> AsyncVoiceLiveConnection:
            if self._connection is not None:
                raise ValueError("Already connected to the Voice Live API.")
            if not project_name:
                raise ValueError("Project name is required.")
            if not agent_id:
                raise ValueError("Agent ID is required.")
            if not agent_access_token:
                raise ValueError("Agent access token is required.")
    
            azure_ws_endpoint = self._azure_endpoint.rstrip('/').replace("https://", "wss://")
            debug_uri = "&debug=on" if debug else ""
            
            url = f"{azure_ws_endpoint}/voice-live/realtime?api-version={self._api_version}&agent-project-name={project_name}&agent-id={agent_id}&agent-access-token={agent_access_token}{debug_uri}"
    
            auth_header = {"Authorization": f"Bearer {self._token}"} if self._token else {"api-key": self._api_key}
            request_id = uuid.uuid4()
            headers = {"x-ms-client-request-id": str(request_id), **auth_header}
    
            self._connection = AsyncVoiceLiveConnection(
                url,
                additional_headers=headers,
            )
            return self._connection
    
    class AudioPlayerAsync:
        def __init__(self):
            self.queue = deque()
            self.lock = threading.Lock()
            self.stream = sd.OutputStream(
                callback=self.callback,
                samplerate=AUDIO_SAMPLE_RATE,
                channels=1,
                dtype=np.int16,
                blocksize=2400,
            )
            self.playing = False
    
        def callback(self, outdata, frames, time, status):
            if status:
                logger.warning(f"Stream status: {status}")
            with self.lock:
                data = np.empty(0, dtype=np.int16)
                while len(data) < frames and len(self.queue) > 0:
                    item = self.queue.popleft()
                    frames_needed = frames - len(data)
                    data = np.concatenate((data, item[:frames_needed]))
                    if len(item) > frames_needed:
                        self.queue.appendleft(item[frames_needed:])
                if len(data) < frames:
                    data = np.concatenate((data, np.zeros(frames - len(data), dtype=np.int16)))
            outdata[:] = data.reshape(-1, 1)
    
        def add_data(self, data: bytes):
            with self.lock:
                np_data = np.frombuffer(data, dtype=np.int16)
                self.queue.append(np_data)
                if not self.playing and len(self.queue) > 10:
                    self.start()
    
        def start(self):
            if not self.playing:
                self.playing = True
                self.stream.start()
    
        def stop(self):
            with self.lock:
                self.queue.clear()
            self.playing = False
            self.stream.stop()
    
        def terminate(self):
            with self.lock:
                self.queue.clear()
            self.stream.stop()
            self.stream.close()
    
    async def listen_and_send_audio(connection: AsyncVoiceLiveConnection) -> None:
        logger.info("Starting audio stream ...")
    
        stream = sd.InputStream(channels=1, samplerate=AUDIO_SAMPLE_RATE, dtype="int16")
        try:
            stream.start()
            read_size = int(AUDIO_SAMPLE_RATE * 0.02)
            while True:
                if stream.read_available >= read_size:
                    data, _ = stream.read(read_size)
                    audio = base64.b64encode(data).decode("utf-8")
                    param = {"type": "input_audio_buffer.append", "audio": audio, "event_id": ""}
                    data_json = json.dumps(param)
                    await connection.send(data_json)
        except Exception as e:
            logger.error(f"Audio stream interrupted. {e}")
        finally:
            stream.stop()
            stream.close()
            logger.info("Audio stream closed.")
    
    async def receive_audio_and_playback(connection: AsyncVoiceLiveConnection) -> None:
        last_audio_item_id = None
        audio_player = AudioPlayerAsync()
    
        logger.info("Starting audio playback ...")
        try:
            while True:
                async for raw_event in connection:
                    event = json.loads(raw_event)
                    print(f"Received event:", {event.get("type")})
    
                    if event.get("type") == "session.created":
                        session = event.get("session")
                        logger.info(f"Session created: {session.get('id')}")
                        await write_conversation_log(f'SessionID: {session.get("id")}')
    
                    elif event.get("type") == "session.updated":
                        session = event.get("session")
                        print(f"Session updated: {session.get('id')}")
                        logger.info(f"Session updated: {session.get('id')}")
    
                    elif event.get("type") == "input_audio_buffer.speech_started":
                        print("User started speaking")
                        audio_player.stop()  # Clear buffered audio when user starts speaking
    
                    elif event.get("type") == "conversation.item.input_audio_transcription.completed":
                        user_transcript = f'User Input: {event.get("transcript", "")}'
                        print(f'\n\t{user_transcript}\n')
                        await write_conversation_log(user_transcript)
    
                    elif event.get("type") == "response.audio.delta":
                        if event.get("item_id") != last_audio_item_id:
                            last_audio_item_id = event.get("item_id")
    
                        bytes_data = base64.b64decode(event.get("delta", ""))
                        audio_player.add_data(bytes_data)
    
                    elif event.get("type") == "response.text.done":
                        agent_text_response = f'Agent Text Response: {event.get("text", "")}'
                        print(f'\n\t{agent_text_response}\n')
                        await write_conversation_log(agent_text_response)
    
                    elif event.get("type") == "response.audio_transcript.done":
                        agent_audio_response = f'Agent Audio Response: {event.get("transcript", "")}'
                        print(f'\n\t{agent_audio_response}\n')
                        await write_conversation_log(agent_audio_response)
    
                    elif event.get("type") == "response.done":
                        logger.info("Response done.")
    
                    elif event.get("type") == "error":
                        error_details = event.get("error", {})
                        error_type = error_details.get("type", "Unknown")
                        error_code = error_details.get("code", "Unknown")
                        error_message = error_details.get("message", "No message provided")
                        raise ValueError(f"Error received: Type={error_type}, Code={error_code}, Message={error_message}")
    
        except Exception as e:
            logger.error(f"Error in audio playback: {e}")
        finally:
            audio_player.terminate()
            logger.info("Playback done.")
    
    async def read_keyboard_and_quit() -> None:
        print("Press 'q' and Enter to quit the chat.")
        while True:
            # Run input() in a thread to avoid blocking the event loop
            user_input = await asyncio.to_thread(input)
            if user_input.strip().lower() == 'q':
                print("Quitting the chat...")
                break
    
    # Global variable for log filename (will be set in main)
    logfilename = ""
    
    async def write_conversation_log(message: str) -> None:
        """Write a message to the conversation log."""
        try:
            with open(f'logs/{logfilename}', 'a', encoding='utf-8') as conversation_log:
                conversation_log.write(message + "\n")
        except Exception as e:
            logger.error(f"Failed to write to conversation log: {e}")
    
    if __name__ == "__main__":
        try:
            # Set up conversation/session logging
            if not os.path.exists('logs'):
                os.makedirs('logs')
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            logfilename = f'session_{timestamp}.log'
            with open(f'logs/{logfilename}', 'w', encoding='utf-8') as conversation_log:
                conversation_log.write("Agent Session Log:\n")
            
            # Set up technical logging
            logging.basicConfig(
                filename='logs/voicelive.log',
                filemode="w",
                level=logging.DEBUG,
                format='%(asctime)s:%(name)s:%(levelname)s:%(message)s'
            )
            load_dotenv()
            asyncio.run(main())
        except Exception as e:
            print(f"Error: {e}")
    ```

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the Python file.

    ```shell
    python voice-live-agents-quickstart.py
    ```

1. You can start speaking with the agent and hear responses. You can interrupt the model by speaking. Enter "q" to quit the conversation.

## Output

The output of the script is printed to the console. You see messages indicating the status of the connection, audio stream, and playback. The audio is played back through your speakers or headphones.

```text
Using agent: asst_NEQPZ5grNgCqCowPM0HJdXvH
Project name: contoso-proj-agentic
Session created:  {"type": "session.update", "session": {"turn_detection": {"type": "azure_semantic_vad", "threshold": 0.3, "prefix_padding_ms": 200, "silence_duration_ms": 200, "remove_filler_words": true, "end_of_utterance_detection": {"model": "semantic_detection_v1", "threshold": 0.1, "timeout": 4}}, "input_audio_noise_reduction": {"type": "azure_deep_noise_suppression"}, "input_audio_echo_cancellation": {"type": "server_echo_cancellation"}, "voice": {"name": "en-US-Aria:DragonHDLatestNeural", "type": "azure-standard", "temperature": 0.8}, "output_audio_timestamp_types": ["word"], "modalities": ["text", "audio"]}, "event_id": ""}
Starting the chat ...
Received event: {'session.created'}
Press 'q' and Enter to quit the chat.
Received event: {'session.updated'}
Session updated: sess_nLYa2BlHblzWObD8hn90T
Received event: {'input_audio_buffer.speech_started'}
User started speaking
Received event: {'input_audio_buffer.speech_stopped'}
Received event: {'input_audio_buffer.committed'}
Received event: {'conversation.item.input_audio_transcription.completed'}

        User Input: Tell me a story.

Received event: {'conversation.item.created'}
Received event: {'response.created'}
Received event: {'response.output_item.added'}
Received event: {'conversation.item.created'}
Received event: {'response.content_part.added'}
Received event: {'response.audio_transcript.delta'}
Received event: {'response.audio_transcript.delta'}

REDACTED FOR BREVITY

Received event: {'response.audio.delta'}
Received event: {'response.audio.delta'}
Received event: {'response.audio_transcript.delta'}
Received event: {'response.audio_transcript.delta'}

REDACTED FOR BREVITY

Received event: {'response.audio.delta'}
Received event: {'response.audio.delta'}
Received event: {'response.audio.done'}
Received event: {'response.audio_timestamp.done'}
Received event: {'response.audio_transcript.done'}

        Agent Audio Response: Sure! Here's a short story for you:

Once upon a time in a small village nestled between towering mountains, there lived a curious little girl named Elara. Elara loved exploring the forests and streams around her home, always eager to discover new wonders. One day, while wandering deeper into the woods than ever before, she stumbled upon a hidden glade where the sunlight danced through the leaves in dazzling patterns.

In the center of the glade stood an ancient tree with bark that shimmered like silver. As Elara approached, she noticed a tiny door carved into the trunk. With a mix of excitement and courage, she gently knocked. To her surprise, the door creaked open, revealing a cozy little room filled with glowing flowers and twinkling lights.

Inside, Elara met a wise old fairy who told her that the tree was the heart of the forest, protecting its magic and harmony. The fairy entrusted Elara with a special seed, saying it held the power to heal and grow new life wherever it was planted.     

Elara promised to care for the seed and share its magic with the world. From that day on, she became the forest's guardian, weaving magic and kindness wherever she went. And thus, the village flourished, wrapped in the gentle embrace of nature's wonder, all thanks to the brave little girl who dared to peek behind the silver bark.

The end.

Would you like to hear another story or about something specific?

Received event: {'response.content_part.done'}
Received event: {'response.output_item.done'}
Received event: {'response.done'}
Received event: {'input_audio_buffer.speech_started'}
User started speaking
Received event: {'input_audio_buffer.speech_stopped'}
Received event: {'input_audio_buffer.committed'}
Received event: {'conversation.item.input_audio_transcription.completed'}

        User Input: Stop.

Received event: {'conversation.item.created'}
Received event: {'response.created'}
Received event: {'response.output_item.added'}
Received event: {'conversation.item.created'}
Received event: {'response.content_part.added'}
Received event: {'response.audio_transcript.delta'}
Received event: {'response.audio_transcript.delta'}

REDACTED FOR BREVITY

Received event: {'response.audio.delta'}
Received event: {'response.audio.delta'}
Received event: {'response.audio.done'}
Received event: {'response.audio_timestamp.done'}
Received event: {'response.audio_transcript.done'}

        Agent Audio Response: Alright, I've stopped. If you need anything else or have any questions, feel free to ask!       

Received event: {'response.content_part.done'}
Received event: {'response.output_item.done'}
Received event: {'response.done'}
q
Quitting the chat...
Chat done.
```

The script that you ran creates a log file named `voicelive.log` in the same directory as the script.

```python
logging.basicConfig(
    filename='voicelive.log',
    filemode="w",
    level=logging.DEBUG,
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s'
)
```

The `voicelive.log` file contains information about the connection to the Voice Live API, including the request and response data. You can view the log file to see the details of the conversation.

```text
2025-07-29 09:43:32,574:websockets.client:DEBUG:= connection is CONNECTING
2025-07-29 09:43:32,825:websockets.client:DEBUG:> GET /voice-live/realtime?api-version=2025-05-01-preview&agent-project-name=contoso-proj-agentic&agent-id=<your-agent-id>&agent-access-token=<your-token>&debug=on HTTP/1.1
2025-07-29 09:43:32,825:websockets.client:DEBUG:> Host: contoso-proj-agentic-foundry-res.cognitiveservices.azure.com
2025-07-29 09:43:32,825:websockets.client:DEBUG:> Upgrade: websocket
2025-07-29 09:43:32,825:websockets.client:DEBUG:> Connection: Upgrade
2025-07-29 09:43:32,825:websockets.client:DEBUG:> Sec-WebSocket-Key: 9c5PxKUKYk8esZIM201OQA==
2025-07-29 09:43:32,825:websockets.client:DEBUG:> Sec-WebSocket-Version: 13
2025-07-29 09:43:32,825:websockets.client:DEBUG:> Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits
2025-07-29 09:43:32,825:websockets.client:DEBUG:> x-ms-client-request-id: a7e5e46b-3c0a-41ca-b583-120678e8e038
2025-07-29 09:43:32,825:websockets.client:DEBUG:> Authorization: Bearer <your-token>
2025-07-29 09:43:32,825:websockets.client:DEBUG:> User-Agent: Python/3.12 websockets/15.0.1
2025-07-29 09:43:34,201:websockets.client:DEBUG:< HTTP/1.1 101 Switching Protocols
2025-07-29 09:43:34,201:websockets.client:DEBUG:< Upgrade: websocket
2025-07-29 09:43:34,202:websockets.client:DEBUG:< Connection: Upgrade
2025-07-29 09:43:34,202:websockets.client:DEBUG:< Sec-WebSocket-Accept: 41S61wZZ8zxD7ytcL9nVykuB5O0=
2025-07-29 09:43:34,202:websockets.client:DEBUG:< Date: Tue, 29 Jul 2025 16:43:34 GMT
2025-07-29 09:43:34,202:websockets.client:DEBUG:= connection is OPEN
2025-07-29 09:43:34,202:websockets.client:DEBUG:< TEXT '{"event_id":"event_2b3HeBPjTmeRpti25LwvrV","typ...WZ0W1TClHOo4TuNhF5O"}}}' [2036 bytes]
2025-07-29 09:43:34,204:websockets.client:DEBUG:> TEXT '{"type": "session.update", "session": {"turn_de...dio"]}, "event_id": ""}' [623 bytes]
2025-07-29 09:43:34,208:__main__:INFO:Starting audio stream ...
2025-07-29 09:43:34,270:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...NAA0A", "event_id": ""}' [1346 bytes]

REDACTED FOR BREVITY

2025-07-29 09:44:46,559:websockets.client:DEBUG:> CLOSE 1000 (OK) [2 bytes]
2025-07-29 09:44:46,559:websockets.client:DEBUG:= connection is CLOSING
2025-07-29 09:44:46,577:__main__:INFO:Audio stream closed.
2025-07-29 09:44:46,876:__main__:INFO:Playback done.
2025-07-29 09:44:47,686:websockets.client:DEBUG:< CLOSE 1000 (OK) [2 bytes]
2025-07-29 09:44:47,689:websockets.client:DEBUG:< EOF
2025-07-29 09:44:47,689:websockets.client:DEBUG:> EOF
2025-07-29 09:44:47,690:websockets.client:DEBUG:= connection is CLOSED
2025-07-29 09:44:47,690:websockets.client:DEBUG:x closing TCP connection
```

A session log file is created in the `logs` folder with the name `session_<session_id>.log`. This file contains detailed information about the session, including the request and response data.

```text
Agent Session Log:
Using agent: asst_NEQPZ5grNgCqCowPM0HJdXvH
Project name: contoso-proj-agentic
Session Config: {"type": "session.update", "session": {"turn_detection": {"type": "azure_semantic_vad", "threshold": 0.3, "prefix_padding_ms": 200, "silence_duration_ms": 200, "remove_filler_words": true, "end_of_utterance_detection": {"model": "semantic_detection_v1", "threshold": 0.1, "timeout": 4}}, "input_audio_noise_reduction": {"type": "azure_deep_noise_suppression"}, "input_audio_echo_cancellation": {"type": "server_echo_cancellation"}, "voice": {"name": "en-US-Aria:DragonHDLatestNeural", "type": "azure-standard", "temperature": 0.8}, "output_audio_timestamp_types": ["word"], "modalities": ["text", "audio"]}, "event_id": ""}
SessionID: sess_nLYa2BlHblzWObD8hn90T
User Input: Tell me a story.
Agent Audio Response: Sure! Here's a short story for you:

Once upon a time in a small village nestled between towering mountains, there lived a curious little girl named Elara. Elara loved exploring the forests and streams around her home, always eager to discover new wonders. One day, while wandering deeper into the woods than ever before, she stumbled upon a hidden glade where the sunlight danced through the leaves in dazzling patterns.

In the center of the glade stood an ancient tree with bark that shimmered like silver. As Elara approached, she noticed a tiny door carved into the trunk. With a mix of excitement and courage, she gently knocked. To her surprise, the door creaked open, revealing a cozy little room filled with glowing flowers and twinkling lights.

Inside, Elara met a wise old fairy who told her that the tree was the heart of the forest, protecting its magic and harmony. The fairy entrusted Elara with a special seed, saying it held the power to heal and grow new life wherever it was planted.

Elara promised to care for the seed and share its magic with the world. From that day on, she became the forest's guardian, weaving magic and kindness wherever she went. And thus, the village flourished, wrapped in the gentle embrace of nature's wonder, all thanks to the brave little girl who dared to peek behind the silver bark.

The end.

Would you like to hear another story or about something specific?
User Input: Stop.
Agent Audio Response: Alright, I've stopped. If you need anything else or have any questions, feel free to ask!
```

Here are the key differences between the [technical log](#technical-log) and the [session log](#session-log):

| Aspect | Session Log | Technical Log |
|--------|-------------|---------------|
| **Audience** | Business users, content reviewers | Developers, IT operations |
| **Content** | What was said in conversations | How the system is working |
| **Level** | Application/conversation level | System/infrastructure level |
| **Troubleshooting** | "What did the agent say?" | "Why did the connection fail?" |

**Example**: If your agent wasn't responding, you'd check:
- **voicelive.log** → "WebSocket connection failed" or "Audio stream error"
- **session log** → "Did the user actually say anything?"

Both logs are complementary - session logs for conversation analysis, technical logs for system diagnostics!

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

### Session log
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
