---
title: Using Azure resources in custom NER
titleSuffix: Azure AI services
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/21/2024
ms.author: jboback
---


### Create a new Language resource using PowerShell

You can create a new resource and a storage account using the following CLI [template](https://github.com/Azure-Samples/cognitive-services-sample-data-files) and [parameters](https://github.com/Azure-Samples/cognitive-services-sample-data-files) files, which are hosted on GitHub.

Edit the following values in the parameters file:

| Parameter name | Value description |
|--|--|
|`name`| Name of your Language resource|
|`location`| Region in which your resource is hosted. for more information, see [Service limits](../service-limits.md#regional-availability).|
|`sku`| [Pricing tier](../service-limits.md#language-resource-limits) of your resource. |
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

See the ARM template documentation for information on [deploying templates](/azure/azure-resource-manager/templates/deploy-powershell#json-parameter-files) and [parameter files](/azure/azure-resource-manager/templates/parameter-files#parameter-file).
