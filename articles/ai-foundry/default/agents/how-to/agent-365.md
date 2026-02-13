---
title: Publish a Microsoft Foundry agent to Agent 365
description: Publish a Microsoft Foundry hosted agent to Agent 365 by using the FoundryA365 sample, approve it, and optionally connect it to Microsoft Teams.
author: aahill
ms.author: aahi
ms.date: 01/21/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Publish an agent as a digital worker in Agent 365 

Use this article to publish a Microsoft Foundry hosted agent to as a digital worker Microsoft Agent 365 (Agent 365) by running the FoundryA365 sample.

The sample uses the Azure Developer CLI to create the required Azure resources, publish an agent application, and then guides you through admin approval and (optionally) Microsoft Teams configuration.

## Prerequisites 

- Enrollment in the [Frontier preview program](https://adoption.microsoft.com/en-us/copilot/frontier-program/).
- An Azure subscription where you can create resources.
- The required permissions:
  - **Owner** role on the Azure subscription
  - **Azure AI User** or **Cognitive Services User** role at subscription or resource group scope
  - A tenant admin role for organization-wide configuration
- [Azure CLI](/cli/azure/install-azure-cli)
- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd)
- [Docker](https://www.docker.com/)
- [.NET 9.0 SDK](https://dotnet.microsoft.com/download)
- Git

## Before you begin

- Start Docker before you deploy.
- Treat your deployment outputs as sensitive. The `azd env get-values` output can include IDs and endpoints you don't want to publish.

## Run the sample

Use the FoundryA365 sample on GitHub: https://go.microsoft.com/fwlink/?linkid=2343518

1. Clone the sample repository and switch to the sample folder.

    ```powershell
    git clone https://github.com/microsoft-foundry/foundry-samples.git
    cd foundry-samples\samples\csharp\FoundryA365
    ```

1. Authenticate to Azure and Azure Developer CLI.

    ```powershell
    # Azure CLI
    az login
    az login --scope https://ai.azure.com/.default
    az login --scope https://graph.microsoft.com//.default
    az login --scope https://management.azure.com/.default

    # Azure Developer CLI
    azd auth login
    ```

    > [!NOTE]
    > Depending on your tenant security settings, you might not need all scopes. If authentication succeeds with fewer scopes, you can skip the others.

1. Deploy the sample.

    ```powershell
    azd provision --verbose
    ```

1. Get the deployment outputs.

    ```powershell
    azd env get-values
    ```

    You use these values in the next steps.

## Approve your agent

After the deployment publishes your agent, an admin must approve it before it's available.

1. Go to the Microsoft 365 admin center: https://admin.cloud.microsoft/?#/agents/all/requested
1. Under **Requests**, find your agent.
1. Select **Approve request and activate**.

## Optional: Configure Microsoft Teams integration

To use your Agent 365 agent in Teams, configure the agent blueprint.

1. Open the Teams Developer Portal: https://dev.teams.microsoft.com/tools/agent-blueprint

    The portal lists only 100 agent blueprints. If you don't see your agent blueprint, open any agent blueprint and then replace the agent blueprint ID in the URL with your agent blueprint ID.

1. Get your agent blueprint ID from the deployment outputs.

    ```powershell
    azd env get-values
    ```

1. In the agent blueprint, go to **Configuration** and set **Bot ID** to your agent blueprint ID.

## Validate

1. Confirm the Microsoft 365 admin center approves the agent request.
1. If you configured Teams integration, go to Microsoft Teams and create an agent instance:
    1. Go to **Apps**.
    1. Go to **Agents for your team**.
    1. Find your agent and create an instance.

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| `azd provision` fails before resource creation starts | Missing permissions | Confirm you have **Owner** on the subscription and **Azure AI User** (or **Cognitive Services User**) at subscription or resource group scope. |
| `azd provision` fails with a region or hosted-agent availability message | Wrong region | Create all resources for this sample in **North Central US**. |
| Container build or push fails | Docker isn't running | Start Docker, and then run `azd provision --verbose` again. |
| You can't find the agent to approve | Approval step not completed or you don't have the required tenant permissions | Confirm the deployment completed successfully and you have a tenant admin role to approve requests. |
| You can't find your blueprint in the Teams Developer Portal list | Portal only shows the first 100 blueprints | Open any blueprint and replace the blueprint ID in the URL with your blueprint ID from `azd env get-values`. |

## How this integration works

Microsoft Agent 365 acts as a control plane for enterprise AI agents. It helps your organization register agents, apply security and compliance controls, and make agents available across Microsoft 365 and other environments.

Agent 365 can help you:

- Manage hosted agents at scale with unified identity and lifecycle controls.
- Enforce least-privilege access and compliance controls by using Microsoft Defender, Microsoft Entra, and Microsoft Purview.
- Integrate agents with Microsoft 365 apps.
- Monitor agent activity through centralized management experiences.

When you use Agent 365 with Microsoft Foundry, this sample sets up:

- A Foundry project configured for hosted agents, including container build and storage.
- An agent application that provides a stable endpoint and identity.
- An Azure Bot Service resource that relays requests from Microsoft 365 surfaces to the agent application.
- A hosted agent built from the sample code as a container image.
- A deployment that attaches the hosted agent to the agent application.

For more information about agent applications, identity, and publishing behavior in Foundry, see [Publish and share agents in Microsoft Foundry](publish-agent.md).

## Next steps

- [Publish and share agents in Microsoft Foundry](publish-agent.md)
- [Publish agents to Microsoft 365 Copilot and Microsoft Teams](publish-copilot.md)
- [Agent identity concepts in Microsoft Foundry](../concepts/agent-identity.md)
- [Hosted agents in Microsoft Foundry](../concepts/hosted-agents.md)
- [MCP server authentication](mcp-authentication.md)
