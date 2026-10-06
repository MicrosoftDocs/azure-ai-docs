---
title: "Use Flex processing with Azure OpenAI in Foundry Models (preview)"
description: "Learn when to use Flex processing, send Flex requests, implement a Standard fallback, and monitor usage and costs for Azure OpenAI."
author: swingfu
ms.author: shiyingfu
manager: mcleans
ms.reviewer: seramasu
reviewer: rsethur
ms.date: 10/06/2026
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer with delay-tolerant AI workloads, I want to use Flex processing and implement a Standard fallback so that I can reduce cost without making my application unreliable.
---

# Use Flex processing with Azure OpenAI in Microsoft Foundry Models (preview)

Flex processing (preview) provides inference at a 50% discount compared with Standard processing for workloads that can tolerate slower response times and occasional resource unavailability. Select Flex processing for an individual Responses API or Chat Completions API request by setting `service_tier` to `flex`.

Use Flex processing for noninteractive and lower-priority work, such as model evaluations, data enrichment, document analysis, and asynchronous application workflows. For latency-sensitive or capacity-sensitive workloads, use Standard processing, Priority processing, or provisioned throughput instead.

> [!IMPORTANT]
> With the introduction of Flex processing, requests that set `service_tier` to `flex` are processed only when the selected model supports Flex processing. An unsupported model returns an HTTP 400 `invalid_request_error` and doesn't fall back to Standard processing. Flex processing has no latency SLA or service SLA.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource with a supported model deployed by using the Global Standard deployment type.
- The resource endpoint and an API key or Microsoft Entra ID credentials. The examples in this article use an API key stored in the `AZURE_OPENAI_API_KEY` environment variable.
- A workload that can tolerate variable latency and transient resource-unavailable responses.
- Python 3.10 or later and the OpenAI Python package for the Python examples:

    ```bash
    pip install --upgrade openai
    ```

## Send a Flex request

Set `service_tier` to `flex` in each request that should use Flex processing. The `model` value is the name of your Azure model deployment.

### Python

The following example sends a Flex request by using the Responses API:

```python
import os

from openai import OpenAI

AZURE_OPENAI_ENDPOINT = "https://YOUR-RESOURCE-NAME.openai.azure.com"

# Create a client with a longer timeout for Flex requests.
openai = OpenAI(
    base_url=f"{AZURE_OPENAI_ENDPOINT}/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    timeout=900.0,
)

# Send a request for Flex processing.
response = openai.responses.create(
    model="YOUR-GPT-5.6-SOL-DEPLOYMENT-NAME",
    input="Analyze these records and summarize the recurring themes.",
    service_tier="flex",
)

print(response.output_text)
print(f"Processed by service tier: {response.service_tier}")
```

```output
<generated-analysis>
Processed by service tier: flex
```

The response contains the generated analysis and the service tier that processes the request.

**Reference:** [Responses API](../reference-preview-latest.md)

### REST

The following example sends the same request directly to the Responses API:

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "YOUR-GPT-5.6-SOL-DEPLOYMENT-NAME",
    "input": "Analyze these records and summarize the recurring themes.",
    "service_tier": "flex"
  }'
```

```output
{
    "service_tier": "flex",
    "status": "completed",
    "output": [<response-output>]
}
```

To verify which tier processes the request, check the `service_tier` field in a successful response.

**Reference:** [Responses API REST reference](/rest/api/microsoft-foundry/aiproject#responses)

## Choose a processing option

Flex, Standard, and Priority processing are service-tier choices for online API requests. Batch and provisioned throughput are separate deployment and purchasing options.

| Option | How you select it | Latency and availability | Cost model | Best for |
| --- | --- | --- | --- | --- |
| **Flex processing** | Set request-level `service_tier` to `flex`. | Variable latency. Requests can return HTTP 429 when Flex capacity isn't available. | 50% discount compared with Standard token rates. Cached-token discounts also apply. | Evaluations, enrichment, offline analysis, and delay-tolerant background work. |
| **Standard processing** | Set request-level `service_tier` to `default`, or use the Standard tier configured for the deployment. | Best-effort online processing for general workloads. | Standard pay-per-token rate. | Development, testing, and production workloads with variable traffic. |
| **Priority processing** | Configure Priority on the deployment or set request-level `service_tier` to `priority`. | Lower and more consistent latency, with a defined target for supported models. | Priority pay-per-token rate. | Latency-sensitive online applications without a reserved-capacity commitment. |
| **Batch** | Submit an asynchronous batch job to a Batch deployment. | Results target completion within 24 hours. No real-time latency target. | Discounted batch rate. | Large offline jobs that don't require an immediate response. |
| **Provisioned throughput** | Create a provisioned deployment and purchase or reserve provisioned throughput units (PTUs). | Reserved capacity with predictable throughput and latency. | Hourly PTU billing or an Azure reservation. | High-volume, mission-critical production workloads. |

Choose Flex processing when all of the following conditions apply:

- Your workload can tolerate longer and variable processing times.
- You prefer lower cost over predictable latency.
- Your application can retry transient failures or route a failed request to Standard processing.
- The selected model and request context are supported.

Don't use Flex processing when any of the following conditions apply:

- A user is waiting for an interactive response.
- The request must complete within a strict latency target.
- Your application can't tolerate or retry transient HTTP 429 responses.
- You require reserved processing capacity or predictable throughput.

Flex processing has the following characteristics:

- **Request-level selection:** Set `service_tier` to `flex` on each request that should use Flex processing.
- **No separate deployment:** Send Standard and Flex requests to the same Global Standard deployment, and select the tier per request.
- **Supported APIs:** Use the Responses API or Chat Completions API.
- **Synchronous response:** The API call remains synchronous, even though the workload can take longer to complete. Flex processing isn't the same as the Batch API.
- **Capacity-dependent availability:** A request can return HTTP 429 when Flex capacity isn't available.
- **No automatic Standard fallback:** Your application must explicitly retry with `service_tier` set to `default` if Standard processing is acceptable.
- **Shared quota:** Flex and Standard requests use the quota assigned to the Global Standard deployment.
- **Same model output quality:** Flex uses the same underlying model as Standard. The processing tier changes latency, availability, and price, not model quality.

> [!NOTE]
> Flex input and output tokens receive a 50% discount compared with the corresponding Standard token rates. Eligible cached input tokens also receive the applicable cached-token discount. For current rates, see [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

## Review supported models

Flex processing has limited model availability at launch. `gpt-5.6-sol` is the first supported model. The following table lists supported models. Microsoft adds more models as support becomes available.

| Model | Version | Deployment type | Region availability |
| --- | --- | --- | --- |
| `gpt-5.6-sol` | `2026-07-09` | Global Standard | All Azure regions where Global Standard is available |
| `gpt-5.6-luna` | `2026-07-09` | Global Standard | All Azure regions where Global Standard is available |
| `gpt-5.6-terra` | `2026-07-09` | Global Standard | All Azure regions where Global Standard is available |
| `gpt-6-astra` | `2026-09-03` | Global Standard | All Azure regions where Global Standard is available |

Check this table before you send a Flex request. Don't assume that a model or a new model version supports Flex processing because it supports Standard or Priority processing. An unsupported model returns HTTP 400. To avoid disrupting your application, implement an application-level fallback to Standard processing when Standard pricing and performance are acceptable.

## Fall back to Standard processing

Flex processing doesn't automatically route a request to Standard when Flex capacity is unavailable. If completing the request is more important than retaining Flex pricing, retry the request with `service_tier` set to `default`.

The following example uses a completion-first policy. It first attempts Flex processing and retries once with Standard processing after any HTTP 429 response:

```python
import os

from openai import OpenAI, RateLimitError

AZURE_OPENAI_ENDPOINT = "https://YOUR-RESOURCE-NAME.openai.azure.com"

# Create a client with a longer timeout for Flex requests.
openai = OpenAI(
    base_url=f"{AZURE_OPENAI_ENDPOINT}/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    timeout=900.0,
)

request = {
    "model": "YOUR-GPT-5.6-SOL-DEPLOYMENT-NAME",
    "input": "Analyze these records and summarize the recurring themes.",
}

# Try Flex processing, and fall back to Standard after an HTTP 429 response.
try:
    response = openai.responses.create(**request, service_tier="flex")
except RateLimitError:
    response = openai.responses.create(**request, service_tier="default")

print(response.output_text)
print(f"Processed by service tier: {response.service_tier}")
```

```output
<generated-analysis>
Processed by service tier: <flex-or-default>
```

Fallback to Standard changes the request's pricing and performance characteristics. Use this pattern only when the workload can accept Standard pricing.

An HTTP 429 response can indicate unavailable Flex capacity or a quota limit. Because Flex and Standard processing share quota, the Standard request might also fail when quota caused the original response. Apply retry limits and handle a second `RateLimitError` in your application. When the service returns the Flex-specific error identifier, use it to limit fallback to capacity-related responses.

For workloads that prioritize the lowest cost, retry Flex processing with exponential backoff before falling back. For workloads that prioritize completion time, fall back to Standard after the first Flex capacity error.

**Reference:** [`RateLimitError`](https://github.com/openai/openai-python/blob/main/src/openai/_exceptions.py)

## Handle Flex errors

Distinguish permanent request errors from transient capacity errors.

| HTTP status | Error | Cause | Recommended handling |
| --- | --- | --- | --- |
| **400** | `invalid_request_error` | The selected model, model version, context length, API, or request configuration doesn't support Flex processing. | Don't retry the same request unchanged. Select a supported model or context length, or explicitly retry with `service_tier` set to `default`. |
| **408** | Request timeout | The request doesn't complete within the configured client or service timeout. Flex requests can take longer than Standard requests. | Use a longer client timeout. Retry with bounded exponential backoff. If completion time is more important than Flex pricing, retry with Standard. |
| **429** | Resource unavailable or rate limited | Flex capacity is temporarily unavailable, or the request exceeded an applicable rate limit. Flex capacity is preemptible, so temporary unavailability is more likely during peak hours. | If the request exceeded a rate limit, increase the Global Standard deployment's rate limit by assigning more quota. Flex and Standard share this quota. If the subscription doesn't have enough quota for a large-throughput workload, request a quota increase. If Flex capacity is temporarily unavailable, retry with exponential backoff and jitter, distribute delay-tolerant work to off-peak periods such as weekday nights or weekends, or retry with `service_tier` set to `default`. Honor `Retry-After` when present. |
| **500, 502, 503, or 504** | Transient service error | A temporary service or gateway issue prevented completion. | Retry with bounded exponential backoff. Don't send an unlimited number of retries. |
| **401 or 403** | Authentication or authorization error | The credential is missing, invalid, expired, or doesn't have access to the resource. | Correct the credential or role assignment. Don't retry until the configuration changes. |
| **404** | Deployment not found | The deployment name or endpoint is incorrect. | Verify that `model` matches the deployment name and that the base URL points to the correct Azure OpenAI resource. |

> [!NOTE]
> A Flex request rejected because processing capacity is unavailable isn't billed. However, you might notice less available rate-limit capacity because Flex and Standard requests share the quota assigned to the Global Standard deployment.

Use exponential backoff with random jitter for HTTP 408, 429, and transient 5xx responses. Set a maximum retry count and maximum delay so that a failed request doesn't remain in an unbounded retry loop.

1. Honor `Retry-After` when the response includes it.
1. Otherwise, wait for an exponentially increasing delay with random jitter.
1. Retry Flex only while the delay remains acceptable for the workload.
1. Fall back to Standard if the retry budget is exhausted and the application allows the higher Standard cost.
1. Return an explicit failure if neither delayed Flex processing nor Standard fallback meets the application's requirements.

Don't repeatedly retry the same unsupported Flex request. A retry succeeds only after you change the model, context length, API configuration, or service tier.

## Monitor usage and costs

Use Azure Monitor metrics to compare Flex and Standard traffic on the same deployment. Monitor request volume, token consumption, latency, failures, and the rate at which Flex requests fall back to Standard in your application.

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Go to your Azure OpenAI resource, and select **Metrics**.
1. Add the **Azure OpenAI Requests** metric. You can also add **Azure OpenAI Latency**, **Azure OpenAI Usage**, and error metrics.
1. Add a filter where **ServiceTierRequest** equals `flex`.

    :::image type="content" source="../media/how-to/flex-monitor.png" alt-text="Screenshot of Azure Monitor metrics filtered to Flex requests by using the ServiceTierRequest property." lightbox="../media/how-to/flex-monitor.png":::

1. Create alerts for sustained HTTP 429 responses, increased error rates, and latency that exceeds your workload's retry budget.

Track the following signals for each workload:

| Signal | Why it matters |
| --- | --- |
| Flex request count | Shows adoption and traffic routed for lower-cost processing. |
| Successful Flex request rate | Shows how often Flex capacity accepts and completes requests. |
| HTTP 429 rate | Shows periods when Flex capacity or deployment quota is constrained. |
| Standard fallback count and rate | Shows the reliability benefit and added cost from application-controlled fallback. |
| Input, cached input, and output tokens | Supports cost attribution and verifies the effect of prompt caching. |
| End-to-end latency | Helps determine whether a workload remains suitable for Flex. |
| HTTP 400 `invalid_request_error` count | Identifies unsupported models, model versions, context lengths, or request configurations. |

For more information about monitoring model deployments, see [Monitor Azure OpenAI](../../../foundry-classic/openai/how-to/monitor-openai.md).

Flex usage is billed on dedicated Flex meters so that you can distinguish it from Standard usage. Use Cost Analysis to review Flex token costs by resource and deployment.

1. In the [Azure portal](https://portal.azure.com), open **Cost Management + Billing** > **Cost analysis**.
1. Filter to the subscription, resource group, or Azure OpenAI resource that contains the deployment.
1. Group or filter by **Meter** to separate Flex usage from Standard usage.
1. Add a billing **Tag** filter, select **deployment**, and choose the deployment name.
1. Compare Flex cost savings with Standard fallback costs and the workload's completion requirements.

Flex input and output tokens are priced at 50% of the corresponding Standard rates. Prompt caching can reduce the cost of eligible cached input tokens further. A Flex request rejected because processing capacity is unavailable isn't billed.

## Apply production best practices

- **Set a longer timeout.** Flex requests can take longer than Standard requests. Start with a client timeout appropriate for your workload, such as 15 minutes, and test with representative prompts.
- **Use bounded retries.** Limit retry attempts and total elapsed time.
- **Add jitter.** Randomize backoff delays to avoid synchronized retry spikes.
- **Make fallback explicit.** Set `service_tier` to `default` rather than relying on implicit behavior.
- **Track the processed tier.** Record the response `service_tier` value with latency, status, token usage, and cost data.
- **Separate interactive and background traffic.** Keep user-facing requests on Standard, Priority, or provisioned throughput unless variable Flex latency is acceptable.
- **Control duplicate work.** Ensure the application doesn't submit the same logical job multiple times after client-side timeouts.
- **Test failure paths.** Validate handling for HTTP 400, 408, 429, and transient 5xx responses before using Flex processing in production workflows.
- **Review model support before upgrades.** A replacement model or model version doesn't automatically inherit Flex support.

## Override the service tier with a request header

Use the `x-ms-service-tier` request header when a gateway, proxy, or centralized
routing layer needs to select the service tier without inspecting or modifying
the request body. The header can also reduce migration changes for applications
that already select an OpenAI service tier through a request header.

The header accepts the following values:

| Header value | Requested processing tier |
| --- | --- |
| `flex` | Flex |
| `priority` | Priority |
| `default` | Standard |
| `auto` | Priority |

When the header is present and valid, it takes precedence over the
`service_tier` value in the request body.

| Header input | Request body input | Behavior and output |
| --- | --- | --- |
| Header omitted | Valid `service_tier` value | The request body selects the tier. A successful response identifies the processed tier in `service_tier`. |
| Valid header value | Any value or omitted | The header selects the requested tier. A successful response identifies the processed tier in `service_tier`. |
| Unsupported header value | Any value or omitted | The request returns HTTP 400. The service doesn't fall back to the request body value. |

This example requests Flex processing through the header. The header overrides
the `default` value in the request body:

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "x-ms-service-tier: flex" \
  -d '{
    "model": "YOUR-GPT-5.6-SOL-DEPLOYMENT-NAME",
    "input": "Analyze these records and summarize the recurring themes.",
    "service_tier": "default"
  }'
```

```output
{
    "service_tier": "flex",
    "status": "completed",
    "output": [<response-output>]
}
```

The override header doesn't provide automatic fallback. An invalid header value
or a tier that the selected deployment doesn't support returns HTTP 400.

## Related content

- [Enable Priority processing for Microsoft Foundry Models](../concepts/priority-processing.md)
- [Use global batch processing with Azure OpenAI](batch.md)
- [Review deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md)