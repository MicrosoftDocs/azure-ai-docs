---
titleSuffix: Foundry Tools
description: Learn about the steps for using Azure resources with custom named entity recognition (NER).
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
You can use an existing Language resource to get started with custom NER as long as this resource meets the below requirements:

|Requirement  |Description  |
|---------|---------|
|Regions     | Make sure your existing resource is provisioned in one of the [supported regions](../service-limits.md#regional-availability). If not, you need to create a new resource in one of these regions.        |
|Pricing tier     | Learn more about [supported pricing tiers](../service-limits.md#language-resource-limits).        |
|Managed identity     | Make sure that the resource's managed identity setting is enabled. Otherwise, read the next section. |

To use custom named entity recognition, you need to [create an Azure storage account](/azure/storage/common/storage-account-create) if you don't have one already. 

## Enable identity management for your resource

Your Language resource must have identity management, to enable it using the [Azure portal](https://portal.azure.com):

1. Go to your Language resource
2. From left hand menu, under **Resource Management** section, select **Identity**
3. From **System assigned** tab, make sure to set **Status** to **On**


### Enable custom named entity recognition feature

Make sure to enable **Custom text classification / Custom Named Entity Recognition** feature from Azure portal.

1. Go to your Language resource in the [Azure portal](https://portal.azure.com).
2. From the left side menu, under **Resource Management** section, select **Features**.
3. Enable **Custom text classification / Custom Named Entity Recognition** feature.
4. Connect your storage account.
5. Select **Apply**.

>[!Important]
 > Make sure that the user making changes the **storage blob data contributor** role assigned for them.

### Add required roles

[!INCLUDE [required roles](../includes/roles-for-resource-and-storage.md)]

### Enable CORS for your storage account

Make sure to allow (**GET, PUT, DELETE**) methods when enabling Cross-Origin Resource Sharing (CORS). 
Set allowed origins field to `https://language.cognitive.azure.com`. Allow all header by adding `*` to the allowed header values, and set the maximum age to `500`.

:::image type="content" source="../media/cors.png" alt-text="A screenshot showing how to use CORS for storage accounts." lightbox="../media/cors.png":::
