---
title: "Manage traffic with spillover for provisioned deployments"
description: "Learn how to manage traffic bursts in Azure OpenAI provisioned deployments using the spillover feature. Optimize performance and reduce disruptions effectively."
#customer intent: As a developer, I want to enable spillover for my provisioned deployments so that I can manage traffic bursts effectively.
author: msakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.reviewer: seramasu
reviewer: rsethur
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 03/04/2026
ms.custom:
  - dev-focus
  - classic-and-new
  - doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to manage traffic bursts on my provisioned deployments by routing overage traffic to standard deployments using spillover.
---

# Manage traffic with spillover for provisioned deployments

[!INCLUDE [spillover-traffic-management 1](../includes/how-to-spillover-traffic-management-1.md)]

## Enable spillover for all requests on a provisioned deployment

# [Foundry portal](#tab/portal)

See the REST API tab to learn how to enable spillover.

# [REST API](#tab/rest-api)

The spillover capability can be enabled for all requests on a provisioned deployment using a deployment property or it can be managed on a per-request basis using request headers. To enable spillover for all requests on a provisioned deployment, set the deployment property `spilloverDeploymentName` to the standard deployment target for spillover requests. This property can be set during the creation of a new provisioned deployment or can be added to an existing provisioned deployment. The `spilloverDeploymentName` property needs to be set to the name of a standard deployment within the same Azure OpenAI resource as your provisioned deployment. 

```bash
curl -X PUT https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource-group-temp/providers/Microsoft.CognitiveServices/accounts/docs-openai-test-001/deployments/spillover-ptu-deployment?api-version=2024-10-01 \
  -H "Content-Type: application/json" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' \
  -d '{"sku":{"name":"GlobalProvisionedManaged","capacity":100},"properties": {"spilloverDeploymentName": "spillover-standard-deployment", "model":{"format": "OpenAI","name": "gpt-4o-mini","version": "2024-07-18"}}}'
```

A successful request returns HTTP status `200` or `201` with a JSON response containing the deployment details.

**Reference:** [Deployments - Create Or Update](/rest/api/aiservices/accountmanagement/deployments/create-or-update)

### Enable spillover for select inference requests

To selectively enable spillover on a per-request basis, set the `x-ms-spillover-deployment` inference request header to the standard deployment target for spillover requests. If the `x-ms-spillover-deployment` header isn't set on a given request, spillover is initiated in the event of a non-200 response. The use or omission of this header provides the flexibility to control when spillover should or should not be initiated for a given workload or scenario.

```bash
curl $AZURE_OPENAI_ENDPOINT/openai/deployments/spillover-ptu-deployment/chat/completions?api-version=2024-10-21 \
  -H "Content-Type: application/json" \
  -H "x-ms-spillover-deployment: spillover-standard-deployment" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' \
  -d '{"messages":[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},{"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},{"role": "user", "content": "Do other Azure services support this too?"}]}'

```

A successful request returns HTTP status `200` with the chat completion response. If spillover occurs, the response includes the `x-ms-spillover-from-deployment` header.

**Reference:** [Create chat completion](../latest.md#create-chat-completion)

> [!NOTE]
> If the spillover capability is enabled for the deployment using the `spilloverDeploymentName` property and also enabled at the request level using the `x-ms-spillover-deployment` header, the system defaults to the setting of the deployment property. If you want to ensure that spillover is only enabled on per-request basis, don't set the `spilloverDeploymentName` property on the provisioned deployment and only rely on the `x-ms-spillover-deployment` header on a per-request basis. 

---

[!INCLUDE [spillover-traffic-management 2](../includes/how-to-spillover-traffic-management-2.md)]

## Identify spillover requests

The following HTTP response headers indicate that a specific request spilled over:

- `x-ms-spillover-from-deployment`. This header contains the PTU deployment name. The presence of this header indicates that the request is a spillover request.

- `x-ms-deployment-name`. This header contains the name of the deployment that serves the request. If the request spills over, the deployment name is the name of the standard deployment.

For a request that spills over, if the standard deployment request fails for any reason, the original PTU response is used in the response to the customer. The customer sees a header `x-ms-spillover-error` that contains the response code of the spillover request (such as `429` or `500`) so that they know the reason for the failed spillover.

## Monitor spillover usage

Since the spillover capability relies on a combination of provisioned and standard deployments to manage traffic overages, monitoring can be conducted at the deployment level for each deployment. To view how many requests were processed on the primary provisioned deployment versus the spillover standard deployment, apply the splitting feature in Azure Monitor metrics to view the requests processed by each deployment and their respective status codes. Similarly, use the splitting feature to view how many tokens were processed on the primary provisioned deployment versus the spillover standard deployment for a given time period.

[!INCLUDE [spillover-traffic-management 3](../includes/how-to-spillover-traffic-management-3.md)]
