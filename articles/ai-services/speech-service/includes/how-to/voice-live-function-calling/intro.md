---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 04/06/2026
ms.author: pafarley
ai-usage: ai-assisted
---

## Implementation steps

The code sample in this article does these basic steps to set up function calling.

1. **Write backend functions**: Define callables that fulfill business tasks (time lookup, weather, database queries) and serialize outputs to JSON-friendly dictionaries.
1. **Describe tools for Voice Live**: Create function tool definitions with names, parameter schemas, and text descriptions, and bundle them into the session configuration so the model understands available actions.
1. **Initialize the session**: Connect to the Voice Live endpoint, provide credentials, pass in the defined function tools, choose your target model and voice, and enable audio modalities, transcription, and turn detection.
1. **Start audio processing**: Capture microphone input, encode it (PCM16, 24 kHz), and stream it to the Voice Live connection. Simultaneously prepare playback for assistant audio responses.
1. **Run the event loop**: Handle Voice Live events, react to user speech boundaries, and stream the assistant's audio back to the user. When a function call event arrives, locate the callable, execute it with parsed arguments, send the result back to the session, and trigger a new response so the assistant can incorporate the result in its reply.
