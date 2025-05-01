---
title: Azure OpenAI in Azure Government
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI in the Azure Government cloud.
author: challenp
ms.service: azure-ai-openai
ms.topic: how-to
ms.custom: references_regions, azuregovernment
ms.date: 4/7/2025
recommendations: false
---

# Azure OpenAI Service and features in Azure Government

This article highlights the differences when using Azure OpenAI in Azure Government as compared to the commercial cloud offering. Learn more about the Azure OpenAI Service itself in [Azure OpenAI Service documentation](/azure/ai-services/openai/).
<br><br>

## Azure OpenAI models

Learn more about the different capabilities of each model in [Azure OpenAI Service models](./concepts/models.md). For customers with [Business Continuity and Disaster Recovery (BCDR) considerations](./how-to/business-continuity-disaster-recovery.md), take careful note of the deployment types, regions, and model availability as not all model/type combinations are available in both regions. 

The following sections show model availability by region and deployment type. Models and versions not listed are not currently available in Azure Government. For general limits, quotas, and other details refer to [Azure OpenAI Service quotas and limits](/azure/ai-services/openai/quotas-limits/). 

<br>

## Standard deployment model availability
|   **Region**  | **o3-mini USGov DataZone** | **gpt-4o**, **2024-05-13** | **gpt-4o-mini**, **2024-07-18** | **gpt-4**, **1106-Preview** | **gpt-35-turbo**, **0125** | **gpt-35-turbo**, **1106** | **text-embedding-3-large**, **1** | **text-embedding-ada-002**, **2** |
|:--------------|:--------------------------:|:--------------------------:|:-------------------------------:|:---------------------------:|:--------------------------:|:--------------------------:|:---------------------------------:|:---------------------------------:|
| usgovarizona  | ✅ | ✅ | ✅ | ✅ | ✅ | -  | ✅ | ✅ |
| usgovvirginia | ✅ | ✅ | -  | ✅ | ✅ | ✅ |  - | ✅ |

* USGov DataZone provides access to the model from both usgovarizona and usgovvirginia.
* Data stored at rest remains in the designated Azure region of the resource.
* Data may be processed for inferencing in either of the two Azure Government regions. 

SKU name in code: DataZoneStandard

Data zone standard deployments are available in the same Azure OpenAI resource as all other Azure OpenAI deployment types but allow you to leverage Azure global infrastructure to dynamically route traffic to the data center within the Microsoft defined data zone with the best availability for each request. Data zone standard provides higher default quotas than our Azure geography-based deployment types.

To request quota increases for these models, submit a request at [https://aka.ms/AOAIGovQuota](https://aka.ms/AOAIGovQuota). Note the following maximum quota limits allowed via that form:

| **gpt-4o** | **gpt-4o-mini** | **gpt-4** | **gpt-35-turbo** | **text-embedding-3-large** | **text-embedding-ada-002**|
|:----------:|:---------------:|:---------:|:----------------:|:--------------------------:|:-------------------------:|
|    300k    |      600k       |    200k   |      500k        |            700k            |           700k            |

<br>

## Provisioned deployment model availability
|   **Region**  | **gpt-4o**, **2024-05-13** | **gpt-4o-mini**, **2024-07-18** | **gpt-4**, **1106-Preview** | **gpt-35-turbo**, **0125** | **gpt-35-turbo**, **1106** |
|:--------------|:--------------------------:|:-------------------------------:|:---------------------------:|:--------------------------:|:--------------------------:|
| usgovarizona  | ✅ | - | - | ✅ | - |
| usgovvirginia | ✅ | - | - | ✅ | - |

[NOTE]
> Provisioned Throughput Units (PTUs) are different from standard quota in Azure OpenAI and are not available by default in Azure Government. To learn more about this offering contact your Microsoft Account Team.

<br>

## Azure OpenAI features

The following feature differences exist when comparing Azure OpenAI in Azure Government vs commercial cloud.

|Feature|Description|
|--------|--------|
| Structured Outputs | Not currently supported. |
| Reservation Based Purchases | Not currently supported. |
| Batch Deployments | Not currently supported. |
| Connect your data | Virtual network and private links are supported. Deployment to a web app or a copilot in Copilot Studio is not supported. |
| Abuse Monitoring | Not all features of Abuse Monitoring are enabled for Azure OpenAI in Azure Government. You are responsible for implementing reasonable technical and operational measures to detect and mitigate any use of the service in violation of the Product Terms. [Automated Content Classification and Filtering](./concepts/content-filter.md) remains enabled by default for Azure Government. If modified content filters are required, apply at [https://aka.ms/AOAIGovModifyContentFilter](https://aka.ms/AOAIGovModifyContentFilter)|
| Data Storage | In Azure Government, there are no Azure OpenAI features currently enabled that store customer data at rest. However, Customer Managed Keys (CMK) can still be enabled in Azure Government to support use of the same policies in Azure Government as in Public cloud. Note also that if Azure OpenAI features that store customer data are enabled in Azure Government in the future, any existing CMK deployment would be applied to that data at that time. Learn more at [Azure OpenAI Data Privacy](/../legal/cognitive-services/openai/data-privacy).|
| Compliance | View the current status of Azure OpenAI compliance in Azure Government at [Azure Government Services Audit Scope](/azure/azure-government/compliance/azure-services-in-fedramp-auditscope?branch=pr-en-us-76518#azure-government-services-by-audit-scope)|
| Service Endpoints | openai.azure.us |
| Key Portals | <ul><li>AI Foundry Portal - ai.azure.us</li><li>Azure OpenAI Studio - aoai.azure.us</li><li>Azure portal - portal.azure.us</li></ul> |

<br>

## Provisioned deployments in Azure Government

The following guide walks you through setting up a provisioned deployment with your Azure OpenAI Service resource in Azure Government. 

### Prerequisites

- An Azure Government subscription
- An Azure OpenAI resource
- An approved quota for a provisioned deployment and purchased a commitment

### Managing provisioned throughput commitments

For Azure OpenAI in Azure Government, provisioned throughput deployments require prepurchased commitments created and managed from the **Manage Commitments** view in Azure OpenAI Studio. You can navigate to this view by selecting **Manage Commitments** from the Quota pane.

From the Manage Commitments view, you can do several things:
* Purchase new commitments or edit existing commitments.
* Monitor all commitments in your subscription.
* Identify and take action on commitments that might cause unexpected billing.

| Setting | Notes |
|---------|-------|
| **Select a resource** | Choose the resource where you create the provisioned deployment. Once you have purchased the commitment, you are unable to use the quota on another resource until the current commitment expires. |
| **Select a commitment type** | Select Provisioned. (Provisioned is equivalent to Provisioned Managed) |
| **Current uncommitted provisioned quota** | The number of PTUs currently available for you to commit to this resource. | 
| **Amount to commit (PTU)** | Choose the number of PTUs you're committing to. **This number can be increased during the commitment term, but can't be decreased**. Enter values in increments of 50 for the commitment type Provisioned. |
| **Commitment tier for current period** | The commitment period is set to one month. |
| **Renewal settings** | Autorenew at current PTUs <br> Autorenew at lower PTUs <br> Do not autorenew |

> [!IMPORTANT]
> A new commitment is billed up-front for the entire term. If the renewal settings are set to auto-renew, then you will be billed again on each renewal date based on the renewal settings.

> [!IMPORTANT]
> When you add PTUs to a commitment, they will be billed immediately, at a pro-rated amount from the current date to the end of the existing commitment term. Adding PTUs does not reset the commitment term.

### Changing renewal settings

Commitment renewal settings can be changed at any time before the expiration date of your commitment.

> [!IMPORTANT]
> If you allow a commitment to expire or decrease in size such that the deployments under the resource require more PTUs than you have in your resource commitment, you will receive hourly overage charges for any excess PTUs.  For example, a resource that has deployments that total 500 PTUs and a commitment for 300 PTUs will generate hourly overage charges for 200 PTUs.

### Common commitment management scenarios

**Discontinue use of provisioned throughput**

To end use of provisioned throughput and prevent hourly overage charges after commitment expiration, two steps must be taken:

1. Set the renewal policy on all commitments to *Don't autorenew*.
2. Delete the provisioned deployments using the quota.

**Move a commitment/deployment to a new resource in the same subscription/region**

It isn't possible in Azure OpenAI Studio to directly *move* a deployment or a commitment to a new resource. Instead, a new deployment needs to be created on the target resource and traffic moved to it. This process requires a new commitment purchase on the new resource. Because commitments are charged up-front for a 30-day period, it's necessary to time this move with the expiration of the original commitment to minimize overlap with the new commitment and “double-billing” during the overlap.

There are two approaches that can be taken to implement this transition.

**Option 1: No-Overlap Switchover**

This option requires some downtime, but requires no extra quota and generates no extra costs.

| Steps | Notes |
|-------|-------|
|Set the renewal policy on the existing commitment to expire| This action prevents the commitment from renewing and generating further charges |
|Before expiration of the existing commitment, delete its deployment | Downtime starts at this point and will last until the new deployment is created and traffic is moved. You can minimize the duration by timing the deletion to happen as close to the expiration date/time as possible.|
|After expiration of the existing commitment, create the commitment on the new resource|Minimize downtime by executing this step and the next step as soon after expiration as possible.|
|Create the deployment on the new resource and move traffic to it||

**Option 2: Overlapped Switchover**

This option has no downtime by having both existing and new deployments live at the same time. This method also requires having quota available to create the new deployment and  generates extra costs during the overlapped deployments.

| Steps | Notes |
|-------|-------|
|Set the renewal policy on the existing commitment to expire| Doing so prevents the commitment from renewing and generating further charges.|
|Before expiration of the existing commitment:<br>1. Create the commitment on the new resource.<br>2. Create the new deployment.<br>3. Switch traffic<br>4.	Delete existing deployment| Ensure you leave enough time for all steps before the existing commitment expires, otherwise overage charges will be generated (see next section) for options. |
