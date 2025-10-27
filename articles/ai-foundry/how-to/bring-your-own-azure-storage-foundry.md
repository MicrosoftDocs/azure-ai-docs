---
title: Connect to your own storage
titleSuffix: Azure AI Foundry
ms.reviewer: andyaviles
description: Learn how to bring your own storage to Azure AI Foundry for agents, evaluations, datasets, and other capabilities.
#customer intent: As a developer, I want to set up capability hosts for agents so that I can use my own storage instead of Microsoft-managed storage.
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.custom: ignite-2024, build-2025
ms.topic: how-to
ms.date: 10/24/2025
ai-usage: ai-assisted
---

# Connect to your own storage

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Azure AI Foundry supports connecting your own storage for various features and capabilities. You can manage storage connections at both the resource level and project level, giving you flexibility in how you organize and secure your data.

This article shows you how to connect your storage to AI Foundry by using three different approaches depending on which features you plan to use. Each approach serves specific capabilities and has different configuration requirements.

## Prerequisites

Before connecting your storage, ensure you have:

- An Azure subscription with an active AI Foundry resource
- A storage account in the same subscription
- Contributor or Owner permissions on both the AI Foundry resource and storage account
- Understanding of your feature requirements (agents, evaluations, datasets, speech, or language)

## Understand storage connection approaches

Azure AI Foundry provides three methods to connect to storage, each serving different features:

| **Approach** | **Features Supported** | **Scope** |
|-------------|------------------------|-----------|
| Foundry connections (shared data pointer) | Agents, Evaluations, Datasets, Content Understanding | Resource or project level |
| Capability hosts (feature override binding) | Agents standard setup (explicit assignment) | Resource and project level |
| userOwnedStorage field (resource storage binding) | Speech, Language | Resource level only |

### Foundry connections

Foundry connections act as shared data pointers across AI Foundry capabilities (agents, evaluations, datasets, content understanding). Each connection wraps the target storage endpoint plus authentication so users with project access can use the data without direct storage account permissions. Use connections as the default pattern; create a capability host only when you need to explicitly bind (override) a single feature to one connection among several.

### Capability hosts

[Capability hosts](/azure/ai-foundry/agents/concepts/capability-hosts) bind specific features to designated connections when multiple storage connections exist. They define which storage connection a particular feature uses. Use capability hosts most commonly for agents standard setup. If you don't create capability hosts for agents, AI Foundry uses Microsoft-managed storage for that feature.

### userOwnedStorage field

The userOwnedStorage field enables customer-managed storage for Speech and Language capabilities. Set this field during resource creation at the resource level, so all projects within the resource share the same storage account for these capabilities with backwards compatibility to the approach used for Azure Speech and Azure Language resource types.

## Create a Foundry storage connection

Create a storage connection to enable agents, evaluations, datasets, and content understanding features with your own storage account.

1. Sign in to [Azure AI Foundry](https://ai.azure.com).

1. Go to your AI Foundry resource or project where you want to add the connection.

1. In the left navigation, select **Connected resources** or **Connections**.

1. Select **+ New connection**.

1. In the connection type list, select **Azure Blob Storage**.

1. Enter the following information:

   - **Name**: Enter a descriptive name for your connection
   - **Subscription**: Select your Azure subscription
   - **Storage account**: Select your storage account
   - **Authentication**: Choose your preferred authentication method (system-assigned managed identity recommended)

1. Select **Create** to establish the connection.

The storage connection is now available for use with evaluations, datasets, and content understanding features.

## Configure capability hosts for agents

Set up [capability hosts](/azure/ai-foundry/agents/concepts/capability-hosts) to use your storage connection for agents standard setup. You need to configure capability hosts at both the resource and project levels.

### Create resource-level capability host

1. Use the [Azure CLI](/azure/ml/capability-host) or [Azure REST API](/rest/api/azureml/capability-hosts/create-or-update) to create a resource-level capability host.

1. Reference your previously created storage connection in the capability host configuration.

1. Set the capability type to support agents.

### Create project-level capability host

After creating your AI Foundry project:

1. Create a project-level capability host that references the resource-level capability host.

1. Configure the capability host to enable agents functionality.

1. Verify the capability host is properly linked to your storage connection as demonstrated in this [code sample for Standard agent setup](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup#41-standard-agent-setup).

Your agents standard setup now uses your own storage account instead of Microsoft-managed storage.

## Set userOwnedStorage for Speech and Language

Set the userOwnedStorage field during resource creation to use your storage account for Speech and Language capabilities.

> [!IMPORTANT]
> Set the userOwnedStorage field during resource creation. It applies to all projects within the resource. This setting has specific restrictions and can't be changed after resource creation.

1. Create your AI Foundry resource with Azure CLI, Azure PowerShell, or Azure Resource Manager templates.

1. In the resource properties, add the userOwnedStorage field with your storage account details.

1. Finish the resource creation process.

All Speech and Language capabilities in the resource now use your specified storage account.

## Configure content understanding

Connect your storage account to content understanding features through the AI Foundry portal.

1. Sign in to [Azure AI Foundry](https://ai.azure.com).

1. Go to your AI Foundry resource.

1. In the left navigation, select **Content Understanding**.

1. Select your existing resource-level storage connection from the available options.

Content understanding now uses your connected storage account for processing and storing data.

## Set up complete customer-managed storage

For enterprise scenarios that require customer-managed storage for all features, configure all three approaches together.

Follow these steps in order to ensure proper configuration:

1. Create your AI Foundry resource with the `userOwnedStorage` field in the resource properties.

1. Create a resource-level capability host for agents.

1. Create your AI Foundry project.

1. Create a project-level capability host for agents.

1. Create a resource-level storage account connection through Foundry connections.

1. Navigate to the AI Foundry portal and configure content understanding to use your storage connection.

After completing these steps, all AI Foundry features use your customer-managed storage account instead of Microsoft-managed storage.

## Related content

- [Learn about capability hosts for agents](../agents/concepts/capability-hosts.md).
- [Understand agents standard setup](../agents/concepts/standard-agent-setup.md).
- [Add connections to your project](connections-add.md).
- [Explore AI Foundry REST API](/rest/api/aifoundry/aiprojects/datasets).
- [Connect your own storage to Speech/Language](../../ai-services/speech-service/bring-your-own-storage-speech-resource.md?tabs=portal).
