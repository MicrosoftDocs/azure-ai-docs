---
title: Create, test, and deploy your custom question answering (CQA) knowledge base
description: You can create a custom question answering knowledge from your own content, such as FAQs or product manuals. This article includes an example of creating a custom question answering knowledge base.
ms.service: azure-ai-language
ms.topic: how-to
author: laujan
ms.author: lajanuar
ms.date: 12/15/2025
ms.custom: language-service-question-answering, mode-other
---
# Create, test, and deploy: CQA knowledge base

This guide walks you through the essential steps needed to create, test, and deploy a custom question answering (CQA) knowledge base in the Microsoft Foundry. Whether you're transitioning from Language Studio or starting from scratch, this guide is for you. It provides clear and actionable instructions to achieve a fast and successful CQA deployment in the Foundry.

> [!NOTE]
>
> * If you already have an Azure Language in Foundry Tools or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Foundry portal. For more information, see [How to use Foundry Tools in the Foundry portal](/azure/ai-services/connect-services-foundry-portal).
> * In Foundry, a fine-tuning task serves as your workspace for your CQA solutions. Previously, a **fine-tuning task** was referred to as a **CQA project**. You might encounter both terms used interchangeably in older CQA documentation.
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

1. After you select the Foundry project to use for this project, select **fine-tuning** from the left navigation menu.

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

1. For this project, choose **Add URLS**.

1. In the **Add URLs** window, add the following values:

   * **URL name**: **Surface Book User Guide**
   * **URL**: **https://download.microsoft.com/download/7/B/1/7B10C82E-F520-4080-8516-5CF0D803EEE0/surface-book-user-guide-EN.pdf** 
   * **Classify file structure**: Leave the default setting (**Auto-detect**)

     :::image type="content" source="../media/agents/add-urls.png" alt-text="Screenshot of the select url source selection and add button in the Foundry.":::

1. Finally, select the **Add URLs** button. 

    The extraction process requires a short amount of time to analyze the document and detect questions and answers. During this step, the service evaluates whether the content is structured or unstructured.<br>

    Once the source is successfully added, you can edit its contents and include added custom question-and-answer pairs.


1. Once the source is successfully added, it appears in the **Manage sources** window. There you have the option to edit its contents and include additional custom question-and-answer pairs.

     :::image type="content" source="../media/agents/manage-url-sources.png" alt-text="Screenshot of manage sources listing in the Foundry.":::

## Test your knowledge base

1. Select **Test knowledge base** from the **Getting Started** menu.

1. In the main window,  Enter the question **How do I set up my Surface Book?** and then select the **Run** button. Answers are returned using the question-and-answer pairs that were automatically detected and taken from the source URL:


    :::image type="content" source="../media/agents/test-knowledge-base.png" alt-text="Screenshot of the inspection interface response in the Foundry." lightbox="../media/agents/test-knowledge-base.png":::


## Deploy your knowledge base

Deploying a CQA knowledge base means publishing your curated question-and-answer content as a live, searchable endpoint. This process moves your project from a testing phase to a production environment enabling client applications to use it for various projects and solutions, including chatbots.

1. Once your inspection is complete, choose the **Deploy knowledge base** section from the **Getting Started** menu.

1. Select the **Deploy** button first from the **Deploy knowledge base** main window and then from the **Deploy this project** pop-up window. It takes a few minutes to deploy.

1. After deployment is complete, your deployed project is listed in the **Deploy knowledge base** window.

That's it! Your Custom Question Answering (CQA) knowledge base provides a natural language interface to your data, allowing users to interact with information in a conversational manner. By deploying this solution, you can create advanced chatbots and interactive agents that comprehend user questions, supply precise answers, and adjust to changing informational requirements.

## Clean up resources

To clean up and remove an Azure AI subscription, you can delete either the individual resource or the entire resource group. If you delete the resource group, all resources contained within it will also be deleted.

## Next steps
