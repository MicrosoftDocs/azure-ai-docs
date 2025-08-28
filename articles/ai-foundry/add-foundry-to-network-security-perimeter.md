---
title: Add Azure AI Foundry to Network Security Perimeter (Preview)
description: Discover how to secure your Azure AI Foundry resource by joining it to a network security perimeter, ensuring enhanced data protection and controlled access.
author: jonburchel
ms.author: jburchel
ms.reviewer: meerakurup
ms.date: 08/28/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
ai.usage: ai-assisted
---

# Add an Azure AI Foundry to a network security perimeter (preview)

> [!NOTE]
> This feature is in preview.

## Overview

This article explains how to join an Azure AI Foundry resource to a network security perimeter to control network access to your Azure AI Foundry resource. By joining a network security perimeter, you can:

- Log all access to your account in context with other Azure resources
  in the same perimeter.

- Block any data exfiltration from the account to other services outside
  the perimeter.

- Allow access to your account using inbound and outbound access
  capabilities of the network security perimeter.

You can add an Azure AI Foundry resource to a network security perimeter in the Azure portal, as described in this article. Alternatively, you can use the Azure Virtual Network Manager REST API to join a service and use the Management REST APIs to view and synchronize the configuration settings.

## Limitations and considerations

- Azure AI Foundry customer-managed keys might not behave as expected. The Azure AI Foundry resources in the Azure subscription might not be able to use the fine-tune API or assistants API.

- Network security perimeter controls only data plane operations within Azure AI Foundry, not control plane operations. For example, users can deploy a model within their Azure OpenAI resource secured by the perimeter, but cannot use fine-tuned models, upload files, or start a session in the Chat Playground. In these data plane scenarios, an
  error message will show that access is blocked by the Network Security Perimeter, as expected.

- For an Azure AI Foundry service within a network security perimeter, the resource must use a system or user-assigned managed identity and have a role assignment that permits read-access to data sources.

- Consider securing with a network security perimeter when configuring Azure Blob Storage for Azure AI Foundry. Azure AI Foundry now supports using Azure Blob Storage for Azure AI Foundry Batch input and output files. Secure communications with Blob Storage and Azure OpenAI by placing both resources in the same perimeter. For more on the Azure OpenAI Batch and Blob Storage scenario, see Configuring Azure Blob Storage for Azure OpenAI.

- The Foundry Agent Service is designed to support various deployment scenarios for AI agents, with different levels of network security. In Basic and Basic key-based set-up, Network Security Perimeter (NSP) is supported. For Standard set-up, NSP is also applicable. However, in the more advanced scenario of Secured Standard Agents with network isolation, NSP is not required and not supported. This is because all necessary resources are expected to use Private Link to securely connect to the customer’s virtual network.

Scenarios to enable NSP

- Agent services
- Evaluations
-

## Prerequisites

> [!CAUTION]
> Make sure you fully understand the limitations and impact to your Azure Subscription listed in the previous section before registering the preview feature.

Register the network security perimeter feature from the Azure portal preview features. The feature names are the following:

- OpenAI.NspPreview

Or use the following CLI commands to register the two Preview features

- az feature registration create --name OpenAI.NspPreview --namespace
  Microsoft.CognitiveServices

Ensure the Microsoft.CognitiveServices and Microsoft.Network providers are registered. To check if the feature flags are allowlisted, use command az feature registration list.

## Assign an Azure AI Foundry account to a network security perimeter

Copy info here with updated screenshots: [Add an Azure OpenAI network security perimeter | Microsoft Learn](/azure/ai-foundry/openai/how-to/network-security-perimeter)

## Network security perimeter access modes

## Network security perimeter and Azure OpenAI service networking settings

## Change the network security perimeter access mode

## Enable logging network access

## Reading network access logs

## Add an access rule for your Azure OpenAI service

## Add an inbound access rule

## Add an outbound access rule

## Test your connection through network security perimeter

## View and manage network security perimeter configuration

## Related content
