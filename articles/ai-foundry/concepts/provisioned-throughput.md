---
title: Provisioned throughput offering for Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn about the provisioned throughput offering for Azure AI Foundry and which Azure AI Foundry Models support this capability.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 06/02/2025
ms.reviewer: shiyingfu
reviewer: swingfu
ms.author: mopeakande
author: msakande
ms.custom: references_regions
---

# Provisioned throughput for Azure AI Foundry

The Azure AI Foundry provisioned throughput offering enables customers to effectively use their provisioned throughput units (PTU) quota and PTU reservation across a diverse portfolio of [models exclusively hosted and sold by Azure](foundry-models-overview.md#models-sold-directly-by-azure). These models include Azure OpenAI models and newly introduced flagship model families like Azure DeepSeek, Azure Grok, Azure Llama, and more within Azure AI Foundry Models. By utilizing the PTU capability, you gain unparalleled flexibility, advanced deployment options, and the ability to optimize operational efficiency while managing costs strategically with Azure AI Foundry provisioned throughput reservation.

The provisioned throughput offering is a model deployment type that allows you to specify the amount of throughput you require in a model deployment. Azure AI Foundry allocates the necessary model processing capacity and ensures it's ready for you. You can use the PTU quota you requested to deploy models that are hosted and sold directly by Azure. The PTU offering provides:

- A boarder model choice on the latest flagship models

- Flexibility to switch models and deployments with given PTU quota

- Significant discounts and the ability to boost your reservation utilization with a more flexible reservation choice


## Cost management under shared PTU reservation

You can use the PTU capability to seamlessly manage costs for Foundry Models under a shared PTU reservation. However, the required PTU units for deployment and throughput performance are dynamically tailored to the chosen models. To learn more about PTU costs and model latency points, see [Understanding costs associated with provisioned throughput units (PTU)](../../ai-services/openai/how-to/provisioned-throughput-onboarding.md).

Existing PTU reservations are automatically upgraded to empower customers with enhanced efficiency and cost savings as they deploy Foundry Models. For example, suppose you have an existing PTU reservation with 500 PTU purchased. You use 300 units for Azure OpenAI models, and you choose to also use PTU to deploy Azure DeepSeek, Azure Llama, or other models with PTU capability on Foundry Models.

- If you use the remaining 200 PTU for DeepSeek-R1, the 200 PTU share the reservation discount automatically, and your total usage for the reservation is 500 PTU. 

- If you use 300 PTU for DeepSeek-R1, then 200 PTU share the reservation discount automatically while 100 PTU exceed the reservation and are charged with DeepSeek-R1's hourly rate.  

To learn about saving costs with PTU reservations, see [Save costs with Microsoft Azure AI Foundry Provisioned Throughput Reservations](/azure/cost-management-billing/reservations/azure-openai).


## Foundry Models with provisioned throughput capability  

This section lists Foundry Models that support the provisioned throughput capability. You can use your PTU quota and PTU reservation across the models shown in the table. 

The following points are some important takeaways from the table:

- The model version isn't included in this table. Check the version supported for each model when you choose the deployment option in the Azure AI Foundry portal. 

- Regional provisioned throughput deployment option varies by region.  

- New models hosted and sold by Microsoft are onboarded with Global provisioned throughput deployment option first. The Data zone provisioned option comes later.  

- PTUs are managed regionally and by offer type. PTU quota and any reservations must be in the region and shape (Global, Data zone, Regional) you wish to use. 

| Model Family   | Model name      | Global provisioned | Data zone provisioned | Regional provisioned | Spillover feature |
|----------------|-----------------|--------------------|-----------------------|----------------------|-------------------|
| **Azure OpenAI**   | Gpt4.1          | ✅                 | ✅                    | ✅                   | ✅                |
|                | Gpt 4.1 mini    | ✅                 | ✅                    | ✅                   | ✅                |
|                | Gpt 4.1 nano    | ✅                 | ✅                    | ✅                   | ✅                |
|                | Gpt 4o          | ✅                 | ✅                    | ✅                   | ✅                |
|                | Gpt 4o mini     | ✅                 | ✅                    | ✅                   | ✅                |
|                | Gpt 3.5 Turbo   | ✅                 | ✅                    | ✅                   | ✅                |
|                | o1              | ✅                 | ✅                    | ✅                   | ✅                |
|                | O3 mini         | ✅                 | ✅                    | ✅                   | ✅                |
|                | O4 mini         | ✅                 | ✅                    | ✅                   | ✅                |
| **Azure DeepSeek** | DeepSeek-R1     | ✅                 |                       |                      |                   |
|                | DeepSeek-V3-0324| ✅                 |                       |                      |                   |
|                | MAI-DeepSeek-R1 | ✅                 |                       |                      |                   |


## Related content

- [What is provisioned throughput?](../../ai-services/openai/concepts/provisioned-throughput.md)
- [Get started using provisioned deployments on the Azure OpenAI in Azure AI Foundry Models](../../ai-services/openai/how-to/provisioned-get-started.md)
