---
title: 'How to use a virtual network with the Azure AI Foundry Agent Service'
titleSuffix: Azure AI Foundry
description: Learn how to use your own virtual network with the Azure AI Foundry Agent Service. 
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 05/12/2025
author: aahill
ms.author: aahi
ms.reviewer: fosteramanda
ms.custom: azure-ai-agents
---

# Create a new network-secured environment with user-managed identity

Azure AI Foundry Agent Service offers **Standard Setup with private networking** environment setup, allowing you to bring your own (BYO) private virtual network. This set up creates an isolated network environment that lets you securely access data and perform actions while maintaining full control over your network infrastructure. This guide provides a step-by-step walkthrough of the setup process and outlines all necessary requirements.

## Security features

By default, the Standard Setup with Private Network Isolation ensures:
- **No public egress**: foundational infrastructure ensures the right authentication and security for your agents and tools, without you having to do trusted service bypass.

- **Container injection**: allows the platform network to host APIs and inject a subnet into your network, enabling local communication of your Azure resources within the same virtual network.

- **Private resource access**: If your resources are marked as private and nondiscoverable from the internet, the platform network can still access them, provided the necessary credentials and authorization are in place.

For customers without an existing virtual network, the Standard Setup with Private Networking template simplifies deployment by automatically provisioning the necessary network infrastructures. 

## Architecture diagram

:::image type="content" source="../media/private-network-isolation.png" alt-text="A diagram showing virtual network architecture.":::
### Known limitations

- Subnet IP address limitation: only class B and C are supported
- Azure Blob Storage: Using Azure Blob Storage files with the File Search tool isn't supported.

## Prerequisites
* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).
* Ensure that the individual creating the account and project has the **Azure AI Account Owner** role at the subscription scope
* The person deploying the template must also have permissions to assign roles to required resources (Cosmos DB, Search, Storage).
    * The built-in role needed is **Role Based Access Administrator**.
    * Alternatively, having the **Owner** role at the subscription level also satisfies this requirement.
    * The key permission needed is: `Microsoft.Authorization/roleAssignments/write`
* [Python 3.8 or later](https://www.python.org/)
* Once the agent environment is configured, ensure that each team member who wants to use the Agent Playground or SDK to create or edit agents has been assigned the built-in **Azure AI User** [RBAC role](../../../ai-foundry/concepts/rbac-azure-ai-foundry.md) for the project.
    * The minimum set of permissions required is: **agents/*/read**, **agents/*/action**, **agents/*/delete**  
* Register providers. The following providers must be registered:
    * `Microsoft.KeyVault`
    * `Microsoft.CognitiveServices`
    * `Microsoft.Storage`
    * `Microsoft.MachineLearningServices`
    * `Microsoft.Search`
    * `Microsoft.Network`
    * `Microsoft.App`
    * To use Bing Search tool: `Microsoft.Bing`

    ```console
       az provider register --namespace 'Microsoft.KeyVault'
       az provider register --namespace 'Microsoft.CognitiveServices'
       az provider register --namespace 'Microsoft.Storage'
       az provider register --namespace 'Microsoft.MachineLearningServices'
       az provider register --namespace 'Microsoft.Search'
       # only to use Grounding with Bing Search tool
       az provider register --namespace 'Microsoft.Bing'
    ```

## Configure a new network-secured environment 

**Network secured setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you incur costs based on your usage. The following bicep template provides:

* An account and project are created. 
* A gpt-4o model is deployed. 
* Azure resources for storing customer data — Azure Storage, Azure Cosmos DB, and Azure AI Search — are automatically created if existing resources are not provided. 
* These resources are connected to your project to store files, threads, and vector data. 
* A Microsoft-managed key vault is used by default. 


### Manually deploy the bicep template

> [!NOTE]
> Using the Bicep template is the only way to deploy a network secured environment for Azure AI Foundry Agent Service.

1. To deploy and customize the bicep templates, [download the template from GitHub](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/15-private-network-standard-agent-setup). Download the following from the `private-network-standard-agent-setup` folder:
    1. `main.bicep`
    1. `azuredeploy.parameters.json`
    1. `modules-network-secured folder`
1. To authenticate to your Azure subscription from the Azure CLI, use the following command: 

    ```console
    az login
    ```

1. Create a resource group:

    ```console
    az group create --name {my_resource_group} --location eastus
    ```

    Make sure you have the Azure AI Developer role for the resource group you created. 

1. Using the resource group you created in the previous step and one of the template files (`private-network-standard-agent-setup`), run one of the following commands: 

    1. To use default resource names, run:

        ```console
        az deployment group create --resource-group {my_resource_group} --template-file main.bicep
        ```
For more details, see the [README](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/15-private-network-standard-agent-setup).

## Deep Dive Standard Setup with Private Networking Template
When you use the Standard Setup with Private Networking Agent Template, the following will automatically be provisioned, unless you bring your own: 

**Network Infrastructure**
* A Virtual Network (192.168.0.0/16) is created 
* Agent Subnet (192.168.0.0/24): Hosts Agent client 
* Private endpoint Subnet (192.168.1.0/24): Hosts private endpoints

**Private DNS Zones** 
The following DNS zones are configured: 
* privatelink.blob.core.windows.net 
* privatelink.cognitiveservices.azure.com 
* privatelink.documents.azure.com 
* privatelink.file.core.windows.net 
* privatelink.openai.azure.com 
* privatelink.search.windows.net 
* privatelink.services.ai.azure.com  

### Virtual network (Vnet) capabilities
Virtual networks enable you to specify which endpoints can make API calls to your resources. The Azure service automatically rejects API calls from devices outside your defined network. You can establish allowed networks using either formula-based definitions or by creating an exhaustive list of permitted endpoints. This security layer can be combined with other security measures for enhanced protection.


### Network rules

All accounts and their corresponding projects are protected by default with **deny-by-default network rules**, requiring explicit configuration to allow access through private endpoints.

These rules apply to **all protocols**, including REST and WebSocket. Even internal testing tools like Azure portal's test consoles require explicit permission to access your account and its child resources—ensuring complete security across all agent projects.


### Private endpoints

For Agents, private endpoints ensure secure, internal-only connectivity for the following Azure resources:

- Azure AI Foundry
- Azure AI Search
- Azure Storage
- Azure Cosmos DB


### DNS zone configurations summary

| Private Link Resource Type | Sub Resource | Private DNS Zone Name | Public DNS Zone Forwarders |
|----------------------------|--------------|------------------------|-----------------------------|
| **Azure AI Foundry**       | account      | `privatelink.cognitiveservices.azure.com`<br>`privatelink.openai.azure.com`<br>`privatelink.services.ai.azure.com` | `cognitiveservices.azure.com`<br>`openai.azure.com`<br>`services.ai.azure.com` |
| **Azure AI Search**        | searchService| `privatelink.search.windows.net` | `search.windows.net` |
| **Azure Cosmos DB**        | Sql          | `privatelink.documents.azure.com` | `documents.azure.com` |
| **Azure Storage**          | blob         | `privatelink.blob.core.windows.net` | `blob.core.windows.net` |



### Access your secured agents

Once your template deployment is complete, you can access your Foundry project behind a virtual network using one of the following methods:
* **Azure VPN Gateway**: Connects on-premises networks to the virtual network over a private connection. Connection is made over the public internet. There are two types of VPN gateways that you might use: 
    * **Point-to-site**: Each client computer uses a VPN client to connect to the virtual network. 
    * **Site-to-site**: A VPN device connects the virtual network to your on-premises network. 
* **ExpressRoute**: Connects on-premises networks into the cloud over a private connection. Connection is made using a connectivity provider.
* **Azure Bastion**: In this scenario, you create an Azure Virtual Machine (sometimes called a jump box) inside the virtual network. You then connect to the VM using Azure Bastion. Bastion allows you to connect to the VM using either an RDP or SSH session from your local web browser. You then use the jump box as your development environment. Since it is inside the virtual network, it can directly access the workspace.


## Summary

**Private Networking for Standard Agent Setup** delivers enterprise-grade isolation and control:
- ✅ All inbound and outbound traffic remains isolation from public internet 
- ✅ Dedicated private endpoints secure all your customer data  
- ✅ Automatic private DNS resolution for seamless internal access 
- ✅ Strict deny-by-default network rules for maximum security 

This setup enables AI agents to operate entirely within a dedicated, isolated virtual network. By leveraging private network isolation (BYO VNet), organizations can enforce custom security policies, ensuring that AI agents operate within their trusted infrastructure.    

Our goal is to accelerate the development and deployment of AI agents without compromising critical security requirements. With our bicep and ARM templates, you can quickly set up your agent environment while still maintaining full control over their networking and data.   


## What's next?
You’ve now successfully configured a Network Secure Account and project, use the [quickstart](../quickstart.md) to create your first agent. 
