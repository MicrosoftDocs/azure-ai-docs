---
title: Get started with provisioned deployments in Microsoft Foundry
titleSuffix: Azure OpenAI
description: Learn how to create and configure provisioned throughput deployments, verify quota, handle high utilization, and run benchmarks in Microsoft Foundry.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: openai, pilot-ai-workflow-jan-2026 
ms.topic: how-to
author: msakande
ms.author: mopeakande
ms.reviewer: seramasu
reviewer: rsethur
ms.date: 02/10/2026
recommendations: false
#customerIntent: As a developer, I want to create and configure provisioned deployments so I can optimize performance and throughput for my AI applications.
---

# Get started with provisioned deployments in Microsoft Foundry

[!INCLUDE [version-banner](../../includes/version-banner.md)]

The following guide walks you through key steps in creating a provisioned deployment with your Microsoft Foundry resource. For more details on the concepts discussed here, see:
* [Foundry Provisioned Throughput Onboarding Guide](./provisioned-throughput-onboarding.md)
* [Foundry Provisioned Throughput Concepts](../concepts/provisioned-throughput.md) 

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- Azure Contributor or Cognitive Services Contributor role
- A [Foundry resource](./create-resource.md) in a region with available PTU quota
- Azure CLI - [Install the Azure CLI](/cli/azure/install-azure-cli) (required only for CLI-based deployment)

## Verify PTU quota availability

Provisioned throughput deployments are sized in units called Provisioned Throughput Units (PTUs). PTU quota for each provisioned deployment type is granted to a subscription regionally and limits the total number of PTUs that can be deployed in that region across all models and versions. 

Creating a new deployment requires available (unused) quota to cover the desired size of the deployment. For example: If a subscription has the following in South Central US: 

* Total PTU Quota = 500 PTUs 
* Deployments: 
    * 100 PTUs: GPT-4o, 2024-05-13 
    * 100 PTUs: DeepSeek-R1, 1

Then 200 PTUs of quota are considered used, and there are 300 PTUs available for use to create new deployments. 

A default amount of global, data zone, and regional provisioned quota is assigned to eligible subscriptions in several regions. 

::: moniker range="foundry-classic"

You can view the quota available to you in a region by visiting the Quotas pane in [Foundry portal](https://ai.azure.com/?cid=learnDocs) and selecting the desired subscription and region. For example, the screenshot below shows a quota limit of 300 Global Provisioned Throughput PTUs in West US for the selected subscription. The total usage of this Global PTUs is 50, then you will have 250 PTU units available to deploy Global Provisioned Throughput deployment type.

:::image type="content" source="../media/provisioned/available-quota.png" alt-text="A screenshot of the available quota in Foundry portal." lightbox="../media/provisioned/available-quota.png":::

::: moniker-end

::: moniker range="foundry"

You can view the quota available to you in a region by visiting the **Quota** pane in the [!INCLUDE [foundry-link](../../default/includes/foundry-link.md)] **Operate** section and selecting the desired subscription and region. 

::: moniker-end

Additional quota can be requested by Selecting the **Request Quota** button.

## Create a Foundry resource 

Provisioned deployments are created via Foundry resource objects within Azure. You must have a Foundry resource in each region where you intend to create a deployment. 

::: moniker range="foundry-classic"

Use the Azure portal to [create a resource](./create-resource.md) in a region with available quota, if required.  

::: moniker-end

> [!NOTE]
> Foundry resources can support multiple types of Foundry deployments at the same time.  It is not necessary to dedicate new resources for your provisioned deployments. 

## Discover models with provisioned deployment option

Once you have verified your quota, you can create a deployment. Navigate to Foundry model catalog to discover the models with provisioned deployment options. 

::: moniker range="foundry-classic"

1. [!INCLUDE [classic-sign-in](../../includes/classic-sign-in.md)]
1. Choose the subscription that was enabled for provisioned deployments & select the desired resource in a region where you have the quota. 
1. You can select models by filtering **Direct from Azure** in the model collections filter. Those are models held and served by Azure directly and support provisioned throughput deployment option. 
1. Select the model that you want to deploy and check the model details in the model card.

::: moniker-end

::: moniker range="foundry"

1. [!INCLUDE [foundry-sign-in](../../default/includes/foundry-sign-in.md)]
1. From the Foundry portal homepage, choose the subscription that was enabled for provisioned deployments & select the desired resource in a region where you have the quota. 
1. Select **Discover** in the upper-right navigation, then **Models** in the left pane.
1. Select the **Collections** filter and filter by **Direct from Azure** to see the models held and served by Azure directly. A selection of these models support provisioned throughput deployment option. 
1. Select the model that you want to deploy to open its model card.
1. Select **Deploy** > **Custom settings** to customize your deployment. 
1. Select the **Deployment type** drop down menu to  see if provisioned deployment is available for the model.

::: moniker-end 


## Create your provisioned deployment - capacity is available

::: moniker range="foundry-classic"

To create a provisioned deployment, you can follow these steps; the choices described reflect the entries shown in the screenshot.

:::image type="content" source="../media/provisioned/deployment-screen.png" alt-text="Screenshot of the Foundry portal deployment page for a provisioned deployment." lightbox="../media/provisioned/deployment-screen.png":::

1. Select **Use this model** and configure the following fields. 

1. Select "Global Provisioned Throughput"," Data Zone Provisioned Throughput" or" Regional Provisioned Throughput" as you required in the Deployment type drop-down for your provisioned deployment. 

1. Expand the **advanced options** drop-down menu. 

1. Fill out the values in each field. Here's an example:

| Field | Description |    Example |
|--|--|--|
| Select a model|    Choose the specific model you wish to deploy.    | GPT-4 |
| Model version |    Choose the version of the model to deploy.     | 0613 |
| Deployment Name     | The deployment name is used in your code to call the model by using the client libraries and the REST APIs.    | gpt-4|
| Content filter    | Specify the filtering policy to apply to the deployment. Learn more on our [Content Filtering](../../foundry-models/concepts/content-filter.md) how-to. |     Default |
| Deployment Type    |This impacts the throughput and performance. Choose Global Provisioned Throughput, Data Zone Provisioned Throughput or Regional Provisioned Throughput from the deployment dialog dropdown for your deployment     | Global Provisioned Throughput |
| Provisioned Throughput Units |    Choose the amount of throughput you wish to include in the deployment. |    100 |

> [!NOTE]
> The deployment dialog contains a reminder that you can purchase an Azure Reservation for Foundry Provisioned Throughput to obtain a significant discount for a term commitment. 

Once you have entered the deployment settings, select **Confirm Pricing** to continue.  A pricing confirmation dialog will appear that will display the list price for the deployment, if you choose to pay for it on an hourly basis, with no Azure Reservation to provide a term discount.

If you are unsure of the costs, cancel the deployment and proceed once you understand the payment model and underlying costs for provisioned deployment. This step may prevent unexpected, high charges on your payment invoice. Resources to educate yourself include: 

* [Azure Pricing Portal](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) 
* [Understanding the provisioned throughput costs](provisioned-throughput-onboarding.md) 

The image below shows the pricing confirmation you will see. The price shown is an example only. 

:::image type="content" source="../media/provisioned/confirm-pricing.png" alt-text="Screenshot showing the pricing confirmation screen." lightbox="../media/provisioned/confirm-pricing.png":::

::: moniker-end

You can create your deployment programmatically, using the following Azure CLI command. To specify the deployment type, modify the `sku-name` to `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged` based on the intended deployment type. Update the `sku-capacity` with the desired number of provisioned throughput units.

```cli
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

REST, ARM template, Bicep, and Terraform can also be used to create deployments. See the section on automating deployments in the [Managing Quota](quota.md?tabs=rest#automate-deployment) how-to guide and replace the `sku.name` with `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged` rather than `Standard`.

::: moniker range="foundry-classic"

## Create your provisioned deployment – Capacity is not available

Due to the dynamic nature of capacity availability, it is possible that the region of your selected resource might not have the service capacity to create the deployment of the specified model, version, and number of PTUs. 

In this event, the wizard in [!INCLUDE [foundry-link](../../default/includes/foundry-link.md)] will direct you to other regions with available quota and capacity to create a deployment of the desired model. If this happens, the deployment dialog will look like this: 

:::image type="content" source="../media/provisioned/deployment-screen-2.png" alt-text="Screenshot of the Foundry portal deployment page for a provisioned deployment with no capacity available." lightbox="../media/provisioned/deployment-screen-2.png":::

Things to notice: 

* A message displays showing you many PTUs you have in available quota, and how many can currently be deployed at this time. 
* If you select a number of PTUs greater than service capacity, a message will appear that provides options for you to obtain more capacity, and a button to allow you to select an alternate region. Selecting the "See other regions" button will display a dialog that shows a list of Foundry resources where you can create a deployment, along with the maximum sized deployment that can be created based on available quota and service capacity in each region. 

:::image type="content" source="../media/provisioned/choose-different-resource.png" alt-text="Screenshot of the Foundry portal deployment page for choosing a different resource and region." lightbox="../media/provisioned/choose-different-resource.png":::

Selecting a resource and selecting **Switch resource** will cause the deployment dialog to redisplay using the selected resource. You can then proceed to create your deployment in the new region.

## Create a new deployment or exchange models with your quota

If you still have quota available under the subscription and region, you can create new provisioned deployments for other models that direct host and sold from Microsoft. 

The steps are the same as the above example. When you create a new deployment, you will see the total available quota you can use in the deployment widget. In the screenshot below, the available quota is 250 units. 

:::image type="content" source="../media/provisioned/deepseek-deployment.png" alt-text="Screenshot of the fungible PTU to deploy flagship models." lightbox="../media/provisioned/deepseek-deployment.png":::

After you deploy the new model, check the quota usage in [Foundry portal](https://ai.azure.com). You can manage your quota by either requesting new quota or deleting existing deployments to free up PTU quotas for new provisioned deployments. 

:::image type="content" source="../media/provisioned/fungible-quota.png" alt-text="Screenshot of the fungible PTU quota in quota page." lightbox="../media/provisioned/fungible-quota.png":::

::: moniker-end

## Optionally purchase a reservation 

Following the creation of your deployment, you might want to purchase a term discount via an Azure Reservation.  An Azure Reservation can provide a substantial discount on the hourly rate for users intending to use the deployment beyond a few days.   

For more information on the purchase model and reservations, see:
* [Save costs with Microsoft Foundry provisioned throughput reservations](/azure/cost-management-billing/reservations/azure-openai).
* [Foundry provisioned throughput onboarding guide](./provisioned-throughput-onboarding.md) 
* [Guide for Foundry provisioned throughput reservations](../concepts/provisioned-throughput.md) 

> [!IMPORTANT]
> Capacity availability for model deployments is dynamic and changes frequently across regions and models. To prevent you from purchasing a reservation for more PTUs than you can use, create deployments first, and then purchase the Azure Reservation to cover the PTUs you have deployed. This best practice will ensure that you can take full advantage of the reservation discount and prevent you from purchasing a term commitment that you cannot use.

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


## Understand expected throughput

The amount of throughput that you can achieve on the endpoint is a factor of the number of PTUs deployed, input size, output size, and call rate. The number of concurrent calls and total tokens processed can vary based on these values. 

::: moniker range="foundry-classic"

Our recommended way for determining the throughput for your deployment is as follows:
1. Use the Capacity calculator for a sizing estimate. You can find the capacity calculator in [Foundry portal](https://ai.azure.com/?cid=learnDocs) under the quotas page and Provisioned tab.  
1. Benchmark the load using real traffic workload. For more information about benchmarking, see the [benchmarking](#run-a-benchmark) section.

::: moniker-end

## Measure deployment utilization
When you deploy a specified number of provisioned throughput units (PTUs), a set amount of inference throughput is made available to that endpoint. Utilization of this throughput is a complex formula based on the model, model-version call rate, prompt size, generation size. To simplify this calculation, we provide a utilization metric in Azure Monitor. Your deployment returns a 429 on any new calls after the utilization rises above 100%. The Provisioned utilization is defined as follows:

PTU deployment utilization = (PTUs consumed in the time period) / (PTUs deployed in the time period)

You can find the utilization measure in the Azure-Monitor section for your resource. To access the monitoring dashboards sign-in to [https://portal.azure.com](https://portal.azure.com), go to your Azure OpenAI resource and select the Metrics page from the left nav. On the metrics page, select the 'Provisioned-managed utilization V2' metric. If you have more than one deployment in the resource, you should also split the values by each deployment by selecting the 'Apply Splitting' button.

:::image type="content" source="../media/provisioned/azure-monitor-utilization.jpg" alt-text="Screenshot of the provisioned managed utilization on the resource's metrics blade in the Azure portal." lightbox="../media/provisioned/azure-monitor-utilization.jpg":::

::: moniker range="foundry-classic"

For more information about monitoring your deployments, see the [Monitoring Azure OpenAI](./monitor-openai.md) page.

::: moniker-end

## Handle high utilization
Provisioned deployments provide you with an allocated amount of compute capacity to run a given model. The 'Provisioned-Managed Utilization V2' metric in Azure Monitor measures the utilization of the deployment in one-minute increments. Provisioned-Managed deployments are also optimized so that calls accepted are processed with a consistent per-call max latency. When the workload exceeds its allocated capacity, the service returns a 429 HTTP status code until the utilization drops down below 100%. The time before retrying is provided in the `retry-after` and `retry-after-ms` response headers that provide the time in seconds and milliseconds respectively. This approach maintains the per-call latency targets while giving the developer control over how to handle high-load situations – for example retry or divert to another experience/endpoint. 

### What should I do when I receive a 429 response?
A 429 response indicates that the allocated PTUs are fully consumed at the time of the call. The response includes the `retry-after-ms` and `retry-after` headers that tell you the time to wait before the next call will be accepted. How you choose to handle a 429 response depends on your application requirements. Here are some considerations:
-    If you are okay with longer per-call latencies, implement client-side retry logic to wait the `retry-after-ms` time and retry. This approach lets you maximize the throughput on the deployment. Microsoft-supplied client SDKs already handle it with reasonable defaults. You might still need further tuning based on your use-cases.
-    Consider redirecting the traffic to other models, deployments, or experiences. This approach is the lowest-latency solution because this action can be taken as soon as you receive the 429 signal.
The 429 signal isn't an unexpected error response when pushing to high utilization but instead part of the design for managing queuing and high load for provisioned deployments. 

### Modifying retry logic within the client libraries
The Azure OpenAI SDKs retry 429 responses by default and behind the scenes in the client (up to the maximum retries). The libraries respect the `retry-after` time. You can also modify the retry behavior to better suit your experience. Here's an example with the python library. 


You can use the `max_retries` option to configure or disable retry settings:

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


## Run a benchmark
The exact performance and throughput capabilities of your instance depends on the kind of requests you make and the exact workload. The best way to determine the throughput for your workload is to run a benchmark on your own data. 

To assist you in this work, the benchmarking tool provides a way to easily run benchmarks on your deployment. The tool comes with several possible preconfigured workload shapes and outputs key performance metrics. Learn more about the tool and configuration settings in our GitHub Repo: [https://github.com/Azure/azure-openai-benchmark](https://github.com/Azure/azure-openai-benchmark). 

We recommend the following workflow:
1. Estimate your throughput PTUs using the capacity calculator.
1. Run a benchmark with this traffic shape for an extended period of time (10+ min) to observe the results in a steady state.
1. Observe the utilization, tokens processed and call rate values from benchmark tool and Azure Monitor.
1. Run a benchmark with your own traffic shape and workloads using your client implementation. Be sure to implement retry logic using either an Azure OpenAI client library or custom logic. 


## Troubleshoot provisioned deployments

| Issue | Cause | Resolution |
|-------|-------|------------|
| Deployment creation fails with quota error | Not enough PTU quota available in the selected region | Check quota usage in the Foundry portal **Quota** pane and request more quota or free up existing deployments |
| Deployment stuck in provisioning state | Capacity constraints in the region | Wait and retry, or try deploying in a different region with available capacity |
| Unexpected high charges on invoice | Provisioned deployments bill hourly regardless of usage | Consider purchasing an [Azure Reservation](/azure/cost-management-billing/reservations/azure-openai) for a term discount, or delete unused deployments |
| 429 responses despite low utilization | Burst of requests exceeding momentary capacity | Implement retry logic as described in the [handle high utilization](#handle-high-utilization) section |

## Related content

* For more information on cloud application best practices, check out [Best practices in cloud applications](/azure/architecture/best-practices/index-best-practices)
* For more information on provisioned deployments, check out [What is provisioned throughput?](../concepts/provisioned-throughput.md)
* For more information on retry logic within each SDK, check out:
    * [Python reference documentation](https://github.com/openai/openai-python?tab=readme-ov-file#retries)
    * [.NET reference documentation](/dotnet/api/overview/azure/ai.openai-readme)
    * [Java reference documentation](/java/api/com.azure.ai.openai.openaiclientbuilder?view=azure-java-preview&preserve-view=true#com-azure-ai-openai-openaiclientbuilder-retryoptions(com-azure-core-http-policy-retryoptions))
    * [JavaScript reference documentation](/azure/ai-foundry/openai/supported-languages?tabs=dotnet-secure%2Csecure%2Cpython-secure%2Ccommand&pivots=programming-language-javascript)
    * [GO reference documentation](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai#ChatCompletionsOptions)
