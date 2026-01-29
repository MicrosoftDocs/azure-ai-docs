---
title: "How to add proactive messages to a Voice Live real-time voice agent"
description: "Learn how to make your Voice Live agent speak first by triggering proactive greetings using pregenerated assistant messages or LLM-generated messages."
author: goergenj
ms.author: jagoerge
reviewer: patrickfarley
ms-reviewer: pafarley
ms.topic: how-to
ms.service: azure-ai-voicelive
ms.date: 01/28/2026
---

# How to add proactive messages to a Voice Live real-time voice agent

Proactive engagement allows your Voice Live agent to **speak first**, before the user interacts with the system. This can make agents feel more natural, more helpful, and more responsive at the start of a conversation.  

This article shows how to implement proactive messages, building on the event‑loop pattern introduced in the *Get started with Voice Live for real-time voice agents* quickstart.  

Voice Live offers two supported methods:

- **Pre-generated greeting** - best for deterministic or branded messaging
- **LLM-generated greeting** - best for dynamic and adaptive starts

Both methods integrate naturally with the session event loop and ensure the message becomes part of the conversation context.

Use the approach that best matches your product and conversational goals.

You'll learn:

- How proactive messaging fits into the event loop
- How to track conversation start  
  
## Prerequisites

Before starting, we recommend you have:

- Completed the [Quickstart: Create a voice live real-time voice agent](./voice-live-quickstart.md).
- A working Voice Live setup.
- A working event loop handling Voice Live events.

## How proactive messages integrate with the event loop

Voice Live applications typically process events using an asynchronous loop:

::: zone pivot="programming-language-python"
```python
async for event in conn:
    await self._handle_event(event)
```
::: zone-end

::: zone pivot="programming-language-csharp"
```csharp
await foreach (SessionUpdate serverEvent in session.GetUpdatesAsync(cancellationToken))
{
    await HandleSessionUpdateAsync(serverEvent, cancellationToken);
}
```
::: zone-end

::: zone pivot="programming-language-java"
```java
session.receiveEvents()
    .subscribe(
        event -> handleServerEvent(event, audioProcessor),
        error -> System.err.println("Error: " + error.getMessage())
    );
```
::: zone-end

::: zone pivot="programming-language-javascript"
```javascript
const subscription = session.subscribe({
    onSessionUpdated: async (event, context) => {
        await handleEvent(event);
    }
});
```
::: zone-end

When a session is ready, the service sends a `SESSION_UPDATED` event. This is the ideal moment to initiate proactive engagement.

Because the greeting should only happen once per session, you track state:

::: zone pivot="programming-language-python"
```python
self.greeting_sent = False
```
::: zone-end

::: zone pivot="programming-language-csharp"
```csharp
private bool _greetingSent = false;
```
::: zone-end

::: zone pivot="programming-language-java"
```java
private AtomicBoolean greetingSent = new AtomicBoolean(false);
```
::: zone-end

::: zone pivot="programming-language-javascript"
```javascript
let greetingSent = false;
```
::: zone-end

Inside your event handler:

::: zone pivot="programming-language-python"
```python
if event.type == ServerEventType.SESSION_UPDATED:
    if not self.greeting_sent:
        # ... send proactive message ...
        self.greeting_sent = True
```
::: zone-end

::: zone pivot="programming-language-csharp"
```csharp
if (serverEvent is SessionUpdateSessionUpdated)
{
    if (!_greetingSent)
    {
        // ... send proactive message ...
        _greetingSent = true;
    }
}
```
::: zone-end

::: zone pivot="programming-language-java"
```java
if (event.getType() == ServerEventType.SESSION_UPDATED) {
    if (!greetingSent.getAndSet(true)) {
        // ... send proactive message ...
    }
}
```
::: zone-end

::: zone pivot="programming-language-javascript"
```javascript
if (event.type === "session.updated") {
    if (!greetingSent) {
        // ... send proactive message ...
        greetingSent = true;
    }
}
```
::: zone-end

This ensures:

* The greeting triggers exactly once
* The user can begin interacting immediately afterward
* The message enters the conversation context so the LLM understands what was spoken

## Supported proactive message options

Voice Live supports two mechanisms for kicking off the conversation proactively.

You should choose the method that best suits your scenario.

### Option 1: Pregenerated assistant message

*(Best for deterministic or branded greetings)*

Use this option when your application already knows what the agent should say—for example:

* Static welcome messages
* Randomly selected greetings from a predefined list
* Personalized welcome text (for example, 'Welcome back, Lisa!')

The message is,

* inserted directly into the conversation context as an assistant message
* synthesized by TTS
* under full developer control

#### Example: Pregenerated greeting

::: zone pivot="programming-language-python"
```python
from azure.ai.voicelive.models import (
    ResponseCreateParams,
    AssistantMessageItem,
    OutputTextContentPart,
)

# Send a pre-generated assistant greeting
await conn.response.create(
    response=ResponseCreateParams(
        pre_generated_assistant_message=AssistantMessageItem(
            content=[
                OutputTextContentPart(
                    text="Hi Lisa, welcome back! How can I assist you today?"
                )
            ]
        )
    )
)
```
::: zone-end

::: zone pivot="programming-language-csharp"
```csharp
using System.Text.Json;

// Send a pre-generated assistant greeting
var greeting = "Hi Lisa, welcome back! How can I assist you today?";
var responseCreatePayload = new
{
    type = "response.create",
    response = new
    {
        pre_generated_assistant_message = new
        {
            type = "message",
            role = "assistant",
            content = new[]
            {
                new { type = "text", text = greeting }
            }
        }
    }
};
BinaryData eventData = BinaryData.FromObjectAsJson(responseCreatePayload);
await session.SendCommandAsync(eventData, cancellationToken).ConfigureAwait(false);
```
::: zone-end

::: zone pivot="programming-language-java"
```java
import com.azure.ai.voicelive.models.*;

// Send a pre-generated assistant greeting
ResponseCreateOptions responseOptions = new ResponseCreateOptions()
    .setPreGeneratedAssistantMessage(new AssistantMessageItem()
        .setContent(Arrays.asList(
            new OutputTextContentPart()
                .setText("Hi Lisa, welcome back! How can I assist you today?")
        ))
    );

session.sendEvent(new ClientEventResponseCreate().setResponse(responseOptions)).subscribe();
```
::: zone-end

::: zone pivot="programming-language-javascript"
```javascript
// Send a pre-generated assistant greeting
await session.sendEvent({
    type: "response.create",
    response: {
        preGeneratedAssistantMessage: {
            content: [
                {
                    type: "output_text",
                    text: "Hi Lisa, welcome back! How can I assist you today?"
                }
            ]
        }
    }
});
```
::: zone-end

#### When to use this option

| Scenario                                | Use?  |
| --------------------------------------- | ----- |
| Consistent, branded messaging           | ✔ Yes |
| Template- or rule-based personalization | ✔ Yes |
| Want deterministic output               | ✔ Yes |
| Want model creativity                   | ✖ No  |

### Option 2: LLM-generated proactive greeting

*(Best for dynamic and personalized greetings)*

In this pattern, you instruct the LLM to generate the greeting itself.  
You first create a conversation item with a system instruction, then trigger a response.

#### Example: LLM-generated greeting

::: zone pivot="programming-language-python"
```python
from azure.ai.voicelive.models import (
    MessageItem,
    InputTextContentPart,
)

# Add an instruction telling the LLM to greet the user
await conn.conversation.item.create(
    item=MessageItem(
        role="system",
        content=[
            InputTextContentPart(
                text="Say something to welcome the user."
            )
        ]
    )
)

# Trigger LLM-generated greeting
await conn.response.create()
```
::: zone-end

::: zone pivot="programming-language-csharp"
```csharp
using System.Text.Json;

// Add an instruction telling the LLM to greet the user
var conversationItemPayload = new
{
    type = "conversation.item.create",
    item = new
    {
        type = "message",
        role = "system",
        content = new[]
        {
            new { type = "input_text", text = "Say something to welcome the user." }
        }
    }
};
BinaryData itemEventData = BinaryData.FromObjectAsJson(conversationItemPayload);
await session.SendCommandAsync(itemEventData, cancellationToken).ConfigureAwait(false);

// Trigger LLM-generated greeting
await session.StartResponseAsync().ConfigureAwait(false);
```
::: zone-end

::: zone pivot="programming-language-java"
```java
import com.azure.ai.voicelive.models.*;

// Add an instruction telling the LLM to greet the user
MessageItem messageItem = new MessageItem()
    .setRole("system")
    .setContent(Arrays.asList(
        new InputTextContentPart()
            .setText("Say something to welcome the user.")
    ));

session.sendEvent(new ClientEventConversationItemCreate().setItem(messageItem)).subscribe();

// Trigger LLM-generated greeting
session.sendEvent(new ClientEventResponseCreate()).subscribe();
```
::: zone-end

::: zone pivot="programming-language-javascript"
```javascript
// Add an instruction telling the LLM to greet the user
await session.addConversationItem({
    type: "message",
    role: "system",
    content: [
        {
            type: "input_text",
            text: "Say something to welcome the user."
        }
    ]
});

// Trigger LLM-generated greeting
await session.sendEvent({
    type: "response.create"
});
```
::: zone-end

#### When to use this option

| Scenario                          | Use?  |
| --------------------------------- | ----- |
| Adaptive, context-aware greetings | ✔ Yes |
| Personalized tone or content      | ✔ Yes |
| Variation across sessions         | ✔ Yes |
| Predictable output required       | ✖ No  |

## Integrating proactive messaging in your event handler

Below is a combined pattern that connects event-loop handling, conversation start tracking, and both proactive messaging options.

### Session event integration

::: zone pivot="programming-language-python"
```python
async def _handle_event(self, event):
    conn = self.connection
    ap = self.audio_processor

    if event.type == ServerEventType.SESSION_UPDATED:
        print("Session is ready.")
        self.session_ready = True

        # Start microphone capture
        ap.start_capture()

        # Trigger greeting once
        if not self.greeting_sent:
            self.greeting_sent = True

            # ----- Option 1: Pre-generated greeting -----
            # await send_pre_generated_greeting(conn)

            # ----- Option 2: LLM-generated greeting -----
            # await send_llm_generated_greeting(conn)

    elif event.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
        print("🎤 Listening...")
        ap.skip_pending_audio()

    elif event.type == ServerEventType.RESPONSE_AUDIO_DELTA:
        ap.queue_audio(event.delta)

    elif event.type == ServerEventType.RESPONSE_AUDIO_DONE:
        print("🎤 Ready for next input...")
```
::: zone-end

::: zone pivot="programming-language-csharp"
```csharp
private async Task HandleSessionUpdateAsync(SessionUpdate serverEvent, CancellationToken cancellationToken)
{
    if (serverEvent is SessionUpdateSessionUpdated sessionUpdated)
    {
        Console.WriteLine("Session is ready.");
        _sessionReady = true;

        // Start microphone capture
        await _audioProcessor.StartCaptureAsync();

        // Trigger greeting once
        if (!_greetingSent)
        {
            _greetingSent = true;

            // ----- Option 1: Pre-generated greeting -----
            // await SendPreGeneratedGreetingAsync(_session, cancellationToken);

            // ----- Option 2: LLM-generated greeting -----
            // await SendLlmGeneratedGreetingAsync(_session, cancellationToken);
        }
    }
    else if (serverEvent is SessionUpdateInputAudioBufferSpeechStarted)
    {
        Console.WriteLine("🎤 Listening...");
        await _audioProcessor.StopPlaybackAsync();
    }
    else if (serverEvent is SessionUpdateResponseAudioDelta audioDelta)
    {
        await _audioProcessor.QueueAudioAsync(audioDelta.Delta.ToArray());
    }
    else if (serverEvent is SessionUpdateResponseAudioDone)
    {
        Console.WriteLine("🎤 Ready for next input...");
    }
}
```
::: zone-end

::: zone pivot="programming-language-java"
```java
private void handleServerEvent(SessionUpdate event, AudioProcessor audioProcessor) {
    ServerEventType eventType = event.getType();

    if (eventType == ServerEventType.SESSION_UPDATED) {
        System.out.println("Session is ready.");
        sessionReady = true;

        // Start microphone capture
        audioProcessor.startCapture();

        // Trigger greeting once
        if (!greetingSent.getAndSet(true)) {

            // ----- Option 1: Pre-generated greeting -----
            // sendPreGeneratedGreeting(session);

            // ----- Option 2: LLM-generated greeting -----
            // sendLlmGeneratedGreeting(session);
        }
    } else if (eventType == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED) {
        System.out.println("🎤 Listening...");
        audioProcessor.skipPendingAudio();
    } else if (eventType == ServerEventType.RESPONSE_AUDIO_DELTA) {
        SessionUpdateResponseAudioDelta audioEvent = (SessionUpdateResponseAudioDelta) event;
        audioProcessor.queueAudio(audioEvent.getDelta());
    } else if (eventType == ServerEventType.RESPONSE_AUDIO_DONE) {
        System.out.println("🎤 Ready for next input...");
    }
}
```
::: zone-end

::: zone pivot="programming-language-javascript"
```javascript
const subscription = session.subscribe({
    onSessionUpdated: async (event, context) => {
        console.log("Session is ready.");
        sessionReady = true;

        // Start microphone capture
        startMicrophoneCapture();

        // Trigger greeting once
        if (!greetingSent) {
            greetingSent = true;

            // ----- Option 1: Pre-generated greeting -----
            // await sendPreGeneratedGreeting(session);

            // ----- Option 2: LLM-generated greeting -----
            // await sendLlmGeneratedGreeting(session);
        }
    },

    onInputAudioBufferSpeechStarted: async (event, context) => {
        console.log("🎤 Listening...");
        skipPendingAudio();
    },

    onResponseAudioDelta: async (event, context) => {
        queueAudio(event.delta);
    },

    onResponseAudioDone: async (event, context) => {
        console.log("🎤 Ready for next input...");
    }
});
```
::: zone-end

### Greeting helper functions

::: zone pivot="programming-language-python"
```python
async def send_pre_generated_greeting(conn):
    await conn.response.create(
        response=ResponseCreateParams(
            pre_generated_assistant_message=AssistantMessageItem(
                content=[
                    OutputTextContentPart(
                        text="Welcome! I'm here to help you get started."
                    )
                ]
            )
        )
    )

async def send_llm_generated_greeting(conn):
    await conn.conversation.item.create(
        item=MessageItem(
            role="system",
            content=[
                InputTextContentPart(
                    text="Greet the user warmly and briefly explain how you can help."
                )
            ]
        )
    )
    await conn.response.create()
```
::: zone-end

::: zone pivot="programming-language-csharp"
```csharp
private async Task SendPreGeneratedGreetingAsync(
    VoiceLiveSession session, 
    CancellationToken cancellationToken)
{
    var greeting = "Welcome! I'm here to help you get started.";
    var responseCreatePayload = new
    {
        type = "response.create",
        response = new
        {
            pre_generated_assistant_message = new
            {
                type = "message",
                role = "assistant",
                content = new[]
                {
                    new { type = "text", text = greeting }
                }
            }
        }
    };
    BinaryData eventData = BinaryData.FromObjectAsJson(responseCreatePayload);
    await session.SendCommandAsync(eventData, cancellationToken).ConfigureAwait(false);
}

private async Task SendLlmGeneratedGreetingAsync(
    VoiceLiveSession session, 
    CancellationToken cancellationToken)
{
    var conversationItemPayload = new
    {
        type = "conversation.item.create",
        item = new
        {
            type = "message",
            role = "system",
            content = new[]
            {
                new { type = "input_text", text = "Greet the user warmly and briefly explain how you can help." }
            }
        }
    };
    BinaryData itemEventData = BinaryData.FromObjectAsJson(conversationItemPayload);
    await session.SendCommandAsync(itemEventData, cancellationToken).ConfigureAwait(false);
    await session.StartResponseAsync().ConfigureAwait(false);
}
```
::: zone-end

::: zone pivot="programming-language-java"
```java
private void sendPreGeneratedGreeting(VoiceLiveSessionAsyncClient session) {
    ResponseCreateOptions responseOptions = new ResponseCreateOptions()
        .setPreGeneratedAssistantMessage(new AssistantMessageItem()
            .setContent(Arrays.asList(
                new OutputTextContentPart()
                    .setText("Welcome! I'm here to help you get started.")
            ))
        );

    session.sendEvent(new ClientEventResponseCreate().setResponse(responseOptions)).subscribe();
}

private void sendLlmGeneratedGreeting(VoiceLiveSessionAsyncClient session) {
    MessageItem messageItem = new MessageItem()
        .setRole("system")
        .setContent(Arrays.asList(
            new InputTextContentPart()
                .setText("Greet the user warmly and briefly explain how you can help.")
        ));

    session.sendEvent(new ClientEventConversationItemCreate().setItem(messageItem)).subscribe();
    session.sendEvent(new ClientEventResponseCreate()).subscribe();
}
```
::: zone-end

::: zone pivot="programming-language-javascript"
```javascript
async function sendPreGeneratedGreeting(session) {
    await session.sendEvent({
        type: "response.create",
        response: {
            preGeneratedAssistantMessage: {
                content: [
                    {
                        type: "output_text",
                        text: "Welcome! I'm here to help you get started."
                    }
                ]
            }
        }
    });
}

async function sendLlmGeneratedGreeting(session) {
    await session.addConversationItem({
        type: "message",
        role: "system",
        content: [
            {
                type: "input_text",
                text: "Greet the user warmly and briefly explain how you can help."
            }
        ]
    });
    await session.sendEvent({
        type: "response.create"
    });
}
```
::: zone-end

## Choosing the right approach

| Requirement                               | Pregenerated | LLM-generated |
| ----------------------------------------- | ------------- | ------------- |
| Predictable, scripted greetings           | ✔             | ✖             |
| Brand consistency and controlled language | ✔             | Depending on Instructions |
| Adaptive and personalized content         | Unless you implement it | ✔             |
| Conversational variety                    | ✖             | ✔             |
| Minimal model prompting                   | ✔             | ✖             |

## Next steps

- Try the Voice Live **Playground [Foundry portal](./voice-live-quickstart.md?pivots=ai-foundry-portal) to experiment with proactive engagement
- Learn more about [How to use the Voice live API](./voice-live-how-to.md)
- See the [Voice live API reference](./voice-live-api-reference.md)
