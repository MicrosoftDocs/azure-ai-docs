---
title: Understanding deployment types in Azure AI model inference
titleSuffix: Azure AI Foundry
description: Learn how to use deployment types in Azure AI model deployments
author: santiagxf
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 1/21/2025
ms.author: fasantia
ms.custom: ignite-2024, github-universe-2024
---

# Deployment types in Azure AI model inference

Azure AI model inference makes models available using the *model deployment* concept in Azure AI Services resources. *Model deployments* are also Azure resources and, when created, they give access to a given model under certain configurations. Such configuration includes the infrastructure require to process the requests. 

Azure AI model inference provides customers with choices on the hosting structure that fits their business and usage patterns. Those options are translated to different deployments types (or SKUs) that are available at model deployment time in the Azure AI Services resource.

:::image type="content" source="../media/add-model-deployments/models-deploy-deployment-type.png" alt-text="Screenshot showing how to customize the deployment type for a given model deployment." lightbox="../media/add-model-deployments/models-deploy-deployment-type.png":::

Different model providers offer different deployments SKUs that you can select from. When selecting a deployment type, consider your **data residency needs** and **call volume/capacity** requirements.

## Deployment types for Azure OpenAI models

The service offers two main types of deployments: **standard** and **provisioned**. For a given deployment type, customers can align their workloads with their data processing requirements by choosing an Azure geography (`Standard` or `Provisioned-Managed`), Microsoft specified data zone (`DataZone-Standard` or `DataZone Provisioned-Managed`), or Global (`Global-Standard` or `Global Provisioned-Managed`) processing options.

To learn more about deployment options for Azure OpenAI models see [Azure OpenAI documentation](../../../ai-services/openai/how-to/deployment-types.md).

## Deployment types for Models-as-a-Service models

Models with pay-as-you-go billing (collectively called Models-as-a-Service), makes models available in Azure AI model inference under **standard** deployments with a Global processing option (`Global-Standard`). 

> [!TIP]
> Models-as-a-Service offers regional deployment options under [Serverless API endpoints](../../../ai-studio/how-to/deploy-models-serverless.md) in Azure AI Foundry. However, those deployments can't be accessed using the Azure AI model inference endpoint in Azure AI Services and they need to be created within a project.

### Global-Standard

Global deployments leverage Azure's global infrastructure to dynamically route traffic to the data center with best availability for each request. Global standard provides the highest default quota and eliminates the need to load balance across multiple resources. Data stored at rest remains in the designated Azure geography, while data may be processed for inferencing in any Azure location. Learn more about [data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/).

## Control deployment options

Administrators can control which model deployment types are available to their users by using Azure Policies. Learn more about [How to control AI model deployment with custom policies](../../../ai-studio/how-to/custom-policy-model-deployment.md).

## Related content

- [Quotas & limits](../quotas-limits.md)
- [Data privacy, and security for Models-as-a-Service models](../../../ai-studio/how-to/concept-data-privacy.md)
