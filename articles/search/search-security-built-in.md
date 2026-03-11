---
title: Data, Privacy, and Built-In Protections
titleSuffix: Azure AI Search
description: Learn about Microsoft-managed security, data residency, encryption, and compliance features built into Azure AI Search.
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: conceptual
ms.date: 02/24/2026
ai-usage: ai-assisted
---

# Data, privacy, and built-in protections in Azure AI Search

Azure AI Search includes security protections that Microsoft manages automatically, requiring no action from customers. Understanding what Microsoft handles helps you focus your security efforts on the controls and configurations for which you're responsible. 

This article covers Microsoft's built-in protections, including network architecture, encryption (in transit, in use, and at rest), data residency, privacy guarantees, and compliance certifications. For security best practices that you should configure, see [Secure an Azure AI Search service](search-security-best-practices.md).

## What Microsoft manages automatically

Azure AI Search provides comprehensive built-in security protections across network, data, and service operations. These features are active by default and don't require configuration:

+ **Transport Layer Security (TLS)**: All connections use TLS 1.2 or 1.3 for encryption in transit.

+ **Service-managed encryption**: Data is encrypted at rest using 256-bit Advanced Encryption Standard (AES) encryption.

+ **Internal network security**: Service-to-service calls occur over the secure Microsoft backbone network.

+ **Compliance certifications**: Azure AI Search maintains certifications for global, regional, and industry-specific standards.

+ **Operational security**: Microsoft manages infrastructure security, patching, and service updates.

## Network security architecture

Azure AI Search uses Microsoft's secure network infrastructure to protect traffic to, from, and within your search servic

### Internal traffic protection

Microsoft secures and manages internal requests. You can't configure or control these connections. Internal traffic is isolated from public networks and protected by Microsoft's security infrastructure.

Internal traffic includes:

+ **Service-to-service authentication and authorization**: Calls through Microsoft Entra ID, resource logging sent to Azure Monitor, and [private endpoint connections](service-create-private-endpoint.md) that use Azure Private Link.

+ **Built-in skills processing**: Same-region requests directed to an internally hosted Microsoft Foundry resource used exclusively for [built-in skills processing](cognitive-search-predefined-skills.md) by Azure AI Search.

+ **Semantic ranking**: Requests made to the models that support [semantic ranking](semantic-search-overview.md#availability-and-pricing).

### Transport Layer Security (TLS)

Azure AI Search enforces TLS 1.2 or 1.3 for all connections. TLS 1.3 is the default for newer systems. Earlier TLS versions (1.0 and 1.1) aren't supported.

All endpoints require HTTPS on port 443. Client systems must support TLS 1.2 or later. For implementation guidance, see:

+ [Encryption of data in transit](/azure/security/fundamentals/encryption-overview#encryption-of-data-in-transit)
+ [TLS best practices](/dotnet/framework/network-programming/tls)
+ [TLS support in .NET Framework](/dotnet/framework/network-programming/tls#tls-support-in-net-framework)

### Same-region Azure Storage and Azure AI Search

If Azure Storage and Azure AI Search are in the same region, network traffic is routed through a private IP address and occurs over the Microsoft backbone network. Because private IP addresses are used, you can't configure IP firewalls or a private endpoint for network security on the storage account for these connections.

This same-region optimization ensures high performance and low latency while maintaining security through network isolation. The traffic never leaves the Microsoft network infrastructure.

## Data encryption

Azure AI Search automatically encrypts all customer data at multiple layers.

### Data in transit

All data transmitted to and from Azure AI Search is encrypted using TLS 1.2 or later. This data includes:

+ Client application requests to the search service endpoint
+ Responses from the search service to client applications
+ API requests for index management, query operations, and indexing

Data in transit is protected end-to-end between your client and the search service. For internal service-to-service communication, encryption occurs over the Microsoft backbone network.

### Data in use

By default, Azure AI Search deploys your search service on standard Azure infrastructure. This infrastructure encrypts data at rest and in transit, but it doesn't protect data while it's being actively processed in memory.

For scenarios requiring hardware-based protection of data in use, Azure AI Search offers confidential computing. This compute type has limited regional availability, disables or restricts certain features, and increases the cost of running your search service. For more information, see [(Optional) Enable confidential computing](search-security-best-practices.md#optional-enable-confidential-computing).

### Data at rest

Azure AI Search automatically encrypts all data at rest using 256-bit [AES encryption](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) with Microsoft-managed keys. This applies to indexes, synonym maps, and object definitions (indexers, data sources, and skillsets) on both data disks and temporary disks. For more information, see [Azure encryption at rest](/azure/security/fundamentals/encryption-atrest).

Service-managed encryption:

+ Is built-in and automatic (no configuration required)
+ Is available on all pricing tiers in all regions
+ Uses FIPS 140-2 compliant encryption

You can configure customer-managed keys (CMK) to manage your own encryption keys. CMK adds a second encryption layer on top of service-managed encryption. For more information, see [(Optional) Add customer-managed key encryption](search-security-best-practices.md#optional-add-customer-managed-key-encryption).

## Data residency

When you create a search service, you select a region within an [Azure geography](https://azure.microsoft.com/explore/global-infrastructure/geographies/). Azure AI Search stores and processes your data within that geography, but Microsoft might replicate data to other regions within the same geography for high availability. The exception is Brazil South, where data stays within the region.

Data stays in your geography unless you configure features that write to Azure Storage (enrichment cache, debug sessions, knowledge stores) in a different region.

Object names (indexes, fields, indexers) might also be processed outside your selected region. These names appear in telemetry logs that Microsoft uses for service support. Avoid placing sensitive data in object names.

For more information, see:

+ [Data residency in Azure](https://azure.microsoft.com/explore/global-infrastructure/data-residency/)
+ [Products available by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/)

## Privacy and data handling

Microsoft is committed to protecting your data and respecting your privacy when you use Azure AI Search.

### No customer data used for model training

Microsoft doesn't use customer data from Azure AI Search to train or improve any models, including built-in skills, semantic ranking, or other AI features. Your documents, queries, and other data are used solely to deliver and operate the configured search service.

### Data logging

Azure AI Search doesn't log user identities, so you can't refer to logs for information about a specific user. However, the service does log create, read, update, and delete (CRUD) operations, which you might be able to correlate with other logs to determine who performed specific actions.

Resource logs capture:

+ Administrative operations (service creation, configuration changes)
+ Query operations (with query text but no user identity)
+ Indexing operations (document additions, updates, deletions)

Resource logs don't capture:

+ Individual user identities
+ Personal information about users
+ Document contents in detail (only metadata about documents being indexed)

For information about setting up logs, see [Monitor Azure AI Search](monitor-azure-cognitive-search.md) and [Monitor query requests](search-monitor-queries.md).

## Compliance and certifications

Azure AI Search undergoes regular third-party audits and maintains certifications against global, regional, government, and industry-specific standards, including [ISO 27001](/azure/compliance/offerings/offering-iso-27001), [ISO 27018](/azure/compliance/offerings/offering-iso-27018), [ISO 27701](/azure/compliance/offerings/offering-iso-27701), [SOC 2](/azure/compliance/offerings/offering-soc-2), [FedRAMP](/azure/compliance/offerings/offering-fedramp), [HIPAA](/azure/compliance/offerings/offering-hipaa-us), and [GDPR](/compliance/regulatory/gdpr).

For complete certification lists, audit reports, and compliance documentation, see:

+ [Azure compliance offerings](/azure/compliance/offerings/)
+ [Microsoft Azure Compliance Offerings white paper](https://servicetrust.microsoft.com/DocumentPage/7adf2d9e-d7b5-4e71-bad8-713e6a183cf3/)
+ [Microsoft Trust Center](https://www.microsoft.com/trust-center/compliance/compliance-overview)

### Shared responsibility model

Azure AI Search operates under the [shared responsibility model](/azure/security/fundamentals/shared-responsibility). Microsoft secures the infrastructure and built-in platform features described in this article. You're responsible for configuring security controls for your specific deployment.

+ **Microsoft manages** physical security, network infrastructure, platform security, default encryption (in transit, in use, and at rest), compliance certifications, and infrastructure updates.

+ **You configure** network access controls, authentication and authorization, outbound connections, document-level permissions, monitoring and alerting, and optional CMK and confidential computing.

## Related content

+ [Secure an Azure AI Search service](search-security-best-practices.md)
+ [Azure security fundamentals](/azure/security/fundamentals/)
+ [Shared responsibility in the cloud](/azure/security/fundamentals/shared-responsibility)
