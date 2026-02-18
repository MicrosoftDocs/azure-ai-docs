---
title: Chat with your Agent Application using the Responses API protocol
description: Chat with an existing Agent Application using the Responses API protocol
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.date: 02/13/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Invoke your agent application using the responses API protocol

After publishing, you can invoke your agent application using the Responses API protocol or the Activity Protocol. The Activity Protocol is used when your agent is published to Microsoft 365 and Teams.

This article focuses on how you invoke your Agent Application using the Responses API protocol. 

## Prerequisites

- **Test your agent thoroughly** in the Foundry portal before publishing. Confirm it responds correctly and any tools work as expected.
- **Publish your agent as an Agent Application**: An Agent Application is a managed Azure resource that wraps your agent with a stable endpoint for external consumption. To publish your agent, see [Publish and share agents in Microsoft Foundry](publish-agent.md).
- [Azure AI User role](../../../concepts/rbac-foundry.md) on the Agent Application scope to chat with a published agent using the Responses API protocol
- **Before running the code sample, ensure you have**:
    - Python 3.8 or later installed
    - [Azure CLI](/cli/azure/install-azure-cli) installed and configured
    - Required Python packages installed:
      ```bash
      pip install openai azure-identity
      ```
    - Authenticated to Azure CLI:
      ```bash
      az login
      ```
    For more information on setting up your development environment, see [Prepare your development environment](../../../how-to/develop/install-cli-sdk.md).

## Use OpenAI client with Agent Applications endpoint

```python
# filepath: Direct OpenAI compatible approach
from openai import OpenAI 
from azure.identity import DefaultAzureCredential, get_bearer_token_provider 

# Replace placeholders in base_url with your <foundry-resource-name>, <project-name>, and <app-name>
openai_client = OpenAI(
    api_key=get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default"),
    base_url="https://<foundry-resource-name>.services.ai.azure.com/api/projects/<project-name>/applications/<app-name>/protocols/openai",
    default_query = {"api-version": "2025-11-15-preview"}
)

response = openai_client.responses.create( 
  input="Write a haiku", 
) 
print(f"Response output: {response.output_text}")
```
This approach authenticates using Azure credentials and requires the caller to have the Azure AI User role on the Agent Application resource.

## Limitations



| Limitation | Description |
| --- | --- |
| Stateless Responses API only | Only the stateless Responses API is supported. Other APIs including `/conversations`, `/files`, `/vector_stores`, and `/containers` are inaccessible. |


## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| `403 Forbidden` when invoking the endpoint | Caller lacks invoke permissions on the Agent Application resource | Assign the Azure AI User role on the Agent Application resource to the caller. |
| `401 Unauthorized` when invoking the endpoint | The access token is missing, expired, or for the wrong resource | Reauthenticate and request a token for `https://ai.azure.com`. |
| Tool calls fail after publishing | The Agent Application identity doesn’t have the same access as the project identity | Reassign the required RBAC roles to the published agent identity for any downstream Azure resources it must access. |
| Multi-turn conversations don’t work as expected | Agent Applications don’t store conversation state for you | Store conversation history in your client and send the context as part of your request. |


## FAQs

**1. Why are conversations not persisted for published agents (aka why is only stateless responses supported)?**

Today there’s a temporary limitation where published agents only support stateless Responses API interactions (that is, no persistent conversations). Work to fix this is already underway.

The reason for this limitation is that while Foundry Agent Service supports managed conversation history, it doesn't yet enforce end-user isolation between conversations within the same project. In other words, if someone knows another user’s conversation ID, they could access that conversation history even though it isn’t theirs. That’s acceptable in a development context within a single project, but it’s not acceptable for production, where customers need strict per-user conversation isolation. 

Agent Applications are intended to expose functionality to a different audience (for example, others in your org or your customers), separate from project developers, with stable versions, configuration, and controlled access. Given that goal, users of agent applications naturally expect their interactions with the application to be private and not visible to others. This isn’t currently possible because the single-user OpenAI APIs we’ve built on top of don't provide native data isolation, and we need to build that isolation layer ourselves. Until we support full end-user data isolation for applications, only stateless responses are available. This limitation is temporary.

**2. What is the pricing model for a published agent? Is the cost based on a consumption model, or does the client incur charges simply because the application resource (endpoint) has underlying infrastructure deployed once the agent is published?**

Published agents use a publisher-pays model: the publisher (the Foundry project owner) incurs costs based on the underlying infrastructure that is deployed when the agent is published as an application, not based on per-call consumption. End users of the published application do not incur any costs by default, though customers may choose to place their own metering or billing layer in front of the application if they want to implement a consumption-based model for their organization or external users.
