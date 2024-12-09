---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure
ms.topic: include
ms.date: 11/13/2024
---

## Set up your Azure AI Hub and Agent project

The following section shows you how to set up the required resources for getting started with Azure AI Agents Service: 

1. Creating an [Azure AI Hub](../../../ai-studio/quickstarts/get-started-playground.md) to set up your app environment and Azure resources.

1. Creating an Azure AI project under your Hub creates an endpoint for your app to call, and sets up app services to access to resources in your tenant.

1. Connecting an Azure OpenAI resource or an Azure AI resource


## Choose Basic or Standard Agent Setup
   
**Basic Setup**:  Agents use multitenant search and storage resources fully managed by Microsoft. You don't have visibility or control over these underlying Azure resources.

**Standard Setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you incur costs based on your usage.

| Description   | Autodeploy |
| -----------------------------------------------| -----------------------|
| Deploy a basic agent setup that uses Managed Identity for authentication. | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fbasic-agent-identity%2Fazuredeploy.json)
| Deploy a standard agent setup that uses Managed Identity for authentication. | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Frefs%2Fheads%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fstandard-agent%2Fazuredeploy.json)

## Basic agent setup resource architecture
:::image type="content" source="../media/quickstart/basic-agent-setup-resources.png" alt-text="An architecture diagram for basic agent setup." lightbox="../media/quickstart/basic-agent-setup-resources.png":::

Resources for the AI hub, AI project, storage account, and AI Services are created for you. The AI Services account is connected to your project/hub and a gpt-4o-mini model is deployed in the eastus region. A Microsoft-managed key vault is used by default.

## Standard agent setup resource architecture
:::image type="content" source="../media/quickstart/standard-agent-setup-resources.png" alt-text="An architecture diagram for standard agent setup." lightbox="../media/quickstart/standard-agent-setup-resources.png":::

Resources for the AI hub, AI project, key vault, storage account, AI Services, and AI Search are created for you. The AI Services, AI Search, key vault, and storage account are connected to your project and hub. A gpt-4o-mini model is deployed in eastus region using the AI Services resource OpenAI endpoint.