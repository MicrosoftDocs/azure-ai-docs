---
title: 'Create and manage Azure OpenAI in Microsoft Foundry Models deployments in the Azure portal'
titleSuffix: Azure OpenAI
description: Learn how to use the Azure portal to create an Azure OpenAI resource and manage deployments with the Azure OpenAI.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 05/20/2024
---

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Access permissions to [create Azure OpenAI resources and to deploy models](../how-to/role-based-access-control.md).

## Create a resource

The following steps show how to create an Azure OpenAI resource in the Azure portal. 

### Identify the resource

1. Sign in with your Azure subscription in the Azure portal.

1. Select **Create a resource** and search for the **Azure OpenAI**. When you locate the service, select **Create**.

   :::image type="content" source="../media/create-resource/create-azure-openai-resource-portal.png" alt-text="Screenshot that shows how to create a new Azure OpenAI in Microsoft Foundry Models resource in the Azure portal.":::

1. On the **Create Azure OpenAI** page, provide the following information for the fields on the **Basics** tab:

   | Field | Description |
   |---|---|
   | **Subscription** | The Azure subscription used in your Azure OpenAI onboarding application. |
   | **Resource group** | The Azure resource group to contain your Azure OpenAI resource. You can create a new group or use a pre-existing group. |
   | **Region** | The location of your instance. Different locations can introduce latency, but they don't affect the runtime availability of your resource. |
   | **Name** | A descriptive name for your Azure OpenAI resource, such as _MyOpenAIResource_. |
   | **Pricing Tier** | The pricing tier for the resource. Currently, only the Standard tier is available for the Azure OpenAI. For more info on pricing visit the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) |

   :::image type="content" source="../media/create-resource/create-resource-basic-settings.png" alt-text="Screenshot that shows how to configure an Azure OpenAI resource in the Azure portal.":::

1. Select **Next**.

### Configure network security

The **Network** tab presents three options for the security **Type**:
   
- Option 1: **All networks, including the internet, can access this resource.**
- Option 2: **Selected networks, configure network security for your Foundry Tools resource.**
- Option 3: **Disabled, no networks can access this resource. You could configure private endpoint connections that will be the exclusive way to access this resource.**

:::image type="content" source="../media/create-resource/create-resource-network-settings.png" alt-text="Screenshot that shows the network security options for an Azure OpenAI resource in the Azure portal.":::

Depending on the option you select, you might need to provide additional information.

#### Option 1: Allow all networks

The first option allows all networks, including the internet, to access your resource. This option is the default setting. No extra settings are required for this option.

#### Option 2: Allow specific networks only

The second option lets you identify specific networks that can access your resource. When you select this option, the page updates to include the following required fields:

| Field | Description |
|---|---|
| **Virtual network** | Specify the virtual networks that are permitted access to your resource. You can edit the default virtual network name in the Azure portal. |
| **Subnets** | Specify the subnets that are permitted access to your resource. You can edit the default subnet name in the Azure portal. |

:::image type="content" source="../media/create-resource/create-resource-network-settings-specific.png" alt-text="Screenshot that shows how to configure network security for an Azure OpenAI resource to allow specific networks only.":::

The **Firewall** section provides an optional **Address range** field that you can use to configure firewall settings for the resource.

#### Option 3: Disable network access

The third option lets you disable network access to your resource. When you select this option, the page updates to include the **Private endpoint** table.

:::image type="content" source="../media/create-resource/create-resource-network-settings-disable.png" alt-text="Screenshot that shows how to disable network security for an Azure OpenAI resource in the Azure portal.":::

As an option, you can add a private endpoint for access to your resource. Select **Add private endpoint**, and complete the endpoint configuration.

### Confirm the configuration and create the resource

1. Select **Next** and configure any **Tags** for your resource, as desired.

1. Select **Next** to move to the final stage in the process: **Review + submit**.

1. Confirm your configuration settings, and select **Create**.

1. The Azure portal displays a notification when the new resource is available. Select **Go to resource**.

   :::image type="content" source="../media/create-resource/create-resource-go-to-resource.png" alt-text="Screenshot showing the Go to resource button in the Azure portal.":::

## Deploy a model

Before you can generate text or inference, you need to deploy a model. You can select from one of several available models in Foundry portal.

To deploy a model, follow these steps:

1. [!INCLUDE [classic-sign-in](../../includes/classic-sign-in.md)]
1. In **Keep building with Foundry** section select **View all resources**.
1. Find and select your resource.

    > [!IMPORTANT]
    > At this step you might be offered to upgrade your Azure OpenAI resource to Foundry. See comparison between the two resource types and details on resource upgrade and rollback at [this page](../../how-to/upgrade-azure-openai.md). Select **Cancel** to proceed without resource type upgrade. Alternately select **Next**.
    > 
    > See additional information about Foundry resource in [this article](../../../ai-services/multi-service-resource.md).

1. Select **Deployments** from **Shared resources** section in the left pane. (In case you upgraded to Foundry in the previous step, select **Models + endpoints** from **My assets** section in the left pane.)
1. Select **+ Deploy model** > **Deploy base model** to open the deployment window. 
1. Select the desired model and then select **Confirm**. For a list of available models per region, see [Model summary table and region availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#model-summary-table-and-region-availability).
1. In the next window configure the following fields:

   | Field | Description |
   |---|---|
   | **Deployment name** | Choose a name carefully. The deployment name is used in your code to call the model by using the client libraries and the REST APIs. |
   |**Deployment type** | **Standard**, **Global-Batch**, **Global-Standard**, **Provisioned-Managed**. Learn more about [deployment type options](../../foundry-models/concepts/deployment-types.md). |  
   | **Deployment details** (Optional) | You can set optional advanced settings, as needed for your resource. <br> - For the **Content Filter**, assign a content filter to your deployment.<br> - For the **Tokens per Minute Rate Limit**, adjust the Tokens per Minute (TPM) to set the effective rate limit for your deployment. You can modify this value at any time by using the [**Quotas**](../how-to/quota.md) menu. [**Dynamic Quota**](../how-to/dynamic-quota.md) allows you to take advantage of more quota when extra capacity is available. |

    > [!IMPORTANT]
    > When you access the model via the API, you need to refer to the deployment name rather than the underlying model name in API calls, which is one of the [key differences](../how-to/switching-endpoints.yml) between OpenAI and Azure OpenAI. OpenAI only requires the model name. Azure OpenAI always requires deployment name, even when using the model parameter. In our documentation, we often have examples where deployment names are represented as identical to model names to help indicate which model works with a particular API endpoint. Ultimately your deployment names can follow whatever naming convention is best for your use case.

1. Select **Deploy**.
1. Deployment **Details** shows all the information of your new deployment. When the deployment completes, your model **Provisioning** state changes to _Succeeded_.
