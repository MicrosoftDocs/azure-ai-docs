---
title: Create, test, and deploy your custom question answering project in Azure AI Foundry
description: Create a custom question answering project from your own content, such as FAQs or product manuals. This article includes an example of creating a custom question answering project from a simple FAQ webpage, to answer questions.
ms.service: azure-ai-language
ms.topic: include
ms.date: 06/30/2025
---

This quickstart guides you through the essential steps needed to create, test, and deploy a custom question answering (CQA) project in the Azure AI Foundry. Whether you're transitioning from Language Studio or starting from scratch, this quickstart is for you. It provides clear and actionable instructions to achieve a fast and successful CQA project deployment.

> [!NOTE]
>
> * If you already have an Azure AI Language or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Azure AI Foundry portal. For more information, see [How to use Azure AI services in the Azure AI Foundry portal](../../../../ai-services/connect-services-ai-foundry-portal.md).
> * In Azure AI Foundry, a fine-tuning task serves as your workspace for your CQA solutions. Previously, a **fine-tuning task** was referred to as a **CQA project**. You might encounter both terms used interchangeably in older CQA documentation.
> * We highly recommend that you use an Azure AI Foundry resource in the AI Foundry; however, you can also follow these instructions using a Language resource.
>

## Prerequisites

Before you get started, you need the following resources and permissions:

* **An active Azure subscription**. If you don't have one, [create one for free](https://azure.microsoft.com/free/cognitive-services).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](../../../openai/how-to/role-based-access-control.md#cognitive-services-contributor).
*   An [Azure AI Foundry multi-service resource](../../../multi-service-resource.md) or an [Azure AI Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
*   An [Azure AI Search resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.Search) (required for accessing CQA). For more information on how to connect your Azure AI Search resource, *see* [Configure connections in AI Foundry](../../conversational-language-understanding/how-to/configure-azure-resources.md#step-2-configure-connections-in-ai-foundry)
* A Foundry project created in the Azure AI Foundry. For more information, *see* [Create an AI Foundry project](/azure/ai-foundry/how-to/create-projects).

Let's begin:

1. Navigate to the [Azure AI Foundry](https://ai.azure.com/).
1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.
1. Once signed in, you can create or access your existing projects within Azure AI Foundry.
1. If you're not already at your project for this task, select it.

## Create your CQA fine tuning task

* After you select the Azure AI Foundry project to use for this quickstart, from the left navigation menu select **fine-tuning**.

   :::image type="content" source="../media/agents/fine-tuning-selection.png" alt-text="Screenshot of the fine-tuning menu selection in the Azure AI Foundry.":::

*  From the main window, select the **AI Service fine-tuning** tab and then the **+ Fine-tune button**.

    :::image type="content" source="../media/agents/fine-tune-button.png" alt-text="Screenshot of fine-tune button in the Azure AI Foundry.":::

* From the **Create service fine-tuning** window, choose the **Custom question answering** tab and then select **Next**.

    :::image type="content" source="../media/agents/custom-question-answering-tab.png" alt-text="Screenshot of custom question answering tab in the Azure AI Foundry.":::

*  Select your **Connected Azure AI Search resource** from the **Create CQA fine tuning task** window. For more information, *see* [Configure Azure resource connections](../../conversational-language-understanding/how-to/configure-azure-resources.md#step-2-configure-connections-in-ai-foundry).

* Next, complete the **Name** and **Language** fields. For this project, you can leave the **Default answer when no answer is returned** field as **No answer found**. Select the **Create** button.

## Add a knowledge base source

*  From the **Getting Started** menu, select **Manage sources**.

   :::image type="content" source="../media/agents/manage-sources.png" alt-text="Screenshot of manage sources selection in the Azure AI Foundry.":::

* From the main window, select the **+ Add source** drop-down menu.

*  From the menu you can select **Add chit chat**, **Add URLs**, or **Add Files**.

  :::image type="content" source="..media/agents/add-source-menu.png" alt-text="Screenshot of add source drop-down menu in the Azure AI Foundry.":::

* For this project, let's choose **Add chitchat**.

*  From the **Add new source** window, let's choose **Friendly**. Finally, select **Add**. It may take a few minutes for the source to be created.

   :::image type="content" source="../media/agents/select-source-type.png" alt-text="Screenshot of the select source selection and add button in the Azure AI Foundry.":::


*  Once created, the source is listed in the **Manage sources** window.

   :::image type="content" source="../media/agents/manage-sources-list.png" alt-text="Screenshot of manage sources list in the Azure AI Foundry.":::


## Test your knowledge base

* Select **Test knowledge base** from the **Getting Started** menu.

*  Type the following in the **Type your question** field and then select **Run**.

   ```text
      Hello! How are you doing today?

   ```

* In the inspection interface, you can review the response confidence level and choose the most suitable answer.

:::image type="content" source="../media/agents/inspection-interface.png" alt-text="Screenshot of the inspection interface in the Azure AI Foundry.":::


## Deploy the Knowledge Base

*  Once your inspection is complete, choose the **Deploy knowledge base** section from the **Getting Started** menu.

* Select the **Deploy** button first from the **Deploy knowledge base** main window and then from the **Deploy this project** pop-up window. It takes a few minutes to deploy.

* Once deployment is complete, your deployed project is listed in the **Deploy knowledge base** window.

That's it! Your Custom Question Answering (CQA) knowledge base enables a natural language interface for your data. With this deployed solution, you can build intelligent chatbots and interactive agents that understand user queries, deliver accurate responses, and adapt to evolving informational needs.



