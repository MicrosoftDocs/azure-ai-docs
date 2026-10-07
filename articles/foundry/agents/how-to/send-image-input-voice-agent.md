---
title: "Send image input to a voice agent"
description: "Learn how to send text and image input in one turn to a voice agent in Microsoft Foundry Agent Service and validate the response."
author: sdgilley
ms.author: sgilley
ms.date: 09/30/2026
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.custom: preview, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: voice-agent-image-input-language
# customer intent: As a developer, I want to send image context during a voice-agent session so that the agent can answer questions about visual information.
---

# Send image input to a voice agent

Send text and an image in the same turn to give a voice-based prompt agent visual context. This article shows how to connect to an existing voice agent, send an uploaded image, add optional camera frames, and validate the response lifecycle.

This workflow uses the Foundry Agent Service voice endpoint. It doesn't use the separate Voice Live API.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with access to voice-based agents.
- [Foundry User role](../../concepts/rbac-foundry.md) on the Foundry account.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]
- An existing voice-based prompt agent. To create one and complete a text turn, see [Create a voice-based prompt agent](../quickstarts/prompt-voice-agent.md).
- A model deployment that supports image input. A voice-capable model isn't necessarily image-capable. Confirm support for the deployment selected by your agent.
- A small, non-sensitive image for your first test. Don't use customer data, credentials, or screenshots that contain secrets.
- The Azure CLI, signed in with `az login`.
- The public voice-agent samples for [Python](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/voice-agents), [C#](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/VoiceAgents), [JavaScript](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents), [TypeScript](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/typescript/voice-agents), or [Java](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/java/voice-agents).

::: zone pivot="python"

- Python 3.10 or later.
- Version 2.7.0 or later of the Azure AI Projects client library with the `voice` extra. Install it with `python -m pip install "azure-ai-projects[voice]>=2.7.0" azure-identity`.
- The `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_VOICE_AGENT_NAME` environment variables from the [Python voice-agent quickstart](../quickstarts/prompt-voice-agent.md?pivots=python#set-environment-variables).

::: zone-end

::: zone pivot="csharp"

- .NET 8 or later.
- Version 3.0.0-beta.3 of `Azure.AI.Projects` and `Azure.AI.Projects.Agents`, version 2.14.0 of `OpenAI`, and `Azure.Identity`. Suppress the `AAIP001`, `AAIP002`, and `OPENAI002` preview diagnostics as shown in the public C# voice-agent samples.
- The `FOUNDRY_PROJECT_ENDPOINT` environment variable set to your project endpoint and `FOUNDRY_VOICE_AGENT_NAME` set to your existing voice-agent name.

::: zone-end

::: zone pivot="javascript"

- Node.js 22 or later.
- Version 2.7.0 or later of the Azure AI Projects client library. Install it with `npm install @azure/ai-projects@2.7.0 @azure/identity`.
- The `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_VOICE_AGENT_NAME` environment variables from the [JavaScript voice-agent quickstart](../quickstarts/prompt-voice-agent.md?pivots=javascript#set-environment-variables).

::: zone-end

::: zone pivot="java"

- JDK 8 or later and Apache Maven.
- Version 2.6.0 or later of the Azure AI Agents client library for Java. The public Java voice-agent samples declare `com.azure:azure-ai-agents:2.6.0` and `com.azure:azure-identity:1.18.6`.
- The `FOUNDRY_PROJECT_ENDPOINT` environment variable set to your project endpoint and `FOUNDRY_VOICE_AGENT_NAME` set to your existing voice-agent name.

::: zone-end

## Understand an image turn

An image turn sends one `conversation.item.create` event with a user message. The message contains these ordered content parts:

1. An `input_text` part that asks a question about the image.
1. An `input_image` part whose `image_url` value is a Base64 data URL.

After you add the message, send one `response.create` event. Don't request another response while the first response is active.

The connection uses the voice-agent route relative to the Foundry project endpoint:

`wss://<project-endpoint-host>/<project-endpoint-path>/agents/<agent-name>/endpoint/protocols/voice?api-version=v1`

Preserve the existing project endpoint path, and URL-encode the agent name. A native SDK client supplies Microsoft Entra authentication. A browser client requires an authenticated server-side proxy because browser WebSockets can't set an arbitrary `Authorization` header. Never put a bearer token in the WebSocket URL.

## Connect to the voice agent

Start with the connection and response-handling pattern from the voice-agent quickstart. Wait for the session to be ready before you send image input. An open WebSocket connection alone doesn't indicate that the session is ready.

::: zone pivot="python"

Use `AIProjectClient` with `DefaultAzureCredential`, and open the connection through `project_client.beta.voice_agents.realtime.connect`. If the agent has a greeting, receive its complete response before you send the image turn.

The Python 2.7.0 SDK exposes `input_image`, `image_url`, and `detail` through `RealtimeConversationItemMessageUserContent`.

Use the public [Python realtime text sample](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/voice-agents/voice_agent_realtime_text_conversation.py) for the connection, event loop, response timeout, error handling, and cleanup pattern.

::: zone-end

::: zone pivot="csharp"

Use `AIProjectClient` with `DefaultAzureCredential`, and open the connection through `ProjectsRealtimeClient.StartSessionAsync`. The returned `ProjectsRealtimeSessionClient` uses the same realtime command and event model as the OpenAI .NET client.

Version 3.0.0-beta.3 doesn't expose a typed factory for an image content part. Use the session's protocol-method overload, `SendCommandAsync(BinaryData, RequestOptions)`, to send the complete, verified client event.

Use the public [C# realtime text and tools sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/VoiceAgents/realtime-text-and-tools) for the connection and response lifecycle.

::: zone-end

::: zone pivot="javascript"

Use `AIProjectClient` with `DefaultAzureCredential`, and open the connection through `project.beta.voiceAgents.realtime.connect`. Configure the session, and receive the agent's greeting before you send the image turn.

The JavaScript 2.7.0 SDK exposes `input_image`, `image_url`, and `detail` through `RealtimeConversationItemMessageUserContent`. `VoiceAgentConnection.sendEvent` sends the complete client protocol event.

Use the public [JavaScript realtime text and tools sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/realtime-text-and-tools) or its [TypeScript equivalent](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/typescript/voice-agents/realtime-text-and-tools) for the connection and response lifecycle. For a browser application, start with the [browser voice console](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/browser-voice-console) so authentication remains on the server.

::: zone-end

::: zone pivot="java"

Use `AgentsClientBuilder` with `DefaultAzureCredentialBuilder`, enable preview APIs with `allowPreview(true)`, and create a `BetaVoiceAgentWebSocketSessionClient` through `BetaVoiceAgentWebSocketClient.openWebSocketSession`.

Version 2.6.0 doesn't expose a typed image content model. Use the session's `sendEvent(BinaryData)` overload to send the complete, verified client event.

Use the public [Java realtime text sample](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/java/voice-agents/src/main/java/com/azure/ai/agents/voice/VoiceAgentLiveTextConversationSample.java) for the connection, receive loop, timeout, response handling, and cleanup pattern.

::: zone-end

## Send text and an image

Read the image as bytes, encode the bytes as Base64, and prefix the encoded value with the image's media type. For example, a PNG data URL starts with `data:image/png;base64,`.

Don't log the data URL. It contains the complete image and can be much larger than the original binary value.

The sample clients accept one JPEG, PNG, or WebP image up to 8 MiB and send it with `detail` set to `low`. These values are sample choices, not published service or model requirements.

::: zone pivot="python"

1. Read the image and construct its Base64 data URL.
1. Create a `RealtimeConversationItemMessageUser`.
1. Add a `RealtimeConversationItemMessageUserContent` value with `type="input_text"` and the question.
1. Add a second content value with `type="input_image"`, the data URL in `image_url`, and the selected image detail.
1. Call `conn.conversation.item.create` once with the user message.
1. Call `conn.response.create` once.

:::code language="python" source="~/foundry-samples-main/samples/python/voice-agents/voice_agent_realtime_image_conversation.py" id="image_turn":::

Expected output:

```output
Agent: <answer based on the image>
```

::: zone-end

::: zone pivot="csharp"

1. Read the image and construct its Base64 data URL.
1. Create an object for the complete `conversation.item.create` event.
1. Add an `input_text` content part with the question.
1. Add an `input_image` content part with the data URL in `image_url` and the selected image detail.
1. Serialize the event with `BinaryData.FromObjectAsJson`.
1. Call `session.SendCommandAsync` once with the serialized event.
1. Call `session.StartResponseAsync` once.

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/VoiceAgents/realtime-image-input/RealtimeImageInput.cs" id="image_turn":::

Expected output:

```output
<answer based on the image>
```

::: zone-end

::: zone pivot="javascript"

1. Read the image and construct its Base64 data URL.
1. Create a `conversation.item.create` event whose item has `type: "message"` and `role: "user"`.
1. Add an `input_text` content part with the question.
1. Add an `input_image` content part with the data URL in `image_url` and the selected image detail.
1. Pass the event to `connection.sendEvent`.
1. Call `connection.requestResponse` once.

### JavaScript

:::code language="javascript" source="~/foundry-samples-main/samples/javascript/voice-agents/realtime-image-input/app.js" id="image_turn":::

Expected output:

```output
Agent: <answer based on the image>
```

### TypeScript

:::code language="typescript" source="~/foundry-samples-main/samples/typescript/voice-agents/realtime-image-input/src/voice-agents-realtime-image-input.ts" id="image_turn":::

Expected output:

```output
Agent: <answer based on the image>
```

::: zone-end

::: zone pivot="java"

1. Read the image and construct its Base64 data URL.
1. Create maps for the complete `conversation.item.create` event and its ordered content parts.
1. Add an `input_text` content part with the question.
1. Add an `input_image` content part with the data URL in `image_url` and the selected image detail.
1. Serialize the event with `BinaryData.fromObject`.
1. Call `session.sendEvent` once with the serialized event.
1. Call `session.createResponse` once.

:::code language="java" source="~/foundry-samples-main/samples/java/voice-agents/src/main/java/com/azure/ai/agents/voice/VoiceAgentLiveImageConversationSample.java" id="image_turn":::

Expected output:

```output
Agent: <answer based on the image>
```

::: zone-end

If the user doesn't provide a question, the sample clients use `Describe this image briefly.` This default is sample behavior, not a service requirement.

## Add camera context

Camera context uses the same `input_image` content part as an uploaded image. A browser client can capture a JPEG frame approximately every two seconds instead of streaming continuous video.

1. Request camera permission only after the user starts the camera.
1. Add each sampled frame as a user conversation item.
1. Don't send `response.create` for each camera frame.
1. Send a text or audio turn when the user wants the agent to respond to the retained visual context.
1. Stop the camera to release the device.

The reference client retains three frames by default and allows a value from one through five. These values are client choices, not service limits. Camera access requires `localhost` or HTTPS and browser permission. Cleanup of remote context is best effort when a connection closes unexpectedly.

## Validate the response

Process server events until the response reaches a terminal state:

- Treat `session.created` and `session.updated` as session-readiness signals.
- Handle `error` events and unexpected connection closure explicitly.
- Collect text, audio, or audio-transcript deltas according to the agent's output configuration.
- On `response.done`, check that the response status is `completed`.

A `conversation.item.created` event confirms that the service accepted the item. It doesn't prove that the model understood the image. Verify the answer against the actual image.

## Distinguish model input, storage, and traces

The `input_image` content part is the model-input path. Conversation storage and content capture are separate settings with separate data-retention effects. Setting `store` to `true` doesn't enable trace content capture.

Image tracing doesn't require an image-specific setting. When approved [content capture](../../observability/how-to/traces-sensitive-content.md) is enabled, traces can contain model inputs and outputs, including customer content. Protect `gen_ai.input.messages` by applying the trace access and retention controls described in [Manage sensitive content in traces](../../observability/how-to/traces-sensitive-content.md).

A correct model answer doesn't prove that tracing is enabled, and a trace that contains an image doesn't prove visual understanding.

Use synthetic data when you test. Image previews remain in browser memory, and content capture can retain image data. Don't share Base64 data, signed URLs, bearer tokens, raw wire payloads, or unreviewed log exports.

## Troubleshoot image turns

| Symptom | Check |
|---|---|
| The text-only turn works, but the image turn fails | Confirm that the selected model deployment supports image input. |
| The client rejects the file | Check the client sample's media-type and size validation. Don't treat those values as service limits. |
| The browser shows a preview, but the answer ignores the image | Confirm that the client sent an `input_image` part and requested one response after the item. |
| The service reports an active response | Wait for the current `response.done` event before requesting another response. |
| The image turn is sent before the greeting completes | Wait for the greeting's terminal response and session-readiness events. |
| The camera doesn't start | Use `localhost` or HTTPS, grant browser permission, and confirm that another application isn't holding the camera. |
| A trace doesn't contain the image | Confirm that approved content capture is enabled. Don't use an empty telemetry query alone as proof that capture is disabled. |

## Related content

- [Create a voice-based prompt agent](../quickstarts/prompt-voice-agent.md)
- [Configure a voice agent](configure-voice-agent.md)
- [Monitor voice agents](../concepts/voice-agent-observability.md)
