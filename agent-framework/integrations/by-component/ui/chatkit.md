---
title: ChatKit
description: Connect an Agent Framework Python backend to an OpenAI ChatKit user interface.
author: eavanvalkenburg
ms.topic: article
ms.author: edvan
ms.date: 10/01/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

# ChatKit

`agent-framework-chatkit` converts OpenAI ChatKit thread items into Agent Framework messages and converts streamed agent updates back into ChatKit events. Use it when you want a ChatKit frontend with an Agent Framework Python backend.

The integration provides:

- `ThreadItemConverter` for converting ChatKit thread items and attachments.
- `stream_agent_response()` for converting streamed agent updates to ChatKit events.
- `simple_to_agent_input()` for the default message-conversion path.

## Prerequisites

- Python 3.10 or later.
- A backend web framework such as FastAPI.
- Node.js for the ChatKit frontend.
- A ChatKit domain key for a production frontend domain.

## Install the package

```bash
pip install agent-framework-chatkit --pre
```

## Create a ChatKit server

Subclass `ChatKitServer`, create the Agent Framework agent, and configure a converter for thread items and attachments.

:::code language="python" source="~/../agent-framework-code/python/samples/05-end-to-end/chatkit-integration/app.py" range="211-248":::

## Convert and stream responses

Load the thread history, convert it to Agent Framework messages, run the agent in streaming mode, and yield ChatKit events.

:::code language="python" source="~/../agent-framework-code/python/samples/05-end-to-end/chatkit-integration/app.py" range="341-416":::

`ThreadItemConverter` preserves `StructuredInputItem` status and represents each question as answered, skipped, or unanswered in a user message. Override the asynchronous `structured_input_to_input()` method to customize formatting or redact answers. Return one `Message`, a list of messages, or `None` to omit the item.

The converter also preserves completed `GeneratedImageItem` values as model
context on later turns. The default conversion creates a user `Message` with a
short text preface and the generated image URI. Data URIs retain their embedded
media type, external URLs use `image/*`, and unfinished items without an image
are skipped.

Override the asynchronous `generated_image_to_input()` method to customize
generated image context, such as resolving a private image URL. Return one
`Message`, a list of messages, or `None` to omit the item.

The complete sample also demonstrates SQLite-backed threads, file uploads, attachment storage, actions, and interactive widgets.

> [!WARNING]
> The ChatKit frontend is loaded from OpenAI's CDN and makes outbound requests to OpenAI domains. It can't currently be self-hosted and isn't suitable for air-gapped environments.

## Next steps

> [!div class="nextstepaction"]
> [DevUI](devui/index.md)
