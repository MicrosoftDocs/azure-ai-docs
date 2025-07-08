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
> See the following information about backward compatibility for Azure OpenAI users who onboarded to the Azure AI Foundry developer platform:
>
> Users who previously managed their model deployments and ran evaluations by using `oai.azure.com` and have since onboarded to the Azure AI Foundry developer platform have a few limitations when using `ai.azure.com`:
>
> - Users are unable to view their evaluations that were created by using the Azure OpenAI API. To view these evaluations, users have to navigate back to `oai.azure.com`.
> - Users are unable to use the Azure OpenAI API to run evaluations within Azure AI Foundry. Instead, these users should continue to use `oai.azure.com` for this task. However, users can use the Azure OpenAI evaluators that are available directly in Azure AI Foundry (`ai.azure.com`) in the dataset evaluation creation option. The fine-tuned model evaluation option isn't supported if the deployment is a migration from Azure OpenAI to Azure AI Foundry.
>
> For the dataset upload and bring your own storage scenario, there are a few configuration requirements:
>
> - Account authentication must be Microsoft Entra ID.
> - The storage must be added to the account, because if it's added to the project, you get service errors.
> - The user must add their project to their storage account through access control in the Azure portal.
>
> To learn more about creating evaluations with OpenAI evaluation graders in the Azure OpenAI hub, see [How to use Azure OpenAI in Azure AI Foundry models evaluation](../../ai-services/openai/how-to/evaluations.md).
