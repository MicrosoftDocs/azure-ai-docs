---
title: How to create custom text classification projects
titleSuffix: Azure AI services
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 06/30/2025
ms.author: lajanuar
---


You can create a new resource and a storage account using the following CLI [template](https://github.com/Azure-Samples/cognitive-services-sample-data-files) and [parameters](https://github.com/Azure-Samples/cognitive-services-sample-data-files) files, which are hosted on GitHub.

Edit the following values in the parameters file:

| Parameter name | Value description |
|--|--|
|`name`| Name of your Language resource|
|`location`| The region in which your resource is hosted. See [region support](../service-limits.md#regional-availability) for more information.|
|`sku`| The pricing tier of your resource. See [service limits](../service-limits.md#language-resource-limits) for more information. |
|`storageResourceName`| Name of your storage account|
|`storageLocation`| Region in which your storage account is hosted.|
|`storageSkuType`| SKU of your [storage account](/rest/api/storagerp/srp_sku_types).|
|`storageResourceGroupName`| Resource group of your storage account|

Use the following PowerShell command to deploy the Azure Resource Manager (ARM) template with the files you edited.

```powershell
New-AzResourceGroupDeployment -Name ExampleDeployment -ResourceGroupName ExampleResourceGroup `
  -TemplateFile <path-to-arm-template> `
  -TemplateParameterFile <path-to-parameters-file>
```

See the ARM template documentation for information on [deploying templates](/azure/azure-resource-manager/templates/deploy-powershell#json-parameter-files) and [parameter files](/azure/azure-resource-manager/templates/parameter-files?tabs=json).
