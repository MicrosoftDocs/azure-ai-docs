---
title: Copy custom analyzers
titleSuffix: Foundry Tools
description: Copy custom analyzers within a resource and across Azure resources.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - build-2025
---

# Copy custom analyzers

Every Content Understanding resource provides access to all prebuilt analyzers by default. For a complete list, see [prebuilt analyzers](../concepts/prebuilt-analyzers.md). Custom analyzers are analyzers you define to process specific content where you can define the content type, schema, and any other processing logic. For more information on defining a custom analyzer, see [defining a custom analyzer](./customize-analyzer-content-understanding-studio.md).

The copy operation on analyzers supports a few different scenarios:
* **Copy within a resource** to create a copy of an existing analyzer in the same resource as a backup or a version you can iterate on.
* **Copy across resources** to copy an analyzer from one Foundry resource to another. This supports failover scenarios and sharing analyzers across teams.

> [!IMPORTANT]
>
> The copy operation for copying across resources supports copying analyzers across subscriptions and even Azure tenants.

## Copy within a Foundry resource

The copy operation within a Foundry resource is a single-step operation. Specify the target analyzer ID in the request URL and provide the source analyzer ID in the request body.

```http
POST https://{resource}.ai.azure.com/contentunderstanding/analyzers/{targetAnalyzer}:copy?api-version=2025-11-01
Content-Type: application/json
Ocp-Apim-Subscription-Key: {Auth key}

{
  "sourceAnalyzerId": "{sourceAnalyzerId}"

}
```

## Copy across Foundry resources

Copying an analyzer across Foundry resources is a multi-step process because a service principal might not have permissions on both resources:

1. Get a copy authorization on the source analyzer by providing the fully qualified resource ID for the copy target and the target region. 
1. Copy the resulting response and use it as the body of the next request.
1. Issue a copy request on the target resource by providing the fully qualified source resource, the source analyzer ID, and the region.

```http
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
> Analyzers now support classification/segmentation and analysis of each of the identified classes and segments in a single request. When copying an analyzer that uses this feature, you need to copy any referenced analyzers as well.

You can then validate that the analyzer was copied by calling the GET analyzer on the resource if this copy was within the resource, or on the target resource if this copy was across resources.

```http
GET https://{target resource}.services.ai.azure.com/contentunderstanding/analyzers/{target analyzer id}?api-version=2025-11-01
Ocp-Apim-Subscription-Key: {Auth key}

```
