---
title: "Microsoft Agent 365 and Microsoft Foundry"
description: "Learn how Microsoft Agent 365 provides governance, security, and lifecycle management for AI agents built in Microsoft Foundry."
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.date: 04/14/2026
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
---

# Foundry agents in Microsoft Agent 365 

This article describes how Foundry agents can be managed and governed in Microsoft Agent 365. Additionally, it describes how AI teammates can be created, approved, and hired in A365. 

## What is Microsoft Agent 365?

[Microsoft Agent 365 (A365)](/microsoft-agent-365/overview) is Microsoft's IT admin control plane for AI agents. It helps you apply identity, security, governance, and lifecycle management controls to AI agents and manage them at scale, regardless of where they're built or acquired.

### Agent 365 core capabilities

- **Registry**: A complete inventory of agents in the organization, including agents built in Microsoft Foundry and Copilot Studio, agents registered by administrators, and shadow agents discovered in the tenant.
- **Access control**: Brings agents under management and limits access to only the resources they need by using Microsoft Entra–based controls and risk-based Conditional Access policies.
- **Visualization**: Enables organizations to explore connections between agents, people, and data, and to monitor agent behavior and performance in real time.
- **Interoperability**: Equips agents with access to Microsoft 365 apps and organizational data so they can participate in real workflows. Agents can also be connected to Work IQ to apply organizational context and knowledge.
- **Security**: Protects agents from threats and vulnerabilities by integrating with Microsoft's security stack. It also helps protect data agents create or use from oversharing, leaks, and risky behavior.

## How does Foundry integrate with Agent 365?

All Foundry agents automatically appear in the Agent 365 agent registry on creation. In A365, admins can see critical agent metadata such as the name, description, tools, agent identity, agent blueprint, and more associate with an agent. 

## Create AI teammates

There's also a specific use case in which Foundry hosted agents can be pushed as AI teammates to Agent 365. Once approved in the Microsoft admin center, these agents can then be hired by others in your organization. This experience currently has no UI and must be completed by using a code sample.


The rest of this article walks through that process.

### Prerequisites 

- Enrollment in the [Frontier preview program](https://adoption.microsoft.com/en-us/copilot/frontier-program/).
- An Azure subscription where you can create resources.
- The required permissions:
  - **Owner** role on the Azure subscription
  - **Azure AI User** or **Cognitive Services User** role at subscription or resource group scope
  - A tenant admin role that can approve agent requests in the Microsoft 365 admin center
- Use a region that supports hosted agents. For the current supported regions, see [Hosted agents in Microsoft Foundry](../concepts/hosted-agents.md#region-availability).
- [Azure CLI](/cli/azure/install-azure-cli)
- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd)
- [Docker](https://www.docker.com/)
- [.NET 9.0 SDK](https://dotnet.microsoft.com/download)

### What the sample creates

The sample provisions Azure resources and publishes a hosted agent end-to-end. Specifically: 

- Creates or updates Azure resources required to run the sample.
- Creates an agent version and configures endpoint traffic to route to always route to that version
- Submits an AI teammate request that requires admin approval in the Microsoft 365 admin center.

### Run the code sample
Follow the steps in the [FoundryA365 sample README on GitHub](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/FoundryA365).

At a high level, you typically:

1. Clone the `foundry-samples` repository.
1. Change to the `samples/csharp/FoundryA365` directory.
1. Run the Azure Developer CLI (`azd`) workflow described in the README (for example, sign in, create resources, and deploy).
1. Wait for provisioning, container build, and deployment to complete. The first run can take longer.

If you want a quick command-oriented starting point, the sample generally follows this flow (see the README for the complete, up-to-date sequence):

```bash
az login
azd auth login
azd provision
azd env get-values
```

> [!NOTE]
> Depending on your tenant settings, you might need to sign in with more Azure CLI scopes before provisioning (for example, for Foundry, Microsoft Graph, and Azure Resource Manager). Follow the exact commands in the sample README.

When the sample completes successfully (for example, the `azd` commands finish without errors), you have a published agent application and a digital worker request ready for approval in the Microsoft 365 admin center. Once approved by an admin, you should see the agent in the Agent 365 registry. You might not see anything to approve yet until you complete the approval steps in the README.

### Validate

1. Approve the agent blueprint request in the Microsoft 365 admin center.
  You can review approval requests at <https://admin.cloud.microsoft/?#/agents/all/requested>.
  :::image type="content" source="../media/approve-agent.png" alt-text="Screenshot of an agent awaiting or showing approval in the Microsoft 365 admin center agent registry." lightbox="../media/approve-agent.png":::
1. Once approved, verify your agent shows up in the Agent 365 agent registry.
  :::image type="content" source="../media/agent-in-registry.png" alt-text="Screenshot of an approved agent in A365 registry." lightbox="../media/agent-in-registry.png":::
1. Configure Teams integration in the Teams Developer Portal:
    1. Go to the [Teams Developer Portal](https://dev.teams.microsoft.com/tools/agent-blueprint) and locate your approved agent blueprint.
    1. If you don't see your blueprint, copy the blueprint ID from `azd env get-values`. Then open any blueprint and replace the blueprint ID in the browser URL with your blueprint ID.
1. In Microsoft Teams, verify that you can find the agent and create an instance:
    1. Go to **Apps**.
    1. Go to **Agents for your team**.
    1. Find your agent and create an instance.
    
  :::image type="content" source="../media/create-instance.png" alt-text="Screenshot of creating an agent instance of a digital worker in Microsoft Teams." lightbox="../media/create-instance.png":::

### Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| `azd provision` fails before resource creation starts | Missing permissions | Confirm you have **Owner** on the subscription and **Azure AI User** (or **Cognitive Services User**) at subscription or resource group scope. |
| `azd provision` fails with a region or hosted-agent availability message | Wrong region | Create all resources for this sample in a region that hosted agents are supported in. |
| Container build or push fails | Docker isn't running | Start Docker, and then run `azd provision --verbose` again. |
| You can't find the agent to approve | Approval step not completed or you don't have the required tenant permissions | Verify tenant admin permissions and confirm the deployment completed successfully. |
| You can't find your blueprint in the Teams Developer Portal list | Portal only shows the first 100 blueprints | Open any blueprint and replace the blueprint ID in the URL with your blueprint ID from `azd env get-values`. |


## Related content

- [Configure and share your agent](./configure-agent.md)
- [Publish agents to Microsoft 365 Copilot and Microsoft Teams](./publish-copilot.md)
- [Migrate from Agent Applications to the new agent model](./migrate-agent-applications.md)
