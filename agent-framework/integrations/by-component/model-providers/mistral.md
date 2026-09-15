---
title: Mistral
description: Use Mistral AI chat and embedding models with Agent Framework Python.
author: eavanvalkenburg
ms.topic: article
ms.author: edvan
ms.date: 08/31/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

# Mistral

The Mistral integration provides `MistralChatClient` for chat agents and
`MistralEmbeddingClient` for text embeddings in Agent Framework Python.

## Install the package

```bash
pip install agent-framework-mistral --pre
```

## Configuration

```bash
MISTRAL_API_KEY="<api-key>"
MISTRAL_CHAT_MODEL="mistral-small-latest"
MISTRAL_EMBEDDING_MODEL="mistral-embed"
# Optional compatible endpoint:
MISTRAL_SERVER_URL="<server-url>"
```

You can also pass `api_key`, `model`, and `server_url` directly to either
client.

## Create a chat agent

Create an `Agent` with `MistralChatClient`. The client reads the API key and
chat model from the environment variables shown in the previous section.

```python
import asyncio

from agent_framework import Agent
from agent_framework.mistral import MistralChatClient


async def main() -> None:
    client = MistralChatClient()
    try:
        agent = Agent(
            client=client,
            instructions="You are a helpful assistant.",
        )
        response = await agent.run("How many days are in a week?")
        print(response.text)
    finally:
        await client.close()


asyncio.run(main())
```

The selected Mistral model determines which model-level capabilities are
available.

## Chat capabilities

`MistralChatClient` supports the following Agent Framework features:

| Capability | Usage |
|---|---|
| Streaming | Call `agent.run(..., stream=True)` to iterate over response updates. |
| Function tools | Add Agent Framework function tools to `Agent(tools=...)`. |
| Structured output | Pass a Pydantic model, JSON schema mapping, or JSON object mode through `response_format`. |
| Multimodal input | Send image data or URLs and PDF document URLs in user messages. |
| Reasoning | Set `reasoning_effort` for supported models and read returned thinking as `text_reasoning` content. |

For a runnable function-tool and streaming example, see the
[Mistral agent sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/02-agents/providers/mistral/mistral_agent_basic.py).

## Generate embeddings

Create the client and call `get_embeddings()`.

:::code language="python" source="~/../agent-framework-code/python/samples/02-agents/providers/mistral/mistral_embeddings.py" range="20-55":::

Use `MistralEmbeddingOptions` to request a supported output dimension. You can also set `MISTRAL_SERVER_URL` when the application uses a custom compatible endpoint.

> [!IMPORTANT]
> Mistral AI is a third-party system. Review its service terms, data handling, regional boundaries, model licensing, and usage costs before sending application data.

## Tools

`MistralChatClient` supports locally invoked function tools and the Agent
Framework function-invocation loop. The selected model must support function
calling.

## Next steps

> [!div class="nextstepaction"]
> [RAG](../../../agents/rag.md)
