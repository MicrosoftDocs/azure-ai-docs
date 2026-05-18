---
title: "Quickstart: Create a provisioned throughput deployment"
description: "Create a provisioned throughput deployment in Microsoft Foundry, make an inference call, and verify utilization."
ai-usage: ai-assisted
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.custom:
  - openai
  - classic-and-new
  - doc-kit-assisted
ms.topic: quickstart
author: msakande
ms.author: mopeakande
ms.reviewer: seramasu
reviewer: rsethur
ms.date: 05/18/2026
recommendations: false
#customerIntent: As a developer, I want to create a provisioned throughput deployment and make my first inference call so I can start using dedicated model capacity for my application.
---

# Quickstart: Create a provisioned throughput deployment

In this quickstart, you create a provisioned throughput deployment in Microsoft Foundry, make an inference call to confirm it works, and view its utilization metric.

A provisioned throughput deployment gives your application dedicated model processing capacity with predictable latency. Billing is done per provisioned throughput unit (PTU) per hour. For a full conceptual introduction, see [What is provisioned throughput for Foundry Models?](./concepts/provisioned-throughput.md).

> [!NOTE]
> PTU quota isn't available by default for all subscriptions or regions. If you don't already have PTU quota, request it through the [quota request form](https://aka.ms/oai/stuquotarequest) before following this quickstart. Quota approval can take several days, and you receive an email notification when the request is approved..

## Prerequisites

- An Azure subscription — [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- **Azure Contributor** or **Cognitive Services Contributor** role on the subscription or resource group where you plan to create the deployment.
- A Foundry resource in the region where you have PTU quota. See [Create a Foundry resource](../../foundry-classic/openai/how-to/create-resource.md).
- PTU quota approved for your target region and deployment type. To check your quota, go to **Operate** > **Quota** > **Provisioned throughput unit** in the [Foundry portal](https://ai.azure.com/?cid=learnDocs). If you don't have quota, select **Request Quota** and complete the form.
- (Azure CLI only) [Azure CLI installed](/cli/azure/install-azure-cli).

> [!NOTE]
> If you plan to purchase a reservation after creating your deployment, verify that you have the owner role or reservation purchaser role on an Azure subscription. The role needed to purchase reservations differs from the role needed to create deployments. See [Provisioned Throughput reservations](https://aka.ms/oai/docs/ptum-reservations) for role requirements. 

## Check model and region availability

Before creating a deployment, confirm that your model supports provisioned throughput in your target region

1. Go to the [model and region availability table](../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=provisioned) to see if your model supports provisioned throughput deployment in your target region.
1. Filter by your region and verify the model appears in a **Provisioned** deployment type.

Also note the model's minimum PTU count, as you need this information when you configure the deployment. Minimums vary by model and are listed in [Throughput and deployment parameter values by model](./how-to/provisioned-throughput-onboarding.md#throughput-and-deployment-parameter-values-by-model).

## Create a provisioned deployment

**Using the Foundry portal:**

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]
1. Select the subscription and the Foundry resource in the region where you have PTU quota.
1. Select **Discover** in the upper-right navigation, then select **Models** in the left pane.
1. Select the **Collections** filter and select **Direct from Azure** to view Foundry Models sold by Azure.
1. Select the model you want to deploy to open its model card.
1. Select **Deploy** > **Custom settings**.
1. In the **Deployment type** dropdown, select a provisioned deployment type: **Global Provisioned Throughput**, **Data Zone Provisioned Throughput**, or **Regional Provisioned Throughput**.
1. Fill in the deployment fields:

   | Field | Description |
   |---|---|
   | **Deployment name** | A name you choose. Use this name in your code to call the model. |
   | **Model** | The model to deploy. |
   | **Model version** | The version of the model. |
   | **Provisioned throughput units** | The number of PTUs to allocate. Must meet the model's minimum. |
   | **Content filter** | The filtering policy. See [Content filtering](../foundry-models/concepts/content-filter.md). |

1. Select **Confirm pricing** to review the hourly rate for the deployment.

   > [!IMPORTANT]
   > Billing starts as soon as the deployment is created, even when no requests are being sent. You stop billing by deleting your deployment. If you're unsure of the costs, select **Cancel** and review [PTU billing, sizing, and cost management](./how-to/provisioned-throughput-onboarding.md) before continuing.

1. Confirm and create the deployment.

> [!TIP]
> If the portal shows that your target region doesn't have sufficient capacity, select **See other regions**. The portal lists your Foundry resources in other regions with available capacity. Select a resource in a region with sufficient capacity, select **Switch resource**, and complete the deployment.

**Using the Azure CLI:**

The following code snippet shows how to use the CLI to create a provisioned deployment for GPT-4 with a PTU count of 100 PTUs.

- Replace `<myResourceName>`, `<myResourceGroupName>`, `<myDeploymentName>` with your values.

- `--sku-name` specifies the deployment type, which could be one of `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged`. 

- `--sku-capacity` is the number of PTUs. Here, it's set to 100.

```azurecli
az cognitiveservices account deployment create \
--name <myResourceName> \
--resource-group <myResourceGroupName> \
--deployment-name <myDeploymentName> \
--model-name GPT-4 \
--model-version 0613 \
--model-format OpenAI \
--sku-capacity 100 \
--sku-name ProvisionedManaged
```

REST, ARM template, Bicep, and Terraform can also be used to create deployments. See [Automate deployments](../../foundry-classic/openai/how-to/quota.md?tabs=rest#automate-deployment) and replace `sku.name` with `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged`.

## Make an inference call

The inference code for a provisioned deployment is the same as for any other deployment type. Use your deployment name (not the model name) as the `model` parameter value.

Before running the sample, set the following environment variables:

- `AZURE_OPENAI_ENDPOINT` — Your Foundry resource endpoint, in the format `https://<myResourceName>.openai.azure.com/`.
- `AZURE_OPENAI_API_KEY` — Your resource API key.

> [!IMPORTANT]
> Don't hard-code credentials in your application. For production workloads, use a secure credential store such as [Azure Key Vault](/azure/key-vault/general/overview). See [Security features for Azure AI services](../../ai-services/security-features.md).

# [Python](#tab/python)

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-10-21",
)

response = client.chat.completions.create(
    model="<myDeploymentName>",  # Your deployment name, not the model name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is provisioned throughput?"},
    ],
    max_tokens=100,
)

print(response.choices[0].message.content)
```

# [REST](#tab/rest)

```http
POST https://<myResourceName>.openai.azure.com/openai/deployments/<myDeploymentName>/chat/completions?api-version=2024-10-21
Content-Type: application/json
api-key: <myAPIKey>

{
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "What is provisioned throughput?" }
  ],
  "max_tokens": 100
}
```

---

> [!TIP]
> Set `max_tokens` close to your expected response size. The service estimates compute cost using the `max_tokens` value — setting it much higher than the actual response length reduces the number of concurrent requests your deployment can handle.

## View deployment utilization

After making calls, confirm that traffic is reaching your deployment by checking its utilization in the Azure portal.

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Navigate to your Foundry resource and select **Metrics** in the left navigation.
1. Select the **Provisioned-managed utilization V2** metric.
1. If you have more than one deployment in the resource, select **Apply Splitting** to view utilization per deployment.

A utilization reading near 0% immediately after your test call is normal — the metric updates on a monitoring window. [TO VERIFY: confirm metric update frequency or window duration]

For a full explanation of how utilization is calculated and what to do when it reaches 100%, see [Operate provisioned deployments in production](./how-to/provisioned-get-started.md#measure-deployment-utilization).

## Consider purchasing a reservation

Your deployment is billed at the hourly rate. If you plan to keep it running for more than a few days, purchasing an **Azure Reservation** reduces your effective $/PTU/hr cost compared to hourly billing.

> [!IMPORTANT]
> Always create and confirm your deployment before purchasing a reservation. The reservation must match your deployment's type (Global, Data Zone, or Regional), region, and subscription scope. Committing to a reservation for capacity you haven't confirmed is available can result in a financial commitment you can't use.

For sizing guidance, purchase steps, and management, see [Azure Reservations for provisioned throughput](./how-to/provisioned-throughput-onboarding.md#azure-reservations-for-provisioned-throughput).

## Clean up resources

To stop hourly billing, delete the deployment.

> [!IMPORTANT]
> Deleting the Foundry resource doesn't automatically delete its deployments. Always delete all deployments before deleting the resource, as charges for deployments on a deleted resource continue until the resource is purged. See [Delete deployments before deleting resources](./how-to/provisioned-throughput-onboarding.md#delete-deployments-before-deleting-resources).

1. In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), navigate to your resource.
1. Select the deployment, then select **Delete** and confirm.

> [!NOTE]
> Deleting a deployment doesn't cancel an Azure Reservation. If you purchased one, cancel or exchange it separately on the [Reservations page in the Azure portal](https://portal.azure.com/#view/Microsoft_Azure_Reservations/ReservationsBrowseBlade/productType/Reservations). Cancellation might incur an early termination fee.

## Next step

- [Operate provisioned deployments in production](./how-to/provisioned-get-started.md)
