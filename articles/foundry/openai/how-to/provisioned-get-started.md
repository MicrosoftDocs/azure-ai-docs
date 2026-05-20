---
title: Operate provisioned throughput deployments in production
description: "Learn to benchmark, monitor utilization, handle high load, and scale provisioned throughput deployments in production. Get started today."
ai-usage: ai-assisted
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-models
ms.custom:
  - openai, pilot-ai-workflow-jan-2026
  - classic-and-new
  - doc-kit-assisted
ms.topic: how-to
author: msakande
ms.author: mopeakande
ms.reviewer: seramasu
reviewer: rsethur
ms.date: 05/18/2026
recommendations: false
#customerIntent: As a developer with a provisioned throughput deployment, I want to benchmark, monitor, and scale it so I can run it reliably in production.
---

# Operate provisioned deployments in production

This article covers the operational tasks for running provisioned throughput deployments in production: sizing workloads, benchmarking, monitoring utilization, handling high load, and scaling. If you don't have a deployment yet, start with [Quickstart: Create a provisioned throughput deployment](../provisioned-quickstart.md).

This article assumes familiarity with the concepts in [What is provisioned throughput?](../concepts/provisioned-throughput.md) and the billing details in [PTU costs and billing](./provisioned-throughput-onboarding.md).

## Prerequisites

- An Azure subscription — [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Azure Contributor or Cognitive Services Contributor role.
- A [Foundry resource](../../../foundry-classic/openai/how-to/create-resource.md) in each region where you intend to create a deployment. Foundry resources support multiple deployment types simultaneously. You don't need to dedicate a separate resource to provisioned deployments.
- (For Azure CLI-based deployment only) [Azure CLI installed](/cli/azure/install-azure-cli).

## Estimate PTU requirements

For the estimation formulas, worked example, and capacity calculator walkthrough, see [Determine PTU requirements for a workload](./provisioned-throughput-onboarding.md#determine-ptu-requirements-for-a-workload).

## Check and request PTU quota

PTU quota is granted per subscription, per region, and limits the total PTUs you can deploy in that region across all models. For details on how quota and capacity relate, see [PTU quota vs. capacity](../concepts/provisioned-throughput.md#quota-and-capacity).

To check current usage or request additional quota:

1. Go to **Operate** > **Quota** > **Provisioned throughput unit** in the [Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. Select the desired subscription and region to view current usage.
1. To request more quota, select **Request Quota** and complete the form.

## Create a provisioned deployment

To create a provisioned deployment, see [Quickstart: Create a provisioned throughput deployment](../provisioned-quickstart.md).

PTU quota is shared across all provisioned deployments of the same deployment type within a region. If you have remaining quota after your initial deployment, you can use it to deploy other supported models without requesting more quota. Check your quota usage in the **Quota** pane under **Operate** in the [Foundry portal](https://ai.azure.com/?cid=learnDocs). 

You can manage your quota by requesting additional quota, or by deleting existing deployments to free up PTUs for new deployments.

## Scale your deployment

You can increase or decrease the PTU count of a provisioned deployment at any time through the Foundry portal or the Azure CLI. For capacity constraints on scale-up, billing adjustment timing, and the effect on existing reservations, see [Scale provisioned deployments](./provisioned-throughput-onboarding.md#scale-provisioned-deployments).

## Purchase a reservation

After your provisioned deployment is in place, consider purchasing an Azure Reservation to get a discounted rate on your PTU billing. A reservation provides a significant discount over hourly billing for deployments you plan to run for more than a few days.

> [!IMPORTANT]
> Capacity availability is dynamic. Always create your deployments first to confirm capacity is available, then purchase the reservation to cover the PTUs you've deployed. This approach ensures you can take full advantage of the reservation discount and prevents you from committing to PTUs you can't use.

For guidance on sizing and purchasing a reservation, see [Azure Reservations for provisioned throughput](./provisioned-throughput-onboarding.md#azure-reservations-for-provisioned-throughput).

## Make inference calls

For inference code examples using your provisioned deployment, see the [quickstart](../provisioned-quickstart.md#make-an-inference-call). The inferencing code for provisioned deployments is the same as for any other deployment type. Use your deployment name (not the model name) as the `model` parameter value.

## Run a benchmark

The exact performance and throughput capabilities of your deployment depend on the number of PTUs deployed, the kind of requests you make, and your workload shape (including prompt size, generation size, call rate, and similar factors). The best way to determine the throughput for your workload is to run a benchmark on your own data.

The **benchmarking tool** provides preconfigured workload shapes and outputs key performance metrics. Use this tool to run benchmarks on your deployment. For details and configuration settings, see the [azure-openai-benchmark](https://github.com/Azure/azure-openai-benchmark) repository on GitHub.

Recommended benchmarking workflow:

1. Estimate your PTU requirements using the capacity calculator.
1. Run a benchmark with this traffic shape for at least 10 minutes to observe steady-state results.
1. Observe utilization, tokens processed, and call rate from the benchmark tool and Azure Monitor.
1. Run a benchmark with your own traffic shape and workload using your client implementation. Implement retry logic using an Azure OpenAI client library or custom retry logic.

## Measure deployment utilization

When you create a provisioned deployment, the service allocates a fixed amount of inference throughput. To track how much of that capacity your workload consumes, use the **Provisioned-managed utilization V2** metric in Azure Monitor.

PTU utilization is defined as:

*PTU deployment utilization = (PTUs consumed in the time period) / (PTUs deployed in the time period)*

To view the metric:

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Navigate to your Foundry resource and select **Metrics** in the left navigation.
1. Select the **Provisioned-managed utilization V2** metric.
1. If you have more than one deployment in the resource, select **Apply Splitting** to see values split by deployment.

:::image type="content" source="../media/provisioned/azure-monitor-utilization.jpg" alt-text="Screenshot of the Provisioned-managed utilization V2 metric displayed on the resource metrics blade in the Azure portal." lightbox="../media/provisioned/azure-monitor-utilization.jpg":::

### How utilization works

Each customer has a set amount of capacity they can use on a provisioned deployment. To maintain utilization below 100% while allowing some burstiness in traffic, the service uses a variation of the leaky bucket algorithm as follows:

1. **Throttling at 100%**: When a request is made, if current utilization is at 100%, the service returns HTTP 429 immediately, with `retry-after-ms` and `retry-after` response headers indicating how long to wait.
1. **Request estimate**: For each incoming request, the service estimates the compute cost by combining the prompt token count (less any cached tokens) and the specified `max_tokens` in the call. Cached tokens receive a 100% discount and don't contribute to utilization. If `max_tokens` isn't specified, the service estimates a value—this can lead to lower concurrency than expected when actual generated tokens are fewer than estimated. For highest concurrency, set `max_tokens` as close as possible to your true generation size.
1. **Post-request correction**: When a request finishes, the service corrects the utilization estimate using actual token counts. If the actual compute cost exceeds the estimate, the difference is added to utilization; if it's less, the difference is subtracted.
1. **Continuous drain**: Utilization drains continuously at a rate proportional to deployed PTUs. A deployment with more PTUs drains faster.

Accepted requests always complete with predictable latency, because 429 responses are returned immediately rather than queuing traffic.

> [!NOTE]
> Calls are accepted until utilization reaches 100%. Bursts just over 100% might be permitted for short periods, but over time your traffic is capped at 100% utilization.

:::image type="content" source="../media/provisioned/utilization.jpg" alt-text="Screenshot of the leaky bucket algorithm for provisioned throughput utilization showing how requests add to utilization while capacity drains based on deployed PTU count." lightbox="../media/provisioned/utilization.jpg":::

## Handle high utilization

When utilization reaches 100%, the service returns HTTP 429 immediately and includes the `retry-after` and `retry-after-ms` response headers indicating how long to wait before the next request is accepted. This approach maintains per-call latency targets while giving you control over how to handle high-load situations.

A 429 from a provisioned deployment is not a service error; rather, it's a traffic-management signal.

### What to do when you receive a 429 response

The response includes the `retry-after-ms` and `retry-after` headers that tell you how long to wait before the next call is accepted. How you handle a 429 depends on your application requirements:

- **Redirect to another deployment or model**: This option produces the lowest additional latency because the action can be taken as soon as you receive the 429 signal. The [spillover feature](./spillover-traffic-management.md) automates the process of redirecting requests from your provisioned deployment to a standard deployment.
- **Retry using the wait time in the response headers**: If you need the provisioned deployment and can tolerate added latency, wait the time indicated in `retry-after-ms` and retry. The [Azure OpenAI SDKs implement this retry behavior by default](#modify-retry-logic-in-the-client-libraries). You might still need further tuning based on your use-cases.

### Concurrent call limits

The number of concurrent calls a deployment can sustain depends on each call's shape—prompt size, `max_tokens` value, and similar factors. The service accepts calls until utilization reaches 100%. To estimate the maximum concurrent calls for a specific call shape, use the [capacity calculator](https://ai.azure.com/resource/calculator). If the model generates fewer tokens than the `max_tokens` value, the deployment can accept more concurrent requests.

### Modify retry logic in the client libraries

The Azure OpenAI SDKs retry 429 responses by default, respecting the `retry-after` time. You can configure or disable the retry behavior using the `max_retries` option:

```python
import os
from openai import AzureOpenAI

# Configure the default for all requests:
client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-10-21",
    max_retries=5,# default is 2
)

# Or, configure per-request:
client.with_options(max_retries=5).chat.completions.create(
    model="gpt-4", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure services support this too?"}
    ]
)
```

## Related content

- [Quickstart: Create a provisioned throughput deployment](../provisioned-quickstart.md)
- [What is provisioned throughput?](../concepts/provisioned-throughput.md)
- [PTU costs and billing](./provisioned-throughput-onboarding.md)
- [Best practices in cloud applications](/azure/architecture/best-practices/index-best-practices)
- Retry logic SDK documentation:
    - [Python](https://github.com/openai/openai-python?tab=readme-ov-file#retries)
    - [.NET](/dotnet/api/overview/azure/ai.openai-readme)
    - [Java](/java/api/com.azure.ai.openai.openaiclientbuilder?view=azure-java-preview&preserve-view=true#com-azure-ai-openai-openaiclientbuilder-retryoptions(com-azure-core-http-policy-retryoptions))
    - [JavaScript](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-secure%2Ccommand&pivots=programming-language-javascript)
    - [Go](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai#ChatCompletionsOptions)
