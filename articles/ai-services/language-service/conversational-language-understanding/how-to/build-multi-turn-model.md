---
title: Build multi-turn conversational language understanding (CLU) models with entity slot filling
titleSuffix: Azure AI services
description: This article shows you how to create a CLU model for multi-turn interactions using slot-filling
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/052025
ms.author: lajanuar
ms.custom: language-service-clu
---

# Build multi-turn CLU models with entity slot filling

In this article, you'll learn how to build a CLU model that uses entity slot filling to enable multi-turn conversations. This approach allows your model to collect information progressively across multiple conversation turns, rather than requiring users to provide all details in a single interaction. 

You'll create a model that can maintain conversation context and extract entities as they're mentioned to complete tasks naturally and efficiently.

## Prerequisites

* **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](/azure/ai-foundry/openai/how-to/role-based-access-control#cognitive-services-contributor).
*  An [**Azure AI Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics). 

     > [!NOTE]
     >  You need to have an **owner** role assigned on the **resource group** to create a Language resource.

* **A Foundry project created in the Azure AI Foundry**. For more information, *see* [Create an AI Foundry project](/azure/ai-foundry/how-to/create-projects).

 * A [**deployed OpenAI model**](#deploy-an-openai-model-in-azure-ai-foundry-required) in Azure AI Foundry.

## Configure required roles, permissions, and settings

Let's begin by configuring your resources:

### Add required roles for your Azure AI Language resource

1. From the Language resource page in the [Azure portal](https://portal.azure.com/), select **Access Control (IAM)** in the left pane.
1. Select **Add** to **Add Role Assignments**, and add **Cognitive Services Language Owner** or **Cognitive Services Contributor** role assignment for your Language resource.
1. Within **Assign access to**, select **User, group, or service principal**.
1. Select **Select members**.
1. Select ***your user name***. You can search for user names in the **Select** field. Repeat this step for all roles.
1. Repeat these steps for all the user accounts that need access to this resource.

## Connect your Azure Language resource to Azure AI Foundry

Next we create a connection to your Azure AI Language resource so Azure AI Foundry can access it securely. This connection provides secure identity management and authentication, as well as controlled and isolated access to data.

  >![NOTE]
  > Currently, the multi-turn capability is only available in the Azure AI Foundry (classic) portal.

1. Navigate to the [Azure AI Foundry (classic)](https://ai.azure.com/).

1. Access your existing Azure AI project for this quickstart.

1. Select **Management center** from the left navigation menu.

1. Select **Connected resources** from the **Hub** section of the **Management center** menu.

1. In the main  window, select the **+ New connection** button.

1. Select **Azure AI Language** from the **Add a connection to external assets** window.

1. Select **Add connection**, then select **Close.**

    :::image type="content" source="../media/add-connection.png" alt-text="Screenshot of the connection window in Azure AI Foundry.":::

## Deploy an OpenAI model in Azure AI Foundry

An OpenAI model serves as the foundational source of intelligence and advanced reasoning for your model.

1. Select **Models + endpoints** from the **My assets** section of the navigation menu:

   :::image type="content" source="../media/models-endpoints.png" alt-text="Screenshot of the deploy model button menu in Azure AI Foundry.":::

1. From the main window, select the **+ Deploy model** button.

1. Select **Deploy base model** from the drop-down menu.

   :::image type="content" source="../media/deploy-model-button.png" alt-text="Screenshot of the connected resources menu selection in Azure AI Foundry.":::

1. From the **Select a model** window, choose a model. The **gpt-4** base model is a good choice for this project.

   :::image type="content" source="../media/gpt-4-selection.png" alt-text="Screenshot of the select a model selection in Azure AI Foundry.":::

1. Next, select the **Confirm** button.

1. In the **Deploy gpt-4** window, keep the default values and select the **Deploy** button.

   :::image type="content" source="../media/deploy-gpt-4.png" alt-text="Screenshot of the gpt-4 deployment window in Azure AI Foundry.":::

1. Great! The model deployment step is complete.

## Build your multi-turn model

With your Language resource, Foundry project and, OpenAI deployment in place, you're ready to begin building your model.

### Create a CLU Project

For this project, we're creating a travel agent model and launch it using Quick Deploy.

1. Navigate to [Azure AI Foundry (classic)](ttps://ai.azure.com).
1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.
1. Once signed in, you can create or access your existing projects within Azure AI Foundry.
1. If you're not already at your project for this task, select it.
1. On the left side navigation pane **Overview** section, select Fine-tuning.
1. From the main window, select the **AI Service fine-tuning** tab and then the **+ Fine-tune** button.
1. From the **Create service fine-tuning** window, choose the **Conversational language understanding** tab, and then select **Next**.
1. In the **create CLU fine-tuning task** window, complete the fields as follows:

   * **Connected service**. The name of your language service resource should appear in this field by default. if not, add it from the drop-down menu.
   * **Name**. Give your fine-tuning task project a name.
   * **Language**. English is set as the default and already appears in the field.
   * **Description**. You can optionally provide a description or leave this field empty.
1. Finally, select the **Create** button. It can take a few minutes for the creating operation to complete.

### Add intents

1. From the **Getting Started** menu, choose **Define schema** data. 
1. In the main window, select the **Add Intent** button.
1. The **Add Intent** window has to required fields:
   * Intent name
   * Intent description (required for Quick Deploy)

1. After you complete these two fields, select the **+Add** button to repeat the process.
1. Let's add the following intents

    |Intent name (Pascal case)|Intent description|
    |---|---|
    |BookFlight|Make a travel reservation for an airline flight.|
    |FlightTime| The scheduled departure and/or arrival time for a airline flight.|
    |FlightStatus|The current status of a scheduled flight.|

1. After completing the intents, select the **Add Intent** button.


### Add entities

1. Next, select the **Entities** tab and then select the **Add entity** button.
1. The **Add an entity** window has to required fields:
   * Entity name
   * Description (required for Quick Deploy)
1. After you complete each of the entity fields, select the **Add an entity** button
1. Let's add the following entities:

    |Entity name (Pascal case)|Entity description|
    |---|---|
    |TravelDate|Desired travel date.|
    |FlightDepartureTime| Departure time for scheduled flight|
    |FlightNumber|Flight number for scheduled flight.|
1. For common data we can add a prebuilt type.

  * Select your **TravelDate** entity
    * Under the **Prebuilt** section, select **Add prebuilt**, select **DateTime** from the drop down list, then select the **Add** button.
  * Select your **FlightDepartureTime** entity
    * Under the **Prebuilt** section, select **Add prebuilt**, select **DateTime** from the drop down list, then select the **Add** button.


### Associate intents with entities

1. Select the **Associations** tab
1. Select each intent and, from the **Available entities** section link it the required entity. This ensures the model knows which slots to fill for each intent.
1. All entities must have an association with at least one intent. After you select the associations, select **Update associations**


   |Intent|Association|
   |---|---|
   |BookFlight|TravelDate|
   |FlightTime| FlightDepartureTime, TravelDate|
   |FlightStatus|FlightNumber, FlightDepartureTime,TravelDate

Now that all your entities have an association, you can **Quick deploy with LLM**.


### Quick deploy with LLM

1. From the **Getting Started** menu, select **Train model**.
1. In the **Train your model**, select the **Quick deploy with LLM** button.
1. Complete the **Quick deploy with LLM** window fields as follows:

   * **Deployment name**. Give the deployment a name.
   * **Select Azure OpenAI Model Deployment**. Choose the Azure OpenAI model deployment that you created for this project.
   * **Deployment regions**. Select the region associated with the Azure Language resource.
1. Select the **Create** button. Foundry manages the configuration and deployment processes via back-end operations.

o    Use Quick Deploy to train and deploy the model.
o    Select your deployment name and model (e.g., GPT-4O).
o    Foundry handles configuration and deployment behind the scenes.


### Test in playground

1. From the **Getting Started** menu, select **Deploy your model**.
1. In the main window, select your model.
1. From the main window, select the **Try in playground** button.
1. In the playground, select the **Conversational language understanding** tile.
1. Under the left **Configuration** menu in the main window, make sure the following fields are completed correctly:
   
   * **Project name**. The project name should be the one you created for this CLU fine-tuning project
   * **Deployment name**. The deployment name is the the name you assigned to your Open AI model
1. Finally, select the **Multi-turn** understanding checkbox.
1. Next, you're going to simulate a multi-turn dialog by entering the following:

   ```text
   User: Hello, I would like to book a flight.
   Agent: Hello!  On which day do you intend to travel?
   User: Tomorrow.
   Agent: What departure time would you prefer for your flight?   
   User: Anytime after 5:00 PM.
   ```
1. Select the **Run** button.
1. The model returns a response in both **Text** and **JSON** formats.
1. On the right, the **Details** menu, lists the **Top Intent** and detected **Entities**.

That's it! The multi-turn model creation a project is complete. You now know how to use slot filling to create a CLU model for multi-turn interactions.

## Clean up resources

To clean up and remove an Azure AI resource, you can delete either the individual resource or the entire resource group. If you delete the resource group, all resources contained within are also deleted.

## Related content

[Learn more abut how CLU handles entity slot-filling across multi-turn conversations](../concepts/multi-turn-conversations.md)