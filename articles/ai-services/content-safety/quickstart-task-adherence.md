---
title: Quickstart - Use Task Adherence for your Agent Workflows
description: Learn how to use the Task Adherence API in Azure AI Content Safety to ensure agent tool actions align with user instructions and intent.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-content-safety
ms.topic: quickstart
ms.date: 08/05/2025
manager: nitinme
zone_pivot_groups: programming-languages-content-safety-foundry-rest
---

# QuickStart: Use Task Adherence for your Agent Workflows

In this quickstart, you use the Task Adherence feature. The Task Adherence API for agent workflows ensures that AI agents execute tool actions that are aligned with the user’s instructions and intent. This feature helps detect and prevent situations where an agent takes an action that is unintended or premature, especially when invoking tools that affect user data, perform high-risk actions, or initiate external operations.

Task Adherence is useful in systems where agents have the ability to plan and act autonomously. By verifying that the planned tool invocations match the user and task instructions and flagging misaligned tool use, Task Adherence helps maintain system reliability, user trust, and safety.

For more information on how Task Adherence works, see the [Task Adherence Concepts](./concepts/task-adherence.md) page. 


::: zone pivot="programming-language-foundry-portal"

[!INCLUDE [Foundry portal quickstart](./includes/quickstarts/foundry-quickstart-task-adherence.md)]

::: zone-end

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API quickstart](./includes/quickstarts/rest-quickstart-task-adherence.md)]

::: zone-end

## Clean up resources

If you want to clean up and remove an Azure AI services subscription, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Related content

* [Harm categories](./concepts/harm-categories.md)
* Configure filters for each category and test on datasets using [Content Safety Studio](studio-quickstart.md), export the code and deploy.

