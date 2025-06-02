---
title: Azure OpenAI in Azure Government
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI in the Azure Government cloud.
author: challenp
ms.service: azure-ai-openai
ms.topic: how-to
ms.custom: references_regions, azuregovernment
ms.date: 5/29/2025
recommendations: false
---

# Azure OpenAI and features in Azure Government

This article highlights the differences when using Azure OpenAI in Azure Government as compared to the commercial cloud offering. Learn more about the Azure OpenAI itself in [Azure OpenAI documentation](/azure/ai-services/openai/).
<br><br>

## Azure OpenAI models

Learn more about the different capabilities of each model in [Azure OpenAI models](./concepts/models.md). For customers with [Business Continuity and Disaster Recovery (BCDR) considerations](./how-to/business-continuity-disaster-recovery.md), take careful note of the deployment types, regions, and model availability as not all model/type combinations are available in both regions. 

The following sections show model availability by region and deployment type. Models and versions not listed are not currently available in Azure Government. For general limits, quotas, and other details refer to [Azure OpenAI quotas and limits](/azure/ai-services/openai/quotas-limits/). 

<br>

## Standard deployment model availability
|   **Region**  | **o3-mini USGov DataZone** | **gpt-4o**, **2024-05-13** | **gpt-4o-mini**, **2024-07-18** | **gpt-4**, **1106-Preview** | **gpt-35-turbo**, **0125** | **text-embedding-3-large**, **1** | **text-embedding-3-small**, **1** | **text-embedding-ada-002**, **2** |
|:--------------|:--------------------------:|:--------------------------:|:-------------------------------:|:---------------------------:|:--------------------------:|:---------------------------------:|:---------------------------------:|:---------------------------------:|
| usgovarizona  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| usgovvirginia | ✅ | ✅ | -  | ✅ | ✅ | - | - | ✅ |

* USGov DataZone provides access to the model from both usgovarizona and usgovvirginia.
* Data stored at rest remains in the designated Azure region of the resource.
* Data may be processed for inferencing in either of the two Azure Government regions. 

Data zone standard deployments are available in the same Azure OpenAI resource as all other Azure OpenAI deployment types but allow you to leverage Azure Government infrastructure to dynamically route traffic to the data center within the USGov data zone with the best availability for each request.

To request quota increases for these models, submit a request at [https://aka.ms/AOAIGovQuota](https://aka.ms/AOAIGovQuota). Note the following maximum quota limits allowed via that form:

| **gpt-4o** | **gpt-4o-mini** | **gpt-4** | **gpt-35-turbo** | **text-embedding-3-large** | **text-embedding-ada-002**|
|:----------:|:---------------:|:---------:|:----------------:|:--------------------------:|:-------------------------:|
|    300k    |      600k       |    200k   |      500k        |            700k            |           700k            |

<br>

## Provisioned deployment model availability
|   **Region**  | **gpt-4o**, **2024-05-13** | **gpt-4o-mini**, **2024-07-18** | **gpt-4**, **1106-Preview** | **gpt-35-turbo**, **0125** |
|:--------------|:--------------------------:|:-------------------------------:|:---------------------------:|:--------------------------:|
| usgovarizona  | ✅ | - | - | ✅ |
| usgovvirginia | ✅ | - | - | ✅ |

<br>

## Azure OpenAI features

The following feature differences exist when comparing Azure OpenAI in Azure Government vs commercial cloud.

|Feature|Description|
|--------|--------|
| Batch Deployments | Not currently supported. |
| Connect your data | Virtual network and private links are supported. Deployment to a web app or a copilot in Copilot Studio is not supported. |
| Abuse Monitoring | Not all features of Abuse Monitoring are enabled for Azure OpenAI in Azure Government. You are responsible for implementing reasonable technical and operational measures to detect and mitigate any use of the service in violation of the Product Terms. [Automated Content Classification and Filtering](./concepts/content-filter.md) remains enabled by default for Azure Government. If modified content filters are required, apply at [https://aka.ms/AOAIGovModifyContentFilter](https://aka.ms/AOAIGovModifyContentFilter)|
| Data Storage | In Azure Government, there are no Azure OpenAI features currently enabled that store customer data at rest. However, Customer Managed Keys (CMK) can still be enabled in Azure Government to support use of the same policies in Azure Government as in Public cloud. Note also that if Azure OpenAI features that store customer data are enabled in Azure Government in the future, any existing CMK deployment would be applied to that data at that time. Learn more at [Azure OpenAI Data Privacy](/../legal/cognitive-services/openai/data-privacy).|
| Compliance | View the current status of Azure OpenAI compliance in Azure Government at [Azure Government Services Audit Scope](/azure/azure-government/compliance/azure-services-in-fedramp-auditscope?branch=pr-en-us-76518#azure-government-services-by-audit-scope)|
| Service Endpoints | openai.azure.us |
| Key Portals | <ul><li>AI Foundry Portal - ai.azure.us</li><li>Azure OpenAI Studio - aoai.azure.us</li><li>Azure portal - portal.azure.us</li></ul> |

