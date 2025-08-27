---
title: Deploy a custom question and answering agent
titleSuffix: Azure AI services
description:  Deploy an Custom Question Answering (CQA) in Azure AI Foundry
#services: cognitive-services
manager: nitinme
author: laujan
ms.author: lajanuar
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 08/26/2025
ms.custom: language-service-question-answering
---

# Deploy a custom question and answering agent

Azure AI Foundry offers a unified platform for building, managing, and deploying AI solutions with a wide array of models and tools. Azure AI Foundry playgrounds are interactive environments within the Azure AI Foundry portal designed for exploring, testing, and prototyping with various AI models and tools.

In this article, we show you how to Deploy your custom question and answering agent in the Azure AI Foudry

> [!NOTE]
>
> * If you already have an Azure AI Language or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Azure AI Foundry portal. 
> * For more information, see [How to use Azure AI services in the Azure AI Foundry portal](/azure/ai-services/connect-services-ai-foundry-portal).
> * We highly recommended that you use an Azure AI Foundry resource in the AI Foundry; however, you can also follow these instructions using a Language resource.

## Prerequisites

* **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/free/cognitive-services).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](/azure/ai-foundry/openai/how-to/role-based-access-control#cognitive-services-contributor).
*  [Azure AI Foundry multi-service resource](/azure/ai-services/multi-service-resource). For more information, *see* [Configure an Azure AI Foundry resource](../../how-to/configure-azure-resources.md#option-1-configure-an-azure-ai-foundry-resource). Alternately, you can use an [Azure AI Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
* Foundry project created in the Azure AI Foundry. For more information, *see* [Create an AI Foundry project](/azure/ai-foundry/how-to/create-projects).
* At least one deployed CQA knowledge base.