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
> Users who previously managed their model deployments and ran evaluations by using `oai.azure.com`, and then onboarded to the Microsoft Foundry developer platform, have these limitations when they use `ai.azure.com`:
>
> - These users can't view their evaluations that were created through the Azure OpenAI API. To view these evaluations, they have to go back to `oai.azure.com`.
> - These users can't use the Azure OpenAI API to run evaluations within Foundry. Instead, they should continue to use `oai.azure.com` for this task. However, they can use the Azure OpenAI evaluators that are available directly in Foundry (`ai.azure.com`) in the option for dataset evaluation creation. The option for fine-tuned model evaluation isn't supported if the deployment is a migration from Azure OpenAI to Foundry.
>
> For the scenario of dataset upload and bring your own storage, there are a few configuration requirements:
>
> - Account authentication must be Microsoft Entra ID.
> - The storage must be added to the account. Adding it to the project causes service errors.
> - Users must add their project to their storage account through access control in the Azure portal.
>
> To learn more about creating evaluations with OpenAI evaluation graders in the Azure OpenAI hub, see [How to use Azure OpenAI in Foundry models evaluation](../../ai-services/openai/how-to/evaluations.md).

