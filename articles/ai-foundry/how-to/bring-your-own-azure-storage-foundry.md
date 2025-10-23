---
title: Connect Azure Storage accounts to AI Foundry
titleSuffix: Azure AI Foundry
ms.reviewer: andyaviles
description: Learn how to bring your own Azure Storage account to Azure AI Foundry for agents, evaluations, datasets, and other capabilities.
#customer intent: As a developer, I want to set up capability hosts for agents so that I can use my own Azure Storage account instead of Microsoft-managed storage.
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.custom: ignite-2024, build-2025
ms.topic: how-to-guide
ms.date: 01/23/2025
ai-usage: ai-assisted
---

# Connect Azure Storage accounts to AI Foundry

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Azure AI Foundry supports connecting your own Azure Storage accounts for various features and capabilities. You can manage storage connections at both the resource level and project level, giving you flexibility in how you organize and secure your data.

This article shows you how to connect your Azure Storage accounts to AI Foundry by using three different approaches depending on which features you plan to use. Each approach serves specific capabilities and has different configuration requirements.

## Prerequisites

Before connecting your Azure Storage account, ensure you have:

- An Azure subscription with an active AI Foundry resource
- An Azure Storage account in the same subscription
- Contributor or Owner permissions on both the AI Foundry resource and Storage account
- Understanding of your feature requirements (agents, evaluations, datasets, speech, or language)

## Understand storage connection approaches

Azure AI Foundry provides three methods to connect Azure Storage accounts, each serving different features:

| **Approach** | **Features Supported** | **Scope** |
|-------------|------------------------|-----------|
| Foundry connections | Agents, Evaluations, Datasets, Content Understanding | Resource or project level |
| Capability hosts | Agents standard setup | Resource and project level |
| userOwnedStorage field | Speech, Language | Resource level only |

### Foundry connections

Foundry connections are sub-resources that store the external service's endpoint and authentication details. Users with permissions on the AI Foundry project automatically have access to connected resources without needing separate permissions on the storage account. This approach works best for most scenarios.

### Capability hosts

Capability hosts bind specific features to designated connections when multiple storage connections exist. They define which storage connection a particular feature uses. Use capability hosts most commonly for agents standard setup. If you don't create capability hosts for agents, AI Foundry uses Microsoft-managed storage for that feature.

### userOwnedStorage field

The userOwnedStorage field enables customer-managed storage for Speech and Language capabilities. Set this field during resource creation at the resource level, so all projects within the resource share the same storage account for these capabilities.

## Create a Foundry storage connection

::: moniker range="azure-ai-foundry-classic"

Create a storage connection to enable agents, evaluations, datasets, and content understanding features with your own storage account.

1. Sign in to [Azure AI Foundry](https://ai.azure.com).

1. Go to your AI Foundry resource or project where you want to add the connection.

1. In the left navigation, select **Connected resources** or **Connections**.

1. Select **+ New connection**.

1. In the connection type list, select **Azure Blob Storage**.

1. Enter the following information:

   - **Name**: Enter a descriptive name for your connection
   - **Subscription**: Select your Azure subscription
   - **Storage account**: Select your Azure Storage account
   - **Authentication**: Choose your preferred authentication method (system-assigned managed identity recommended)

1. Select **Create** to establish the connection.

The storage connection is now available for use with evaluations, datasets, and content understanding features.

::: moniker-end

::: moniker range="azure-ai-foundry"

Create a storage connection to enable agents, evaluations, datasets, and content understanding features with your own storage account by using Azure CLI, Azure PowerShell, or Azure REST API.

Use the Azure AI Foundry REST API or Azure CLI to create a storage connection at the resource or project level. Reference your Azure Storage account and specify your preferred authentication method (system-assigned managed identity recommended).

The storage connection is now available for use with evaluations, datasets, and content understanding features.

::: moniker-end

## Configure capability hosts for agents

Set up capability hosts to use your storage connection for agents standard setup. You need to configure capability hosts at both the resource and project levels.

### Create resource-level capability host

1. Use the Azure CLI or Azure REST API to create a resource-level capability host.

1. Reference your previously created storage connection in the capability host configuration.

1. Set the capability type to support agents.

### Create project-level capability host

After creating your AI Foundry project:

1. Create a project-level capability host that references the resource-level capability host.

1. Configure the capability host to enable agents functionality.

1. Verify the capability host is properly linked to your storage connection.

Your agents standard setup now uses your own Azure Storage account instead of Microsoft-managed storage.

## Set userOwnedStorage for Speech and Language

Set the userOwnedStorage field during resource creation to use your storage account for Speech and Language capabilities.

> [!IMPORTANT]
> Set the userOwnedStorage field during resource creation. It applies to all projects within the resource. This setting has specific restrictions and can't be changed after resource creation.

1. Create your AI Foundry resource with Azure CLI, Azure PowerShell, or Azure Resource Manager templates.

1. In the resource properties, add the userOwnedStorage field with your storage account details.

1. Finish the resource creation process.

All Speech and Language capabilities in the resource now use your specified storage account.

## Configure content understanding

::: moniker range="azure-ai-foundry-classic"

Connect your storage account to content understanding features through the AI Foundry portal.

1. Sign in to [Azure AI Foundry](https://ai.azure.com).

1. Go to your AI Foundry resource.

1. In the left navigation, select **Content Understanding**.

1. Select your existing resource-level storage connection from the available options.

Content understanding now uses your connected storage account for processing and storing data.

::: moniker-end

::: moniker range="azure-ai-foundry"

Connect your storage account to content understanding features by using Azure CLI, Azure PowerShell, or Azure REST API.

Configure your AI Foundry resource to use your existing resource-level storage connection for content understanding capabilities.

Content understanding now uses your connected storage account for processing and storing data.

::: moniker-end

## Set up complete customer-managed storage

For enterprise scenarios that require customer-managed storage for all features, configure all three approaches together.

Follow these steps in order to ensure proper configuration:

1. Create your AI Foundry resource with the `userOwnedStorage` field in the resource properties.

1. Create a resource-level capability host for agents.

1. Create your AI Foundry project.

1. Create a project-level capability host for agents.

1. Create a resource-level Azure Storage account connection through Foundry connections.

::: moniker range="azure-ai-foundry-classic"

1. Navigate to the AI Foundry portal and configure content understanding to use your storage connection.

::: moniker-end

::: moniker range="azure-ai-foundry"

1. Configure content understanding to use your storage connection by using Azure CLI, Azure PowerShell, or Azure REST API.

::: moniker-end

After completing these steps, all AI Foundry features use your customer-managed Azure Storage account instead of Microsoft-managed storage.

## Related content

- [Learn about capability hosts for agents](../agents/concepts/capability-hosts.md).
- [Understand agents standard setup](../agents/concepts/standard-agent-setup.md).
- [Add connections to your project](connections-add.md).
- [Explore AI Foundry REST API](/rest/api/aifoundry/aiprojects/datasets?view=rest-aifoundry-aiprojects-v1).
- [Connect Azure Storage accounts for Speech and Language resources](../../ai-services/speech-service/bring-your-own-storage-speech-resource.md?tabs=portal).
