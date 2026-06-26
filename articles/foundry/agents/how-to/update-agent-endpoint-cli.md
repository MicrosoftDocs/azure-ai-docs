---
title: "Update a hosted agent endpoint and agent card"
description: "Patch a Microsoft Foundry hosted agent endpoint and agent card metadata with azd without creating a new hosted agent version."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/15/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Update a hosted agent endpoint and agent card

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use `azd ai agent endpoint update` to patch endpoint and card metadata on an already-deployed Microsoft Foundry agent. You can refresh consumer-facing details without cutting a new agent version.

## Prerequisites

- An existing hosted agent deployed to a Foundry project. `endpoint update` doesn't create a hosted agent.
- An azd project that has the agent declared in `azure.yaml`, or an explicit Foundry project endpoint. For more information, see [Set the azd project context](cli-project-context.md).
- The [azd Foundry extensions installed](install-cli-foundry-extensions.md).
- An authenticated `azd` session.

## Decide when to update metadata

Use `azd ai agent endpoint update` when you only need to refresh metadata that consumers and tooling read about the agent. This metadata includes the public endpoint, display name, description, and contact info.

Common cases include:

- You changed the public-facing display name or description on the agent card and want it reflected in the Foundry portal without redeploying.
- You moved or re-issued the public agent endpoint URL.
- You updated owner or contact metadata on the card for routing or governance.

If you changed the model, instructions, tools, code, or environment variables, don't use `endpoint update`. Those changes need a new version. Run `azd deploy` or `azd up` instead.

## Update the endpoint and card

1. Edit the `agent_endpoint` section, the `agent_card` section, or both in your `agent.yaml`.

1. Run the update command:

   ```bash
   azd ai agent endpoint update
   ```

1. In a multi-service project, pass the service name as a positional:

   ```bash
   azd ai agent endpoint update my-agent
   ```

The CLI reads the two sections from `agent.yaml` and patches the existing agent record. No new agent version is created, no container is rebuilt, and no infrastructure is touched.

## Verify the update

Confirm the change took effect:

```bash
azd ai agent show
```

The output reflects the new endpoint and card values. The version number is unchanged.

## Review fields updated

`endpoint update` only updates endpoint and card metadata. Use the table to decide whether your change requires a full deploy.

| Field on `agent.yaml` | Updated by `endpoint update`? |
|---|---|
| `agent_endpoint` | Yes |
| `agent_card` | Yes |
| `model`, `model_deployment` | No -- requires `azd deploy` |
| `instructions` | No -- requires `azd deploy` |
| `tools`, `toolboxes`, `skills` | No -- requires `azd deploy` |
| `environment_variables` | No -- requires `azd deploy` |
| Container image / entry point / runtime | No -- requires `azd deploy` |

If you aren't sure whether a change qualifies for `endpoint update`, run `azd ai agent doctor` afterward. It flags any divergence between `agent.yaml` and the deployed agent state.

## Related content

- [Diagnose hosted agent issues](agent-doctor.md) to catch `agent.yaml` versus deployed-state drift.
- [Deploy a hosted agent](deploy-hosted-agent.md) when you need a new agent version.
- [Agent YAML reference](../concepts/agent-yaml-reference.md) to understand `agent.yaml` fields.
