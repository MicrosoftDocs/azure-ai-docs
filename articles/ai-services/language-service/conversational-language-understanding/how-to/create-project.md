---
title: Create Projects in Conversational Language Understanding
titleSuffix: Azure AI services
description: Use this article to learn how to create projects in conversational language understanding (CLU).
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 05/01/2025
ms.author: lajanuar
ms.custom: language-service-clu
---

# Create a CLU fine-tuning task

Use this article to learn how to set up these requirements and create a project.

## Prerequisites

* An Azure subscription. If you don't have one, you can [create one for free](https://azure.microsoft.com/free/cognitive-services).
* An Azure AI Language resource.

### Create a Language resource

Before you start using CLU, you need an Azure AI Language resource.

> [!NOTE]
> You need to have an Owner role assigned on the resource group to create a Language resource.

[!INCLUDE [create a new resource from the Azure portal](../includes/resource-creation-azure-portal.md)]

[!INCLUDE [create a new resource from Language Studio](../includes/resource-creation-language-studio.md)]

## Sign in to Language Studio

[!INCLUDE [Sign in to Language studio](../includes/language-studio/sign-in-studio.md)]

## Create a conversation project

After you create a Language resource, create a CLU project.

### [Azure AI Foundry](#tab/azure-ai-foundry)

[!INCLUDE [Create project](../includes/language-studio/create-project.md)]

### [REST APIs](#tab/rest-api)

[!INCLUDE [create project](../includes/rest-api/create-project.md)]

---

## Import project

### [Azure AI Foundry](#tab/azure-ai-foundry)

You can export a CLU project as a JSON file at any time. On the conversation projects page, select a project, and on the top menu, select **Export**.

:::image type="content" source="../media/export.png" alt-text="A screenshot that shows the CLU Export button." lightbox="../media/export.png":::

You can reimport that project as a new project. If you import a project with the exact same name, it replaces the project's data with the newly imported project's data.

If you have an existing Language Understanding (LUIS) application, you can _import_ the LUIS application JSON to CLU directly. It creates a Conversation project with all the pieces that are currently available: intents, machine learning entities, and utterances. For more information, see [Migrate from Language Understanding (LUIS) to conversational language understanding (CLU)](../how-to/migrate-from-luis.md).

To import a project, select the arrow button next to **Create a new project** and select **Import**. Then select the LUIS or CLU JSON file.

:::image type="content" source="../media/import.png" alt-text="A screenshot that shows the CLU Import button." lightbox="../media/import.png":::

### [REST APIs](#tab/rest-api)

You can import a CLU JSON into the service.

[!INCLUDE [Import project](../includes/rest-api/import-project.md)]

---

## Export project

### [Azure AI Foundry](#tab/azure-ai-foundry)

You can export a CLU project as a JSON file at any time. On the conversation projects page, select a project, and select **Export**.

### [REST APIs](#tab/rest-api)

You can export a CLU project as a JSON file at any time.

[!INCLUDE [Export project](../includes/rest-api/export-project.md)]

---

## Get CLU project details

### [Azure AI Foundry](#tab/azure-ai-foundry)

[!INCLUDE [Language Studio project details](../includes/language-studio/project-details.md)]

### [REST APIs](#tab/rest-api)

[!INCLUDE [REST APIs project details](../includes/rest-api/project-details.md)]

---

## Delete project

### [Azure AI Foundry](#tab/azure-ai-foundry)

[!INCLUDE [Delete project](../includes/language-studio/delete-project.md)]

### [REST APIs](#tab/rest-api)

When you don't need your project anymore, you can use the APIs to delete your project.

[!INCLUDE [Delete project](../includes/rest-api/delete-project.md)]

---

## Related content

- [Build schema](./build-schema.md)
