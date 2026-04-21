---
title: "Migrate from Agent Applications to the new agent model"
description: "Migrate from the legacy Agent Application publishing model to the new agent object model in Microsoft Foundry."
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.date: 04/14/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
---

# Migrate from agent applications to the new agent endpoint and publishing experience

This guide helps you understand the differences between the legacy Agent Application model and the new agent object model, and walks you through migrating your existing agents and published applications.

## Overview of the change

The new agent object model collapses **Agent Applications** and **Agent Deployments** into the **Agent** object itself. Previously, publishing created a separate Agent Application resource with its own identity, endpoint, and deployment. Now, every agent has these capabilities from the moment it's created.

### Before (legacy model)

```
Project → Agent → Agent Version
                     ↓ (publish)
              Agent Application → Deployment → Agent Application Stable Endpoint
                   (unique identity, blueprint)
```

### After (new model)

```
Project → Agent (unique identity, blueprint, stable endpoint from creation)
            ↕
        Agent Version(s)
            ↓ (configure endpoint: version routing, protocols, auth)
        Stable endpoint is ready to invoke
            ↓ (optionally publish to M365/Teams channels)
```

The key shift: **creating an agent is the only step needed** to get a stable endpoint and unique agent identity. There's no separate "publish" step for that. "Publishing" now refers specifically to registering the agent with M365/Teams channels.

## Agent types during the transition

During the transition period, you may encounter three types of agents:

| Type | `agent.identity` | Description |
|------|-------------------|-------------|
| **New agent** | Non-null | Created after the object model update. Has unique identity and blueprint. All new features available. |
| **Draft agent** | Null | Created before the object model update. Uses the shared project identity and blueprint. Is backfilled with the new agent properties (protocols, agent_endpoint, agent_card, etc) but cannot be published to Teams/M365 via it's stable endpoint unless it has a unique agent identity |
| **Agent Application** | N/A (separate resource) | Legacy resource from the old publish flow. Wraps a Deployment pointing to an agent version. |

The `agent.identity` value distinguishes new agents from draft agents: **null means draft, non-null means new**.

## What continues to work

- **Existing Agent Applications** continue to serve traffic through their endpoints.
- **Agents published to M365/Teams** via Agent Applications continue to work.
- **The project endpoint** remains available for backward compatibility (though it's no longer the recommended path).
- **Draft agents** remain fully functional for development and testing in the Foundry project.

## What's different for new agents

| Capability | Legacy (Agent Application) | New (Agent) |
|------------|---------------------------|-------------|
| Unique agent identity | Created at publish time on the Application | Exists from agent creation — no identity change at any point |
| Stable endpoint | Created at publish time on the Application | Exists from agent creation — available immediately |
| Version routing | Via Deployment resource inside Application | Via `version_selector` on `agent_endpoint` (configure, not publish) |
| Publishing to M365/Teams | Publishing the Agent Application's stable endpoint | Publish the agent's stable endpoint |
| Updating versions | Update Deployment to reference new version | Update `version_selector` on agent and configure traffic routing (no republish needed) |
| Protocols | One protocol per Application is supported (e.g. both activity and responses cannot be activated only one) | Multiple protocols simultaneously |
| User isolation | Not supported | Built into agent stable endpoint from creation |

## Migration paths

### Path 1: New agents (no action needed)

If you create agents after the object model update, they automatically get the new model with unique identity, stable endpoint, and all new features. No migration is required.

### Path 2: Upgrade a draft agent

Draft agents (created before the update) use the shared project identity and can't be published via the new model. To upgrade:

1. **Check if your agent is a draft agent**:

   ```
   GET {endpoint}/agents/{agent_name}?api-version=2025-11-15-preview
   Authorization: Bearer {{token}}
   Foundry-Features: AgentEndpoints=V1Preview
   ```

   If `instance_identity` is null in the response, it's a draft agent.

2. **Create a new agent using the same definition**:

   > [!NOTE]
   > There is currently no way to upgrade a draft agent to a unique identity in place. To get a unique identity, create a new agent using the same definition (instructions, tools, model configuration). The new agent automatically receives a unique identity and stable endpoint. An in-place upgrade path is planned for a future update.

3. **Once the new agent is created**, it has a unique identity and you can use all new features including the new publishing experience that uses the agent endpoint.

### Path 3: Migrate an existing Agent Application

If you have an Agent Application published to M365/Teams and want to migrate to the new model:

1. **Create a new agent using the same definition** as the agent behind your Agent Application (instructions, tools, model configuration). The new agent automatically receives a unique identity and stable endpoint. See [Path 2](#path-2-upgrade-a-draft-agent) for details.

2. **Publish the new agent** using the new publish API:

   ```
   POST {endpoint}/agents/{agent_name}/publish?api-version=2025-11-15-preview
   Authorization: Bearer {{token}}
   Content-Type: application/json
   Foundry-Features: AgentEndpoints=V1Preview

   {
     "displayName": "My Agent",
     "version": "1.0.0",
     "shortDescription": "Description of what the agent does",
     "fullDescription": "Full description of agent capabilities",
     "developerName": "Your Organization",
     "website": "https://your-website.com",
     "termsOfUseUrl": "https://your-website.com/terms",
     "privacyStatementUrl": "https://your-website.com/privacy",
     "agentPublishScope": "organization",
     "isDigitalWorker": false
   }
   ```

3. **Verify the new agent works** in M365/Teams with the new stable endpoint.

4. **Decommission the old Agent Application** once you've confirmed the new agent works:
   - Delete the Agent Application Azure resource (this doesn't delete your agent versions).
   - Update any integrations that reference the old Application endpoint URL to use the new agent stable endpoint URL.

### Endpoint URL changes

When migrating, update any code or integrations that reference the old endpoint format:

| Aspect | Legacy endpoint | New endpoint |
|--------|----------------|--------------|
| Responses | `https://{account}.../projects/{project}/applications/{app}/protocols/openai` | `https://{account}.../projects/{project}/agents/{agent}/protocols/openai/v1/responses` |
| Activity | `https://{account}.../projects/{project}/applications/{app}/protocols/activityprotocol` | `https://{account}.../projects/{project}/agents/{agent}/protocols/activityprotocol` |

## Publishing UX during the transition

During the transition, you may see different publishing experiences depending on the agent type:

- **New agents** (`agent.identity` != null): You see the new publishing UX with stable endpoint selection, version routing, and direct publish to M365/Teams.
- **Draft agents** (`agent.identity` == null): You see the legacy Agent Application publishing UX. A banner may indicate the new experience is available with a link to upgrade.

## Timeline and deprecation

| Phase | Status |
|-------|--------|
| New agent object model available | ✅ Available |
| Legacy Agent Applications continue working | ✅ Supported |
| Draft agent identity upgrade gesture | 🔄 Coming soon |
| Agent Application deprecation announced | 📅 Planned |
| Agent Application end of support | 📅 TBD |

## FAQs

**Do I need to migrate immediately?**

No. Existing Agent Applications continue to work. However, new features (traffic splitting, multiple protocols, disable/enable, A2A) are only available on the new agent model.

**Will my Agent Application stop working?**

Not immediately. Agent Applications will be deprecated with advance notice and a migration period. They continue to function until the end-of-support date.

**Can I have both an Agent Application and a new-model agent for the same underlying agent?**

During the transition, yes. The Agent Application and the new agent endpoint can coexist. However, they are separate resources with separate identities and endpoints.

**What happens to RBAC roles I assigned on Agent Application resources?**

RBAC on Agent Application resources doesn't transfer to the agent object. You'll need to assign roles (such as **Foundry Agent Consumer**) on the agent resource for the new endpoint.

**My agent uses tools that authenticate with agent identity. What changes?**

With the new model, the agent has a unique identity from creation — so there's no identity change at publish time. However, if migrating from a draft agent, the agent will get a new identity that differs from both the shared project identity and any Agent Application identity. You'll need to reassign RBAC for downstream resources.

## Related content

- [Publish and share agents in Microsoft Foundry](./publish-agent.md)
- [Publish agents to Microsoft 365 Copilot and Teams](./publish-copilot.md)
- [Agent identity concepts in Foundry](../concepts/agent-identity.md)
