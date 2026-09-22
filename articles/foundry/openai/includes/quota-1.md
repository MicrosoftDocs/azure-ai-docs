---
title: Include file
description: Include file
author: alvinashcraft
ms.reviewer: shiyingfu
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/16/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

Quota provides the flexibility to actively manage the allocation of rate limits across the deployments within your subscription. This article walks through the process of managing your Azure OpenAI quota.

## Prerequisites

> [!IMPORTANT]
> For any task that requires viewing available quota, use the **Cognitive Services Usages Reader** role. This role provides the minimal access necessary to view quota usage across an Azure subscription. For more information, see [Access quota and usage information](../../concepts/rbac-foundry.md#access-quota-and-usage-information).
>
> In the Azure portal, go to **Subscriptions** > **Access control (IAM)** > **Add role assignment**, and search for **Cognitive Services Usages Reader**. Assign the role at the subscription scope. A resource group or resource-level assignment doesn't authorize access to the subscription-scoped Usages API.
>
> The subscription **Reader** role also provides access, but it grants read access beyond what's required to view quota and model deployments.

## Introduction to quota

Azure OpenAI's quota feature enables assignment of rate limits to your deployments, up-to a global limit called your *quota*. Quota is assigned to your subscription on a per-region, per-model, per-deployment-type basis in units of **Tokens-per-Minute (TPM)**. When you onboard a subscription to Azure OpenAI, you receive default quota for most available models. Then, you assign TPM to each deployment as it is created, and the available quota for that model is reduced by that amount. You can continue to create deployments and assign them TPM until you reach your quota limit. Once that happens, you can only create new deployments of that model by reducing the TPM assigned to other deployments of the same model (thus freeing TPM for use), or by requesting and being approved for a model quota increase in the desired region.

> [!NOTE]
> With a quota of 240,000 TPM for GPT-4o in East US, a customer can create a single deployment of 240 K TPM, 2 deployments of 120 K TPM each, or any number of deployments in one or multiple Azure OpenAI resources as long as their TPM adds up to less than 240 K total in that region.

When a deployment is created, the assigned TPM directly maps to the tokens-per-minute rate limit enforced on its inferencing requests. A **Requests-Per-Minute (RPM)** rate limit is also enforced, whose value is set proportionally to the TPM assignment using the following ratio:

> [!IMPORTANT]
> The ratio of Requests Per Minute (RPM) to Tokens Per Minute (TPM) for quota can vary by model. When you deploy a model programmatically or [request a quota increase](https://aka.ms/oai/stuquotarequest) you don't have granular control over TPM and RPM as independent values. Quota is allocated in terms of units of capacity, which have corresponding amounts of RPM & TPM:
>
> | Model                  | Capacity   | Requests Per Minute (RPM)  | Tokens Per Minute (TPM) |
> |------------------------|:----------:|:--------------------------:|:-----------------------:|
> | **Older chat models**  | 1 Unit     | 6 RPM                      | 1,000 TPM               |
> | **o1 & o1-preview**    | 1 Unit     | 1 RPM                      | 6,000 TPM               |
> | **o3**                 | 1 Unit     | 1 RPM                      | 1,000 TPM               |
> | **o4-mini**            | 1 Unit     | 1 RPM                      | 1,000 TPM               |
> | **o3-mini**            | 1 Unit     | 1 RPM                      | 10,000 TPM              |
> | **o1-mini**            | 1 Unit     | 1 RPM                      | 10,000 TPM              |
> | **o3-pro**             | 1 Unit     | 1 RPM                      | 10,000 TPM              |
>
> This is particularly important for programmatic model deployment as changes in RPM/TPM ratio can result in accidental  misallocation of quota.

The flexibility to distribute TPM globally within a subscription and region has allowed Azure OpenAI to loosen other restrictions:

- The maximum resources per region are increased to 30.
- The limit on creating no more than one deployment of the same model in a resource has been removed.

## Request more quota

[!INCLUDE [quota-increase-request](./quota-increase-request.md)]

## Model specific settings

Different model deployments, also called model classes have unique max TPM values that you're now able to control. **This represents the maximum amount of TPM that can be allocated to that type of model deployment in a given region.**

All other model classes have a common max TPM value.

> [!NOTE]
> Quota Tokens-Per-Minute (TPM) allocation isn't related to the maximum input token limit of a model. Model input token limits are defined in the [models table](../../foundry-models/concepts/models-sold-directly-by-azure.md) and aren't impacted by changes made to TPM.
