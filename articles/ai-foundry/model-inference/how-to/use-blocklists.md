---
title: 'How to use blocklists with Azure AI Foundry Models in Azure AI Foundry Service'
titleSuffix: Azure AI Foundry
description: Learn how to use blocklists with Foundry Models in Azure AI Foundry Service.
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 1/21/2025
author: santiagxf
ms.author: fasantia
ms.custom: ignite-2024, github-universe-2024
---

# How to use blocklists with Foundry Models in Azure AI Foundry services

The configurable content filters are sufficient for most content moderation needs. However, you may need to filter terms specific to your use case. 

## Prerequisites

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Foundry Models](quickstart-github-models.md) if it's your case.

* An Azure AI Foundry services resource. For more information, see [Create an Azure AI Foundry Services resource](../../../ai-services/multi-service-resource.md?context=/azure/ai-services/model-inference/context/context).

* An Azure AI Foundry project [connected to your Azure AI Foundry services resource](configure-project-connection.md).

* A model deployment. See [Add and configure models to Azure AI Foundry services](create-model-deployments.md) for adding models to your resource.

    > [!NOTE]
    > Blocklist (preview) is only supported for Azure OpenAI models.

[!INCLUDE [use-blocklists](../../includes/use-blocklists.md)]

## Next steps

* [Configure content filtering](configure-content-filters.md)
