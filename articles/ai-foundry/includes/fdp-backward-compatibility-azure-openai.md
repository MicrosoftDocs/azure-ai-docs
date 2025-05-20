---
title: Include file
description: Include file
author: lgayhardt
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 5/08/2025
ms.author: lagayhar
ms.custom: include file

---

> [!CAUTION]
> Backward compatibility for Azure OpenAI users who onboarded to Foundry Developer Platform:
>
> Users who previously used oai.azure.com to manage their model deployments and run evaluations and have since onboarded to Foundry Developer Platform (FDP) will have a few limitations when using ai.azure.com:
>
> - First, users will be unable to view their evaluations that were created using the Azure OpenAI API. Instead, to view these, users have to navigate back to oai.azure.com.
> - Second, users will be unable to use the Azure OpenAI API to run evaluations within AI Foundry. Instead, these users should continue to use oai.azure.com for this. However, users can use the Azure OpenAI evaluators that are available directly in AI Foundry (ai.azure.com) in the dataset evaluation creation option. The Fine-tuned  model evaluation option isn't supported if the deployment is a migration from Azure OpenAI to Azure Foundry.
> - For the dataset upload + bring your own storage scenario, a few configurations requirements need to happen:
>
>   - Account authentication needs to be Entra ID.
>   - The storage needs to be added to the account (if it’s added to the project, you'll get service errors).
>   - User needs to add their project to their storage account through access control in the Azure portal.
>
> To learn more about creating evaluations specifically with OpenAI evaluation graders in Azure OpenAI Hub, see [How to use Azure OpenAI in Azure AI Foundry Models evaluation](../../ai-services/openai/how-to/evaluations.md)
