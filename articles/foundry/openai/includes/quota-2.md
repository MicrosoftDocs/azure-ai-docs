---
title: Include file
description: Include file
author: alvinashcraft
ms.reviewer: shiyingfu
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/06/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

## Migrating existing deployments

As part of the transition to the new quota system and TPM based allocation, all existing Azure OpenAI model deployments have been automatically migrated to use quota. In cases where the existing TPM/RPM allocation exceeds the default values due to previous custom rate-limit increases, equivalent TPM were assigned to the impacted deployments.

## Understanding rate limits

Assigning TPM to a deployment sets the Tokens-Per-Minute (TPM) and Requests-Per-Minute (RPM) rate limits for the deployment, as described above. TPM rate limits are based on the maximum number of tokens that are estimated to be processed by a request at the time the request is received. It isn't the same as the token count used for billing, which is computed after all processing is completed.  

As each request is received, Azure OpenAI computes an estimated max processed-token count that includes the following:

- Prompt text and count
- The max_tokens parameter setting
- The best_of parameter setting

As requests come into the deployment endpoint, the estimated max-processed-token count is added to a running token count of all requests that is reset each minute. If at any time during that minute, the TPM rate limit value is reached, then further requests will receive a 429 response code until the counter resets.

> [!IMPORTANT]
> The token count used in the rate limit calculation is an estimate based in part on the character count of the API request. The rate limit token estimate isn't the same as the token calculation that is used for billing/determining that a request is below a model's input token limit. Due to the approximate nature of the rate limit token calculation, it's expected behavior that a rate limit can be triggered prior to what might be expected in comparison to an exact token count measurement for each request.  

RPM rate limits are based on the number of requests received over time. The rate limit expects that requests be evenly distributed over a one-minute period. If this average flow isn't maintained, then requests might receive a 429 response even though the limit isn't met when measured over the course of a minute. To implement this behavior, Azure OpenAI evaluates the rate of incoming requests over a small period of time, typically 1 or 10 seconds. If the number of requests received during that time exceeds what would be expected at the set RPM limit, then new requests receive a 429 response code until the next evaluation period. For example, if Azure OpenAI is monitoring request rate on 1-second intervals, then rate limiting occurs for a 600-RPM deployment if more than 10 requests are received during each 1-second period (600 requests per minute = 10 requests per second).

> [!NOTE]
> If you're using provisioned throughput units (PTU), the system calculates rate limits differently. For details, see the **Utilization-based request evaluation** section of [What is provisioned throughput for Foundry Models?](../concepts/provisioned-throughput.md).

### Rate limit response headers

Azure OpenAI includes rate limit information in the HTTP response headers of every API call. Use these headers to programmatically monitor your usage and proactively avoid 429 errors.

| Header | Example Value | Description |
|--------|---------------|-------------|
| `x-ratelimit-limit-requests` | `60` | Maximum number of requests permitted per minute for this deployment. |
| `x-ratelimit-limit-tokens` | `150000` | Maximum number of tokens permitted per minute for this deployment. |
| `x-ratelimit-remaining-requests` | `59` | Remaining requests before hitting the rate limit. |
| `x-ratelimit-remaining-tokens` | `149984` | Remaining tokens before hitting the rate limit. |
| `x-ratelimit-reset-requests` | `10` | Time until the request-based rate limit resets. |
| `x-ratelimit-reset-tokens` | `300` | Time until the token-based rate limit resets. |
| `retry-after-ms` | `2000` | Included in 429 responses. The recommended wait time (in milliseconds) before retrying. |

> [!TIP]
> Monitor `x-ratelimit-remaining-requests` and `x-ratelimit-remaining-tokens` in your application to detect when you're approaching limits and proactively throttle requests before receiving a 429.

---

### Rate limit best practices

To minimize issues related to rate limits, use the following techniques:

#### Optimize your requests

- **Set `max_tokens` to the minimum value that serves your scenario.** The rate limit token estimate includes `max_tokens`, even if your actual response is much shorter. For example, if you expect responses of about 200 tokens, don't set `max_tokens` to 4,000.
- **Set `best_of` to 1** unless you specifically need multiple completions. Each increment of `best_of` multiplies the token count against your rate limit.
- **Reduce prompt size** where possible. Shorter prompts use fewer tokens toward your rate limit.

#### Implement retry logic with exponential backoff

Automatically retry requests when you receive a 429 response. Use the `retry-after-ms` header value if present; otherwise, use exponential backoff with random jitter:

1. Wait a short, random delay after the first failure.
1. If the retry fails, double the delay (exponential backoff).
1. Add random jitter to prevent all clients from retrying at the same instant.
1. Set a maximum number of retries (for example, 5–10) to avoid infinite loops.

> [!IMPORTANT]
> Unsuccessful requests still count toward your per-minute rate limit. Continuously resending a request without backing off makes throttling worse.

**Option 1: Use the SDK's built-in retry (simplest - recommended)**

The Azure OpenAI Python SDK (`openai` v1.0+) has **built-in automatic retry with exponential backoff** for 429 and transient errors. The default is two retries. You can increase it:

```python
from openai import AzureOpenAI

# Set max_retries globally on the client (default is 2)
client = AzureOpenAI(
    azure_endpoint="https://<your-resource>.openai.azure.com/",
    api_key="<your-api-key>",
    api_version="2024-10-21",
    max_retries=5  # up to 5 retries with automatic exponential backoff
)

# All calls through this client automatically retry on 429
response = client.chat.completions.create(
    model="gpt-4o",  # deployment name
    messages=[{"role": "user", "content": "Hello"}]
)

# Or override per-request:
response = client.with_options(max_retries=8).chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
```

> [!NOTE]
> The SDK automatically respects `retry-after` headers and uses exponential backoff with jitter. For most applications, configuring `max_retries` on the client is sufficient - you don't need a third-party retry library.

**Option 2: Custom retry with the `tenacity` library (advanced)**

Use this when you need more control over retry behavior (for example, custom logging, selective exception handling, circuit breakers):

```python
import openai
from openai import AzureOpenAI
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

client = AzureOpenAI(
    azure_endpoint="https://<your-resource>.openai.azure.com/",
    api_key="<your-api-key>",
    api_version="2024-10-21",
    max_retries=0  # disable SDK built-in retry to avoid double-retrying
)

@retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
    retry=retry_if_exception_type(openai.RateLimitError),  # only retry on 429
    reraise=True
)
def chat_completion_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

response = chat_completion_with_backoff(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
```

> [!IMPORTANT]
> When using a custom retry library, set `max_retries=0` on the SDK client to disable its built-in retry. Otherwise, each attempt from tenacity might itself trigger up to two additional SDK retries, leading to far more requests than expected.

**Option 3: Manual implementation (no third-party library)**

```python
import time
import random
import openai
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://<your-resource>.openai.azure.com/",
    api_key="<your-api-key>",
    api_version="2024-10-21",
    max_retries=0  # disable SDK built-in retry
)

def retry_with_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 10,
    errors: tuple = (openai.RateLimitError,),
):
    """Retry a function with exponential backoff."""
    def wrapper(*args, **kwargs):
        num_retries = 0
        delay = initial_delay
        while True:
            try:
                return func(*args, **kwargs)
            except errors as e:
                num_retries += 1
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    ) from e
                delay *= exponential_base * (1 + jitter * random.random())
                time.sleep(delay)
            except Exception as e:
                raise e
    return wrapper

@retry_with_exponential_backoff
def chat_completion_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)
```

**C# example using Polly (v7):**

```csharp
using Azure;
using Azure.AI.OpenAI;
using Polly;

var retryPolicy = Policy
    .Handle<RequestFailedException>(ex => ex.Status == 429)
    .WaitAndRetryAsync(
        retryCount: 6,
        sleepDurationProvider: (retryAttempt, exception, context) =>
        {
            // Use retry-after-ms header if available
            if (exception is RequestFailedException rfEx)
            {
                var raw = rfEx.GetRawResponse();
                if (raw != null && raw.Headers.TryGetValue("retry-after-ms", out string value)
                    && int.TryParse(value, out int ms))
                {
                    return TimeSpan.FromMilliseconds(ms);
                }
            }
            // Otherwise, exponential backoff with jitter
            return TimeSpan.FromSeconds(Math.Pow(2, retryAttempt))
                + TimeSpan.FromMilliseconds(Random.Shared.Next(0, 1000));
        },
        onRetry: (exception, timespan, retryCount, context) =>
        {
            Console.WriteLine($"Retry {retryCount} after {timespan.TotalSeconds:F1}s due to: {exception.Message}");
        }
    );

// Usage
var endpoint = new Uri("https://<your-resource>.openai.azure.com/");
var credential = new AzureKeyCredential("<your-api-key>");
var client = new AzureOpenAIClient(endpoint, credential);

await retryPolicy.ExecuteAsync(async () =>
{
    var response = await client.GetChatClient("gpt-4o")
        .CompleteChatAsync([new UserChatMessage("Hello")]);
    Console.WriteLine(response.Value.Content[0].Text);
});
```

> [!NOTE]
> The Azure SDK for .NET also has built-in retry support. When constructing `AzureOpenAIClientOptions`, you can configure `options.Retry.MaxRetries` and `options.Retry.Mode = RetryMode.Exponential` instead of using Polly. Use Polly when you need more advanced patterns (circuit breakers, bulkheads, and so on).

#### Monitor and manage deployment-level usage

- **Check per-deployment TPM allocation**, not just subscription-level quota. You might have approved quota at the subscription level but hit 429s because the quota isn't allocated to the specific deployment receiving traffic.
- **Rebalance quota across deployments** based on observed usage. Use [Azure Monitor metrics](/azure/ai-services/openai/how-to/monitoring) to review 24-hour and seven-day usage trends and detect bursty patterns.
- Use quota management in the [Foundry portal](https://ai.azure.com) to increase TPM on high-traffic deployments and reduce TPM on underutilized ones.

#### Distribute traffic evenly

- **Avoid sharp spikes in workload.** RPM rate limits expect requests to be evenly distributed over each minute. Even if your total requests are below the per-minute limit, a burst within a 1-second or 10-second window can trigger a 429.
- **Ramp up traffic gradually** when onboarding new workloads or increasing load.
- **Spread requests across multiple deployments or regions** if your workload requires higher throughput than a single deployment supports.

#### Use asynchronous / batch processing where possible

If your use case doesn't require immediate responses, consider using asynchronous patterns:
- Queue requests and process them at a controlled rate.
- Use multiple deployments to parallelize processing without exceeding any single deployment's rate limit.

---

## Understanding 429 throttling errors and what to do 

A 429 error ("Too Many Requests") means the system rejected your request because a rate limit was exceeded or the system can't process your request at this time. **Not all 429 errors have the same root cause**, and the correct action depends on why the 429 occurred.

### Types of 429 errors

| Scenario | Error message indicator | Root cause | Recommended action |
|----------|------------------------|------------|-------------------|
| **Rate limit exceeded** | "Requests to … have been limited" or "Rate limit is exceeded" | Your requests exceeded the TPM or RPM rate limit for your deployment's allocated quota. | Increase the deployment's TPM allocation, rebalance quota across deployments, or [request a quota increase](https://aka.ms/oai/stuquotarequest). |
| **System capacity throttling** | "The service is temporarily unable to process your request" or "System is experiencing high demand" | Backend capacity is constrained. This condition is often transient. | Retry after the `retry-after-ms` delay. If persistent, consider upgrading to [Provisioned Throughput (PTU)](/azure/ai-services/openai/concepts/provisioned-throughput) for guaranteed capacity. |
| **Temporary rate limit adjustment** | 429 responses occur but your configured quota hasn't changed; `x-ratelimit-limit-tokens` in response headers is lower than your deployment's configured TPM | Standard (pay-as-you-go) deployments share a resource pool. When demand approaches capacity limits, the system temporarily reduces your deployment's effective rate limit to maintain reliability for all customers. This reduction is protective and temporary. | Retry with `retry-after-ms` backoff. The adjustment typically resolves within a few hours. For workloads requiring consistent throughput, consider [Provisioned Throughput (PTU)](/azure/ai-services/openai/concepts/provisioned-throughput). |
| **Token budget exceeded by request parameters** | Rate limit triggered but token usage metrics appear low | The rate limit calculation includes `max_tokens` and prompt estimate, not just billed tokens. A request with a high `max_tokens` value can consume rate limit budget even if the actual response is small. | Reduce `max_tokens` to match your expected response size. |

> [!IMPORTANT]
> Many customers misinterpret capacity-related 429s as quota problems, leading to incorrect remediation (for example, requesting quota increases when the issue is transient capacity pressure). Always check the error message and response headers to identify the root cause before taking action.

### Why you might see 429s even when token usage metrics are below quota

Azure OpenAI **rate limiting** and **usage metrics** aren't the same:

- **Token usage metrics** in Azure Monitor show **billed tokens from successfully processed requests**.
- **Rate limiting** applies to **API requests at the time they're received**, including requests that are later rejected or never billed.

Because of this difference, you can get 429 responses even when your token usage metrics look well below quota. Common reasons include:

- **`max_tokens` overestimation**: Rate limits are calculated using the *estimated maximum* token count (prompt + `max_tokens`), not the actual tokens generated.
- **Rejected requests**: Requests rejected due to input length limits (HTTP 400) might still count toward rate limiting but won't appear in billed token metrics.
- **Burst patterns**: RPM enforcement evaluates requests in small time windows (1–10 seconds). A burst of requests in a short window triggers throttling even if the per-minute total is within limits.
- **Temporary rate limit adjustment for service reliability**: Standard (pay-as-you-go) deployments share a common resource pool across customers. To keep service reliable and fair, the system continuously monitors demand across this shared pool. When demand from a deployment approaches or exceeds capacity limits, the system might **temporarily reduce the effective rate limit** for that deployment. During this adjustment period, requests that would have been accepted under normal conditions return 429 responses — even though your configured quota didn't change. This protective measure prevents service degradation for all customers sharing the resource pool. The adjustment is **temporary** and typically resolves within a few hours once traffic stabilizes. You can monitor for this condition by checking if your effective rate limit (visible in `x-ratelimit-limit-tokens` response headers) is lower than your configured TPM allocation.
- **Distributed enforcement**: Rate limit enforcement across distributed infrastructure might not be perfectly precise or immediately reflected in aggregated metrics.

> [!TIP]
> If you see 429 responses during a temporary rate limit adjustment period:
> 1. **Retry with backoff** — honor the `retry-after-ms` header. The adjustment is temporary and will resolve as demand stabilizes.
> 1. **Spread traffic** — if possible, distribute requests across multiple deployments or regions.
> 1. **Review your traffic pattern** — sustained heavy bursts are the most common trigger. Gradually ramping workloads reduces the likelihood of adjustments.
> 1. **Consider Provisioned Throughput (PTU)** — for production workloads that need consistent throughput without shared-pool variability, [Provisioned Throughput](/azure/ai-services/openai/concepts/provisioned-throughput) provides dedicated capacity with guaranteed rate limits.

**What to rely on:**
- Use **token usage metrics** to understand billed consumption.
- Use **HTTP response codes (429)** and **response headers** (`x-ratelimit-remaining-*`, `x-ratelimit-limit-*`) to detect and respond to rate limit enforcement in real time.
- Compare `x-ratelimit-limit-tokens` in response headers against your configured TPM to detect if a temporary adjustment is active.

### When to retry vs. when to escalate

| Situation | Action |
|-----------|--------|
| Occasional 429s that resolve with `retry-after-ms` backoff | **Retry** — this behavior is normal and expected for shared (Standard) deployments. |
| 429s during development or testing | **Often acceptable** — non-production 429s might be intentional cost guardrails. |
| Sustained 429s in production, below approved quota | **Escalate** — open a [support request](/azure/azure-portal/supportability/how-to-create-azure-support-request) for engineering investigation. |
| Rate limit increases not reflected in effective limits | **Escalate** — verify quota allocation at the deployment level first, then escalate if the issue persists. |
| Latency-sensitive or mission-critical production workloads experiencing frequent 429s | **Upgrade** — consider [Provisioned Throughput (PTU)](/azure/ai-services/openai/concepts/provisioned-throughput) for guaranteed capacity and latency SLA. |

> [!NOTE]
> Standard (pay-as-you-go) deployments use a shared resource pool. Throttling protects overall service reliability for all users. Occasional transient 429s are expected behavior, not a service defect. For workloads that require predictable latency and guaranteed throughput, Provisioned Throughput (PTU) is the recommended deployment type.



## Programmatically check quota and capacity

In addition to the [Foundry portal](https://ai.azure.com/resource/quota), you can use two Azure Resource Manager REST APIs to programmatically check your subscription's quota consumption and available model capacity.

### Choose the right API

| | **Usages API** | **Model Capacities API** |
|---|---|---|
| **Question it answers** | How much of my quota have I consumed vs. my limit? | How much deployable capacity is available for a specific model? |
| **Scope** | Subscription + location | Subscription (all locations at once) |
| **Input** | Location only | Model name, version, and format |
| **Returns** | Every quota line in that region — current usage and limit | Available capacity per location and deployment type for one model |
| **Typical use case** | Monitor consumption, trigger alerts when approaching limits | Pre-check capacity before creating or scaling a deployment |
| **API reference** | [Usages - List](/rest/api/aiservices/accountmanagement/usages/list) | [Model Capacities - List](/rest/api/aiservices/accountmanagement/model-capacities/list) |

Use the **Usages API** when you need a ledger view of what you've consumed and what's left. Use the **Model Capacities API** when you want to know where you _can_ deploy a model and how much capacity is available in each location.

> [!NOTE]
> Both APIs return information for all models associated with your subscription, including [retired models](../concepts/model-retirements.md) that are no longer available for new deployments.

### Usages API

The Usages API returns every quota line for a given region, including your current consumption (`currentValue`) and assigned limit.

**Request**:

```http
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{location}/usages?api-version=2024-10-01
```

**Example — check quota usage in East US**:

# [Python](#tab/python)

```python
import requests
import json
from azure.identity import DefaultAzureCredential

subscription_id = "<your-subscription-id>"
location = "eastus"

credential = DefaultAzureCredential()
token = credential.get_token("https://management.azure.com/.default")
headers = {"Authorization": f"Bearer {token.token}"}

url = (
    f"https://management.azure.com/subscriptions/{subscription_id}"
    f"/providers/Microsoft.CognitiveServices/locations/{location}/usages"
    f"?api-version=2024-10-01"
)

response = requests.get(url, headers=headers)
usages = response.json()

# Show quota lines that have a non-zero limit
for item in usages["value"]:
    if item["limit"] > 0:
        print(f"{item['name']['localizedValue']}: {item['currentValue']}/{item['limit']}")
```

# [Bash](#tab/bash)

```bash
SUBSCRIPTION_ID="<your-subscription-id>"
LOCATION="eastus"

az rest --method get \
  --url "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/providers/Microsoft.CognitiveServices/locations/$LOCATION/usages?api-version=2024-10-01"
```

# [Sample output](#tab/output)

```json
{
  "value": [
    {
      "name": {
        "value": "OpenAI.Standard.gpt-4o",
        "localizedValue": "Tokens Per Minute (thousands) - gpt-4o"
      },
      "currentValue": 0,
      "limit": 150,
      "unit": "Count"
    }
  ]
}
```

---

**Key fields**:

| Field | Description |
|---|---|
| `name.value` | Quota name in the format `{Provider}.{DeploymentType}.{Model}` |
| `name.localizedValue` | Human-readable description including the unit |
| `currentValue` | How much of this quota is currently consumed by deployments |
| `limit` | Your subscription's quota limit for this model and deployment type |

### Model Capacities API

The Model Capacities API returns the available deployment capacity for a specific model across all locations and deployment types in your subscription.

**Request**:

```http
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/modelCapacities?api-version=2024-10-01&modelFormat={format}&modelName={name}&modelVersion={version}
```

**Example — check where gpt-4o capacity is available**:

# [Python](#tab/python)

```python
import requests
import json
from azure.identity import DefaultAzureCredential

subscription_id = "<your-subscription-id>"
model_name = "gpt-4o"
model_version = "2024-08-06"

credential = DefaultAzureCredential()
token = credential.get_token("https://management.azure.com/.default")
headers = {"Authorization": f"Bearer {token.token}"}

url = (
    f"https://management.azure.com/subscriptions/{subscription_id}"
    f"/providers/Microsoft.CognitiveServices/modelCapacities"
    f"?api-version=2024-10-01"
    f"&modelFormat=OpenAI&modelName={model_name}&modelVersion={model_version}"
)

response = requests.get(url, headers=headers)
capacities = response.json()

# Show locations with available capacity for Standard deployments
for item in capacities["value"]:
    props = item["properties"]
    if props["availableCapacity"] > 0 and "Standard" in props["skuName"]:
        print(f"{item['location']} ({props['skuName']}): {props['availableCapacity']} available")
```

# [Bash](#tab/bash)

```bash
SUBSCRIPTION_ID="<your-subscription-id>"

az rest --method get \
  --url "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/providers/Microsoft.CognitiveServices/modelCapacities?api-version=2024-10-01&modelFormat=OpenAI&modelName=gpt-4o&modelVersion=2024-08-06"
```

# [Sample output](#tab/output)

```json
{
  "value": [
    {
      "location": "eastus",
      "properties": {
        "model": {
          "name": "gpt-4o",
          "format": "OpenAI",
          "version": "2024-08-06"
        },
        "skuName": "Standard",
        "availableCapacity": 150,
        "availableFinetuneCapacity": 0
      }
    }
  ]
}
```

---

**Key fields**:

| Field | Description |
|---|---|
| `location` | Azure region |
| `properties.skuName` | Deployment type (Standard, GlobalStandard, DataZoneStandard, ProvisionedManaged, etc.) |
| `properties.availableCapacity` | Capacity units available in your subscription for this model, location, and deployment type |
| `properties.availableFinetuneCapacity` | Fine-tuning capacity available (when applicable) |

## Automate deployment

To programmatically create Azure OpenAI deployments and assign tokens-per-minute (TPM) quota using REST, Azure CLI, Azure PowerShell, ARM, Bicep, or Terraform, see [Automate Azure OpenAI deployments with quota in Microsoft Foundry](../how-to/automate-quota-deployments.md).

## Resource deletion

When an attempt to delete an Azure OpenAI resource is made from the Azure portal if any deployments are still present deletion is blocked until the associated deployments are deleted. Deleting the deployments first allows quota allocations to be properly freed up so they can be used on new deployments.

However, if you delete a resource using the REST API or some other programmatic method, this bypasses the need to delete deployments first. When this occurs, the associated quota allocation will remain unavailable to assign to a new deployment for 48 hours until the resource is purged. To trigger an immediate purge for a deleted resource to free up quota, follow the [purge a deleted resource instructions](/azure/ai-services/manage-resources?tabs=azure-portal#purge-a-deleted-resource).

## Next steps

- To review quota defaults for Azure OpenAI, consult the [quotas & limits article](../quotas-limits.md)
