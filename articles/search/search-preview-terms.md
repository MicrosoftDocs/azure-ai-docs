---
title: Azure AI Search Preview Terms
description: Review the supplemental preview terms that apply to features, capabilities, and properties marked (preview) in the Azure AI Search documentation.
ms.service: azure-ai-search
ms.topic: legal
ms.date: 07/29/2026
ai-usage: ai-assisted
---

# Azure AI Search preview terms

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

Azure AI Search releases some features, capabilities, and properties in preview. In the documentation, this functionality is marked (preview). Preview functionality, whether standalone or part of a generally available feature, isn't covered by a service-level agreement, isn't recommended for production workloads, and might change or be constrained before it becomes generally available.

The terms in this article are based on the most recent data plane preview, the `2026-08-01-preview` [Search Service REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-08-01-preview&preserve-view=true). Depending on the preview version and functionality, some terms might not apply. Nevertheless, you're still responsible for complying with all applicable terms.

## Licensing and preview terms

Preview features and functionality are licensed to you as part of your Azure subscription and are subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## Connections to other services

Some preview features support connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.

It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.

## Access and permissions

Preview features can't modify access permissions that were set outside of Azure AI Search. If you use one of these features with access- or permission-restricted content, a timing lag will occur before Azure AI Search recognizes changes to those access or permission restrictions.

## Cross-origin resource sharing (CORS)

You can use some preview features to enable CORS, which allows browser-based applications to request data directly from the service. Depending on your CORS configuration, external webpages might access or invoke the service and its data by using the user's browser context, which can create security risks. Enabling CORS is at your own risk.

## Responsible AI and application testing

You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

## Related content

+ [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/)
+ [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note)
