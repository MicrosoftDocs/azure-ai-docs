---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
reviewer: PatrickFarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 04/06/2026
ai-usage: ai-assisted
---

Learn how to use function calling in a Voice Live session using the VoiceLive SDK for C#. This article builds on the [Quickstart: Get started with Voice Live for real-time voice agents](../../../voice-live-quickstart.md) by adding function calling so the assistant can invoke backend tools during a conversation.

[!INCLUDE [Header](../../common/voice-live-csharp.md)]

[!INCLUDE [Implementation steps](intro.md)]

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later.
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- The `Azure.AI.VoiceLive`, `Azure.Identity`, and `NAudio` packages installed.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Prepare the environment

Before you continue, complete the [Quickstart: Get started with Voice Live for real-time voice agents](../../../voice-live-quickstart.md) to set up your Foundry resource, install the VoiceLive SDK for .NET, configure authentication, and verify that you can run a basic Voice Live conversation end-to-end. The function calling sample in this article reuses the same resource, credentials, and environment variables.

Install the required packages:

```dotnetcli
dotnet add package Azure.AI.VoiceLive
dotnet add package Azure.Identity
dotnet add package NAudio
```

## Sample code

The following sample extends the basic Voice Live conversation from the [Quickstart: Get started with Voice Live for real-time voice agents](../../../voice-live-quickstart.md) by registering two function tools (`get_current_time` and `get_current_weather`) and handling the function call events the service returns.

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
