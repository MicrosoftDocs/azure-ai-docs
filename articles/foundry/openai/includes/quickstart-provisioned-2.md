---
title: Include file
description: Include file
author: msakande
ms.reviewer: seramasu
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/25/2026
ms.custom: include
---

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

REST, ARM template, Bicep, and Terraform can also be used to create deployments. See [Automate deployments](../../../foundry-classic/openai/how-to/quota.md?tabs=rest#automate-deployment) and replace `sku.name` with `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged`.

## Make an inference call

The inference code for a provisioned deployment is the same as for any other deployment type. Use your deployment name (not the model name) as the `model` parameter value.

The code in this section uses API key authentication. You can also use Entra ID authentication. For details on using Entra ID authentication when making an inference call, see [How to generate text responses with Microsoft Foundry Models](../../foundry-models/how-to/generate-responses.md).

Before running the sample, set the following environment variable:

- `AZURE_OPENAI_API_KEY`: your resource API key.

> [!IMPORTANT]
> Don't hard-code credentials in your application. For production workloads, use a secure credential store such as [Azure Key Vault](/azure/key-vault/general/overview). See [Security features for Azure AI services](../../../ai-services/security-features.md).

# [Python SDK](#tab/python)

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

# [REST API](#tab/rest-api)

Send a POST request to the Responses API endpoint. Replace `<myResourceName>` with your Foundry resource name and `<myDeploymentName>` with your deployment name.

```bash
curl https://<myResourceName>.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "<myDeploymentName>",
    "input": "What is provisioned throughput?",
    "max_output_tokens": 100
  }'
```

---

## View deployment utilization

After making calls, confirm that traffic is reaching your deployment by checking its utilization in the Azure portal.

1. Sign in to the [Azure portal](https://portal.azure.com).
1. Navigate to your Foundry resource and select **Metrics** in the left navigation.
1. Select the **Provisioned-managed utilization V2** metric.
1. If you have more than one deployment in the resource, filter by the deployment name to view utilization per deployment.

A utilization reading near 0% immediately after your test call is normal — the metric updates on a monitoring window.

:::image type="content" source="../media/provisioned-quickstart/provisioned-managed-utilization-v2-metric.png" alt-text="Screenshot of Azure Metrics showing Provisioned-managed Utilization V2 chart filtered by deployment name." lightbox="../media/provisioned-quickstart/provisioned-managed-utilization-v2-metric.png":::

For a full explanation of how utilization is calculated and what to do when it reaches 100%, see [Operate provisioned deployments in production](../how-to/provisioned-get-started.md#measure-deployment-utilization).


## Consider setting up spillover

Spillover automatically routes overflow requests from your provisioned deployment to a standard deployment in the same Foundry resource. When your provisioned deployment is fully utilized and returns a `429` code, spillover redirects those excess requests to the standard deployment instead of failing them, helping reduce disruptions during traffic bursts. To learn more about enabling spillover and monitoring spillover requests, see [Manage traffic with spillover for provisioned deployments](../how-to/spillover-traffic-management.md).


## Consider purchasing a reservation

Your deployment is billed at the hourly rate. If you plan to keep it running for more than a few days, purchasing an **Azure Reservation** reduces your effective $/PTU/hr cost compared to hourly billing.

If you plan to purchase a reservation after creating your deployment, verify that you have the **owner role** or **reservation purchaser role** on an Azure subscription. The role needed to purchase reservations differs from the role needed to create deployments. See [Provisioned Throughput reservations](https://aka.ms/oai/docs/ptum-reservations) for role requirements.

> [!IMPORTANT]
> Always create and confirm your deployment before purchasing a reservation. The reservation must match your deployment's type (Global, Data Zone, or Regional) and subscription scope. For Data Zone and Regional deployments, the reservation region must also match. For Global deployments, a single Global reservation can cover Global PTU deployments across multiple regions. Committing to a reservation for capacity you haven't confirmed is available can result in a financial commitment you can't use.

For sizing guidance, purchase steps, and management, see [Azure Reservations for provisioned throughput](../concepts/provisioned-throughput-billing.md#azure-reservations-for-provisioned-throughput).


## Clean up resources

Deleting the Foundry resource doesn't automatically delete its deployments. Always delete all deployments before deleting the resource, as charges for deployments on a deleted resource continue until the resource is purged. See [Clean up resources](../how-to/provisioned-get-started.md#clean-up-resources).

> [!NOTE]
> Deleting a deployment doesn't cancel an Azure Reservation. If you purchased one, cancel or exchange it separately on the [Reservations page in the Azure portal](https://portal.azure.com/#view/Microsoft_Azure_Reservations/ReservationsBrowseBlade/productType/Reservations). Cancellation might incur an early termination fee.


Follow these steps to stop hourly billing by deleting the deployment.

### Delete deployment in the Foundry portal

1. In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), navigate to your deployments.
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

- [What is provisioned throughput for Foundry Models?](../concepts/provisioned-throughput.md)
