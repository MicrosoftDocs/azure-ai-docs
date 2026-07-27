---
title: "Publish an autopilot in Microsoft Agent 365"
description: "Learn how to publish a Foundry Hosted agent as an autopilot in Microsoft Agent 365, submit it for approval, and validate it in Teams."
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.date: 06/05/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
---

# Publish an autopilot in Microsoft Agent 365

Publish a Foundry Hosted agent as an autopilot in Microsoft Agent 365 so an admin can approve it and make it available in Microsoft 365 surfaces such as Microsoft Teams.

For an overview of how Foundry integrates with A365, supported agent types, data collection, and data residency, see [Microsoft Agent 365 integration with Foundry](../concepts/agent-365-integration.md).

> [!IMPORTANT]
> This flow uses Hosted agents. Review [Hosted agents in Foundry Agent Service](../concepts/hosted-agents.md) before you start.

## Prerequisites

Microsoft Agent 365 is generally available.

- **Licensing:**
  - Microsoft 365 licensing that supports Microsoft Agent 365. Agent 365 works best with Microsoft E5, and at least one user in your organization must have a qualifying [Microsoft Agent 365 license](https://www.microsoft.com/microsoft-agent-365#plans-and-pricing) such as Microsoft 365 Copilot.
  - A Microsoft 365 license assigned to the users who create, approve, or use the agent.
- **Azure permissions:**
  - An Azure subscription where you can create resources.
  - **Owner** at the subscription or resource group scope. The `azd` workflow creates Azure resources and assigns required roles automatically; Owner provides the permissions needed for both.
  - **Foundry User** or **Foundry Project Manager** at the Foundry project scope to create and deploy agents.

    [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

    For the full permission matrix, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).
  - **Owner** or **Contributor** at the resource group scope to create and configure the Azure Bot Service resource. Foundry-scoped roles (**Foundry User**, **Foundry Project Manager**, and similar) don't include `Microsoft.BotService/*` permissions.
- **Microsoft 365 admin permissions:**
  - **AI Administrator** or **Global Administrator** in the Microsoft 365 admin center to approve pending agent requests.
- **Tenant and service setup:**
  - Use a region that supports Hosted agents. For the current supported regions, see [Hosted agents in Foundry Agent Service](../concepts/hosted-agents.md#region-availability).
  - If the `Microsoft.BotService` resource provider isn't already registered in your subscription, register it:

    ```azurecli
    az provider register --namespace Microsoft.BotService
    ```

- **Local tools:**
  - [Azure CLI](/cli/azure/install-azure-cli)
  - [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd)
  - [Docker](https://www.docker.com/)
  - [.NET 9.0 SDK](https://dotnet.microsoft.com/download)

## What the sample creates

The sample provisions the Azure infrastructure required by the current template and publishes a Hosted agent end-to-end. Specifically:

- Creates or updates the Azure resources required by the sample template, including a Foundry account and project, model deployment, hosted agent and agent version, Azure Container Registry, Azure Bot Service resource, and Application Insights with a Log Analytics workspace.
- Creates an agent version and configures endpoint traffic to always route to that version.
- Submits an autopilot request that creates an agent blueprint in the Microsoft 365 admin center for admin approval.

### Run the code sample

Follow the steps in the [FoundryA365 sample README on GitHub](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/foundry-autopilot-agent#readme). Follow the sample README for the complete, authoritative command sequence. After the sample completes, return here to verify the deployment and complete the admin approval flow.


### Provision and deploy

> [!NOTE]
> Depending on your tenant settings, you might need to sign in with more Azure CLI scopes before provisioning (for example, for Foundry, Microsoft Graph, and Azure Resource Manager). If `azd auth login` returns an authorization error, see the sample README for the required sign-in commands and scopes.

The sample provisions Azure resources, builds and pushes a container, and deploys the agent. Here is the high-level command flow (see the README for the complete, authoritative sequence):

```bash
az login
azd auth login
azd provision
azd env get-values
```

### Verify deployment before approval

Verify the following before you open the Microsoft 365 admin center:

1. Run `azd env get-values` and save the output. Note especially the bot app ID and messaging endpoint — you need these values in the Developer verification steps.
1. Confirm the `azd` deployment completes successfully with no failed resources.
1. Confirm the sample completed the publishing step and submitted the autopilot request.

When the sample completes successfully, you have a published agent application and an agent blueprint ready for approval in the Microsoft 365 admin center. After an admin approves the request, the agent appears in the Agent 365 registry.

## Validate the deployment

### Admin approval

A Microsoft 365 admin must approve the agent blueprint before it's available in Teams.

1. Sign in to the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested) and locate the pending agent blueprint request.
  :::image type="content" source="../media/approve-agent.png" alt-text="Screenshot of an agent awaiting or showing approval in the Microsoft 365 admin center agent registry." lightbox="../media/approve-agent.png":::
1. Approve the request. After approval, verify your agent appears in the Agent 365 agent registry.
  :::image type="content" source="../media/agent-in-registry.png" alt-text="Screenshot of an approved agent in A365 registry." lightbox="../media/agent-in-registry.png":::

### Developer verification

After an admin approves the request, complete these verification steps.

1. In the [Teams Developer Portal](https://dev.teams.microsoft.com/apps), find your approved agent blueprint and confirm its configuration.
    1. Select the agent blueprint from the list.
    1. Verify the messaging endpoint and app ID match the values from `azd env get-values`.
    1. Save any required fields and publish the update if prompted.
1. In Microsoft Teams, verify that you can find the agent and create an instance:
    1. Go to **Apps**.
    1. Go to **Agents for your team**.
    1. Find your agent and create an instance.
    
  :::image type="content" source="../media/create-instance.png" alt-text="Screenshot of creating an agent instance of an autopilot in Microsoft Teams." lightbox="../media/create-instance.png":::

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| `azd provision` fails before resource creation starts | Missing permissions | Confirm you have **Owner** at the subscription or resource group scope (needed for `azd` to create resources and assign roles), and **Foundry User** or **Foundry Project Manager** at the Foundry project scope. |
| Publishing to Teams or Microsoft 365 fails with a Bot Service authorization error | Foundry roles don't include Bot Service permissions | Confirm the identity running the publish step has **Owner** or **Contributor** at the resource group scope. Foundry-scoped roles (**Foundry User**, **Foundry Project Manager**) don't include `Microsoft.BotService/*` permissions. For details, see [Azure Bot Service setup](../concepts/hosted-agent-permissions.md#azure-bot-service-setup). |
| `azd provision` fails with a region or hosted-agent availability message | Wrong region | Create all resources for this sample in a region that Hosted agents are supported in. |
| `azd provision` or `azd auth login` prompts for more sign-in or consent steps | Additional scopes required | Run the exact sign-in commands from the sample README and grant any required Foundry, Microsoft Graph, or Azure Resource Manager scopes before rerunning the workflow. |
| Container build or push fails | Docker isn't running | Start Docker, and then run `azd provision --verbose` again. |
| You can't find the agent to approve | Approval step not completed or you don't have the required tenant permissions | Verify tenant admin permissions and confirm the deployment completed successfully. |
| You can't find your blueprint in the Teams Developer Portal list | The list might not show every blueprint | Verify the approval completed successfully, rerun `azd env get-values` to recover the sample output, and follow the current sample guidance for locating the approved blueprint. |


## Next steps

After publishing, you can update your agent by deploying a new agent version and repeating the `azd` workflow. To monitor agent activity and set up observability, see [Grant Agent 365 observability permissions](./grant-agent-365-permissions.md).

## Related content

- [Microsoft Agent 365 integration with Foundry](../concepts/agent-365-integration.md)
- [Manage Hosted agent lifecycle](./manage-hosted-agent.md)
- [Publish agents to Microsoft 365 Copilot and Microsoft Teams](./publish-copilot.md)
- [Configure Agent 365 data collection for Microsoft Foundry](./configure-agent-365-data-collection.md)
