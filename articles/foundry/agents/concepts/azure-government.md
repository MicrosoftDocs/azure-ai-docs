---
title: "Foundry Agent Service feature availability in Azure Government"
titleSuffix: Microsoft Foundry
description: "Agent types, tools, and publishing options supported by Microsoft Foundry Agent Service in Azure Government (USGov Virginia and USGov Arizona)."
author: jvenezia
ms.author: jvenezia
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: concept-article
ms.date: 06/12/2026
ai-usage: ai-assisted
ms.custom:
  - references_regions
  - azure-ai-agents
keywords:
  - Foundry Agent Service
  - Azure Government
  - USGov Virginia
  - USGov Arizona
  - feature parity
---

# Foundry Agent Service feature availability in Azure Government

This article shows which Microsoft Foundry Agent Service agent types, tools, and publishing options are available in Azure Government — and which aren't. For platform-level features, endpoints, and portal URLs, see [Microsoft Foundry in Azure Government](../../concepts/foundry-azure-government.md). For an introduction to Agent Service, see the [Foundry Agent Service overview](../overview.md).

## Supported regions

Foundry Agent Service is available in the following Azure Government regions:

| Region | Region identifier |
| --- | --- |
| US Gov Virginia | `usgovvirginia` |
| US Gov Arizona | `usgovarizona` |

Agent Service features and tools are available in both regions unless noted otherwise in the tables below.

## Agent types

| Agent type | Available |
| --- | --- |
| Prompt agents | Yes |
| Workflows | Preview |
| Hosted agents | No |

### Preview features in Azure Government

Features marked **Preview** are available for early adoption but might not carry the same compliance commitments (such as FedRAMP, DoD IL5, or CJIS) as generally available features. Confirm the compliance posture of any preview feature with your security and compliance team before using it for production or regulated workloads.

## Tools

The following table lists tool availability for Foundry Agent Service in Azure Government. For details on each tool, see the [Foundry tool catalog](../concepts/tool-catalog.md).

| Tool | Available |
| --- | --- |
| Code Interpreter | Yes |
| Custom Code Interpreter | Preview |
| File Search | Yes |
| Azure AI Search | Yes |
| Azure Functions | Yes |
| Function calling | Yes |
| Web search | No |
| Grounding with Bing | No |
| Image Generation | No |
| Browser Automation | No |
| Computer Use | No |
| Microsoft Fabric | No |
| SharePoint | No |
| MCP servers | No |
| Agent-to-Agent (A2A) | No |
| OpenAPI tool | No |

## Publishing

Azure Government supports publishing agents. Each published agent gets a stable managed endpoint and a Microsoft Entra identity. You can register the agent with the Entra Agent Registry for discovery within your tenant. Publishing to Microsoft Teams and Microsoft 365 Copilot isn't supported. For more information, see [Publish an agent](../how-to/publish-copilot.md).

## SDK configuration for Azure Government

Agent Service in Azure Government requires `azure-ai-projects` version **2.0.0 or later**. Install the package with:

```bash
pip install "azure-ai-projects>=2.0.0" azure-identity
```

The token audience and project endpoint differ from public cloud. Set `credential_scopes` to `https://ai.azure.us/.default` and use your Azure Government project endpoint, which has the format `https://{resource-name}.services.ai.azure.us/api/projects/{project-name}`.

The following example creates a simple prompt agent, sends a message, and prints the response:

```python
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.projects import AIProjectClient

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
scope = "https://ai.azure.us/.default"

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint,
        credential=credential,
        credential_scopes=[scope],
    ) as project_client,
):
    api_key = get_bearer_token_provider(credential, scope)

    with project_client.get_openai_client(api_key=api_key) as openai_client:
        from azure.ai.projects.models import PromptAgentDefinition

        agent = project_client.agents.create_version(
            agent_name="MyAgent",
            definition=PromptAgentDefinition(
                model=os.environ["FOUNDRY_MODEL_NAME"],
                instructions="You are a helpful assistant",
            ),
        )
        print(f"Agent created (name: {agent.name}, version: {agent.version})")

        conversation = openai_client.conversations.create(
            items=[{"type": "message", "role": "user", "content": "Hello!"}],
        )

        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )
        print(f"Response: {response.output_text}")

        openai_client.conversations.delete(conversation_id=conversation.id)
        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
```

For samples that use tools like file search, code interpreter, and function calling, see the [agent SDK samples on GitHub](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/agents).

## Quotas, limits, and models

- For Agent Service quotas, limits, and regional support, see [Quotas and limits for Microsoft Foundry Agent Service](./limits-quotas-regions.md).
- For the list of Foundry Models available in Azure Government, see [Foundry Models sold by Azure in Azure Government](../../foundry-models/concepts/models-sold-directly-by-azure-gov.md).

## Related content

- [Microsoft Foundry in Azure Government](../../concepts/foundry-azure-government.md) — Platform features, endpoints, and portal URLs
- [Quotas and limits for Microsoft Foundry Agent Service](./limits-quotas-regions.md) — Service quotas and regional support
- [Foundry Agent Service overview](../overview.md) — Introduction to Agent Service
- [Foundry tool catalog](../concepts/tool-catalog.md) — Detailed information on all tools
- [Foundry Models sold by Azure in Azure Government](../../foundry-models/concepts/models-sold-directly-by-azure-gov.md) — Available models in Azure Government
