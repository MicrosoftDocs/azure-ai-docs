---
title: Fine-Tuning Inactivity Guidance
titleSuffix: Azure OpenAI
description: Describes the fine-tuning guidance for a model deployment that's inactive for more than 15 days.
author: mrbullwinkle 
ms.author: mbullwin 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 03/26/2025
manager: nitinme
keywords: ChatGPT

---

> [!IMPORTANT]
> After you deploy a customized model, if at any time the deployment remains inactive for more than 15 days, the deployment is deleted. The deployment of a customized model is _inactive_ if the model was deployed more than 15 days ago and no chat completions or response API calls were made to it during a continuous 15-day period.
>
> The deletion of an inactive deployment doesn't delete or affect the underlying customized model. The customized model can be redeployed at any time.
>
> As described in [Azure OpenAI in Microsoft Foundry Models pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/), each customized (fine-tuned) model that's deployed incurs an hourly hosting cost regardless of whether chat completions or response API calls are made to the model. To learn more about planning and managing costs with Azure OpenAI, see [Plan and manage costs for Azure OpenAI](../../concepts/manage-costs.md#fine-tuned-models).
