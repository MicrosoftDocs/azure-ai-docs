---
title: Create, test, and deploy your custom question answering project in Microsoft Foundry
description: Create a custom question answering project from your own content, such as FAQs or product manuals. This article includes an example of creating a custom question answering project from a simple FAQ webpage, to answer questions.
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
---
This quickstart guides you through the essential steps needed to create, test, and deploy a custom question answering (CQA) project in the Microsoft Foundry. Whether you're transitioning from Language Studio or starting from scratch, this quickstart is for you. It provides clear and actionable instructions to achieve a fast and successful CQA project deployment.

> [!NOTE]
>
> * If you already have an Azure Language in Foundry Tools or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Foundry portal. For more information, see [How to use Foundry Tools in the Foundry portal](../../../../ai-services/connect-services-foundry-portal.md).
> * We highly recommend that you use a Foundry resource in the Foundry; however, you can also follow these instructions using a Language resource.
>

## Prerequisites

Before you get started, you need the following resources and permissions:

* **An active Azure subscription**. If you don't have one, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](../../../openai/how-to/role-based-access-control.md#cognitive-services-contributor).
*   A [Foundry resource](../../../multi-service-resource.md) or a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
*   An [Azure AI Search resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.Search) (required for accessing CQA). For more information on how to connect your Azure AI Search resource, *see* [Configure connections in Foundry](../../conversational-language-understanding/how-to/configure-azure-resources.md#step-2-configure-connections-in-ai-foundry)
* A Foundry project created in the Foundry. For more information, *see* [Create a Foundry project](/azure/ai-foundry/how-to/create-projects).

## Get started

1. Navigate to the [Foundry](https://ai.azure.com/).

1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.

1. Once signed in, you can create or access your existing projects within Foundry.

1. If you're not already at your project for this task, select it.

## Create your CQA fine tuning task

In the Foundry, a fine-tuning task serves as your workspace for your CQA solutions. Previously, a **fine-tuning task** was referred to as a **CQA project**. You might encounter both terms used interchangeably in older CQA documentation.

1. After you select the Foundry project to use for this quickstart, select **fine-tuning** from the left navigation menu.

     :::image type="content" source="../media/agents/fine-tuning-selection.png" alt-text="Screenshot of the fine-tuning menu selection in the Foundry.":::

1. From the main window, select the **AI Service fine-tuning** tab and then the **+ Fine-tune button**.

     :::image type="content" source="../media/agents/fine-tune-button.png" alt-text="Screenshot of fine-tune button in the Foundry.":::

1. From the **Create service fine-tuning** window, choose the **Custom question answering** tab and then select **Next**.

     :::image type="content" source="../media/agents/custom-question-answering-tab.png" alt-text="Screenshot of custom question answering tab in the Foundry.":::

1. Select your **Connected Azure AI Search resource** from the **Create CQA fine tuning task** window. For more information, *see* [Configure Azure resource connections](../../conversational-language-understanding/how-to/configure-azure-resources.md#step-2-configure-connections-in-ai-foundry).

1. Next, complete the **Name** and **Language** fields. For this project, you can leave the **Default answer when no answer is returned** field as is (**No answer found**).

1. Select the **Create** button.

## Add a CQA knowledge base source

A CQA knowledge base is a structured set of question-and-answer pairs optimized for conversational AI. The knowledge base uses natural language processing to interpret user queries and return context-aware, accurate answers from a specific dataset.

1. From the **Getting Started** menu, select **Manage sources**.

     :::image type="content" source="../media/agents/manage-sources.png" alt-text="Screenshot of manage sources selection in the Foundry.":::

1. From the main window, select the **+ Add source** drop-down menu.

1. From the drop-down menu you can select **Add chit chat**, **Add URLs**, or **Add Files**.

     :::image type="content" source="../media/agents/add-source-menu.png" alt-text="Screenshot of add source drop-down menu in the Foundry.":::

1. For this project, let's choose **Add chitchat**.

1. From the **Add new source** window, let's choose **Friendly**.

     :::image type="content" source="../media/agents/select-source-type.png" alt-text="Screenshot of the select source selection and add button in the Foundry.":::

1. Finally, select **Add**. It may take a few minutes for the source to be created.

1. Once created, the source is listed in the **Manage sources** window.

     :::image type="content" source="../media/agents/manage-sources-list.png" alt-text="Screenshot of manage sources list in the Foundry.":::

## Test your knowledge base

1. Select **Test knowledge base** from the **Getting Started** menu.

1. Type the following in the **Type your question** field and then select **Run**.

     ```text
       Hello! How are you doing today?

     ```

1. In the inspection interface, you can review the response confidence level and choose the most suitable answer.

    :::image type="content" source="../media/agents/inspection-interface.png" alt-text="Screenshot of the inspection interface in the Foundry.":::


## Deploy your knowledge base

Deploying a CQA knowledge base means publishing your curated question-and-answer content as a live, searchable endpoint. This process moves your project from a testing phase to a production environment enabling client applications to use it for various projects and solutions, including chatbots.

1. Once your inspection is complete, choose the **Deploy knowledge base** section from the **Getting Started** menu.

1. Select the **Deploy** button first from the **Deploy knowledge base** main window and then from the **Deploy this project** pop-up window. It takes a few minutes to deploy.

1. After deployment is complete, your deployed project is listed in the **Deploy knowledge base** window.

That's it! Your Custom Question Answering (CQA) knowledge base provides a natural language interface to your data, allowing users to interact with information in a conversational manner. By deploying this solution, you can create advanced chatbots and interactive agents that comprehend user questions, supply precise answers, and adjust to changing informational requirements.





