---
title: "Publish agents to Microsoft 365 Copilot and Microsoft Teams"
description: "Publish a Microsoft Foundry agent to Microsoft 365 Copilot and Microsoft Teams from the Foundry portal."
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.date: 07/07/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
---

# Publish agents to Microsoft 365 Copilot and Microsoft Teams in the Foundry portal

After you build and test an agent, the next step is often sharing it with others in the surfaces where they already work. Publishing a Foundry agent to Microsoft 365 Copilot and Teams lets you and others interact with and discover your agent through the Microsoft 365 Copilot and Teams UI. What gets published is the agent's stable endpoint, so end users always interact with a consistent agent entity while you seamlessly roll out new agent versions that receive traffic through the endpoint. 

This article explains how to publish agents from the Foundry portal. 

> [!NOTE]
> Publishing from the Foundry portal isn't available for projects that disable public network access because additional networking configuration is required. To publish these agents, use the REST API. For more information, see [Publish a virtual network agent to Microsoft 365 and Teams](./publish-copilot-virtual-network.md).

## Prerequisites

- Access to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs)
- A [Foundry project](../../how-to/create-projects.md) with an agent version you tested and want to publish
- The following role assignments:
    - Permission to create an Azure Bot Service resource (`Microsoft.BotService/botServices/write`) and configure its channels (`Microsoft.BotService/botServices/channels/write`) in the resource group where you publish, such as the **Contributor** or **Owner** role. Foundry roles don't grant these permissions. For details, see [Azure Bot Service setup](../concepts/hosted-agent-permissions.md#azure-bot-service-setup).
    - **Foundry User** role on the Foundry project scope to create, manage, and publish agents.

      [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]
    - For details, see [Role-based access control in the Foundry portal](../../concepts/rbac-foundry.md).
- **Test your agent thoroughly** in the Foundry portal before publishing. Confirm it responds correctly and any tools work as expected.
- **Select the active agent version** you want consumers to interact with in Microsoft 365 and Teams.
- Verify that required Azure resource providers are registered in your subscription. The publishing process creates an Azure Bot Service resource, which requires the `Microsoft.BotService` provider.

   If you use Azure CLI, you can register the provider with:

   ```azurecli
   az provider register --namespace Microsoft.BotService
   ```

## Select an active agent version

The active version is the version that your agent's stable endpoint serves to consumers, so confirm it before you publish. For more information about agent versions and other settings, see [Configure your agent endpoint and settings](./configure-agent.md).

### [Foundry portal](#tab/portal)

Set the active version from either of two entry points.

**From the Details tab**

1. Open your agent and select the **Details** tab.
1. In **Agent configuration**, next to **Active version**, select **Edit**.
1. Select **Always use latest**, or select a specific version.

**From the Publish button**

1. In the Microsoft Foundry portal, select **Publish**.
1. Next to **Active version**, select the arrow.
1. Select **Always use latest**, or select a specific version.

### [REST API](#tab/rest)

To pin traffic to a specific version, update the agent's `version_selector`. Set `agent_version` to the version you want to serve.

```
PATCH {{endpoint}}/agents/{{agent_name}}?api-version=v1
Authorization: ******
Content-Type: application/merge-patch+json

{
  "agent_endpoint": {
    "version_selector": {
      "version_selection_rules": [
        {
          "type": "FixedRatio",
          "agent_version": "2",
          "traffic_percentage": 100
        }
      ]
    }
  }
}
```

---

[!INCLUDE [publish-what-happens](../includes/publish-copilot-what-happens.md)]

## Publish to Microsoft 365 and Teams

Publishing from the portal calls Foundry's Microsoft 365 publish API and builds the Teams app package for you. To publish by using the REST API instead, for example to automate publishing or to publish from a project that disables public network access, see [Publish a virtual network agent to Microsoft 365 and Teams](./publish-copilot-virtual-network.md). Steps 1 through 4 in that article are the REST equivalent of this portal flow and work for any project; only the final networking step is specific to disabled public network access.

You can open the publish dialog from the **Details** tab (in the **Channels** section, select **Teams & Microsoft 365 Copilot**) or from the **Publish** button. These steps use the **Publish** button.

1. In Microsoft Foundry portal, select **Publish**, and then select **Teams and Microsoft 365 Copilot**.

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

For agent publishing limitations, including requirements when your project disables public network access, see [Limitations](./publish-copilot-virtual-network.md#limitations).

## Troubleshoot publishing

Use the following table to resolve errors that occur while you publish from the portal. For more extensive troubleshooting, including how to find a published agent in the store and resolve errors when you chat with it, see [Troubleshooting](./publish-copilot-virtual-network.md#troubleshooting).

| Symptom | Cause | Resolution |
|-------|-------|------------|
| Error publishing the agent | Invalid metadata or version | Ensure the agent has a unique identity (`agent.identity` isn't null). Confirm the developer name is 32 characters or fewer. |
| Azure Bot Service creation fails | Missing permissions or unregistered provider | Confirm you have permission to create resources. Register `Microsoft.BotService` if needed. |
| The **Azure bot services** field shows a `403 AuthorizationFailed` error for `Microsoft.BotService/botServices/write` | Your identity doesn't have permission to create or update the Azure Bot Service resource in the target resource group | Assign the **Contributor** or **Owner** role on the resource group that contains the bot service, then refresh your credentials and reopen the publish flow. |

If the portal shows **This agent uses an older format that can no longer be published to Teams and Microsoft 365 Copilot. Upgrade to new format to publish.**, the agent uses the older agent application format, which the generally available publish flow doesn't support for new publishing. Upgrade the agent to the new format, and then publish. Existing agents in the older format keep working and can still be updated. See [Migrate from agent applications to the new agent model](./migrate-agent-applications.md).

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
- [Publish a virtual network agent to Microsoft 365 and Teams](./publish-copilot-virtual-network.md)
- [Role-based access control in the Foundry portal](../../concepts/rbac-foundry.md)
- [Migrate from Agent Applications to the new agent model](./migrate-agent-applications.md)
