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
- Permissions to publish agents in your project. For details, see [Role-based access control in the Foundry portal](../../../concepts/rbac-foundry.md).
- An Azure subscription where you can create Azure Bot Service resources and Microsoft Entra ID app registrations

## Before you begin

- If your agent uses tools that access Azure resources, plan to reassign any required permissions after publishing. A published agent application uses its own agent identity. For details, see [Agent identity concepts in Microsoft Foundry](../concepts/agent-identity.md) and [Publish and share agents in Microsoft Foundry](publish-agent.md).
- Decide whether you want **Shared scope** or **Organization scope** for distribution. If you choose **Organization scope**, an admin must approve the app before it's available to users.

## Publish your agent as an agent application

> [!NOTE]
> To work programmatically, you can also use the [C# sample](https://github.com/OfficeDev/microsoft-365-agents-toolkit-samples/tree/dev/ProxyAgent-CSharp).

1. In the Microsoft Foundry portal, select your agent version.
1. Select **Publish** to create an agent application.

    :::image type="content" source="../media/publish-agent.png" alt-text="Screenshot of the Publish option for an agent version in Microsoft Foundry." lightbox="../media/publish-agent.png":::

1. Select **Publish** again, and then select **Publish to Teams and Microsoft 365 Copilot**.
1. Enter the information in the window that appears.

   An application ID and tenant ID are created automatically.

   1. In the Azure Bot Service dropdown, select **Create an Azure Bot Service** to create the bot resource.

1. Complete the required metadata, such as the name, description, icons, publisher information, privacy policy, and terms of use.

   Don't include secrets in any metadata fields.

1. Select **Prepare Agent** to start packaging the agent.
1. When the Microsoft 365 publishing package is ready, choose one of the following options:
   - Download the package to test it.
   - Continue the in-product publishing flow for Microsoft Teams and Microsoft 365 Copilot.

## Choose a publish scope

Choose the scope that matches how you want people to discover your agent.

- **Shared scope**: The agent appears under **Your agents** in the agent store for Microsoft 365 Copilot.
- **Organization scope**: The agent appears under **Built by your org** in the agent store for Microsoft 365 Copilot. This option requires admin approval.

:::image type="content" source="../media/agent-store.png" alt-text="Screenshot of the agent store showing sections such as Your agents and Built by your org." lightbox="../media/agent-store.png":::

## Download and test the publishing package

If you download the package, test it before broad distribution.

1. After the package finishes preparing, download it from the publishing UI.
1. In Microsoft Teams, upload the downloaded package for testing.
1. Confirm your agent loads and responds as expected.

## Troubleshooting

Use these checks to unblock common publishing issues.

- **Azure Bot Service creation fails**: Confirm you have permission to create resources in the selected Azure subscription and that required providers are registered for your subscription.
- **Organization scope agent doesn't appear**: Confirm an admin approved the app and that app policies in your tenant allow users to access it.
- **Agent works in Foundry but fails after publishing**: If your agent uses tools that call Azure resources, make sure the published agent identity has the required roles. For details, see [Agent identity concepts in Microsoft Foundry](../concepts/agent-identity.md).

## Related content

[Publish and share agents in Microsoft Foundry](publish-agent.md)

[Publish an agent to Agent 365](agent-365.md)
