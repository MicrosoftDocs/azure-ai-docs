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

In this article, you learn how to use Voice Live with [Microsoft Foundry models](/azure/ai-foundry/concepts/foundry-models-overview) using the VoiceLive SDK for Python.

[!INCLUDE [Header](../../common/voice-live-python.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.10 or later version</a>. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see [Region support](/azure/ai-services/speech-service/regions).

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
    > We recommend that you create and activate a new Python environment to use to install the packages you need for this tutorial. Don't install packages into your global python installation. You should always use a virtual or conda environment when installing python packages, otherwise you can break your global installation of Python.

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

The sample code in this quickstart uses either Microsoft Entra ID or an API key for authentication. You can set the script argument to be either your API key or your access token.

1. Create the `voice-live-quickstart.py` file with the following code:

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
        """Basic voice assistant implementing the VoiceLive SDK patterns."""

        def __init__(
            self,
            endpoint: str,
            credential: Union[AzureKeyCredential, AsyncTokenCredential],
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
            self._active_response = False
            self._response_api_done = False

        async def start(self):
            """Start the voice assistant session."""
            try:
                logger.info("Connecting to VoiceLive API with model %s", self.model)

                # Connect to VoiceLive WebSocket API
                async with connect(
                    endpoint=self.endpoint,
                    credential=self.credential,
                    model=self.model,
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
                instructions=self.instructions,
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
                self.session_ready = True

                # Start audio capture once session is ready
                ap.start_capture()

            elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
                logger.info("User started speaking - stopping playback")
                print("🎤 Listening...")

                ap.skip_pending_audio()

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
            "--model",
            help="VoiceLive model to use",
            type=str,
            default=os.environ.get("AZURE_VOICELIVE_MODEL", "gpt-realtime"),
        )

        parser.add_argument(
            "--voice",
            help="Voice to use for the assistant. E.g. alloy, echo, fable, en-US-AvaNeural, en-US-GuyNeural",
            type=str,
            default=os.environ.get("AZURE_VOICELIVE_VOICE", "en-US-Ava:DragonHDLatestNeural"),
        )

        parser.add_argument(
            "--instructions",
            help="System instructions for the AI assistant",
            type=str,
            default=os.environ.get(
                "AZURE_VOICELIVE_INSTRUCTIONS",
                "You are a helpful AI assistant. Respond naturally and conversationally. "
                "Keep your responses concise but engaging.",
            ),
        )

        parser.add_argument(
            "--use-token-credential", help="Use Azure token credential instead of API key", action="store_true", default=False
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
            model=args.model,
            voice=args.voice,
            instructions=args.instructions,
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
    python voice-live-quickstart.py --use-token-credential
    ```

1. The Voice Live API starts to return audio with the model's initial response. You can interrupt the model by speaking. Enter "Ctrl+C" to quit the conversation.

## Output

The output of the script is printed to the console. You see messages indicating the status of system. The audio is played back through your speakers or headphones.

```console
============================================================
🎤 VOICE ASSISTANT READY
Start speaking to begin conversation
Press Ctrl+C to exit
============================================================

🎤 Listening...
🤔 Processing...
🎤 Ready for next input...
🎤 Listening...
🤔 Processing...
🎤 Ready for next input...
🎤 Listening...
🤔 Processing...
🎤 Ready for next input...
🎤 Listening...
🤔 Processing...
🎤 Listening...
🎤 Ready for next input...
🤔 Processing...
🎤 Ready for next input...
```

The script that you ran creates a log file named `<timestamp>_voicelive.log` in the `logs` folder.

The default loglevel is set to **INFO** but you can change it by running the quickstart with the command line parameter `--verbose` or by changing the logging config within the code as follows:

```python
logging.basicConfig(
    filename=f'logs/{timestamp}_voicelive.log',
    filemode="w",
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    level=logging.INFO
)
```

The log file contains information about the connection to the Voice Live API, including the request and response data. You can view the log file to see the details of the conversation.

```text
2025-10-02 14:47:37,901:__main__:INFO:Using Azure token credential
2025-10-02 14:47:37,901:__main__:INFO:Connecting to VoiceLive API with model gpt-realtime
2025-10-02 14:47:37,901:azure.core.pipeline.policies.http_logging_policy:INFO:Request URL: 'https://login.microsoftonline.com/organizations/v2.0/.well-known/openid-configuration'
Request method: 'GET'
Request headers:
    'User-Agent': 'azsdk-python-identity/1.22.0 Python/3.11.9 (Windows-10-10.0.26200-SP0)'
No body was attached to the request
2025-10-02 14:47:38,057:azure.core.pipeline.policies.http_logging_policy:INFO:Response status: 200
Response headers:
    'Date': 'Thu, 02 Oct 2025 21:47:37 GMT'
    'Content-Type': 'application/json; charset=utf-8'
    'Content-Length': '1641'
    'Connection': 'keep-alive'
    'Cache-Control': 'max-age=86400, private'
    'Strict-Transport-Security': 'REDACTED'
    'X-Content-Type-Options': 'REDACTED'
    'Access-Control-Allow-Origin': 'REDACTED'
    'Access-Control-Allow-Methods': 'REDACTED'
    'P3P': 'REDACTED'
    'x-ms-request-id': 'f81adfa1-8aa3-4ab6-a7b8-908f411e0d00'
    'x-ms-ests-server': 'REDACTED'
    'x-ms-srs': 'REDACTED'
    'Content-Security-Policy-Report-Only': 'REDACTED'
    'Cross-Origin-Opener-Policy-Report-Only': 'REDACTED'
    'Reporting-Endpoints': 'REDACTED'
    'X-XSS-Protection': 'REDACTED'
    'Set-Cookie': 'REDACTED'
    'X-Cache': 'REDACTED'
2025-10-02 14:47:42,105:azure.core.pipeline.policies.http_logging_policy:INFO:Request URL: 'https://login.microsoftonline.com/organizations/oauth2/v2.0/token'
Request method: 'POST'
Request headers:
    'Accept': 'application/json'
    'x-client-sku': 'REDACTED'
    'x-client-ver': 'REDACTED'
    'x-client-os': 'REDACTED'
    'x-ms-lib-capability': 'REDACTED'
    'client-request-id': 'REDACTED'
    'x-client-current-telemetry': 'REDACTED'
    'x-client-last-telemetry': 'REDACTED'
    'X-AnchorMailbox': 'REDACTED'
    'User-Agent': 'azsdk-python-identity/1.22.0 Python/3.11.9 (Windows-10-10.0.26200-SP0)'
A body is sent with the request
2025-10-02 14:47:42,466:azure.core.pipeline.policies.http_logging_policy:INFO:Response status: 200
Response headers:
    'Date': 'Thu, 02 Oct 2025 21:47:42 GMT'
    'Content-Type': 'application/json; charset=utf-8'
    'Content-Length': '6587'
    'Connection': 'keep-alive'
    'Cache-Control': 'no-store, no-cache'
    'Pragma': 'no-cache'
    'Expires': '-1'
    'Strict-Transport-Security': 'REDACTED'
    'X-Content-Type-Options': 'REDACTED'
    'P3P': 'REDACTED'
    'client-request-id': 'REDACTED'
    'x-ms-request-id': '2e82e728-22c0-4568-b3ed-f00ec79a2500'
    'x-ms-ests-server': 'REDACTED'
    'x-ms-clitelem': 'REDACTED'
    'x-ms-srs': 'REDACTED'
    'Content-Security-Policy-Report-Only': 'REDACTED'
    'Cross-Origin-Opener-Policy-Report-Only': 'REDACTED'
    'Reporting-Endpoints': 'REDACTED'
    'X-XSS-Protection': 'REDACTED'
    'Set-Cookie': 'REDACTED'
    'X-Cache': 'REDACTED'
2025-10-02 14:47:42,467:azure.identity._internal.interactive:INFO:InteractiveBrowserCredential.get_token succeeded
2025-10-02 14:47:42,884:__main__:INFO:AudioProcessor initialized with 24kHz PCM16 mono audio
2025-10-02 14:47:42,884:__main__:INFO:Setting up voice conversation session...
2025-10-02 14:47:42,887:__main__:INFO:Session configuration sent
2025-10-02 14:47:42,943:__main__:INFO:Audio playback system ready
2025-10-02 14:47:42,943:__main__:INFO:Voice assistant ready! Start speaking...
2025-10-02 14:47:42,975:__main__:INFO:Session ready: sess_CMLRGjWnakODcHn583fXf
2025-10-02 14:47:42,994:__main__:INFO:Started audio capture
2025-10-02 14:47:47,513:__main__:INFO:\U0001f3a4 User started speaking - stopping playback
2025-10-02 14:47:47,593:__main__:INFO:Stopped audio playback
2025-10-02 14:47:51,757:__main__:INFO:\U0001f3a4 User stopped speaking
2025-10-02 14:47:51,813:__main__:INFO:Audio playback system ready
2025-10-02 14:47:51,816:__main__:INFO:\U0001f916 Assistant response created
2025-10-02 14:47:58,009:__main__:INFO:\U0001f916 Assistant finished speaking
2025-10-02 14:47:58,009:__main__:INFO:\u2705 Response complete
2025-10-02 14:48:07,309:__main__:INFO:Received shutdown signal
```
