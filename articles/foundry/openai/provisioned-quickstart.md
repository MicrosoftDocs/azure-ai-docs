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

A provisioned throughput deployment gives your application dedicated model processing throughput with predictable latency. Billing is done per provisioned throughput unit (PTU) per hour. You also have the option of using Azure Reservations with provisioned throughput to obtain financial discounts that are more cost-effective than hourly billing for long-term, sustained workloads. For a full conceptual introduction, see [What is provisioned throughput for Foundry Models?](./concepts/provisioned-throughput.md).

<!-- > [!NOTE]
> If you don't already have PTU quota, request it through the [quota request form](https://aka.ms/oai/stuquotarequest) before following this quickstart. Quota approval can take several days, and you receive an email notification when the request is approved.. -->

## Prerequisites

- An Azure subscription — [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- **Azure Contributor** or **Cognitive Services Contributor** role on the subscription or resource group where you plan to create the deployment.
- A Foundry resource in the region where you have PTU quota. See [Create a Foundry resource](../../foundry-classic/openai/how-to/create-resource.md).
<!-- - PTU quota approved for your target region and deployment type. To check your quota, go to **Operate** > **Quota** > **Provisioned throughput unit** in the [Foundry portal](https://ai.azure.com/?cid=learnDocs). If you don't have quota, select **Request Quota** and complete the form. -->
- Optionally, for deployment using Azure CLI, have [Azure CLI installed](/cli/azure/install-azure-cli).

## Check model and region availability

Before creating a deployment, confirm that your model supports provisioned throughput in your target region.

1. Go to the [model and region availability table](../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=provisioned) to see if your model supports provisioned throughput deployment in your target region.
1. Filter by your region and verify that the model appears in a **Provisioned** deployment type.

Also note the model's minimum PTU count, as you need this information when you configure the deployment. Minimums vary by model and are listed in [Throughput and deployment parameter values by model](./how-to/provisioned-throughput-onboarding.md#throughput-and-deployment-parameter-values-by-model).

## Create a provisioned deployment

**Using the Foundry portal:**

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]
1. Select the subscription and the Foundry resource in the region where you have PTU quota.
1. Select **Discover** in the upper-right navigation, then select **Models** in the left pane.
1. Select the model you want to deploy to open its model card, such as `gpt-5.1`.
1. Select **Deploy** > **Custom settings**.
1. In the **Deployment type** dropdown, select a provisioned deployment type: **Global Provisioned Throughput**, **Data Zone Provisioned Throughput**, or **Regional Provisioned Throughput**.
1. Fill in the deployment fields:

   | Field | Description |
   |---|---|
   | **Deployment name** | A name you choose. Use this name in your code to call the model. |
   | **Model** | The model to deploy. |
   | **Model version** | The version of the model. |
   | **Provisioned throughput units** | The number of PTUs to allocate. Must meet the model's minimum. |
   | **Content filter** | The filtering policy. See [Content filtering](../../foundry-classic/foundry-models/concepts/content-filter.md). |

1. Select **Confirm pricing** to review the hourly rate for the deployment. **Billing starts immediately the deployment is created, even when no requests are being sent**. You stop billing by deleting your deployment. If you're unsure of the costs, select **Cancel** and review [PTU billing, sizing, and cost management](./how-to/provisioned-throughput-onboarding.md) before continuing.

1. Confirm and create the deployment.

**Optionally, create deployment with the Azure CLI:**

Alternatively, you can create your deployment by using the Azure CLI. The following code snippet shows how to use the CLI to create a provisioned deployment for GPT-5.1 with a PTU count of 50 PTUs.

- Replace `<myResourceName>`, `<myResourceGroupName>`, `<myDeploymentName>` with your values.

- `--sku-name` specifies the deployment type, which could be one of `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged`. 

- `--sku-capacity` is the number of PTUs. Here, it's set to 100.

```azurecli
az cognitiveservices account deployment create \
--name <myResourceName> \
--resource-group <myResourceGroupName> \
--deployment-name <myDeploymentName> \
--model-name GPT-5.1 \
--model-version "2025-11-13" \
--model-format OpenAI \
--sku-capacity 50 \
--sku-name GlobalProvisionedManaged
```

Reference: [az cognitiveservices account deployment](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account/deployment)

Confirm that the deployment completed successfully:
 
```azurecli
az cognitiveservices account deployment show \
    --deployment-name <myDeploymentName> \
    --name <myResourceName> \
    --resource-group <myResourceGroupName> \
| jq '.properties.provisioningState'
```

The output should display `"Succeeded"`. The model is ready to use after provisioning completes.

Reference: [az cognitiveservices account list-models](https://learn.microsoft.com/cli/azure/cognitiveservices/account#az-cognitiveservices-account-deployment-show)

REST, ARM template, Bicep, and Terraform can also be used to create deployments. See [Automate deployments](../../foundry-classic/openai/how-to/quota.md?tabs=rest#automate-deployment) and replace `sku.name` with `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged`.

## Make an inference call

The inference code for a provisioned deployment is the same as for any other deployment type. Use your deployment name (not the model name) as the `model` parameter value.

The code in this section uses API key authentication. You can also use Entra ID authentication. For details on using Entra ID authentication when making an inference call, see [How to generate text responses with Microsoft Foundry Models](../foundry-models/how-to/generate-responses.md).

Before running the sample, set the following environment variable:

- `AZURE_OPENAI_API_KEY` — Your resource API key.

> [!IMPORTANT]
> Don't hard-code credentials in your application. For production workloads, use a secure credential store such as [Azure Key Vault](/azure/key-vault/general/overview). See [Security features for Azure AI services](../../ai-services/security-features.md).

1. Install the OpenAI SDK:

    ```bash
    pip install openai
    ```

1. Configure the OpenAI client object in the project route, specify your deployment, and generate responses.

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://<myResourceName>.openai.azure.com/openai/v1/",
)

response = client.responses.create(
    model="<myDeploymentName>",  # Your deployment name, not the model name
    input="What is provisioned throughput?",
    max_output_tokens=100,
)

print(response.choices[0].message.content)
```

## View deployment utilization

After making calls, confirm that traffic is reaching your deployment by checking its utilization in the Azure portal.

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Navigate to your Foundry resource and select **Metrics** in the left navigation.
1. Select the **Provisioned-managed utilization V2** metric.
1. If you have more than one deployment in the resource, filter by the deployment name to view utilization per deployment.

For a full explanation of how utilization is calculated and what to do when it reaches 100%, see [Operate provisioned deployments in production](./how-to/provisioned-get-started.md#measure-deployment-utilization).


## Consider setting up spillover

Spillover automatically routes overflow requests from your provisioned deployment to a standard deployment in the same Foundry resource. When your provisioned deployment is fully utilized and returns a `429` code, spillover redirects those excess requests to the standard deployment instead of failing them, helping reduce disruptions during traffic bursts.


To enable spillover for all requests on your deployment, you need an active standard deployment for the same model and version in the same Foundry resource as your provisioned deployment. Follow these steps to enable it:

**Using the Foundry portal:**

Enable spillover during deployment creation by selecting **Traffic spillover** in the custom deployment settings. If you already created your deployment without spillover, delete and recreate it with **Traffic spillover** selected.

**Optionally, enable spillover with the Azure CLI:**

Set the `spilloverDeploymentName` property on an existing provisioned deployment to the name of the target standard deployment. This approach lets you add spillover to an existing deployment without recreating it.

You can also enable spillover selectively per request, using the `x-ms-spillover-deployment` request header, which gives you fine-grained control over when overflow routing applies.

For step-by-step instructions on both approaches, and guidance on monitoring spillover requests, see [Manage traffic with spillover for provisioned deployments](./how-to/spillover-traffic-management.md).


## Consider purchasing a reservation

Your deployment is billed at the hourly rate. If you plan to keep it running for more than a few days, purchasing an **Azure Reservation** reduces your effective $/PTU/hr cost compared to hourly billing.

If you plan to purchase a reservation after creating your deployment, verify that you have the **owner role** or **reservation purchaser role** on an Azure subscription. The role needed to purchase reservations differs from the role needed to create deployments. See [Provisioned Throughput reservations](https://aka.ms/oai/docs/ptum-reservations) for role requirements.

> [!IMPORTANT]
> Always create and confirm your deployment before purchasing a reservation. The reservation must match your deployment's type (Global, Data Zone, or Regional), region, and subscription scope. Committing to a reservation for capacity you haven't confirmed is available can result in a financial commitment you can't use.

For sizing guidance, purchase steps, and management, see [Azure Reservations for provisioned throughput](./how-to/provisioned-throughput-onboarding.md#azure-reservations-for-provisioned-throughput).


## Clean up resources

Deleting the Foundry resource doesn't automatically delete its deployments. Always delete all deployments before deleting the resource, as charges for deployments on a deleted resource continue until the resource is purged. See [Delete deployments before deleting resources](./how-to/provisioned-throughput-onboarding.md#delete-deployments-before-deleting-resources).

> [!NOTE]
> Deleting a deployment doesn't cancel an Azure Reservation. If you purchased one, cancel or exchange it separately on the [Reservations page in the Azure portal](https://portal.azure.com/#view/Microsoft_Azure_Reservations/ReservationsBrowseBlade/productType/Reservations). Cancellation might incur an early termination fee.


Follow these steps to stop hourly billing by deleting the deployment.

**Using the Foundry portal:**

1. In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), navigate to your resource.
1. Select the deployment, then select **Delete** and confirm.
 
**Optionally, delete deployment with the Azure CLI:**

```azurecli
az cognitiveservices account deployment delete \
    --deployment-name <myDeploymentName> \
    --name <myResourceName> \
    --resource-group <myResourceGroupName>
```

Reference: [az cognitiveservices account deployment delete](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-delete)


## Next step

- [Operate provisioned deployments in production](./how-to/provisioned-get-started.md)
