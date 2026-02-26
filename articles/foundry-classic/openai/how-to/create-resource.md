---
title: 'How-to: Create and deploy an Azure OpenAI in Microsoft Foundry Models resource'
titleSuffix: Azure OpenAI
description: Learn how to get started with Azure OpenAI and create your first resource and deploy your first model in the Azure CLI or the Azure portal.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: devx-track-azurecli, build-2023, build-2023-dataai, devx-track-azurepowershell, innovation-engine
ms.topic: how-to
ms.date: 11/26/2025
zone_pivot_groups: openai-create-resource
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---

# Create and deploy an Azure OpenAI in Microsoft Foundry Models resource

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://go.microsoft.com/fwlink/?linkid=2303211)

This article describes how to get started with Azure OpenAI and provides step-by-step instructions to create a resource and deploy a model. You can create resources in Azure in several different ways:

- The [Azure portal](https://portal.azure.com/?microsoft_azure_marketplace_ItemHideKey=microsoft_openai_tip#create/Microsoft.CognitiveServicesOpenAI)
- The REST APIs, the Azure CLI, PowerShell, or client libraries
- Azure Resource Manager (ARM) templates

In this article, you review examples for creating and deploying resources in the Azure portal, with the Azure CLI, and with PowerShell.

::: zone pivot="web-portal"

[!INCLUDE [Azure portal resource](../includes/create-resource-portal.md)]

::: zone-end

::: zone pivot="cli"

[!INCLUDE [Azure CLI resource](../includes/create-resource-cli.md)]

::: zone-end

::: zone pivot="ps"

[!INCLUDE [Azure PowerShell resource](../includes/create-resource-powershell.md)]

::: zone-end

## Next steps

- [Get started with the Azure OpenAI security building block](/azure/developer/ai/get-started-securing-your-ai-app?tabs=github-codespaces&pivots=python)
- Learn more about the [Azure OpenAI models](../../foundry-models/concepts/models-sold-directly-by-azure.md).
- For information on pricing visit the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
