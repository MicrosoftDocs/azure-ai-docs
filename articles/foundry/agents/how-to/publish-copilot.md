---
title: "Publish agents to Microsoft 365 Copilot and Microsoft Teams"
description: "Publish a Microsoft Foundry agent to Microsoft 365 Copilot and Microsoft Teams from the Foundry portal."
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

# Publish agents to Microsoft 365 Copilot and Microsoft Teams

After you build and test an agent, the next step is often sharing it with others in the surfaces where they already work. Publishing a Foundry agent to Microsoft 365 Copilot and Teams lets you and others interact with and discover your agent through the Microsoft 365 Copilot and Teams UI. What gets published is the agent's stable endpoint, so end users always interact with a consistent agent entity while you seamlessly roll out new agent versions that receive traffic through the endpoint. You publish to M365/Teams from the Foundry portal.

> [!NOTE]
> If you're migrating from a previous publishing model, see [Migrate from Agent Applications to the new agent model](./migrate-hosted-agent-preview.md).

## Prerequisites

- Access to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs)
- A [Foundry project](../../how-to/create-projects.md) with an agent version you tested and want to publish
- The following role assignments:
    - **Azure AI User** role on the Foundry project scope to create, manage, and publish agents.
    - For details, see [Role-based access control in the Foundry portal](../../concepts/rbac-foundry.md).
- An Azure subscription where Azure Bot Service resources can be created
- **Test your agent thoroughly** in the Foundry portal before publishing. Confirm it responds correctly and any tools work as expected.
- **Select the active agent version** you want consumers to interact with in Microsoft 365 and Teams.
- Verify that required Azure resource providers are registered in your subscription. The publishing process creates an Azure Bot Service resource, which requires the `Microsoft.BotService` provider.

   If you use Azure CLI, you can register the provider with:

   ```azurecli
   az provider register --namespace Microsoft.BotService
   ```

## Select an active agent version in the Foundry UI

For more information on selecting an active agent version and configuring other agent settings, see [Publish and share agents](./configure-agent.md).

1. In the Microsoft Foundry portal, select **Publish**.

    **Expected result**: A publish dropdown opens showing endpoint URLs, the active version, and a link to publish to Teams and Microsoft 365 Copilot.
    :::image type="content" source="../media/publish-dropdown.png" alt-text="Expanded publish dropdown showing options":::

1. Select the arrow icon to the right of **Active version**.

    **Expected result**: A popup opens with options to always use the latest version or select a specific version.
   :::image type="content" source="../media/active-version.png" alt-text="Screenshot of the active version popup showing Always use latest and specific version options.":::

1. Select the active version you want to receive traffic from your agent's stable endpoint.

    **Expected result**: The publish dropdown closes and the **Publish** button displays a checkmark to indicate success.
   ::image type="content" source="../media/success-select-version.png" alt-text="Screenshot of the Publish button with a checkmark indicating the version was successfully selected.":::

## Publish to Microsoft 365 and Teams

1. In Microsoft Foundry portal, select **Publish**, then select **Publish to Teams and Microsoft 365 Copilot**.

   **Expected result**: The **Publish to Teams and Microsoft 365** dialog opens.

1. An Azure Bot Service resource is either automatically created or shown as read-only if one already exists.

1. Complete the required metadata:

   | Field | Description |
   |-------|-------------|
   | **Name** | Display name for your agent (appears in the agent store) |
   | **Publish version** | Three-part version number (major.minor.patch) |
   | **Short description** | One-sentence description of what your agent does |
   | **Description** | Longer description of your agent's responsibilities and the actions it can take |
   | **Developer** | Your name or organization name (under **Author**) |

   To add optional metadata, expand **More** and complete the following fields:

   | Field | Description |
   |-------|-------------|
   | **Developer website** | URL to your website (HTTPS required) |
   | **Terms of use** | URL to your terms of use (HTTPS required) |
   | **Privacy statement** | URL to your privacy policy (HTTPS required) |

   > [!WARNING]
   > Don't include secrets, API keys, or sensitive information in any metadata fields. These fields are visible to users.

1. Select **Next: Publish options**.

1. Choose how to publish. You can either [publish your agent directly from Foundry](#direct-publish) or [download and customize the agent manifest, then manually sideload it in Teams](#download-and-customize).

### Direct publish

1. On the **Publish options** step, select the **Direct publish** tab.

    **Expected result**: Section  **Choose who can use this agent** is displayed.

2. Under **Choose who can use this agent**, select a scope:

   | Option | Behavior | Admin approval | Best for |
   |--------|----------|----------------|----------|
   | **Just you** | Available immediately. The agent appears under **Your agents** in the agent store. Share it with others by sending the agent link. | Not required | Personal testing, small teams, pilots |
   | **People in your organization** | The agent is submitted for admin approval. Your Microsoft 365 admin reviews the request and assigns access. Once approved, the agent appears under **Built by your org** for all tenant users. | Required | Organization-wide distribution, production deployments |

   **Just you**:
   - Available immediately after publishing — no admin approval required.
   - Only you see the agent initially under **Your agents** in the agent store.
   - Share with specific users by sending the agent link.

   **People in your organization**:
   - After publishing, a Microsoft 365 admin must review and approve the request in the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested).
   - Once approved, the agent appears under **Built by your org** in the agent store for all tenant users.
   - App policies in your tenant control which users can access the agent.
   - To check approval status, go to the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested) and look for your agent under **Requests**.

     :::image type="content" source="../media/agent-store.png" alt-text="A screenshot of the Agent store in Microsoft 365 Copilot.":::

1. Select **Publish**.

   **Expected result**: A **Publish successful** dialog confirms the agent was successfully published.

### Download and customize

If you want to customize the agent manifest before distributing:

1. On the **Publish options** step, select the **Download & customize** tab.

    **Expected result**: The tab displays instructions for after downloading and a **Download ZIP** button.

1. Select **Download ZIP**.

   **Expected result**: A `.zip` file containing the agent manifest downloads to your local machine.

1. Customize the manifest in the downloaded package as needed.

1. In Microsoft Teams, upload the package you downloaded
    1. Go to **Apps** > **Manage your apps** > **Upload an app**
    1. Select  **Upload a custom app** or **Submit an app to your org** and choose the downloaded `.zip` file.

## Update a published agent in M365/Teams

### Update the active agent version

To roll out a new agent version, update the agent's version selector in the Foundry portal. The stable endpoint URL stays the same — no need to republish to M365/Teams.

### Update end user metadata in M365/Teams

To update metadata visible in Teams and M365 (display name, descriptions, URLs), in the **Publish** dropdown select **Update agent Teams and Microsoft 365 Copilot display properties**. The updated fields overwrite the existing values; unchanged fields are carried forward; and version will auto increment if not manually incremented.

## Limitations

| Limitation | Description |
| --- | --- |
| File uploads and image generation in Microsoft 365 | These don't work for agents published to Microsoft 365. They work in Microsoft Teams. |
| Private Link | Not supported for Teams or Azure Bot Service integrations. |
| Streaming and citations | Published agents don't support streaming responses or citations. |

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| Error publishing the agent | Invalid metadata or version | Ensure the agent has a unique identity (`agent.identity` is not null). Confirm the developer name is 32 characters or fewer. |
| Azure Bot Service creation fails | Missing permissions or unregistered provider | Confirm you have permission to create resources. Register `Microsoft.BotService` if needed. |
| Organization scope agent doesn't appear | Admin approval pending | Confirm an admin approved in the [M365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested). Check app policies. |
| Agent works in Foundry but fails after publishing | Agent identity missing permissions | Assign RBAC roles to the agent's identity for any Azure resources it accesses. |
| Publishing fails with identity error | The agent doesn't have a unique identity (`agent.identity` is null) | See the [migration guide](./migrate-agent-applications.md) for steps to resolve this. |
| Users can't find the agent | Wrong scope or approval pending | For Individual scope, share the direct link. For Organization scope, confirm admin approval. |

## FAQs

**If I select Organization scope, where do I approve the agent?**

In the Microsoft 365 admin center. Once approved, the agent appears under **Built by your org** in the agent store.

**If I publish my agent to Individual Scope (previously called Shared Scope), how do I share it with others in my organization?**

The agent appears under Your agents in the agent store for Microsoft 365 Copilot. You can share it by sending the agent link to selected users in your organization. 

:::image type="content" source="../media/share-published-agent.png" alt-text="Screenshot of how to share an Individual scoped published agent with others in your org." lightbox="../media/agent-store.png":::

**What happens when I create a new agent version if my agent is published to M365?**

If the version selector is set to "Always use latest" (the default), the new version is automatically served in M365/Teams. If pinned to a specific version, you must update the version selector to serve the new version.

## Related content

- [Configure your agent endpoint and settings](./configure-agent.md)
- [Role-based access control in the Foundry portal](../../concepts/rbac-foundry.md)
- [Migrate from Agent Applications to the new agent model](./migrate-agent-applications.md)
