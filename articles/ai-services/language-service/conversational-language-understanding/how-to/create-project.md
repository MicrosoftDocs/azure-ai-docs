---
title: Create a CLU project with REST API
titleSuffix: Azure AI services
description: This article shows you how to create a CLU project using the REST API
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 07/23/2025
ms.author: lajanuar
ms.custom: language-service-clu
---

# Create a CLU project REST API

Azure Conversational Language Understanding (CLU) projects enable the development of custom natural language understanding models designed to extract intents and entities from conversational text. These models can be integrated into conversational AI applications and systems that require intelligent processing and response to natural language inputs.

If you already have an Azure AI Language or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Azure AI Foundry portal. For more information, see [How to use Azure AI services in the Azure AI Foundry portal](../../../../ai-services/connect-services-ai-foundry-portal.md).

## Prerequisites

* An Azure subscription. If you don't have one, you can [create one for free](https://azure.microsoft.com/free/cognitive-services).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](../../../openai/how-to/role-based-access-control.md#cognitive-services-contributor).
* An [Azure AI Foundry resource](../../../multi-service-resource.md)
  * For more information, *see* [Configure an Azure AI Foundry resource](configure-azure-resources.md#option-1-configure-an-azure-ai-foundry-resource).
* After you create an Azure AI Foundry resource, [create a CLU project](#create-a-clu-project).

## Create a CLU project

Projects are designed to help you organize your work. They offer various tools and resources that support the development, customization, and management of AI applications all within a centralized environment.

[!INCLUDE [create project](../includes/rest-api/create-project.md)]


## Import an existing Azure AI project

You can import your CLU config.json file. Importing the configuration file allows you to bring your existing settings directly into the platform, making it easier to set up and customize your service based on your predefined preferences.

[!INCLUDE [Import project](../includes/rest-api/import-project.md)]


## Export a project

You can export a CLU project as a config.json file. Exporting your configuration file enables you to save the current state of your project's settings and structure, making it easy to back up or transfer your project as needed.

[!INCLUDE [Export project](../includes/rest-api/export-project.md)]

## View and manage project details

You have the ability to access, view, and manage all of your project details by utilizing the REST API. You can retrieve up-to-date information about your projects, make any necessary changes, and oversee project management tasks efficiently through API endpoints.

[!INCLUDE [REST APIs project details](../includes/rest-api/project-details.md)]

## Delete a project

If your project is no longer required, you can delete it using the REST API. This process ensures that the project and all of its associated data are permanently removed from the system. To proceed, access the REST API and follow the documented steps for project deletion to complete this action.

[!INCLUDE [Delete project](../includes/rest-api/delete-project.md)]



## Related content

- [Build schema](./build-schema.md)

