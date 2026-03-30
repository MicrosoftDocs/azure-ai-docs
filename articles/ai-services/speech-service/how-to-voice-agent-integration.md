---
title: How to build a voice agent
titleSuffix: Foundry Tools
description: Learn how to use Voice Live with Foundry Agent Service to build real-time voice agents.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 02/20/2026
author: PatrickFarley
reviewer: PatrickFarley
ms.author: pafarley
ms.reviewer: pafarley
zone_pivot_groups: voice-live-howto-agents
recommendations: false
ai-usage: ai-assisted
---

# How to build a voice agent (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

> [!NOTE]
> Foundry agent integration currently only supports agents available on public endpoints. Foundry agents deployed in private VNet aren't supported.

::: zone pivot="programming-language-python"
[!INCLUDE [Python quickstart](./includes/how-to/voice-live-agents/python.md)]
::: zone-end

::: zone pivot="programming-language-csharp"
[!INCLUDE [Csharp how-to](./includes/how-to/voice-live-agents/csharp.md)]
::: zone-end

::: zone pivot="programming-language-java"
[!INCLUDE [Java how-to](./includes/how-to/voice-live-agents/java.md)]
::: zone-end

::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript how-to](./includes/how-to/voice-live-agents/javascript.md)]
::: zone-end

## Migrate from Agent Service (classic)

If you're using Voice Live with Agent Service (classic), we recommend you migrate to the new Foundry Agent Service. For general Agent Service migration steps, see [Migrate from Agent Service (classic) to Foundry Agent Service](/azure/foundry/agents/how-to/migrate).

### Voice Live SDK changes

The Voice Live SDK introduces typed configuration classes that replace the raw query parameters used in the classic integration:

| Classic (v1) | New (v2) |
|---|---|
| `agent-id` query parameter | `agent_name` in `AgentConfig` / `AgentSessionConfig` |
| `agent-project-name` query parameter | Project endpoint in client constructor |
| `agent-access-token` query parameter | Handled automatically by SDK |
| Manual `connect()` with query dict | Strongly-typed `AgentSessionConfig` passed to session options |

### Minimum SDK versions

| Language | Package | Minimum version |
|---|---|---|
| Python | `azure-ai-voicelive` | 1.0.0b5 |
| C# | `Azure.AI.VoiceLive` | 1.1.0-beta.2 |
| Java | `azure-ai-voicelive` | 1.0.0-beta.5 |
| JavaScript | `@azure/ai-voicelive` | 1.0.0-beta.3 |

### Before and after: Python connection setup

**Classic (v1)** — raw query parameters in `connect()`:

```python
async with connect(
    endpoint=self.endpoint,
    credential=self.credential,
    query={
        "agent-id": self.agent_id,
        "agent-project-name": self.foundry_project_name,
        "agent-access-token": agent_access_token
    },
) as connection:
```

**New (v2)** — strongly-typed `AgentSessionConfig`:

```python
from azure.ai.voicelive import AgentConfig, AgentSessionConfig

agent_config = AgentConfig(agent_name=agent_name)
agent_session_config = AgentSessionConfig(agent_config=agent_config)

session_options = VoiceLiveSessionOptions(
    agent_session_config=agent_session_config,
    # ... other options
)
```

For complete code examples, see the [new agent quickstart](voice-live-agents-quickstart.md). The [classic quickstart](voice-live-agents-quickstart-classic.md) remains available.

## Related content

- Explore [How to add proactive messages](./how-to-voice-live-proactive-messages.md)
- Explore [How to improve tool calling and latency wait times](./how-to-voice-live-interim-response.md)
- Learn more about [How to use the Voice Live API](./voice-live-how-to.md)
- See the [Voice Live API reference](./voice-live-api-reference-2025-10-01.md)
