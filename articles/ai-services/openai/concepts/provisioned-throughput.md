---
title: Azure OpenAI Service provisioned throughput
description: Learn about provisioned throughput and Azure OpenAI.
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 08/07/2024
manager: nitinme
author: mrbullwinkle #ChrisHMSFT
ms.author: mbullwin #chrhoder
recommendations: false
---

# What is provisioned throughput?

> [!NOTE]
> The Azure OpenAI Provisioned offering received significant updates on August 12, 2024, including aligning the purchase model with Azure standards and moving to model-independent quota. It is highly recommended that customers onboarded before this date read the Azure [OpenAI provisioned August update](./provisioned-migration.md) to learn more about these changes.


The provisioned throughput capability allows you to specify the amount of throughput you require in a deployment. The service then allocates the necessary model processing capacity and ensures it's ready for you. Throughput is defined in terms of provisioned throughput units (PTU) which is a normalized way of representing the throughput for your deployment. Each model-version pair requires different amounts of PTU to deploy and provide different amounts of throughput per PTU. 

## What do the provisioned deployment types provide?

- **Predictable performance:** stable max latency and throughput for uniform workloads.
- **Reserved processing capacity:** A deployment configures the amount of throughput. Once deployed, the throughput is available whether used or not.
- **Cost savings:** High throughput workloads might provide cost savings vs token-based consumption.

An Azure OpenAI Deployment is a unit of management for a specific OpenAI Model. A deployment provides customer access to a model for inference and integrates more features like Content Moderation ([See content moderation documentation](content-filter.md)). Global provisioned deployments are available in the same Azure OpenAI resources as all other deployment types but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center with the best availability for each request. Similarly, data zone provisioned deployments are also available in the same resources as all other deployment types but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center within the Microsoft specified data zone with the best availability for each request. 

## What do you get?

| Topic | Provisioned|
|---|---|
| What is it? | Provides guaranteed throughput at smaller increments than the existing provisioned offer. Deployments have a consistent max latency for a given model-version. |
| Who is it for? | Customers who want guaranteed throughput with minimal latency variance. |
| Quota |Provisioned Managed Throughput Unit, Global Provisioned Managed Throughput Unit, or Data Zone Provisioned Managed Throughput Unit assigned per region. Quota can be used across any available Azure OpenAI model.|
| Latency | Max latency constrained from the model. Overall latency is a factor of call shape.  |
| Utilization | Provisioned-managed Utilization V2 measure provided in Azure Monitor. |
| Estimating size | Provided calculator in Azure AI Foundry & benchmarking script. |
|Prompt caching | For supported models, we discount up to 100% of cached input tokens. |


## How much throughput per PTU you get for each model
The amount of throughput (tokens per minute or TPM) a deployment gets per PTU is a function of the input and output tokens in the minute. Generating output tokens requires more processing than input tokens and so the more output tokens generated the lower your overall TPM. The service dynamically balances the input & output costs, so users do not have to set specific input and output limits. This approach means your deployment is resilient to fluctuations in the workload shape.

To help with simplifying the sizing effort, the following table outlines the TPM per PTU for the `gpt-4o` and `gpt-4o-mini` models which represent the max TPM assuming all traffic is either input or output. To understand how different ratios of input and output tokens impact your Max TPM per PTU, see the [Azure OpenAI capacity calculator](https://oai.azure.com/portal/calculator). The table also shows Service Level Agreement (SLA) Latency Target Values per model.  For more information about the SLA for Azure OpenAI Service, see the [Service Level Agreements (SLA) for Online Services page](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services?lang=1)

|Topic| **gpt-4o**, **2024-05-13**   & **gpt-4o**, **2024-08-06**   | **gpt-4o-mini**, **2024-07-18**   |
| --- | --- | --- |
|Global & data zone provisioned minimum deployment|15|15|
|Global & data zone provisioned scale increment|5|5|
|Regional provisioned minimum deployment | 50 | 25|
|Regional provisioned scale increment|50|25|
|Max Input TPM per PTU | 2,500 | 37,000  |
|Max Output TPM per PTU| 833|12,333|
|Latency Target Value |25 Tokens Per Second|33 Tokens Per Second|

For a full list see the [AOAI in Azure AI Foundry calculator](https://oai.azure.com/portal/calculator).


> [!NOTE]
> Global provisioned deployments are only supported for gpt-4o, 2024-08-06 and gpt-4o-mini, 2024-07-18 models at this time. Data zone provisioned deployments are only supported for gpt-4o, 2024-08-06, gpt-4o, 2024-05-13, and gpt-4o-mini, 2024-07-18 models at this time. For more information on model availability, review the [models documentation](./models.md).

## Key concepts

### Deployment types

When creating a provisioned deployment in Azure AI Foundry, the deployment type on the Create Deployment dialog can be set to the Global Provisioned-Managed, DataZone Provisioned-Managed, or regional Provisioned-Managed deployment type depending on the data processing needs for the given workload.

When creating a provisioned deployment in Azure OpenAI via CLI or API, the `sku-name` can be set to `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged` depending on the data processing need for the given workload. To adapt the Azure CLI example command below to a different deployment type, simply update the `sku-name` parameter to match the deployment type you wish to deploy.

```azurecli
az cognitiveservices account deployment create \
--name <myResourceName> \
--resource-group  <myResourceGroupName> \
--deployment-name MyDeployment \
--model-name gpt-4 \
--model-version 0613  \
--model-format OpenAI \
--sku-capacity 100 \
--sku-name ProvisionedManaged
```

### Quota

#### Provisioned throughput units

Provisioned throughput units (PTU) are generic units of model processing capacity that you can use to size provisioned deployments to achieve the required throughput for processing prompts and generating completions.   Provisioned throughput units are granted to a subscription as quota. Each quota is specific to a region and defines  the maximum number of PTUs that can be assigned to deployments in that subscription and region.


#### Model independent quota

Unlike the Tokens Per Minute (TPM) quota used by other Azure OpenAI offerings, PTUs are model-independent. The PTUs might be used to deploy any supported model/version in the region.

:::image type="content" source="../media/provisioned/model-independent-quota.png" alt-text="Diagram of model independent quota with one pool of PTUs available to multiple Azure OpenAI models." lightbox="../media/provisioned/model-independent-quota.png":::

For provisioned deployments, the new quota shows up in Azure AI Foundry as a quota item named **Provisioned Managed Throughput Unit**. For global provisioned deployments, the new quota shows up in the Azure AI Foundry as a quota item named **Global Provisioned Managed Throughput Unit**.  For data zone provisioned deployments, the new quota shows up in Azure AI Foundry as a quota item named **Data Zone Provisioned Managed Throughput Unit.** In the Foundry Quota pane, expanding the quota item shows the deployments contributing to usage of each quota.

:::image type="content" source="../media/provisioned/ptu-quota-page.png" alt-text="Screenshot of quota UI for Azure OpenAI provisioned." lightbox="../media/provisioned/ptu-quota-page.png":::

#### Obtaining PTU Quota

PTU quota is available by default in many regions. If more quota is required, customers can request quota via the Request Quota link. This link can be found to the right of the designated provisioned deployment type quota tabs in Azure AI Foundry The form allows the customer to request an increase in the specified PTU quota for a given region. The customer receives an email at the included address once the request is approved, typically within two business days. 

#### Per-Model PTU Minimums

The minimum PTU deployment, increments, and processing capacity associated with each unit varies by model type & version.

## Capacity transparency

Azure OpenAI is a highly sought-after service where customer demand might exceed service GPU capacity. Microsoft strives to provide capacity for all in-demand regions and models, but selling out a region is always a possibility. This constraint can limit some customers' ability to create a deployment of their desired model, version, or number of PTUs in a desired region - even if they have quota available in that region. Generally speaking:

- Quota places a limit on the maximum number of PTUs that can be deployed in a subscription and region, and does not guarantee of capacity availability.
- Capacity is allocated at deployment time and is held for as long as the deployment exists.  If service capacity is not available, the deployment will fail
- Customers use real-time information on quota/capacity availability to choose an appropriate region for their scenario with the necessary model capacity
- Scaling down or deleting a deployment releases capacity back to the region.  There is no guarantee that the capacity will be available should the deployment be scaled up or re-created later.

#### Regional capacity guidance

To find the capacity needed for their deployments, use the capacity API or the Azure AI Foundry deployment experience to provide real-time information on capacity availability.

In Azure AI Foundry, the deployment experience identifies when a region lacks the capacity needed to deploy the model. This looks at the desired model, version and number of PTUs. If capacity is unavailable, the experience directs  users to a select an alternative region.

Details on the new deployment experience can be found in the Azure OpenAI [Provisioned get started guide](../how-to/provisioned-get-started.md).

The new [model capacities API](/rest/api/aiservices/accountmanagement/model-capacities/list?view=rest-aiservices-accountmanagement-2024-04-01-preview&tabs=HTTP&preserve-view=true) can  be used to programmatically identify the maximum sized deployment of a specified model.  The API considers both your quota and service capacity in the region.

If an acceptable region isn't available to support the desire model, version and/or PTUs, customers can also try the following steps:

- Attempt the deployment with a smaller number of PTUs.
- Attempt the deployment at a different time. Capacity availability changes dynamically based on customer demand and more capacity might become available later.
- Ensure that quota is available in all acceptable regions. The [model capacities API](/rest/api/aiservices/accountmanagement/model-capacities/list?view=rest-aiservices-accountmanagement-2024-04-01-preview&tabs=HTTP&preserve-view=true) and Azure AI Foundry experience consider quota availability in returning alternative regions for creating a deployment.

### Determining the number of PTUs needed for a workload

PTUs represent an amount of model processing capacity. Similar to your computer or databases, different workloads or requests to the model will consume different amounts of underlying processing capacity. The conversion from call shape characteristics (prompt size, generation size and call rate) to PTUs is complex and nonlinear. To simplify this process, you can use the [Azure OpenAI Capacity calculator](https://oai.azure.com/portal/calculator) to size specific workload shapes.

A few high-level considerations:
- Generations require more capacity than prompts
- For GPT-4o and later models, the TPM per PTU is set for input and output tokens separately. For older models, larger calls are progressively more expensive to compute. For example, 100 calls of with a 1000 token prompt size requires less capacity than one call with 100,000 tokens in the prompt. This tiering means that the distribution of these call shapes is important in overall throughput. Traffic patterns with a wide distribution that includes some large calls might experience lower throughput per PTU than a narrower distribution with the same average prompt & completion token sizes.

### How utilization performance works

Provisioned deployments provide you with an allocated amount of model processing capacity to run a given model.

In all provisioned deployment types, when capacity is exceeded, the API will return a 429 HTTP Status Error. This fast response enables the user to make decisions on how to manage their traffic. Users can redirect requests to a separate deployment, to a standard pay-as-you-go instance, or use a retry strategy to manage a given request. The service continues to return the 429 HTTP status code until the utilization drops below 100%.

### How can I monitor capacity?

The [Provisioned-Managed Utilization V2 metric](../how-to/monitoring.md#azure-openai-metrics) in Azure Monitor measures a given deployments utilization on 1-minute increments. All provisioned deployment types are optimized to ensure that accepted calls are processed with a consistent model processing time (actual end-to-end latency is dependent on a call's characteristics).  

#### What should  I do when I receive a 429 response?
The 429 response isn't an error, but instead part of the design for telling users that a given deployment is fully utilized at a point in time. By providing a fast-fail response, you have control over how to handle these situations in a way that best fits your application requirements.

The  `retry-after-ms` and `retry-after` headers in the response tell you the time to wait before the next call will be accepted. How you choose to handle this response depends on your application requirements. Here are some considerations:
-    You can consider redirecting the traffic to other models, deployments, or experiences. This option is the lowest-latency solution because the action can be taken as soon as you receive the 429 signal. For ideas on how to effectively implement this pattern see this [community post](https://github.com/Azure/aoai-apim).
-    If you're okay with longer per-call latencies, implement client-side retry logic. This option gives you the highest amount of throughput per PTU. The Azure OpenAI client libraries include built-in capabilities for handling retries.

#### How does the service decide when to send a 429?

In all provisioned deployment types, each request is evaluated individually according to its prompt size, expected generation size, and model to determine its expected utilization. This is in contrast to pay-as-you-go deployments, which have a [custom rate limiting behavior](../how-to/quota.md) based on the estimated traffic load. For pay-as-you-go deployments this can lead to HTTP 429 errors being generated prior to defined quota values being exceeded if traffic is not evenly distributed.

For provisioned deployments, we use a variation of the leaky bucket algorithm to maintain utilization below 100% while allowing some burstiness in the traffic. The high-level logic is as follows:

1. Each customer has a set amount of capacity they can utilize on a deployment
1. When a request is made:

    a.    When the current utilization is above 100%, the service returns a 429 code with the `retry-after-ms` header set to the time until utilization is below 100%

    b.    Otherwise, the service estimates the incremental change to utilization required to serve the request by combining prompt tokens and the specified `max_tokens` in the call. For requests that include at least 1024 cached tokens, the cached tokens are subtracted from the prompt token value. A customer can receive up to a 100% discount on their prompt tokens depending on the size of their cached tokens. If the `max_tokens` parameter is not specified, the service estimates a value. This estimation can lead to lower concurrency than expected when the number of actual generated tokens is small.  For highest concurrency, ensure that the `max_tokens` value is as close as possible to the true generation size.

1.  When a request finishes, we now know the actual compute cost for the call. To ensure an accurate accounting, we correct the utilization using the following logic:

    a.    If the actual > estimated, then the difference is added to the deployment's utilization.

    b.    If the actual < estimated, then the difference is subtracted.

1.  The overall utilization is decremented down at a continuous rate based on the number of PTUs deployed. 

> [!NOTE]
> Calls are accepted until utilization reaches 100%. Bursts just over 100% may be permitted in short periods, but over time, your traffic is capped at 100% utilization.


:::image type="content" source="../media/provisioned/utilization.jpg" alt-text="Diagram showing how subsequent calls are added to the utilization." lightbox="../media/provisioned/utilization.jpg":::

#### How many concurrent calls can I have on my deployment?

The number of concurrent calls you can achieve depends on each call's shape (prompt size, max_token parameter, etc.). The service continues to accept calls until the utilization reach 100%. To determine the approximate number of concurrent calls, you can model out the maximum requests per minute for a particular call shape in the [capacity calculator](https://oai.azure.com/portal/calculator). If the system generates less than the number of samplings tokens like max_token, it will accept more requests.

## What models and regions are available for provisioned throughput?

[!INCLUDE [Provisioned](../includes/model-matrix/provisioned-models.md)]

> [!NOTE]
> The provisioned version of `gpt-4` **Version:** `turbo-2024-04-09` is currently limited to text only.

## Next steps

- [Learn about the onboarding steps for provisioned deployments](../how-to/provisioned-throughput-onboarding.md)
- [Provisioned Throughput Units (PTU) getting started guide](../how-to//provisioned-get-started.md)
