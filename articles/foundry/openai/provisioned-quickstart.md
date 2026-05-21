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
ms.date: 05/20/2026
recommendations: false
#customerIntent: As a developer, I want to create a provisioned throughput deployment and make my first inference call so I can start using dedicated model capacity for my application.
---

# Quickstart: Create a provisioned throughput deployment

In this quickstart, you create a provisioned throughput deployment in Microsoft Foundry, make an inference call to confirm it works, and view its utilization metric.

A provisioned throughput deployment gives your application dedicated model processing throughput with predictable latency. Billing is done per provisioned throughput unit (PTU) per hour. For long-term workloads, Azure Reservations offer financial discounts compared to hourly billing. For a full conceptual introduction, see [What is provisioned throughput for Foundry Models?](./concepts/provisioned-throughput.md).


## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.
- **Azure Contributor** or **Cognitive Services Contributor** role on the subscription or resource group where you plan to create the deployment.
- A [Microsoft Foundry project](../how-to/create-projects.md) in the region where you have PTU quota. A Foundry project is managed under a Foundry resource.
- Optionally, for deployment using Azure CLI, have [Azure CLI installed](/cli/azure/install-azure-cli).

## Check model and region availability

Before creating a deployment, confirm that your model supports provisioned throughput in your target region.

1. Go to the [model and region availability table](../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=provisioned) to see if your model supports provisioned throughput deployment in your target region.
1. Filter by your region and verify that the model appears in a **Provisioned** deployment type.

Also note the model's minimum PTU count, as you need this information when you configure the deployment. Minimums vary by model and are listed in [Deployment parameters and throughput values by model](./how-to/determine-ptu-requirements.md#deployment-parameters-and-throughput-values-by-model).

## Check PTU quota

Before following this quickstart, check that you have quota for your target region and deployment type. To check your quota:

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]
1. Select the subscription and the Foundry resource in the region where you have PTU quota.
1. Select **Operate** in the upper-right navigation, then select **Quota** in the left pane.
1. Select **Provisioned throughput unit** to see your available quota. If you don't have quota, select **Request Quota** and complete the form. Quota approval can take several days, and you receive an email notification when the request is approved.

    > [!TIP]
    > You can also follow this [direct link to the quota request form](https://aka.ms/oai/stuquotarequest).

## Create a provisioned deployment

### Use the Foundry portal for deployment

1. Select **Discover** in the upper-right navigation, then select **Models** in the left pane.
1. Select the model you want to deploy to open its model card, such as `gpt-5.1`.
1. Select **Deploy** > **Custom settings**.
1. In the **Deployment type** dropdown, select a provisioned deployment type: **Global Provisioned Throughput**, **Data Zone Provisioned Throughput**, or **Regional Provisioned Throughput**.
1. Fill in the deployment fields:

   | Field | Description |
   |---|---|
   | **Deployment name** | A name you choose. Use this name in your code to call the model. |
   | **Model** | The model to deploy, e.g., `gpt-5.1`. |
   | **Model version** | The version of the model. |
   | **Provisioned throughput units** | The number of PTUs to allocate. Must meet the model's minimum, e.g., `50`. |
   | **Content filter** | The filtering policy. See [Content filtering](../../foundry-classic/foundry-models/concepts/content-filter.md). |

1. Select **Confirm pricing** to review the hourly rate for the deployment. **Billing starts immediately the deployment is created, even when no requests are being sent**. You stop billing by deleting your deployment. If you're unsure of the costs, select **Cancel** and review [PTU billing, sizing, and cost management](./concepts/provisioned-throughput-billing.md) before continuing.

1. Confirm and create the deployment.

### (Optional) Use the Azure CLI for deployment

Alternatively, you can create your deployment by using the Azure CLI. 

1. Create a provisioned deployment for GPT-5.1 with a PTU count of 50 PTUs.

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

    - Replace `<myResourceName>`, `<myResourceGroupName>`, `<myDeploymentName>` with your values.
    
    - `--sku-name` specifies the deployment type: `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged`.
    
    - `--sku-capacity` is the number of PTUs. Here, it's set to 50.
    
    Reference: [az cognitiveservices account deployment](/cli/azure/cognitiveservices/account/deployment)

1. Confirm that the deployment completed successfully:
 
    ```azurecli
    az cognitiveservices account deployment show \
        --deployment-name <myDeploymentName> \
        --name <myResourceName> \
        --resource-group <myResourceGroupName> \
        --query "properties.provisioningState" -o tsv
    ```

    The output should display `Succeeded`. The model is ready to use after provisioning completes.

    Reference: [az cognitiveservices account deployment show](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-show)

REST, ARM template, Bicep, and Terraform can also be used to create deployments. See [Automate deployments](../../foundry-classic/openai/how-to/quota.md?tabs=rest#automate-deployment) and replace `sku.name` with `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged`.

## Make an inference call

The inference code for a provisioned deployment is the same as for any other deployment type. Use your deployment name (not the model name) as the `model` parameter value.

The code in this section uses API key authentication. You can also use Entra ID authentication. For details on using Entra ID authentication when making an inference call, see [How to generate text responses with Microsoft Foundry Models](../foundry-models/how-to/generate-responses.md).

Before running the sample, set the following environment variable:

- `AZURE_OPENAI_API_KEY`: your resource API key.

> [!IMPORTANT]
> Don't hard-code credentials in your application. For production workloads, use a secure credential store such as [Azure Key Vault](/azure/key-vault/general/overview). See [Security features for Azure AI services](../../ai-services/security-features.md).

1. Install the OpenAI SDK:

    ```bash
    pip install openai
    ```

1. Configure the OpenAI client, specify your deployment, and generate responses. Replace `<myResourceName>` with your Foundry resource name.

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
    
    print(response.output_text)
    ```

## View deployment utilization

After making calls, confirm that traffic is reaching your deployment by checking its utilization in the Azure portal.

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Navigate to your Foundry resource and select **Metrics** in the left navigation.
1. Select the **Provisioned-managed utilization V2** metric.
1. If you have more than one deployment in the resource, filter by the deployment name to view utilization per deployment.

A utilization reading near 0% immediately after your test call is normal — the metric updates on a monitoring window.

:::image type="content" source="media/provisioned-quickstart/provisioned-managed-utilization-v2-metric.png" alt-text="Screenshot of Azure Metrics showing Provisioned-managed Utilization V2 chart filtered by deployment name." lightbox="media/provisioned-quickstart/provisioned-managed-utilization-v2-metric.png":::

For a full explanation of how utilization is calculated and what to do when it reaches 100%, see [Operate provisioned deployments in production](./how-to/provisioned-get-started.md#measure-deployment-utilization).


## Consider setting up spillover

Spillover automatically routes overflow requests from your provisioned deployment to a standard deployment in the same Foundry resource. When your provisioned deployment is fully utilized and returns a `429` code, spillover redirects those excess requests to the standard deployment instead of failing them, helping reduce disruptions during traffic bursts.


To enable spillover for all requests on your deployment, you need an active standard deployment for the same model and version in the same Foundry resource as your provisioned deployment. Follow these steps to enable it:

### Enable spillover in the Foundry portal

Enable spillover during deployment creation by selecting **Traffic spillover** in the custom deployment settings. If you already created your deployment without spillover, delete and recreate it with **Traffic spillover** selected.

### (Optional) Use the REST API to enable spillover

Set the `spilloverDeploymentName` property on an existing provisioned deployment to the name of the target standard deployment. This approach lets you add spillover to an existing deployment without recreating it.

You can also enable spillover selectively per request, using the `x-ms-spillover-deployment` request header, which gives you fine-grained control over when overflow routing applies.

For step-by-step instructions on both approaches, and guidance on monitoring spillover requests, see [Manage traffic with spillover for provisioned deployments](./how-to/spillover-traffic-management.md).


## Consider purchasing a reservation

Your deployment is billed at the hourly rate. If you plan to keep it running for more than a few days, purchasing an **Azure Reservation** reduces your effective $/PTU/hr cost compared to hourly billing.

If you plan to purchase a reservation after creating your deployment, verify that you have the **owner role** or **reservation purchaser role** on an Azure subscription. The role needed to purchase reservations differs from the role needed to create deployments. See [Provisioned Throughput reservations](https://aka.ms/oai/docs/ptum-reservations) for role requirements.

> [!IMPORTANT]
> Always create and confirm your deployment before purchasing a reservation. The reservation must match your deployment's type (Global, Data Zone, or Regional), region, and subscription scope. Committing to a reservation for capacity you haven't confirmed is available can result in a financial commitment you can't use.

For sizing guidance, purchase steps, and management, see [Azure Reservations for provisioned throughput](./concepts/provisioned-throughput-billing.md#azure-reservations-for-provisioned-throughput).


## Clean up resources

Deleting the Foundry resource doesn't automatically delete its deployments. Always delete all deployments before deleting the resource, as charges for deployments on a deleted resource continue until the resource is purged. See [Clean up resources](./how-to/provisioned-get-started.md#clean-up-resources).

> [!NOTE]
> Deleting a deployment doesn't cancel an Azure Reservation. If you purchased one, cancel or exchange it separately on the [Reservations page in the Azure portal](https://portal.azure.com/#view/Microsoft_Azure_Reservations/ReservationsBrowseBlade/productType/Reservations). Cancellation might incur an early termination fee.


Follow these steps to stop hourly billing by deleting the deployment.

### Delete deployment in the Foundry portal

1. In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), navigate to your resource.
1. Select the deployment, then select **Delete** and confirm.
 
### (Optional) Delete deployment with the Azure CLI

```azurecli
az cognitiveservices account deployment delete \
    --deployment-name <myDeploymentName> \
    --name <myResourceName> \
    --resource-group <myResourceGroupName>
```

Reference: [az cognitiveservices account deployment delete](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-delete)


## Next step

- [Operate provisioned deployments in production](./how-to/provisioned-get-started.md)
