---
title: Create and deploy a custom question and answering (CQA) agent in Microsoft Foundry
titleSuffix: Foundry Tools
description: Use this guide to create a CQA Microsoft Foundry agent.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 11/18/2025
---
# Create and deploy a CQA agent

This article gives you clear steps and important tips for building and deploying a CQA agent. Whether you're new to this process or updating your skills, this guide helps you set up and launch your agent successfully.

> [!NOTE]
>
> * If you already have an Azure Language in Foundry Tools or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Microsoft Foundry portal. For more information, see [How to use Foundry Tools in the Foundry portal](/azure/ai-services/connect-services-foundry-portal).
> * In Foundry, a fine-tuning task serves as your workspace for your CQA solutions. Previously, a **fine-tuning task** was referred to as a **CQA project**. You might encounter both terms used interchangeably in older CQA documentation.
> * We highly recommend that you use a Foundry resource in the Foundry; however, you can also follow these instructions using a Language resource.
>

## Prerequisites

Before you get started, you need the following resources and permissions:

* **An active Azure subscription**. If you don't have one, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](../../../openai/how-to/role-based-access-control.md#cognitive-services-contributor).
*   A [Foundry resource](../../../multi-service-resource.md) or a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
*   An [Azure AI Search resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.Search) (required for accessing CQA). For more information on how to connect your Azure AI Search resource, *see* [Configure connections in Foundry](../../conversational-language-understanding/how-to/configure-azure-resources.md#step-2-configure-connections-in-ai-foundry)
* A Foundry project created in the Foundry with a **deployed CQA knowledge base**. For more information, *see* [Create and deploy a CQA project](create-test-deploy.md)

## Step 1: Get started

Let's begin:

1. Navigate to the Foundry.

1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.

1. Once signed in, you can create or access your existing projects within Foundry.

1. If you're not already in your Foundry project with your deployed CQA knowledge base, select it now.


## Step 2: Deploy an OpenAI model in Foundry (required)

An OpenAI model serves as the foundational source of intelligence and advanced reasoning for your agent.

1. Select **Models + endpoints** from the **My assets** section of the navigation menu:

   :::image type="content" source="../media/agents/models-endpoints.png" alt-text="Screenshot of the deploy model button menu in Foundry.":::

1. From the main window, select the **+ Deploy model** button.

1. Select **Deploy base model** from the drop-down menu.

   :::image type="content" source="../media/agents/deploy-model-button.png" alt-text="Screenshot of the connected resources menu selection in Foundry.":::

1. From the **Select a model** window, select the **gpt-4** base model for this project.

   :::image type="content" source="../media/agents/gpt-4-selection.png" alt-text="Screenshot of the select a model selection in Foundry.":::

1. Next, select the **Confirm** button.

1. In the **Deploy gpt-4** window, keep the default values and select the **Deploy** button.

   :::image type="content" source="../media/agents/deploy-gpt-4.png" alt-text="Screenshot of the gpt-4 deployment window in Foundry.":::

1. Great! The model deployment step is complete.

## Step 3: Connect a custom key (required)

A custom key serves as an enhanced security credential for your agent.

1. Navigate to **Management Center** → **Connected Resources**.

    :::image type="content" source="../media/agents/connected-resources.png" alt-text="Screenshot of Management center navigation menu's connected resources selection in Foundry.":::

1. From the main window, select the **+ New connection** button.

1. From the **Add a connection to external assets** window, under **Other resource types**, select **Custom keys**.

    :::image type="content" source="../media/agents/add-custom-keys.png" alt-text="Screenshot of add your custom keys selection in Foundry.":::

1. In the **Connect a custom resource** window, configure the connection as follows:

   * **Authentication**. Leave this field set to **Custom** (default).

   * **Custom keys**. Select **+ Add key value pairs** and complete the two fields as follows:

    * **First field**. Complete this field with the following key name:

      ```text
      Ocp-Apim-Subscription-Key

      ```
    * **Second field**. Complete this field with the key value from your Azure portal **Foundry** or **Language** resource used to create your CQA knowledge base. Make sure to check the **is secret** box.

        :::image type="content" source="../media/agents/connect-custom-resource.png" alt-text="Screenshot of the connect a custom resource window in the Foundry.":::

    * Next, add a **Connection name**.

    * Finally, select the **Add connection** button.

1. Your new Custom key connection is listed on the **Manage connected resources in this project** page.

1. We now provisioned all the necessary resources to create an agent. Select the **Go to project** button to return to your project with your deployed CQA knowledge base.

    :::image type="content" source="../media/agents/go-to-project.png" alt-text="Screenshot of go to project button in Foundry.":::

## Step 4: Create an agent

With your OpenAI deployment and custom key in place, you're ready to begin building your agent, grounded in the knowledge base you chose for this project.

1. From your project's overview page, select **Fine tuning** from the left navigation menu.
1. In the main window, select the **model name**, created with your deployed CQA knowledge base, from the displayed list.
1. Select **Deploy knowledge base** from the **Getting started** menu.
1. Under next steps, select the **Create an agent** button.

   :::image type="content" source="../media/agents/create-agent-button.png" alt-text="Screenshot of the create agent button in Foundry.":::

1. In the **Create new CQA agent** window, complete the fields as follows:

   * **Foundry Project Name**. The name of your project should already appear in this field by default.
   * **Deployment Model**. The name of the model that you deployed in [Step 2](#step-2-deploy-an-openai-model-in-foundry-required) should already appear in this field by default.
   * **Agent Name**. Name your agent (don't use dashes or underscores).
   * **Custom Connection**. The name of the custom key that you connected in [Step 3](#step-3-connect-a-custom-key-required) should already appear in this field by default.
1. Select the **Next** button:

   :::image type="content" source="../media/agents/create-new-agent.png" alt-text="Screenshot of create CQA agent window in Foundry.":::

1. Review the details of your new agent, and then select the **Create agent** button.

1. Once your agent is successfully created, select the **Try in playground** button.

   :::image type="content" source="../media/agents/review-agent-details.png" alt-text="Screenshot of create CQA agent review and create window in Foundry.":::

## Step 5: Test in agents playground

The agents playground provides a sandbox to test and configure a deployed agent—adding knowledge and defining actions—before deploying it to production, all without writing code.

1. From the **Create and debug your agents** window select the **Try in Playground** button.

    :::image type="content" source="../media/agents/create-debug-agent.png" alt-text="Screenshot of the **Create and debug your agents** window and **Try in playground** button in Foundry":::

1. Once the agent is successfully uploaded to the playground, you can test it by sending test queries.

      :::image type="content" source="../media/agents/agents-playground.png" alt-text="Screenshot of the agents playground in Foundry.":::


That's it! The agent creation and deployment processes are complete. You now know how to deploy a CQA agent using your own custom knowledge base.

## Clean up resources

To clean up and remove an Azure AI resource, you can delete either the individual resource or the entire resource group. If you delete the resource group, all resources contained within are also deleted.

## Next Steps

> [!div class="nextstepaction"]
> [Learn about CQA supported languages](../language-support.md)


