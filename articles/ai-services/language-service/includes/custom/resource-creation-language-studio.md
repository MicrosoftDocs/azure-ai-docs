---
titleSuffix: Azure AI services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 06/30/2025
ms.author: lajanuar
---


### Create a new Language resource from Language Studio

If it's your first time logging in, you'll see a window in [Language Studio](https://aka.ms/languageStudio) that will let you choose an existing Language resource or create a new one. You can also create a resource by clicking the settings icon in the top-right corner, selecting **Resources**, then clicking **Create a new resource**.

Create a Language resource with following details.

|Instance detail  |Required value  |
|---------|---------|
|Azure subscription| **Your Azure subscription**|
|Azure resource group| **Your Azure resource group**|
|Azure resource name| **Your Azure resource name**|
|Location | The region      |
|Pricing tier     | The pricing tier of your Language resource.        |

> [!IMPORTANT]
> * Make sure to enable **Managed Identity** when you create a Language resource. 
> * Read and confirm Responsible AI notice

To use this service, you'll need to [create an Azure storage account](/azure/storage/common/storage-account-create) if you don't have one already. 
