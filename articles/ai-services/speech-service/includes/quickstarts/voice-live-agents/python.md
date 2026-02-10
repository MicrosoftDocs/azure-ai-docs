---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
reviewer: patrickfarley
ms.reviewer: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 11/06/2025
ms.subservice: azure-ai-foundry-openai
---

In this article, you learn how to use Voice Live with [Microsoft Foundry Agent Service](/azure/ai-foundry/agents/overview) using the VoiceLive SDK for python. 

[!INCLUDE [Header](../../common/voice-live-python.md)] 

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.10 or later version</a>. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- A Microsoft Foundry agent created in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). For more information about creating an agent, see the [Create an agent quickstart](/azure/ai-foundry/agents/quickstart).

> [!TIP]
> To use Voice Live, you don't need to deploy an audio model with your Microsoft Foundry resource. Voice Live is fully managed, and the model is automatically deployed for you. For more information about models availability, see the [Voice Live overview documentation](../../../voice-live.md).

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
    > We recommend that you create and activate a new Python environment to use to install the packages you need for this tutorial. Don't install packages into your global Python installation. You should always use a virtual or conda environment when installing Python packages, otherwise you can break your global installation of Python.

1. Create a file named **requirements.txt**. Add the following packages to the file:

    ```txt
    azure-ai-voicelive[aiohttp]
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

## Start a conversation

The sample code in this quickstart uses Microsoft Entra ID for authentication as the current integration only supports this authentication method.

1. Create the `voice-live-agents-quickstart.py` file with the following code:

    ```python
    # -------------------------------------------------------------------------
    # Copyright (c) Microsoft Corporation. All rights reserved.
    # Licensed under the MIT License.
    # -------------------------------------------------------------------------
    from __future__ import annotations
    import os
    import sys
    import argparse
    import asyncio
    import base64
    from datetime import datetime
    import logging
    import queue
    import signal
    from typing import Union, Optional, TYPE_CHECKING, cast
    
    from azure.core.credentials import AzureKeyCredential
    from azure.core.credentials_async import AsyncTokenCredential
    from azure.identity.aio import AzureCliCredential, DefaultAzureCredential
    
    from azure.ai.voicelive.aio import connect
    from azure.ai.voicelive.models import (
        AudioEchoCancellation,
        AudioNoiseReduction,
        AzureStandardVoice,
        InputAudioFormat,
        Modality,
        OutputAudioFormat,
        RequestSession,
        ServerEventType,
        ServerVad
    )
    from dotenv import load_dotenv
    import pyaudio
    
    if TYPE_CHECKING:
        # Only needed for type checking; avoids runtime import issues
        from azure.ai.voicelive.aio import VoiceLiveConnection
    
    ## Change to the directory where this script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Environment variable loading
    load_dotenv('./.env', override=True)
    
    # Set up logging
    ## Add folder for logging
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    ## Add timestamp for logfiles
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    ## Create conversation log filename
    logfilename = f"{timestamp}_conversation.log"
    
    ## Set up logging
    logging.basicConfig(
        filename=f'logs/{timestamp}_voicelive.log',
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
    
        def __init__(self, connection):
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
    
        def start_capture(self):
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
    
        def start_playback(self):
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
    
        def _get_and_increase_seq_num(self):
            seq = self.next_seq_num
            self.next_seq_num += 1
            return seq
    
        def queue_audio(self, audio_data: Optional[bytes]) -> None:
            """Queue audio data for playback."""
            self.playback_queue.put(
                AudioProcessor.AudioPlaybackPacket(
                    seq_num=self._get_and_increase_seq_num(),
                    data=audio_data))
    
        def skip_pending_audio(self):
            """Skip current audio in playback queue."""
            self.playback_base = self._get_and_increase_seq_num()
    
        def shutdown(self):
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
            agent_id: str,
            foundry_project_name: str,
            voice: str,
        ):
    
            self.endpoint = endpoint
            self.credential = credential
            self.agent_id = agent_id
            self.foundry_project_name = foundry_project_name
            self.voice = voice
            self.connection: Optional["VoiceLiveConnection"] = None
            self.audio_processor: Optional[AudioProcessor] = None
            self.session_ready = False
            self.conversation_started = False
            self._active_response = False
            self._response_api_done = False
    
        async def start(self):
            """Start the voice assistant session."""
            try:
                logger.info("Connecting to VoiceLive API with Foundry agent connection %s for project %s", self.agent_id, self.foundry_project_name)
    
                # Get agent access token
                agent_access_token = (await DefaultAzureCredential().get_token("https://ai.azure.com/.default")).token
                logger.info("Obtained agent access token")
    
                # Connect to VoiceLive WebSocket API
                async with connect(
                    endpoint=self.endpoint,
                    credential=self.credential,
                    query={
                        "agent-id": self.agent_id,
                        "agent-project-name": self.foundry_project_name,
                        "agent-access-token": agent_access_token
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
    
        async def _setup_session(self):
            """Configure the VoiceLive session for audio conversation."""
            logger.info("Setting up voice conversation session...")
    
            # Create voice configuration
            voice_config: Union[AzureStandardVoice, str]
            if self.voice.startswith("en-US-") or self.voice.startswith("en-CA-") or "-" in self.voice:
                # Azure voice
                voice_config = AzureStandardVoice(name=self.voice)
            else:
                # OpenAI voice (alloy, echo, fable, onyx, nova, shimmer)
                voice_config = self.voice
    
            # Create turn detection configuration
            turn_detection_config = ServerVad(
                threshold=0.5,
                prefix_padding_ms=300,
                silence_duration_ms=500)
    
            # Create session configuration
            session_config = RequestSession(
                modalities=[Modality.TEXT, Modality.AUDIO],
                voice=voice_config,
                input_audio_format=InputAudioFormat.PCM16,
                output_audio_format=OutputAudioFormat.PCM16,
                turn_detection=turn_detection_config,
                input_audio_echo_cancellation=AudioEchoCancellation(),
                input_audio_noise_reduction=AudioNoiseReduction(type="azure_deep_noise_suppression"),
            )
    
            conn = self.connection
            assert conn is not None, "Connection must be established before setting up session"
            await conn.session.update(session=session_config)
    
            logger.info("Session configuration sent")
    
        async def _process_events(self):
            """Process events from the VoiceLive connection."""
            try:
                conn = self.connection
                assert conn is not None, "Connection must be established before processing events"
                async for event in conn:
                    await self._handle_event(event)
            except Exception:
                logger.exception("Error processing events")
                raise
    
        async def _handle_event(self, event):
            """Handle different types of events from VoiceLive."""
            logger.debug("Received event: %s", event.type)
            ap = self.audio_processor
            conn = self.connection
            assert ap is not None, "AudioProcessor must be initialized"
            assert conn is not None, "Connection must be established"
    
            if event.type == ServerEventType.SESSION_UPDATED:
                logger.info("Session ready: %s", event.session.id)
                await write_conversation_log(f"SessionID: {event.session.id}")
                await write_conversation_log(f"Model: {event.session.model}")
                await write_conversation_log(f"Voice: {event.session.voice}")
                await write_conversation_log(f"Instructions: {event.session.instructions}")
                await write_conversation_log(f"")
                self.session_ready = True
    
                # Invoke Proactive greeting
                if not self.conversation_started:
                    self.conversation_started = True
                    logger.info("Sending proactive greeting request")
                    try:
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
        def _write_to_file():
            with open(f'logs/{logfilename}', 'a', encoding='utf-8') as conversation_log:
                conversation_log.write(message + "\n")
        
        await asyncio.to_thread(_write_to_file)
    
    def parse_arguments():
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(
            description="Basic Voice Assistant using Azure VoiceLive SDK",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    
        parser.add_argument(
            "--api-key",
            help="Azure VoiceLive API key. If not provided, will use AZURE_VOICELIVE_API_KEY environment variable.",
            type=str,
            default=os.environ.get("AZURE_VOICELIVE_API_KEY"),
        )
    
        parser.add_argument(
            "--endpoint",
            help="Azure VoiceLive endpoint",
            type=str,
            default=os.environ.get("AZURE_VOICELIVE_ENDPOINT", "https://your-resource-name.services.ai.azure.com/"),
        )
    
        parser.add_argument(
            "--agent_id",
            help="Foundry agent ID to use",
            type=str,
            default=os.environ.get("AZURE_VOICELIVE_AGENT_ID", ""),
        )
    
        parser.add_argument(
            "--foundry_project_name",
            help="Foundry project name to use",
            type=str,
            default=os.environ.get("AZURE_VOICELIVE_PROJECT_NAME", ""),
        )
    
        parser.add_argument(
            "--voice",
            help="Voice to use for the assistant. E.g. alloy, echo, fable, en-US-AvaNeural, en-US-GuyNeural",
            type=str,
            default=os.environ.get("AZURE_VOICELIVE_VOICE", "en-US-Ava:DragonHDLatestNeural"),
        )
    
        parser.add_argument(
            "--use-token-credential", help="Use Azure token credential instead of API key", action="store_true", default=True
        )
    
        parser.add_argument("--verbose", help="Enable verbose logging", action="store_true")
    
        return parser.parse_args()
    
    
    def main():
        """Main function."""
        args = parse_arguments()
    
        # Set logging level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
    
        # Validate credentials
        if not args.api_key and not args.use_token_credential:
            print("❌ Error: No authentication provided")
            print("Please provide an API key using --api-key or set AZURE_VOICELIVE_API_KEY environment variable,")
            print("or use --use-token-credential for Azure authentication.")
            sys.exit(1)
    
        # Create client with appropriate credential
        credential: Union[AzureKeyCredential, AsyncTokenCredential]
        if args.use_token_credential:
            credential = AzureCliCredential()  # or DefaultAzureCredential() if needed
            logger.info("Using Azure token credential")
        else:
            credential = AzureKeyCredential(args.api_key)
            logger.info("Using API key credential")
    
        # Create and start voice assistant
        assistant = BasicVoiceAssistant(
            endpoint=args.endpoint,
            credential=credential,
            agent_id=args.agent_id,
            foundry_project_name=args.foundry_project_name,
            voice=args.voice,
        )
    
        # Setup signal handlers for graceful shutdown
        def signal_handler(_sig, _frame):
            logger.info("Received shutdown signal")
            raise KeyboardInterrupt()
    
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
        # Start the assistant
        try:
            asyncio.run(assistant.start())
        except KeyboardInterrupt:
            print("\n👋 Voice assistant shut down. Goodbye!")
        except Exception as e:
            print("Fatal Error: ", e)
    
    if __name__ == "__main__":
        # Check audio system
        try:
            p = pyaudio.PyAudio()
            # Check for input devices
            input_devices = [
                i
                for i in range(p.get_device_count())
                if cast(Union[int, float], p.get_device_info_by_index(i).get("maxInputChannels", 0) or 0) > 0
            ]
            # Check for output devices
            output_devices = [
                i
                for i in range(p.get_device_count())
                if cast(Union[int, float], p.get_device_info_by_index(i).get("maxOutputChannels", 0) or 0) > 0
            ]
            p.terminate()
    
            if not input_devices:
                print("❌ No audio input devices found. Please check your microphone.")
                sys.exit(1)
            if not output_devices:
                print("❌ No audio output devices found. Please check your speakers.")
                sys.exit(1)
    
        except Exception as e:
            print(f"❌ Audio system check failed: {e}")
            sys.exit(1)
    
        print("🎙️  Basic Voice Assistant with Azure VoiceLive SDK")
        print("=" * 50)
    
        # Run the assistant
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
2025-10-28 10:26:12,768:__main__:INFO:Using Azure token credential
2025-10-28 10:26:12,769:__main__:INFO:Connecting to VoiceLive API with Foundry agent connection asst_JVSR1R9XpUBxZP1c4YUWy2GA for project myservice-voicelive-eus2
2025-10-28 10:26:12,770:azure.identity.aio._credentials.environment:INFO:No environment configuration found.
2025-10-28 10:26:12,779:azure.identity.aio._credentials.managed_identity:INFO:ManagedIdentityCredential will use IMDS
2025-10-28 10:26:12,780:azure.core.pipeline.policies.http_logging_policy:INFO:Request URL: 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=REDACTED&resource=REDACTED'
Request method: 'GET'
Request headers:
    'User-Agent': 'azsdk-python-identity/1.25.1 Python/3.11.9 (Windows-10-10.0.26200-SP0)'
No body was attached to the request
2025-10-28 10:26:14,527:azure.identity.aio._credentials.chained:INFO:DefaultAzureCredential acquired a token from AzureCliCredential
2025-10-28 10:26:14,527:__main__:INFO:Obtained agent access token
2025-10-28 10:26:16,036:azure.identity.aio._internal.decorators:INFO:AzureCliCredential.get_token succeeded
2025-10-28 10:26:16,575:__main__:INFO:AudioProcessor initialized with 24kHz PCM16 mono audio
2025-10-28 10:26:16,575:__main__:INFO:Setting up voice conversation session...
2025-10-28 10:26:16,576:__main__:INFO:Session configuration sent
2025-10-28 10:26:16,833:__main__:INFO:Audio playback system ready
2025-10-28 10:26:16,833:__main__:INFO:Voice assistant ready! Start speaking...
2025-10-28 10:26:17,691:__main__:INFO:Session ready: sess_Oics8h0KxxxxPne71S1k
2025-10-28 10:26:17,713:__main__:INFO:Started audio capture
2025-10-28 10:26:18,413:__main__:INFO:User started speaking - stopping playback
2025-10-28 10:26:19,007:__main__:INFO:\U0001f3a4 User stopped speaking
2025-10-28 10:26:24,009:__main__:INFO:User started speaking - stopping playback
2025-10-28 10:26:24,771:__main__:INFO:\U0001f3a4 User stopped speaking
2025-10-28 10:26:24,887:__main__:INFO:\U0001f916 Assistant response created
2025-10-28 10:26:30,273:__main__:INFO:\U0001f916 Assistant finished speaking
2025-10-28 10:26:30,275:__main__:INFO:\u2705 Response complete
2025-10-28 10:26:38,461:__main__:INFO:User started speaking - stopping playback
2025-10-28 10:26:39,909:__main__:INFO:\U0001f3a4 User stopped speaking
2025-10-28 10:26:40,090:__main__:INFO:\U0001f916 Assistant response created
2025-10-28 10:26:44,631:__main__:INFO:\U0001f916 Assistant finished speaking
2025-10-28 10:26:44,634:__main__:INFO:\u2705 Response complete
2025-10-28 10:26:47,190:__main__:INFO:User started speaking - stopping playback
2025-10-28 10:26:48,959:__main__:INFO:\U0001f3a4 User stopped speaking
2025-10-28 10:26:49,246:__main__:INFO:\U0001f916 Assistant response created
2025-10-28 10:27:01,306:__main__:INFO:\U0001f916 Assistant finished speaking
2025-10-28 10:27:01,315:__main__:INFO:\u2705 Response complete
2025-10-28 10:27:09,586:__main__:INFO:Received shutdown signal
2025-10-28 10:27:09,634:__main__:INFO:Stopped audio capture
2025-10-28 10:27:09,758:__main__:INFO:Stopped audio playback
2025-10-28 10:27:09,759:__main__:INFO:Audio processor cleaned up
```

Further a session log file is created in the `logs` folder with the name `<timestamp>_conversation.log`. This file contains detailed information about the session, including the request and response data.

```text
SessionID: sess_Oics8h0KxxxxPne71S1k
Model: gpt-4.1-mini
Voice: {'name': 'en-US-Ava:DragonHDLatestNeural', 'type': 'azure-standard'}
Instructions: You are a helpful agent named 'Tobi the agent'.

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

## Hub-based projects

The quickstart uses Foundry projects instead of hub-based projects. If you have a hub-based project, you can still use the quickstart with some modifications.

To use the quickstart with a hub-based project, you need to retrieve the connection string for your agent and use it instead of the ```foundry_project_name```. You can find the connection string in the Azure portal under your Foundry project.

### Overview

For hub-based projects, use the connection string instead of the project name to connect your agent.

Further you must obtain a separate authentication token from scope 'https://ml.azure.com/.default'.

Make the following changes to the quickstart code:

1. Replace the all instances of `foundry_project_name` with `agent-connection-string` following lines in the code to change the authentication:

1. Replace the authentication token scope in line `307`:
    ```python
    # Get agent access token
    agent_access_token = (await DefaultAzureCredential().get_token("https://ml.azure.com/.default")).token
    logger.info("Obtained agent access token")
    ```

1. Replace the query parameter in line `316`:
    ```python
    # Connect to VoiceLive WebSocket API
    async with connect(
        endpoint=self.endpoint,
        credential=self.credential,
        query={
            "agent-id": self.agent_id,
            "agent-connection-string": self.agent-connection-string,
            "agent-access-token": agent_access_token
        },
    ) as connection:
        conn = connection
        self.connection = conn
    ```
    