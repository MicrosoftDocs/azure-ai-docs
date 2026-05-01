---
title: "Manage Azure OpenAI in Microsoft Foundry Models quota (classic)"
description: "Learn how to use Azure OpenAI to control your deployments rate limits. (classic)"
author: mrbullwinkle
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 05/01/2026
ms.author: mbullwin
---

# Manage Azure OpenAI in Microsoft Foundry Models quota (classic)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Quota provides the flexibility to actively manage the allocation of rate limits across the deployments within your subscription. This article walks through the process of managing your Azure OpenAI quota.

## Prerequisites

> [!IMPORTANT]
> For any task that requires viewing available quota we recommend using the **Cognitive Services Usages Reader** role. This role provides the minimal access necessary to view quota usage across an Azure subscription. To learn more about this role and the other roles you'll need to access Azure OpenAI, consult our [Azure role-based access control guide](./role-based-access-control.md). 
>
> This role can be found in the Azure portal under **Subscriptions** > **Access control (IAM)** > **Add role assignment** > search for **Cognitive Services Usages Reader**. This role **must be applied at the subscription level**, it doesn't exist at the resource level.
>
> If you don't wish to use this role, the subscription **Reader** role will provide equivalent access, but it will also grant read access beyond the scope of what is needed for viewing quota and model deployment.

## Introduction to quota

Azure OpenAI's quota feature enables assignment of rate limits to your deployments, up-to a global limit called your *quota*. Quota is assigned to your subscription on a per-region, per-model, per-deployment-type basis in units of **Tokens-per-Minute (TPM)**. When you onboard a subscription to Azure OpenAI, you'll receive default quota for most available models. Then, you'll assign TPM to each deployment as it is created, and the available quota for that model will be reduced by that amount. You can continue to create deployments and assign them TPM until you reach your quota limit. Once that happens, you can only create new deployments of that model by reducing the TPM assigned to other deployments of the same model (thus freeing TPM for use), or by requesting and being approved for a model quota increase in the desired region.

> [!NOTE]
> With a quota of 240,000 TPM for GPT-4o in East US, a customer can create a single deployment of 240 K TPM, 2 deployments of 120 K TPM each, or any number of deployments in one or multiple Azure OpenAI resources as long as their TPM adds up to less than 240 K total in that region.

When a deployment is created, the assigned TPM will directly map to the tokens-per-minute rate limit enforced on its inferencing requests. A **Requests-Per-Minute (RPM)** rate limit will also be enforced whose value is set proportionally to the TPM assignment using the following ratio:

> [!IMPORTANT]
> The ratio of Requests Per Minute (RPM) to Tokens Per Minute (TPM) for quota can vary by model. When you deploy a model programmatically or [request a quota increase](https://aka.ms/oai/stuquotarequest) you don't have granular control over TPM and RPM as independent values. Quota is allocated in terms of units of capacity which have corresponding amounts of RPM & TPM:
>
> | Model                  | Capacity   | Requests Per Minute (RPM)  | Tokens Per Minute (TPM) |
> |------------------------|:----------:|:--------------------------:|:-----------------------:|
> | **Older chat models:** | 1 Unit     | 6 RPM                      | 1,000 TPM               |
> | **o1 & o1-preview:**   | 1 Unit     | 1 RPM                      | 6,000 TPM               |
> | **o3**                 | 1 Unit     | 1 RPM                      | 1,000 TPM               |
> | **o4-mini**            | 1 Unit     | 1 RPM                      | 1,000 TPM               |
> | **o3-mini:**           | 1 Unit     | 1 RPM                      | 10,000 TPM              |
> | **o1-mini:**           | 1 Unit     | 1 RPM                      | 10,000 TPM              |
> | **o3-pro:**            | 1 Unit     | 1 RPM                      | 10,000 TPM              |
>
> This is particularly important for programmatic model deployment as changes in RPM/TPM ratio can result in accidental  misallocation of quota.

The flexibility to distribute TPM globally within a subscription and region has allowed Azure OpenAI to loosen other restrictions:

- The maximum resources per region are increased to 30.
- The limit on creating no more than one deployment of the same model in a resource has been removed.

## Assign quota

When you create a model deployment, you have the option to assign Tokens-Per-Minute (TPM) to that deployment. TPM can be modified in increments of 1,000, and will map to the TPM and RPM rate limits enforced on your deployment, as discussed above.

To create a new deployment from within the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) select **Deployments** > **Deploy model** > **Deploy base model** > **Select Model** > **Confirm**.

Post deployment you can adjust your TPM allocation by selecting and editing your model from the **Deployments** page in [Foundry portal](https://ai.azure.com/?cid=learnDocs). You can also modify this setting from the **Management** > **Model quota** page.

> [!IMPORTANT]
> Quotas and limits are subject to change, for the most up-date-information consult our [quotas and limits article](../quotas-limits.md).

## Request more quota

[!INCLUDE [quota-increase-request](../../../foundry/openai/includes/quota-increase-request.md)]

## Model specific settings

Different model deployments, also called model classes have unique max TPM values that you're now able to control. **This represents the maximum amount of TPM that can be allocated to that type of model deployment in a given region.** 

All other model classes have a common max TPM value.

> [!NOTE]
> Quota Tokens-Per-Minute (TPM) allocation isn't related to the max input token limit of a model. Model input token limits are defined in the [models table](../../foundry-models/concepts/models-sold-directly-by-azure.md) and aren't impacted by changes made to TPM.  

## View and request quota

For an all up view of your quota allocations across deployments in a given region, select **Management** > **Quota** in [Foundry portal](https://ai.azure.com/?cid=learnDocs):

- **Deployment**: Model deployments divided by model class.
- **Quota type**: There's one quota value per region for each model type. The quota covers all versions of that model.  
- **Quota allocation**: For the quota name, this shows how much quota is used by deployments and the total quota approved for this subscription and region. This amount of quota used is also represented in the bar graph.
- **Request Quota**: The icon navigates to [this form](https://aka.ms/oai/stuquotarequest) where requests to increase quota can be submitted.

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

**Option 3: Manual implementation (no third-party library):**

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
| **Temporary rate limit adjustment** | 429 responses occur but your configured quota hasn't changed; `x-ratelimit-limit-tokens` in response headers is lower than your deployment's configured TPM | Standard (PayGo) deployments share a resource pool. When demand approaches capacity limits, the system temporarily reduces your deployment's effective rate limit to maintain reliability for all customers. This reduction is protective and temporary. | Retry with `retry-after-ms` backoff. The adjustment typically resolves within a few hours. For workloads requiring consistent throughput, consider [Provisioned Throughput (PTU)](/azure/ai-services/openai/concepts/provisioned-throughput). |
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
- **Temporary rate limit adjustment for service reliability**: Standard (Pay-As-You-Go) deployments share a common resource pool across customers. To keep service reliable and fair, the system continuously monitors demand across this shared pool. When demand from a deployment approaches or exceeds capacity limits, the system might **temporarily reduce the effective rate limit** for that deployment. During this adjustment period, requests that would have been accepted under normal conditions return 429 responses — even though your configured quota didn't change. This protective measure prevents service degradation for all customers sharing the resource pool. The adjustment is **temporary** and typically resolves within a few hours once traffic stabilizes. You can monitor for this condition by checking if your effective rate limit (visible in `x-ratelimit-limit-tokens` response headers) is lower than your configured TPM allocation.
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
| Sustained 429s in production, below approved quota | **Escalate** — open a [support request](/azure/ai-services/openai/how-to/get-support) for engineering investigation. |
| Rate limit increases not reflected in effective limits | **Escalate** — verify quota allocation at the deployment level first, then escalate if the issue persists. |
| Latency-sensitive or mission-critical production workloads experiencing frequent 429s | **Upgrade** — consider [Provisioned Throughput (PTU)](/azure/ai-services/openai/concepts/provisioned-throughput) for guaranteed capacity and latency SLA. |

> [!NOTE]
> Standard (PayGo) deployments use a shared resource pool. Throttling protects overall service reliability for all users. Occasional transient 429s are expected behavior, not a service defect. For workloads that require predictable latency and guaranteed throughput, Provisioned Throughput (PTU) is the recommended deployment type.



## Automate deployment

This section contains brief example templates to help get you started programmatically creating deployments that use quota to set TPM rate limits. With the introduction of quota you must use API version `2023-05-01` for resource management related activities. This API version is only for managing your resources, and doesn't impact the API version used for inferencing calls like completions, chat completions, embedding, image generation, etc.

# [REST](#tab/rest)

### Deployment

```http
PUT https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/deployments/{deploymentName}?api-version=2023-05-01
```

**Path parameters**

| Parameter | Type | Required? |  Description |
|--|--|--|--|
| ```accountName``` | string |  Required | The name of your Azure OpenAI Resource. |
| ```deploymentName``` | string | Required | The deployment name you chose when you deployed an existing model or the name you would like a new model deployment to have.   |
| ```resourceGroupName``` | string |  Required | The name of the associated resource group for this model deployment. |
| ```subscriptionId``` | string |  Required | Subscription ID for the associated subscription. |
| ```api-version``` | string | Required |The API version to use for this operation. This follows the YYYY-MM-DD format. |

**Supported versions**

- `2023-05-01` [Swagger spec](https://github.com/Azure/azure-rest-api-specs/blob/1e71ad94aeb8843559d59d863c895770560d7c93/specification/cognitiveservices/resource-manager/Microsoft.CognitiveServices/stable/2023-05-01/cognitiveservices.json)

**Request body**

This is only a subset of the available request body parameters. For the full list of the parameters, you can refer to the [REST API reference documentation](/rest/api/aiservices/accountmanagement/deployments/create-or-update?tabs=HTTP).

|Parameter|Type| Description |
|--|--|--|
|sku | Sku | The resource model definition representing SKU.|
|capacity|integer|This represents the amount of [quota](../how-to/quota.md) you're assigning to this deployment. A value of 1 equals 1,000 Tokens per Minute (TPM). A value of 10 equals 10k Tokens per Minute (TPM).|

#### Example request

```Bash
curl -X PUT https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource-group-temp/providers/Microsoft.CognitiveServices/accounts/docs-openai-test-001/deployments/gpt-4o-test-deployment?api-version=2023-05-01 \
  -H "Content-Type: application/json" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' \
  -d '{"sku":{"name":"Standard","capacity":10},"properties": {"model": {"format": "OpenAI","name": "gpt-4o","version": "2024-11-20"}}}'
```

> [!NOTE]
> There are multiple ways to generate an authorization token. The easiest method for initial testing is to launch the Cloud Shell from the [Azure portal](https://portal.azure.com). Then run [`az account get-access-token`](/cli/azure/account?view=azure-cli-latest&preserve-view=true#az-account-get-access-token). You can use this token as your temporary authorization token for API testing.

For more information, see the REST API reference documentation for [usages](/rest/api/aiservices/accountmanagement/usages/list?branch=main&tabs=HTTP) and [deployment](/rest/api/aiservices/accountmanagement/deployments/create-or-update).

### Usage

To query your quota usage in a given region, for a specific subscription

```html
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{location}/usages?api-version=2023-05-01
```
**Path parameters**

| Parameter | Type | Required? |  Description |
|--|--|--|--|
| ```subscriptionId``` | string |  Required | Subscription ID for the associated subscription. |
|```location```        | string | Required | Location to view usage for ex: `eastus` |
| ```api-version``` | string | Required |The API version to use for this operation. This follows the YYYY-MM-DD format. |

**Supported versions**

- `2023-05-01` [Swagger spec](https://github.com/Azure/azure-rest-api-specs/blob/1e71ad94aeb8843559d59d863c895770560d7c93/specification/cognitiveservices/resource-manager/Microsoft.CognitiveServices/stable/2023-05-01/cognitiveservices.json)

#### Example request

```Bash
curl -X GET https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.CognitiveServices/locations/eastus/usages?api-version=2023-05-01 \
  -H "Content-Type: application/json" \
  -H 'Authorization: Bearer YOUR_AUTH_TOKEN' 
```

# [Azure CLI](#tab/cli)

Install the [Azure CLI](/cli/azure/install-azure-cli). Quota requires `Azure CLI version 2.51.0`. If you already have Azure CLI installed locally run `az upgrade` to update to the latest version.

To check which version of Azure CLI you're running use `az version`. Azure Cloud Shell is currently still running 2.50.0 so in the interim local installation of Azure CLI is required to take advantage of the latest Azure OpenAI features.

### Deployment

```azurecli
az cognitiveservices account deployment create --model-format
                                               --model-name
                                               --model-version
                                               --name
                                               --resource-group
                                               [--capacity]
                                               [--deployment-name]
                                               [--scale-capacity]
                                               [--scale-settings-scale-type {Manual, Standard}]
                                               [--sku]
```

To sign into your local installation of the CLI, run the [`az login`](/cli/azure/reference-index#az-login) command:

```azurecli
az login
```

<!--TODO:You can also use the green **Try It** button to run these commands in your browser in the Azure Cloud Shell.-->

By setting sku-capacity to 10 in the command below this deployment will be set with a 10K TPM limit.

```azurecli
az cognitiveservices account deployment create -g test-resource-group -n test-resource-name --deployment-name test-deployment-name --model-name gpt-4o --model-version "2024-11-20" --model-format OpenAI --sku-capacity 10 --sku-name "Standard"
```

### Usage

To [query your quota usage](/cli/azure/cognitiveservices/usage?view=azure-cli-latest&preserve-view=true) in a given region, for a specific subscription

```azurecli
az cognitiveservices usage list --location
```

### Example

```azurecli
az cognitiveservices usage list -l eastus
```

This command runs in the context of the currently active subscription for Azure CLI. Use `az-account-set --subscription` to [modify the active subscription](/cli/azure/manage-azure-subscriptions-azure-cli#change-the-active-subscription).

For more information, see the [Azure CLI reference documentation](/cli/azure/cognitiveservices/account/deployment?view=azure-cli-latest&preserve-view=true)

# [Azure PowerShell](#tab/powershell)

Install the latest version of the [Az PowerShell module](/powershell/azure/install-azure-powershell). If you already have the Az PowerShell module installed locally, run `Update-Module -Name Az` to update to the latest version.

To check which version of the Az PowerShell module you're running, use `Get-InstalledModule -Name Az`. Azure Cloud Shell is currently running a version of Azure PowerShell that can take advantage of the latest Azure OpenAI features.

### Deployment

```azurepowershell
New-AzCognitiveServicesAccountDeployment
   [-ResourceGroupName] <String>
   [-AccountName] <String>
   [-Name] <String>
   [-Properties] <DeploymentProperties>
   [-Sku] <Sku>
   [-DefaultProfile <IAzureContextContainer>]
   [-WhatIf]
   [-Confirm]
   [<CommonParameters>]
```

To sign into your local installation of Azure PowerShell, run the [Connect-AzAccount](/powershell/module/az.accounts/connect-azaccount) command:

```azurepowershell
Connect-AzAccount
```

By setting Sku Capacity to 10 in the command below, this deployment is set to a 10K TPM limit.

```azurepowershell-interactive
$cognitiveServicesDeploymentParams = @{
    ResourceGroupName = 'test-resource-group'
    AccountName = 'test-resource-name'
    Name = 'test-deployment-name'
    Properties = @{
        Model = @{
            Name = 'gpt-4o'
            Version = '2024-11-20'
            Format  = 'OpenAI'
        }
    }
    Sku = @{
        Name = 'Standard'
        Capacity = '10'
    }
}
New-AzCognitiveServicesAccountDeployment @cognitiveServicesDeploymentParams
```

### Usage

To [query your quota usage](/powershell/module/az.cognitiveservices/get-azcognitiveservicesusage) in a given region for a specific subscription:

```azurepowershell
Get-AzCognitiveServicesUsage -Location <location>
```

### Example

```azurepowershell-interactive
Get-AzCognitiveServicesUsage -Location eastus
```

This command runs in the context of the currently active subscription for Azure PowerShell. Use `Set-AzContext` to [modify the active subscription](/powershell/azure/manage-subscriptions-azureps#change-the-active-subscription).

For more information on `New-AzCognitiveServicesAccountDeployment` and `Get-AzCognitiveServicesUsage`, see [Azure PowerShell reference documentation](/powershell/module/az.cognitiveservices/).

# [Azure Resource Manager](#tab/arm)

```json
//
// This Azure Resource Manager template shows how to use the new schema introduced in the 2023-05-01 API version to 
// create deployments that set the model version and the TPM limits for standard deployments.
//
{
    "type": "Microsoft.CognitiveServices/accounts/deployments",
    "apiVersion": "2023-05-01",
    "name": "arm-je-aoai-test-resource/arm-je-std-deployment",    // Update reference to parent Azure OpenAI resource
    "dependsOn": [
        "[resourceId('Microsoft.CognitiveServices/accounts', 'arm-je-aoai-test-resource')]"  // Update reference to parent Azure OpenAI resource
    ],
    "sku": {
        "name": "Standard",      
        "capacity": 10            // The deployment will be created with a 10K TPM limit
    },
    "properties": {
        "model": {
            "format": "OpenAI",
            "name": "gpt-4o",
            "version": "2024-11-20"       
        }
    }
}
```

For more information, see the [full Azure Resource Manager reference documentation](/azure/templates/microsoft.cognitiveservices/accounts/deployments?pivots=deployment-language-arm-template).

# [Bicep](#tab/bicep)

```bicep
//
// This Bicep template shows how to use the new schema introduced in the 2023-05-01 API version to 
// create deployments that set the model version and the TPM limits for standard deployments.
//
resource arm_je_std_deployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: arm_je_aoai_resource   // Replace this with a reference to the parent Azure OpenAI resource
  name: 'arm-je-std-deployment'
  sku: {
    name: 'Standard'            
    capacity: 10                 // The deployment will be created with a 10K TPM limit
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-11-20'          
    }
  }
}
```

For more information, see the [full Bicep reference documentation](/azure/templates/microsoft.cognitiveservices/accounts/deployments?pivots=deployment-language-bicep).

# [Terraform](#tab/terraform)

```terraform
# This Terraform template shows how to use the new schema introduced in the 2023-05-01 API version to 
# create deployments that set the model version and the TPM limits for standard deployments.
# 
# The new schema is not yet available in the AzureRM provider (target v4.0), so this template uses the AzAPI
# provider, which provides a Terraform-compatible interface to the underlying ARM structures.
# 
# For more details on these providers:
#     AzureRM: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
#     AzAPI: https://registry.terraform.io/providers/azure/azapi/latest/docs
#

# 
terraform {
  required_providers {
    azapi   = { source  = "Azure/azapi" }
    azurerm = { source  = "hashicorp/azurerm" }
  }
}

provider "azapi" {
  # Insert auth info here as necessary
}

provider "azurerm" {
    # Insert auth info here as necessary  
    features {
    }
}

# 
# To create a complete example, AzureRM is used to create a new resource group and Azure OpenAI Resource
# 
resource "azurerm_resource_group" "TERRAFORM-AOAI-TEST-GROUP" {
  name     = "TERRAFORM-AOAI-TEST-GROUP"
  location = "canadaeast"
}

resource "azurerm_cognitive_account" "TERRAFORM-AOAI-TEST-ACCOUNT" {
  name                  = "terraform-aoai-test-account"
  location              = "canadaeast"
  resource_group_name   = azurerm_resource_group.TERRAFORM-AOAI-TEST-GROUP.name
  kind                  = "OpenAI"
  sku_name              = "S0"
  custom_subdomain_name = "terraform-test-account-"
  }

# 
# AzAPI is used to create the deployment so that the TPM limit and model versions can be set
#
resource "azapi_resource" "TERRAFORM-AOAI-STD-DEPLOYMENT" {
  type      = "Microsoft.CognitiveServices/accounts/deployments@2023-05-01"
  name      = "TERRAFORM-AOAI-STD-DEPLOYMENT"
  parent_id = azurerm_cognitive_account.TERRAFORM-AOAI-TEST-ACCOUNT.id

  body = jsonencode({
    sku = {                            # The sku object specifies the deployment type and limit in 2023-05-01
        name = "Standard",             
        capacity = 10                  # This deployment will be set with a 10K TPM limit
    },
    properties = {
        model = {
            format = "OpenAI",
            name = "gpt-4o",
            version = "2024-11-20"           
        }
    }
  })
}
```

For more information, see the [full Terraform reference documentation](/azure/templates/microsoft.cognitiveservices/accounts/deployments?pivots=deployment-language-terraform).

---

## Resource deletion

When an attempt to delete an Azure OpenAI resource is made from the Azure portal if any deployments are still present deletion is blocked until the associated deployments are deleted. Deleting the deployments first allows quota allocations to be properly freed up so they can be used on new deployments.

However, if you delete a resource using the REST API or some other programmatic method, this bypasses the need to delete deployments first. When this occurs, the associated quota allocation will remain unavailable to assign to a new deployment for 48 hours until the resource is purged. To trigger an immediate purge for a deleted resource to free up quota, follow the [purge a deleted resource instructions](/azure/ai-services/manage-resources?tabs=azure-portal#purge-a-deleted-resource).

## Next steps

- To review quota defaults for Azure OpenAI, consult the [quotas & limits article](../quotas-limits.md)
