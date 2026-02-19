---
title: Azure OpenAI API surfaces
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Information on the division of control plane and data plane API surfaces
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 02/28/2025
---


## API specs

Managing and interacting with Azure OpenAI models and resources is divided across three primary API surfaces:

- Control plane
- Data plane - authoring
- Data plane - inference

Each API surface/specification encapsulates a different set of Azure OpenAI capabilities. Each API has its own unique set of preview and stable/generally available (GA) API releases. Preview releases currently tend to follow a monthly cadence.

> [!IMPORTANT]
> There is now a new preview inference API. Learn more in our [API lifecycle guide](../api-version-lifecycle.md#api-evolution).

| API | Latest preview release | Latest GA release | Specifications | Description |
|:---|:----|:----|:----|:---|
| **Control plane** | `2025-07-01-preview` | [`2025-06-01`](/rest/api/aifoundry/accountmanagement/operation-groups?view=rest-aifoundry-accountmanagement-2025-06-01&preserve-view=true) | [Spec files](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/resource-manager/Microsoft.CognitiveServices/stable/2025-06-01/cognitiveservices.json) | The control plane API is used for operations like [creating resources](/rest/api/aifoundry/accountmanagement/accounts/create?view=rest-aifoundry-accountmanagement-2025-06-01&tabs=HTTP&preserve-view=true), [model deployment](/rest/api/aifoundry/accountmanagement/deployments/create-or-update?view=rest-aifoundry-accountmanagement-2025-06-01&tabs=HTTP&preserve-view=true), and other higher level resource management tasks. The control plane also governs what is possible to do with capabilities like Azure Resource Manager, Bicep, Terraform, and Azure CLI.|
| **Data plane** | [`v1 preview`](/azure/ai-foundry/openai/reference-preview-latest) | [`v1`](/azure/ai-foundry/openai/latest) | [Spec files](https://github.com/Azure/azure-rest-api-specs/tree/main/specification/ai/data-plane/OpenAI.v1) | The data plane API controls inference and authoring operations.  |


## Authentication

Azure OpenAI provides two methods for authentication. You can use  either API Keys or Microsoft Entra ID.

- **API Key authentication**: For this type of authentication, all API requests must include the API Key in the ```api-key``` HTTP header. The [Quickstart](../how-to/responses.md) provides guidance for how to make calls with this type of authentication.

- **Microsoft Entra ID authentication**: You can authenticate an API call using a Microsoft Entra token. Authentication tokens are included in a request as the ```Authorization``` header. The token provided must be preceded by ```Bearer```, for example ```Bearer YOUR_AUTH_TOKEN```. You can read our how-to guide on [authenticating with Microsoft Entra ID](../how-to/managed-identity.md).

### REST API versioning

The service APIs are versioned using the ```api-version``` query parameter. All versions follow the YYYY-MM-DD date structure. For example:

```http
POST https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT_NAME/chat/completions?api-version=2024-06-01
```