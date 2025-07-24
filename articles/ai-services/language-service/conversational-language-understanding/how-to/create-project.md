---
title: Create Projects in Conversational Language Understanding
titleSuffix: Azure AI services
description: This article shows you how to create projects in conversational language understanding (CLU).
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 07/23/2025
ms.author: lajanuar
ms.custom: language-service-clu
---

# Create a CLU project in Azure AI Foundry

Azure AI Foundry projects help you organize your work when exploring new ideas or developing prototypes for specific use cases. A Foundry project is created on an Azure AI Foundry resource. This type of project offers an easy setup and provides access to agents and Azure AI models.

If you already have an Azure AI Language or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Azure AI Foundry portal. For more information, see [How to use Azure AI services in the Azure AI Foundry portal](../../../../ai-services/connect-services-ai-foundry-portal.md).

## Prerequisites

* An Azure subscription. If you don't have one, you can [create one for free](https://azure.microsoft.com/free/cognitive-services).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](../../../openai/how-to/role-based-access-control.md#cognitive-services-contributor).
* An [Azure AI Foundry resource](../../../multi-service-resource.md)
  * For more information, *see* [Configure an Azure AI Foundry resource](configure-azure-resources.md#option-1-configure-an-azure-ai-foundry-resource).
* **A project created in the Azure AI Foundry**. For more information, *see* [Create an AI Foundry project](../../../../ai-foundry/how-to/create-projects.md).

## Create a CLU project

After you create an Azure AI Foundry resource, create a CLU project.

### [Azure AI Foundry](#tab/azure-ai-foundry)

To create a Foundry project, *see* [Create an AI Foundry project](../../../../ai-foundry/how-to/create-projects.md).


### [REST APIs](#tab/rest-api)

[!INCLUDE [create project](../includes/rest-api/create-project.md)]

---

## Import an existing Azure AI project

### [Azure AI Foundry](#tab/azure-ai-foundry)

To import an existing Azure AI services project with Azure AI Foundry, you need to create a connection to the Azure AI services resource within your Azure AI Foundry project. For more information, *see* [Connect Azure AI Services projects to Azure AI Foundry](../../../../ai-services/connect-services-ai-foundry-portal.md)

### [REST APIs](#tab/rest-api)

You can import a CLU JSON into the service.

[!INCLUDE [Import project](../includes/rest-api/import-project.md)]

---

## Export a project

### [Azure AI Foundry](#tab/azure-ai-foundry)

You can download a CLU project as a **config.json** file:

* Navigate to your project home page.
* At the top of the page, select your project from the right page ribbon area.
* Select **Download config file**.

### [REST APIs](#tab/rest-api)

You can export a CLU project as a JSON file at any time.

[!INCLUDE [Export project](../includes/rest-api/export-project.md)]

---

## View and manage project details

### [Azure AI Foundry](#tab/azure-ai-foundry)

* On the project Home page, you can find information about the project in the **Project details** section.
* To view project settings, select **Management center** then select one of the following tabs:
 *  **Overview** to view project details.
 *  **Users** to manage users and roles.
 *  **Models + endpoints** to manage deployments of your models and services.
 *  **Connected resources to manage connected resources for the project.

### [REST APIs](#tab/rest-api)

[!INCLUDE [REST APIs project details](../includes/rest-api/project-details.md)]

---

## Delete a project

### [Azure AI Foundry](#tab/azure-ai-foundry)


If you no longer need your project, you can delete it from the Azure AI Foundry.

1. Navigate to the [Azure AI Foundry](https://ai.azure.com/) home page and sign in if you haven't already done so.
1. Select the project that you want to delete from the **Keep building with Azure AI Foundry**
1. Select **Management center**.
1. On the right select **Delete project**.

To delete the hub along with all its projects:

1. Navigate to the **Overview** tab inn the **Hub** section.
1. On the right, select **Delete hub**. 
1. The link will open the Azure portal for you to delete the hub there.

### [REST APIs](#tab/rest-api)

If you no longer need your project, you can delete it using the REST API.

[!INCLUDE [Delete project](../includes/rest-api/delete-project.md)]

---

## Related content

- [Build schema](./build-schema.md)
