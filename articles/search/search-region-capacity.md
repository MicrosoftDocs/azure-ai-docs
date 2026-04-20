---
title: How to handle regional capacity constraints in Azure AI Search
description: Learn how to handle a regional capacity constraint that effects your Azure AI Search service.
author: mattwojo
ms.author: mattwoj
ms.reviewer: angiesi
ms.date: 04/20/2026
ms.service: azure-ai-search
ms.topic: concept-article
---

# How to handle regional capacity constraints in Azure AI Search

This article helps you decide what to do when your preferred Azure AI Search region is unavailable due to capacity constraints and provides evaluation criteria for selecting an alternative region.

## Capacity constraint options

When a preferred Azure region is unavailable due to capacity constraints, you have two options:

1. Deploy to an alternative region, or 
2. Retry deployment during off-peak hours.

**Deploying to an alternative region is the recommended path.**
Azure AI Search is available across many Azure regions with consistent APIs, SDKs, SLAs, and compliance certifications. For most workloads, the operational difference between regions within the same geography is negligible. See Criteria for selecting an alternative region below for a full evaluation framework.

**Retrying the service during off-peak hours is also a viable consideration.**
Capacity constraints are sometimes temporary. Retrying deployment during low-traffic periods, such as nights or weekends in UTC, may succeed when peak-hour attempts fail. This option is not guaranteed and is not a substitute for evaluating an alternative region. If retries do not succeed within a reasonable window, proceed with an alternative region.

Retry during off-peak hours when:

- The deployment timeline allows for a delay of several days.
- The constraint is likely the result of a temporary regional surge.
- No infrastructure changes are preferred at this time.

## Criteria for selecting an alternative region

Evaluate the following criteria before selecting an alternative region:

- Network latency
- Compliance
- Availability Zones
- Feature and model availability
- Data residency and sovereignty
- Pricing

### Network latency

If existing services — such as applications or databases — remain in a different region than the new Azure AI Search deployment, each API call between them incurs cross-region round-trip time (RTT). For US-to-US regional pairs, this is typically 26–50ms. For most search workloads, latency under 50ms RTT is not perceptible to end users.
Co-locating the application and the search service in the same region eliminates cross-region RTT entirely.
For current region-to-region latency measurements, see [Azure network round-trip latency statistics](/azure/networking/azure-network-latency).

### Compliance

Azure compliance certifications — including FedRAMP High, HIPAA, CJIS, DoD IL2, IRS 1075, PCI DSS, and StateRAMP — are applied at the geography level, not the individual region level. All commercial Azure regions within the same geography carry an identical compliance posture.

For more information, see:

- [Azure compliance documentation](/azure/compliance)
- [Azure regions list](/azure/reliability/azure-regions-list)

### Availability Zones

Availability Zones (AZ) are physically separate datacenters within an Azure region. When a search service has two or more replicas in an AZ-supported region, Azure automatically distributes them across zones at no additional cost and with no configuration required.

AZ support is relevant when the workload requires a 99.99% query SLA or operates in a regulated industry with documented high-availability requirements. For dev/test environments or workloads protected by a multi-region disaster recovery strategy, AZ support is generally not a blocking requirement.

For the current list of regions that support Availability Zones for Azure AI Search, see [Azure regions with Availability Zones](/azure/reliability/availability-zones-region-support).

## Feature and model availability

Not all Azure AI Search features and AI models are available in every region. Before selecting an alternative region, verify availability for the specific capabilities your workload depends on, including any Azure OpenAI or Azure AI Foundry models used in retrieval-augmented generation (RAG), semantic ranking, or AI enrichment pipelines.

When selecting an alternative region for Azure AI Search, verify model availability in the same region. Co-locating Azure AI Search with Azure OpenAI or Azure AI Foundry in the same region eliminates cross-service latency and simplifies compliance and data residency requirements.

For more information, see:

- [Azure AI Search regional availability](/azure/search/search-region-support)
- [Azure OpenAI Service models by region](/azure/ai-services/openai/concepts/models)
- [Azure AI Foundry regional availability](/azure/ai-foundry/concepts/region-support)
- [Azure OpenAI quotas and limits](azure/ai-services/openai/quotas-limits)

### Data residency and sovereignty

Azure replicates data for resiliency within the same geography. For all commercial Azure regions within the United States geography, data at rest remains within the United States. This satisfies data residency requirements common in federal, state, and regulated industry workloads.

For more information, see:

- [Data, privacy, and built-in protections in Azure AI Search](/azure/search/search-security-overview)
- [Azure data residency](https://azure.microsoft.com/explore/global-infrastructure/data-residency/)

### Pricing

Azure AI Search service pricing is uniform across all regions within the same geography. Selecting an alternative region within the same geography incurs no change in service tier pricing.

For current pricing, see [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search/).

## Move or restore an Azure AI Search service

Indexes, skillsets, indexers, and synonym maps can be backed up and restored to any region using official scripts and tooling. This enables both migration to an alternative region and a return to the original region when capacity becomes available.

For more information, see:
- [Backup and restore scripts (GitHub)](https://github.com/Azure/azure-search-backup-restore)
- [Move your Azure AI Search service to another region](/azure/search/search-howto-move-across-resource-group)

## Related content


- [Azure AI Search regional availability](/azure/search/search-region-support)
- [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search/)
- [Azure network round-trip latency statistics](/azure/networking/azure-network-latency)
- [Azure regions list](/azure/reliability/azure-regions-list)
- [Azure compliance documentation](/azure/compliance/)
- [Azure OpenAI Service models by region](/azure/ai-services/openai/concepts/models)
- [Azure AI Foundry regional availability](/azure/ai-foundry/concepts/region-support)
- [Move your Azure AI Search service to another region](/azure/search/search-howto-move-across-resource-group)
- [Azure regions with Availability Zones](/azure/reliability/availability-zones-region-support)
- [Data, privacy, and built-in protections in Azure AI Search](/azure/search/search-security-overview)






