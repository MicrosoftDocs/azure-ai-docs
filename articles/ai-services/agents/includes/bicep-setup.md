---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure
ms.topic: include
ms.date: 11/13/2024
---

## Set up your Azure AI Hub and Agent project

The following section will show you how to set up the required resources for getting started with Azure AI Agents Service: 

1. Creating an [Azure AI Hub](../../../ai-studio/quickstarts/get-started-playground.md) to set up your app environment and Azure resources.

1. Creating an Azure AI project under your Hub creates an endpoint for your app to call, and sets up app services to access to resources in your tenant.

1. Connecting an Azure OpenAI resource or an Azure AI resource


## Choose Basic or Standard Agent Setup
   
**Basic Setup**:  Agents use multitenant search and storage resources fully managed by Microsoft. You don't have visibility or control over these underlying Azure resources.

**Standard Setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you will incur costs based on your usage.

| Description   | Autodeploy |
| -----------------------------------------------| -----------------------|
| Deploy a basic agent setup that uses Managed Identity for authentication. | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fbasic-agent-identity%2Fazuredeploy.json)
| Deploy a standard agent setup that uses Managed Identity for authentication. | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Frefs%2Fheads%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fstandard-agent%2Fazuredeploy.json)

Resources for the AI hub, project, storage account, and AI Services that are needed to create agents will be created for you. The AI Services account will be connected to your project/hub and a gpt-4o-mini model will be deployed in the eastus region. A Microsoft-managed key vault will be used by default.
