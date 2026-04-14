---
title: "How-to: Copy custom analyzers using the Content Understanding REST API"
author: PatrickFarley
manager: nitinme
description: Learn to copy custom analyzers with Content Understanding using the REST API.
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 01/29/2026
ms.author: pafarley
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

This guide shows you how to use the [Content Understanding REST API](/rest/api/contentunderstanding/content-analyzers?view=rest-contentunderstanding-2025-11-01&preserve-view=true) to copy custom analyzers within a resource and across Foundry resources.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](../../language-region-support.md).
* [cURL](https://everything.curl.dev/install/index.html) installed for your dev environment.
* An existing custom analyzer in your resource. See [Create a custom analyzer](../../tutorial/create-custom-analyzer.md) if you need to create one.

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

1. Call the [Grant Copy Authorization](/rest/api/contentunderstanding/content-analyzers/grant-copy-authorization?view=rest-contentunderstanding-2025-11-01) API on the source analyzer, providing the fully qualified resource ID of the copy target and the target region. The response contains a copy authorization token with an expiration time (`expiresAt`).
1. Copy the resulting response body and use it as the body of the copy request in the next step.
1. Call the copy API on the target resource, providing the fully qualified source resource ID, the source analyzer ID, and the source region.

> [!IMPORTANT]
> Both the source and target resources require the **Cognitive Services User** role to be granted to the credential used to run the code. This role is required for cross-resource copying operations.

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

## Verify the copy

You can validate that the analyzer was copied by calling the GET analyzer on the resource if this copy was within the resource, or on the target resource if this copy was across resources.

```http
GET https://{target resource}.services.ai.azure.com/contentunderstanding/analyzers/{target analyzer id}?api-version=2025-11-01
Ocp-Apim-Subscription-Key: {Auth key}

```
