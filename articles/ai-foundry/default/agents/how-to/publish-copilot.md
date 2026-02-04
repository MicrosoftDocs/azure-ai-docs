---
title: Publish agents to Microsoft 365 Copilot and Microsoft Teams
description: Publish a Microsoft Foundry agent to Microsoft 365 Copilot and Microsoft Teams by creating an agent application and packaging it for distribution.
author: aahill
ms.author: aahi
ms.date: 01/21/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Publish agents to Microsoft 365 Copilot and Microsoft Teams

Use this article to publish a Microsoft Foundry agent so people can use it in Microsoft 365 Copilot and Microsoft Teams.

Publishing creates an agent application with a stable endpoint and then prepares a Microsoft 365 publishing package for testing and distribution.

## Prerequisites 

- Access to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs)
- A [Foundry project](../../../how-to/create-projects.md) with an agent version you tested and want to publish
- The following role assignments:
  - **Azure AI Project Manager** role on the Foundry project scope to publish agents
  - **Azure AI User** role on the Agent Application scope to invoke or chat with published agents
  - For details, see [Role-based access control in the Foundry portal](../../../concepts/rbac-foundry.md).
- An Azure subscription where you can create Azure Bot Service resources and Microsoft Entra ID app registrations
- Permissions to register applications in Microsoft Entra ID (for the automatic app registration)

## Before you begin

- **Test your agent thoroughly** in the Foundry portal before publishing. Confirm it responds correctly and any tools work as expected.
- If your agent uses tools that access Azure resources, plan to reassign any required permissions after publishing. A published agent application uses its own agent identity separate from your project identity. For details, see [Agent identity concepts in Microsoft Foundry](../concepts/agent-identity.md) and [Publish and share agents in Microsoft Foundry](publish-agent.md).
- Decide whether you want **Shared scope** or **Organization scope** for distribution:
  - **Shared scope**: Best for personal or team-level testing. No admin approval required.
  - **Organization scope**: Best for organization-wide distribution. Requires admin approval before users can access it.
- Verify that required Azure resource providers are registered in your subscription. The publishing process creates an Azure Bot Service resource, which requires the `Microsoft.BotService` provider.

## Publish your agent as an agent application

> [!NOTE]
> To work programmatically, you can also use the [C# sample](https://github.com/OfficeDev/microsoft-365-agents-toolkit-samples/tree/dev/ProxyAgent-CSharp).

1. In the Microsoft Foundry portal, select your agent version.

   **Expected result**: The agent details page opens, showing the agent configuration and a **Publish** button.

1. Select **Publish** to create an agent application.

    :::image type="content" source="../media/publish-agent.png" alt-text="Screenshot of the Publish option for an agent version in Microsoft Foundry." lightbox="../media/publish-agent.png":::

   **Expected result**: A publishing dialog opens with distribution options.

1. Select **Publish** again, and then select **Publish to Teams and Microsoft 365 Copilot**.

   **Expected result**: The Microsoft 365 publishing configuration window opens.

1. Enter the information in the window that appears.

   1. An application ID and tenant ID are created automatically. Note these values for troubleshooting.

   1. In the Azure Bot Service dropdown, select **Create an Azure Bot Service** to create the bot resource.

   **Expected result**: The portal creates an Azure Bot Service resource in your subscription and displays the resource name.

1. Complete the required metadata:

   | Field | Description |
   |-------|-------------|
   | **Name** | Display name for your agent (appears in the agent store) |
   | **Description** | Brief description of what your agent does |
   | **Icons** | Small (32x32) and large (192x192) icons in PNG format |
   | **Publisher information** | Your organization name and contact details |
   | **Privacy policy** | URL to your privacy policy |
   | **Terms of use** | URL to your terms of use |

   > [!WARNING]
   > Don't include secrets, API keys, or sensitive information in any metadata fields. These fields are visible to users.

1. Select **Prepare Agent** to start packaging the agent.

   **Expected result**: The portal shows a progress indicator while it creates the Microsoft 365 publishing package. This process typically takes 1-2 minutes.

1. When the Microsoft 365 publishing package is ready, choose one of the following options:
   - **Download the package** to test it locally before broad distribution.
   - **Continue the in-product publishing flow** for Microsoft Teams and Microsoft 365 Copilot.

   **Verification**: After the package is ready, confirm the status shows "Ready" or "Published" in the agent details page.

## Choose a publish scope

Choose the scope that matches how you want people to discover your agent.

| Scope | Visibility | Admin approval | Best for |
|-------|------------|----------------|----------|
| **Shared scope** | Appears under **Your agents** in the agent store | Not required | Personal testing, small teams, or pilots |
| **Organization scope** | Appears under **Built by your org** in the agent store | Required | Organization-wide distribution, production deployments |

:::image type="content" source="../media/agent-store.png" alt-text="Screenshot of the agent store showing sections such as Your agents and Built by your org." lightbox="../media/agent-store.png":::

### Shared scope details

- The agent is available immediately after publishing.
- Only the publisher can see and use the agent initially.
- You can share the agent with specific users by providing them the agent link.
- No admin approval or tenant configuration required.

### Organization scope details

- After you publish, an admin must approve the app in the Microsoft 365 admin center.
- Once approved, the agent appears in the **Built by your org** section for all users in your tenant.
- App policies in your tenant control which users can access the agent.
- To check approval status, go to the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested) and look for your agent under **Requests**.

## Download and test the publishing package

If you download the package, test it before broad distribution.

1. After the package finishes preparing, download it from the publishing UI.

   **Expected result**: A `.zip` file downloads to your local machine.

1. In Microsoft Teams, upload the downloaded package for testing:
   1. Open Microsoft Teams.
   1. Go to **Apps** > **Manage your apps** > **Upload an app**.
   1. Select **Upload a custom app** and choose the downloaded `.zip` file.

   **Expected result**: Teams installs the app and shows it in your apps list.

1. Open the agent in Teams and send a test message.

   **Verification checklist**:
   - [ ] The agent responds to messages.
   - [ ] Any configured tools work correctly.
   - [ ] The agent identity has access to required Azure resources (if applicable).
   - [ ] Response times are acceptable.

1. If your agent uses tools that access Azure resources, verify the published agent identity has the required role assignments. See [Agent identity concepts in Microsoft Foundry](../concepts/agent-identity.md) for details on reassigning permissions.

## Troubleshooting

Use these checks to unblock common publishing issues.

| Issue | Cause | Resolution |
|-------|-------|------------|
| Azure Bot Service creation fails | Missing permissions or unregistered resource provider | Confirm you have permission to create resources in the selected Azure subscription. Register the `Microsoft.BotService` provider if needed. |
| Organization scope agent doesn't appear | Admin approval pending or app policies block access | Confirm an admin approved the app in the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested). Check that app policies in your tenant allow users to access it. |
| Agent works in Foundry but fails after publishing | Agent identity missing required role assignments | The published agent uses its own identity. Reassign RBAC permissions to the new agent identity for any Azure resources the agent accesses. See [Agent identity concepts](../concepts/agent-identity.md). |
| Package upload fails in Teams | Invalid package format or missing metadata | Verify all required metadata fields are complete. Re-download the package and try again. |
| Agent doesn't respond in Teams | Bot Service configuration issue | Verify the Azure Bot Service resource is running. Check the Bot Service logs in the Azure portal for errors. |
| Users can't find the agent in the store | Wrong scope or approval pending | For shared scope, share the direct link. For organization scope, confirm admin approval is complete. |

### Verify your publishing configuration

To confirm your agent is published correctly:

1. In the Foundry portal, go to your agent and check the **Published** status.
1. Note the **Application ID** and **Tenant ID** from the publishing details.
1. In the Azure portal, verify the Azure Bot Service resource exists and is running.
1. For organization scope, check the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested) for approval status.

## Next steps

- [Publish and share agents in Microsoft Foundry](publish-agent.md) — Learn about agent applications, identity, and other publishing options.
- [Publish an agent to Agent 365](agent-365.md) — Publish to Microsoft Agent 365 for enterprise-wide distribution.
- [Agent identity concepts in Microsoft Foundry](../concepts/agent-identity.md) — Understand how agent identity works after publishing.

## Related content

- [Role-based access control in the Foundry portal](../../../concepts/rbac-foundry.md)
- [Microsoft Foundry Playgrounds](../../../concepts/concept-playgrounds.md)
