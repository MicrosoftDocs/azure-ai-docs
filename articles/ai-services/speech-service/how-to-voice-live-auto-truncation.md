---
title: "Handle voice interruptions in chat history"
description: "Learn how to automatically truncate conversation text results to match audio when users interrupt Voice Live agent responses during playback."
author: goergenj
ms.author: jagoerge
reviewer: patrickfarley
ms-reviewer: pafarley
ms.topic: how-to
ms.service: azure-ai-speech
ms.date: 01/28/2026
zone_pivot_groups: how-to-voice-live-auto-truncation
ai-usage: ai-assisted
---

# Handle voice interruptions in chat history (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A common scenario with voice agents is when users interrupt the audio playback of agent responses. The Voice Live service generates and returns audio responses to the client, but users might not listen to complete responses—they often interrupt by speaking again before the response finishes. This creates a mismatch between the actual audio conversation and the transcribed conversation results used to log conversation history.

In this case, the session context should be updated to reflect what the user actually heard. Otherwise, the LLM would assume it said something that was never actually delivered to the user.
  
## Prerequisites

Before starting, we recommend you have:

- Completed the [Quickstart: Create a Voice Live real-time voice agent](./voice-live-quickstart.md).
- A working Voice Live setup.
- A working event loop handling Voice Live events.

::: zone pivot="programming-language-python"

> [!IMPORTANT]
> Auto truncation requires `azure-ai-voicelive >= 1.2.0b2` and API version `2026-01-01-preview`. Install the preview SDK with:
>
> ```bash
> pip install azure-ai-voicelive --pre
> ```
>
> This SDK is currently in preview. Features and APIs may change before general availability.

::: zone-end

::: zone pivot="programming-language-csharp"

> [!IMPORTANT]
> Auto truncation requires `Azure.AI.VoiceLive >= 1.1.0-beta.1` and API version `2026-01-01-preview`. Install the preview SDK with:
>
> ```dotnetcli
> dotnet add package Azure.AI.VoiceLive --prerelease
> ```
>
> This SDK is currently in preview. Features and APIs may change before general availability.

::: zone-end

::: zone pivot="programming-language-java"

> [!IMPORTANT]
> Auto truncation requires `azure-ai-voicelive >= 1.0.0-beta.3` and API version `2026-01-01-preview`. Add the preview dependency to your `pom.xml`:
>
> ```xml
> <dependency>
>     <groupId>com.azure</groupId>
>     <artifactId>azure-ai-voicelive</artifactId>
>     <version>1.0.0-beta.3</version>
> </dependency>
> ```
>
> This SDK is currently in preview. Features and APIs may change before general availability.

::: zone-end

::: zone pivot="programming-language-javascript"

> [!IMPORTANT]
> Auto truncation requires `@azure/ai-voicelive >= 1.0.0-beta.2` and API version `2026-01-01-preview`. This SDK requires Node.js 20 or later. Install the preview SDK with:
>
> ```bash
> npm install @azure/ai-voicelive@1.0.0-beta.2
> ```
>
> This SDK is currently in preview. Features and APIs may change before general availability.

::: zone-end

## Parameters

Two parameters are introduced to handle this scenario:

### `auto_truncate`

When `auto_truncate` is set to `true` in VAD configuration, the service automatically truncates the last turn's response when it detects user speech during playback. The service assumes the response is played at real-time speed.

**Dependencies:**

- `interrupt_response` must be set to `true` (default). Auto truncation only makes sense when response interruption is enabled—if the response continues playing after the user speaks, there's nothing to truncate.

When truncation occurs:

1. The session context is updated to include only the portion of the response played before the user started speaking.
2. A `conversation.item.truncated` message is returned to the client.

### `appended_text_after_truncation`

Sometimes developers may want to inform the LLM that the user interrupted the response, rather than simply truncating it silently. In this case, `appended_text_after_truncation` can be set to a string value.

When truncation occurs, the service appends this string to the truncated response before updating the session context.

**Example:**

- `appended_text_after_truncation`: `" [The user interrupted me.]"`
- Original response: `"Hello, how can I help you today?"`
- User interrupts after: `"Hello, how"`
- Final context stored: `"Hello, how [The user interrupted me.]"`

> **Note:** When using this feature, developers should update the system prompt to inform the LLM about this behavior and test carefully to avoid unexpected results.

## Supported VAD Types

| VAD Type                         | `auto_truncate` | `appended_text_after_truncation` |
| -------------------------------- | --------------- | -------------------------------- |
| `azure_semantic_vad`             | ✅               | ✅                                |
| `azure_semantic_vad_multilingual`| ✅               | ✅                                |
| `server_vad`                     | ✅               | ❌                                |
| `semantic_vad` (OpenAI)          | ✅               | ❌                                |

## Example Configuration

::: zone pivot="programming-language-python"
```python
from azure.ai.voicelive.models import (
    RequestSession,
    AzureSemanticVadTurnDetection,
)

# Configure session with auto truncation enabled
session_config = RequestSession(
    instructions="You are a helpful assistant.",
    turn_detection=AzureSemanticVadTurnDetection(
        interrupt_response=True,
        auto_truncate=True,
        appended_text_after_truncation=" [The user interrupted me.]"
    )
)

await conn.session.update(session=session_config)
```
::: zone-end

::: zone pivot="programming-language-csharp"
```csharp
using Azure.AI.VoiceLive;

// Configure session with auto truncation enabled
var sessionOptions = new VoiceLiveSessionOptions
{
    Instructions = "You are a helpful assistant.",
    TurnDetection = new AzureSemanticVadTurnDetection
    {
        InterruptResponse = true,
        AutoTruncate = true,
        AppendedTextAfterTruncation = " [The user interrupted me.]"
    }
};

await session.ConfigureSessionAsync(sessionOptions).ConfigureAwait(false);
```
::: zone-end

::: zone pivot="programming-language-java"
```java
import com.azure.ai.voicelive.models.*;

// Configure session with auto truncation enabled
AzureSemanticVadTurnDetection turnDetection = new AzureSemanticVadTurnDetection()
    .setInterruptResponse(true)
    .setAutoTruncate(true)
    .setAppendedTextAfterTruncation(" [The user interrupted me.]");

RequestSession sessionConfig = new RequestSession()
    .setInstructions("You are a helpful assistant.")
    .setTurnDetection(turnDetection);

session.sendEvent(new ClientEventSessionUpdate().setSession(sessionConfig)).subscribe();
```
::: zone-end

::: zone pivot="programming-language-javascript"
```javascript
// Configure session with auto truncation enabled
await session.updateSession({
    instructions: "You are a helpful assistant.",
    turnDetection: {
        type: "azure_semantic_vad",
        interruptResponse: true,
        autoTruncate: true,
        appendedTextAfterTruncation: " [The user interrupted me.]"
    }
});
```
::: zone-end

The equivalent JSON payload for the session configuration:

```json
{
  "turn_detection": {
    "type": "azure_semantic_vad",
    "interrupt_response": true,
    "auto_truncate": true,
    "appended_text_after_truncation": " [The user interrupted me.]"
  }
}
```

## Handling the truncation event

When truncation occurs, the service sends a `conversation.item.truncated` event. You can handle this event in your event loop:

::: zone pivot="programming-language-python"
```python
async def _handle_event(self, event):
    if event.type == ServerEventType.CONVERSATION_ITEM_TRUNCATED:
        print(f"Response was truncated. Item ID: {event.item_id}")
        print(f"Truncated at index: {event.content_index}")
        # Log or handle the truncation as needed
```
::: zone-end

::: zone pivot="programming-language-csharp"
```csharp
private async Task HandleSessionUpdateAsync(SessionUpdate serverEvent, CancellationToken cancellationToken)
{
    if (serverEvent is SessionUpdateConversationItemTruncated truncatedEvent)
    {
        Console.WriteLine($"Response was truncated. Item ID: {truncatedEvent.ItemId}");
        Console.WriteLine($"Truncated at index: {truncatedEvent.ContentIndex}");
        // Log or handle the truncation as needed
    }
}
```
::: zone-end

::: zone pivot="programming-language-java"
```java
private void handleServerEvent(SessionUpdate event) {
    if (event.getType() == ServerEventType.CONVERSATION_ITEM_TRUNCATED) {
        SessionUpdateConversationItemTruncated truncatedEvent = 
            (SessionUpdateConversationItemTruncated) event;
        System.out.println("Response was truncated. Item ID: " + truncatedEvent.getItemId());
        System.out.println("Truncated at index: " + truncatedEvent.getContentIndex());
        // Log or handle the truncation as needed
    }
}
```
::: zone-end

::: zone pivot="programming-language-javascript"
```javascript
const subscription = session.subscribe({
    onConversationItemTruncated: async (event, context) => {
        console.log(`Response was truncated. Item ID: ${event.itemId}`);
        console.log(`Truncated at index: ${event.contentIndex}`);
        // Log or handle the truncation as needed
    }
});
```
::: zone-end

## Next steps

- Learn more about [How to use the Voice Live API](./voice-live-how-to.md)
- See the [Voice Live API reference](./voice-live-api-reference.md)
- Explore [How to add proactive messages](./how-to-voice-live-proactive-messages.md)
