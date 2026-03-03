---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
reviewer: patrickfarley
ms.reviewer: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 3/2/2026
ms.subservice: azure-ai-foundry-openai
ai-usage: ai-assisted
---

In this article, you learn how to use Voice Live with [Microsoft Foundry models](/azure/ai-foundry/concepts/foundry-models-overview) using the VoiceLive SDK for JavaScript.

[!INCLUDE [Header](../../common/voice-live-javascript.md)] 

[!INCLUDE [Introduction](intro.md)]

> [!NOTE]
> The JavaScript Voice Live SDK is designed for browser-based applications with built-in WebSocket and Web Audio support. This quickstart uses Node.js with `node-record-lpcm16` and `speaker` for a console experience.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [Node.js](https://nodejs.org/) version 18 or later.
- [SoX](https://sox.sourceforge.io/) installed on your system (required by `node-record-lpcm16` for microphone capture).
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

1. Create a **package.json** file with the following content:

    :::code language="json" source="~/cognitive-services-quickstart-code/javascript/speech/package.json":::

1. Install the dependencies:

    ```shell
    npm install
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

## Start a conversation

The sample code in this quickstart supports both Microsoft Entra ID and API key authentication. The `--use-token-credential` flag switches to `DefaultAzureCredential` if you prefer keyless authentication.

The sample connects to Voice Live and configures the session with these fields:

- `model`: The model deployment name to invoke (for example, `gpt-realtime`).
- `voice`: The voice to use for audio responses. Supports Azure standard voices and OpenAI voices.
- `modalities`: The modalities the session supports. Use `["text", "audio"]` for voice conversations.
- `instructions`: System-level instructions that configure the assistant's behavior.
- `inputAudioFormat`: The format of the input audio stream. Use `pcm16` for raw PCM audio.

1. Create the **model-quickstart.js** file with the following code:

    ```javascript
    // Copyright (c) Microsoft Corporation. All rights reserved.
    // Licensed under the MIT License.

    import "dotenv/config";
    import { VoiceLiveClient } from "@azure/ai-voicelive";
    import { AzureKeyCredential } from "@azure/core-auth";
    import { DefaultAzureCredential } from "@azure/identity";
    import { spawn } from "node:child_process";
    import { existsSync, mkdirSync, appendFileSync } from "node:fs";
    import { join, dirname } from "node:path";
    import { fileURLToPath } from "node:url";

    const __dirname = dirname(fileURLToPath(import.meta.url));

    const logsDir = join(__dirname, "logs");
    if (!existsSync(logsDir)) mkdirSync(logsDir, { recursive: true });

    const timestamp = new Date()
      .toISOString()
      .replace(/[:.]/g, "-")
      .replace("T", "_")
      .slice(0, 19);
    const conversationLogFile = join(logsDir, `conversation_${timestamp}.log`);

    function writeConversationLog(message) {
      appendFileSync(conversationLogFile, message + "\n", "utf-8");
    }

    function printUsage() {
      console.log("Usage: node model-quickstart.js [options]");
      console.log("");
      console.log("Options:");
      console.log("  --api-key <key>             VoiceLive API key");
      console.log("  --endpoint <url>            VoiceLive endpoint URL");
      console.log("  --model <name>              Model to use (default: gpt-realtime)");
      console.log(
        "  --voice <name>              Voice (default: en-US-Ava:DragonHDLatestNeural)",
      );
      console.log("  --instructions <text>       System instructions for the assistant");
      console.log("  --audio-input-device <name> Explicit SoX input device name (Windows)");
      console.log("  --list-audio-devices        List available audio input devices and exit");
      console.log("  --greeting-text <text>      Send a pre-defined greeting instead of LLM-generated");
      console.log("  --use-token-credential      Use Azure credential instead of API key");
      console.log("  --no-audio                  Connect and configure session without mic/speaker");
      console.log("  -h, --help                  Show this help text");
    }

    function parseArguments(argv) {
      const parsed = {
        apiKey: process.env.AZURE_VOICELIVE_API_KEY,
        endpoint: process.env.AZURE_VOICELIVE_ENDPOINT,
        model: process.env.AZURE_VOICELIVE_MODEL ?? "gpt-realtime",
        voice:
          process.env.AZURE_VOICELIVE_VOICE ?? "en-US-Ava:DragonHDLatestNeural",
        instructions:
          process.env.AZURE_VOICELIVE_INSTRUCTIONS ??
          "You are a helpful AI assistant. Respond naturally and conversationally. Keep your responses concise but engaging.",
        audioInputDevice: process.env.AUDIO_INPUT_DEVICE,
        listAudioDevices: false,
        greetingText: undefined,
        useTokenCredential: false,
        noAudio: false,
        help: false,
      };

      for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        switch (arg) {
          case "--api-key":
            parsed.apiKey = argv[++i];
            break;
          case "--endpoint":
            parsed.endpoint = argv[++i];
            break;
          case "--model":
            parsed.model = argv[++i];
            break;
          case "--voice":
            parsed.voice = argv[++i];
            break;
          case "--instructions":
            parsed.instructions = argv[++i];
            break;
          case "--audio-input-device":
            parsed.audioInputDevice = argv[++i];
            break;
          case "--list-audio-devices":
            parsed.listAudioDevices = true;
            break;
          case "--greeting-text":
            parsed.greetingText = argv[++i];
            break;
          case "--use-token-credential":
            parsed.useTokenCredential = true;
            break;
          case "--no-audio":
            parsed.noAudio = true;
            break;
          case "--help":
          case "-h":
            parsed.help = true;
            break;
          default:
            if (arg?.startsWith("-")) {
              throw new Error(`Unknown option: ${arg}`);
            }
            break;
        }
      }

      return parsed;
    }

    /**
     * List available audio input devices on Windows (AudioEndpoint via WMI).
     * Falls back to a note on non-Windows platforms.
     */
    async function listAudioDevices() {
      if (process.platform !== "win32") {
        console.log("Device listing is currently supported on Windows only.");
        console.log("On macOS/Linux, run: sox -V6 -n -t coreaudio -n trim 0 0  (or similar)");
        return;
      }

      const { execSync } = await import("node:child_process");
      try {
        const output = execSync(
          'powershell -NoProfile -Command "Get-CimInstance Win32_PnPEntity | Where-Object { $_.PNPClass -eq \'AudioEndpoint\' } | Select-Object -ExpandProperty Name"',
          { encoding: "utf-8", timeout: 10000 },
        ).trim();

        if (!output) {
          console.log("No audio endpoint devices found.");
          return;
        }

        console.log("Available audio endpoint devices:");
        console.log("");
        for (const line of output.split(/\r?\n/)) {
          const name = line.trim();
          if (name) console.log(`  ${name}`);
        }
        console.log("");
        console.log("Use the device name (or a unique substring) with --audio-input-device.");
        console.log('Example: node model-quickstart.js --audio-input-device "Microphone"');
      } catch (err) {
        console.error("Failed to query audio devices:", err.message);
      }
    }

    function resolveVoiceConfig(voiceName) {
      const looksLikeAzureVoice = voiceName.includes("-") || voiceName.includes(":");
      if (looksLikeAzureVoice) {
        return {
          type: "azure-standard",
          name: voiceName,
        };
      }

      return {
        type: "openai",
        name: voiceName,
      };
    }

    class AudioProcessor {
      constructor(enableAudio = true, inputDevice = undefined) {
        this._enableAudio = enableAudio;
        this._inputDevice = inputDevice;
        this._recorder = null;
        this._soxProcess = null;
        this._speaker = null;
        this._skipSeq = 0;
        this._nextSeq = 0;
        this._recordModule = null;
        this._speakerCtor = null;
      }

      async _ensureAudioModulesLoaded() {
        if (!this._enableAudio) return;
        if (this._recordModule && this._speakerCtor) return;

        try {
          const recordModule = await import("node-record-lpcm16");
          const speakerModule = await import("speaker");
          this._recordModule = recordModule.default;
          this._speakerCtor = speakerModule.default;
        } catch {
          throw new Error(
            "Audio dependencies are unavailable. Install optional packages (node-record-lpcm16, speaker) and required native build tools, or run with --no-audio for connectivity-only validation.",
          );
        }
      }

      async startCapture(session) {
        if (!this._enableAudio) {
          console.log("[audio] --no-audio enabled: microphone capture skipped");
          return;
        }
        if (this._recorder || this._soxProcess) return;

        if (this._inputDevice) {
          console.log(`[audio] Using explicit input device: ${this._inputDevice}`);
          const soxArgs = [
            "-q", "-t", "waveaudio", this._inputDevice,
            "-r", "24000", "-c", "1",
            "-e", "signed-integer", "-b", "16",
            "-t", "raw", "-",
          ];

          this._soxProcess = spawn("sox", soxArgs, {
            stdio: ["ignore", "pipe", "pipe"],
          });

          this._soxProcess.stdout.on("data", (chunk) => {
            if (session.isConnected) {
              session.sendAudio(new Uint8Array(chunk)).catch(() => {
                // Ignore send errors during disconnect
              });
            }
          });

          this._soxProcess.stderr.on("data", (data) => {
            const msg = data.toString().trim();
            if (msg) {
              console.error(`[audio] sox stderr: ${msg}`);
            }
          });

          this._soxProcess.on("error", (error) => {
            console.error(`[audio] SoX process error: ${error?.message ?? error}`);
          });

          this._soxProcess.on("close", (code) => {
            if (code !== 0) {
              console.error(`[audio] SoX exited with code ${code}`);
            }
            this._soxProcess = null;
          });

          console.log("[audio] Microphone capture started");
          return;
        }

        await this._ensureAudioModulesLoaded();

        const recorderOptions = {
          sampleRate: 24000,
          channels: 1,
          audioType: "raw",
          recorder: "sox",
          encoding: "signed-integer",
          bitwidth: 16,
        };

        this._recorder = this._recordModule.record(recorderOptions);
        const recorderStream = this._recorder.stream();

        recorderStream.on("data", (chunk) => {
          if (session.isConnected) {
            session.sendAudio(new Uint8Array(chunk)).catch(() => {
              // Ignore send errors during disconnect
            });
          }
        });

        recorderStream.on("error", (error) => {
          console.error(`[audio] Recorder stream error: ${error?.message ?? error}`);
          console.error(
            "[audio] SoX capture failed. Check microphone permissions/device and run with DEBUG=record for details.",
          );
        });

        console.log("[audio] Microphone capture started");
      }

      async startPlayback() {
        if (!this._enableAudio) {
          console.log("[audio] --no-audio enabled: speaker playback skipped");
          return;
        }
        if (this._speaker) return;
        await this._resetSpeaker();
        console.log("[audio] Playback ready");
      }

      queueAudio(base64Delta) {
        const seq = this._nextSeq++;
        if (seq < this._skipSeq) return;
        const chunk = Buffer.from(base64Delta, "base64");
        if (this._speaker && !this._speaker.destroyed) {
          this._speaker.write(chunk);
        }
      }

      skipPendingAudio() {
        if (!this._enableAudio) return;
        this._skipSeq = this._nextSeq++;
        this._resetSpeaker().catch(() => {
          // best-effort reset
        });
      }

      shutdown() {
        if (this._soxProcess) {
          try {
            this._soxProcess.kill();
          } catch {
            // no-op
          }
          this._soxProcess = null;
        }

        if (this._recorder) {
          this._recorder.stop();
          this._recorder = null;
        }

        if (this._speaker) {
          this._speaker.end();
          this._speaker = null;
        }

        console.log("[audio] Audio processor shut down");
      }

      async _resetSpeaker() {
        await this._ensureAudioModulesLoaded();

        if (this._speaker && !this._speaker.destroyed) {
          try {
            this._speaker.end();
          } catch {
            // no-op
          }
        }

        this._speaker = new this._speakerCtor({
          channels: 1,
          bitDepth: 16,
          sampleRate: 24000,
          signed: true,
        });

        this._speaker.on("error", () => {
          // Swallow transient audio device errors
        });
      }
    }

    class BasicModelVoiceAssistant {
      constructor(options) {
        this.endpoint = options.endpoint;
        this.credential = options.credential;
        this.model = options.model;
        this.voice = options.voice;
        this.instructions = options.instructions;
        this.audioInputDevice = options.audioInputDevice;
        this.greetingText = options.greetingText;
        this.noAudio = options.noAudio;

        this._session = null;
        this._subscription = null;
        this._audio = new AudioProcessor(!options.noAudio, options.audioInputDevice);
        this._activeResponse = false;
        this._responseApiDone = false;
        this._greetingSent = false;
      }

      async start() {
        const client = new VoiceLiveClient(this.endpoint, this.credential);
        const session = client.createSession({ model: this.model });
        this._session = session;

        console.log(
          `[init] Connecting to VoiceLive with model "${this.model}" at "${this.endpoint}" ...`,
        );

        this._subscription = session.subscribe({
          onSessionUpdated: async (event, context) => {
            const s = event.session;
            const model = s?.model;
            const voice = s?.voice;

            console.log(`[session] Session ready: ${context.sessionId}`);
            writeConversationLog(
              [
                `SessionID: ${context.sessionId}`,
                `Model: ${typeof model === "string" ? model : model?.toString?.() ?? ""}`,
                `Voice Name: ${voice?.name ?? ""}`,
                `Voice Type: ${voice?.type ?? ""}`,
                "",
              ].join("\n"),
            );

            if (!this._greetingSent) {
              this._greetingSent = true;
            }
          },

          onConversationItemInputAudioTranscriptionCompleted: async (event) => {
            const transcript = event.transcript ?? "";
            console.log(`👤 You said:\t${transcript}`);
            writeConversationLog(`User Input:\t${transcript}`);
          },

          onResponseTextDone: async (event) => {
            const text = event.text ?? "";
            console.log(`🤖 Assistant text:\t${text}`);
            writeConversationLog(`Assistant Text Response:\t${text}`);
          },

          onResponseAudioTranscriptDone: async (event) => {
            const transcript = event.transcript ?? "";
            console.log(`🤖 Assistant audio transcript:\t${transcript}`);
            writeConversationLog(`Assistant Audio Response:\t${transcript}`);
          },

          onInputAudioBufferSpeechStarted: async () => {
            console.log("🎤 Listening...");
            this._audio.skipPendingAudio();

            if (this._activeResponse && !this._responseApiDone) {
              try {
                await session.sendEvent({ type: "response.cancel" });
              } catch (err) {
                const msg = err?.message ?? "";
                if (!msg.toLowerCase().includes("no active response")) {
                  console.warn("[barge-in] Cancel failed:", msg);
                }
              }
            }
          },

          onInputAudioBufferSpeechStopped: async () => {
            console.log("🤔 Processing...");
          },

          onResponseCreated: async () => {
            this._activeResponse = true;
            this._responseApiDone = false;
          },

          onResponseAudioDelta: async (event) => {
            if (event.delta) {
              this._audio.queueAudio(event.delta);
            }
          },

          onResponseAudioDone: async () => {
            console.log("🎤 Ready for next input...");
          },

          onResponseDone: async () => {
            console.log("✅ Response complete");
            this._activeResponse = false;
            this._responseApiDone = true;
          },

          onServerError: async (event) => {
            const msg = event.error?.message ?? "";
            if (msg.includes("Cancellation failed: no active response")) {
              return;
            }
            console.error(`❌ VoiceLive error: ${msg}`);
          },

          onConversationItemCreated: async (event) => {
            console.log(`[event] Conversation item created: ${event.item?.id ?? ""}`);
          },
        });

        await session.connect();
        console.log("[init] Connected to VoiceLive session websocket");

        await this._setupSession();

        if (!this._greetingSent) {
          this._greetingSent = true;
          await this._sendProactiveGreeting();
        }

        await this._audio.startPlayback();
        await this._audio.startCapture(session);

        console.log("\n" + "=".repeat(60));
        console.log("🎤 VOICE ASSISTANT READY");
        console.log("Start speaking to begin conversation");
        console.log("Press Ctrl+C to exit");
        console.log("=".repeat(60) + "\n");

        if (this.noAudio) {
          setTimeout(() => {
            process.emit("SIGINT");
          }, 6000);
        }

        await new Promise((resolve) => {
          const onSignal = () => resolve();
          process.once("SIGINT", onSignal);
          process.once("SIGTERM", onSignal);

          const poll = setInterval(() => {
            if (!session.isConnected) {
              clearInterval(poll);
              resolve();
            }
          }, 500);
        });

        await this.shutdown();
      }

      /**
       * Send a proactive greeting when the session starts.
       * Supports pre-defined (--greeting-text) or LLM-generated (default).
       */
      async _sendProactiveGreeting() {
        const session = this._session;

        if (this.greetingText) {
          console.log("[session] Sending pre-generated greeting ...");
          try {
            await session.sendEvent({
              type: "response.create",
              response: {
                preGeneratedAssistantMessage: {
                  content: [{ type: "text", text: this.greetingText }],
                },
              },
            });
          } catch (err) {
            console.error("[session] Failed to send pre-generated greeting:", err.message);
          }
        } else {
          console.log("[session] Sending proactive greeting ...");
          try {
            await session.addConversationItem({
              type: "message",
              role: "system",
              content: [
                {
                  type: "input_text",
                  text: "Say something to welcome the user in English.",
                },
              ],
            });
            await session.sendEvent({ type: "response.create" });
          } catch (err) {
            console.error("[session] Failed to send greeting:", err.message);
          }
        }
      }

      async _setupSession() {
        console.log("[session] Configuring session ...");

        await this._session.updateSession({
          model: this.model,
          modalities: ["text", "audio"],
          instructions: this.instructions,
          voice: resolveVoiceConfig(this.voice),
          inputAudioFormat: "pcm16",
          outputAudioFormat: "pcm16",
          turnDetection: {
            type: "server_vad",
            threshold: 0.5,
            prefixPaddingInMs: 300,
            silenceDurationInMs: 500,
          },
          inputAudioEchoCancellation: { type: "server_echo_cancellation" },
          inputAudioNoiseReduction: { type: "azure_deep_noise_suppression" },
          inputAudioTranscription: { model: "azure-speech" },
        });

        console.log("[session] Session configuration sent");
      }

      async shutdown() {
        if (this._subscription) {
          await this._subscription.close();
          this._subscription = null;
        }

        if (this._session) {
          try {
            await this._session.disconnect();
          } catch {
            // ignore disconnect errors during shutdown
          }

          this._audio.shutdown();

          try {
            await this._session.dispose();
          } catch {
            // ignore dispose errors during shutdown
          }

          this._session = null;
        }
      }
    }

    async function main() {
      let args;
      try {
        args = parseArguments(process.argv.slice(2));
      } catch (err) {
        console.error(`❌ ${err.message}`);
        printUsage();
        process.exit(1);
      }

      if (args.help) {
        printUsage();
        return;
      }

      if (args.listAudioDevices) {
        await listAudioDevices();
        return;
      }

      if (!args.endpoint) {
        console.error(
          "❌ Missing endpoint. Set AZURE_VOICELIVE_ENDPOINT or pass --endpoint.",
        );
        process.exit(1);
      }

      if (!args.apiKey && !args.useTokenCredential) {
        console.error("❌ No authentication provided.");
        console.error(
          "Provide --api-key / AZURE_VOICELIVE_API_KEY or use --use-token-credential.",
        );
        process.exit(1);
      }

      const credential = args.useTokenCredential
        ? new DefaultAzureCredential()
        : new AzureKeyCredential(args.apiKey);

      console.log("Configuration:");
      console.log(`  AZURE_VOICELIVE_ENDPOINT: ${args.endpoint}`);
      console.log(`  AZURE_VOICELIVE_MODEL: ${args.model}`);
      console.log(`  AZURE_VOICELIVE_VOICE: ${args.voice}`);
      console.log(`  AUDIO_INPUT_DEVICE: ${args.audioInputDevice ?? "(not set)"}`);
      if (args.greetingText) {
        console.log(`  Proactive greeting: pre-defined`);
      } else {
        console.log(`  Proactive greeting: LLM-generated (default)`);
      }
      console.log(`  No audio mode: ${args.noAudio ? "enabled" : "disabled"}`);
      console.log(
        `  Authentication: ${args.useTokenCredential ? "DefaultAzureCredential" : "API Key"}`,
      );

      const assistant = new BasicModelVoiceAssistant({
        endpoint: args.endpoint,
        credential,
        model: args.model,
        voice: args.voice,
        instructions: args.instructions,
        audioInputDevice: args.audioInputDevice,
        greetingText: args.greetingText,
        noAudio: args.noAudio,
      });

      try {
        await assistant.start();
      } catch (err) {
        if (err?.code === "ERR_USE_AFTER_CLOSE") return;
        console.error("Fatal error:", err);
        process.exit(1);
      }
    }

    console.log("🎙️  Basic Voice Assistant with Azure VoiceLive SDK (Model Mode)");
    console.log("=".repeat(60));
    main().then(
      () => console.log("\n👋 Voice assistant shut down. Goodbye!"),
      (err) => {
        console.error("Unhandled error:", err);
        process.exit(1);
      },
    );
    ```

1. Run the voice assistant:

    ```shell
    node model-quickstart.js
    ```

    To use Microsoft Entra ID authentication instead of an API key, sign in first and add the `--use-token-credential` flag:

    ```shell
    az login
    node model-quickstart.js --use-token-credential
    ```

1. Start speaking with the model and hear responses. You can interrupt the model by speaking. Enter "Ctrl+C" to quit the conversation.

## Output

The output of the script is printed to the console. You see messages indicating the status of the connection, audio stream, and playback. The audio is played back through your speakers or headphones.

```text
🎙️  Basic Voice Assistant with Azure VoiceLive SDK (Model Mode)
============================================================

Configuration:
  AZURE_VOICELIVE_ENDPOINT: https://<your-resource>.cognitiveservices.azure.com/
  AZURE_VOICELIVE_MODEL: gpt-realtime
  AZURE_VOICELIVE_VOICE: en-US-Ava:DragonHDLatestNeural
  AUDIO_INPUT_DEVICE: (not set)
  Proactive greeting: LLM-generated (default)
  No audio mode: disabled
  Authentication: API Key

============================================================
🎤 VOICE ASSISTANT READY
Start speaking to begin conversation
Press Ctrl+C to exit
============================================================

🎤 Listening...
🤔 Processing...
👤 You said:	Hello.
🎤 Ready for next input...
🤖 Assistant text:	Hello! How can I assist you today?
🎤 Listening...
🤔 Processing...
👤 You said:	What's the capital of France?
🎤 Ready for next input...
🤖 Assistant text:	The capital of France is Paris. It's one of the most visited cities in the world, known for landmarks like the Eiffel Tower, the Louvre museum, and Notre-Dame Cathedral. Is there anything else you'd like to know?

👋 Voice assistant shut down. Goodbye!
```

A conversation log file is created in the `logs` folder with the name `conversation_YYYYMMDD_HHmmss.log`. This file contains session metadata and the conversation transcript.

```text
SessionID: sess_2n3aSMKTRqkKqacFPzRqUM
Model: gpt-realtime
Voice Name: en-US-Ava:DragonHDLatestNeural
Voice Type: azure-standard

User Input:	Hello.
Assistant Text Response:	Hello! How can I assist you today?
User Input:	What's the capital of France?
Assistant Text Response:	The capital of France is Paris...
```

Here are the key differences between the [technical log](#technical-log) and the [conversation log](#conversation-log):

| Aspect | Conversation Log | Technical Log |
|--------|-------------|---------------|
| **Audience** | Business users, content reviewers | Developers, IT operations |
| **Content** | What was said in conversations | How the system is working |
| **Level** | Application/conversation level | System/infrastructure level |
| **Troubleshooting** | "What did the model say?" | "Why did the connection fail?" |

**Example**: If your assistant wasn't responding, you'd check:
- **Console log** → "WebSocket connection failed" or "Audio stream error"
- **Conversation log** → "Did the user actually say anything?"

Both logs are complementary - conversation logs for conversation analysis and testing, technical logs for system diagnostics.

### Technical log
**Purpose**: Technical debugging and system monitoring

**Contents**:
- WebSocket connection events
- Audio stream status
- Error messages and stack traces
- System-level events (session.created, response.done, etc.)
- Network connectivity issues
- Audio processing diagnostics

**Format**: Console output with bracketed prefixes (for example, `[session]`, `[audio]`, `[init]`)

**Use cases**:
- Debugging connection problems
- Monitoring system performance
- Troubleshooting audio issues
- Developer/operations analysis

### Conversation log
**Purpose**: Conversation transcript and user experience tracking

**Contents**:
- Model and session identification
- Session configuration details
- **User transcripts**: "What's the weather today?", "Stop"
- **Model responses**: Full response text
- Conversation flow and interactions

**Format**: Plain text, human-readable conversation format

**Use cases**:
- Analyzing conversation quality
- Reviewing what was actually said
- Understanding user interactions and model responses
- Business/content analysis
