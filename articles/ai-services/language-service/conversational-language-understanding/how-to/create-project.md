---
title: Create a CLU fine-tuning task in Microsoft Foundry or with the REST API
titleSuffix: Foundry Tools
description: This article shows you how to create CLU fine-tuning task projects the Microsoft Foundry or using the REST API.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-clu
---
# Create a fine-tuning task project

A Conversational Language Understanding (CLU) fine-tuning task is a workspace project where you customize a language model to identify user intent and extract key information (entities) from user input (utterances). In this workspace, you define the intents and entities relevant to your application, label sample user utterances accordingly, and use this labeled data to fine-tune the model. This process tailors the model to better understand the specific needs and nuances of your conversational application. In this guide, we walk you through configuring a fine-tuning workspace in the Microsoft Foundry or using the REST API.

> [!NOTE]
>
> * If you already have an Azure Language in Foundry Tools or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Foundry portal. For more information, see [How to use Foundry Tools in the Foundry portal](../../../../ai-services/connect-services-foundry-portal.md).
> * In Foundry, a fine-tuning task serves as your workspace when customizing your CLU model. Previously, a **fine-tuning task** was referred to as a **CLU project**. You might encounter both terms used interchangeably in older CLU documentation.
> * We highly recommend that you use a Foundry resource in the Foundry; however, you can also follow these instructions using a Language resource.
>

## Prerequisites

* An **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](../../../openai/how-to/role-based-access-control.md#cognitive-services-contributor).
*  An [**Foundry resource**](../../../multi-service-resource.md). For more information, *see* [Configure a Foundry resource](configure-azure-resources.md#option-1-configure-a-foundry-resource). Alternately, you can use a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
* **A Foundry project created in the Foundry**. For more information, *see* [Create a Foundry project](../../../../ai-foundry/how-to/create-projects.md).

## Fine-tune a CLU model

 To create a CLU fine-tuning model, you first configure your environment and then create a fine-tuning project, which serves as your workspace for customizing your CLU model.

### [Foundry](#tab/azure-ai-foundry)

1. Navigate to the [Foundry](https://ai.azure.com/).
1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.
1. Once signed in, you can create or access your existing projects within Foundry.
1. If you're not already at your project for this task, select it.
1. Select Fine-tuning from the left navigation pane.

   :::image type="content" source="../media/select-fine-tuning.png" alt-text="Screenshot of fine-tuning selector in the Foundry.":::

1. From the main window, select **the AI Service fine-tuning** tab and then the **+ Fine-tune** button.

   :::image type="content" source="../media/fine-tune-button.png" alt-text="Screenshot of fine-tune button in the Foundry.":::

1. From the **Create service fine-tuning** window, choose the **Conversational language understanding** tab, and then select **Next**.

   :::image type="content" source="../media/select-project.png" alt-text="Screenshot of conversational language understanding tab in the Foundry.":::

1. In the **Create CLU fine-tuning task** window, complete the **Name** and **Language** fields. If you're planning to fine-tune a model using the free **Standard Training** mode, select **English** for the language field.

1. Select the  **Create** button. It can take a few minutes for the *creating* operation to complete.

   > [!NOTE]
   >
   > * **Standard training** enables faster training times and quicker iterations; however it's only available for English.
   > * **Advanced training** includes longer training durations and is supported for English, other languages, and multilingual projects.
   > * For more information, *see* [Training modes](train-model.md#training-modes).

1. Once the task creation is complete, select the task from the Foundry Tool fine-tuning window to arrive at the **Getting started with fine-tuning** page.

   :::image type="content" source="../media/create-project/getting-started-fine-tuning.png" alt-text="Screenshot of the getting started with fine-tuning page in the Foundry." lightbox="../media/create-project/getting-started-fine-tuning.png":::

### [REST APIs](#tab/rest-api)

[!INCLUDE [create project](../includes/rest-api/create-project.md)]

---


That's it! You can get started on your fine-tuning task project. For more information, *see* [Next steps](#next-steps).

## View and manage project details

You can retrieve up-to-date information about your projects, make any necessary changes, and oversee project management tasks efficiently through the Foundry or REST API endpoints.

### [Foundry](#tab/azure-ai-foundry)

Your Foundry project overview page displays information about your fine-tuning task project, including its name, subscription, resource group, and connected resources. You can also access the project's resources in the Azure portal by selecting **Manage in Azure portal** on the overview page.

* On the project Home page, information about the project is found in the **Project details** section.
* To view project settings, select **Management center** from the bottom of the left navigation pane, then select one of the following tabs:
   *  **Overview** to view project details.
   *  **Users** to manage users and roles.
   *  **Models + endpoints** to manage deployments of your models and services.
   *  **Connected resources** to manage connected resources for the project.

   :::image type="content" source="../media/create-project/project-details.png" alt-text="Screenshot of the project details list in the Foundry.":::

### [REST APIs](#tab/rest-api)

You can access, view, and manage all of your project details via the REST API.

[!INCLUDE [REST APIs project details](../includes/rest-api/project-details.md)]

---

## Import an existing Foundry project

Importing the configuration file allows you to bring your existing settings directly into the platform, making it easier to set up and customize your service based on your predefined preferences.

### [Foundry](#tab/azure-ai-foundry)

To import an existing Foundry Tools project with Foundry, you need to create a connection to the Foundry Tools resource within your Foundry project. For more information, *see* [Connect Foundry Tools projects to Foundry](../../../../ai-services/connect-services-foundry-portal.md)

### [REST APIs](#tab/rest-api)

You can import your CLU config.json file using the REST API

[!INCLUDE [Import project](../includes/rest-api/import-project.md)]

---

## Export a fine-tuning project

Exporting your configuration file enables you to save the current state of your project's settings and structure, making it easy to back up or transfer your project as needed.

### [Foundry](#tab/azure-ai-foundry)

You can download a Microsoft Foundry fine-tuning task project as a **config.json** file:

1. Navigate to your project home page.
1. At the top of the page, select your project from the right page ribbon area.
1. Select **Download config file**.

    :::image type="content" source="../media/create-project/download-config-json.png" alt-text="Screenshot of project drop-down menu with the download config file hyperlink in the Foundry.":::

### [REST APIs](#tab/rest-api)

You can export a CLU project as a config.json file.

[!INCLUDE [Export project](../includes/rest-api/export-project.md)]

---


## Delete a project

Deleting a project ensures that it and all of its associated data are permanently removed from the system.

### [Foundry](#tab/azure-ai-foundry)

If you no longer need your project, you can delete it from the Foundry.

1. Navigate to the [Foundry](https://ai.azure.com/) home page. Initiate the authentication process by signing in, unless you already completed this step and your session is active.
1. Select the project that you want to delete from the **Keep building with Foundry**
1. Select **Management center**.
1. Select **Delete project**.

   :::image type="content" source="../media/create-project/delete-project.png" alt-text="Screenshot of the Delete project button in the Foundry.":::

To delete the hub along with all its projects:

1. Navigate to the **Overview** tab inn the **Hub** section.

   :::image type="content" source="../media/create-project/hub-details.png" alt-text="Screenshot of the hub details list in the Foundry.":::

1. On the right, select **Delete hub**.
1. The link opens the Azure portal for you to delete the hub.

   :::image type="content" source="../media/create-project/delete-hub.png" alt-text="Screenshot of the Delete hub button in the Foundry.":::

### [REST APIs](#tab/rest-api)

If your project is no longer required, you can delete it using the REST API. To proceed, access the REST API and follow the documented steps for project deletion to complete this action.

[!INCLUDE [Delete project](../includes/rest-api/delete-project.md)]

---

## Next steps

After you create your fine-tuning workspace, start your fine-tuning task by defining your intents and entities and adding them to your schema:

* [Build your fine-tuning schema](build-schema.md)
* [Label utterances](tag-utterances.md)