---
title: Manage traffic with spillover for provisioned deployments
description: Learn how to manage traffic bursts in Azure OpenAI provisioned deployments using the spillover feature. Optimize performance and reduce disruptions effectively.
#customer intent: As a developer, I want to enable spillover for my provisioned deployments so that I can manage traffic bursts effectively.
author: msakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.reviewer: seramasu
reviewer: rsethur
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/30/2026
ms.custom: dev-focus
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to manage traffic bursts on my provisioned deployments by routing overage traffic to standard deployments using spillover.
---

# Manage traffic with spillover for provisioned deployments

[!INCLUDE [version-banner](../../includes/version-banner.md)]

This article describes how to manage traffic with spillover for provisioned deployments in Azure OpenAI. Spillover manages traffic fluctuations by routing overage traffic to a corresponding standard deployment. This optional capability can be set for all requests on a deployment or managed on a per-request basis, helping you reduce disruptions during traffic bursts.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/cognitive-services).

- A provisioned managed deployment and a standard deployment in the same Azure OpenAI resource

- The data processing level of your standard deployment must match your provisioned deployment. For example, use a global provisioned deployment with a global standard spillover deployment.

- Azure CLI installed for REST API examples, or access to the Foundry portal

- The `AZURE_OPENAI_ENDPOINT` environment variable set to your Azure OpenAI endpoint URL

- **Cognitive Services Contributor** role or higher on the Azure OpenAI resource to create or modify deployments

## Enable spillover for all requests on a provisioned deployment

# [Foundry portal](#tab/portal)

::: moniker range="foundry-classic"

To deploy a model with the spillover capability, go to the [Foundry portal](https://ai.azure.com/?cid=learnDocs). On the left navigation menu, then select **Deployments**.


Select **Deploy model**. In the menu that appears, select **Customize**.

:::image type="content" source="../media/provisioned/customize.png" alt-text="A screenshot showing the deployment customization button." lightbox="../media/provisioned/customize.png":::

Specify one of the provisioned options as the **Deployment type**, for example **Global Provisioned Throughput**. Select **Traffic spillover** to enable spillover for your provisioned deployment. 

> [!TIP]
> * To enable spillover, your account must have at least one active pay-as-you-go deployment that matches the model and version of your current provisioned deployment.
> * To see how to enable spillover for select inference requests, select the **REST API** tab above.

:::image type="content" source="../media/provisioned/spillover.png" alt-text="A screenshot showing the spillover option." lightbox="../media/provisioned/spillover.png":::

::: moniker-end

::: moniker range="foundry"

See the REST API tab to learn how to enable spillover.

::: moniker-end

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

A successful request returns HTTP status `200` with the chat completion response. If spillover occurs, the response includes the `x-ms-spillover-from-<deployment-name>` header.

**Reference:** [Create chat completion](../latest.md#create-chat-completion)

> [!NOTE]
> If the spillover capability is enabled for the deployment using the `spilloverDeploymentName` property and also enabled at the request level using the `x-ms-spillover-deployment` header, the system defaults to the setting of the deployment property. If you want to ensure that spillover is only enabled on per-request basis, don't set the `spilloverDeploymentName` property on the provisioned deployment and only rely on the `x-ms-spillover-deployment` header on a per-request basis. 

---

## When to enable spillover

To maximize the utilization of your provisioned deployment, enable spillover for all global and data zone provisioned deployments. With spillover, bursts or fluctuations in traffic can be automatically managed by the service. This capability reduces the risk of experiencing disruptions when a provisioned deployment is fully utilized. Alternatively, spillover is configurable per-request to provide flexibility across different scenarios and workloads. Spillover also works with the [Foundry Agent Service](../../agents/overview.md).  

## When spillover comes into effect

When you enable spillover for a deployment or configure it for a given inference request, spillover initiates when a specific non-`200` response code is received as a result of one of these scenarios:

- Provisioned throughput units (PTU) are completely used, which results in a `429` response code.

- You send a long context token request, which results in a `400` error code. For example, when you use `gpt 4.1` series models, PTU supports only context lengths less than 128K and returns HTTP 400.

- Server errors occur when processing your request, which results in error code `500` or `503`.

When a request results in one of these non-`200` response codes, Azure OpenAI automatically sends the request from your provisioned deployment to your standard deployment to be processed.

> [!NOTE]
> Even if a subset of requests is routed to the standard deployment, the service prioritizes sending requests to the provisioned deployment before sending any overage requests to the standard deployment. This prioritization might incur additional latency.

## Identify spillover requests

The following HTTP response headers indicate that a specific request spilled over:

- `x-ms-spillover-from-<deployment-name>`. This header contains the PTU deployment name. The presence of this header indicates that the request is a spillover request.

- `x-ms-<deployment-name>`. This header contains the name of the deployment that serves the request. If the request spills over, the deployment name is the name of the standard deployment.

For a request that spills over, if the standard deployment request fails for any reason, the original PTU response is used in the response to the customer. The customer sees a header `x-ms-spillover-error` that contains the response code of the spillover request (such as `429` or `500`) so that they know the reason for the failed spillover.

## Monitor spillover usage

Since the spillover capability relies on a combination of provisioned and standard deployments to manage traffic overages, monitoring can be conducted at the deployment level for each deployment. To view how many requests were processed on the primary provisioned deployment versus the spillover standard deployment, apply the splitting feature in Azure Monitor metrics to view the requests processed by each deployment and their respective status codes. Similarly, use the splitting feature to view how many tokens were processed on the primary provisioned deployment versus the spillover standard deployment for a given time period. 

::: moniker range="foundry-classic"

For more information on observability within Azure OpenAI, review the [Monitor Azure OpenAI](./monitor-openai.md) documentation. 

::: moniker-end

## Spillover cost

Because spillover uses a combination of provisioned and standard deployments to manage traffic fluctuations, billing for spillover involves two components:

- For any requests processed by your provisioned deployment, only the hourly provisioned deployment cost applies. No additional costs are incurred for these requests.

- For any requests routed to your standard deployment, the request is billed at the associated input token, cached token, and output token rates for the specified model version and deployment type.

## Monitor metrics in the Azure portal

The following Azure Monitor metrics chart provides an example of the split of requests between the primary provisioned deployment and the spillover standard deployment when spillover is initiated. To create a chart, navigate to your resource in the [Azure portal](https://portal.azure.com). 

1. Select **Monitoring** > **Metrics** from the left navigation menu.

1. Add the `Azure OpenAI Requests` metric.
    
    :::image type="content" source="../media/provisioned/spillover-metrics-menu.png" alt-text="A screenshot showing the metrics for a basic spillover example in the Azure portal." lightbox="../media/provisioned/spillover-metrics-menu.png":::
    
1. Select **Apply splitting** and apply the `ModelDeploymentName` split and `StatusCode` splits to the `Azure OpenAI Requests` metric. This shows a chart with the `200` (success) and `429` (too many requests) response codes generated for your resource.   

    :::image type="content" source="../media/provisioned/add-splitting.png" alt-text="A screenshot showing the menu for adding splits in the Azure portal." lightbox="../media/provisioned/add-splitting.png":::
    
    Be sure to add the model deployments you want to view when applying the `ModelDeploymentName` split.

    :::image type="content" source="../media/provisioned/model-filter.png" alt-text="A screenshot showing the available model filters." lightbox="../media/provisioned/model-filter.png":::

    The following example shows an instance where a spike in requests sent to the provisioned throughput deployment generates `429` error codes. Shortly after, spillover occurs and requests begin going to the pay-as-you-go deployment used for spillover, generating `200` responses for that deployment.
    

    :::image type="content" source="../media/provisioned/spillover-chart-simplified.png" alt-text="A screenshot showing the metrics for visualizing spillover." lightbox="../media/provisioned/spillover-chart-simplified.png":::

    > [!NOTE]
    > As requests go to the pay-as-you-go deployment, they still generate 429 response codes on the provisioned deployment before being redirected.
    > :::image type="content" source="../media/provisioned/spillover-chart-errors.png" alt-text="A screenshot showing the response codes from a provisioned deployment." lightbox="../media/provisioned/spillover-chart-errors.png":::

### View spillover metrics

Applying the `IsSpillover` split lets you view the requests to your deployment that are being redirected to your spillover deployment. Following from the previous example, you can see how the `429` responses from the primary deployment match the `200` response codes generated by the spillover deployment.

:::image type="content" source="../media/provisioned/spillover-chart.png" alt-text="A screenshot showing the spillover split in Azure portal." lightbox="../media/provisioned/spillover-chart.png":::

## See also

* [What is provisioned throughput?](../concepts/provisioned-throughput.md)
* [Onboarding to provisioned throughput](./provisioned-throughput-onboarding.md)
