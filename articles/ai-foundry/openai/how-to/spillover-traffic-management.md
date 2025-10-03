---
title: Manage traffic with spillover for Provisioned deployments
description: Article outlining how to use the spillover feature to manage traffic bursts for Azure OpenAI in Azure AI Foundry Models provisioned deployments
author: msakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 10/02/2025
---

# Manage traffic with spillover for provisioned deployments

Spillover manages traffic fluctuations on provisioned deployments by routing overage traffic to a corresponding standard deployment. Spillover is an optional capability that can be set for all requests on a given deployment or can be managed on a per-request basis. When spillover is enabled, Azure OpenAI in Azure AI Foundry Models sends any overage traffic from your provisioned deployment to a standard deployment for processing.

> [!NOTE]
> Spillover is currently not available for the [responses API](./responses.md).

## Prerequisites
- You need to have a provisioned managed deployment and a standard deployment.

- The provisioned and standard deployments must be in the same Azure OpenAI resource to be eligible for spillover.

- The data processing level of your standard deployment must match your provisioned deployment (for example, a global provisioned deployment must be used with a global standard spillover deployment).

## When to enable spillover on provisioned deployments
To maximize the utilization of your provisioned deployment, you can enable spillover for all global and data zone provisioned deployments. With spillover, bursts or fluctuations in traffic can be automatically managed by the service. This capability reduces the risk of experiencing disruptions when a provisioned deployment is fully utilized. Alternatively, spillover is configurable per-request to provide flexibility across different scenarios and workloads. Spillover can also now be used for the [Azure AI Foundry Agent Service](../../agents/overview.md).  

## When does spillover come into effect?
When you enable spillover for a deployment or configure it for a given inference request, spillover initiates when a specific non-`200` response code is received for a given inference request as a result of one of these scenarios:

- Provisioned throughput units (PTU) are completely used, resulting in a `429` response code.

- You send a long context token request, resulting in a `400` error code. For example, when using `gpt 4.1` series models, PTU supports only context lengths less than 128k and returns HTTP 400.

- Server errors when processing your request, resulting in error code `500` or `503`.

When a request results in one of these non-`200` response codes, Azure OpenAI automatically sends the request from your provisioned deployment to your standard deployment to be processed.

> [!NOTE]
> Even if a subset of requests is routed to the standard deployment, the service prioritizes sending requests to the provisioned deployment before sending any overage requests to the standard deployment, which might incur additional latency.

## How to know a request spilled over

The following HTTP response headers indicate that a specific request spilled over:

- `x-ms-spillover-from-<deployment-name>`. This header contains the PTU deployment name. The presence of this header indicates that the request was a spillover request.

- `x-ms-<deployment-name>`. This header contains the name of the deployment that served the request. If the request spilled over, the deployment name is the name of the standard deployment.

For a request that spilled over, if the standard deployment request failed for any reason, the original PTU response is used in the response to the customer. The customer sees a header `x-ms-spillover-error` that contains the response code of the spillover request (such as `429` or `500`) so that they know the reason for the failed spillover.

## How does spillover affect cost?
Since spillover uses a combination of provisioned and standard deployments to manage traffic fluctuations, billing for spillover involves two components:

- For any requests processed by your provisioned deployment, only the hourly provisioned deployment cost applies. No additional costs are incurred for these requests.

- For any requests routed to your standard deployment, the request is billed at the associated input token, cached token, and output token rates for the specified model version and deployment type.

## Enable spillover for all requests on a provisioned deployment

# [Azure AI Foundry portal](#tab/portal)

To deploy a model with the spillover capability, navigate to the [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs). On the left navigation menu, then select **Deployments**.


Select **Deploy model**. In the menu that appears, select **Customize**.

:::image type="content" source="../media/provisioned/customize.png" alt-text="A screenshot showing the deployment customization button." lightbox="../media/provisioned/customize.png":::

Specify one the provisioned options as the **Deployment type**, for example **Global Provisioned Throughput**. Select **Traffic spillover** to enable spillover for your provisioned deployment. 

> [!TIP]
> * To enable spillover, your account must have at least one active pay-as-you-go deployment that matches the model and version of your current provisioned deployment.
> * To see how to enable spillover for select inference requests, click the **REST API** tab above.

:::image type="content" source="../media/provisioned/spillover.png" alt-text="A screenshot showing the spillover option." lightbox="../media/provisioned/spillover.png":::

# [REST API](#tab/rest-api)

The spillover capability can be enabled for all requests on a provisioned deployment using a deployment property or it can be managed on a per-request basis using request headers. To enable spillover for all requests on a provisioned deployment, set the deployment property `spilloverDeploymentName` to the standard deployment target for spillover requests. This property can be set during the creation of a new provisioned deployment or can be added to an existing provisioned deployment. The `spilloverDeploymentName` property needs to be set to the name of a standard deployment within the same Azure OpenAI resource as your provisioned deployment. 


```Bash
curl -X PUT https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource-group-temp/providers/Microsoft.CognitiveServices/accounts/docs-openai-test-001/deployments/spillover-ptu-deployment?api-version=2024-10-01 \
  -H "Content-Type: application/json" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' \
  -d '{"sku":{"name":"GlobalProvisionedManaged","capacity":100},"properties": {"spilloverDeploymentName": "spillover-standard-deployment", "model":{"format": "OpenAI","name": "gpt-4o-mini","version": "2024-07-18"}}}'
```
### Enable spillover for select inference requests
To selectively enable spillover on a per-request basis, set the `x-ms-spillover-deployment` inference request header to the standard deployment target for spillover requests. If the `x-ms-spillover-deployment` header is not set on a given request, spillover is initiated in the event of a non-200 response. The use or omission of this header provides the flexibility to control when spillover should or should not be initiated for a given workload or scenario.

```bash
curl $AZURE_OPENAI_ENDPOINT/openai/deployments/spillover-ptu-deployment/chat/completions?api-version=2025-02-01-preview \
  -H "Content-Type: application/json" \
  -H "x-ms-spillover-deployment: spillover-standard-deployment" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' \
  -d '{"messages":[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},{"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},{"role": "user", "content": "Do other Azure services support this too?"}]}'

```

> [!NOTE]
> If the spillover capability is enabled for the deployment using the `spilloverDeploymentName` property and also enabled at the request level using the `x-ms-spillover-deployment` header, the system defaults to the setting of the deployment property. If you would like to ensure that spillover is only enabled on per-request basis, do not set the `spilloverDeploymentName` property on the provisioned deployment and only rely on the `x-ms-spillover-deployment` header on a per-request basis. 

---

## How do I monitor my spillover usage?
Since the spillover capability relies on a combination of provisioned and standard deployments to manage traffic overages, monitoring can be conducted at the deployment level for each deployment. To view how many requests were processed on the primary provisioned deployment versus the spillover standard deployment, apply the splitting feature within Azure Monitor metrics to view the requests processed by each deployment and their respective status codes. Similarly, the splitting feature can be used to view how many tokens were processed on the primary provisioned deployment versus the spillover standard deployment for a given time period. For more information on observability within Azure OpenAI, review the [Monitor Azure OpenAI](./monitor-openai.md) documentation. 

## Monitor metrics in the Azure portal

The following Azure Monitor metrics chart provides an example of the split of requests between the primary provisioned deployment and the spillover standard deployment when spillover is initiated. To create a chart, navigate to your resource in the [Azure portal](https://ai.azure.com/?cid=learnDocs). 

1.  Select **Monitoring** > **metrics** from the left navigation menu.

1. Add the `Azure OpenAI Requests` requests metric. 
    
    :::image type="content" source="../media/provisioned/spillover-metrics-menu.png" alt-text="A screenshot showing the metrics for a basic spillover example in the Azure portal." lightbox="../media/provisioned/spillover-metrics-menu.png":::
    
1. Select **Apply splitting** and apply the `ModelDeploymentName` split and `StatusCode` splits to the `Azure OpenAI Requests` metric. This will show you a chart with the `200` (success) and `429` (too many requests) response codes that are generated for your resource.   

    :::image type="content" source="../media/provisioned/add-splitting.png" alt-text="A screenshot showing the menu for adding splits in the Azure portal." lightbox="../media/provisioned/add-splitting.png":::
    
    Be sure to add the model deployments you want to view when applying the `ModelDeploymentName` split.

    :::image type="content" source="../media/provisioned/model-filter.png" alt-text="A screenshot showing the available model filters." lightbox="../media/provisioned/model-filter.png":::

    The following example shows an instance where a spike in requests sent to the provisioned throughput deployment generates `429` error codes. Shortly after, spillover occurs and requests begin to be sent to the pay-as-you-go deployment being used for spillover, generating `200` responses for that deployment.
    

    :::image type="content" source="../media/provisioned/spillover-chart-simplified.png" alt-text="A screenshot showing the metrics for visualizing spillover." lightbox="../media/provisioned/spillover-chart-simplified.png":::

    > [!NOTE]
    > As requests are sent to the pay-as-you-go deployment, they still will generate 429 response codes on the provisioned deployment before being redirected.
    > :::image type="content" source="../media/provisioned/spillover-chart-errors.png" alt-text="A screenshot showing the response codes from a provisioned deployment." lightbox="../media/provisioned/spillover-chart-errors.png":::
    
### Viewing spillover metrics

Applying the `IsSpillover` split lets you view the requests to your deployment that are being redirected to your spillover deployment. Following from the previous example, you can see how the `429` responses from the primary deployment match the `200` response codes generated by the spillover deployment.

:::image type="content" source="../media/provisioned/spillover-chart.png" alt-text="A screenshot showing the spillover split in Azure portal." lightbox="../media/provisioned/spillover-chart.png":::



## See also

* [What is provisioned throughput](../concepts/provisioned-throughput.md)
* [Onboarding to provisioned throughput](./provisioned-throughput-onboarding.md)
