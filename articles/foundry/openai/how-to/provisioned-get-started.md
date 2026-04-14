---
title: "Get started with provisioned deployments in Microsoft Foundry"
description: "Learn how to create provisioned deployments, estimate PTU requirements, benchmark your workload, and monitor utilization in Microsoft Foundry."
ai-usage: ai-assisted
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom:
  - openai, pilot-ai-workflow-jan-2026
  - classic-and-new
  - doc-kit-assisted
ms.topic: how-to
author: msakande
ms.author: mopeakande
ms.reviewer: seramasu
reviewer: rsethur
ms.date: 04/10/2026
recommendations: false
#customerIntent: As a developer, I want to create and configure provisioned deployments so I can optimize performance and throughput for my AI applications.
---

# Get started with provisioned deployments in Microsoft Foundry

This guide walks you through the end-to-end process of setting up a provisioned deployment: verifying quota, sizing your deployment, creating it, purchasing a reservation, making inference calls, and monitoring utilization. This article assumes you're familiar with the concepts in [What is provisioned throughput?](../concepts/provisioned-throughput.md) and the billing details in [PTU costs and billing](./provisioned-throughput-onboarding.md).

## Prerequisites

- An Azure subscription — [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Azure Contributor or Cognitive Services Contributor role.
- A [Foundry resource](../../../foundry-classic/openai/how-to/create-resource.md) in each region where you intend to create a deployment. Foundry resources support multiple deployment types simultaneously—you don't need to dedicate a separate resource to provisioned deployments.
- Azure CLI — [install the Azure CLI](/cli/azure/install-azure-cli) (required only for CLI-based deployment).

## Estimate PTU requirements

Before creating your deployment, estimate how many PTUs your workload requires. PTU requirements depend on your expected requests per minute, prompt size, response size, and cache hit rate. 

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]
1. Select **Operate** > **Quota** > **Provisioned throughput unit**
1. Select **Capacity calculator**.
1. Add workloads to your PTU calculation.

For the PTU estimation formulas, a worked example, and details about the parameters you need to provide in the capacity calculator, see [Determine PTU requirements for a workload](./provisioned-throughput-onboarding.md#determine-ptu-requirements-for-a-workload).

## Verify PTU quota availability

PTU quota is granted per subscription, per region, and limits the total PTUs you can deploy in that region across all models. Before creating a deployment, verify that your subscription has enough available (unused) quota to cover the PTU count you plan to deploy. For details on how quota and capacity relate, see [PTU quota vs. capacity](../concepts/provisioned-throughput.md#ptu-quota-vs-capacity).

To view your quota and current usage:

1. From the **Quota** pane in the **Operate** section, select the desired subscription and region.
1. To request additional quota, select **Request Quota** and complete the form.

## Discover models with provisioned deployment option

1. Return to the Foundry portal homepage.
1. Select the subscription and the resource in the region where you have quota.
1. Select **Discover** in the upper-right navigation, then **Models** in the left pane.
1. Select the **Collections** filter and filter by **Direct from Azure** to see models sold directly by Azure. A selection of these models support the provisioned throughput deployment option.
1. Select the model you want to deploy to open its model card.
1. Select **Deploy** > **Custom settings** to configure your deployment. The **Deployment type** drop down menu lists provisioned deployment typesthat are available for the selected model.


## Create a provisioned deployment

When you're ready to create a provisioned deployment, you might encounter one of two situations. On one hand, is capacity is available, you can proceed to create thea provisioned deployment. On the other hand, if capacity isn't available, you can take some options to resolve the situation to create your deployment.

### When capacity is available

**In the Foundry portal:**

Continuing from the model card, with **Deploy** > **Custom settings** open:

1. In the **Deployment type** dropdown, select the provisioned deployment type: **Global Provisioned Throughput**, **Data Zone Provisioned Throughput**, or **Regional Provisioned Throughput**.
1. Expand **Advanced options**.
1. Fill in the deployment fields:

   | Field | Description |
   |---|---|
   | Model | The model to deploy. |
   | Model version | The version of the model. |
   | Deployment name | The name used in your code to call the model. |
   | Content filter | The filtering policy for the deployment. See [Content filtering](../../foundry-models/concepts/content-filter.md). |
   | Provisioned throughput units | The number of PTUs to allocate. |

1. Select **Confirm pricing** to review the hourly list price for the deployment.

   > [!IMPORTANT]
   > If you're unsure of the costs, cancel the deployment and review [PTU costs and billing](./provisioned-throughput-onboarding.md) before proceeding. See also [Azure pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

   > [!NOTE]
   > The deployment dialog includes a reminder that you can purchase an Azure Reservation for a significant discount on the hourly rate.

1. Confirm and create the deployment.

**Using the Azure CLI:**

To specify the deployment type, modify the `sku-name` to `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged` based on the intended deployment type. Update the `sku-capacity` with the desired number of provisioned throughput units.

```azurecli
az cognitiveservices account deployment create \
--name <myResourceName> \
--resource-group <myResourceGroupName> \
--deployment-name MyModel \
--model-name GPT-4 \
--model-version 0613  \
--model-format OpenAI \
--sku-capacity 100 \
--sku-name ProvisionedManaged
```

REST, ARM template, Bicep, and Terraform can also be used to create deployments. See the section on automating deployments in the [Managing Quota](../../../foundry-classic/openai/how-to/quota.md?tabs=rest#automate-deployment) how-to guide and replace the `sku.name` with `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged` rather than `Standard`.

### When capacity isn't available

Provisioned capacity is allocated at deployment time and availability can change throughout the day. If the region you selected doesn't have sufficient capacity for the requested PTU count, the deployment dialog shows how many PTUs are available for deployment and provides options to resolve the situation.

If you enter a PTU count that exceeds available capacity:

1. Select **See other regions** in the deployment dialog. The portal lists your Foundry resources in other regions, along with the maximum deployable PTU count for each, based on your available quota and current service capacity in that region.
1. Select a resource in a region with sufficient capacity, then select **Switch resource**. The deployment dialog updates to reflect the selected region.
1. Complete the deployment in the new region.

If no alternative region has enough capacity:

- Try deploying with fewer PTUs than originally planned.
- Use the [model capacities API](/rest/api/aiservices/accountmanagement/model-capacities/list) to programmatically query deployable PTU counts across regions.
- Retry later. Capacity availability changes dynamically throughout the day as demand fluctuates.

## Create more deployments with your remaining quota

PTU quota is shared across all provisioned deployments of the same deployment type within a region. If you have quota remaining after your initial deployment, you can use it to deploy other supported models without requesting more quota.

The steps are the same as creating your first deployment. When you configure the new deployment, the deployment dialog shows the total available quota you can use. After you create the new deployment, check your updated quota usage in the **Quota** pane under **Operate** in the [Foundry portal](https://ai.azure.com/?cid=learnDocs). You can manage your quota by requesting additional quota, or by deleting existing deployments to free up PTUs for new deployments.

## Optionally purchase a reservation

After your provisioned deployment is in place, consider purchasing an Azure Reservation to get a discounted rate on your PTU billing. A reservation provides a significant discount over hourly billing for deployments you plan to run for more than a few days.

> [!IMPORTANT]
> Capacity availability is dynamic. Always create your deployments first to confirm capacity is available, then purchase the reservation to cover the PTUs you've deployed. This approach ensures you can take full advantage of the reservation discount and prevents you from committing to PTUs you can't use.

For guidance on sizing and purchasing a reservation, see [Azure Reservations for provisioned throughput](./provisioned-throughput-onboarding.md#azure-reservations-for-provisioned-throughput).

## Make your first inferencing calls

The inferencing code for provisioned deployments is the same as a standard deployment type. The following code snippet shows a chat completions call to a GPT-4 model. For your first time using these models programmatically, we recommend starting with our [quickstart guide](./responses.md). Our recommendation is to use the OpenAI library with version 1.0 or greater since this includes retry logic within the library.

```python
    import os
    from openai import AzureOpenAI

    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version="2024-10-21"
    )

    response = client.chat.completions.create(
        model="gpt-4", # model = "deployment_name".
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
            {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
            {"role": "user", "content": "Do other Azure services support this too?"}
        ]
    )

    print(response.choices[0].message.content)
```

> [!IMPORTANT]
> For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see this [security](../../../ai-services/security-features.md) article.

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

:::image type="content" source="../media/provisioned/azure-monitor-utilization.jpg" alt-text="Screenshot of the provisioned managed utilization on the resource's metrics blade in the Azure portal." lightbox="../media/provisioned/azure-monitor-utilization.jpg":::

### How utilization works

Each customer has a set amount of capacity they can use on a provisioned deployment. To maintain utilization below 100% while allowing some burstiness in traffic, the service uses a variation of the leaky bucket algorithm as follows:

1. **Throttling at 100%**: When a request is made, if current utilization is at 100%, the service returns HTTP 429 immediately, with `retry-after-ms` and `retry-after` response headers indicating how long to wait.
1. **Request estimate**: For each incoming request, the service estimates the compute cost by combining the prompt token count (less any cached tokens) and the specified `max_tokens` in the call. Cached tokens receive a 100% discount and don't contribute to utilization. If `max_tokens` isn't specified, the service estimates a value—this can lead to lower concurrency than expected when actual generated tokens are fewer than estimated. For highest concurrency, set `max_tokens` as close as possible to your true generation size.
1. **Post-request correction**: When a request finishes, the service corrects the utilization estimate using actual token counts. If the actual compute cost exceeds the estimate, the difference is added to utilization; if it's less, the difference is subtracted.
1. **Continuous drain**: Utilization drains continuously at a rate proportional to deployed PTUs. A deployment with more PTUs drains faster.

Accepted requests always complete with predictable latency, because 429 responses are returned immediately rather than queuing traffic.

> [!NOTE]
> Calls are accepted until utilization reaches 100%. Bursts just over 100% might be permitted for short periods, but over time your traffic is capped at 100% utilization.

:::image type="content" source="../media/provisioned/utilization.jpg" alt-text="Diagram of the leaky bucket algorithm for provisioned throughput utilization showing how incoming requests add to utilization while capacity drains based on deployed PTU count." lightbox="../media/provisioned/utilization.jpg":::

## Handle high utilization

When utilization reaches 100%, the service returns HTTP 429 immediately and includes the `retry-after` and `retry-after-ms` response headers indicating how long to wait before the next request is accepted. This approach maintains per-call latency targets while giving you control over how to handle high-load situations.

A 429 from a provisioned deployment is a traffic-management signal—not a service error.

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

- [What is provisioned throughput?](../concepts/provisioned-throughput.md)
- [PTU costs and billing](./provisioned-throughput-onboarding.md)
- [Best practices in cloud applications](/azure/architecture/best-practices/index-best-practices)
- Retry logic SDK documentation:
    - [Python](https://github.com/openai/openai-python?tab=readme-ov-file#retries)
    - [.NET](/dotnet/api/overview/azure/ai.openai-readme)
    - [Java](/java/api/com.azure.ai.openai.openaiclientbuilder?view=azure-java-preview&preserve-view=true#com-azure-ai-openai-openaiclientbuilder-retryoptions(com-azure-core-http-policy-retryoptions))
    - [JavaScript](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-secure%2Ccommand&pivots=programming-language-javascript)
    - [Go](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai#ChatCompletionsOptions)
