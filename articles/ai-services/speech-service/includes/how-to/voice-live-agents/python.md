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

```python
import os
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

voice_live_configuration = {
    "session": {
        "voice": {"name": "en-US-Ava:DragonHDLatestNeural", "type": "azure-standard", "temperature": 0.8},
        "input_audio_transcription": {"model": "azure-speech", "language": "en"},
        "turn_detection": {"type": "azure_semantic_vad",
            "end_of_utterance_detection": {
                "model": "semantic_detection_v1"
            },
        },
        "input_audio_noise_reduction": {"type": "azure_deep_noise_suppression"},
        "input_audio_echo_cancellation": {"type": "server_echo_cancellation"}
    }
}

agent = project_client.agents.create_version(
    agent_name=os.environ["AGENT_NAME"],
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions="You are a helpful assistant that answers general questions",
    ),
    metadata={
        "microsoft.voice-live.configuration": json.dumps(voice_live_configuration)
    },
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```

## Talk with a voice agent

The sample code in this quickstart uses Microsoft Entra ID for authentication as the current integration only supports this authentication method.

1. Create the `voice-live-agents-quickstart.py` file with the following code:

    ```python
    from __future__ import annotations
    import os
    import sys
    import asyncio
    import base64
    from datetime import datetime
    import logging
    import queue
    import signal
    from typing import Any, Union, Optional, TYPE_CHECKING, cast
    
    from azure.core.credentials import AzureKeyCredential
    from azure.core.credentials_async import AsyncTokenCredential
    from azure.identity.aio import AzureCliCredential
    
    from azure.ai.voicelive.aio import connect
    from azure.ai.voicelive.models import (
        InputAudioFormat,
        Modality,
        OutputAudioFormat,
        RequestSession,
        ServerEventType,
        MessageItem,
        InputTextContentPart,
    )
    from dotenv import load_dotenv
    import pyaudio
    
    if TYPE_CHECKING:
        # Only needed for type checking; avoids runtime import issues
        from azure.ai.voicelive.aio import VoiceLiveConnection
    
    # Environment variable loading
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(_script_dir, '.env'), override=True)
    
    # Set up logging
    ## Add folder for logging
    os.makedirs(os.path.join(_script_dir, 'logs'), exist_ok=True)
    
    ## Add timestamp for logfiles
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    ## Create conversation log filename
    logfilename = f"{timestamp}_conversation.log"
    
    ## Set up logging
    logging.basicConfig(
        filename=os.path.join(_script_dir, 'logs', f'{timestamp}_voicelive.log'),
        filemode="w",
        format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    
    class AudioProcessor:
        """
        Handles real-time audio capture and playback for the voice assistant.
    
        Threading Architecture:
        - Main thread: Event loop and UI
        - Capture thread: PyAudio input stream reading
        - Send thread: Async audio data transmission to VoiceLive
        - Playback thread: PyAudio output stream writing
        """
        
        loop: asyncio.AbstractEventLoop
        
        class AudioPlaybackPacket:
            """Represents a packet that can be sent to the audio playback queue."""
            def __init__(self, seq_num: int, data: Optional[bytes]):
                self.seq_num = seq_num
                self.data = data
    
        def __init__(self, connection: VoiceLiveConnection) -> None:
            self.connection = connection
            self.audio = pyaudio.PyAudio()
    
            # Audio configuration - PCM16, 24kHz, mono as specified
            self.format = pyaudio.paInt16
            self.channels = 1
            self.rate = 24000
            self.chunk_size = 1200 # 50ms
    
            # Capture and playback state
            self.input_stream = None
    
            self.playback_queue: queue.Queue[AudioProcessor.AudioPlaybackPacket] = queue.Queue()
            self.playback_base = 0
            self.next_seq_num = 0
            self.output_stream: Optional[pyaudio.Stream] = None
    
            logger.info("AudioProcessor initialized with 24kHz PCM16 mono audio")
    
        def start_capture(self) -> None:
            """Start capturing audio from microphone."""
            def _capture_callback(
                in_data,      # data
                _frame_count,  # number of frames
                _time_info,    # dictionary
                _status_flags):
                """Audio capture thread - runs in background."""
                audio_base64 = base64.b64encode(in_data).decode("utf-8")
                asyncio.run_coroutine_threadsafe(
                    self.connection.input_audio_buffer.append(audio=audio_base64), self.loop
                )
                return (None, pyaudio.paContinue)
    
            if self.input_stream:
                return
    
            # Store the current event loop for use in threads
            self.loop = asyncio.get_event_loop()
    
            try:
                self.input_stream = self.audio.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    input=True,
                    frames_per_buffer=self.chunk_size,
                    stream_callback=_capture_callback,
                )
                logger.info("Started audio capture")
    
            except Exception:
                logger.exception("Failed to start audio capture")
                raise
    
        def start_playback(self) -> None:
            """Initialize audio playback system."""
            if self.output_stream:
                return
    
            remaining = bytes()
            def _playback_callback(
                _in_data,
                frame_count,  # number of frames
                _time_info,
                _status_flags):
    
                nonlocal remaining
                frame_count *= pyaudio.get_sample_size(pyaudio.paInt16)
    
                out = remaining[:frame_count]
                remaining = remaining[frame_count:]
    
                while len(out) < frame_count:
                    try:
                        packet = self.playback_queue.get_nowait()
                    except queue.Empty:
                        out = out + bytes(frame_count - len(out))
                        continue
                    except Exception:
                        logger.exception("Error in audio playback")
                        raise
    
                    if not packet or not packet.data:
                        # None packet indicates end of stream
                        logger.info("End of playback queue.")
                        break
    
                    if packet.seq_num < self.playback_base:
                        # skip requested
                        # ignore skipped packet and clear remaining
                        if len(remaining) > 0:
                            remaining = bytes()
                        continue
    
                    num_to_take = frame_count - len(out)
                    out = out + packet.data[:num_to_take]
                    remaining = packet.data[num_to_take:]
    
                if len(out) >= frame_count:
                    return (out, pyaudio.paContinue)
                else:
                    return (out, pyaudio.paComplete)
    
            try:
                self.output_stream = self.audio.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    output=True,
                    frames_per_buffer=self.chunk_size,
                    stream_callback=_playback_callback
                )
                logger.info("Audio playback system ready")
            except Exception:
                logger.exception("Failed to initialize audio playback")
                raise
    
        def _get_and_increase_seq_num(self) -> int:
            seq = self.next_seq_num
            self.next_seq_num += 1
            return seq
    
        def queue_audio(self, audio_data: Optional[bytes]) -> None:
            """Queue audio data for playback."""
            self.playback_queue.put(
                AudioProcessor.AudioPlaybackPacket(
                    seq_num=self._get_and_increase_seq_num(),
                    data=audio_data))
    
        def skip_pending_audio(self) -> None:
            """Skip current audio in playback queue."""
            self.playback_base = self._get_and_increase_seq_num()
    
        def shutdown(self) -> None:
            """Clean up audio resources."""
            if self.input_stream:
                self.input_stream.stop_stream()
                self.input_stream.close()
                self.input_stream = None
    
            logger.info("Stopped audio capture")
    
            # Inform thread to complete
            if self.output_stream:
                self.skip_pending_audio()
                self.queue_audio(None)
                self.output_stream.stop_stream()
                self.output_stream.close()
                self.output_stream = None
    
            logger.info("Stopped audio playback")
    
            if self.audio:
                self.audio.terminate()
    
            logger.info("Audio processor cleaned up")
    
    class BasicVoiceAssistant:
        """
            Basic voice assistant implementing the VoiceLive SDK patterns with Foundry Agent.
            This sample also demonstrates how to collect a conversation log of user and agent interactions.
        """
    
    
        def __init__(
            self,
            endpoint: str,
            credential: Union[AzureKeyCredential, AsyncTokenCredential],
            agent_name: str,
            project_name: str
        ):
    
            self.endpoint = endpoint
            self.credential = credential
            self.agent_name = agent_name
            self.project_name = project_name
            self.connection: Optional["VoiceLiveConnection"] = None
            self.audio_processor: Optional[AudioProcessor] = None
            self.session_ready = False
            self.greeting_sent = False
            self._active_response = False
            self._response_api_done = False
    
        async def start(self) -> None:
            """Start the voice assistant session."""
            try:
                logger.info("Connecting to VoiceLive API with Foundry agent connection %s for project %s", self.agent_name, self.project_name)
    
                # Connect to VoiceLive WebSocket API
                async with connect(
                    endpoint=self.endpoint,
                    credential=self.credential,
                    query={
                        "agent-name": self.agent_name,
                        "agent-project-name": self.project_name
                    },
                ) as connection:
                    conn = connection
                    self.connection = conn
    
                    # Initialize audio processor
                    ap = AudioProcessor(conn)
                    self.audio_processor = ap
    
                    # Configure session for voice conversation
                    await self._setup_session()
    
                    # Start audio systems
                    ap.start_playback()
    
                    logger.info("Voice assistant ready! Start speaking...")
                    print("\n" + "=" * 60)
                    print("🎤 VOICE ASSISTANT READY")
                    print("Start speaking to begin conversation")
                    print("Press Ctrl+C to exit")
                    print("=" * 60 + "\n")
    
                    # Process events
                    await self._process_events()
            finally:
                if self.audio_processor:
                    self.audio_processor.shutdown()
    
        async def _setup_session(self) -> None:
            """Configure the VoiceLive session for audio conversation."""
            logger.info("Setting up voice conversation session...")
    
            # Create session configuration
            session_config = RequestSession(
                modalities=[Modality.TEXT, Modality.AUDIO],
                input_audio_format=InputAudioFormat.PCM16,
                output_audio_format=OutputAudioFormat.PCM16,
            )
    
            conn = self.connection
            if conn is None:
                raise RuntimeError("Connection must be established before setting up session")
            await conn.session.update(session=session_config)
    
            logger.info("Session configuration sent")
    
        async def _process_events(self) -> None:
            """Process events from the VoiceLive connection."""
            try:
                conn = self.connection
                if conn is None:
                    raise RuntimeError("Connection must be established before processing events")
                async for event in conn:
                    await self._handle_event(event)
            except Exception:
                logger.exception("Error processing events")
                raise
    
        async def _handle_event(self, event: Any) -> None:
            """Handle different types of events from VoiceLive."""
            logger.debug("Received event: %s", event.type)
            ap = self.audio_processor
            conn = self.connection
            if ap is None or conn is None:
                raise RuntimeError("AudioProcessor and Connection must be initialized")
    
            if event.type == ServerEventType.SESSION_UPDATED:
                logger.info("Session ready: %s", event.session.id)
                s, a, v = event.session, event.session.agent, event.session.voice
                await write_conversation_log("\n".join([
                    f"SessionID: {s.id}", f"Agent Name: {a.name}",
                    f"Agent Description: {a.description}", f"Agent ID: {a.agent_id}",
                    f"Thread ID: {a.thread_id}",
                    f"Voice Name: {v['name']}", f"Voice Type: {v['type']}",
                    f"Voice Temperature: {v['temperature']}", ""
                ]))
                self.session_ready = True
    
                # Invoke Proactive greeting
                if not self.greeting_sent:
                    self.greeting_sent = True
                    logger.info("Sending proactive greeting request")
                    try:
                        await conn.conversation.item.create(
                            item=MessageItem(
                                role="system",
                                content=[
                                    InputTextContentPart(
                                        text="Say something to welcome the user."
                                    )
                                ]
                            )
                        )
                        await conn.response.create()
                    except Exception:
                        logger.exception("Failed to send proactive greeting request")
    
                # Start audio capture once session is ready
                ap.start_capture()
    
            elif event.type == ServerEventType.CONVERSATION_ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED:
                print(f'👤 You said:\t{event.get("transcript", "")}')
                await write_conversation_log(f'User Input:\t{event.get("transcript", "")}')
    
            elif event.type == ServerEventType.RESPONSE_TEXT_DONE:
                print(f'🤖 Agent responded with text:\t{event.get("text", "")}')
                await write_conversation_log(f'Agent Text Response:\t{event.get("text", "")}')
    
            elif event.type == ServerEventType.RESPONSE_AUDIO_TRANSCRIPT_DONE:
                print(f'🤖 Agent responded with audio transcript:\t{event.get("transcript", "")}')
                await write_conversation_log(f'Agent Audio Response:\t{event.get("transcript", "")}')
    
            elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
                logger.info("User started speaking - stopping playback")
                print("🎤 Listening...")
    
                ap.skip_pending_audio()
    
                # Only cancel if response is active and not already done
                if self._active_response and not self._response_api_done:
                    try:
                        await conn.response.cancel()
                        logger.debug("Cancelled in-progress response due to barge-in")
                    except Exception as e:
                        if "no active response" in str(e).lower():
                            logger.debug("Cancel ignored - response already completed")
                        else:
                            logger.warning("Cancel failed: %s", e)
    
            elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STOPPED:
                logger.info("🎤 User stopped speaking")
                print("🤔 Processing...")
    
            elif event.type == ServerEventType.RESPONSE_CREATED:
                logger.info("🤖 Assistant response created")
                self._active_response = True
                self._response_api_done = False
    
            elif event.type == ServerEventType.RESPONSE_AUDIO_DELTA:
                logger.debug("Received audio delta")
                ap.queue_audio(event.delta)
    
            elif event.type == ServerEventType.RESPONSE_AUDIO_DONE:
                logger.info("🤖 Assistant finished speaking")
                print("🎤 Ready for next input...")
    
            elif event.type == ServerEventType.RESPONSE_DONE:
                logger.info("✅ Response complete")
                self._active_response = False
                self._response_api_done = True
    
            elif event.type == ServerEventType.ERROR:
                msg = event.error.message
                if "Cancellation failed: no active response" in msg:
                    logger.debug("Benign cancellation error: %s", msg)
                else:
                    logger.error("❌ VoiceLive error: %s", msg)
                    print(f"Error: {msg}")
    
            elif event.type == ServerEventType.CONVERSATION_ITEM_CREATED:
                logger.debug("Conversation item created: %s", event.item.id)
    
            else:
                logger.debug("Unhandled event type: %s", event.type)
    
    async def write_conversation_log(message: str) -> None:
        """Write a message to the conversation log."""
        log_path = os.path.join(_script_dir, 'logs', logfilename)
        await asyncio.to_thread(
            lambda: open(log_path, 'a', encoding='utf-8').write(message + "\n")
        )
    
    def main() -> None:
        """Main function."""
        endpoint = os.environ.get("VOICELIVE_ENDPOINT", "")
        agent_name = os.environ.get("AGENT_NAME", "")
        project_name = os.environ.get("PROJECT_NAME", "")
    
        if not endpoint or not agent_name or not project_name:
            sys.exit("Set VOICELIVE_ENDPOINT, AGENT_NAME, and PROJECT_NAME in your .env file.")
    
        # Create client with appropriate credential
        credential = AzureCliCredential()
        logger.info("Using Azure token credential")
    
        # Create and start voice assistant
        assistant = BasicVoiceAssistant(
            endpoint=endpoint,
            credential=credential,
            agent_name=agent_name,
            project_name=project_name
        )
    
        # Handle SIGTERM for graceful shutdown (SIGINT already raises KeyboardInterrupt)
        signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    
        # Start the assistant
        try:
            asyncio.run(assistant.start())
        except KeyboardInterrupt:
            print("\n👋 Voice assistant shut down. Goodbye!")
        except Exception as e:
            print("Fatal Error: ", e)
    
    def _check_audio_devices() -> None:
        """Verify audio input/output devices are available."""
        p = pyaudio.PyAudio()
        try:
            def _has_channels(key):
                return any(
                    cast(Union[int, float], p.get_device_info_by_index(i).get(key, 0) or 0) > 0
                    for i in range(p.get_device_count())
                )
            if not _has_channels("maxInputChannels"):
                sys.exit("❌ No audio input devices found. Please check your microphone.")
            if not _has_channels("maxOutputChannels"):
                sys.exit("❌ No audio output devices found. Please check your speakers.")
        finally:
            p.terminate()
    
    if __name__ == "__main__":
        try:
            _check_audio_devices()
        except SystemExit:
            raise
        except Exception as e:
            sys.exit(f"❌ Audio system check failed: {e}")
    
        print("🎙️ Basic Foundry Voice Agent with Azure VoiceLive SDK")
        print("=" * 60)
        main()
    ```

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
