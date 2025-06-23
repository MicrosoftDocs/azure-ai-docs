---
title: Deploy Azure AI Foundry Models to managed compute with pay-as-you-go billing 
titleSuffix: Azure AI Foundry
description: Learn how to deploy protected models from partners and community on Azure AI Foundry managed compute and understand how pay-as-you-go surcharge billing works.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
ms.topic: how-to
ms.date: 06/23/2025
ms.reviewer: tinaem
reviewer: tinaem
ms.author: mopeakande
author: msakande
---

# Deploy Azure AI Foundry Models with pay-as-you-go billing to managed compute

Azure AI Foundry Models include a comprehensive catalog of models organized into two categories—Models sold directly by Azure, and [Models from partners and community](../concepts/foundry-models-overview.md#models-from-partners-and-community). These models from partners and community, which are available for deployment on a managed compute, are either open or protected models. In this article, you learn how to use protected models from partners and community, offered via Azure Marketplace for deployment on managed compute with pay-as-you-go billing. 


## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- If you don't have one, [create a [!INCLUDE [hub](../includes/hub-project-name.md)]](create-projects.md?pivots=hub-project).

- [Azure Marketplace purchases enabled](/azure/cost-management-billing/manage/enable-marketplace-purchases) for your Azure subscription.

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned a *custom role* with the following permissions. User accounts assigned the *Owner* or *Contributor* role for the Azure subscription can also create deployments. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).


- On the Azure subscription— **to subscribe the workspace/project to the Azure Marketplace offering**:

  - Microsoft.MarketplaceOrdering/agreements/offers/plans/read
  - Microsoft.MarketplaceOrdering/agreements/offers/plans/sign/action
  - Microsoft.MarketplaceOrdering/offerTypes/publishers/offers/plans/agreements/read
  - Microsoft.Marketplace/offerTypes/publishers/offers/plans/agreements/read
  - Microsoft.SaaS/register/action

- On the resource group— **to create and use the SaaS resource**:

  - Microsoft.SaaS/resources/read
  - Microsoft.SaaS/resources/write

- On the workspace— **to deploy endpoints**:

  - Microsoft.MachineLearningServices/workspaces/marketplaceModelSubscriptions/*
  - Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*

## Subscription scope and unit of measure for Azure Marketplace offer

Azure AI Foundry enables a seamless subscription and transaction experience for protected models as you create and consume your dedicated model deployments at scale. The deployment of protected models on managed compute involves pay-as-you-go billing for the customer in two dimensions: 

- Per-hour Azure Machine Learning compute billing for the virtual machines employed in the deployment.
- Surcharge billing for the model as set by the model publisher on the Azure Marketplace offer. 

Pay-as-you-go billing of Azure compute and model surcharge are pro-rated per minute based on the uptime of the managed online deployments. The surcharge for a model is a per GPU-hour price, set by the partner (or model's publisher) on Azure Marketplace, for all the supported GPUs that can be used to deploy the model on Azure AI Foundry managed compute.  

A user's subscription to Azure Marketplace offers are scoped to the project resource within Azure AI Foundry. If a subscription to the Azure Marketplace offer for a particular model already exists within the project, the user is informed in the deployment wizard that the subscription already exists for the project. 

To find all the SaaS subscriptions that exist in an Azure subscription:

1. Sign in to the [Azure portal](https://portal.azure.com) and go to your Azure subscription.

1. Select **Subscriptions** and then select your Azure subscription to open its overview page.

1. Select **Settings** > **Resources**  to see the list of resources.

1. Use the **Type** filter to select the SaaS resource type.
 
The consumption-based surcharge is accrued to the associated SaaS subscription and billed to a user via Azure Marketplace. You can view the invoice in the **Overview** tab of the respective SaaS subscription.

## Subscribe and deploy on managed compute

1. Sign in to [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs).
1. If you're not already in your project, select it. 
1. Select **Model catalog** from the left pane.
1. Select the **Deployment options** filter in the model catalog and choose **Managed compute**.
1. Filter the list further by selecting the **Collection** and model of your choice. In this article, we use **Cohere Command A** from the [list of supported models](#supported-models-for-managed-compute-deployment-with-pay-as-you-go-billing) for illustration.
1. From the model's page, select **Use this model** to open the deployment wizard.
1. Choose from one of the supported VM SKUs for the model. You need to have Azure Machine Learning Compute quota for that SKU in your Azure subscription.
1. Select **Customize** to specify your deployment configuration for parameters such as the instance count. You can also select an existing endpoint for the deployment or create a new one. For this example, we specify an instance count of **1** and create a new endpoint for the deployment.

    :::image type="content" source="../media/deploy-models-managed-pay-go/deployment-configuration.png" alt-text="Screenshot of the deployment configuration screen for a protected model in Azure AI Foundry." lightbox="../media/deploy-models-managed-pay-go/deployment-configuration.png":::

1. Select **Next** to proceed to the *pricing breakdown* page.
1. Review the pricing breakdown for the deployment, terms of use, and license agreement associated with the model's offer on Azure Marketplace. The pricing breakdown tells you what the aggregated pricing for the deployed model would be, where the surcharge for the model is a function of the number of GPUs in the VM instance that is selected in the previous steps. In addition to the applicable surcharge for the model, Azure compute charges also apply, based on your deployment configuration. If you have existing reservations or Azure savings plan, the invoice for the compute charges honors and reflects the discounted VM pricing.

    :::image type="content" source="../media/deploy-models-managed-pay-go/pricing-breakdown.png" alt-text="Screenshot of the pricing breakdown page for a protected model deployment in Azure AI Foundry." lightbox="../media/deploy-models-managed-pay-go/pricing-breakdown.png":::

1. Select the checkbox to acknowledge that you understand and agree to the terms of use. Then, select **Deploy**. Azure AI Foundry creates the user's subscription to the marketplace offer and then creates the deployment of the model on a managed compute. It takes about 15-20 minutes for the deployment to complete.

## Network isolation of deployments

Collections in the model catalog can be deployed within your isolated networks using workspace managed virtual network. For more information on how to configure your workspace managed networks, see [Configure a managed virtual network to allow internet outbound](../../machine-learning/how-to-managed-network.md#configure-a-managed-virtual-network-to-allow-internet-outbound).

#### Limitation

An Azure AI Foundry project with ingress Public Network Access disabled can only support a single active deployment of one of the protected models from the catalog. Attempts to create more active deployments result in deployment creation failures.

## Supported models for managed compute deployment with pay-as-you-go billing

| Collection | Model | Task |
|--|--|--|
| Paige AI | [Virchow2G](https://ai.azure.com/explore/models/Virchow2G/version/1/registry/azureml-paige) | Image Feature Extraction |
| Paige AI | [Virchow2G-Mini](https://ai.azure.com/explore/models/Virchow2G-Mini/version/1/registry/azureml-paige) | Image Feature Extraction |
| Cohere | [Command A](https://ai.azure.com/explore/models/cohere-command-a/version/3/registry/azureml-cohere) | Chat completion |
| Cohere | [Embed v4](https://ai.azure.com/explore/models/embed-v-4-0/version/4/registry/azureml-cohere) | Embeddings |
| Cohere | [Rerank v3.5](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/2/registry/azureml-cohere) | Text classification |



## Related content

* [How to deploy and inference a managed compute deployment](deploy-models-managed.md)
* [Explore Azure AI Foundry Models](../concepts/foundry-models-overview.md)

