---
title: Set up your environment for Azure AI Foundry Agent Service
titleSuffix: Azure AI Foundry
description: Use this guide to set up your agent environment
manager: nitinme
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda 
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 05/09/2025
ms.custom: azure-ai-agents
---

# Set up your environment

Creating your first agent with Azure AI Foundry Agent Service is a two-step process: 
1. Set up your agent environment.
1. Create and configure your agent using either the SDK of your choice or the Azure Foundry Portal. 

Use this article to learn more about setting up your agents.

### Required permissions 

| Action                                                                 | Required Role                   |
|------------------------------------------------------------------------|----------------------------------|
| Create an account and project                                          | Azure AI Account Owner           |
| **Standard Setup Only:** Assign RBAC for required resources (Cosmos DB, Search, Storage, etc.) | Role Based Access Administrator  |
| Create and edit agents                                                 | Azure AI User                    |

## Set up your agent environment
To get started, you need an account and a project.  
Agents are scoped at the project level, which ensures data isolation—agents within the same project share access to the same resources. 

### Prerequisites 

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).
* Ensure that the individual creating the account and project has the **Azure AI Account Owner** role at the subscription scope
* If configuring **Standard Setup**, the same individual must also have permissions to assign roles to required resources (Cosmos DB, Search, Storage).
    * The built-in role needed is **Role Based Access Administrator**.
    * Alternatively, having the **Owner** role at the subscription level also satisfies this requirement.
    * The key permission needed is: `Microsoft.Authorization/roleAssignments/write`

### Choose your setup
Azure AI Foundry Agent Service offers three environment configuration modes to suit different needs: 

- **Basic Setup**:  

   This setup is compatible with OpenAI Assistants and manages agent states using the platform's built-in storage. It includes the same tools and capabilities as the Assistants API, with added support for non-OpenAI models and tools such as Azure AI Search, and Bing. 

- **Standard Setup**:  

   Includes everything in the basic setup and fine-grained control over your data by allowing you to use your own Azure resources. All customer data—including files, threads, and vector stores—are stored in your own Azure resources, giving you full ownership and control. 

- **Standard Setup with Bring Your Own (BYO) Virtual Network**:  

   Includes everything in the Standard Setup, with the added ability to operate entirely within your own virtual network. This setup supports Bring Your Own Virtual Network (BYO virtual network), allowing for strict control over data movement and helping prevent data exfiltration by keeping traffic confined to your network environment. 

### Compare setup options

| Use Cases                                                                | Basic Setup | Standard Setup with Public Networking | Standard Setup with Private Networking |
|--------------------------------------------------------------------------|-------------|----------------------------------------|----------------------------------------|
| Get started quickly without managing resources                          | ✅          |                                        |                                        |
| All conversation history, file, and vector stores are stored in your own resources |             | ✅                                      | ✅                                      |
| Support for Customer Managed Keys (CMK)                                 |             | ✅                                      | ✅                                      |
| Private Network Isolation (Bring your own virtual network)              |             |                                        | ✅                                      |

### Deployment options
To customize these templates, see [use your own resources](./how-to/use-your-own-resources.md). 

If you want support for Private Network Isolation see [network-secured setup](./how-to/virtual-networks.md) for more information on how to bring your own virtual network.

| Description and Autodeploy  |  Diagram (click to zoom in) |
|-----------------------------|------------------------------|
| Deploy a basic agent setup that uses **Managed Identity** for authentication. <br> An account and project are created. <br> A GPT-4o model is deployed. <br> A Microsoft-managed Key Vault is used by default. <br> [![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure-ai-foundry%2Ffoundry-samples%2Frefs%2Fheads%2Fmain%2Fsamples%2Fmicrosoft%2Finfrastructure-setup%2F40-basic-agent-setup%2Fbasic-setup.json) | :::image type="content" source="./media/quickstart/basic-setup-resources-foundry.png" alt-text="An architecture diagram for basic agent setup." lightbox="./media/quickstart/basic-setup-resources-foundry.png"::: |
| Deploy a standard agent setup that uses **Managed Identity** for authentication. <br>An account and project are created. <br> A GPT-4o model is deployed. <br> Azure resources for storing customer data - **Azure Storage**, **Azure Cosmos DB**, and **Azure AI Search** - are automatically created if existing resources are't  provided. <br> These resources are connected to your project to store files, threads, and vector data. <br> A Microsoft-managed Key Vault is used by default.</li></ul> <br> [![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure-ai-foundry%2Ffoundry-samples%2Frefs%2Fheads%2Fmain%2Fsamples%2Fmicrosoft%2Finfrastructure-setup%2F41-standard-agent-setup%2Fazuredeploy.json) | :::image type="content" source="./media/quickstart/standard-agent-setup.png" alt-text="An architecture diagram for standard agent setup." lightbox="./media/quickstart/standard-agent-setup.png"::: |

### [Optional] Model selection in autodeploy template
You can customize the model used by your agent by editing the model parameters in the autodeploy template. To deploy a different model, you need to update at least the `modelName` and `modelVersion` parameters. 

By default, the deployment template is configured with the following values:

| Model Parameter  | Default Value  |
|------------------|----------------|
| modelName        | gpt-4o         |
| modelFormat      | OpenAI (for Azure OpenAI) |
| modelVersion     | 2024-11-20     |
| modelSkuName     | GlobalStandard |
| modelLocation    | eastus         |

> [!IMPORTANT]
> **Don't change the modelFormat parameter.** 
>
> The templates only support deployment of Azure OpenAI models. See which Azure OpenAI models are supported in the [Azure AI Foundry Agent Service model support](./concepts/model-region-support.md) documentation.


### What's next?
* [Create your first agent](./quickstart.md)
* Explore more:
    * [Use your existing resources](./how-to/use-your-own-resources.md)
    * [Network secured agent setup](./how-to/virtual-networks.md)