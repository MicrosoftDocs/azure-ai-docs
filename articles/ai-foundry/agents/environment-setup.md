---
title: Set up your environment for Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Use this guide to set up your agent environment
manager: nitinme
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/11/2026
ms.custom: azure-ai-agents
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Set up your environment

[!INCLUDE [version-banner](../includes/version-banner.md)]

In this article, you deploy the infrastructure needed to create agents with Foundry Agent Service. After completing this setup, you can create and configure agents using either the SDK of your choice or the Foundry portal.

Creating your first agent is a two-step process:

1. Set up your agent environment (this article).
1. Create and configure your agent.

### Required permissions 

| Action                                                                 | Required Role                   |
|------------------------------------------------------------------------|----------------------------------|
| Create an account and project                                          | Azure AI Account Owner           |
| [standard setup](#choose-your-setup) Only: Assign RBAC for required resources (Cosmos DB, Search, Storage, etc.) | Role Based Access Control Administrator  |
| Create and edit agents                                                 | Azure AI User                    |

## Set up your agent environment
To get started, you need a Microsoft Foundry resource and a Foundry project.  
Agents are created within a specific project, and each project acts as an isolated workspace. This means:
* All agents in the same project share access to the same file storage, thread storage (conversation history), and search indexes.
* Data is isolated between projects. Agents in one project cannot access resources from another.
Projects are currently the unit of sharing and isolation in Foundry. See the [what is AI foundry](../../ai-foundry/what-is-foundry.md) article for more information on Foundry projects.

### Prerequisites 

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* Ensure that the individual creating the account and project has the **Azure AI Account Owner** role at the subscription scope
* If configuring a [standard setup](#choose-your-setup), the same individual must also have permissions to assign roles to required resources (Cosmos DB, Azure AI Search, Azure Blob Storage). For more information on RBAC roles, specific to Agent Service, see [Agent Service RBAC roles](../concepts/rbac-foundry.md).
    * The built-in role needed is **Role Based Access Administrator**.
    * Alternatively, having the **Owner** role at the subscription level also satisfies this requirement.
    * The key permission needed is: `Microsoft.Authorization/roleAssignments/write`

### Choose your setup
Agent Service offers three environment configuration modes to suit different needs: 

- **Basic Setup**:  

   This setup is compatible with OpenAI Assistants and manages agent states using the platform's built-in storage. It includes the same tools and capabilities as the Assistants API, with added support for non-OpenAI models and tools such as Azure AI Search, and Bing. 

- **Standard Setup**:  

   Includes everything in the basic setup and fine-grained control over your data by allowing you to use your own Azure resources. All customer data—including files, threads, and vector stores—are stored in your own Azure resources, giving you full ownership and control. 

- **Standard Setup with Bring Your Own (BYO) Virtual Network**:  

   Includes everything in the Standard Setup, with the added ability to operate entirely within your own virtual network. This setup supports Bring Your Own Virtual Network (BYO virtual network), allowing for strict control over data movement and helping prevent data exfiltration by keeping traffic confined to your network environment. 

### Compare setup options

> [!NOTE]
> Private Network Isolation in the table below refers to Secured Agent outbound communication. Basic setup doesn't apply, and you can use Private Network Isolation for your Agents with Standard Setup only.
> 
> Inbound secured communication can be applied to all of setups below, by adding a private endpoint and disabling the inbound public access for your Foundry Account.

| Use Cases                                                                | Basic Setup | Standard Setup with Public Networking | Standard Setup with Private Networking |
|--------------------------------------------------------------------------|-------------|----------------------------------------|----------------------------------------|
| Get started quickly without managing resources                          | ✅          |                                        |                                        |
| All conversation history, file, and vector stores are stored in your own resources |             | ✅                                      | ✅                                      |
| Support for Customer Managed Keys (CMK)                                 |             | ✅                                      | ✅                                      |
| Private Network Isolation (Bring your own virtual network)              |             |                                        | ✅                                      |

### Deployment options

To customize these templates, see [use your own resources](how-to/use-your-own-resources.md).

If you want support for Private Network Isolation, see [network-secured setup](how-to/virtual-networks.md) for more information on how to bring your own virtual network.

| Description and Autodeploy  |  Diagram (click to zoom in) |
|-----------------------------|------------------------------|
| Deploy a basic agent setup that uses **Managed Identity** for authentication. <br> An account and project are created. <br> A GPT-4.1 model is deployed. <br> A Microsoft-managed Key Vault is used by default. <br> [![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure-ai-foundry%2Ffoundry-samples%2Frefs%2Fheads%2Fmain%2Finfrastructure%2Finfrastructure-setup-bicep%2F40-basic-agent-setup%2Fazuredeploy.json) | :::image type="content" source="./media/quickstart/basic-setup-resources-foundry.png" alt-text="An architecture diagram for basic agent setup." lightbox="./media/quickstart/basic-setup-resources-foundry.png"::: |
| Deploy a standard agent setup that uses **Managed Identity** for authentication. <br>An account and project are created. <br> A GPT-4.1 model is deployed. <br> Azure resources for storing customer data—**Azure Storage**, **Azure Cosmos DB**, and **Azure AI Search**—are automatically created if existing resources aren't provided. <br> These resources are connected to your project to store files, threads, and vector data. <br> A Microsoft-managed Key Vault is used by default. <br> [![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure-ai-foundry%2Ffoundry-samples%2Frefs%2Fheads%2Fmain%2Finfrastructure%2Finfrastructure-setup-bicep%2F41-standard-agent-setup%2Fazuredeploy.json) | :::image type="content" source="./media/quickstart/standard-agent-setup.png" alt-text="An architecture diagram for standard agent setup." lightbox="./media/quickstart/standard-agent-setup.png"::: |

### [Optional] Model selection in autodeploy template

> [!IMPORTANT]
> **Don't change the modelFormat parameter.** 
>
> The templates only support deployment of Azure OpenAI models. See which Azure OpenAI models are supported in the [model support](./concepts/model-region-support.md) article.

You can customize the model used by your agent by editing the model parameters in the autodeploy template. To deploy a different model, you need to update at least the `modelName` and `modelVersion` parameters. 

By default, the deployment template is configured with the following values:

| Model Parameter  | Default Value  |
|------------------|----------------|
| modelName        | gpt-4.1        |
| modelFormat      | OpenAI (for Azure OpenAI) |
| modelVersion     | 2025-04-14     |
| modelSkuName     | GlobalStandard |
| modelLocation    | eastus         |

### Verify your deployment

After deployment completes (typically 5-10 minutes), verify that your resources were created successfully:

1. Go to the [Azure portal](https://portal.azure.com).
1. Search for your resource group name.
1. Confirm that the following resources exist:
   - **Basic setup**: Foundry account, project, and model deployment.
   - **Standard setup**: All basic resources plus Azure Storage account, Azure Cosmos DB account, and Azure AI Search service.

> [!TIP]
> If the deployment fails, check the **Deployments** section in your resource group for error details. Common issues include insufficient quota for the model or missing permissions.

### Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Deployment fails with quota error | Insufficient quota for GPT-4.1 in the selected region | Request a quota increase or select a different region |
| Permission denied during deployment | Missing **Role Based Access Administrator** role | Ask your subscription owner to grant you the required role |
| Resources created but agent creation fails | Project not properly connected to resources | Verify the connection in the Foundry portal under **Project settings** > **Connected resources** |
| Model not available | Model not deployed in your region | Check [model region support](./concepts/model-region-support.md) and select an available region |

### What's next?

:::moniker range="foundry-classic"

* [Create your first agent](quickstart.md)

:::moniker-end

:::moniker range="foundry"

* [Create your first agent](../quickstarts/get-started-code.md)

:::moniker-end

* Explore more:
    * [Use your existing resources](how-to/use-your-own-resources.md)
    * [Network secured agent setup](how-to/virtual-networks.md)
