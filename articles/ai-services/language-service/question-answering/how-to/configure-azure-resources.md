---
title: Configure the custom question answering service for fine-tune models
description: This article details Azure AI resource configurations for custom question answering fine-tune models.
ms.service: azure-ai-language
ms.topic: how-to
author: laujan
ms.author: lajanuar
ms.date: 11/18/2025
ms.custom: language-service-question-answering
---
# Configure your environment for Azure AI resources

In this guide, we walk you through configuring your Azure AI resources and permissions for custom question and answering projects, enabling you to fine-tune models with Azure AI Search and Custom Question Answering (CQA). Completing this setup is essential for fully integrating your environment with Foundry Tools resources. You only need to perform this setup once—afterward, you have seamless access to advanced, AI-powered question answering capabilities.

In addition, we show you how to assign the correct roles and permissions within the Azure portal. These steps help you get started quickly and effectively with Azure Language in Foundry Tools.

## Prerequisites

Before you can set up your resources, you need:

* **An active Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](../../../openai/how-to/role-based-access-control.md#cognitive-services-contributor).
*   A [Microsoft Foundry resource](../../../multi-service-resource.md) or a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
*   An [Azure AI Search resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.Search) (required for accessing CQA)


> [!NOTE]
>
> We highly recommend that you use a Foundry resource in the Foundry; however,  you can also follow these instructions using a Language resource.

## Step 1: Assign the correct role to your Search resource

Azure RBAC is an authorization system built on Azure Resource Manager. It provides fine-grained access management to Azure resources.

1. Navigate to the [Azure portal](https://azure.microsoft.com/#home).

1. Go to your Azure Search resource. (See **All resources** to find your Search resource.)

1. In the Settings section on the left panel, select **Keys**.

1. Make sure the **API Access control** button is set to **API keys**.

   :::image type="content" source="../media/configure-resources/api-access-control.png" alt-text="Screenshot of API access control selector in the Azure portal."::: 

1. Next, select **Access Control (IAM)** on the left panel, then select **Add role assignment**.

   :::image type="content" source="../media/configure-resources/add-role-assignment.png" alt-text="Screenshot of add role assignment selector in the Azure portal.":::

1. Search and select the **Azure AI Administrator** role. Select **Next**.

   :::image type="content" source="../media/configure-resources/azure-ai-administrator.png" alt-text="Screenshot of Azure AI Administrator from the job function roles list in the Azure portal." lightbox="../media/configure-resources/azure-ai-administrator.png":::

1. Navigate to the **Members** tab and then select **Assign access to User, group, or service principal**.

   :::image type="content" source="../media/configure-resources/user-group-service-principal.png" alt-text="Screenshot of assign member access selector in the Azure portal.":::

1. Select **Select members**, then add your account name, and choose **Select**.

1. Finally, select **Review + assign** to confirm your selection.

## Step 2: Configure connections in Foundry

Foundry offers a unified platform where you can easily build, manage, and deploy AI solutions using a wide range of models and tools. Connections enable authentication and access to both Microsoft and external resources within your Foundry projects.

1. Sign **into** [Foundry](https://ai.azure.com/) using your account and required subscription. Then, select the project containing your Foundry resource.

1. Next, navigate to the **Management Center** in the bottom left corner of the page.

1. Scroll to the **Connected resources** section of the Management center.

   :::image type="content" source="../media/configure-resources/ai-foundry-management-center.png" alt-text="Screenshot of the management center selector in the Foundry.":::

1. Select the  **+ New connection** button.

   :::image type="content" source="../media/configure-resources/new-connection.png" alt-text="Screenshot of the new connection button in the Foundry.":::

1. In the new window, select **Azure AI Search** as the resource type.

1. Search for and display the Azure AI Search resource you connected in [Step 1](#step-1-assign-the-correct-role-to-your-search-resource).

1. Ensure the Authentication is set to **API key**.

1. Select **Add connection** then select **Close**.

   :::image type="content" source="../media/configure-resources/connect-azure-search.png" alt-text="Screenshot of connect search resource selector in the Foundry.":::

## Step 3: Create a fine-tuning task with connected resources

1. Navigate to **Go to project** at the end of the left navigation pane.

   :::image type="content" source="../media/configure-resources/go-to-project.png" alt-text="Screenshot the go-to-project button in the Foundry.":::

1. Select **Fine-tuning** from the left navigation pane, choose the **AI Service fine-tuning** tab, and then select the **+ Fine-tune** button.

   :::image type="content" source="../media/configure-resources/fine-tuning.png" alt-text="Screenshot of the fine tuning selector in the Foundry.":::

1. Choose **Custom question answering** as the task type from the new window, then select **Next**.

1. Under **Connected service**, select your selected Foundry resource. Then select your newly connected search resource.

1. Your resources are now set up properly. Continue with setting up the fine-tuning task and customizing your CQA project.

## Change Azure AI Search resource

> [!WARNING]
> If you change the Azure Search service associated with your language resource, you lose access to all the projects already present in it. Make sure you export the existing projects before you change the Azure Search service.

If you create a language resource and its dependencies (such as Search) through the Azure portal, a Search service is created for you and linked to the language resource. After these resources are created, you can update the Search resource in the **Features** tab.

1.  Go to your language resource in the Azure portal.

1.  Select **Features** and select the Azure AI Search service you want to link with your language resource.

    > [!NOTE]
    > Your Language resource retains your Azure AI Search keys. If you update your search resource (for example, regenerating your keys), you need to select **Update Azure AI Search keys for the current search service**.

    > [!div class="mx-imgBorder"]
    > ![Add QnA to TA](../media/configure-resources/update-custom-feature.png)

1.  Select **Save**.

## Next Steps

[Create, test, and deploy a custom question answering project](create-test-deploy.md)
