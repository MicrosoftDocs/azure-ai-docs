---
title: Create a CLU fine-tuning task in Azure AI Foundry
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

# Create a fine-tuning task Azure AI Foundry

A Conversational Language Understanding (CLU) fine-tuning task is a workspace project in Azure AI Foundry where you customize a language model to identify user intent and extract key information (entities) from user input (utterances). In this workspace, you define the intents and entities relevant to your application, label sample user utterances accordingly, and use this labeled data to fine-tune the model. This process tailors the model to better understand the specific needs and nuances of your conversational application.

In this guide, we walk you through configuring a fine-tuning workspace in the Azure AI Foundry. To set up a CLU fine-tuning workspace, you first configure your environment and then create a fine-tuning task, which serves as your workspace for customizing your CLU model.

> [!NOTE]
>
> If you already have an Azure AI Language or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Azure AI Foundry portal. For more information, see [How to use Azure AI services in the Azure AI Foundry portal](../../../../ai-services/connect-services-ai-foundry-portal.md).
>
> In Azure AI Foundry, you set up a fine-tuning task to serve as your workspace when customizing your CLU model. Previously, a **fine-tuning task** was referred to as a **CLU project**. You might encounter both terms used interchangeably in older CLU documentation.
>

## Prerequisites

* An Azure subscription. If you don't have one, you can [create one for free](https://azure.microsoft.com/free/cognitive-services).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](../../../openai/how-to/role-based-access-control.md#cognitive-services-contributor).
* An [Azure AI Foundry resource](../../../multi-service-resource.md)
  * For more information, *see* [Configure an Azure AI Foundry resource](configure-azure-resources.md#option-1-configure-an-azure-ai-foundry-resource).
* A Foundry project created in the Azure AI Foundry. For more information, *see* [Create an AI Foundry project](../../../../ai-foundry/how-to/create-projects.md).


## Create a CLU fine-tuning task

1. Navigate to the [Azure AI Foundry](https://ai.azure.com/).
1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.
1. Once signed in, you can create or access your existing projects within Azure AI Foundry.
1. If you're not already at your project for this task, select it.
1. Select Fine-tuning from the left navigation panel.

   :::image type="content" source="../media/select-fine-tuning.png" alt-text="Screenshot of fine-tuning selector in the Azure AI Foundry.":::

1. Select **the AI Service fine-tuning** tab and then **+ Fine-tune** button.

   :::image type="content" source="../media/fine-tune-button.png" alt-text="Screenshot of fine-tuning button in the Azure AI Foundry.":::

1. From **Create service fine-tuning** window, choose the **Conversational language understanding** tab then select **Next**.

   :::image type="content" source="../media/select-project.png" alt-text="Screenshot of conversational language understanding tab in the Azure AI Foundry.":::

1. In **Create CLU fine-tuning task** window, complete the **Name** and **Language** fields. If you're planning to fine-tune a model using the free **Standard Training** mode, select **English** for the language field.

1. Navigate to the [Azure AI Foundry](https://ai.azure.com/).
1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.
1. Once signed in, you can create or access your existing projects within Azure AI Foundry.
1. If you're not already at your project for this task, select it.
1. Select Fine-tuning from the left navigation panel.

    :::image type="content" source="../media/select-fine-tuning.png" alt-text="Screenshot of fine-tuning selector in the Azure AI Foundry.":::

1. Select **the AI Service fine-tuning** tab and then **+ Fine-tune** button.

    :::image type="content" source="../media/fine-tune-button.png" alt-text="Screenshot of fine-tuning button in the Azure AI Foundry.":::

1. From **Create service fine-tuning** window, choose the **Conversational language understanding** tab then select **Next**.

    :::image type="content" source="../media/select-project.png" alt-text="Screenshot of conversational language understanding tab in the Azure AI Foundry.":::

1. In **Create CLU fine tuning task** window, select your **Connected service** from the drop-down menu, then complete the **Name** and **Language** fields. If you're using the free **Standard Training** mode, select **English** for the language field.

1. Select the  **Create** button. It can take a few minutes for the *creating* operation to complete.


   > [!NOTE]
   >
   > * **Standard training** enables faster training times and quicker iterations; however it's only available for English.
   > * **Advanced training** includes longer training durations and is supported for English, other languages, and multilingual projects.
   > * For more information, *see* [Training modes](train-model.md#training-modes).

1. Once the task creation is complete, select the task from the AI Service fine-tuning window to arrive at the Getting started with fine-tuning page.

   :::image type="content" source="../media/create-project/getting-started-fine-tuning.png" alt-text="Screenshot of the getting started with fine-tuning page in the Azure AI Foundry." lightbox="../media/create-project/getting-started-fine-tuning.png":::

That's it! You can get started on your fine-tuning task project. For more information, *see* [Next steps](#next-steps).

## View and manage project details

* On the project Home page, information about the project is found in the **Project details** section.
* To view project settings, select **Management center** from the bottom of the left navigation pane, then select one of the following tabs:
   *  **Overview** to view project details.
   *  **Users** to manage users and roles.
   *  **Models + endpoints** to manage deployments of your models and services.
   *  **Connected resources** to manage connected resources for the project.

   :::image type="content" source="../media/create-project/project-details.png" alt-text="Screenshot of the project details list in the Azure AI Foundry.":::


## Delete a project

If you no longer need your project, you can delete it from the Azure AI Foundry.

1. Navigate to the [Azure AI Foundry](https://ai.azure.com/) home page. Initiate the authentication process by signing in, unless you already completed this step and your session is active.
1. Select the project that you want to delete from the **Keep building with Azure AI Foundry**
1. Select **Management center**.
1. Select **Delete project**.

   :::image type="content" source="../media/create-project/delete-project.png" alt-text="Screenshot of the Delete project button in the Azure AI Foundry.":::

To delete the hub along with all its projects:

1. Navigate to the **Overview** tab inn the **Hub** section.

   :::image type="content" source="../media/create-project/hub-details.png" alt-text="Screenshot of the hub details list in the Azure AI Foundry.":::

1. On the right, select **Delete hub**.
1. The link opens the Azure portal for you to delete the hub there.

   :::image type="content" source="../media/create-project/delete-hub.png" alt-text="Screenshot of the Delete hub button in the Azure AI Foundry.":::

## Next steps

After you create your fine-tuning workspace, start your fine-tuning task by defining your intents and entities and adding them to your schema.

* [Build your fine-tuning schema](build-schema.md)
* [Label utterances](tag-utterances.md)
