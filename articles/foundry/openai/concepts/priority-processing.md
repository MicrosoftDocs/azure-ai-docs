---
title: Enable priority processing for Microsoft Foundry Models
description: "Learn how to enable priority processing for Microsoft Foundry models to achieve low latency and high availability for time-sensitive workloads."
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 03/16/2026
ms.author: mopeakande
author: msakande
ms.reviewer: seramasu
reviewer: rsethur
ai-usage: ai-assisted
ms.custom:
  - ignite-2025, pilot-ai-workflow-jan-2026
  - classic-and-new
  - doc-kit-assisted
#customerIntent: As a developer or data scientist working with latency-sensitive AI applications, I want to understand and implement priority processing for Microsoft Foundry models so that I can achieve predictable low latency and high availability for time-critical workloads without requiring long-term commitments or provisioned capacity.
---

# Enable priority processing for Microsoft Foundry models

Priority processing provides low-latency performance with the flexibility of pay-as-you-go. In this article, you enable priority processing on a model deployment, verify which service tier processed your requests, and monitor associated costs.

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry project with a model of the deployment type `GlobalStandard` or `DataZoneStandard` deployed.
- API version `2025-12-01` or later.

## Key use cases

- **Consistent, low latency** for responsive user experiences.
- **Pay-as-you-go simplicity** with no long-term commitments. 
- **Business-hour or bursty traffic** that benefits from scalable, cost-efficient performance. Optionally, you can combine priority processing with Provisioned Throughput Units (PTU) for steady-state capacity and cost optimization.

> [!NOTE]
> Priority processing uses the same quota as standard processing. This means your standard deployment that's enabled with priority processing consumes quota from your existing standard allocation.

## Latency target

| Model | Latency target value<sup>2</sup> | 
| --- | --- |
| gpt-5.4, 2026-03-05<sup>1</sup> | 99% > 50 Tokens Per Second |
| gpt-5.2, 2025-12-11 | 99% > 50 Tokens Per Second |
| gpt-5.1, 2025-11-13 | 99% > 50 Tokens Per Second |
| gpt-4.1, 2025-04-14<sup>1</sup> | 99% > 80 Tokens Per Second |

<sup>1</sup> Long context requests (that is, requests estimated at larger than 128k prompt tokens) will be downgraded to standard processing

<sup>2</sup> Calculated as p50 request latency on a per 5 minute basis.

## Priority processing support

# [Global standard](#tab/global-standard)

### Global standard model availability

| **Region**     | **gpt-5.4, 2026-03-05** | **gpt-5.2, 2025-12-11** | **gpt-5.1, 2025-11-13** | **gpt-4.1, 2025-04-14** |
|:---------------|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|
| centralus      | ✅                      | ✅                      | ✅                      | ✅                      |
| koreacentral   | ✅                      | ✅                      | ✅                      | ✅                      |
| southcentralus | ✅                      | ✅                      | ✅                      | ✅                      |


# [Data Zone standard](#tab/datazone-standard)

### Data zone standard model availability

| **Region**     | **gpt-5.4, 2026-03-05** | **gpt-5.2, 2025-12-11** | **gpt-5.1, 2025-11-13** | **gpt-4.1, 2025-04-14** |
|:---------------|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|
| centralus      | ✅                      | ✅                     | ✅                      | ✅                      |
| southcentralus | ✅                      | ✅                     | ✅                      | ✅                      |


---

## Enable priority processing at the deployment level

You can enable priority processing at the deployment level and [(optionally) at the request level](#enable-priority-processing-at-the-request-level).

> [!NOTE]
> Priority processing uses the same quota as standard processing. This means your deployment that's enabled with priority processing consumes quota from your existing standard allocation.

In the [!INCLUDE [foundry-link](../../includes/foundry-link.md)] portal, you can enable priority processing during deployment setup. Turn on the **Priority processing** toggle on the deployment details page when creating the deployment or update the setting of a deployed model by editing the deployment details.

:::image type="content" source="../media/priority-processing/enable-priority-processing-foundry.png" alt-text="Screenshot showing how to enable priority processing during model deployment in the Foundry portal." lightbox="../media/priority-processing/enable-priority-processing-foundry.png":::
> [!NOTE]
> If you prefer to use code to enable priority processing at the deployment level, you can do so via the REST API for deployment by setting the `service_tier` attribute as follows: `"properties" : {"service_tier" : "priority"}`. Allowed values for the `service_tier` attribute are `default` and `priority`. `default` implies standard processing, while `priority` enables priority processing.

Once a model deployment is configured to use priority processing, you can start sending requests to the model.

## View usage metrics

You can view the utilization measure for your resource in the Azure Monitor section in the Azure portal. 

To view the volume of requests processed by standard processing versus priority processing, split by the service tier (standard or priority) that was in the original request:

1. Sign in to [https://portal.azure.com](https://portal.azure.com).
1. Go to your Azure OpenAI resource and select the **Metrics** option from the left navigation.
1. On the metrics page, add the **Azure OpenAI requests** metric. You can also select other metrics like **Azure OpenAI latency**, **Azure OpenAI usage**, and others.
1. Select **Add filter** to select the standard deployment for which priority processing requests were processed.
1. Select **Apply splitting** to split the values by **ServiceTierRequest** and **ServiceTierResponse**.

:::image type="content" source="../media/priority-processing/azure-monitor-priority-processsing-utilization.png" alt-text="Screenshot of the priority processing utilization on the resource's metrics page in the Azure portal." lightbox="../media/priority-processing/azure-monitor-priority-processsing-utilization.png":::

For more information about monitoring your deployments, see [Monitor Azure OpenAI](../../../foundry-classic/openai/how-to/monitor-openai.md).

## Monitor costs

You can see a breakdown of costs for priority and standard requests in the Azure portal's cost analysis page by filtering on deployment name and billing tags as follows:

1. Go to the cost analysis page in the [Azure portal](https://portal.azure.com).
1. (Optional) Filter by resource.
1. To filter by deployment name: Add a filter for billing **Tag** > select **deployment** as the value, then choose your deployment name.

:::image type="content" source="../media/priority-processing/cost-analysis-priority-processing.png" alt-text="Screenshot of the priority processing utilization on the resource's cost analysis page in the Azure portal." lightbox="../media/priority-processing/cost-analysis-priority-processing.png":::

For information about pricing for priority processing, see the [Azure OpenAI Service pricing overview](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

## Enable priority processing at the request level

Enabling priority processing at the request level is **optional**. Both the chat completions API and responses API have an optional attribute `service_tier` that specifies the processing type to use when serving a request. The following example shows how to set `service_tier` to `priority` in a responses request.

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
     "model": "gpt-4.1",
     "input": "This is a test",
     "service_tier": "priority"
    }'
```

Use the `service_tier` attribute to override the deployment-level setting. `service_tier` can take the values `auto`, `default`, and `priority`. 

- If you don't set the attribute, it defaults to `auto`. 

- `service_tier = auto` means the request uses the service tier configured in the deployment.  

- `service_tier = default` means the request uses the standard pricing and performance for the selected model.  

- `service_tier = priority` means the request uses the priority processing service tier. 

The following table summarizes which service tier processes your requests based on the deployment-level and request-level settings for `service_tier`.

| Deployment-level setting | Request-level setting | Request processed by service tier |
|----------------------------|------------------------|----------------------------|
| default | auto, default | Standard |
| default | priority | Priority processing |
| priority | auto, priority | Priority processing |
| priority | default | Standard |

## Limitations

- The service currently doesn't support regional standard deployments and EU datazone standard deployments.

- The service might re-route some priority requests to standard processing during these scenarios:

    - If rapid increases to your priority processing tokens per minute lead to hitting _ramp rate limits_. Currently, the ramp rate limit is defined as increasing traffic by more than 50% tokens per minute in less than 15 minutes.
    - During periods of peak requests to priority processing.
    
    > [!NOTE]
    > - The service bills requests processed by the standard service tier at standard rates. Requests processed by the standard service tier include `service_tier = default` in the response, while requests processed by priority processing tier include `service_tier = priority` in the response.
    >
    > - If you routinely encounter ramp rate limits, consider purchasing PTU instead of or in addition to priority processing. 

## Troubleshooting

| Issue | Cause | Resolution |
| ------- | ------- | ------------ |
| Requests downgraded to standard tier | One of two situations: <br>- Traffic ramped up more than 50% tokens per minute in under 15 minutes, hitting the ramp rate limit. <br>- Requests sent during periods of peak requests to priority processing. | - Increase traffic gradually, if you've encountered ramp rate limits.<br> - Consider purchasing PTU for steady-state capacity. |

## Related content

- [Provisioned throughput](provisioned-throughput.md)
- [Spillover traffic management](../how-to/spillover-traffic-management.md)
- [Deployment types](../../foundry-models/concepts/deployment-types.md)
- [Monitoring Azure OpenAI](../../../foundry-classic/openai/how-to/monitor-openai.md)
- [Understanding costs associated with PTU](../how-to/provisioned-throughput-onboarding.md)
