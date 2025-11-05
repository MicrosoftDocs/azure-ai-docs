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
*  An [**Azure AI Language resource with a storage account**](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics). On the **select additional features** page, select the **Custom text classification, Custom named entity recognition, Custom sentiment analysis & Custom Text Analytics for health** box to link a required storage account to this resource:

    :::image type="content" source="../media/select-additional-features.png" alt-text="Screenshot of the select additional features option in the Azure AI Foundry.":::

* **A Foundry project created in the Azure AI Foundry**. For more information, *see* [Create an AI Foundry project](/azure/ai-foundry/how-to/create-projects).

     > [!NOTE]
     >  * You need to have an **owner** role assigned on the resource group to create a Language resource.
     >  * If you're connecting a preexisting storage account, you should have an owner role assigned to it.
     >  * Don't move the storage account to a different resource group or subscription once linked with the Language resource.

## Configure required roles, permissions, and settings

Let's begin by configuring your resources:

### Add required roles for your Azure AI Language resource

1. From the Language resource page in the [Azure portal](https://portal.azure.com/), select **Access Control (IAM)** in the left pane.
1. Select **Add** to **Add Role Assignments**, and add **Cognitive Services Language Owner** or **Cognitive Services Contributor** role assignment for your Language resource.
1. Within **Assign access to**, select **User, group, or service principal**.
1. Select **Select members**.
1. Select ***your user name***. You can search for user names in the **Select** field. Repeat this step for all roles.
1. Repeat these steps for all the user accounts that need access to this resource.

### Add required roles for your storage account

1. Go to your storage account page in the [Azure portal](https://portal.azure.com/).
1. Select **Access Control (IAM)** in the left pane.
1. Select **Add** to **Add Role Assignments**, and choose the **Storage blob data contributor** role on the storage account.
1. Within **Assign access to**, select **Managed identity**.
1. Select **Select members**.
1. Select your subscription, and **Language** as the managed identity. You can search for your language resource in the **Select** field.

### Add required user roles

> [!IMPORTANT]
> If you skip this step, you get a 403 error when you try to connect to your custom project. It's important that your current user has this role to access storage account blob data, even if you're the owner of the storage account.
>

1. Go to your storage account page in the [Azure portal](https://portal.azure.com/).
1. Select **Access Control (IAM)** in the left pane.
1. Select **Add** to **Add Role Assignments**, and choose the **Storage blob data contributor** role on the storage account.
1. Within **Assign access to**, select **User, group, or service principal**.
1. Select **Select members**.
1. Select your User. You can search for user names in the **Select** field.

> [!IMPORTANT]
> If you have a Firewall or virtual network or private endpoint, be sure to select **Allow Azure services on the trusted services list to access this storage account** under the **Networking tab** in the Azure portal.

   :::image type="content" source="../media/allow-azure-services.png" alt-text="Screenshot of allow Azure services enabled in Azure AI Foundry.":::



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

## Deploy an OpenAI model in Azure AI Foundry (required)

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

With your Language resource, storage account OpenAI deployment in place, you're ready to begin building your model.

### Create a CLU Project
*    Navigate to Foundry Classic and create a new CLU project.

### Add intents

o    Define intents relevant to your scenario (e.g., BookFlight, FlightStatus).
o    Provide descriptions for each intent because quick deploy requires them.


### Add entities

o    Go to the Entities tab and create entities like TravelDate, FlightNumber, TimeOfFlight.
o    Use prebuilt types for common data (e.g., DateTime for travel date).


### Associate intents with entities

o    In the Associations view, link each intent to its required entities: 
    BookFlight → TravelDate
    FlightStatus → FlightNumber
o    This ensures the bot knows which slots to fill for each intent.


### Quick deploy

o    Use Quick Deploy to train and deploy the model.
o    Select your deployment name and model (e.g., GPT-4O).
o    Foundry handles configuration and deployment behind the scenes.


### Test in playground

o    Enable Conversation-Level Understanding.
o    Simulate a multi-turn dialog (e.g., "I want to book a flight" → "What day?" → "Tomorrow").
o    Verify that the API returns intents and slot-filled entities in JSON.

