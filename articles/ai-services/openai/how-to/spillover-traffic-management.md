---
# Required metadata
# For more information, see https://review.learn.microsoft.com/en-us/help/platform/learn-editor-add-metadata?branch=main
# For valid values of ms.service, ms.prod, and ms.topic, see https://review.learn.microsoft.com/en-us/help/platform/metadata-taxonomies?branch=main

title: Manage traffic with spillover for Provisioned deployments
description: Article outlining how to use the spillover feature to manage traffic bursts for Azure OpenAI Service provisioned deployments
author:      sydneemayers # GitHub alias
ms.author: sydneemayers
ms.service: azure-ai-openai
ms.topic: how-to
ms.date:     03/05/2025
---

# Manage traffic with spillover for provisioned deployments (Preview)

Spillover is a capability that automates the process of sending overage traffic from provisioned deployments to standard deployments when a non-200 response is received. Spillover is an optional capability that can be set for all requests on a given deployment or can be managed on a per-request basis. When spillover is enabled, Azure OpenAI service will take care of sending any overage traffic from your provisioned deployment to a designated standard deployment to be processed.

## Prerequisites
- A global provisioned or data zone provisioned deployment to be used as your primary deployment.
- A global or data zone standard deployment to be used as your spillover deployment. 

- The provisioned and standard deployments must be in the same Azure OpenAI Service resource to be eligible for spillover.

- The data processing level of your standard deployment must match your provisioned deployment (e.g. global provisioned deployment must be used with a global standard spillover deployment).

## When to enable spillover on provisioned deployments
To maximize the utilization of your provisioned deployment, it is recommended to enable spillover for all global and data zone provisioned deployments. With spillover, bursts or fluctuations in traffic can be automatically managed by the service, which reduces the risk of experience disruptions caused by a fully utilized provisioned deployment. If there are particular use cases or workloads where spillover is not required, this capability can be controlled on a per-request basis with request headers to provide full configurability across different scenarios and workloads.  

## When does spillover come into effect?
When spillover is enabled for a deployment or configured for a given inference request, the spillover capability will be initiated when a non-200 response code is received for a request originally sent to your primary provisioned deployment. When a request results in a non-200 response code, the Azure OpenAI Service will automatically send the request to the designated spillover standard deployment to be processed. Even if a subset of requests are routed to the standard spillover deployment, the service will prioritize sending requests to the primary provisioned deployment before sending any overage to the spillover standard deployment.

## How does spillover impact cost?
Since spillover leverages a combination of provisioned and standard deployments to manage traffic fluctuations, billing for spillover will involve two aspects:
- For any requests that are processed by your primary provisioned deployment, only the hourly provisioned deployment cost will apply. No additional costs will be incurred for these requests.
- For any requests that are routed to your spillover standard deployment, the request will be billed at the associated input token, cached token, and output token rates for the specified model version and deployment type.

## How to enable spillover
The spillover capability can be enabled for two distinct scenarios: (1) enable spillover for all requests on a provisioned deployment or (2) only enable spillover for select inference requests. The following explains how to configure spillover for each of these scenarios. 

### Enable spillover for all requests on a provisioned deployment
To enable spillover for all requests on a provisioned deployment, the deployment property `spilloverDeploymentName` needs to be set to point to the spillover standard deployment required to support spillover requests. This property can be set during the creation of a new provisioned deployment or can be added to an existing provisioned deployment. The `spilloverDeploymentName` property needs to be set to the name of a newly created or existing standard deployment within the same Azure OpenAI Service resource as your provisioned deployment. 

```Bash
curl -X PUT https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource-group-temp/providers/Microsoft.CognitiveServices/accounts/docs-openai-test-001/deployments/spillover-ptu-deployment?api-version=2024-10-01 \
  -H "Content-Type: application/json" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' \
  -d '{"sku":{"name":"GlobalProvisionedManaged","capacity":100},"properties": {"spilloverDeploymentName": "spillover-standard-deployment", "model":{"format": "OpenAI","name": "gpt-4o-mini","version": "2024-07-18"}}}'
```
### Enable spillover for select inference requests
To selectively enable spillover on a per-request basis, the inference request header `x-ms-spillover-deployment` is used to specify the spillover standard deployment to direct overage traffic to in the event of a non-200 response code. If the `x-ms-spillover-deployment` header is not set on a request, spillover will not be initiated in the event of a non-200 response. The use or omission of this header provides the flexibility to control when spillover should or should not be initiated for a given workload or scenario.

```bash
curl $AZURE_OPENAI_ENDPOINT/openai/deployments/spillover-ptu-deployment/chat/completions?api-version=2025-02-01-preview \
  -H "Content-Type: application/json" \
  -H "x-ms-spillover-deployment: spillover-standard-deployment" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' \
  -d '{"messages":[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},{"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},{"role": "user", "content": "Do other Azure AI services support this too?"}]}'

```
> [!NOTE]
> If the spillover capability is enabled for the deployment using the `spilloverDeploymentName` property and also enabled at the request level using the `x-ms-spillover-deployment` header, the system will default to the setting of the deployment property. If you would like to ensure that spillover is only enabled on per-request basis, do not set the `spilloverDeploymentName` property on the provisioned deployment and only rely on the `x-ms-spillover-deployment` header on a per-request basis. 

## How do I monitor my spillover usage?
Since the spillover capability relies on a combination of provisioned and standard deployments to manage traffic overages, monitoring can be conducted at the deployment level for each deployment. To view how many requests were processed on the primary provisioned deployment versus the spillover standard deployment, leverage the splitting feature within Azure Monitor metrics to view the requests processed by each deployment and their respective status codes. Similarly, the splitting feature can be used to view how many tokens were processed on the primary provisioned deployment versus the spillover standard deployment for a given time period. For more information on observability within Azure OpenAI, review the [Monitor Azure OpenAI](./monitor-openai.md) documentation. 

The following Azure Monitor metrics chart provides an example of the split of requests between the primary provisioned deployment and the spillover standard deployment when spillover is initiated. As shown in the chart, for every request that has a non-200 response code for the provisioned deployment ("gpt-4o-ptu"), there is a corresponding request with a 200 response code on the spillover standard deployment ("gpt-4o-paygo-spillover"), indicating that these overage requests were routed to the spillover standard deployment for successful processing. ![Azure monitor chart showing spillover requests from a provisioned deployment to a standard deployment.](media/spillover-traffic-management/monitor-spillover-usage.png)