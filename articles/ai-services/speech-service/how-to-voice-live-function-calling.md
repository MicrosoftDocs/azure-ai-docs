---
title: Function Calling with Voice Live API
description: Learn how to do function calling scenarios in a voice session using the Voice Live API.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: quickstart
ms.date: 11/06/2025
---

# Quickstart: Use function calling in a Voice Live session

[!INCLUDE [Header](./includes/common/voice-live-python.md)]

The Voice Live API supports function calling in voice conversations. This allows you to create voice assistants that can call external functions to get real-time information and include that information in their spoken responses.

## Implementation steps

The code sample below does these basic steps to set up function calling.

1. **Write backend functions**: Define Python callables that fulfill business tasks (time lookup, weather, database queries) and serialize outputs to JSON-friendly dictionaries.

1. **Describe tools for Voice Live**: Create **FunctionTool** definitions with names, parameter schemas, and text descriptions, and bundle them into the session configuration so the model understands the available actions.

1. **Initialize the session**: Connect using `azure.ai.voicelive.aio.connect`, provide credentials, pass in the defined **FunctionTool**, choose your target model/voice, and enable audio modalities, transcription, and turn detection.

1. **Start audio processing**: Spin up **AudioProcessor** to capture microphone input, encode it (PCM16, 24 kHz), and stream it to the Voice Live connection; simultaneously prepare playback for assistant audio responses.

1. **Run the event loop**: Await Voice Live events, updating session state, reacting to user speech boundaries, and streaming the assistant's audio/text back to the user interface. When a **ResponseFunctionCallItem** arrives, the application locates the callable, executes it with parsed arguments, packages the result into a **FunctionCallOutputItem**, and sends it back so the assistant can finalize its reply.

## Sample code

The following examples show async function calling with the Voice Live API. Before running either sample, complete the setup steps in the [Quickstart](/azure/ai-services/speech-service/voice-live-quickstart).

#### [Python](#tab/python)

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
import json
import base64
from datetime import datetime
import logging
import queue
import signal
from typing import Union, Optional, Dict, Any, Mapping, Callable, TYPE_CHECKING, cast

from azure.core.credentials import AzureKeyCredential
from azure.core.credentials_async import AsyncTokenCredential
from azure.identity.aio import AzureCliCredential, DefaultAzureCredential

from azure.ai.voicelive.aio import connect
from azure.ai.voicelive.models import (
    AudioEchoCancellation,
    AudioNoiseReduction,
    AzureStandardVoice,
    InputAudioFormat,
    ItemType,
    Modality,
    OutputAudioFormat,
    RequestSession,
    ServerEventType,
    ServerVad,
    FunctionTool,
    FunctionCallOutputItem,
    ToolChoiceLiteral,
    AudioInputTranscriptionOptions,
    Tool,
)
from dotenv import load_dotenv
import pyaudio

if TYPE_CHECKING:
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



class AsyncFunctionCallingClient:
    """Voice assistant with function calling capabilities using VoiceLive SDK patterns."""

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
        self.conversation_started = False
        self._active_response = False
        self._response_api_done = False
        self._pending_function_call: Optional[Dict[str, Any]] = None

        # Define available functions
        self.available_functions: Dict[str, Callable[[Union[str, Mapping[str, Any]]], Mapping[str, Any]]] = {
            "get_current_time": self.get_current_time,
            "get_current_weather": self.get_current_weather,
        }

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

                logger.info("Voice assistant with function calling ready! Start speaking...")
                print("\n" + "=" * 60)
                print("🎤 VOICE ASSISTANT WITH FUNCTION CALLING READY")
                print("Try saying:")
                print("  • 'What's the current time?'")
                print("  • 'What's the weather in Seattle?'")
                print("Press Ctrl+C to exit")
                print("=" * 60 + "\n")

                # Process events
                await self._process_events()
        finally:
            if self.audio_processor:
                self.audio_processor.shutdown()

    async def _setup_session(self):
        """Configure the VoiceLive session for audio conversation with function tools."""
        logger.info("Setting up voice conversation session with function tools...")

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

        # Define function tools
        function_tools: list[Tool] = [
            FunctionTool(
                name="get_current_time",
                description="Get the current time",
                parameters={
                    "type": "object",
                    "properties": {
                        "timezone": {
                            "type": "string",
                            "description": "The timezone to get the current time for, e.g., 'UTC', 'local'",
                        }
                    },
                    "required": [],
                },
            ),
            FunctionTool(
                name="get_current_weather",
                description="Get the current weather in a given location",
                parameters={
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g., 'San Francisco, CA'",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The unit of temperature to use (celsius or fahrenheit)",
                        },
                    },
                    "required": ["location"],
                },
            ),
        ]

        # Create session configuration with function tools
        session_config = RequestSession(
            modalities=[Modality.TEXT, Modality.AUDIO],
            instructions=self.instructions,
            voice=voice_config,
            input_audio_format=InputAudioFormat.PCM16,
            output_audio_format=OutputAudioFormat.PCM16,
            turn_detection=turn_detection_config,
            input_audio_echo_cancellation=AudioEchoCancellation(),
            input_audio_noise_reduction=AudioNoiseReduction(type="azure_deep_noise_suppression"),
            tools=function_tools,
            tool_choice=ToolChoiceLiteral.AUTO,
            input_audio_transcription=AudioInputTranscriptionOptions(model="whisper-1"),
        )

        conn = self.connection
        assert conn is not None, "Connection must be established before setting up session"
        await conn.session.update(session=session_config)

        logger.info("Session configuration with function tools sent")

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

            # Proactive greeting
            if not self.conversation_started:
                self.conversation_started = True
                logger.info("Sending proactive greeting request")
                try:
                    await conn.response.create()

                except Exception:
                    logger.exception("Failed to send proactive greeting request")

            # Start audio capture once session is ready
            ap.start_capture()

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

            # Execute pending function call if arguments are ready
            if self._pending_function_call and "arguments" in self._pending_function_call:
                await self._execute_function_call(self._pending_function_call)
                self._pending_function_call = None

        elif event.type == ServerEventType.ERROR:
            msg = event.error.message
            if "Cancellation failed: no active response" in msg:
                logger.debug("Benign cancellation error: %s", msg)
            else:
                logger.error("❌ VoiceLive error: %s", msg)
                print(f"Error: {msg}")

        elif event.type == ServerEventType.CONVERSATION_ITEM_CREATED:
            logger.debug("Conversation item created: %s", event.item.id)

            if event.item.type == ItemType.FUNCTION_CALL:
                function_call_item = event.item
                self._pending_function_call = {
                    "name": function_call_item.name,
                    "call_id": function_call_item.call_id,
                    "previous_item_id": function_call_item.id
                }
                print(f"🔧 Calling function: {function_call_item.name}")
                logger.info(f"Function call detected: {function_call_item.name} with call_id: {function_call_item.call_id}")

        elif event.type == ServerEventType.RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE:
            if self._pending_function_call and event.call_id == self._pending_function_call["call_id"]:
                logger.info(f"Function arguments received: {event.arguments}")
                self._pending_function_call["arguments"] = event.arguments

    async def _execute_function_call(self, function_call_info):
        """Execute a function call and send the result back to the conversation."""
        conn = self.connection
        assert conn is not None, "Connection must be established"
        
        function_name = function_call_info["name"]
        call_id = function_call_info["call_id"]
        previous_item_id = function_call_info["previous_item_id"]
        arguments = function_call_info["arguments"]

        try:
            if function_name in self.available_functions:
                logger.info(f"Executing function: {function_name}")
                result = self.available_functions[function_name](arguments)

                function_output = FunctionCallOutputItem(call_id=call_id, output=json.dumps(result))

                # Send result back to conversation
                await conn.conversation.item.create(previous_item_id=previous_item_id, item=function_output)
                logger.info(f"Function result sent: {result}")
                print(f"✅ Function {function_name} completed")

                # Request new response to process the function result
                await conn.response.create()
                logger.info("Requested new response with function result")

            else:
                logger.error(f"Unknown function: {function_name}")

        except Exception as e:
            logger.error(f"Error executing function {function_name}: {e}")

    def get_current_time(self, arguments: Optional[Union[str, Mapping[str, Any]]] = None) -> Dict[str, Any]:
        """Get the current time."""
        from datetime import datetime, timezone
        
        if isinstance(arguments, str):
            try:
                args = json.loads(arguments)
            except json.JSONDecodeError:
                args = {}
        else:
            args = arguments if isinstance(arguments, dict) else {}

        timezone_arg = args.get("timezone", "local")
        now = datetime.now()

        if timezone_arg.lower() == "utc":
            now = datetime.now(timezone.utc)
            timezone_name = "UTC"
        else:
            timezone_name = "local"

        formatted_time = now.strftime("%I:%M:%S %p")
        formatted_date = now.strftime("%A, %B %d, %Y")

        return {"time": formatted_time, "date": formatted_date, "timezone": timezone_name}

    def get_current_weather(self, arguments: Union[str, Mapping[str, Any]]):
        """Get the current weather for a location."""
        if isinstance(arguments, str):
            try:
                args = json.loads(arguments)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse weather arguments: {arguments}")
                return {"error": "Invalid arguments"}
        else:
            args = arguments if isinstance(arguments, dict) else {}

        location = args.get("location", "Unknown")
        unit = args.get("unit", "celsius")

        # Simulated weather response
        try:
            return {
                "location": location,
                "temperature": 22 if unit == "celsius" else 72,
                "unit": unit,
                "condition": "Partly Cloudy",
                "humidity": 65,
                "wind_speed": 10,
            }
        except Exception as e:
            logger.error(f"Error getting weather: {e}")
            return {"error": str(e)}


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Voice Assistant with Function Calling using Azure VoiceLive SDK",
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
            "You are a helpful AI assistant with access to functions. "
            "Use the functions when appropriate to provide accurate, real-time information. "
            "If you are asked about the weather, please respond with 'I will get the weather for you. Please wait a moment.' and then call the get_current_weather function. "
            "If you are asked about the time, please respond with 'I will get the time for you. Please wait a moment.' and then call the get_current_time function. "
            "Explain when you're using a function and include the results in your response naturally. Always start the conversation in English.",
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
        credential = AzureCliCredential()
        logger.info("Using Azure token credential")
    else:
        credential = AzureKeyCredential(args.api_key)
        logger.info("Using API key credential")

    # Create and start voice assistant with function calling
    client = AsyncFunctionCallingClient(
        endpoint=args.endpoint,
        credential=credential,
        model=args.model,
        voice=args.voice,
        instructions=args.instructions,
    )

    # Signal handlers for graceful shutdown
    def signal_handler(_sig, _frame):
        logger.info("Received shutdown signal")
        raise KeyboardInterrupt()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        asyncio.run(client.start())
    except KeyboardInterrupt:
        print("\n👋 Voice assistant shut down. Goodbye!")
    except Exception as e:
        logger.exception("Fatal error")
        print(f"Fatal Error: {e}")
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

    print("🎙️  Voice Assistant with Function Calling - Azure VoiceLive SDK")
    print("=" * 65)

    # Run the assistant
    main()
```

#### [C#](#tab/csharp)

Install the required packages:

```dotnetcli
dotnet add package Azure.AI.VoiceLive
dotnet add package Azure.Identity
dotnet add package NAudio
```

```csharp
// -------------------------------------------------------------------------
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
// -------------------------------------------------------------------------
using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Azure.AI.VoiceLive;
using Azure.Core;
using Azure.Identity;
using Microsoft.Extensions.Logging;
using NAudio.Wave;

// ---------------------------------------------------------------------------
// Program entry point
// ---------------------------------------------------------------------------
var endpoint = Environment.GetEnvironmentVariable("AZURE_VOICELIVE_ENDPOINT")
    ?? "https://<your-resource-name>.services.ai.azure.com/";
var model = Environment.GetEnvironmentVariable("AZURE_VOICELIVE_MODEL") ?? "gpt-realtime";
var voice = Environment.GetEnvironmentVariable("AZURE_VOICELIVE_VOICE") ?? "en-US-Ava:DragonHDLatestNeural";
var instructions = Environment.GetEnvironmentVariable("AZURE_VOICELIVE_INSTRUCTIONS")
    ?? "You are a helpful AI assistant with access to functions. "
     + "Use the functions when appropriate to provide accurate, real-time information. "
     + "If asked about the weather, call the get_current_weather function. "
     + "If asked about the time, call the get_current_time function. "
     + "Always start the conversation in English.";

using var cts = new CancellationTokenSource();
Console.CancelKeyPress += (_, e) => { e.Cancel = true; cts.Cancel(); };

using var loggerFactory = LoggerFactory.Create(b => b.AddConsole());
var logger = loggerFactory.CreateLogger<FunctionCallingClient>();

var client = new FunctionCallingClient(
    endpoint,
    new DefaultAzureCredential(),
    model,
    voice,
    instructions,
    logger);

try
{
    await client.StartAsync(cts.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("\nVoice assistant shut down. Goodbye!");
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Fatal error: {ex.Message}");
    return 1;
}
return 0;

/// <summary>
/// Handles real-time audio capture and playback for the voice assistant.
/// Threading architecture mirrors the Python equivalent:
/// - Capture: WaveInEvent callbacks stream microphone audio to VoiceLive.
/// - Playback: BufferedWaveProvider feeds a WaveOutEvent output stream.
/// </summary>
public sealed class AudioProcessor : IDisposable
{
    private readonly VoiceLiveSession _connection;
    private readonly ILogger _logger;
    // PCM16, 24 kHz, mono -- matches the Python AudioProcessor configuration.
    private readonly WaveFormat _waveFormat = new WaveFormat(24000, 16, 1);
    private WaveInEvent? _waveIn;
    private WaveOutEvent? _waveOut;
    private BufferedWaveProvider? _bufferedProvider;

    public AudioProcessor(VoiceLiveSession connection, ILogger logger)
    {
        _connection = connection;
        _logger = logger;
        _logger.LogInformation("AudioProcessor initialized with 24 kHz PCM16 mono audio");
    }

    /// <summary>Starts capturing audio from the default microphone.</summary>
    public void StartCapture()
    {
        _waveIn = new WaveInEvent
        {
            WaveFormat = _waveFormat,
            BufferMilliseconds = 50  // 50 ms chunks, matching Python chunk_size = 1200 frames
        };

        _waveIn.DataAvailable += async (_, e) =>
        {
            var audioBytes = new byte[e.BytesRecorded];
            Array.Copy(e.Buffer, audioBytes, e.BytesRecorded);
            await _connection.SendInputAudioAsync(audioBytes);
        };

        _waveIn.StartRecording();
        _logger.LogInformation("Started audio capture");
    }

    /// <summary>Initializes the audio playback pipeline.</summary>
    public void StartPlayback()
    {
        _bufferedProvider = new BufferedWaveProvider(_waveFormat)
        {
            // Large buffer avoids discarding mid-response audio when the AI
            // speaks for more than the default ~5 seconds.
            BufferDuration = TimeSpan.FromSeconds(60),
            // Don't silently drop audio — we explicitly call ClearBuffer()
            // for barge-in cancellation instead.
            DiscardOnBufferOverflow = false
        };

        _waveOut = new WaveOutEvent
        {
            // Larger latency window gives more tolerance for bursty delta
            // packet arrival and prevents hardware buffer underruns.
            DesiredLatency = 200,
            NumberOfBuffers = 4
        };
        _waveOut.Init(_bufferedProvider);
        _waveOut.Play();
        _logger.LogInformation("Audio playback system ready");
    }

    /// <summary>Queues decoded PCM audio data for playback.</summary>
    public void QueueAudio(byte[]? audioData)
    {
        if (audioData is { Length: > 0 } && _bufferedProvider is not null)
            _bufferedProvider.AddSamples(audioData, 0, audioData.Length);
    }

    /// <summary>Discards buffered playback audio (barge-in cancellation).</summary>
    public void SkipPendingAudio() => _bufferedProvider?.ClearBuffer();

    public void Dispose()
    {
        _waveIn?.StopRecording();
        _waveIn?.Dispose();
        _waveOut?.Stop();
        _waveOut?.Dispose();
        _logger.LogInformation("Audio processor cleaned up");
    }
}

/// <summary>Voice assistant with function calling capabilities.</summary>
public sealed class FunctionCallingClient
{
    private readonly string _endpoint;
    private readonly TokenCredential _credential;
    private readonly string _model;
    private readonly string _voice;
    private readonly string _instructions;
    private readonly ILogger<FunctionCallingClient> _logger;

    private VoiceLiveSession? _connection;
    private AudioProcessor? _audioProcessor;
    private bool _sessionReady;
    private bool _conversationStarted;
    private bool _activeResponse;
    private bool _responseApiDone;
    private Dictionary<string, object>? _pendingFunctionCall;

    private readonly Dictionary<string, Func<JsonElement, Dictionary<string, object>>> _availableFunctions;

    public FunctionCallingClient(
        string endpoint,
        TokenCredential credential,
        string model,
        string voice,
        string instructions,
        ILogger<FunctionCallingClient> logger)
    {
        _endpoint = endpoint;
        _credential = credential;
        _model = model;
        _voice = voice;
        _instructions = instructions;
        _logger = logger;

        _availableFunctions = new Dictionary<string, Func<JsonElement, Dictionary<string, object>>>
        {
            ["get_current_time"] = GetCurrentTime,
            ["get_current_weather"] = GetCurrentWeather,
        };
    }

    public async Task StartAsync(CancellationToken cancellationToken = default)
    {
        _logger.LogInformation("Connecting to VoiceLive API with model {Model}", _model);

        var client = new VoiceLiveClient(new Uri(_endpoint), _credential);

        await using var connection = await client.StartSessionAsync(_model, cancellationToken);
        _connection = connection;

        using var audioProcessor = new AudioProcessor(connection, _logger);
        _audioProcessor = audioProcessor;

        await SetupSessionAsync();
        audioProcessor.StartPlayback();

        Console.WriteLine(new string('=', 60));
        Console.WriteLine("VOICE ASSISTANT WITH FUNCTION CALLING READY");
        Console.WriteLine("Try saying:");
        Console.WriteLine("  - 'What''s the current time?'");
        Console.WriteLine("  - 'What''s the weather in Seattle?'");
        Console.WriteLine("Press Ctrl+C to exit");
        Console.WriteLine(new string('=', 60));

        await ProcessEventsAsync(cancellationToken);
    }

    private async Task SetupSessionAsync()
    {
        _logger.LogInformation("Setting up voice conversation session with function tools...");

        var getTimeFunction = new VoiceLiveFunctionDefinition("get_current_time")
        {
            Description = "Get the current time",
            Parameters = BinaryData.FromObjectAsJson(new
            {
                type = "object",
                properties = new
                {
                    timezone = new
                    {
                        type = "string",
                        description = "The timezone to get the current time for, e.g., 'UTC', 'local'"
                    }
                },
                required = Array.Empty<string>()
            })
        };

        var getWeatherFunction = new VoiceLiveFunctionDefinition("get_current_weather")
        {
            Description = "Get the current weather in a given location",
            Parameters = BinaryData.FromObjectAsJson(new
            {
                type = "object",
                properties = new
                {
                    location = new
                    {
                        type = "string",
                        description = "The city and state, e.g., 'San Francisco, CA'"
                    },
                    unit = new
                    {
                        type = "string",
                        @enum = new[] { "celsius", "fahrenheit" },
                        description = "The unit of temperature to use (celsius or fahrenheit)"
                    }
                },
                required = new[] { "location" }
            })
        };

        var sessionConfig = new VoiceLiveSessionOptions
        {
            Model = _model,
            Instructions = _instructions,
            Voice = new AzureStandardVoice(_voice),
            InputAudioFormat = InputAudioFormat.Pcm16,
            OutputAudioFormat = OutputAudioFormat.Pcm16,
            TurnDetection = new AzureSemanticVadTurnDetection
            {
                Threshold = 0.5f,
                PrefixPadding = TimeSpan.FromMilliseconds(300),
                SilenceDuration = TimeSpan.FromMilliseconds(500),
            },
            InputAudioEchoCancellation = new AudioEchoCancellation(),
            InputAudioNoiseReduction = new AudioNoiseReduction(AudioNoiseReductionType.AzureDeepNoiseSuppression),
            ToolChoice = ToolChoiceLiteral.Auto,
            InputAudioTranscription = new AudioInputTranscriptionOptions(AudioInputTranscriptionOptionsModel.Whisper1)
        };

        sessionConfig.Modalities.Clear();
        sessionConfig.Modalities.Add(InteractionModality.Text);
        sessionConfig.Modalities.Add(InteractionModality.Audio);

        sessionConfig.Tools.Add(getTimeFunction);
        sessionConfig.Tools.Add(getWeatherFunction);

        await _connection!.ConfigureSessionAsync(sessionConfig);
        _logger.LogInformation("Session configuration with function tools sent");
    }

    private async Task ProcessEventsAsync(CancellationToken cancellationToken)
    {
        await foreach (var update in _connection!.GetUpdatesAsync(cancellationToken))
            await HandleEventAsync(update);
    }

    private async Task HandleEventAsync(SessionUpdate update)
    {
        switch (update)
        {
            case SessionUpdateSessionUpdated sessionUpdate:
                _logger.LogInformation("Session ready: {SessionId}", sessionUpdate.Session.Id);
                _sessionReady = true;
                if (!_conversationStarted)
                {
                    _conversationStarted = true;
                    await _connection!.StartResponseAsync();
                }
                _audioProcessor!.StartCapture();
                break;

            case SessionUpdateInputAudioBufferSpeechStarted:
                Console.WriteLine("Listening...");
                _audioProcessor!.SkipPendingAudio();
                if (_activeResponse && !_responseApiDone)
                {
                    try { await _connection!.CancelResponseAsync(); }
                    catch (Exception ex) when (ex.Message.Contains("no active response"))
                    {
                        _logger.LogDebug("Cancel ignored -- response already completed");
                    }
                }
                break;

            case SessionUpdateInputAudioBufferSpeechStopped:
                Console.WriteLine("Processing...");
                break;

            case SessionUpdateResponseCreated:
                _activeResponse = true;
                _responseApiDone = false;
                break;

            case SessionUpdateResponseAudioDelta audioDelta:
                _audioProcessor!.QueueAudio(audioDelta.Delta?.ToArray());
                break;

            case SessionUpdateResponseDone:
                _activeResponse = false;
                _responseApiDone = true;
                if (_pendingFunctionCall?.ContainsKey("arguments") == true)
                {
                    await ExecuteFunctionCallAsync(_pendingFunctionCall);
                    _pendingFunctionCall = null;
                }
                break;

            case SessionUpdateResponseFunctionCallArgumentsDone functionCallFinished:
                _pendingFunctionCall = new Dictionary<string, object>
                {
                    ["name"] = functionCallFinished.Name,
                    ["call_id"] = functionCallFinished.CallId,
                    ["previous_item_id"] = functionCallFinished.ItemId,
                    ["arguments"] = functionCallFinished.Arguments
                };
                Console.WriteLine($"Calling function: {functionCallFinished.Name}");
                break;

            case SessionUpdateError errorUpdate:
                _logger.LogError("VoiceLive error: {Error}", errorUpdate.Error.Message);
                Console.Error.WriteLine($"Error: {errorUpdate.Error.Message}");
                break;
        }
    }

    private async Task ExecuteFunctionCallAsync(Dictionary<string, object> functionCallInfo)
    {
        var functionName = (string)functionCallInfo["name"];
        var callId = (string)functionCallInfo["call_id"];
        var arguments = (string)functionCallInfo["arguments"];

        if (!_availableFunctions.TryGetValue(functionName, out var function))
        {
            _logger.LogError("Unknown function: {FunctionName}", functionName);
            return;
        }

        try
        {
            var argsElement = JsonSerializer.Deserialize<JsonElement>(arguments);
            var result = function(argsElement);
            var resultJson = JsonSerializer.Serialize(result);

            await _connection!.AddItemAsync(new FunctionCallOutputItem(callId, resultJson));
            _logger.LogInformation("Function result sent: {Result}", resultJson);
            Console.WriteLine($"Function {functionName} completed");

            await _connection.StartResponseAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error executing function {FunctionName}", functionName);
        }
    }

    // -----------------------------------------------------------------------
    // Backend functions -- these mirror the Python get_current_time /
    // get_current_weather implementations.
    // -----------------------------------------------------------------------

    private static Dictionary<string, object> GetCurrentTime(JsonElement arguments)
    {
        var timezone = arguments.TryGetProperty("timezone", out var tz)
            ? tz.GetString() ?? "local"
            : "local";

        DateTime now;
        string timezoneName;

        if (timezone.Equals("utc", StringComparison.OrdinalIgnoreCase))
        {
            now = DateTime.UtcNow;
            timezoneName = "UTC";
        }
        else
        {
            now = DateTime.Now;
            timezoneName = "local";
        }

        return new Dictionary<string, object>
        {
            ["time"] = now.ToString("hh:mm:ss tt"),
            ["date"] = now.ToString("dddd, MMMM dd, yyyy"),
            ["timezone"] = timezoneName
        };
    }

    private static Dictionary<string, object> GetCurrentWeather(JsonElement arguments)
    {
        var location = arguments.TryGetProperty("location", out var loc)
            ? loc.GetString() ?? "Unknown"
            : "Unknown";
        var unit = arguments.TryGetProperty("unit", out var u)
            ? u.GetString() ?? "celsius"
            : "celsius";

        // Simulated weather response -- replace with a real weather API call.
        return new Dictionary<string, object>
        {
            ["location"] = location,
            ["temperature"] = unit == "celsius" ? 22 : 72,
            ["unit"] = unit,
            ["condition"] = "Partly Cloudy",
            ["humidity"] = 65,
            ["wind_speed"] = 10
        };
    }
}
```

---

## Related content

- Try the [Voice Live agents quickstart](./voice-live-agents-quickstart.md)
- Learn more about [How to use the Voice Live API](./voice-live-how-to.md)
- See the [Voice Live API reference](./voice-live-api-reference.md)
