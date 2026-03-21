---
title: Include file
description: Include file
author: msakande
ms.reviewer: seramasu
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

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

- The service might re-route some priority requests to standard processing\* during these scenarios:

    - If rapid increases to your priority processing tokens per minute lead to hitting _ramp rate limits_. Currently, the ramp rate limit is defined as increasing traffic by more than 50% tokens per minute in less than 15 minutes.
    - During periods of peak requests to priority processing.
    - Long context requests sent to certain models listed in the [Latency target table](#latency-target).

    > [!TIP]
    > If you routinely encounter ramp rate limits, consider purchasing PTU instead of or in addition to priority processing.
    
    \* The service bills requests processed by the standard service tier at standard rates. Requests processed by the standard service tier include `service_tier = default` in the response, while requests processed by priority processing tier include `service_tier = priority` in the response.

## Troubleshooting

| Issue | Cause | Resolution |
| ------- | ------- | ------------ |
| Requests downgraded to standard tier | One of these situations: <br>- Traffic ramped up more than 50% tokens per minute in under 15 minutes, hitting the ramp rate limit. <br>- Requests sent during periods of peak requests to priority processing.<br> - Long context requests sent to certain models listed in the [Latency target table](#latency-target). | - Increase traffic gradually, if you've encountered ramp rate limits.<br> - Consider purchasing PTU for steady-state capacity. |

## Related content

- [Provisioned throughput](../concepts/provisioned-throughput.md)
- [Spillover traffic management](../how-to/spillover-traffic-management.md)
- [Deployment types](../../foundry-models/concepts/deployment-types.md)
- [Monitoring Azure OpenAI](../../../foundry-classic/openai/how-to/monitor-openai.md)
- [Understanding costs associated with PTU](../how-to/provisioned-throughput-onboarding.md)
