---
title: Configure the conversational language understanding  service for fine-tune models
description: This article details Azure AI resource configurations for conversational language understanding fine-tune models.
ms.service: azure-ai-language
ms.topic: how-to
author: laujan
ms.author: lajanuar
ms.date: 06/25/2025
ms.custom: language-service-question-answering
---

# Configure your environment for Azure AI resources and permissions

In this guide, we walk you through configuring your Azure AI resources and permissions for conversational language understanding (CLU) projects. We present two options:

* [**Option 1: Configure an Azure AI Foundry resource**](#option-1-configure-an-azure-ai-foundry-resource). Azure AI Foundry offers a unified environment for building generative AI applications and using Azure AI services. All essential tools are together in one environment for all stages of AI app development.

* [**Option 2: Configure Azure Language and Azure OpenAI resources**](#option-2-configure-azure-language-resource-and-azure-openai-resources). Azure OpenAI allows users to access OpenAI's language models within the Azure platform, providing security, regulatory compliance, and integration with other Azure services.

Completing these setups is essential for fully integrating your environment with Azure AI Services. You only need to perform this setup once—afterward, you have seamless access to advanced, AI-powered conversational language understanding capabilities.

In addition, we show you how to assign the correct roles and permissions within the Azure portal. These steps help you get started quickly and effectively with Azure AI Language.

## Prerequisites

Before you can set up your resources, you need:

* **An active Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/free/cognitive-services).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](../../../openai/how-to/role-based-access-control.md#cognitive-services-contributor).
* An [Azure AI Foundry multi-service resource](../../../multi-service-resource.md) or an [Azure AI Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).

* An [Azure OpenAI resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI) (optional but required for [option 2](#option-2-configure-azure-language-resource-and-azure-openai-resources))

> [!NOTE]
>
> We highly recommend that you use an Azure AI Foundry resource in the AI Foundry; however, you can also follow these instructions using a Language resource.

## Option 1: Configure an Azure AI Foundry resource

Azure AI Foundry offers a unified platform for building, managing, and deploying AI solutions with a wide array of models and tools. With this integration, you gain access to features like **Quick Deploy** for rapid model **fine-tuning** and **suggest utterances** to expand your training data with generative AI. New features are continually added, making Azure AI Foundry the recommended choice for scalable CLU solutions.

1. Navigate to the [Azure portal](https://azure.microsoft.com/#home).

1. Go to your Azure AI Foundry resource (select **All resources** to locate your resource).

1. Next, select **Access Control (IAM)** on the left panel, then select **Add role assignment**.

   :::image type="content" source="../media/configure-resources/add-role-assignment.png" alt-text="Screenshot of add role assignment selector in the Azure portal.":::

1. Search and select the **Cognitive Services User** role. Select **Next**.

   :::image type="content" source="../media/configure-resources/cognitive-services-user.png" alt-text="Screenshot of Cognitive Services User from the job function roles list in the Azure portal.":::

1. Navigate to the **Members** tab and then select **Managed Identity**.

   :::image type="content" source="../media/configure-resources/managed-identity.png" alt-text="Screenshot of assign member access selector in the Azure portal.":::

1. Select **Select members**, then in the right panel, search for and choose your Azure AI Foundry resource (the one you're using for this project), and choose **Select**.

1. Finally, select **Review + assign** to confirm your selection.

1. Your resources are now set up properly. Continue with setting up the fine-tuning task and continue customizing your CLU project.

## Option 2: Configure Azure Language resource and Azure OpenAI resources

Azure OpenAI is a cloud-based solution that brings the advanced capabilities of OpenAI's language models to the Azure platform. With this service, you can easily incorporate natural language processing features into your applications without extensive AI or machine learning expertise. 

##### Step 1: Assign the correct role to the Azure OpenAI resource

1. Navigate to the [Azure portal](https://azure.microsoft.com/#home).

1. Go to your Azure OpenAI resource. (select **All resources** to locate your resource).

1. Next, select **Access Control (IAM)** on the left panel, then select **Add role assignment**.

   :::image type="content" source="../media/configure-resources/add-role-assignment.png" alt-text="Screenshot of add role assignment selector in the Azure portal.":::

1. Search and select the **Cognitive Services User** role, then select **Next**.

   :::image type="content" source="../media/configure-resources/cognitive-services-user.png" alt-text="Screenshot of Cognitive Services User from the job function roles list in the Azure portal.":::

1. Navigate to the **Members** tab and then select **Managed Identity**.

   :::image type="content" source="../media/configure-resources/managed-identity.png" alt-text="Screenshot of assign member access selector in the Azure portal.":::

1. Select **Select members**, then in the right panel, search for and choose your Azure AI Foundry resource (the one you're using for this project), and choose **Select**.

1. Finally, select **Review + assign** to confirm your selection.


##### Step 2: Configure connections in AI Foundry

Azure AI Foundry offers a unified platform where you can easily build, manage, and deploy AI solutions using a wide range of models and tools. Connections enable authentication and access to both Microsoft and external resources within your Azure AI Foundry projects.

1. Sign into [Azure AI Foundry](https://ai.azure.com/) using your account and required subscription. Then, select the project containing your desired Azure AI Foundry resource.

1. Next, navigate to the **Management Center** in the bottom left corner of the page.

1. Scroll to the **Connected resources** section of the Management center.

    :::image type="content" source="../media/configure-resources/ai-foundry-management-center.png" alt-text="Screenshot of the management center selector in the Azure AI Foundry.":::


1. Select the  **+ New connection** button.

   :::image type="content" source="../media/configure-resources/new-connection.png" alt-text="Screenshot of the new connection button in the Azure AI Foundry.":::


1. In the new window, select **Azure AI Language** as the resource type, then find your Azure AI Language resource.

1. Select **Add connection** in the corner of your selected Azure AI Language resource.

1. Select **Azure OpenAI** as the resource type, then find your desired Azure OpenAI resource.

1. Ensure **Authentication** is set to **API key**.

1. Select **Add connection**, then select **Close**.

   :::image type="content" source="../media/configure-resources/connect-language-resource.png" alt-text="Screenshot of connect search resource selector in the Azure AI Foundry.":::

1. Your resources are now set up properly. Continue with setting up the fine-tuning task and customizing your CLU project.

## Next Steps

[Create a CLU fine-tuning task](train-model.md#train-your-model)

