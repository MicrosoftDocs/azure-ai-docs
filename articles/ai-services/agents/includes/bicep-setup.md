---
manager: nitinme
author: fosteramanda
ms.author: fosteramanda
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 11/13/2024
---

## Set up your Azure AI Foundry Agent Service project

The following section shows you how to set up the required resources for getting started with Azure AI Foundry Agent Service: 

1. Creating an [Azure AI project](../../../ai-foundry/quickstarts/get-started-playground.md) creates an endpoint for your app to call, and sets up app services to access to resources in your tenant.

1. Connecting an Azure OpenAI resource or an Azure AI Services resource


## Choose Basic or Standard Agent Setup
 
> [!TIP]
> We recommend reading the [Setup your environment](../how-to/environment-setup.md) article to learn more about the two different agent setups you can create. 

Creating your first agent with Azure AI Agent Service is a two-step process: 
1. Set up your agent environment.
1. Create and configure your agent using either the SDK of your choice or the Azure Foundry Portal. 

When you set up your agent enviornment, you can choose a basic setup or a standard setup.
  
**Basic Setup**:  Agents use multitenant search and storage resources fully managed by Microsoft. You don't have visibility or control over these underlying Azure resources.

**Standard Setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you incur costs based on your usage.

[!INCLUDE [ai-foundry-setup](portal-agent-limitation.md)]

| Description and Autodeploy  |  Diagram (click to zoom in) |
|-----------------------------|------------------------------|
| Deploy a basic agent setup that uses **Managed Identity** for authentication. <br> An account and project are created. <br> A GPT-4o model is deployed. <br> A Microsoft-managed Key Vault is used by default. <br> [![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure-ai-foundry%2Ffoundry-samples%2Frefs%2Fheads%2Fmain%2Fsamples%2Fmicrosoft%2Finfrastructure-setup%2F40-basic-agent-setup%2Fbasic-setup.json) | :::image type="content" source="../media/quickstart/basic-setup-resources-foundry.png" alt-text="An architecture diagram for basic agent setup." lightbox="../media/quickstart/basic-setup-resources-foundry.png"::: |
| Deploy a standard agent setup that uses **Managed Identity** for authentication. <br>An account and project are created. <br> A GPT-4o model is deployed. <br> Azure resources for storing customer data - **Azure Storage**, **Azure Cosmos DB**, and **Azure AI Search** - are automatically created if existing resources are't  provided. <br> These resources are connected to your project to store files, threads, and vector data. <br> A Microsoft-managed Key Vault is used by default.</li></ul> <br> [![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure-ai-foundry%2Ffoundry-samples%2Frefs%2Fheads%2Fmain%2Fsamples%2Fmicrosoft%2Finfrastructure-setup%2F41-standard-agent-setup%2Fazuredeploy.json) | :::image type="content" source="../media/quickstart/standard-agent-setup.png" alt-text="An architecture diagram for standard agent setup." lightbox="../media/quickstart/standard-agent-setup.png"::: |

You will need to assign the **Azure AI User**  [RBAC role](../../../ai-foundry/concepts/rbac-azure-ai-foundry.md) to each team member who needs to create or edit agents using the SDK or Agent Playground.
* This role must be assigned at the project scope
* Minimum required permissions: `agents/*/read`, `agents/*/action`, `agents/*/delete`