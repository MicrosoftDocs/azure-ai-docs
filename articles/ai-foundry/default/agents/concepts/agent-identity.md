---
title: Manage Agent Identities with Microsoft Entra ID
description: Explore how Azure AI Foundry automates Agent Identity management, streamlining permissions and enhancing security throughout the AI agent lifecycle.
#customer intent: As a security administrator, I want to know how Agent Identity eliminates the need for passwords and certificates so that I can reduce security risks in my environment.
author: sdgilley
ms.author: sgilley
ms.reviewer: fosteramanda
ms.date: 10/23/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
---

# Agent identity concepts in Azure AI Foundry

**Agent Identity** is a specialized identity type in Microsoft Entra ID designed specifically for AI agents. It provides a standardized framework for governing, authenticating, and authorizing AI agents across Microsoft services, enabling agents to securely access resources, interact with users, and communicate with other systems.

Agent identities integrate seamlessly with Azure AI Foundry, automatically provisioning and managing identities for agents throughout their lifecycle. This integration simplifies permission management while maintaining security and auditability as agents move from development to production.

## Prerequisites

* Understanding of Microsoft Entra ID and OAuth authentication
* Familiarity with [Azure role-based access control (RBAC)](/azure/role-based-access-control/overview)
* Basic knowledge of AI agents and their runtime requirements

## Agent identity

An Agent Identity (AID) is the primary account an AI agent uses to authenticate to systems. Each agent identity has unique identifiers—the object ID and app ID, which always share the same value—that enable reliable authentication and authorization decisions.

Agent identities support three key authentication scenarios:

* **Request agent tokens**: Agents can request access tokens from Entra ID with the agent identity as the subject
* **Receive incoming tokens**: Agents can receive access tokens issued by Entra ID with the agent identity as the audience
* **Request user tokens**: Agents can request tokens for authenticated users, where the subject is the user and the actor (azp or appId claim) is the agent identity

Unlike traditional service principals, agent identities don't use passwords, certificates, or client secrets. Instead, they authenticate by presenting access tokens issued to the service or platform hosting the agent. Agent identities operate within a single Entra tenant and cannot access resources in other tenants.

## Agent identity blueprint

An Agent Identity Blueprint serves as the "parent" of agent identities and fulfills three essential purposes:

**Type classification**: The blueprint establishes the category of agent identity, such as "Contoso Sales Agent" or "DataDog Cloud Monitoring Agent." This classification enables administrators to manage multiple individual agents of the same type as a collection and apply security policies like "block all requests from all Contoso Sales Agent IDs." The blueprint also stores common attributes, metadata, and settings across all its agent identities, including role definitions.

**Identity creation authority**: Services creating agent identities use the blueprint to authenticate. Blueprints have an OAuth client ID and credentials including client secrets, certificates, and federated identity credentials like managed identities. Services use these credentials to request access tokens from Entra ID, then present those tokens to create, update, or delete agent identities.

**Runtime authentication platform**: The hosting service or platform uses the blueprint during runtime authentication. The service requests an access token using the blueprint's OAuth credentials, then presents that token to Entra ID to obtain a token for one of its agent identities.

## Azure AI Foundry identity management

Azure AI Foundry automatically integrates with Entra Agent ID by creating and managing identities throughout the agent development lifecycle. When you create your first agent in a Foundry project, the system provisions a default Agent Identity Blueprint and a default Agent Identity for your project.

### Shared project identity

All unpublished or in-development agents within the same project share a common identity. This design simplifies permission management because unpublished agents typically require the same access patterns and permission configurations. The shared identity approach:

* Reduces administrative overhead by controlling all development agents through a single identity
* Minimizes agent sprawl in the tenant
* Enables developers to build agents independently once project permissions are established
* Eliminates the need for new permission requests for each development agent

To find your shared Agent Identity Blueprint and Agent Identity, navigate to your Foundry project in the Azure Portal. On the Overview page, select "Json View" and choose the latest API version to view and copy the identities.

:::image type="content" source="../../media/agent-identity/azure-agent-identity-json-view.png" alt-text="Screenshot of the JSON view in Azure Portal displaying Agent Identity Blueprint and Agent Identity details for a Foundry project." lightbox="../../media/agent-identity/azure-agent-identity-json-view.png":::

### Distinct agent identity

When an agent's permissions, auditability, or lifecycle requirements diverge from the project defaults, you should upgrade to a distinct identity. Publishing an agent automatically creates a dedicated Agent Identity Blueprint and Agent Identity, both bound to the Agent Application resource. This distinct identity represents the agent's system authority for accessing its own resources.

Common scenarios requiring distinct identities include:

* Agents ready for integration testing
* Agents prepared for production consumption
* Agents requiring unique permission sets
* Agents needing independent audit trails

To find the distinct Agent Identity Blueprint and Agent Identity, navigate to your Agent Application resource in the Azure Portal. On the Overview page, select "Json View" and choose the latest API version to view and copy the identities.

## Tool authentication

Agents access remote resources and tools using Agent Identity for authentication. The authentication mechanism differs based on the agent's publication status:

* **Unpublished agents**: Authenticate using the shared project's Agent Identity
* **Published agents**: Authenticate using their unique Agent Identity associated with the Agent Application

When you [publish an agent](../how-to/publish-agent.md), you must reassign RBAC permissions to the new Agent Identity for any resources the agent needs to access. This ensures the published agent maintains appropriate access while operating under its distinct identity.

### MCP server authentication

Agent identities support authentication with Model Context Protocol (MCP) servers that accept Agent Identity credentials. To configure MCP server authentication:

1. Assign your Agent Identity the proper RBAC role for the underlying service powering the MCP server (refer to specific MCP server documentation for required roles)
2. Specify the scope URI of the service when connecting the MCP server to your agent (for example, `http://ai.azure.com` for Azure AI Foundry MCP server)

When the agent invokes the MCP server, it uses the available Agent Identity to obtain an authorization token from the scope URI and passes it to the MCP server for authentication.

## Next step

[Publish agents in Azure AI Foundry](../how-to/publish-agent.md)