---
title: Azure OpenAI Provisioned Managed Offering in Azure Government
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI Provisioned Managed Deployments in the Azure Government cloud.
author: challenp
ms.author: chaparker
ms.service: azure-ai-openai
ms.topic: how-to
ms.custom: references_regions, azuregovernment
ms.date: 05/30/2025
recommendations: false
---

# Azure OpenAI Provisioned Managed Offering in Azure Government

Microsoft launched improvements to its Provisioned Throughput offering in Azure Commercial that are now coming to Azure Government and that address customer feedback on usability and operational agility that open new payment options and deployment scenarios. 

This article highlights specific considerations for Azure Government. For general considerations on Provionsed Deployments and Reservations refer to:
* [Azure OpenAI Provisioned Concepts](./provisioned-throughput.md)
* [Getting started using provisioned deployments on the Azure OpenAI in Azure AI Foundry Models](../how-to/provisioned-get-started.md)
* [Azure OpenAI Provisioned Onboarding Guide](../how-to/provisioned-throughput-onboarding.md)
* [Azure Reservations](https://aka.ms/oai/docs/ptum-reservations)

## What's changing?

> [!IMPORTANT]
> The changes in this article describe changes made to provisioned managed offering in Azure Government in May 2025. 

### Usability improvements

|Feature | Benefit|
|---|---|
|Model-independent quota | A single quota limit covering all models/versions reduces quota administration and accelerates experimentation with new models. |
|Default provisioned-managed quota | Get started quickly without having to first request quota. |

### New hourly/reservation commercial model

|Feature | Benefit|
|---|---|
|Non-binding, Hourly option | Hourly payment option without any binding enables short-term deployment scenarios. Ideal for testing new models and assessing benefits of Provisioned Throughput. |
|Term discounts via Azure Reservations | Azure reservations provide substantial discounts over the hourly rate for one month and one year terms, and provide flexible scopes that minimize administration and associated with today’s resource-bound commitments.|
| Flexible choice of payment model for existing provisioned customers | Customers with commitments can stay on the commitment model until the end of life of the currently supported models or can choose to migrate existing commitments to hourly/reservations. We recommend migrating to hourly/ reservations to take advantage of term discounts and to work with the latest models. |

## Usability improvement details

Provisioned quota granularity is changing from model-specific to model-independent. Rather than each model and version within subscription and region having its own quota limit, there's a single quota item per subscription and region that limits the total number of PTUs that can be deployed across all supported models and versions.

## Model-independent quota

By May 5th, 2025, existing customers' current, model-specific quota will be converted to model-independent. This happens automatically. No quota is lost in the transition. Existing quota limits are summed and assigned to a new model-independent quota item.

:::image type="content" source="../media/provisioned/consolidation.png" alt-text="Diagram showing quota consolidation." lightbox="../media/provisioned/consolidation.png":::

The new model-independent quota shows up as a quota item named **Provisioned Managed Throughput Unit**, with model and version no longer included in the name. In the Azure AI Foundry's quota pane, expanding the quota item still shows all of the deployments that contribute to the quota item. 

### Default quota

New and existing subscriptions are assigned a small amount of provisioned quota. This allows customers to start using those regions without having to first request quota.

For existing customers, if the region already contains a quota assignment, the quota limit isn't changed for the region. For example, it isn't automatically increased by the new default amount.

## New hourly reservation payment model

Microsoft has introduced a new "Hourly/reservation" payment model for provisioned deployments. This is in addition to the current **Commitment** payment model, which will continue to be supported until end of life of the currently supported limited model list. You also have the option to purchase Azure Reservations to support additional discounts.

### New Azure Reservations for data zone provisioned deployments

In addition to the updates for the hourly payment model, new [Azure Reservations](https://aka.ms/oai/docs/ptum-reservations) were introduced specifically for data zone provisioned deployment types. With these new Azure Reservations, every provisioned deployment type will have a separate Azure Reservation that can be purchased to support additional discounts. The mapping between each provisioned deployment type and the associated Azure Reservation are as follows:

| Provisioned deployment type | Sku name in code  | Azure Reservation product name |
|---|---|---|
| Data zone provisioned | `DataZoneProvisionedManaged`  | Provisioned Managed Data Zone  |
| Provisioned | `ProvisionedManaged`  | Provisioned Managed Regional |

> [!IMPORTANT]
> Azure Reservations for Azure OpenAI provisioned offers are not interchangeable across deployment types. The Azure Reservation purchased must match the provisioned deployment type. If the Azure Reservation purchased does not match the provisioned deployment type, the provisioned deployment will default to the hourly payment model until a matching Azure Reservation product is purchased. For more information, see the [Azure Reservations for Azure OpenAI provisioned guidance](https://aka.ms/oai/docs/ptum-reservations).

### Commitment payment model

- A regional, monthly commitment is required to use provisioned (longer terms available contractually).

- Commitments are bound to Azure OpenAI resources, which will make moving deployments across resources difficult.

- Commitments can't be canceled or altered during their term, except to add new PTUs.

#### Supported models on commitment payment model:

Only the following list of Azure OpenAI models are supported in Commitments. For onboarding any other models that aren't in the list below, or any newer models on provisioned throughput offering, refer to the [Azure OpenAI provisioned onboarding guide](../how-to/provisioned-throughput-onboarding.md) and [Azure Reservations for Azure OpenAI provisioned deployments](../how-to/provisioned-throughput-onboarding.md#azure-reservations-for-azure-ai-foundry-provisioned-throughput)
    
|Supported models on Commitment plan |Versions|
|-|-|
|gpt-35-turbo| 0125,1106|
|gpt-4| 0613, 1106-Preview, 0125-Preview|
|gpt-4o| 2024-05-13, 2024-08-06|
|gpt-4o-mini| 2024-07-18|

### Hourly reservation payment model

- The payment model is aligned with Azure standards for other products.

- Hourly usage is supported, without commitment.

- One month and one year term discounts can be purchased as regional Azure Reservations.

- Reservations can be flexibly scoped to cover multiple subscriptions, and the scope can be changed mid-term.

- Supports all models, both old and new.

## Payment model framework

With the release of the hourly/reserved payment model, payment options are more flexible and the model around provisioned payments has changed. When the one-month commitments were the only way to purchase provisioned, the model **was**: 

1. Get a PTU quota from your Microsoft account team.
1. "Purchase" quota from a commitment on the resource where you want to deploy.
1. Create deployments on the resource up to the limit of the commitment.

The key difference between this model and the new model is that previously the only way to pay for provisioned was through a one-month term discount. Now, you can deploy and pay for deployments hourly if you choose and make a separate decision on whether to discount them via **either** a one-month commitment (like before) or an Azure reservation. 

With this insight, the new way to think about payment models is: 

1. Create deployments using your existing or default quota.
1. Optionally request additional PTU quota as needed.
1. Optionally purchase or extend a commitment or a reservation to apply a term discount to your deployments. 

Steps 1 and 2 are the same in all cases. The difference is whether a commitment or an Azure reservation is used as the vehicle to provide the discount. In both models: 

* It's possible to deploy more PTUs than you discount. (for example creating a short-term deployment to try a new model is enabled by deploying without purchasing a discount) 
* The discount method (commitment or reservation) applies the discounted price to a fixed number of PTUs and has a scope that defines which deployments are counted against the discount.

    |Discount type  |Available Scopes (within a region)  |
    |---------|---------|
    |Commitment     |  Azure OpenAI resource        |
    |Reservation     | Resource group, single subscription, management group (group of subscriptions), shared (all subscriptions in a billing account)          |

* The discounted price is applied to deployed PTUs up to the number of discounted PTUs in the discount. 
* The number of deployed PTUs exceeding the discounted PTUs (or not covered by any discount) will be charged the hourly rate. 
* The best practice is to create deployments first, and then to apply discounts. This is to guarantee that service. capacity is available to support your deployments prior to creating a term agreement for PTUs you can't use. 

> [!NOTE] 
> When you follow best practices, you might receive hourly charges between the time you create the deployment and increase your discount (commitment or reservation).   
>
> For this reason, we recommend that you're prepared to increase your discount immediately following the deployment. The prerequisites for purchasing an Azure reservations are different than for commitments, and we recommend you validate them prior to deployment if you intend to use them to discount your deployment. For more information, see [Permissions to view and manage Azure reservations](/azure/cost-management-billing/reservations/view-reservations) 

## Mapping deployments to discounting method 

Customers using Azure OpenAI Provisioned offer in Azure Government prior to May 2025 can use either or both payment models simultaneously within a subscription. The payment model used for each deployment is determined based on its Azure OpenAI resource: 

**Resource has an active Commitment** 

* The commitment discounts all deployments on the resource up to the number of PTUs on the commitment. Any excess PTUs is billed hourly unless the excess PTUs aren't in the scope of an active reservation. If the excess PTUs exist in the scope of an active reservation, will be discounted as a group, up to the number of PTUs on the reservation and any excess spill still leftover will be billed hourly. 

**Resource does not have an active commitment** 

* The deployments under the resource are eligible to be discounted by an Azure reservation. For these deployments to be discounted, they must exist within the scope of an active reservation. All deployments within the scope of the reservation (including possibly deployments on other resources in the same or other subscriptions) will be discounted as a group up to the number of PTUs on the reservation. Any excess PTUs will be billed hourly. 

### Changes to the existing payment mode

Customers that have commitments today can continue to use them at least until the supported model's retirement. This includes purchasing new PTUs on new or existing commitments and managing commitment renewals. However, the May update has changed certain aspects of commitments operation.

- Azure OpenAI has stopped supporting enrollment on to new commitments, starting June 2025
- Only a limited set of models can be deployed on a resource with a commitment. 

- If the deployed PTUs under a commitment exceed the committed PTUs, the hourly overage charges are emitted against the same hourly meter as used for the new hourly/reservation payment model. This allows the overage charges to be discounted via an Azure Reservation.
- It's possible to deploy more PTUs than are committed on the resource. This supports the ability to guarantee capacity availability prior to increasing the commitment size to cover it.

## Migrating existing resources off commitments

Existing customers can choose to migrate their existing resources from the Commitment to the Hourly/Reservation payment model to benefit from the ability to deploy the latest models, or to consolidate discounting for diverse deployments under a single reservation.

### Self-service migration

The self-service migration approach allows a customer to organically resources off of their commitments by allowing them to expire. The process to migrate a resource is as follows:

- Set existing commitment to not autorenew and note the expiration date.

- Before the expiration date, a customer should purchase an Azure Reservation covering the total number of committed PTUs per subscription. If an existing reservation already has the subscription in its scope, it can be increased in size to cover the new PTUs.

- When the commitment expires, the deployments under the resource will automatically switch to the Hourly/Reservation mode with the usage discounted by the reservation.

This self-service migration approach will result in an overlap where the reservation and commitment are both active. This is a characteristic of this migration mode and the reservation or commitment time for this overlap won't be credited back to the customer.

An alternative approach to self-service migration is to switch the reservation purchase to occur after the expiration of the commitment. In this approach, the deployments will generate hourly usage for the period between the commitment expiration and the purchase of the reservation. As with the previous model, this is a characteristic of this approach, and this hourly usage won't be credited.

**Self-service migration advantages:**

* Individual resources can be migrated at different times.
* Customers manage the migration without any dependencies on Microsoft.

**Self-service migration disadvantages:**

* There will be a short period of double-billing or hourly charges during the switchover from committed to hourly/reservation billing.

> [!IMPORTANT]
> Self-service approach generates additional charges as the payment mode is switched from Committed to Hourly/Reservation. This is the characteristics of this migration approaches and customers aren't credited for these charges.

## How do I migrate my existing Azure Reservation to the new Azure Reservation products?
Azure Reservations for Azure OpenAI provisioned offers are specific to the provisioned deployment type. If the Azure Reservation purchased does not match the provisioned deployment type, the deployment will default to the hourly payment model. If you choose to migrate to global or data zone provisioned deployments, you might need to purchase a new Azure Reservation for these deployments to support additional discounts. For more information on how to purchase a new Azure Reservation or make changes to an existing Azure Reservation, see the [Azure Reservations for Azure OpenAI Provisioned guidance](https://aka.ms/aoai/reservation-transition).

## Managing Provisioned Throughput Commitments

Provisioned throughput commitments are created and managed by selecting **Management center** in the [Azure AI Foundry portal](https://ai.azure.us/)'s navigation menu > **Quota** > **Manage Commitments**. 

:::image type="content" source="../media/how-to/provisioned-onboarding/notifications.png" alt-text="Screenshot of commitment purchase UI with notifications." lightbox="../media/how-to/provisioned-onboarding/notifications.png":::

From the **Manage Commitments** view, you can do several things:

- Purchase new commitments or edit existing commitments.
- Monitor all commitments in your subscription.
- Identify and take action on commitments that might cause unexpected billing.

The following sections will take you through these tasks.

## Purchase a Provisioned Throughput Commitment

With your commitment plan ready, the next step is to create the commitments. Commitments are created manually via the Azure AI Foundry and require the user creating the commitment to have either the [Contributor or Cognitive Services Contributor role](../how-to/role-based-access-control.md) at the subscription level.

For each new commitment you need to create, follow these steps:

1. Launch the Provisioned Throughput purchase dialog by selecting  **Quota** > **Azure OpenAI Provisioned** > **Manage Commitment plans**.

:::image type="content" source="../media/how-to/provisioned-onboarding/quota.png" alt-text="Screenshot of the purchase dialog." lightbox="../media/how-to/provisioned-onboarding/quota.png":::

2. Select **Purchase commitment**.

3. Select the Azure OpenAI resource and purchase the commitment. You'll see your resources divided into resources with existing commitments, which you can edit and resources that don't currently have a commitment.

| Setting | Notes |
|---------|-------|
| **Select a resource** | Choose the resource where you'll create the provisioned deployment. Once you have purchased the commitment, you'll be unable to use the PTUs on another resource until the current commitment expires. |
| **Select a commitment type** | Select Provisioned. (Provisioned is equivalent to Provisioned Managed) |
| **Current uncommitted provisioned quota** | The number of PTUs currently available for you to commit to this resource. | 
| **Amount to commit (PTU)** | Choose the number of PTUs you're committing to. **This number can be increased during the commitment term, but can't be decreased**. Enter values in increments of 50 for the commitment type Provisioned. |
| **Commitment tier for current period** | The commitment period is set to one month. |
| **Renewal settings** | Autorenew at current PTUs <br> Autorenew at lower PTUs <br> Don't autorenew |

4. Select Purchase. A confirmation dialog will be displayed. After you confirm, your PTUs will be committed, and you can use them to create a provisioned deployment. |

:::image type="content" source="../media/how-to/provisioned-onboarding/commitment-tier.png" alt-text="Screenshot of commitment purchase UI." lightbox="../media/how-to/provisioned-onboarding/commitment-tier.png":::

> [!IMPORTANT]
> A new commitment is billed up-front for the entire term. If the renewal settings are set to auto-renew, then you'll be billed again on each renewal date based on the renewal settings.

### Edit an existing Provisioned Throughput commitment

From the **Manage Commitments** view, you can also edit an existing commitment. There are two types of changes you can make to an existing commitment:

- You can add PTUs to the commitment.
- You can change the renewal settings.

To edit a commitment, select the current to edit, then select Edit commitment.

### Adding Provisioned Throughput Units to existing commitments

Adding PTUs to an existing commitment will allow you to create larger or more numerous deployments within the resource. You can do this at any time during the term of  your commitment.

:::image type="content" source="../media/how-to/provisioned-onboarding/increase-commitment.png" alt-text="Screenshot of commitment purchase UI with an increase in the amount to commit value." lightbox="../media/how-to/provisioned-onboarding/increase-commitment.png":::

> [!IMPORTANT]
> When you add PTUs to a commitment, they'll be billed immediately, at a pro-rated amount from the current date to the end of the existing commitment term. Adding PTUs doesn't reset the commitment term.

### Changing renewal settings

Commitment renewal settings can be changed at any time before the expiration date of your commitment. Reasons you might want to change the renewal settings include ending your use of provisioned throughput by setting the commitment to not autorenew, or to decrease usage of provisioned throughput by lowering the number of PTUs that will be committed in the next period.

> [!IMPORTANT]
> If you allow a commitment to expire or decrease in size such that the deployments under the resource require more PTUs than you have in your resource commitment, you'll receive hourly overage charges for any excess PTUs. For example, a resource that has deployments that total 500 PTUs and a commitment for 300 PTUs will generate hourly overage charges for 200 PTUs.

## Monitor commitments and prevent unexpected billings

The **Manage Commitments** section provides a subscription wide overview of all resources with commitments and PTU usage within a given Azure Subscription. Of particular importance are:

- **PTUs Committed, Deployed and Usage** – These figures provide the sizes of your commitments, and how much is in use by deployments. Maximize your investment by using all of your committed PTUs.
- **Expiration policy and date** - The expiration date and policy tell you when a commitment will expire and what will happen when it does. A commitment set to autorenew will generate a billing event on the renewal date. For commitments that are expiring, be sure you delete deployments from these resources prior to the expiration date to prevent hourly overage billingThe current renewal settings for a commitment. 
- **Notifications** - Alerts regarding important conditions like unused commitments, and configurations that might result in billing overages. Billing overages can be caused by situations such as when a commitment has expired and deployments are still present, but have shifted to hourly billing.

> [!IMPORTANT]
> If you set a commitment to *auto-renew* the renewal date will be the same date next month. If the date doesn't exist, then the renewal date will be end of month.
> Examples -  
> *Scenario 1:* If you purchase a commitment on February 21, and set the commitment on *auto-renew*, the next renewal date for the commitment will be March 21.
>
> *Scenario 2:* If you purchase the commitment on May 31, and set the commitment on *auto-renew*, the next renewal date for the commitment will be June 30 (end of month) as there's no 31st in the month of June.
>
> *Scenario 3:* If you purchase the commitment on January 31, and set the commitment on *auto-renew*, the next renewal date for the commitment will be February 28 (end of month) as there's no 31st or 30th or 29th (in non-leap years) and the renewal date would be February 29 (in a leap-year) in the month of February. 

## Common Commitment Management Scenarios

**Discontinue use of provisioned throughput**

To end use of provisioned throughput, and prevent hourly overage charges after commitment expiration, stop any charges after the current commitments are expired, two steps must be taken:

1. Set the renewal policy on all commitments to *Don't autorenew*.
2. Delete the provisioned deployments using the quota.

> [!IMPORTANT]
> If you allow a commitment to expire with **an intent to discontinue provisioned throughput** and not delete the provisioned deployments, you'll receive hourly overage charges for all PTUs that are still in the deployment. For example, a resource that has deployments that total 500 PTUs and a commitment was selected to *Don't autorenew* will incur hourly charges after the time of expiry of the commitment until the deployment is deleted. There is no option available today that deletes the deployment automatically, it has to be deleted manually when you decide to discontinue use of provisioned throughput.

**Move a commitment/deployment to a new resource in the same subscription/region**

It isn't possible in Azure AI Foundry to directly *move* a deployment or a commitment to a new resource. Instead, a new deployment needs to be created on the target resource and traffic moved to it. There will need to be a commitment purchased established on the new resource to accomplish this. Because commitments are charged up-front for a 30-day period, it's necessary to time this move with the expiration of the original commitment to minimize overlap with the new commitment and “double-billing” during the overlap.

There are two approaches that can be taken to implement this transition.

**Option 1: No-Overlap Switchover**

This option requires some downtime, but requires no extra quota and generates no extra costs.

| Steps | Notes |
|-------|-------|
|Set the renewal policy on the existing commitment to expire| This will prevent the commitment from renewing and generating further charges |
|Before expiration of the existing commitment, delete its deployment | Downtime will start at this point and will last until the new deployment is created and traffic is moved. You'll minimize the duration by timing the deletion to happen as close to the expiration date/time as possible.|
|After expiration of the existing commitment, create the commitment on the new resource|Minimize downtime by executing this and the next step as soon after expiration as possible.|
|Create the deployment on the new resource and move traffic to it||

**Option 2: Overlapped Switchover**

This option has no downtime by having both existing and new deployments live at the same time. This requires having quota available to create the new deployment, and will generate extra costs for the duration of the overlapped deployments.

| Steps | Notes |
|-------|-------|
|Set the renewal policy on the existing commitment to expire| Doing so prevents the commitment from renewing and generating further charges.|
|Before expiration of the existing commitment:<br>1. Create the commitment on the new resource.<br>2. Create the new deployment.<br>3. Switch traffic<br>4.	Delete existing deployment| Ensure you leave enough time for all steps before the existing commitment expires, otherwise overage charges will be generated (see next section) for options. |

If the final step takes longer than expected and will finish after the existing commitment expires, there are three options to minimize overage charges.

- **Take downtime**:  Delete the original deployment then complete the move.
- **Pay overage**: Keep the original deployment and pay hourly until you have moved off traffic and deleted the deployment.
- **Reset the original commitment** to renew one more time. This will give you time to complete the move with a known cost.  

Both paying for an overage and resetting the original commitment will generate charges beyond the original expiration date. Paying overage charges might be cheaper than a new one-month commitment if you only need a day or two to complete the move. Compare the costs of both options to find the lowest-cost approach.

### Move the deployment to a new region and or subscription

The same approaches apply in moving the commitment and deployment within the region, except that having available quota in the new location will be required in all cases.

### View and edit an existing resource

In Azure AI Foundry, select **Management center** > **Quota** > **Provisioned** > **Manage commitments** and select a resource with an existing commitment to view/change it. 
