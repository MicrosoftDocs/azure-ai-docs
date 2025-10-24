---
title: Publish Agents in Azure AI Foundry
description: Learn how to publish agents in Azure AI Foundry, configure authentication, manage permissions, and provide stable endpoints for seamless integration.
#customer intent: As a developer, I want to publish an agent in Azure AI Foundry so that I can provide a stable endpoint for external consumption.
author: sdgilley
ms.author: sgilley
ms.reviewer: amandafoster
ms.date: 10/23/2025
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
---

# Publish agents in Azure AI Foundry

Publishing transforms an agent from a development asset into a managed Azure resource with a dedicated endpoint, independent identity, and governance capabilities. This article shows you how to publish an agent, configure its authentication and permissions, update published versions, and consume the agent through its stable endpoint.

When you publish an agent, Azure AI Foundry creates an Agent Application resource with a dedicated invocation URL and its own Agent Identity Blueprint and Agent Identity. A deployment is created under the application that references your agent version and registers it in the Entra Agent Registry for discovery and governance.

Publishing enables you to share agents with teammates, your organization, or customers without granting access to your Foundry project or source code. The stable endpoint remains consistent as you iterate and deploy new agent versions.

## Prerequisites

- An Azure AI Foundry project with at least one agent version created
- Azure AI Project Manager role on the Foundry project scope to publish agents
- Understanding of Azure RBAC for permission configuration
- For tool authentication: Knowledge of which Azure resources your agent accesses

## Understand Agent Applications and deployments

Before publishing, it's important to understand the relationship between projects, agent versions, applications, and deployments.

:::image type="content" source="../../media/publish-agent/azure-agent-identity-overview.png" alt-text="Diagram illustrating how Azure AI Foundry projects organize agent versions, applications, and deployments, highlighting governance and RBAC roles.":::

An Azure AI Foundry **project** is an organizational container that groups related resources. An **agent version** is a single definition of an agent—including prompts, containers, or workflows—stored as an at-rest object. When you create an agent, it's exposed under the project where developers with project access can create, run, and test it.

An **Agent Application** is the durable interface you use to expose agents. It acts as a SaaS application with authentication, identity, and a stable entry point. A **deployment** is a running instance of an agent version inside an application that can be started, stopped, and updated to reference new agent versions.

During development, all unpublished agents in a project share a default Agent Identity. Once published, an agent receives its own Agent Identity and becomes a nested Azure resource visible in the Azure Portal, enabling independent governance and RBAC configuration.

### Routing and version management

Each Agent Application acts as a routing table to specific agent deployments. Currently, an Agent Application supports one active deployment, directing 100% of traffic to that deployment. When you publish a new agent version to an existing application, the deployment updates to reference the new version. Future updates will introduce traffic splitting across multiple deployments for gradual rollouts.

:::image type="content" source="../../media/publish-agent/agent-application-routing-diagram.png" alt-text="Diagram of an Agent Application routing traffic to a deployment running a specific agent version, showing a stable entry point and traffic flow.":::

## Determine when to publish an agent

Publish an agent when it's ready to be shared and consumed outside your project. Consider publishing in these scenarios:

- **Production environments**: The agent has been tested in development and is stable enough to interact with external users or systems
- **External sharing**: You want to provide access to teammates or customers who shouldn't have access to your Foundry project
- **Distinct identity requirements**: The agent needs its own identity, RBAC rules, and audit trail separate from the project-level default identity
- **Version management**: You need to update or roll out new agent versions without disrupting downstream consumers
- **Code integration**: You want to integrate the agent into your existing codebase (such as a web application) using a stable endpoint
- **Multi-instance deployments**: Different groups require access to the same agent logic with different privileges

Publishing provides a stable endpoint, unique Agent Identity with audit trails, cross-team sharing capabilities, integration with Entra Agent Registry, and the ability to publish your application to Teams and Microsoft 365 Copilot or preview it as a web application.

## Publish an agent from Foundry UI

This section shows you how to publish an agent using the Azure AI Foundry portal interface.

1. In the Agent Playground, create or select an agent version you want to publish.

2. Select **Publish Agent** to create an Agent Application and deployment.

3. Configure authentication for your Agent Application:

   - By default, the authentication type is set to RBAC (Role-Based Access Control)
   - End users calling the agent must have Azure RBAC permissions on the application resource
   - For Azure Bot Service integration (to support Microsoft 365/Microsoft 365 Copilot), requests from a linked Azure Bot Service instance are automatically permitted

4. Assign permissions for tool authentication:

   - If your agent includes tools that use Agent Identity for authentication, the newly created Agent Identity must have appropriate permissions
   - Navigate to each Azure resource your agent accesses and assign the required RBAC role to the new Agent Identity
   - The shared development identity permissions don't carry over—you must reconfigure permissions for the published agent's identity

5. After publishing, you can:

   - Open the agent as a web app
   - Publish it to Teams and Microsoft 365 Copilot
   - Share the published endpoint with external consumers

## Update a published Agent Application

When you need to deploy a new version of your agent, update the existing Agent Application to reference the new agent version.

1. In the Agent Playground, navigate to the specific agent version you want to publish.

2. Select **Publish Updates**.

3. Choose the existing Agent Application you want to update.

4. Confirm the update. The Agent Application automatically directs 100% of traffic to the new agent version.

The stable endpoint URL remains unchanged, ensuring downstream consumers aren't disrupted by the update.

## Consume your published Agent Application

After publishing, you invoke your agent through its endpoint using the responses protocol. The following examples show how to call your published agent using different client libraries.

### Use OpenAI client with Agent Applications endpoint

```python
# filepath: Direct OpenAI compatible approach
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

openai = OpenAI(
    base_url="https://aifoundry.services.ai.azure.com/api/projects/my-project/applications/app-id/openai/",
    api_key=token_provider
)

openai.responses.create(
    input="Write a haiku"
)
```

### Use Project Client with Agent Applications endpoint

```python
# filepath: Using Azure AI Projects client
from azure.ai.projects import ProjectClient
from azure.identity import DefaultAzureCredential

project_client = ProjectClient(
    endpoint="https://aifoundry.services.ai.azure.com/api/projects/my-project",
    credential=DefaultAzureCredential()
)

openai = project_client.get_openai_client_for_application(appid)

openai.responses.create(
    input="Write a haiku"
)
```

Both approaches authenticate using Azure credentials and require the caller to have the Azure AI User role on the Agent Application resource.

## Configure end-user isolation

Agent Applications currently don't provide built-in end-user isolation for conversations, files, memory, and vector stores. A user with access to another user's conversation ID can list all items in that conversation. To achieve end-user isolation, expose your published Agent Application endpoint behind a middle tier that implements authorization logic.

Your middle tier should:

- Authenticate end users using your chosen authentication method
- Validate user authorization before forwarding requests to the Agent Application
- Associate conversations and resources with specific user identities
- Enforce access control policies to prevent cross-user data access

## Related content

- Learn about [Agent identity concepts in Azure AI Foundry](../concepts/agent-identity.md)
- Explore [authentication options for Agent Applications](#)
- Review [best practices for middle tier implementation](#)
