---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-openai
ms.topic: include
ms.date: 7/31/2025
---

In this article, you learn how to use Azure AI Speech voice live with [Azure AI Foundry models](/azure/ai-foundry/concepts/foundry-models-overview) using the VoiceLive SDK for Python.

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- <a href="https://www.python.org/" target="_blank">Python 3.10 or later version</a>. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- An [Azure AI Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [voice live overview documentation](../../../voice-live.md).

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
    azure-core==1.35.0
    azure-identity==1.22.0
    certifi==2025.4.26
    cffi==1.17.1
    cryptography==44.0.3
    numpy==2.2.5
    pycparser==2.22
    python-dotenv==1.1.0
    pyaudio
    requests==2.32.3
    sounddevice==0.5.1
    typing_extensions==4.13.2
    urllib3==2.4.0
    websocket-client==1.8.0
    azure-ai-voicelive==1.0.0b1
    pyaudio
    ```

1. Install the packages:

    ```bash
    pip install -r requirements.txt
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]


## Start a conversation

The sample code in this quickstart uses either Microsoft Entra ID or an API key for authentication. You can set the script argument to be either your API key or your access token. 

1. Create the `voice-live-quickstart.py` file with the following code:

    ```python
    import os
    import sys
    import asyncio
    import base64
    import argparse
    import signal
    import threading
    import queue
    from azure.ai.voicelive.models import ServerEventType
    from typing import Union, Optional, TYPE_CHECKING, cast
    from concurrent.futures import ThreadPoolExecutor
    import logging
    
    # Audio processing imports
    try:
        import pyaudio
    except ImportError:
        print("This sample requires pyaudio. Install with: pip install pyaudio")
        sys.exit(1)
    
    # Environment variable loading
    try:
        from dotenv import load_dotenv
    
        load_dotenv()
    except ImportError:
        print("Note: python-dotenv not installed. Using existing environment variables.")
    
    # Azure VoiceLive SDK imports
    from azure.core.credentials import AzureKeyCredential, TokenCredential
    from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
    
    from azure.ai.voicelive.aio import connect
    
    if TYPE_CHECKING:
        # Only needed for type checking; avoids runtime import issues
        from azure.ai.voicelive.aio import VoiceLiveConnection
    
    from azure.ai.voicelive.models import (
        RequestSession,
        ServerVad,
        AzureStandardVoice,
        Modality,
        AudioFormat,
    )
    
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
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
    
        def __init__(self, connection):
            self.connection = connection
            self.audio = pyaudio.PyAudio()
    
            # Audio configuration - PCM16, 24kHz, mono as specified
            self.format = pyaudio.paInt16
            self.channels = 1
            self.rate = 24000
            self.chunk_size = 1024
    
            # Capture and playback state
            self.is_capturing = False
            self.is_playing = False
            self.input_stream = None
            self.output_stream = None
    
            # Audio queues and threading
            self.audio_queue: "queue.Queue[bytes]" = queue.Queue()
            self.audio_send_queue: "queue.Queue[str]" = queue.Queue()  # base64 audio to send
            self.executor = ThreadPoolExecutor(max_workers=3)
            self.capture_thread: Optional[threading.Thread] = None
            self.playback_thread: Optional[threading.Thread] = None
            self.send_thread: Optional[threading.Thread] = None
            self.loop: Optional[asyncio.AbstractEventLoop] = None  # Store the event loop
    
            logger.info("AudioProcessor initialized with 24kHz PCM16 mono audio")
    
        async def start_capture(self):
            """Start capturing audio from microphone."""
            if self.is_capturing:
                return
    
            # Store the current event loop for use in threads
            self.loop = asyncio.get_event_loop()
    
            self.is_capturing = True
    
            try:
                self.input_stream = self.audio.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    input=True,
                    frames_per_buffer=self.chunk_size,
                    stream_callback=None,
                )
    
                self.input_stream.start_stream()
    
                # Start capture thread
                self.capture_thread = threading.Thread(target=self._capture_audio_thread)
                self.capture_thread.daemon = True
                self.capture_thread.start()
    
                # Start audio send thread
                self.send_thread = threading.Thread(target=self._send_audio_thread)
                self.send_thread.daemon = True
                self.send_thread.start()
    
                logger.info("Started audio capture")
    
            except Exception as e:
                logger.error(f"Failed to start audio capture: {e}")
                self.is_capturing = False
                raise
    
        def _capture_audio_thread(self):
            """Audio capture thread - runs in background."""
            while self.is_capturing and self.input_stream:
                try:
                    # Read audio data
                    audio_data = self.input_stream.read(self.chunk_size, exception_on_overflow=False)
    
                    if audio_data and self.is_capturing:
                        # Convert to base64 and queue for sending
                        audio_base64 = base64.b64encode(audio_data).decode("utf-8")
                        self.audio_send_queue.put(audio_base64)
    
                except Exception as e:
                    if self.is_capturing:
                        logger.error(f"Error in audio capture: {e}")
                    break
    
        def _send_audio_thread(self):
            """Audio send thread - handles async operations from sync thread."""
            while self.is_capturing:
                try:
                    # Get audio data from queue (blocking with timeout)
                    audio_base64 = self.audio_send_queue.get(timeout=0.1)
    
                    if audio_base64 and self.is_capturing and self.loop:
                        # Schedule the async send operation in the main event loop
                        future = asyncio.run_coroutine_threadsafe(
                            self.connection.input_audio_buffer.append(audio=audio_base64), self.loop
                        )
                        # Don't wait for completion to avoid blocking
    
                except queue.Empty:
                    continue
                except Exception as e:
                    if self.is_capturing:
                        logger.error(f"Error sending audio: {e}")
                    break
    
        async def stop_capture(self):
            """Stop capturing audio."""
            if not self.is_capturing:
                return
    
            self.is_capturing = False
    
            if self.input_stream:
                self.input_stream.stop_stream()
                self.input_stream.close()
                self.input_stream = None
    
            if self.capture_thread:
                self.capture_thread.join(timeout=1.0)
    
            if self.send_thread:
                self.send_thread.join(timeout=1.0)
    
            # Clear the send queue
            while not self.audio_send_queue.empty():
                try:
                    self.audio_send_queue.get_nowait()
                except queue.Empty:
                    break
    
            logger.info("Stopped audio capture")
    
        async def start_playback(self):
            """Initialize audio playback system."""
            if self.is_playing:
                return
    
            self.is_playing = True
    
            try:
                self.output_stream = self.audio.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    output=True,
                    frames_per_buffer=self.chunk_size,
                )
    
                # Start playback thread
                self.playback_thread = threading.Thread(target=self._playback_audio_thread)
                self.playback_thread.daemon = True
                self.playback_thread.start()
    
                logger.info("Audio playback system ready")
    
            except Exception as e:
                logger.error(f"Failed to initialize audio playback: {e}")
                self.is_playing = False
                raise
    
        def _playback_audio_thread(self):
            """Audio playback thread - runs in background."""
            while self.is_playing:
                try:
                    # Get audio data from queue (blocking with timeout)
                    audio_data = self.audio_queue.get(timeout=0.1)
    
                    if audio_data and self.output_stream and self.is_playing:
                        self.output_stream.write(audio_data)
    
                except queue.Empty:
                    continue
                except Exception as e:
                    if self.is_playing:
                        logger.error(f"Error in audio playback: {e}")
                    break
    
        async def queue_audio(self, audio_data: bytes):
            """Queue audio data for playback."""
            if self.is_playing:
                self.audio_queue.put(audio_data)
    
        async def stop_playback(self):
            """Stop audio playback and clear queue."""
            if not self.is_playing:
                return
    
            self.is_playing = False
    
            # Clear the queue
            while not self.audio_queue.empty():
                try:
                    self.audio_queue.get_nowait()
                except queue.Empty:
                    break
    
            if self.output_stream:
                self.output_stream.stop_stream()
                self.output_stream.close()
                self.output_stream = None
    
            if self.playback_thread:
                self.playback_thread.join(timeout=1.0)
    
            logger.info("Stopped audio playback")
    
        async def cleanup(self):
            """Clean up audio resources."""
            await self.stop_capture()
            await self.stop_playback()
    
            if self.audio:
                self.audio.terminate()
    
            self.executor.shutdown(wait=True)
            logger.info("Audio processor cleaned up")
    
    
    class BasicVoiceAssistant:
        """Basic voice assistant implementing the VoiceLive SDK patterns."""
    
        def __init__(
            self,
            endpoint: str,
            credential: Union[AzureKeyCredential, TokenCredential],
            model: str,
            voice: str,
            instructions: str,
        ):
    
            self.endpoint = endpoint
            self.credential = credential
            self.model = model
            self.voice = voice
            self.instructions = instructions
            self.connection: Optional["VoiceLiveConnection"] = None
            self.audio_processor: Optional[AudioProcessor] = None
            self.session_ready = False
            self.conversation_started = False
    
        async def start(self):
            """Start the voice assistant session."""
            try:
                logger.info(f"Connecting to VoiceLive API with model {self.model}")
    
                # Connect to VoiceLive WebSocket API
                async with connect(
                    endpoint=self.endpoint,
                    credential=self.credential,
                    model=self.model,
                    connection_options={
                        "max_msg_size": 10 * 1024 * 1024,
                        "heartbeat": 20,
                        "timeout": 20,
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
                    await ap.start_playback()
    
                    logger.info("Voice assistant ready! Start speaking...")
                    print("\n" + "=" * 60)
                    print("🎤 VOICE ASSISTANT READY")
                    print("Start speaking to begin conversation")
                    print("Press Ctrl+C to exit")
                    print("=" * 60 + "\n")
    
                    # Process events
                    await self._process_events()
    
            except KeyboardInterrupt:
                logger.info("Received interrupt signal, shutting down...")
    
            except Exception as e:
                logger.error(f"Connection error: {e}")
                raise
    
            # Cleanup
            if self.audio_processor:
                await self.audio_processor.cleanup()
    
        async def _setup_session(self):
            """Configure the VoiceLive session for audio conversation."""
            logger.info("Setting up voice conversation session...")
    
            # Create strongly typed voice configuration
            voice_config: Union[AzureStandardVoice, str]
            if self.voice.startswith("en-US-") or self.voice.startswith("en-CA-") or "-" in self.voice:
                # Azure voice
                voice_config = AzureStandardVoice(name=self.voice, type="azure-standard")
            else:
                # OpenAI voice (alloy, echo, fable, onyx, nova, shimmer)
                voice_config = self.voice
    
            # Create strongly typed turn detection configuration
            turn_detection_config = ServerVad(threshold=0.5, prefix_padding_ms=300, silence_duration_ms=500)
    
            # Create strongly typed session configuration
            session_config = RequestSession(
                modalities=[Modality.TEXT, Modality.AUDIO],
                instructions=self.instructions,
                voice=voice_config,
                input_audio_format=AudioFormat.PCM16,
                output_audio_format=AudioFormat.PCM16,
                turn_detection=turn_detection_config,
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
    
            except KeyboardInterrupt:
                logger.info("Event processing interrupted")
            except Exception as e:
                logger.error(f"Error processing events: {e}")
                raise
    
        async def _handle_event(self, event):
            """Handle different types of events from VoiceLive."""
            logger.debug(f"Received event: {event.type}")
            ap = self.audio_processor
            conn = self.connection
            assert ap is not None, "AudioProcessor must be initialized"
            assert conn is not None, "Connection must be established"
    
            if event.type == ServerEventType.SESSION_UPDATED:
                logger.info(f"Session ready: {event.session.id}")
                self.session_ready = True
    
                # Start audio capture once session is ready
                await ap.start_capture()
    
            elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
                logger.info("🎤 User started speaking - stopping playback")
                print("🎤 Listening...")
    
                # Stop current assistant audio playback (interruption handling)
                await ap.stop_playback()
    
                # Cancel any ongoing response
                try:
                    await conn.response.cancel()
                except Exception as e:
                    logger.debug(f"No response to cancel: {e}")
    
            elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STOPPED:
                logger.info("🎤 User stopped speaking")
                print("🤔 Processing...")
    
                # Restart playback system for response
                await ap.start_playback()
    
            elif event.type == ServerEventType.RESPONSE_CREATED:
                logger.info("🤖 Assistant response created")
    
            elif event.type == ServerEventType.RESPONSE_AUDIO_DELTA:
                # Stream audio response to speakers
                logger.debug("Received audio delta")
                await ap.queue_audio(event.delta)
    
            elif event.type == ServerEventType.RESPONSE_AUDIO_DONE:
                logger.info("🤖 Assistant finished speaking")
                print("🎤 Ready for next input...")
    
            elif event.type == ServerEventType.RESPONSE_DONE:
                logger.info("✅ Response complete")
    
            elif event.type == ServerEventType.ERROR:
                logger.error(f"❌ VoiceLive error: {event.error.message}")
                print(f"Error: {event.error.message}")
    
            elif event.type == ServerEventType.CONVERSATION_ITEM_CREATED:
                logger.debug(f"Conversation item created: {event.item.id}")
    
            else:
                logger.debug(f"Unhandled event type: {event.type}")
    
    
    def parse_arguments():
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(
            description="Basic Voice Assistant using Azure VoiceLive SDK",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    
        parser.add_argument(
            "--api-key",
            help="Azure VoiceLive API key. If not provided, will use AZURE_VOICE_LIVE_API_KEY environment variable.",
            type=str,
            default=os.environ.get("AZURE_VOICE_LIVE_API_KEY"),
        )
    
        parser.add_argument(
            "--endpoint",
            help="Azure VoiceLive endpoint",
            type=str,
            default=os.environ.get("AZURE_VOICE_LIVE_ENDPOINT", "wss://api.voicelive.com/v1"),
        )
    
        parser.add_argument(
            "--model",
            help="VoiceLive model to use",
            type=str,
            default=os.environ.get("VOICE_LIVE_MODEL", "gpt-4o-realtime-preview"),
        )
    
        parser.add_argument(
            "--voice",
            help="Voice to use for the assistant",
            type=str,
            default=os.environ.get("VOICE_LIVE_VOICE", "en-US-AvaNeural"),
            choices=[
                "alloy",
                "echo",
                "fable",
                "onyx",
                "nova",
                "shimmer",
                "en-US-AvaNeural",
                "en-US-JennyNeural",
                "en-US-GuyNeural",
            ],
        )
    
        parser.add_argument(
            "--instructions",
            help="System instructions for the AI assistant",
            type=str,
            default=os.environ.get(
                "VOICE_LIVE_INSTRUCTIONS",
                "You are a helpful AI assistant. Respond naturally and conversationally. "
                "Keep your responses concise but engaging.",
            ),
        )
    
        parser.add_argument(
            "--use-token-credential", help="Use Azure token credential instead of API key", action="store_true"
        )
    
        parser.add_argument("--verbose", help="Enable verbose logging", action="store_true")
    
        return parser.parse_args()
    
    
    async def main():
        """Main function."""
        args = parse_arguments()
    
        # Set logging level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
    
        # Validate credentials
        if not args.api_key and not args.use_token_credential:
            print("❌ Error: No authentication provided")
            print("Please provide an API key using --api-key or set AZURE_VOICE_LIVE_API_KEY environment variable,")
            print("or use --use-token-credential for Azure authentication.")
            sys.exit(1)
    
        try:
            # Create client with appropriate credential
            credential: Union[AzureKeyCredential, TokenCredential]
            if args.use_token_credential:
                credential = InteractiveBrowserCredential()  # or DefaultAzureCredential() if needed
                logger.info("Using Azure token credential")
            else:
                credential = AzureKeyCredential(args.api_key)
                logger.info("Using API key credential")
    
            # Create and start voice assistant
            assistant = BasicVoiceAssistant(
                endpoint=args.endpoint,
                credential=credential,
                model=args.model,
                voice=args.voice,
                instructions=args.instructions,
            )
    
            # Setup signal handlers for graceful shutdown
            def signal_handler(sig, frame):
                logger.info("Received shutdown signal")
                raise KeyboardInterrupt()
    
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
    
            # Start the assistant
            await assistant.start()
    
        except KeyboardInterrupt:
            print("\n👋 Voice assistant shut down. Goodbye!")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    
    if __name__ == "__main__":
        # Check for required dependencies
        dependencies = {
            "pyaudio": "Audio processing",
            "azure.ai.voicelive": "Azure VoiceLive SDK",
            "azure.core": "Azure Core libraries",
        }
    
        missing_deps = []
        for dep, description in dependencies.items():
            try:
                __import__(dep.replace("-", "_"))
            except ImportError:
                missing_deps.append(f"{dep} ({description})")
    
        if missing_deps:
            print("❌ Missing required dependencies:")
            for dep in missing_deps:
                print(f"  - {dep}")
            print("\nInstall with: pip install azure-ai-voicelive pyaudio python-dotenv")
            sys.exit(1)
    
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
        asyncio.run(main())    
    ```

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the Python file.

    ```shell
    python voice-live-quickstart.py
    ```

1. The Voice Live API starts to return audio with the model's initial response. You can interrupt the model by speaking. Enter "q" to quit the conversation.

## Output

The output of the script is printed to the console. You see messages indicating the status of the connection, audio stream, and playback. The audio is played back through your speakers or headphones.

```text
Session created:  {"type": "session.update", "session": {"instructions": "You are a helpful AI assistant responding in natural, engaging language.","turn_detection": {"type": "azure_semantic_vad", "threshold": 0.3, "prefix_padding_ms": 200, "silence_duration_ms": 200, "remove_filler_words": false, "end_of_utterance_detection": {"model": "semantic_detection_v1", "threshold": 0.1, "timeout": 4}}, "input_audio_noise_reduction": {"type": "azure_deep_noise_suppression"}, "input_audio_echo_cancellation": {"type": "server_echo_cancellation"}, "voice": {"name": "en-US-Ava:DragonHDLatestNeural", "type": "azure-standard", "temperature": 0.8}}, "event_id": ""}
Starting the chat ...
Received event: {'session.created'}
Press 'q' and Enter to quit the chat.
Received event: {'session.updated'}
Received event: {'input_audio_buffer.speech_started'}
Received event: {'input_audio_buffer.speech_stopped'}
Received event: {'input_audio_buffer.committed'}
Received event: {'conversation.item.input_audio_transcription.completed'}
Received event: {'conversation.item.created'}
Received event: {'response.created'}
Received event: {'response.output_item.added'}
Received event: {'conversation.item.created'}
Received event: {'response.content_part.added'}
Received event: {'response.audio_transcript.delta'}
Received event: {'response.audio_transcript.delta'}
Received event: {'response.audio_transcript.delta'}
REDACTED FOR BREVITY
Received event: {'response.audio.delta'}
Received event: {'response.audio.delta'}
Received event: {'response.audio.delta'}
q
Received event: {'response.audio.delta'}
Received event: {'response.audio.delta'}
Received event: {'response.audio.delta'}
Received event: {'response.audio.delta'}
Received event: {'response.audio.delta'}
Quitting the chat...
Received event: {'response.audio.delta'}
Received event: {'response.audio.delta'}
REDACTED FOR BREVITY
Received event: {'response.audio.delta'}
Received event: {'response.audio.delta'}
Chat done.
```

The script that you ran creates a log file named `<timestamp>_voicelive.log` in the `logs` folder.

```python
logging.basicConfig(
    filename=f'logs/{timestamp}_voicelive.log',
    filemode="w",
    level=logging.DEBUG,
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s'
)
```

The log file contains information about the connection to the Voice Live API, including the request and response data. You can view the log file to see the details of the conversation.

```text
2025-05-09 06:56:06,821:websockets.client:DEBUG:= connection is CONNECTING
2025-05-09 06:56:07,101:websockets.client:DEBUG:> GET /voice-live/realtime?api-version=2025-05-01-preview&model=gpt-4o HTTP/1.1
<REDACTED FOR BREVITY>
2025-05-09 06:56:07,551:websockets.client:DEBUG:= connection is OPEN
2025-05-09 06:56:07,551:websockets.client:DEBUG:< TEXT '{"event_id":"event_5a7NVdtNBVX9JZVuPc9nYK","typ...es":null,"agent":null}}' [1475 bytes]
2025-05-09 06:56:07,552:websockets.client:DEBUG:> TEXT '{"type": "session.update", "session": {"turn_de....8}}, "event_id": null}' [551 bytes]
2025-05-09 06:56:07,557:__main__:INFO:Starting audio stream ...
2025-05-09 06:56:07,810:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAAEA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:07,824:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAAAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:07,844:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAAAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:07,874:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAAAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:07,874:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAAEA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:07,905:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...BAAAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:07,926:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAAAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:07,954:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAAAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:07,954:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...///7/", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:07,974:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...BAAAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:08,004:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAAAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:08,035:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAAAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:08,035:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAAAA", "event_id": ""}' [1346 bytes]
<REDACTED FOR BREVITY>
2025-05-09 06:56:42,957:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAP//", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:42,984:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...+/wAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,005:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": .../////", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,034:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...+////", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,034:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...CAAMA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,055:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...CAAIA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,084:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...BAAEA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,114:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...9//3/", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,114:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...DAAMA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,134:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...BAAIA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,165:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAAAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,184:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...+//7/", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,214:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": .../////", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,214:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...+/wAA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,245:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...BAAIA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,264:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...AAP//", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,295:websockets.client:DEBUG:> TEXT '{"type": "input_audio_buffer.append", "audio": ...BAAEA", "event_id": ""}' [1346 bytes]
2025-05-09 06:56:43,295:websockets.client:DEBUG:> CLOSE 1000 (OK) [2 bytes]
2025-05-09 06:56:43,297:websockets.client:DEBUG:= connection is CLOSING
2025-05-09 06:56:43,346:__main__:INFO:Audio stream closed.
2025-05-09 06:56:43,388:__main__:INFO:Playback done.
2025-05-09 06:56:44,512:websockets.client:DEBUG:< CLOSE 1000 (OK) [2 bytes]
2025-05-09 06:56:44,514:websockets.client:DEBUG:< EOF
2025-05-09 06:56:44,514:websockets.client:DEBUG:> EOF
2025-05-09 06:56:44,514:websockets.client:DEBUG:= connection is CLOSED
2025-05-09 06:56:44,514:websockets.client:DEBUG:x closing TCP connection
2025-05-09 06:56:44,514:asyncio:ERROR:Unclosed client session
client_session: <aiohttp.client.ClientSession object at 0x00000266DD8E5400>
```
