---
title: 'Quickstart: Document Intelligence Studio'
titleSuffix: Foundry Tools
description: Learn how to get started processing forms and documents by using Document Intelligence Studio.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: quickstart
ms.date: 11/18/2025
ms.author: lajanuar
monikerRange: '>=doc-intel-3.0.0'
---

<!-- markdownlint-disable MD001 -->

# Get started: Document Intelligence Studio

[Azure Document Intelligence in Foundry Tools Studio](https://formrecognizer.appliedai.azure.com/) is an online tool that you can use to visually explore, understand, and integrate features from the Document Intelligence service into your applications. You can get started by exploring the pretrained models with samples or your own documents. You can also create projects to build custom template models and reference the models in your applications.

## Prerequisites

* An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* An Azure Document Intelligence resource. After you have your Azure subscription, create a [single-service](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) or [Azure multiservice](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) resource in the Azure portal to get your key and endpoint.
* To try the service, use the free pricing tier (F0). You can upgrade later to a paid tier for production.

> [!TIP]
> Create a Microsoft Foundry resource if you plan to access multiple Foundry Tools under a single endpoint/key. For Document Intelligence access only, create a Document Intelligence resource. You need a single-service resource if you intend to use [Microsoft Entra authentication](/azure/active-directory/authentication/overview-authentication).
>
> Document Intelligence now supports Azure Active Directory token authentication in addition to local (key-based) authentication when you access Document Intelligence resources and storage accounts. Follow the instructions to set up correct access roles, especially if your resources are applied with the `DisableLocalAuth` policy.

There are added prerequisites for using custom models in Document Intelligence Studio. For step-by-step guidance, see [Document Intelligence Studio custom projects](studio-custom-project.md).

### Authorization policies

Your organization can opt to disable local authentication and enforce Microsoft Entra (formerly Azure Active Directory) authentication for Document Intelligence resources and Azure Blob Storage.

* Microsoft Entra authentication requires key-based authorization to be disabled. After key access is disabled, Microsoft Entra ID is the only available authorization method.
* Microsoft Entra allows granting minimum privileges and granular control for Azure resources.

For more information, see the following guidance:

  * [Disable local authentication for Foundry Tools](../../disable-local-auth.md)
  * [Prevent Shared Key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent)

If local (key-based) authentication is disabled for your Document Intelligence service resource, be sure to obtain the Cognitive Services User role and your Azure Active Directory token to authenticate requests in Document Intelligence Studio. The Contributor role allows you to list only keys but doesn't give you permission to use the resource when key access is disabled.

#### Designate role assignments

Document Intelligence Studio basic access requires the [Cognitive Services User](/azure/role-based-access-control/built-in-roles/ai-machine-learning#cognitive-services-user) role. For more information, see [Document Intelligence role assignments](try-document-intelligence-studio.md#azure-role-assignments).

* Make sure that you have the Cognitive Services User role and not the Cognitive Services Contributor role when you set up Microsoft Entra ID authentication:

   * **Cognitive Services User**: You need this role for the Document Intelligence or Microsoft Foundry resource to enter the analyze page.
   * **Contributor**: You need this role to create a resource group, Document Intelligence service, or Microsoft Foundry resource.
* In Azure context, the Contributor role can perform actions only to control and manage the resource itself, including listing the access keys.
* User accounts with a Contributor role can access the Document Intelligence service only by calling with access keys. When you set up access with Microsoft Entra ID, key access is disabled, and the Cognitive Services User role is required for an account to use the resources.

### Authentication in Document Intelligence Studio

Go to [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/). If it's your first time signing in, you're prompted to configure your service resource. In accordance with your organization's policy, you have the following options:

* Microsoft Entra authentication: Access by resource (recommended)

  1. Select your existing subscription.
  1. Select an existing resource group within your subscription or create a new one.
  1. Select your existing Document Intelligence or Microsoft Foundry resource.

     :::image type="content" source="../media/studio/configure-service-resource.png" lightbox="../media/studio/configure-service-resource.png" alt-text="Screenshot that shows configuring a service resource in Document Intelligence Studio.":::

* Local authentication: Access by API endpoint and key

  1. Retrieve your endpoint and key from the Azure portal.
  1. Go to the overview page for your resource, and on the left pane, select **Keys and Endpoint**.
  1. Enter values in the appropriate fields.

      :::image type="content" source="../media/studio/keys-and-endpoint.png" lightbox="../media/studio/keys-and-endpoint.png" alt-text="Screenshot that shows the Keys and Endpoint page in the Azure portal.":::

* After you validate the scenario in Document Intelligence Studio, use the [C#](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true), [Java](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true), [JavaScript](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true), or [Python](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true) client libraries or the [REST API](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true) to incorporate Document Intelligence models into your own applications.

### Try a Document Intelligence model

To learn more about the available Document Intelligence models, see [Document Intelligence model support](../studio-overview.md#document-intelligence-model-support).

* Try the different models that Document Intelligence Studio has to offer after you configure your resource. Select any Document Intelligence model to use it with a no-code approach.
* Test any of the document analysis or prebuilt models. Select the model, and use one of the sample documents or upload your own document to analyze. The analysis result appears in the pane on the right that shows content-result code.
* Train the custom models on your documents. For an overview of custom models, see [Custom models overview](../train/custom-model.md).
* Validate the scenario in Document Intelligence Studio. Then use the [C#](get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true), [Java](get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true), [JavaScript](get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true), or [Python](get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) client libraries or the [REST API](get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) to incorporate Document Intelligence models into your own applications.

#### View resource details

 To view resource details such as name and pricing tier, select the **Settings** icon in the upper-right corner of the Document Intelligence Studio home page, and then select the **Resource** tab. If you have access to other resources, you can also switch resources.

:::image type="content" source="../media/studio/form-recognizer-studio-resource-page.png" lightbox="../media/studio/form-recognizer-studio-resource-page.png" alt-text="Screenshot that shows the Settings page Resource tab.":::

With Document Intelligence, you can quickly automate your data processing in applications and workflows, easily enhance data-driven strategies, and skillfully enrich document search capabilities.

#### Manage non-Microsoft settings for Document Intelligence Studio access

##### Microsoft Edge

1. Go to **Settings** for Microsoft Edge.
1. Search for **third-party**.
1. Go to **Manage and delete cookies and site data**.
1. Turn off the setting of **Block third-party cookies**.

##### Chrome

1. Go to **Settings** for Chrome.
1. Search for **Third-party**.
1. Under **Default behavior**, select **Allow third-party cookies**.

##### Firefox

1. Go to **Settings** for Firefox.
1. Search for **cookies**.
1. Under **Enhanced Tracking Protection**, select **Manage Exceptions**.
1. Add an exception for `https://documentintelligence.ai.azure.com` or the Document Intelligence Studio URL of your environment.

##### Safari

1. Select **Safari** > **Preferences**.
1. Select **Privacy**.
1. Clear **Block all cookies**.

### Troubleshooting

|Scenario     |Cause| Resolution|
|-------------|------|----------|
|You receive the error message</br> `Form Recognizer Not Found` when you open a custom project.|Your Document Intelligence resource, which is bound to the custom project, was deleted or moved to another resource group.| There are two ways to resolve this problem: </br>&bullet; Re-create the Document Intelligence resource under the same subscription and resource group with the same name.</br>&bullet; Re-create a custom project with the migrated Document Intelligence resource and specify the same storage account.|
|You receive the error message</br> `PermissionDenied` when you use prebuilt apps or open a custom project.|The principal doesn't have access to the API or operation when it analyzes against prebuilt models or opens a custom project. It's likely that the local (key-based) authentication is disabled for your Document Intelligence resource, and you don't have enough permission to access the resource.|To configure your access roles, see [Azure role assignments](try-document-intelligence-studio.md#azure-role-assignments).|
|You receive the error message</br> `AuthorizationPermissionMismatch` when you open a custom project.|The request isn't authorized to perform the operation by using the designated permission. It's likely that the local (key-based) authentication is disabled for your storage account, and you don't have the granted permission to access the blob data.|To configure your access roles, see [Azure role assignments](try-document-intelligence-studio.md#azure-role-assignments).|
|You can't sign in to Document Intelligence Studio and receive the error message</br> `InteractionRequiredAuthError:login_required:AADSTS50058:A silent sign-request was sent but no user is signed in`.|It's likely that your browser is blocking non-Microsoft cookies, so you can't successfully sign in.|To resolve this issue, see [Manage non-Microsoft settings](#manage-non-microsoft-settings-for-document-intelligence-studio-access) for your browser.|

## Related content

* [Learn how to create custom projects in Document Intelligence Studio](studio-custom-project.md)
* [Get started with Document Intelligence client libraries](get-started-sdks-rest-api.md)
