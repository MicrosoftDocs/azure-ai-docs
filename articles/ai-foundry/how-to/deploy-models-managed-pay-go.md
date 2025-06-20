---
title: Deploy Azure AI Foundry Models with pay-as-you-go billing to managed compute
titleSuffix: Azure AI Foundry
description: Learn how to deploy protected models from partners and community on Azure AI Foundry managed compute and understand how pay-as-you-go surcharge billing works.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
ms.topic: how-to
ms.date: 06/20/2025
ms.reviewer: tinaem
reviewer: tinaem
ms.author: mopeakande
author: msakande
---

# Deploy Azure AI Foundry Models with pay-as-you-go billing to managed compute

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Azure AI Foundry Models include a comprehensive catalog of models organized into two categories—Models sold directly by Azure, and Models from partners and community. These models from partners and community, which are available for deployment on a managed compute, are either open or protected models. The deployment of protected models on managed compute (preview) involves pay-as-you-go billing for the customer in two dimensions: per-hour Azure Machine Learning compute billing for the virtual machines employed in the deployment, and surcharge billing for the model as set by the model publisher on the Azure Marketplace offer. This pay-as-you-go billing of Azure compute and model surcharge is pro-rated per minute based on the uptime of these managed online deployments.

In this article, you learn how to use protected models from partners and community, offered via Azure Marketplace for deployment on managed compute. Azure AI Foundry enables a seamless subscription and transaction experience for these protected models as you create and consume your dedicated model deployments at scale.

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- If you don't have one, [create a [!INCLUDE [hub](../includes/hub-project-name.md)]](create-projects.md?pivots=hub-project).

- [Azure Marketplace purchases enabled](/azure/cost-management-billing/manage/enable-marketplace-purchases) for your Azure subscription.

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned a *custom role* with the following permissions. User accounts assigned the *Owner* or *Contributor* role for the Azure subscription can also create deployments. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).


- On the Azure subscription—**to subscribe the workspace/project to the Azure Marketplace offering**:

  - Microsoft.MarketplaceOrdering/agreements/offers/plans/read
  - Microsoft.MarketplaceOrdering/agreements/offers/plans/sign/action
  - Microsoft.MarketplaceOrdering/offerTypes/publishers/offers/plans/agreements/read
  - Microsoft.Marketplace/offerTypes/publishers/offers/plans/agreements/read
  - Microsoft.SaaS/register/action

- On the resource group—**to create and use the SaaS resource**:

  - Microsoft.SaaS/resources/read
  - Microsoft.SaaS/resources/write

- On the workspace—**to deploy endpoints**:

  - Microsoft.MachineLearningServices/workspaces/marketplaceModelSubscriptions/*
  - Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*

## Subscribe and deploy on managed compute

1.  Sign in to [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) and go to the Home page.

1.  Select Model catalog from the left sidebar.

1.  In the filters section, select the Deployment Option as Managed Compute.

1.  Select the Collection and model of your choice. In this article, we are using **Cohere Command A** as an example.

1.  Click on **Use this model** and pick the Managed Compute deployment option.

1.  The Deploy wizard lets you choose from one of the supported VM SKUs for the model. You need to have Azure Machine Learning Compute quota for that SKU in your Azure subscription.

1.  You can then customize your deployment configuration for parameters such as the instance count and select an existing endpoint for the deployment or create a new one. For this example, we consider an instance count of **1** and create a new endpoint for the deployment.

  :::image type="content" source="media/deploy-models-managed-pay-go/deployment-configuration.png" alt-text="Screenshot of the deployment configuration screen for a protected model in Azure AI Foundry." lightbox="media/deploy-models-managed-pay-go/deployment-configuration.png":::

1.  Click **Next** to proceed to the pricing breakdown page.

1.  Review the pricing breakdown for the deployment, terms of use and license agreement associated with the model's offer on Marketplace. The pricing breakdown helps inform what the aggregated pricing for the model deployed would be, where the surcharge for the model is a function of the number of GPUs in the VM instance that is selected in the previous steps. In addition to the applicable surcharge for the model, Azure Compute charges also apply based on your deployment configuration. If you have existing reservations or azure savings plan, the invoice for the compute charges will honor and reflect the discounted VM pricing.

  :::image type="content" source="media/deploy-models-managed-pay-go/pricing-breakdown.png" alt-text="Screenshot of the pricing breakdown page for a protected model deployment in Azure AI Foundry." lightbox="media/deploy-models-managed-pay-go/pricing-breakdown.png":::

1.  Select the checkbox to acknowledge understanding of pricing and terms of use, and then, click **Deploy**. It takes about 15-20 mins for the deployment to complete.

## Network Isolation of deployments

Collections in the model catalog can be deployed within your isolated networks using workspace managed virtual network. For more information on how to configure your workspace managed networks, see [here.](/azure/machine-learning/how-to-managed-network#configure-a-managed-virtual-network-to-allow-internet-outbound)

#### Limitation

An Azure AI Foundry project with ingress Public Network Access disabled can only support a single active deployment of one of the protected models from the catalog. Attempts to create more active deployments result in deployment creation failures.


## Related content

* [How to deploy and inference a managed compute deployment](deploy-models-managed.md)
