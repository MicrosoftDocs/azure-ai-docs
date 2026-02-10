---
title: Azure Content Understanding in Foundry Tools Disaster recovery
titleSuffix: Foundry Tools
description: Learn about disaster recovery features in Azure Content Understanding.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.custom:
  - build-2025
---

<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD033 -->

# Content Understanding disaster recovery

## Copy API overview

The process for copying an analyzer across regions consists of the following steps:

1. First you issue a copy authorization request to the source resource&mdash;the resource that contains the model to be copied. You receive back the authorization token.
1. Next you send the copy request to the target resource&mdash;that is, the resource that receives the copied model, along with the authorization token.

## Generate copy authorization request

In this operation, you can optionally specify `target` to lock the key to a specific target resource. The authorization token expires in 24 hours.

You can also optionally specify `encryptionKey` to encrypt the authorization token so it can only be used with the corresponding `decryptionKey`. The authorization token includes the source, optional target, and other metadata.

```http
POST {sourceEndpoint}/contentunderstanding/analyzers/{sourceAnalyzerId}:getCopyAuthorization
```

Request body

```json
{
  "target": "https://{targetEndpoint}/contentunderstanding/analyzers/{targetAnalyzerId}",
  "encryptionKey": "{encryptionKey}"
}
```

You receive a `200` response code with a response body that contains the authorization token.

```json
{
  "source": "https://{sourceEndpoint}/contentunderstanding/analyzers/{sourceAnalyzerId}",
  "authorizationToken": "{authorizationToken}",
  "expiresAt": "{expirationDateTime}",
  // "target": "https://{targetEndpoint}/contentunderstanding/analyzers/{targetAnalyzerId}"  // If specified, this is optional
}
```

## Start Copy operation

If you used `encryptionKey` when generating the authorization token, you must specify the corresponding `decryptionKey`. The target resource needs role-based access control (RBAC) access to the source resource, or you must provide an `authorizationToken` for the remote source analyzer.

By default, copied analyzers link to model deployments with the same name in the target resource as the source analyzer. You can override deployment names in the `:copy` request JSON.

If the target resource doesn't contain the named model deployments, the copy fails. The target embedding model must match the source embedding model, or the service returns a 400 error. If the target `chatCompletion` model is different from the source `chatCompletion` model, the service returns a warning.

```http
POST {targetEndpoint}/contentunderstanding/analyzers/{targetAnalyzerId}:copy
```

The body of your request is the response from the previous step.

```json
{
  "source": "https://{sourceEndpoint}/contentunderstanding/analyzers/{sourceAnalyzerId}",
  "authorizationToken": "{authorizationToken}"
  // "decryptionKey": "{decryptionKey}"

  // Optionally override model deployment information.
  "deployments": {
    "chatCompletion": "sourceChatCompletionDeployment"
  }
}
```
You receive a `200` response code with response body that contains the details.

```http
Operation-Location: {targetEndpoint}/contentunderstanding/analyzers/{targetAnalyzerId}/operations/{operationId}?api-version=...
```

```json
{
  "analyzerId": "{targetAnalyzerId}",
  "status": "creating",
}
```

<!-- > [!NOTE]
> The Copy API transparently supports the [AEK/CMK](https://msazure.visualstudio.com/Cognitive%20Services/_wiki/wikis/Cognitive%20Services.wiki/52146/Customer-Managed-Keys) feature. This action doesn't require any special treatment, but note that if you're copying between an unencrypted resource to an encrypted resource, you need to include the request header `x-ms-forms-copy-degrade: true`. If this header isn't included, the copy operation fails and returns a `DataProtectionTransformServiceError`. -->


## Next steps

In this guide, you learned how to use the Copy API to back up your custom models to a secondary Content Understanding resource. Next, explore the API reference docs to see what else you can do with Content Understanding.

* [REST API reference documentation](/rest/api/contentunderstanding/operation-groups)
