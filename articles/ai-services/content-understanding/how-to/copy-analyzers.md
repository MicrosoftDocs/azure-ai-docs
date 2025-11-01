---
title: Copy custom analyzers 
titleSuffix: Azure AI services
description: Copy custom analyzers within a resource and across Azure resources
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 09/16/2025
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - build-2025
---

# Copy Analyzers

All prebuilt analyzers in Content Understanding are available in every resource by default. Find the complete list of all [prebuilt analyzers here](/azure/)<!--TBD-->. Custom analyzers are analyzers you define to process a specific content where you define the content type, schema, and any other processing logic. For more information on defining a custom analyzer, see [defining a custom analyzer](/azure/)<!--TBD-->.

The copy operation on analyzers supports a few scenarios:
* **Copy within resource** to create a copy of an existing analyzer in the same resource as a backup or a version you can iteratively make changes from. 
* **Copy across resources** copy an analyzer from one AI Foundry resource to another. This supports failover scenarios and sharing of analyzers across teams.

> [!IMPORTANT]
>
> The copy operation for copying across resources supports copying analyzers across subscriptions and even Azure tenants.

## Copy within an AI Foundry resource

The copy operation within a Foundry resource is a simple, single step operation. Specify the analyzer you want to copy to as the resource you want to create and provide the analyzer you want to copy from in the request body. 

```
POST https://{resource}.ai.azure.com/contentunderstanding/analyzers/{targetAnalyzer}:copy?api-version=2025-11-01
Content-Type: application/json
Ocp-Apim-Subscription-Key: {Auth key}

{
  "sourceAnalyzerId": "{sourceAnalyzerId}"

}
```

## Copy across AI Foundry resources

Copying the analyzer across AI Foundry resources is a multi-step process because a service principal will likely not have permissions on both resources:

1. Start by obtaining a copy authorization on the source analyzer by providing the fully qualified resource ID for the copy target and the target region. 
2. Copy the resulting response and use it as the body of the next request.
3. Issue a copy request on the target resource providing the fully qualified source resource, the source analyzer ID, and the region.

```
POST https://{source resource}.services.ai.azure.com/contentunderstanding/analyzers/{source analyzer id}:grantCopyAuthorization?api-version=2025-11-01
Content-Type: application/json
Ocp-Apim-Subscription-Key: {Auth key}

{ 
  "targetAzureResourceId":"/subscriptions/{subscription guid}/resourceGroups/{resource group}/providers/Microsoft.CognitiveServices/accounts/{target resource}",
  "targetRegion":"{region}"
}


POST https://{target resource}.services.ai.azure.com/contentunderstanding/analyzers/{target analyzer id}:copy?api-version=2025-11-01
Content-Type: application/json
Ocp-Apim-Subscription-Key: {Auth key}

{
    "sourceAzureResourceId":"/subscriptions/{subscription guid}/resourceGroups/{resource group}/providers/Microsoft.CognitiveServices/accounts/{source resource}",
    "sourceAnalyzerId":"{source analyzer id}",
    "sourceRegion":"{region}"
}
```

 > [!NOTE]
>
> Analyzers now support classification/segmentation and analysis of each of the identified classes/segments in a single request. When copying an analyzer that uses this feature, you need to copy any analyzers referenced as well.

You can then validate that the analyzer was copied by calling the GET analyzer on the resource if this was a copy within the resource, or on the target resource, if this was a copy across resources.

```
GET https://mmi-usw3-eft-foundry.services.ai.azure.com/contentunderstanding/analyzers/{target analyzer id}?api-version=2025-11-01
Ocp-Apim-Subscription-Key: {Auth key}

```
