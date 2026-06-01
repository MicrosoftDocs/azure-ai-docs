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

Learn how to use function calling in a Voice Live session using the VoiceLive SDK for Java. This article builds on the [Quickstart: Create a Voice Live real-time voice agent](../../../voice-live-quickstart.md) with function calling integration.

[!INCLUDE [Header](../../common/voice-live-java.md)]

[!INCLUDE [Implementation steps](intro.md)]

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [Java Development Kit (JDK)](/java/azure/jdk/) version 11 or later.
- [Apache Maven](https://maven.apache.org/download.cgi) installed.
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- The `azure-ai-voicelive`, `azure-core`, `azure-identity`, and `reactor-core` packages added to your project.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Prepare the environment

Complete the [Voice Live quickstart](../../../voice-live-quickstart.md) to set up your environment, configure authentication, and test your first Voice Live conversation.

Add the following dependencies to your `pom.xml`:

```xml
<dependencies>
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-ai-voicelive</artifactId>
        <version>1.0.0-beta.1</version>
    </dependency>
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-core</artifactId>
        <version>1.53.0</version>
    </dependency>
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
        <version>1.11.0</version>
    </dependency>
    <dependency>
        <groupId>io.projectreactor</groupId>
        <artifactId>reactor-core</artifactId>
        <version>3.5.11</version>
    </dependency>
</dependencies>
```

## Sample code

The following sample shows function calling with the Voice Live API.

```java
// -------------------------------------------------------------------------
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
// -------------------------------------------------------------------------

import com.azure.ai.voicelive.VoiceLiveAsyncClient;
import com.azure.ai.voicelive.VoiceLiveClientBuilder;
import com.azure.ai.voicelive.VoiceLiveServiceVersion;
import com.azure.ai.voicelive.VoiceLiveSessionAsyncClient;
import com.azure.ai.voicelive.models.AudioEchoCancellation;
import com.azure.ai.voicelive.models.AudioInputTranscriptionOptions;
import com.azure.ai.voicelive.models.AudioInputTranscriptionOptionsModel;
import com.azure.ai.voicelive.models.AudioNoiseReduction;
import com.azure.ai.voicelive.models.AudioNoiseReductionType;
import com.azure.ai.voicelive.models.AzureStandardVoice;
import com.azure.ai.voicelive.models.ClientEventConversationItemCreate;
import com.azure.ai.voicelive.models.ClientEventResponseCreate;
import com.azure.ai.voicelive.models.ClientEventSessionUpdate;
import com.azure.ai.voicelive.models.FunctionCallOutputItem;
import com.azure.ai.voicelive.models.InputAudioFormat;
import com.azure.ai.voicelive.models.InteractionModality;
import com.azure.ai.voicelive.models.OutputAudioFormat;
import com.azure.ai.voicelive.models.ServerEventType;
import com.azure.ai.voicelive.models.ServerVadTurnDetection;
import com.azure.ai.voicelive.models.SessionUpdate;
import com.azure.ai.voicelive.models.ResponseFunctionCallItem;
import com.azure.ai.voicelive.models.SessionUpdateConversationItemCreated;
import com.azure.ai.voicelive.models.SessionUpdateError;
import com.azure.ai.voicelive.models.SessionUpdateResponseAudioDelta;
import com.azure.ai.voicelive.models.SessionUpdateResponseFunctionCallArgumentsDone;
import com.azure.ai.voicelive.models.SessionUpdateSessionUpdated;
import com.azure.ai.voicelive.models.ToolChoiceLiteral;
import com.azure.ai.voicelive.models.VoiceLiveFunctionDefinition;
import com.azure.ai.voicelive.models.VoiceLiveSessionOptions;
import com.azure.core.credential.KeyCredential;
import com.azure.core.credential.TokenCredential;
import com.azure.core.util.BinaryData;
import com.azure.identity.AzureCliCredentialBuilder;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.SourceDataLine;
import javax.sound.sampled.TargetDataLine;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Function;

/**
 * Voice assistant with function calling using
 * VoiceLive SDK for Java.
 */
public final class FunctionCallingQuickstart {

    private static final int SAMPLE_RATE = 24000;
    private static final int CHANNELS = 1;
    private static final int SAMPLE_SIZE_BITS = 16;
    private static final int CHUNK_SIZE = 1200;

    // Available backend functions
    private static final
        Map<String, Function<Map<String, String>,
            Map<String, Object>>> FUNCTIONS =
                new HashMap<>();

    static {
        FUNCTIONS.put(
            "get_current_time",
            FunctionCallingQuickstart::getCurrentTime);
        FUNCTIONS.put(
            "get_current_weather",
            FunctionCallingQuickstart::getCurrentWeather);
    }

    // Pending function call state
    private static volatile String pendingName;
    private static volatile String pendingCallId;
    private static volatile String pendingItemId;
    private static volatile String pendingArguments;

    private FunctionCallingQuickstart() { }

    // ---------------------------------------------------------------
    // Audio processor
    // ---------------------------------------------------------------

    private static class AudioProcessor {
        private final VoiceLiveSessionAsyncClient session;
        private final AudioFormat audioFormat;

        private TargetDataLine microphone;
        private SourceDataLine speaker;
        private final AtomicBoolean isCapturing =
            new AtomicBoolean(false);
        private final AtomicBoolean isPlaying =
            new AtomicBoolean(false);
        private final BlockingQueue<byte[]>
            playbackQueue = new LinkedBlockingQueue<>();
        private final AtomicInteger nextSeq =
            new AtomicInteger(0);
        private final AtomicInteger playbackBase =
            new AtomicInteger(0);

        AudioProcessor(
            VoiceLiveSessionAsyncClient session) {
            this.session = session;
            this.audioFormat = new AudioFormat(
                AudioFormat.Encoding.PCM_SIGNED,
                SAMPLE_RATE, SAMPLE_SIZE_BITS,
                CHANNELS, CHANNELS * SAMPLE_SIZE_BITS / 8,
                SAMPLE_RATE, false);
        }

        void startCapture() {
            if (isCapturing.get()) return;
            try {
                DataLine.Info info = new DataLine.Info(
                    TargetDataLine.class, audioFormat);
                microphone =
                    (TargetDataLine)
                        AudioSystem.getLine(info);
                microphone.open(audioFormat,
                    CHUNK_SIZE * 4);
                microphone.start();
                isCapturing.set(true);

                Thread t = new Thread(() -> {
                    byte[] buf =
                        new byte[CHUNK_SIZE * 2];
                    while (isCapturing.get()) {
                        int n = microphone.read(
                            buf, 0, buf.length);
                        if (n > 0) {
                            byte[] chunk =
                                Arrays.copyOf(buf, n);
                            session.sendInputAudio(
                                BinaryData.fromBytes(
                                    chunk))
                                .subscribeOn(
                                    Schedulers
                                        .boundedElastic())
                                .subscribe();
                        }
                    }
                }, "AudioCapture");
                t.setDaemon(true);
                t.start();
                System.out.println(
                    "Microphone capture started");
            } catch (Exception e) {
                throw new RuntimeException(
                    "Failed to start microphone", e);
            }
        }

        void startPlayback() {
            if (isPlaying.get()) return;
            try {
                DataLine.Info info = new DataLine.Info(
                    SourceDataLine.class, audioFormat);
                speaker =
                    (SourceDataLine)
                        AudioSystem.getLine(info);
                speaker.open(audioFormat, CHUNK_SIZE * 4);
                speaker.start();
                isPlaying.set(true);

                Thread t = new Thread(() -> {
                    while (isPlaying.get()) {
                        try {
                            byte[] data =
                                playbackQueue.take();
                            if (data.length == 0) break;
                            if (speaker != null
                                && speaker.isOpen()) {
                                speaker.write(
                                    data, 0,
                                    data.length);
                            }
                        } catch (InterruptedException e) {
                            Thread.currentThread()
                                .interrupt();
                            break;
                        }
                    }
                }, "AudioPlayback");
                t.setDaemon(true);
                t.start();
                System.out.println(
                    "Audio playback started");
            } catch (Exception e) {
                throw new RuntimeException(
                    "Failed to start speaker", e);
            }
        }

        void queueAudio(byte[] data) {
            if (data != null && data.length > 0) {
                playbackQueue.offer(data);
            }
        }

        void skipPendingAudio() {
            playbackQueue.clear();
            if (speaker != null && speaker.isOpen()) {
                speaker.flush();
            }
        }

        void shutdown() {
            isCapturing.set(false);
            if (microphone != null) {
                microphone.stop();
                microphone.close();
            }
            isPlaying.set(false);
            playbackQueue.offer(new byte[0]);
            if (speaker != null) {
                speaker.stop();
                speaker.close();
            }
            System.out.println(
                "Audio processor cleaned up");
        }
    }

    // ---------------------------------------------------------------
    // Session setup with function tools
    // ---------------------------------------------------------------

    private static VoiceLiveSessionOptions
        createSessionOptions(
            String voice, String instructions) {

        ServerVadTurnDetection vad =
            new ServerVadTurnDetection()
                .setThreshold(0.5)
                .setPrefixPaddingMs(300)
                .setSilenceDurationMs(500)
                .setInterruptResponse(true)
                .setAutoTruncate(true)
                .setCreateResponse(true);

        VoiceLiveFunctionDefinition getTime =
            new VoiceLiveFunctionDefinition(
                "get_current_time")
                .setDescription("Get the current time")
                .setParameters(BinaryData.fromObject(
                    Map.of(
                        "type", "object",
                        "properties", Map.of(
                            "timezone", Map.of(
                                "type", "string",
                                "description",
                                "The timezone, e.g., "
                                    + "'UTC', 'local'"
                            )),
                        "required", new String[] {}
                    )));

        VoiceLiveFunctionDefinition getWeather =
            new VoiceLiveFunctionDefinition(
                "get_current_weather")
                .setDescription(
                    "Get the current weather "
                        + "in a given location")
                .setParameters(BinaryData.fromObject(
                    Map.of(
                        "type", "object",
                        "properties", Map.of(
                            "location", Map.of(
                                "type", "string",
                                "description",
                                "The city and state, "
                                    + "e.g., "
                                    + "'San Francisco, CA'"
                            ),
                            "unit", Map.of(
                                "type", "string",
                                "enum", new String[] {
                                    "celsius",
                                    "fahrenheit"},
                                "description",
                                "The unit of temperature"
                            )),
                        "required",
                            new String[] {"location"}
                    )));

        VoiceLiveSessionOptions options =
            new VoiceLiveSessionOptions()
                .setInstructions(instructions)
                .setVoice(BinaryData.fromObject(
                    new AzureStandardVoice(voice)))
                .setModalities(Arrays.asList(
                    InteractionModality.TEXT,
                    InteractionModality.AUDIO))
                .setInputAudioFormat(InputAudioFormat.PCM16)
                .setOutputAudioFormat(
                    OutputAudioFormat.PCM16)
                .setInputAudioSamplingRate(SAMPLE_RATE)
                .setInputAudioNoiseReduction(
                    new AudioNoiseReduction(
                        AudioNoiseReductionType
                            .NEAR_FIELD))
                .setInputAudioEchoCancellation(
                    new AudioEchoCancellation())
                .setInputAudioTranscription(
                    new AudioInputTranscriptionOptions(
                        AudioInputTranscriptionOptionsModel
                            .WHISPER_1))
                .setTurnDetection(vad)
                .setToolChoice(BinaryData.fromObject(
                    ToolChoiceLiteral.AUTO));

        options.getTools().add(getTime);
        options.getTools().add(getWeather);

        return options;
    }

    // ---------------------------------------------------------------
    // Event handling
    // ---------------------------------------------------------------

    private static void handleEvent(
        SessionUpdate event,
        AudioProcessor audio,
        VoiceLiveSessionAsyncClient session,
        AtomicBoolean conversationStarted) {

        ServerEventType type = event.getType();

        if (type ==
            ServerEventType.SESSION_UPDATED) {
            System.out.println("Session ready");
            if (!conversationStarted.getAndSet(true)) {
                session.sendEvent(
                    new ClientEventResponseCreate())
                    .subscribe();
            }
            audio.startCapture();

        } else if (type == ServerEventType
            .INPUT_AUDIO_BUFFER_SPEECH_STARTED) {
            System.out.println("Listening...");
            audio.skipPendingAudio();

        } else if (type == ServerEventType
            .INPUT_AUDIO_BUFFER_SPEECH_STOPPED) {
            System.out.println("Processing...");

        } else if (type ==
            ServerEventType.RESPONSE_AUDIO_DELTA) {
            if (event instanceof
                SessionUpdateResponseAudioDelta) {
                byte[] data =
                    ((SessionUpdateResponseAudioDelta)
                        event).getDelta();
                audio.queueAudio(data);
            }

        } else if (type ==
            ServerEventType.RESPONSE_AUDIO_DONE) {
            System.out.println("Ready for next input...");

        } else if (type ==
            ServerEventType.RESPONSE_DONE) {
            System.out.println("Response complete");

            if (pendingArguments != null) {
                executeFunctionCall(session);
            }

        } else if (type == ServerEventType
            .CONVERSATION_ITEM_CREATED) {
            if (event instanceof
                SessionUpdateConversationItemCreated) {
                SessionUpdateConversationItemCreated
                    created =
                        (SessionUpdateConversationItemCreated)
                            event;
                if (created.getItem() instanceof
                    ResponseFunctionCallItem) {
                    ResponseFunctionCallItem funcItem =
                        (ResponseFunctionCallItem)
                            created.getItem();
                    pendingName = funcItem.getName();
                    pendingCallId = funcItem.getCallId();
                    pendingItemId = funcItem.getId();
                    pendingArguments = null;
                    System.out.println(
                        "Calling function: "
                            + pendingName);
                }
            }

        } else if (type == ServerEventType
            .RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE) {
            if (event instanceof
                SessionUpdateResponseFunctionCallArgumentsDone) {
                pendingArguments =
                    ((SessionUpdateResponseFunctionCallArgumentsDone)
                        event).getArguments();
            }

        } else if (type ==
            ServerEventType.ERROR) {
            if (event instanceof SessionUpdateError) {
                System.err.println("VoiceLive error: "
                    + ((SessionUpdateError) event)
                        .getError().getMessage());
            }
        }
    }

    private static void executeFunctionCall(
        VoiceLiveSessionAsyncClient session) {

        String name = pendingName;
        String callId = pendingCallId;
        String args = pendingArguments;

        // Reset state
        pendingName = null;
        pendingCallId = null;
        pendingItemId = null;
        pendingArguments = null;

        Function<Map<String, String>,
            Map<String, Object>> func =
                FUNCTIONS.get(name);
        if (func == null) {
            System.err.println(
                "Unknown function: " + name);
            return;
        }

        try {
            // Parse arguments from JSON string
            @SuppressWarnings("unchecked")
            Map<String, String> parsed =
                BinaryData.fromString(args)
                    .toObject(Map.class);
            Map<String, Object> result = func.apply(parsed);
            String resultJson =
                BinaryData.fromObject(result).toString();

            FunctionCallOutputItem output =
                new FunctionCallOutputItem(
                    callId, resultJson);
            session.sendEvent(
                new ClientEventConversationItemCreate()
                    .setItem(output))
                .then(session.sendEvent(
                    new ClientEventResponseCreate()))
                .subscribe();

            System.out.println(
                "Function " + name + " completed");
        } catch (Exception e) {
            System.err.println(
                "Error executing " + name + ": "
                    + e.getMessage());
        }
    }

    // ---------------------------------------------------------------
    // Backend functions
    // ---------------------------------------------------------------

    private static Map<String, Object> getCurrentTime(
        Map<String, String> args) {
        String tz = args != null
            ? args.getOrDefault("timezone", "local")
            : "local";

        LocalDateTime now;
        String tzName;
        if ("utc".equalsIgnoreCase(tz)) {
            now = LocalDateTime.now(ZoneOffset.UTC);
            tzName = "UTC";
        } else {
            now = LocalDateTime.now();
            tzName = "local";
        }

        Map<String, Object> result = new HashMap<>();
        result.put("time", now.format(
            DateTimeFormatter.ofPattern("hh:mm:ss a")));
        result.put("date", now.format(
            DateTimeFormatter.ofPattern(
                "EEEE, MMMM dd, yyyy")));
        result.put("timezone", tzName);
        return result;
    }

    private static Map<String, Object> getCurrentWeather(
        Map<String, String> args) {
        String location = args != null
            ? args.getOrDefault("location", "Unknown")
            : "Unknown";
        String unit = args != null
            ? args.getOrDefault("unit", "celsius")
            : "celsius";

        // Simulated weather response
        Map<String, Object> result = new HashMap<>();
        result.put("location", location);
        result.put("temperature",
            "celsius".equals(unit) ? 22 : 72);
        result.put("unit", unit);
        result.put("condition", "Partly Cloudy");
        result.put("humidity", 65);
        result.put("wind_speed", 10);
        return result;
    }

    // ---------------------------------------------------------------
    // Main
    // ---------------------------------------------------------------

    public static void main(String[] cliArgs) {
        String endpoint = System.getenv(
            "AZURE_VOICELIVE_ENDPOINT");
        String apiKey = System.getenv(
            "AZURE_VOICELIVE_API_KEY");
        String model = System.getenv(
            "AZURE_VOICELIVE_MODEL") != null
                ? System.getenv("AZURE_VOICELIVE_MODEL")
                : "gpt-realtime";
        String voice = System.getenv(
            "AZURE_VOICELIVE_VOICE") != null
                ? System.getenv("AZURE_VOICELIVE_VOICE")
                : "en-US-Ava:DragonHDLatestNeural";
        String instructions = "You are a helpful AI "
            + "assistant with access to functions. "
            + "Use the functions when appropriate to "
            + "provide accurate, real-time information. "
            + "Always start the conversation in English.";
        boolean useToken =
            Arrays.asList(cliArgs)
                .contains("--use-token-credential");

        if (endpoint == null) {
            System.err.println(
                "Set AZURE_VOICELIVE_ENDPOINT");
            return;
        }
        if (apiKey == null && !useToken) {
            System.err.println(
                "Set AZURE_VOICELIVE_API_KEY "
                    + "or use --use-token-credential");
            return;
        }

        VoiceLiveAsyncClient client;
        if (useToken) {
            TokenCredential credential =
                new AzureCliCredentialBuilder().build();
            client = new VoiceLiveClientBuilder()
                .endpoint(endpoint)
                .credential(credential)
                .serviceVersion(
                    VoiceLiveServiceVersion.V2025_10_01)
                .buildAsyncClient();
        } else {
            client = new VoiceLiveClientBuilder()
                .endpoint(endpoint)
                .credential(new KeyCredential(apiKey))
                .serviceVersion(
                    VoiceLiveServiceVersion.V2025_10_01)
                .buildAsyncClient();
        }

        VoiceLiveSessionOptions sessionOptions =
            createSessionOptions(voice, instructions);
        AtomicReference<AudioProcessor> audioRef =
            new AtomicReference<>();
        AtomicBoolean started = new AtomicBoolean(false);

        client.startSession(model)
            .flatMap(session -> {
                AudioProcessor audio =
                    new AudioProcessor(session);
                audioRef.set(audio);

                session.receiveEvents()
                    .subscribe(
                        event -> handleEvent(
                            event, audio,
                            session, started),
                        err -> System.err.println(
                            "Event error: "
                                + err.getMessage()));

                session.sendEvent(
                    new ClientEventSessionUpdate(
                        sessionOptions))
                    .subscribe();

                audio.startPlayback();

                System.out.println("=".repeat(60));
                System.out.println(
                    "VOICE ASSISTANT WITH "
                        + "FUNCTION CALLING READY");
                System.out.println("Try saying:");
                System.out.println(
                    "  - 'What's the current time?'");
                System.out.println(
                    "  - 'What's the weather "
                        + "in Seattle?'");
                System.out.println(
                    "Press Ctrl+C to exit");
                System.out.println("=".repeat(60));

                Runtime.getRuntime().addShutdownHook(
                    new Thread(() -> {
                        System.out.println(
                            "Shutting down...");
                        audio.shutdown();
                    }));

                return Mono.never();
            })
            .doFinally(sig -> {
                AudioProcessor audio = audioRef.get();
                if (audio != null) audio.shutdown();
            })
            .block();
    }
}
```
