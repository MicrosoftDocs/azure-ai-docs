---
title: include file
description: include file
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: include
ms.date: 07/07/2026
ai-usage: ai-assisted
---
<!-- Shared "what happens when you publish" content for Microsoft 365 and Teams. Included by publish-copilot.md and publish-cilot-virtual-network.md. -->

## What happens when you publish?

When you publish an agent, Foundry performs the following steps:

- Validates the properties you submit, such as the display name, description, and version.
- Compiles a Teams app manifest as a `.zip` package. For more information, see [App manifest schema for Microsoft Teams](/microsoftteams/platform/teams-sdk/teams/manifest).
- Submits the manifest to the Microsoft 365 Copilot and Teams agent catalogs on your behalf.
- Enables the `activity` protocol, which the agent needs to exchange messages with Microsoft 365 and Teams.
- Enables an authorization scheme, either `BotServiceRbac` or `BotServiceTenant`, that controls who can call the agent, based on the scope you select.

### Who can see and call the agent

The scope you select controls *visibility* — who can discover the agent in the Microsoft 365 Copilot and Teams stores. Foundry sets the matching authorization scheme, which controls who can *call* the agent:

- **Just you** (Foundry portal) or `publishScope` set to `Shared` (REST API): Enables `BotServiceRbac` and requires no admin approval. The agent appears in the stores only for you. If you add it to a Teams chat, participants who have the required Foundry permissions on the project can use it.
- **People in your organization** (Foundry portal) or `publishScope` set to `Tenant` (REST API): Enables `BotServiceTenant` and requires admin approval in the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested). After approval, the agent appears for everyone in your tenant under **Built by your org**, and anyone in the tenant can discover and use it.
