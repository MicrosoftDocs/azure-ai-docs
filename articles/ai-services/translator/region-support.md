---
title: Region support for Azure Translator in Foundry Tools
titleSuffix: Foundry Tools
description: Compare region support, endpoints, and data processing locations for text translation, document translation, and custom model training and deployment.
author: laujan
manager: mcleans
ms.service: azure-translator-foundry-tools
ms.topic: concept-article
ms.date: 08/21/2026
ms.author: lajanuar
ms.custom: references_regions
ai-usage: ai-assisted
---

# Region support for Azure Translator in Foundry Tools

Azure Translator in Foundry Tools supports different resource locations, endpoints, and data processing locations depending on the translation capability you use. Review these differences before you create a resource or select an endpoint.

Region support involves three related choices:

* **Resource region**: The location you select when you create an Azure Translator resource. You can select **Global** or an available geographic Azure region.
* **Service endpoint**: The global, geography, or resource-specific endpoint that receives your request.
* **Request processing location**: The datacenter or geography where Translator processes the request.

For the current list of Azure regions where you can create a Translator resource, see [Products available by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=cognitive-services).

## Compare translation capabilities

Use the following tabs to review the regional behavior for each capability.

## [Text translation](#tab/text-translation)

### Compare standard and LLM-based translation

Text Translation supports standard neural machine translation (NMT) and LLM-based translation. The model technology determines which resource and regional configuration applies.

The global Text Translation endpoint is:

```http
https://api.cognitive.microsofttranslator.com
```

| Regional consideration | Standard NMT | LLM-based translation |
| --- | --- | --- |
| **Resource type** | Azure Translator or multi-service resource. | Microsoft Foundry resource. |
| **Processing configuration** | Global, geography, or resource-specific endpoint. | Global, data zone, or regional model deployment. |
| **Availability** | Available through Text Translation APIs. | Available through the Text Translation `2026-06-06` API for supported models. |
| **Regional guidance** | Use the endpoint table in this section. | Review the deployment types in this section and confirm availability for the model you select. |

#### Standard NMT endpoints

Neural machine translation (NMT) supports global, geography, and resource-specific endpoints. The endpoint you use determines where Translator processes the request.

| Service endpoint | Request processing location |
| --- | --- |
| **Global:** `api.cognitive.microsofttranslator.com` | Closest available datacenter. If a datacenter failure occurs, the request might be processed outside the originating geography. |
| **Americas:** `api-nam.cognitive.microsofttranslator.com` | East US 2 or West US 2. |
| **Asia Pacific:** `api-apc.cognitive.microsofttranslator.com` | Japan East or Southeast Asia. |
| **Europe, except Switzerland:** `api-eur.cognitive.microsofttranslator.com` | France Central or West Europe. |
| **Switzerland:** Resource-specific custom endpoint | Switzerland North or Switzerland West. |

To process text translation requests in Switzerland, create the Translator resource in Switzerland North or Switzerland West. Then use the resource-specific endpoint:

```http
https://<resource-name>.cognitiveservices.azure.com/translator/text/v3.0
```

When you use a regional Translator resource or a multi-service resource, include the `Ocp-Apim-Subscription-Region` header. For request examples and requirements by resource type, see [Authentication and authorization](text-translation/reference/authentication.md).

#### LLM-based processing in Foundry

For LLM-based text translation, the model deployment type determines where the model processes translation data:

* **Global** deployments can process data in any Azure region where the model is deployed.
* **Data zone** deployments process data within the selected data zone.
* **Regional** deployments process data in the deployment region.

These deployment types also apply to adaptive custom translation. They don't change standard NMT endpoint routing.

For resource requirements, see [Create and configure Azure resources for Translator](how-to/create-translator-resource.md). For processing boundaries and model availability, see [Deployment types for Microsoft Foundry Models](../../foundry/foundry-models/concepts/deployment-types.md).

## [Document translation](#tab/document-translation)

### Plan where documents are processed

Current Document Translation APIs use NMT. The LLM-based deployment considerations in the Text Translation tab don't apply to Document Translation.

Document Translation uses the resource-specific custom endpoint:

```http
https://<resource-name>.cognitiveservices.azure.com
```

The region where you create the Translator resource determines where document content is processed and temporarily stored during translation.

| Resource region | Request processing location |
| --- | --- |
| **Global** | Closest available datacenter. |
| **Americas** | East US 2 or West US 2. |
| **Asia Pacific** | Japan East or Southeast Asia. |
| **Europe, except Switzerland** | France Central or West Europe. |
| **Switzerland** | Switzerland North or Switzerland West. |

If you use managed identity to authorize Document Translation access to Azure Blob Storage, create the Translator resource in a geographic Azure region instead of **Global**. For setup requirements, see [Managed identities for Document Translation](document-translation/how-to-guides/create-use-managed-identities.md).

For asynchronous batch translation, the locations of your source and target storage accounts also affect your data residency architecture. Translator temporarily stores customer data while it processes a document and deletes the data after processing. For more information, see [Data, privacy, and security for Azure Translator](../../foundry/responsible-ai/translator/data-privacy-security.md).

## [Custom model training and deployment](#tab/custom-translator)

### Choose where to train and publish models

Custom Translator supports training and publishing custom NMT models. After you publish a model, use it with Text Translation or Document Translation. The regions in this section apply to custom model training and deployment, not to a separate inference service.

* Use the [**Custom Translator portal**](https://portal.customtranslator.azure.ai/) to train, test, and publish custom NMT models.

* For **LLM-based customization**, [**adaptive custom translation**](foundry/adaptive-custom-translation.md) is available in Microsoft Foundry. It adapts translation output at runtime by using reference translations or an adaptive dataset instead of training and deploying a custom NMT model.

You can publish a trained model to one or more supported regions. Custom Translator isn't currently available in Switzerland.

The following regions and billing region codes are supported when you create a workspace with the Custom Translator API:

| Region | Billing region code |
| --- | --- |
| Australia East | `AUE` |
| Brazil South | `BRS` |
| Canada Central | `CAC` |
| Central India | `INC` |
| Central US | `USC` |
| East Asia | `AE` |
| East US | `USE` |
| East US 2 | `USE2` |
| France Central | `FC` |
| Global | `GBL` |
| Japan East | `JPE` |
| Japan West | `JPW` |
| Korea Central | `KC` |
| North Central US | `USNC` |
| North Europe | `NEU` |
| South Africa North | `SAN` |
| South Central US | `USSC` |
| Southeast Asia | `ASE` |
| Sweden Central | `SWC` |
| UAE North | `UAEN` |
| UK South | `UKS` |
| West Central US | `USWC` |
| West Europe | `WEU` |
| West US | `USW` |
| West US 2 | `USW2` |

Virtual network scenarios require a regional Translator resource. A global resource isn't supported. Network restrictions can also prevent access to the Custom Translator portal. For configuration details, see [Enable Custom Translator through Azure Virtual Network](custom-translator/how-to/enable-vnet-service-endpoint.md).

---

## Data residency considerations

Select a resource and endpoint based on both the capability and the processing boundary your workload requires. A resource location and a request processing location aren't always the same. For example, the global text translation endpoint routes requests to the closest available datacenter and can route a request outside the originating geography during a datacenter failure.

Translator doesn't persist customer data submitted for text translation. Document Translation temporarily stores customer data during processing and deletes it after processing. For service data-handling details, see [Data, privacy, and security for Azure Translator](../../foundry/responsible-ai/translator/data-privacy-security.md).

## Sovereign clouds

Public Azure and sovereign clouds use different regions, endpoints, and feature availability. For Azure Government and Azure operated by 21Vianet, see [Azure Translator in sovereign clouds](reference/sovereign-clouds.md).

## Business continuity

Endpoint behavior differs by capability, so don't assume that each Translator deployment fails over in the same way.

* Monitor regional service health with [Azure Service Health](/azure/service-health/service-health-overview).
* Keep endpoint and region settings configurable instead of embedding them in application code.
* For Custom Translator, publish or copy models to each region required by your continuity plan.
* Test authentication, storage access, quotas, and feature availability in each deployment region.

For current service-level outages and regional disruptions, see [Azure Translator known issues](reference/known-issues.md#service-level-outages-and-notifications).

## Related content

* [Language support](language-support.md)
* [Create and configure Azure resources for Translator](how-to/create-translator-resource.md)
* [Authentication and authorization](text-translation/reference/authentication.md)
* [Service limits](service-limits.md)
* [Azure Translator in sovereign clouds](reference/sovereign-clouds.md)