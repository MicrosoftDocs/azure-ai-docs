---
title: Create orchestration workflow projects and use Azure resources
titleSuffix: Foundry Tools
description: Use this article to learn how to create projects in orchestration workflow
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-orchestration
---
# How to create projects in orchestration workflow

Orchestration workflow allows you to create projects that connect your applications to:
* Custom Language Understanding
* Question Answering
* LUIS

## Prerequisites

Before you start using orchestration workflow, you will need several things:

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* An Azure Language in Foundry Tools resource 

### Create a Language resource 

Before you start using orchestration workflow, you will need a Language resource.

> [!NOTE]
>  * You need to have an **owner** role assigned on the resource group to create a Language resource.
>  * If you're planning to use question answering, you have to enable question answering in resource creation

[!INCLUDE [create a new resource from the Azure portal](../includes/resource-creation-azure-portal.md)]

## Create an orchestration workflow project (REST API)

Once you have a Language resource created, create an orchestration workflow project. 


[!INCLUDE [create project](../includes/rest-api/create-project.md)]

## Import an orchestration workflow project (REST API)

You can import an orchestration workflow JSON into the service

[!INCLUDE [Import project](../includes/rest-api/import-project.md)]

## Export project (REST API)

You can export an orchestration workflow project as a JSON file at any time.

[!INCLUDE [Export project](../includes/rest-api/export-project.md)]

## Get orchestration project details (REST API)

[!INCLUDE [REST APIs project details](../includes/rest-api/project-details.md)]


## Delete project (REST API)

When you don't need your project anymore, you can delete your project using the APIs.

[!INCLUDE [Delete project](../includes/rest-api/delete-project.md)]


:::image type="content" source="../media/quickstart-intent.png" alt-text="A screenshot showing how to import orchestration project." lightbox="../media/quickstart-intent.png":::

## Next Steps

[Build schema](./build-schema.md)
