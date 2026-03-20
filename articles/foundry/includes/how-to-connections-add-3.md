---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: meerakurup
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## [Bicep](#tab/bicep)

Use [Connection templates](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/01-connections) to create connections through infrastructure deployment.

After deployment, return to your project and verify that the new connection appears in connected resources.

---

## Network isolation

For end-to-end [network isolation](../how-to/configure-private-link.md) with Foundry, you need private endpoints to connect to your connected resource. For example, if your Azure Storage account is set to public network access as __Disabled__, then a private endpoint should be deployed in your virtual network to access in Foundry. 

For more on how to set private endpoints to your connected resources, see the following documentation:
    
|Private resource|Documentation|
|---|---|
|Azure Storage|[Use private endpoints](/azure/storage/common/storage-private-endpoints)|
|Azure Cosmos DB|[Configure Azure Private Link for Azure Cosmos DB](/azure/cosmos-db/how-to-configure-private-endpoints?tabs=arm-bicep)|
|Azure AI Search|[Create a private endpoint for a secure connection](/azure/search/service-create-private-endpoint)|
|Azure OpenAI|[Securing Azure OpenAI inside a virtual network with private endpoints](/azure/ai-foundry/openai/how-to/network)|
|Application Insights|[Use Azure Private Link to connect networks to Azure Monitor](/azure/azure-monitor/logs/private-link-security)|

> [!NOTE]
> Cross-subscription connections used for model deployment are not supported (Foundry, Azure OpenAI). You can't connect to resources from different subscriptions for model deployments.
