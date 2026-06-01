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

Learn how to use function calling in a Voice Live session using the VoiceLive SDK for JavaScript. This article builds on the [Quickstart: Get started with Voice Live for real-time voice agents](../../../voice-live-quickstart.md) by adding function calling so the assistant can invoke backend tools during a conversation.

[!INCLUDE [Header](../../common/voice-live-javascript.md)]

[!INCLUDE [Implementation steps](intro.md)]

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [Node.js](https://nodejs.org/) version 18 or later.
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- The `@azure/ai-voicelive`, `@azure/core-auth`, `@azure/identity`, `dotenv`, and `speaker` packages installed.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

> [!IMPORTANT]
> The `speaker` package is a native Node.js addon that requires C++ build tools to compile. On Windows, install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022) with the **Desktop development with C++** workload and `node-gyp` (`npm install --global node-gyp`) before running `npm install`. On macOS, Xcode Command Line Tools (`xcode-select --install`) are sufficient.

> [!IMPORTANT]
> This sample requires [SoX](https://sox.sourceforge.io/) for microphone capture. Install it before running the sample — on Windows via `winget install SoX.SoX` or [Chocolatey](https://chocolatey.org/) (`choco install sox.portable`), on macOS via [Homebrew](https://brew.sh/) (`brew install sox`).

> [!NOTE]
> The `gpt-realtime` model isn't available in all regions. If you get a connection error, verify that your resource is in a [supported region](/azure/ai-services/speech-service/regions?tabs=voice-live). The `gpt-4o` and `gpt-4.1` models have broader regional availability.

## Prepare the environment

Before you continue, complete the [Quickstart: Get started with Voice Live for real-time voice agents](../../../voice-live-quickstart.md) to set up your Foundry resource, install the VoiceLive SDK for JavaScript, configure authentication, and verify that you can run a basic Voice Live conversation end-to-end. The function calling sample in this article reuses the same resource, credentials, and environment variables.

Install the required packages:

```shell
npm install @azure/ai-voicelive @azure/core-auth @azure/identity dotenv speaker
```

## Sample code

The following sample extends the basic Voice Live conversation from the [Quickstart: Get started with Voice Live for real-time voice agents](../../../voice-live-quickstart.md) by registering two function tools (`get_current_time` and `get_current_weather`) and handling the function call events the service returns.

```javascript
// -------------------------------------------------------------------------
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
// -------------------------------------------------------------------------
import "dotenv/config";
import { VoiceLiveClient } from "@azure/ai-voicelive";
import { AzureKeyCredential } from "@azure/core-auth";
import { DefaultAzureCredential } from "@azure/identity";
import { spawn } from "node:child_process";

// ---------------------------------------------------------------------------
// Backend functions
// ---------------------------------------------------------------------------

function getCurrentTime(args) {
  const timezone = args?.timezone ?? "local";
  const now = new Date();
  const timezoneName =
    timezone.toLowerCase() === "utc" ? "UTC" : "local";
  const options = timezone.toLowerCase() === "utc"
    ? { timeZone: "UTC" }
    : {};

  return {
    time: now.toLocaleTimeString("en-US", {
      hour12: true,
      ...options,
    }),
    date: now.toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
      ...options,
    }),
    timezone: timezoneName,
  };
}

function getCurrentWeather(args) {
  const location = args?.location ?? "Unknown";
  const unit = args?.unit ?? "celsius";

  // Simulated weather response
  return {
    location,
    temperature: unit === "celsius" ? 22 : 72,
    unit,
    condition: "Partly Cloudy",
    humidity: 65,
    wind_speed: 10,
  };
}

const availableFunctions = {
  get_current_time: getCurrentTime,
  get_current_weather: getCurrentWeather,
};

// ---------------------------------------------------------------------------
// Audio processor - microphone capture and speaker playback
// ---------------------------------------------------------------------------

class AudioProcessor {
  constructor() {
    this._soxProcess = null;
    this._speaker = null;
    this._speakerCtor = null;
    this._skipSeq = 0;
    this._nextSeq = 0;
  }

  async startCapture(session) {
    if (this._soxProcess) return;

    const soxArgs = [
      "-q", "-d",
      "-r", "24000", "-c", "1",
      "-e", "signed-integer", "-b", "16",
      "-t", "raw", "-",
    ];

    this._soxProcess = spawn("sox", soxArgs, {
      stdio: ["ignore", "pipe", "pipe"],
    });

    this._soxProcess.stdout.on("data", (chunk) => {
      if (session.isConnected) {
        session.sendAudio(new Uint8Array(chunk)).catch(() => {});
      }
    });

    this._soxProcess.stderr.on("data", () => {});

    this._soxProcess.on("error", (err) => {
      console.error(`SoX process error: ${err.message}`);
    });

    console.log("[audio] Microphone capture started");
  }

  async startPlayback() {
    if (this._speaker) return;
    const speakerModule = await import("speaker");
    this._speakerCtor = speakerModule.default;
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
    this._skipSeq = this._nextSeq++;
    this._resetSpeaker().catch(() => {});
  }

  shutdown() {
    if (this._soxProcess) {
      try { this._soxProcess.kill(); } catch { /* no-op */ }
      this._soxProcess = null;
    }
    if (this._speaker) {
      this._speaker.end();
      this._speaker = null;
    }
    console.log("[audio] Audio processor shut down");
  }

  async _resetSpeaker() {
    if (this._speaker && !this._speaker.destroyed) {
      try { this._speaker.end(); } catch { /* no-op */ }
    }
    this._speaker = new this._speakerCtor({
      channels: 1,
      bitDepth: 16,
      sampleRate: 24000,
      signed: true,
    });
    this._speaker.on("error", () => {});
  }
}

// ---------------------------------------------------------------------------
// Voice assistant with function calling
// ---------------------------------------------------------------------------

function resolveVoiceConfig(voiceName) {
  const looksLikeAzure =
    voiceName.includes("-") || voiceName.includes(":");
  return looksLikeAzure
    ? { type: "azure-standard", name: voiceName }
    : { type: "openai", name: voiceName };
}

class FunctionCallingAssistant {
  constructor(options) {
    this.endpoint = options.endpoint;
    this.credential = options.credential;
    this.model = options.model;
    this.voice = options.voice;
    this.instructions = options.instructions;
    this._session = null;
    this._subscription = null;
    this._audio = new AudioProcessor();
    this._activeResponse = false;
    this._responseApiDone = false;
    this._pendingFunctionCall = null;
  }

  async start() {
    const client = new VoiceLiveClient(
      this.endpoint,
      this.credential,
    );
    const session = client.createSession({
      model: this.model,
    });
    this._session = session;

    this._subscription = session.subscribe({
      onSessionUpdated: async () => {
        console.log("[session] Session ready");
        await this._audio.startCapture(session);
      },

      onInputAudioBufferSpeechStarted: async () => {
        console.log("Listening...");
        this._audio.skipPendingAudio();
        if (this._activeResponse && !this._responseApiDone) {
          try {
            await session.sendEvent({
              type: "response.cancel",
            });
          } catch (err) {
            const msg = err?.message ?? "";
            if (
              !msg
                .toLowerCase()
                .includes("no active response")
            ) {
              console.warn("Cancel failed:", msg);
            }
          }
        }
      },

      onInputAudioBufferSpeechStopped: async () => {
        console.log("Processing...");
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
        console.log("Ready for next input...");
      },

      onResponseDone: async () => {
        console.log("Response complete");
        this._activeResponse = false;
        this._responseApiDone = true;

        if (this._pendingFunctionCall?.arguments) {
          await this._executeFunctionCall(
            this._pendingFunctionCall,
          );
          this._pendingFunctionCall = null;
        }
      },

      onConversationItemCreated: async (event) => {
        if (event.item?.type === "function_call") {
          this._pendingFunctionCall = {
            name: event.item.name,
            callId: event.item.call_id,
            previousItemId: event.item.id,
          };
          console.log(
            `Calling function: ${event.item.name}`,
          );
        }
      },

      onResponseFunctionCallArgumentsDone: async (
        event,
      ) => {
        if (
          this._pendingFunctionCall &&
          event.call_id ===
            this._pendingFunctionCall.callId
        ) {
          this._pendingFunctionCall.arguments =
            event.arguments;
        }
      },

      onServerError: async (event) => {
        const msg = event.error?.message ?? "";
        if (!msg.includes("no active response")) {
          console.error(`VoiceLive error: ${msg}`);
        }
      },
    });

    await session.connect();
    await this._setupSession();
    await this._audio.startPlayback();

    // Proactive greeting
    await session.sendEvent({ type: "response.create" });

    console.log("\n" + "=".repeat(60));
    console.log(
      "VOICE ASSISTANT WITH FUNCTION CALLING READY",
    );
    console.log("Try saying:");
    console.log("  - 'What's the current time?'");
    console.log("  - 'What's the weather in Seattle?'");
    console.log("Press Ctrl+C to exit");
    console.log("=".repeat(60) + "\n");

    await new Promise((resolve) => {
      process.once("SIGINT", resolve);
      process.once("SIGTERM", resolve);
    });

    await this.shutdown();
  }

  async _setupSession() {
    await this._session.updateSession({
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
      inputAudioEchoCancellation: {
        type: "server_echo_cancellation",
      },
      inputAudioNoiseReduction: {
        type: "azure_deep_noise_suppression",
      },
      inputAudioTranscription: { model: "whisper-1" },
      tools: [
        {
          type: "function",
          name: "get_current_time",
          description: "Get the current time",
          parameters: {
            type: "object",
            properties: {
              timezone: {
                type: "string",
                description:
                  "The timezone, e.g., 'UTC', 'local'",
              },
            },
            required: [],
          },
        },
        {
          type: "function",
          name: "get_current_weather",
          description:
            "Get the current weather in a given location",
          parameters: {
            type: "object",
            properties: {
              location: {
                type: "string",
                description:
                  "The city and state, " +
                  "e.g., 'San Francisco, CA'",
              },
              unit: {
                type: "string",
                enum: ["celsius", "fahrenheit"],
                description:
                  "The unit of temperature " +
                  "(celsius or fahrenheit)",
              },
            },
            required: ["location"],
          },
        },
      ],
      toolChoice: "auto",
    });

    console.log(
      "[session] Session configured with function tools",
    );
  }

  async _executeFunctionCall(callInfo) {
    const { name, callId, arguments: argsStr } = callInfo;
    const func = availableFunctions[name];
    if (!func) {
      console.error(`Unknown function: ${name}`);
      return;
    }

    try {
      const args = JSON.parse(argsStr);
      const result = func(args);

      await this._session.addConversationItem({
        type: "function_call_output",
        call_id: callId,
        output: JSON.stringify(result),
      });
      console.log(`Function ${name} completed`);

      // Request a new response that incorporates
      // the function result
      await this._session.sendEvent({
        type: "response.create",
      });
    } catch (err) {
      console.error(
        `Error executing function ${name}: ` +
          err.message,
      );
    }
  }

  async shutdown() {
    if (this._subscription) {
      await this._subscription.close();
      this._subscription = null;
    }
    if (this._session) {
      try {
        await this._session.disconnect();
      } catch { /* no-op */ }
      this._audio.shutdown();
      try {
        await this._session.dispose();
      } catch { /* no-op */ }
      this._session = null;
    }
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

const args = {
  apiKey: process.env.AZURE_VOICELIVE_API_KEY,
  endpoint: process.env.AZURE_VOICELIVE_ENDPOINT,
  model:
    process.env.AZURE_VOICELIVE_MODEL ?? "gpt-realtime",
  voice:
    process.env.AZURE_VOICELIVE_VOICE ??
    "en-US-Ava:DragonHDLatestNeural",
  instructions:
    process.env.AZURE_VOICELIVE_INSTRUCTIONS ??
    "You are a helpful AI assistant with access to " +
      "functions. Use the functions when appropriate " +
      "to provide accurate, real-time information. " +
      "Always start the conversation in English.",
  useTokenCredential: process.argv.includes(
    "--use-token-credential",
  ),
};

if (!args.endpoint) {
  console.error(
    "Missing endpoint. Set AZURE_VOICELIVE_ENDPOINT.",
  );
  process.exit(1);
}

if (!args.apiKey && !args.useTokenCredential) {
  console.error(
    "No auth. Provide AZURE_VOICELIVE_API_KEY " +
      "or --use-token-credential.",
  );
  process.exit(1);
}

const credential = args.useTokenCredential
  ? new DefaultAzureCredential()
  : new AzureKeyCredential(args.apiKey);

const assistant = new FunctionCallingAssistant({
  endpoint: args.endpoint,
  credential,
  model: args.model,
  voice: args.voice,
  instructions: args.instructions,
});

assistant.start().then(
  () => console.log("\nVoice assistant shut down."),
  (err) => {
    if (err?.code === "ERR_USE_AFTER_CLOSE") return;
    console.error("Fatal error:", err);
    process.exit(1);
  },
);
```
