---
title: Azure Content Understanding in Foundry Tools Disaster recovery
titleSuffix: Foundry Tools
description: Learn about disaster recovery features in Azure Content Understanding.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 09/16/2025
ms.service: azure-ai-content-understanding
ms.topic: article
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

## Generate Copy authorization request

In this operation, target can be optionally specified to lock the key to the specific target resource. This authorization token expires in 24 hours. `encryptionKey` can be optionally specified to double encrypt the authorization token such that it can only be used with a corresponding decryptionKey. Authorization token encrypts the source, optional target, and other metadata.

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

You receive a `200` response code with response body that contains the authorization token.

```json
{
  "source": "https://{sourceEndpoint}/contentunderstanding/analyzers/{sourceAnalyzerId}",
  "authorizationToken": "{authorizationToken}",
  "expiresAt": "{expirationDateTime}",
  // "target": "https://{targetEndpoint}/contentunderstanding/analyzers/{targetAnalyzerId}"  // If specified, this is optional
}
```

## Start Copy operation

If `encryptionKey` was used when generating the authorization token, a corresponding `decryptionKey` must be specified. The target resource needs role-based-access-control (RBAC) access to the source resource, or `authorizationToken` for the remote source analyzer is required. Copied analyzers link to model deployments with the same name in the target resource as the source analyzer by default. User may override the deployment names in the `:copy` request JSON. If the target resource doesn't contain the named model deployments, copy fails. The target embedding model must match the source embedding model, or a 400 error will be returned. If the target chatCompletion model is different from the source chatCompletion model, a warning is returned.

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
