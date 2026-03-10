---
title: "Improve tool calling and latency wait times with interim responses"
description: "Learn how to use interim responses in Voice Live to bridge wait times during tool calls or high-latency agent responses, keeping conversations natural."
author: goergenj
ms.author: jagoerge
reviewer: patrickfarley
ms-reviewer: pafarley
ms.topic: how-to
ms.service: azure-ai-speech
ms.date: 01/28/2026
zone_pivot_groups: how-to-voice-live-interim-response
ai-usage: ai-assisted
---

# Improve tool calling and latency wait times (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

When a voice agent calls external tools or takes time to generate a response, users experience silence. Interim responses bridge these wait times with short spoken messages—keeping the conversation flowing naturally while work happens in the background.

Voice Live provides the `interim_response` session configuration to generate these bridging messages automatically. The feature supports both agent mode (Foundry Agent Service) and model mode.

> [!NOTE]
> In model mode, interim responses are only supported with text LLMs in cascaded mode together with `azure-speech` voice output. Realtime audio models don't support interim responses.

Voice Live offers two interim response modes:

- **LLM-generated interim response** (`llm_interim_response`): Uses a lightweight LLM to generate context-aware filler text dynamically. Best for adaptive, natural-sounding responses.
- **Static interim response** (`static_interim_response`): Randomly selects from a predefined list of texts you provide. Best for deterministic or branded messaging.

Both modes can be triggered by:

| Trigger | Description |
|---------|-------------|
| `latency` | Fires when response latency exceeds a configurable threshold (default: 2000 ms). |
| `tool` | Fires when a tool call is being executed. |

Triggers use OR logic—any matching trigger activates an interim response.

## Prerequisites

Before you start, complete the following:

- Complete the [Quickstart: Create a Voice Live real-time voice agent](./voice-live-agents-quickstart.md) or the [Quickstart: Get started with Voice Live](./voice-live-quickstart.md).
- A working Voice Live setup.
- A working event loop handling Voice Live events.

::: zone pivot="programming-language-python"

> [!IMPORTANT]
> Interim responses require `azure-ai-voicelive >= 1.0.0b5` and API version `2026-01-01-preview`. Install the preview SDK with:
>
> ```bash
> pip install azure-ai-voicelive --pre
> ```
>
> This SDK is currently in preview. Features and APIs might change before general availability.

::: zone-end

::: zone pivot="programming-language-csharp"

> [!IMPORTANT]
> Interim responses require `Azure.AI.VoiceLive >= 1.1.0-beta.3` and API version `2026-01-01-preview`. Install the preview SDK with:
>
> ```dotnetcli
> dotnet add package Azure.AI.VoiceLive --prerelease
> ```
>
> This SDK is currently in preview. Features and APIs might change before general availability.

::: zone-end

::: zone pivot="programming-language-java"

> [!IMPORTANT]
> Interim responses require `azure-ai-voicelive >= 1.0.0-beta.5` and API version `2026-01-01-preview`. Add the dependency with:
>
> ```xml
> <dependency>
>     <groupId>com.azure</groupId>
>     <artifactId>azure-ai-voicelive</artifactId>
>     <version>1.0.0-beta.5</version>
> </dependency>
> ```
>
> This SDK is currently in preview. Features and APIs might change before general availability.

::: zone-end

::: zone pivot="programming-language-javascript"

> [!IMPORTANT]
> Interim responses require `@azure/ai-voicelive >= 1.0.0-beta.3` and API version `2026-01-01-preview`. Install the preview SDK with:
>
> ```bash
> npm install @azure/ai-voicelive@1.0.0-beta.3
> ```
>
> This SDK is currently in preview. Features and APIs might change before general availability.

::: zone-end

## Configure LLM-generated interim responses

LLM-generated interim responses use a lightweight model (default: `gpt-4.1-mini`) to create context-aware bridging text. You can customize the instructions and token limits.

### Configuration parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Must be `llm_interim_response` (or equivalent SDK enum). |
| `triggers` | array | List of triggers: `latency`, `tool`, or both. Default: `["latency"]`. |
| `latency_threshold_ms` | integer | Milliseconds before the latency trigger fires. Default: 2000. Minimum: 0. |
| `model` | string | Model for generating interim text. Default: `gpt-4.1-mini`. |
| `instructions` | string | Custom prompt for the interim response LLM. |
| `max_completion_tokens` | integer | Maximum tokens for the generated response. Default: 50. Minimum: 1. |

::: zone pivot="programming-language-python"

### SDK configuration

```python
from azure.ai.voicelive.models import (
    LlmInterimResponseConfig,
    InterimResponseTrigger,
    RequestSession,
)

interim_response_config = LlmInterimResponseConfig(
    triggers=[InterimResponseTrigger.TOOL, InterimResponseTrigger.LATENCY],
    latency_threshold_ms=200,
    instructions="Create friendly interim responses indicating wait time "
                 "due to ongoing processing, if any. Do not include in "
                 "all responses!"
)

session_config = RequestSession(
    interim_response=interim_response_config,
    # ... other session options
)

await connection.session.update(session=session_config)
```

::: zone-end

::: zone pivot="programming-language-csharp"

### SDK configuration

```csharp
var interimConfig = new LlmInterimResponseConfig
{
    Instructions = "Create friendly interim responses indicating "
        + "wait time due to ongoing processing, if any. "
        + "Do not include in all responses!",
};
interimConfig.Triggers.Add(InterimResponseTrigger.Tool);
interimConfig.Triggers.Add(InterimResponseTrigger.Latency);
interimConfig.LatencyThresholdMs = 200;

var options = new VoiceLiveSessionOptions
{
    InterimResponse = BinaryData.FromObjectAsJson(interimConfig),
    // ... other session options
};

await session.ConfigureSessionAsync(options, cancellationToken);
```

::: zone-end

::: zone pivot="programming-language-java"

### SDK configuration

```java
LlmInterimResponseConfig interimResponseConfig = new LlmInterimResponseConfig()
        .setTriggers(Arrays.asList(
                InterimResponseTrigger.TOOL,
                InterimResponseTrigger.LATENCY))
        .setLatencyThresholdMs(200)
        .setInstructions("Create friendly interim responses indicating "
                + "wait time due to ongoing processing, if any. "
                + "Do not include in all responses!");

VoiceLiveSessionOptions sessionOptions = new VoiceLiveSessionOptions()
        .setInterimResponse(BinaryData.fromObject(interimResponseConfig));
        // ... other session options

session.sendEvent(new ClientEventSessionUpdate(sessionOptions)).block();
```

::: zone-end

::: zone pivot="programming-language-javascript"

### SDK configuration

```javascript
await session.updateSession({
    interimResponse: {
        type: "llm_interim_response",
        triggers: ["tool", "latency"],
        latencyThresholdInMs: 200,
        instructions:
            "Create friendly interim responses indicating wait time " +
            "due to ongoing processing, if any. " +
            "Do not include in all responses!",
    },
    // ... other session options
});
```

::: zone-end

## Configure static interim responses

Static interim responses select randomly from a predefined list of texts whenever a trigger fires. This approach gives you full control over what the agent says during wait times.

### Configuration parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Must be `static_interim_response` (or equivalent SDK enum). |
| `triggers` | array | List of triggers: `latency`, `tool`, or both. Default: `["latency"]`. |
| `latency_threshold_ms` | integer | Milliseconds before the latency trigger fires. Default: 2000. Minimum: 0. |
| `texts` | array | List of interim response text options to randomly select from. |

::: zone pivot="programming-language-python"

### Raw JSON configuration

Static interim responses can be sent as a raw `session.update` command:

```python
import json

static_config = {
    "type": "session.update",
    "session": {
        "interim_response": {
            "type": "static_interim_response",
            "triggers": ["tool", "latency"],
            "latency_threshold_ms": 1500,
            "texts": [
                "Let me look that up for you.",
                "One moment while I check on that.",
                "Just a second, I'm working on it."
            ]
        }
    }
}
await connection.send(json.dumps(static_config))
```

::: zone-end

::: zone pivot="programming-language-csharp"

### SDK configuration

```csharp
var staticConfig = new StaticInterimResponseConfig();
staticConfig.Texts.Add("Let me look that up for you.");
staticConfig.Texts.Add("One moment while I check on that.");
staticConfig.Texts.Add("Just a second, I'm working on it.");
staticConfig.Triggers.Add(InterimResponseTrigger.Tool);
staticConfig.Triggers.Add(InterimResponseTrigger.Latency);
staticConfig.LatencyThresholdMs = 1500;

var options = new VoiceLiveSessionOptions
{
    InterimResponse = BinaryData.FromObjectAsJson(staticConfig),
    // ... other session options
};

await session.ConfigureSessionAsync(options, cancellationToken);
```

::: zone-end

::: zone pivot="programming-language-java"

### Raw JSON configuration

```java
String staticConfig = """
    {
        "type": "session.update",
        "session": {
            "interim_response": {
                "type": "static_interim_response",
                "triggers": ["tool", "latency"],
                "latency_threshold_ms": 1500,
                "texts": [
                    "Let me look that up for you.",
                    "One moment while I check on that.",
                    "Just a second, I'm working on it."
                ]
            }
        }
    }
    """;
session.sendEvent(BinaryData.fromString(staticConfig)).block();
```

::: zone-end

::: zone pivot="programming-language-javascript"

### Raw JSON configuration

```javascript
await session.updateSession({
    interimResponse: {
        type: "static_interim_response",
        triggers: ["tool", "latency"],
        latencyThresholdInMs: 1500,
        texts: [
            "Let me look that up for you.",
            "One moment while I check on that.",
            "Just a second, I'm working on it.",
        ],
    },
});
```

::: zone-end

## Choose the right approach

| Requirement | LLM-generated | Static |
|-------------|---------------|--------|
| Context-aware, adaptive responses | ✔ | ✖ |
| Deterministic, predictable text | ✖ | ✔ |
| Brand-controlled language | Depending on instructions | ✔ |
| Conversational variety | ✔ | Limited to configured texts |
| No extra model inference cost | ✖ | ✔ |
| Minimal configuration | ✔ | Requires text list |

## Next steps

- Learn more about [How to use the Voice Live API](./voice-live-how-to.md)
- See the [Voice Live API reference](./voice-live-api-reference.md)
- Explore [How to add proactive messages](./how-to-voice-live-proactive-messages.md)
- Explore [How to handle voice interruptions](./how-to-voice-live-auto-truncation.md)
