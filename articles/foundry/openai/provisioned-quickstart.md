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
ms.date: 05/22/2026
recommendations: false
#customerIntent: As a developer, I want to create a provisioned throughput deployment and make my first inference call so I can start using dedicated model capacity for my application.
---

# Quickstart: Create a provisioned throughput deployment

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **New Foundry portal version** - [Switch to version for the classic Foundry portal](../../foundry-classic/openai/provisioned-quickstart.md)

[!INCLUDE [quickstart-provisioned-1](includes/quickstart-provisioned-1.md)]

## Check PTU quota

Before following this quickstart, check that you have quota for your target region and deployment type. To check your quota:

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]
1. Select the subscription and the Foundry resource in the region where you have PTU quota.
1. Select **Operate** in the upper-right navigation, then select **Quota** in the left pane.
1. Select **Provisioned throughput unit** to see your available quota. If you don't have quota, select **Request Quota** and complete the form. Quota approval can take several days, and you receive an email notification when the request is approved.

    > [!TIP]
    > You can also follow this [direct link to the quota request form](https://aka.ms/oai/stuquotarequest).

## Create a provisioned deployment

In this section, you create a provisioned deployment using the Foundry portal or the Azure CLI.

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

1. Select **Confirm pricing** to review the hourly rate for the deployment. **Billing starts immediately the deployment is created, even when no requests are being sent**. You stop billing by deleting your deployment. If you're unsure of the costs, select **Cancel** and review [PTU billing and cost management](./concepts/provisioned-throughput-billing.md) before continuing.

1. Confirm and create the deployment.

[!INCLUDE [quickstart-provisioned-2](includes/quickstart-provisioned-2.md)]