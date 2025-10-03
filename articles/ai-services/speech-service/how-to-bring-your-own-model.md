---
title: Bring Your Own Model (BYOM) with Voice Live API (Preview)
description: Learn how to integrate your own models with the Voice Live API using Bring Your Own Model (BYOM) capabilities in Azure AI Speech Service.
author: PatrickFarley
ms.author: pafarley
ms.date: 09/26/2025
ms.topic: how-to
ms.service: azure-ai-speech
ms.custom: ai-speech, voice-live, byom, preview
---

# Bring Your Own Model (BYOM) with Voice Live API (Preview)

[!INCLUDE [preview-generic](includes/previews/preview-generic.md)]

The Voice Live API provides Bring Your Own Model (BYOM) capabilities, allowing you to integrate your custom models into the voice interaction workflow. BYOM is useful for the following scenarios:

- **Fine-tuned models**: Use your custom Azure OpenAI or Azure Foundry models
- **Provisioned throughput**: Use your PTU (Provisioned Throughput Units) deployments for consistent performance
- **Content safety**: Apply customized content safety configurations with your LLM

> [!IMPORTANT]
> You can integrate any model that's deployed in the same Azure Foundry resource you're using to call the Voice Live API.

> [!TIP]
> When you use your own model deployment with Voice Live, we recommend you set its content filtering configuration to [Asynchronous filtering](/azure/ai-foundry/openai/concepts/content-streaming#asynchronous-filtering) to reduce latency. Content filtering settings can be configured in the [Azure AI Foundry portal](https://ai.azure.com/).

## Authentication setup

When using Microsoft Entra ID authentication with Voice Live API, in `byom-azure-openai-chat-completion` mode specifically, you need to configure proper permissions for your Foundry resource. Since tokens may expire during long sessions, the system-assigned managed identity of the Foundry resource requires access to model deployments for the `byom-azure-openai-chat-completion` BYOM mode.

Run the following Azure CLI commands to configure the necessary permissions:

```bash
export subscription_id=<your-subscription-id>
export resource_group=<your-resource-group>
export foundry_resource=<your-foundry-resource>

# Enable system-assigned managed identity for the foundry resource
az cognitiveservices account identity assign --name ${foundry_resource} --resource-group ${resource_group} --subscription ${subscription_id}

# Get the system-assigned managed identity object ID
identity_principal_id=$(az cognitiveservices account show --name ${foundry_resource} --resource-group ${resource_group} --subscription ${subscription_id} --query "identity.principalId" -o tsv)

# Assign the Azure AI User role to the system identity of the foundry resource
az role assignment create --assignee-object-id ${identity_principal_id} --role "Azure AI User" --scope /subscriptions/${subscription_id}/resourceGroups/${resource_group}/providers/Microsoft.CognitiveServices/accounts/${foundry_resource}
```


## Choose BYOM integration mode

The Voice Live API supports two BYOM integration modes:

| Mode     | Description           | Example Models |
| ------- | ------------------ | ------------- |
| `byom-azure-openai-realtime`        | Azure OpenAI realtime models for streaming voice interactions              | `gpt-realtime`, `gpt-4o-realtime-preview` |
| `byom-azure-openai-chat-completion` | Azure OpenAI chat completion models for text-based interactions. Also applies to other Foundry models | `gpt-4.1`, `gpt-5-chat`, `grok-3`         |

## Integrate BYOM

#### [REST API call](#tab/rest)

Update the endpoint URL in your API call to include your BYOM configuration:

```curl
wss://<your-foundry-resource>.cognitiveservices.azure.com/voice-live/realtime?api-version=2025-10-01&profile=<your-byom-mode>&model=<your-model-deployment>
```

Get the `<your-model-deployment>` value from the AI Foundry portal. It corresponds to the name you gave the model at deployment time.


#### [Python SDK](#tab/sdk)

Use the [Python SDK quickstart code](/azure/ai-services/speech-service/voice-live-quickstart?tabs=windows%2Ckeyless&pivots=programming-language-python) to start a voice conversation, and make the following changes to enable BYOM:

1. In the `parse_arguments()` function, add a new argument for the BYOM profile type:
   
   ```python
   parser.add_argument(
        "--byom",
        help="BYOM (Bring Your Own Model) profile type",
        type=str,
        choices=["byom-azure-openai-realtime", "byom-azure-openai-chat-completion"],
        default=os.environ.get("VOICELIVE_BYOM_MODE", "byom-azure-openai-chat-completion"),

    )
   ```

1. In the `BasicVoiceAssistant` class, add the `byom` field:

    ```python
    class BasicVoiceAssistant:
    """Basic voice assistant implementing the VoiceLive SDK patterns."""

    def __init__(
        self,
        endpoint: str,
        credential: Union[AzureKeyCredential, TokenCredential],
        model: str,
        voice: str,
        instructions: str,
        byom: Literal["byom-azure-openai-realtime", "byom-azure-openai-chat-completion"] | None = None
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
        self.byom = byom

    async def start(self):
        """Start the voice assistant session."""
        try:
            logger.info(f"Connecting to VoiceLive API with model {self.model}")

            # Connect to VoiceLive WebSocket API
            async with connect(
                endpoint=self.endpoint,
                credential=self.credential,
                model=self.model,
                query={
                    "profile": self.byom
                } if self.byom else None
            ) as connection:
            ...
    ```
1. When you run the code, specify the `--byom` argument along with the `--model` argument to indicate the BYOM profile and model deployment you want to use. For example:

    ```shell
    python voice-live-quickstart.py --byom "byom-azure-openai-chat-completion" --model "gpt-4o"
    ```

---
<!--
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
from typing import Literal, Union, Optional, TYPE_CHECKING, cast, Literal
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
        byom: Literal["byom-azure-openai-realtime", "byom-azure-openai-chat-completion"] | None = None
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
        self.byom = byom

    async def start(self):
        """Start the voice assistant session."""
        try:
            logger.info(f"Connecting to VoiceLive API with model {self.model}")

            # Connect to VoiceLive WebSocket API
            async with connect(
                endpoint=self.endpoint,
                credential=self.credential,
                model=self.model,
                query={
                    "profile": self.byom
                } if self.byom else None
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
        help="Azure VoiceLive API key. If not provided, will use AZURE_VOICELIVE_API_KEY environment variable.",
        type=str,
        default=os.environ.get("AZURE_VOICELIVE_API_KEY"),
    )

    parser.add_argument(
        "--endpoint",
        help="Azure VoiceLive endpoint",
        type=str,
        default=os.environ.get("AZURE_VOICELIVE_ENDPOINT", "wss://api.voicelive.com/v1"),
    )

    parser.add_argument(
        "--model",
        help="VoiceLive model to use",
        type=str,
        default=os.environ.get("VOICELIVE_MODEL", "gpt-4o-realtime-preview"),
    )

    parser.add_argument(
        "--voice",
        help="Voice to use for the assistant",
        type=str,
        default=os.environ.get("VOICELIVE_VOICE", "en-US-AvaNeural"),
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
            "VOICELIVE_INSTRUCTIONS",
            "You are a helpful AI assistant. Respond naturally and conversationally. "
            "Keep your responses concise but engaging.",
        ),
    )

    parser.add_argument(
        "--use-token-credential", help="Use Azure token credential instead of API key", action="store_true"
    )

    parser.add_argument(
        "--byom",
        help="BYOM (Bring Your Own Model) profile type",
        type=str,
        choices=["byom-azure-openai-realtime", "byom-azure-openai-chat-completion"],
        default=os.environ.get("VOICELIVE_BYOM_MODE", "byom-azure-openai-chat-completion"),

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
        print("Please provide an API key using --api-key or set AZURE_VOICELIVE_API_KEY environment variable,")
        print("or use --use-token-credential for Azure authentication.")
        sys.exit(1)

    try:
        # Create client with appropriate credential
        credential: Union[AzureKeyCredential, TokenCredential]
        if args.use_token_credential:
            # credential = InteractiveBrowserCredential()  # or DefaultAzureCredential() if needed
            credential = DefaultAzureCredential()
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
            byom=args.byom,
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
-->