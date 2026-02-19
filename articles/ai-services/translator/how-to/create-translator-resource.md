---
title: Create and configure Azure resources for Translator
titleSuffix: Foundry Tools
description: Learn how to create and configure Azure resources for translation services.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 11/18/2025
ms.service: azure-ai-translator
ms.topic: how-to

---

# Azure resources for Translator

Azure Translator in Foundry Tools is a cloud-based neural machine translation (NMT) service that allows you to add multilingual capabilities to your applications and workflows. The service supports both instant translation and batch processing, making it suitable for a wide range of business needs.

If you already have an Azure Translator or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Translator resources within the Microsoft Foundry portal for NMT deployment. For more information, *see* [How to use Foundry Tools](../../connect-services-foundry-portal.md).

By default, Azure Translator utilizes neural Machine Translation (NMT) technology. With the newest preview release, you now can optionally select either the standard NMT translation or one of two Large Language Model (LLM) deployment types: GPT-4o-mini or GPT-4o. However, **using an LLM model requires you to have a Foundry resource**.

The following table provides an overview of the resource solutions for Translator within the Azure AI ecosystem:

|Foundry Tool|Scope|Use cases|
|---------|------------|---------|
| [Foundry resource](/azure/ai-foundry/what-is-foundry) |This resource type is the recommended resource for building, deploying, and managing generative AI applications and agents in Foundry. |The Foundry resource is suitable for scenarios requiring orchestration of multiple AI models, custom AI agent development, and advanced AI application lifecycle management. |
|[Foundry Tools resource](../../../ai-services/what-are-ai-services.md)|This multi-service resource provides prebuilt, ready-to-use AI models accessible through APIs for tasks like translation, language understanding, speech recognition, and computer vision.|A Foundry Tools resource allows you to integrate advanced features such as text translation, speech transcription,  and image recognition into your applications. You can also enhance models within the Foundry portal using prebuilt AI capabilities.|
| [Azure Translator services resource](../overview.md) | The Azure Translator resource offers access to cloud-based neural machine translation capabilities and the ability to create customized translation models using Custom Translator.|  Azure Translator is production-ready and can seamlessly scale up or down based on translation needs, accommodating both small and large volumes of text or documents across multiple languages.|

## Step 1: create your resource

## [Foundry resource](#tab/foundry)

* A Foundry resource is your main tool for creating, deploying, and managing generative AI applications and agents. With this resource, you can access agent services, use models hosted in a serverless environment, run evaluations, and connect to the Azure OpenAI service.<br>

* If you plan to use an LLM model for translation, **you must use a Foundry resource**.<br>

* To learn how to create and manage a Foundry resource *see* [Create your first Foundry resource](../../../ai-services/multi-service-resource.md)

## [Azure Translator resource](#tab/translator)

An Azure Translator resource is an instance of the service that you create. All API requests to Foundry Tools can be accessed with an *endpoint* URL and a read-only *key* for authenticating access.

### Prerequisites

To get started, you need an active [**Azure account**](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

### Create your Azure Translator resource

With your Azure account, you can access the Translator through two different resource types:

* [**Single-service**](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation) resource types enable access to a single service API key and endpoint.

* [**Multi-service**](https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne) resource types enable access to multiple Foundry Tools by using a single API key and endpoint.

## Complete your project and instance details

After you decide which resource type you want use to access the Translator, you can enter the details for your project and instance.

1. **Subscription**. Select one of your available Azure subscriptions.

1. **Resource Group**. You can create a new resource group or add your resource to a preexisting resource group that shares the same lifecycle, permissions, and policies.

1. **Resource Region**. Choose **Global** unless your business or application requires a specific region. If you're planning on using the Document translation feature with [managed identity authorization](../document-translation/how-to-guides/create-use-managed-identities.md), choose a geographic region such as **East US**.

1. **Name**. Enter a name for your resource. The name you choose must be unique within Azure.

   > [!NOTE]
   > If you're using a Translator feature that needs a custom domain endpoint, such as Document translation, the input in the `name` field it the custom domain name parameter for the endpoint.
  > Make sure to enter the correct value in the `name` field to ensure proper functionality.

1. **Pricing tier**. Select a [pricing tier](https://azure.microsoft.com/pricing/details/cognitive-services/translator) that meets your needs:

   * Each subscription has a free tier.
   * The free tier has the same features and functionality as the paid plans and doesn't expire.
   * Only one free tier resource is available per subscription.
   * Document translation is supported in paid tiers. The Language Studio only supports the S1 or D3 instance tiers. If you just want to try Document translation, select the Standard S1 instance tier.

1. If you created a multi-service resource, the links at the bottom of the **Basics** tab provides technical documentation regarding the appropriate operation of the service.

1. Select **Review + Create**.

1. Review the service terms, and select **Create** to deploy your resource.

1. After your resource successfully deploys, select **Go to resource**.

### Authentication keys and endpoint URL

The quickest method for authenticating your Foundry Tools API requests is to include your endpoint URL and a read-only key in an authentication header. For more information, *see* [Authentication and authorization](../../authentication.md#authenticate-with-a-single-service-resource-key)

* **Authentication keys**. Your key is a unique string that's passed on every request to the Translation service. You can pass your key through a query-string parameter or by specifying it in the HTTP request header.

* **Endpoint URL**. Use the Global endpoint in your API request unless you need a specific Azure region or custom endpoint. For more information, see [Base URLs](../text-translation/reference/v3/reference.md#base-urls). The Global endpoint URL is `api.cognitive.microsofttranslator.com`.

### Get your authentication keys and endpoint

To authenticate your connection to your Translator resource, you need the key and endpoint for your resource.

1. After your new resource deploys, select **Go to resource** or go to your resource page.
1. In the left pane, under **Resource Management**, select **Keys and Endpoint**.
1. Copy and paste your keys and endpoint URL in a convenient location, such as Notepad.

:::image type="content" source="../media/keys-and-endpoint-resource.png" alt-text="Screenshot of the Azure portal showing the Keys and Endpoint page of a Translator resource. The keys and endpoints are highlighted.":::

### Create a Text translation client

Text translation supports both [global and regional endpoints](#complete-your-project-and-instance-details). Once you have your [authentication keys](#authentication-keys-and-endpoint-url), you need to create an instance of the `TextTranslationClient`, using an `AzureKeyCredential` for authentication, to interact with the Text translation service:

* To create a `TextTranslationClient` using a global resource endpoint, you need your resource **API key**:

    ```bash
      AzureKeyCredential credential = new('<apiKey>');
      TextTranslationClient client = new(credential);
    ```

* To create a `TextTranslationClient` using a regional resource endpoint, you need your resource **API key** and the name of the **region** where your resource is located:

    ```bash
     AzureKeyCredential credential = new('<apiKey>');
     TextTranslationClient client = new(credential, '<region>');
    ```

## Get started with Azure Translator REST APIs

In our quickstart, learn how to use the Translator with REST APIs.

> [!div class="nextstepaction"]
> [Get Started with the Translator](../text-translation/quickstart/rest-api.md)

---

## Step 2: configure your resources for Foundry

Completing this setup is essential for fully integrating your environment with Foundry. You only need to perform this setup once—afterward, you have seamless access to advanced, AI-powered question answering capabilities.

In addition, we show you how to assign the correct roles and permissions within the Azure portal. These steps help you get started quickly and effectively with Azure Translator.

## Prerequisites

Before you can set up your environment, you need:

* **An active Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](../../openai/how-to/role-based-access-control.md#cognitive-services-contributor).
* A [Foundry multi-service resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) or an [Azure Translator resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation).

> [!NOTE]
>
> We highly recommend that you use a Foundry resource in the Foundry; however, you can also follow these instructions using an Azure Translator resource.


Foundry offers a unified platform for building, managing, and deploying AI solutions with a wide array of models and tools. With this integration, you gain access to features to expand your training data with generative AI. New features are continually added, making Foundry the recommended choice for scalable Translator solutions.

1. Navigate to the [Azure portal](https://azure.microsoft.com/#home).

1. Go to your Foundry resource (select **All resources** to locate your Foundry or Azure Translator resource).

1. Next, select **Access Control (IAM)** on the left panel, then select **Add role assignment**.

   :::image type="content" source="../media/configure-resources/add-role-assignment.png" alt-text="Screenshot of add role assignment selector in the Azure portal.":::

1. Search and select the **Cognitive Services User** role. Select **Next**.

   :::image type="content" source="../media/configure-resources/cognitive-services-user.png" alt-text="Screenshot of Cognitive Services User from the job function roles list in the Azure portal.":::

1. Navigate to the **Members** tab and then select **Managed Identity**.

   :::image type="content" source="../media/configure-resources/managed-identity.png" alt-text="Screenshot of assign member access selector in the Azure portal.":::

1. Select **Select members**, then in the right panel, search for and choose your Foundry resource (the one you're using for this project), and choose **Select**.

1. Finally, select **Review + assign** to confirm your selection.

1. Your resources are now set up properly. Continue with setting up the fine-tuning task and continue customizing your Azure Translator projects.

### Step 3 (optional): clean up resource

If you want to clean up and remove an Azure resource, you can delete the resource or resource group. 

> [!WARNING]
>
> Deleting a resource group also deletes all resources contained in the group.

To delete the resource:

1. Search and select **Resource groups** in the Azure portal, and select your resource group.
1. Select the resources to be deleted by selecting the adjacent check box.
1. Select **Delete** from the top menu near the right edge.
1. Enter *delete* in the **Delete Resources** dialog box.
1. Select **Delete**.

To delete the resource group:

1. Go to your Resource Group in the Azure portal.
1. Select **Delete resource group** from the top menu bar.
1. Confirm the deletion request by entering the resource group name and selecting **Delete**.

## Next Steps

Learn more about Azure Translator features:

* [Text translation](../text-translation/overview.md)
* [Document translation](../document-translation/overview.md)
* [Custom Translation](../custom-translator/overview.md)
