---
title: Best Practices for Security
titleSuffix: Azure AI Search
description: Learn how to configure security features in Azure AI Search to protect endpoints, content, and operations. Actionable best practices for network security, authentication, and data protection.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
  - horz-security
ms.topic: how-to
ms.date: 02/24/2026
ai-usage: ai-assisted
---

# Secure your Azure AI Search service

This article provides actionable security best practices that you could add to protect your Azure AI Search service. These are customer-configurable security controls that you're responsible for implementing. For information about built-in security protections that Microsoft provides and manages automatically (network architecture, encryption, compliance certifications, etc.), see [Data, privacy, and built-in protections in Azure AI Search](search-security-built-in.md).

As a solution architect, you should configure security controls across three key domains:

+ **Network security**: Control inbound and outbound traffic to your search service
+ **Authentication and authorization**: Determine how, who and what can access your search service and data
+ **Data protection**: Implement encryption, access controls, and monitoring

This article is structured as an actionable checklist. Each section uses directive, action-oriented guidance to help you implement security best practices. Links are provided to detailed documentation for step-by-step configuration instructions.

## Understand network traffic patterns

Before configuring network security, understand the three network traffic patterns in Azure AI Search:

+ **Inbound traffic**: Client requests to your search service (queries, indexing, management operations). Customer configurable.
+ **Outbound traffic**: Search service requests to external resources (indexers connecting to data sources, vectorizers, custom skills). Customer configurable.
+ **Internal traffic**: Service-to-service calls over the Microsoft backbone network. Managed by Microsoft, not customer-configurable.

For detailed information about how Microsoft secures internal traffic, see [Data, privacy, and built-in protections in Azure AI Search](search-security-built-in.md).

## Configure network security

**Restrict inbound access** to your search service using one or more of these approaches, listed from basic to most secure:

### Use IP firewall rules

**Create inbound firewall rules** that admit requests only from specific IP addresses or ranges. All client connections must be made through an allowed IP address, or the connection is denied.
**When to use**: Basic protection scenarios where you need to restrict access to known IP addresses.

:::image type="content" source="media/search-security-overview/inbound-firewall-ip-restrictions.png" alt-text="sample architecture diagram for ip restricted access":::

+ **Configure IP firewall rules**: Restrict access to your search service by allowing only specific IP addresses or ranges, preventing unauthorized access from unknown sources. See [Configure an IP firewall for Azure AI Search](service-configure-firewall.md).

+ **Use Management REST API for programmatic configuration**: Automate IP firewall deployment and management using the IpRule parameter (API version 2020-03-13 or later). See [Services - Create or Update](/rest/api/searchmanagement/services/create-or-update).



### Create a private endpoint

**Establish a private endpoint** for Azure AI Search to allow clients on a virtual network to securely access data in a search index over a Private Link. The private endpoint uses an IP address from your virtual network address space. 
**When to use**: High-security scenarios requiring complete network isolation from the public internet.

:::image type="content" source="media/search-security-overview/inbound-private-link-azure-cog-search.png" alt-text="sample architecture diagram for private endpoint access":::

Network traffic between the client and the search service traverses over the virtual network and a private link on the Microsoft backbone network, eliminating exposure from the public internet.

+ **Create a private endpoint**: Eliminate public internet exposure by routing all traffic through your virtual network using Azure Private Link. See [Create a private endpoint for Azure AI Search](service-create-private-endpoint.md).

+ **Review Private Link pricing**: Understand additional costs before implementation as private endpoints incur extra charges. See [Azure Private Link pricing](https://azure.microsoft.com/pricing/details/private-link/).



### Join a network security perimeter

**Create a network security perimeter** as a logical network boundary around your PaaS resources deployed outside of a virtual network. This establishes a perimeter for controlling public network access through explicit access rules.
**When to use**: Solutions using multiple Azure PaaS resources that need coordinated network boundary protection.

Inbound client connections and service-to-service connections occur within the boundary, simplifying defenses against unauthorized access. Common in Azure AI Search solutions to use multiple Azure resources:

+ **Join Azure AI Search to a network security perimeter**: Create a unified security boundary for Azure AI Search alongside other PaaS resources to prevent data exfiltration and unauthorized access. See [Join a network security perimeter](search-security-network-security-perimeter.md).

+ **Add related services to the same perimeter**: Include Azure OpenAI, Azure Storage, and Azure Monitor in your perimeter for comprehensive protection. See [Network security perimeter for Azure OpenAI](/azure/ai-foundry/openai/how-to/network-security-perimeter), [Network security perimeter for Azure Storage](/azure/storage/common/storage-network-security-perimeter), and [Network security perimeter for Azure Monitor](/azure/azure-monitor/fundamentals/network-security-perimeter).



## Configure authentication and authorization

Azure AI Search supports two authentication approaches. You could choose one and disable the other, or use both with appropriate controls.

### Enable role-based access control (recommended)

**Use Microsoft Entra authentication** to establish the caller (not the request) as the authenticated identity. Azure role assignments determine authorization.

+ **Enable role-based access control**: Replace API keys with Microsoft Entra ID authentication for centralized identity management, conditional access policies, and comprehensive audit trails. See [Enable role-based access in Azure AI Search](search-security-enable-roles.md).

+ **Assign roles to users and groups**: Grant least-privilege access using built-in roles (Search Service Contributor, Search Index Data Contributor, Search Index Data Reader) to control who can manage and query indexes. See [Assign Azure roles for Azure AI Search](search-security-rbac.md).

+ **Configure managed identity for applications**: Enable applications to authenticate without storing credentials by using system-assigned or user-assigned managed identities. See [Keyless connections to Azure AI Search](keyless-connections.md).

**Benefits**: Better security through centralized identity management, conditional access, and auditing. Recommended for production environments.

### Configure API key authentication

**Use key-based authentication** where API keys prove the request originates from a trusted source. Keys are required on every request.
**When to use**: Development environments, legacy applications, or scenarios where Microsoft Entra ID isn't available.

**Important**: We highly recommend to use RBAC roles for production environments. If using API keys, establish a plan for key rotation at regular intervals.

+ **Use API keys for backward compatibility**: Support legacy applications that can't use Microsoft Entra ID by authenticating requests with admin or query API keys. See [Authenticate using API keys](search-security-api-keys.md).

+ **Rotate admin keys on a schedule**: Reduce the risk of key compromise by regularly regenerating admin keys (search services support two admin keys for zero-downtime rotation). See [Regenerate admin keys](search-security-api-keys.md#regenerate-admin-keys).


### Restrict service administration

Control plane operations (service creation, configuration, deletion) are exclusively authorized through role assignments. Three basic roles apply:

+ **Owner**: Full control including access management
+ **Contributor**: Full control except access management  
+ **Reader**: View-only access

+ **Assign administrative roles**: Use built-in Azure roles (Owner, Contributor, Reader) to control who can create, configure, or delete search services. See [Assign roles for service administration](search-security-rbac.md#assign-roles-for-service-administration).

+ **Apply resource locks**: Prevent accidental deletion of production search services by applying CanNotDelete or ReadOnly locks. See [Lock resources to prevent changes](/azure/azure-resource-manager/management/lock-resources).

### Configure data plane authorization

Choose role-based or key-based authorization for operations on indexes, documents, and other data plane objects:

+ **Configure role-based data plane access**: Grant granular permissions for index operations (read, write, delete) using Microsoft Entra roles instead of service-wide API keys. See [Azure RBAC for data plane operations](search-security-rbac.md).

+ **Use API keys for data plane access**: Authenticate data plane requests with admin keys (full access) or query keys (read-only) when role-based access isn't feasible. See [API keys for data plane operations](search-security-api-keys.md).

### Grant access to individual indexes

+ **Grant index-specific permissions**: Restrict user access to individual indexes using custom role definitions for multi-tenant scenarios. See [Grant access to a single index](search-security-rbac.md#grant-access-to-a-single-index).

**Note**: API keys provide service-level access only. Anyone with an [admin key](search-security-api-keys.md) can read, modify, or delete any index in the service. For index-level isolation, use role-based access control or implement isolation in your application's middle tier.

**Pattern for multitenancy**: For solutions requiring security boundaries at the index level, see [Design patterns for multitenant SaaS applications and Azure AI Search](search-modeling-multitenant-saas-applications.md).

## Configure outbound connections

Secure connections from your search service to external resources. Outbound requests originate from a search service to other applications, typically made by indexers, custom skills, and vectorizers.

### Use managed identities (recommended)

**Create a managed identity** for your search service to authenticate to other Azure resources without storing credentials in your code.

+ **Configure a managed identity for the search service**: Enable secure, credential-free authentication to Azure resources by assigning a system-assigned or user-assigned managed identity. See [Configure managed identities for Azure AI Search](search-how-to-managed-identities.md).

+ **Connect to Azure Storage using managed identity**: Authenticate indexer connections to Blob storage, ADLS Gen2, and Table storage without storing access keys. See [Connect to Azure Storage using a managed identity](search-howto-managed-identities-storage.md).

+ **Connect to Azure Cosmos DB using managed identity**: Secure indexer access to Cosmos DB without embedding connection strings in data source definitions. See [Connect to Azure Cosmos DB using a managed identity](search-howto-managed-identities-cosmos-db.md).

+ **Connect to Azure SQL using managed identity**: Authenticate to Azure SQL Database and SQL Managed Instance using Microsoft Entra authentication instead of SQL authentication. See [Connect to Azure SQL using a managed identity](search-howto-managed-identities-sql.md) and [Connect to SQL Managed Instance using a managed identity](search-how-to-index-sql-managed-instance-with-managed-identity.md).

+ **Connect to Azure Functions using managed identity**: Invoke custom skills hosted in Azure Functions without managing function keys. See [Connect to Azure Functions using a managed identity](search-howto-managed-identities-azure-functions.md).

**Benefits**: Eliminates the need to store and rotate connection strings with credentials.

### Secure access to external data

**Configure secure connections** based on how external resources are protected:

+ **Create firewall exceptions for the search service**: Allow indexer traffic through data source firewalls by adding the search service's outbound IP addresses to allowlists. See [Access Azure resources through IP firewalls](search-indexer-howto-access-ip-restricted.md).

+ **Create shared private links**: Connect indexers to data sources protected by Azure Private Link without exposing traffic to the public internet. See [Access Azure resources through private endpoints](search-indexer-howto-access-private.md).

+ **Use trusted service exception for same-region storage**: Enable indexer access to secured Azure Storage accounts in the same region without firewall configuration. See [Access Azure Storage as a trusted service](search-indexer-howto-access-trusted-service-exception.md).

+ **Configure resource instance rules**: Grant specific search services access to Azure Storage accounts protected by network rules. See [Grant access from Azure resource instances](/azure/storage/common/storage-network-security?tabs=azure-portal#grant-access-from-azure-resource-instances).

+ **Connect to SQL Managed Instance private endpoints**: Access SQL Managed Instance databases through private endpoints while maintaining network isolation. See [Access SQL Managed Instance through a private endpoint](search-indexer-how-to-access-private-sql.md).

**When to use same-region optimization**: If Azure Storage and Azure AI Search are in the same region, network traffic is automatically routed through a private IP address over the Microsoft backbone network, eliminating the need for firewall configuration.

### Secure connections for external AI processing

Outbound requests for AI enrichment and vectorization require special consideration:

| Operation | Configuration |
| --------- | ------------- |
| Indexers connecting to data sources | [Secure access to external data](search-indexer-securing-resources.md) |
| Custom skills calling external code | Secure connections to [Azure Functions, web apps, or other hosts](cognitive-search-custom-skill-interface.md#set-the-endpoint-and-time-out-interval) |
| Vectorization during indexing | Connect to [Azure OpenAI](vector-search-integrated-vectorization.md#secure-connections-to-vectorizers-and-models) or custom embedding models |
| Azure Key Vault | Connect to Azure Key Vault for [customer-managed encryption keys](search-security-manage-encryption-keys.md). |



**Note**: For basic RAG patterns where your client application calls a chat completion model, the connection uses the client or user identity (not the search service identity). For agentic retrieval using knowledge bases, the outbound request is made by the search service managed identity.

## Implement document-level access control

User permissions at the document level, also known as *row-level security*, control which documents users can access through query execution.

### Configure document-level security
Configure  fine-grained permissions at the document level, from data ingestion through query execution, essential for building secure AI agentic systems grounding data, Retrieval-Augmented Generation (RAG) applications, and enterprise search solutions that require authorization checks at the document level. For more information see [Document-level access control](search-document-level-access-overview.md).

### Use sensitivity labels (preview)

Configure to automatically detect Microsoft Purview sensitivity labels at the document level during indexing, applying label‑based access controls when queries are executed. For more information, see [Sensitivity labels](search-indexer-sensitivity-labels.md).


## Configure data encryption

Azure AI Search encrypts all data automatically using Microsoft-managed keys. For information about built-in encryption, see [Data, privacy, and built-in protections in Azure AI Search](search-security-built-in.md).

### (Optional) Add customer-managed key encryption

**Enable customer-managed keys (CMK)** for supplemental encryption of indexed content if your compliance requirements demand double encryption or key revocation capabilities.

**When to use**: Organizations with compliance requirements mandating customer control over encryption keys or key revocation capabilities.

+ **Enable customer-managed keys**: Add an extra encryption layer for indexes and synonym maps by managing your own encryption keys in Azure Key Vault (data is automatically encrypted at rest using Microsoft-managed keys by default). See [Configure customer-managed keys for encryption](search-security-manage-encryption-keys.md).

+ **Configure cross-tenant customer-managed keys**: Support multi-tenant scenarios where keys are stored in a different Microsoft Entra tenant than the search service. See [Configure cross-tenant CMK](search-security-managed-encryption-cross-tenant.md).

+ **Find encrypted objects**: Identify which indexes and synonym maps use customer-managed key encryption. See [Find encrypted objects](search-security-get-encryption-keys.md).



**Important considerations**:

+ **Performance impact**: CMK encryption increases index size and can degrade query performance by 30-60%. Only enable for indexes that require it.
+ **Regional availability**: CMK on temporary disks requires services created after May 13, 2021. Earlier services support CMK on data disks only.
+ **Requirements**: Requires Azure Key Vault and a billable search service tier.


### Index encrypted blob content

+ **Index encrypted blob content**: Configure indexers to process content from Azure Blob Storage that's encrypted at rest (separate from customer-managed key encryption of the search index). See [Index encrypted blobs](search-how-to-index-azure-blob-encrypted.md).

### (Optional) Enable confidential computing

[Confidential computing](/azure/confidential-computing/overview) protects data in use from unauthorized access, including from Microsoft, through hardware attestation and encryption. This compute type is only configurable during service creation. For configuration steps, see [Choose a compute type](search-create-service-portal.md#choose-a-compute-type).

We only recommend confidential computing for organizations whose compliance or regulatory requirements necessitate data-in-use protection. For daily usage, the default compute type suffices.

The following table compares both compute types.

| Compute type | Description | Limitations | Cost | Availability |
| ------------ | ----------- | ----------- | ---- | ------------ |
| Default | Standard VMs with built-in encryption for data at rest and in transit. No hardware-based isolation for data in use. | No limitations. | No change to the base cost of free or billable tiers. | Available in all regions. |
| Confidential | Confidential VMs (DCasv5 or DCesv5) in hardware-based trusted execution environment. Isolates computations and memory from the host operating system and other VMs. | Disables or restricts [agentic retrieval](agentic-retrieval-overview.md), [semantic ranker](semantic-search-overview.md), [query rewrite](semantic-how-to-query-rewrite.md), [skillset execution](cognitive-search-concept-intro.md), and indexers that run in the [multitenant environment](search-howto-run-reset-indexers.md#indexer-execution-environment) <sup>1</sup>. | Adds 10% surcharge to the base cost of billable tiers. For more information, see the [pricing page](https://azure.microsoft.com/pricing/details/search/). | Available in some regions. For more information, see the [list of supported regions](search-region-support.md). |

<sup>1</sup> When you enable this compute type, indexers can only run in the private execution environment, meaning they run from the search clusters hosted on confidential computing.

## Enable monitoring and logging

**Configure diagnostic logging** to track operations, detect anomalies, and support security audits. For details on what Azure AI Search logs by default, see [Data, privacy, and built-in protections](search-security-built-in.md#privacy-and-data-handling).

### Enable resource logging

+ **Enable diagnostic logging**: Capture operations for security audits and anomaly detection by sending logs to Azure Monitor, Event Hubs, or Azure Storage. See [Enable diagnostic logging](search-monitor-enable-logging.md).

+ **Monitor queries**: Track search query activity, latency, and throttling to detect unusual patterns. See [Monitor query requests](search-monitor-queries.md).

+ **Monitor indexer operations**: Track indexing activity, errors, and data refresh operations. See [Monitor indexer-based indexing](search-monitor-indexers.md).

+ **Configure alerts for anomalous activity**: Create alert rules for query volume spikes, failed authentication attempts, and unusual access patterns. See [Create or edit an alert rule](/azure/azure-monitor/alerts/alerts-create-new-alert-rule).

+ **Visualize logs using Power BI**: Build dashboards to analyze search service activity and identify security trends. See [Visualize resource logs](search-monitor-logs-powerbi.md).

## Maintain compliance

For information about Azure AI Search compliance certifications and the shared responsibility model, see [Data, privacy, and built-in protections in Azure AI Search](search-security-built-in.md).

### Use Azure Policy

+ **Review built-in policy definitions**: Use Azure Policy to audit and enforce security configurations such as diagnostic logging and private endpoint usage. See [Azure Policy Regulatory Compliance controls](security-controls-policy.md).

+ **Assign the resource logging policy**: Automatically identify search services missing diagnostic logging and remediate the configuration. See [Azure Policy overview](/azure/governance/policy/overview).

+ **Create custom policies**: Define organization-specific security requirements and enforce them across all search services. See [Create custom policy definitions](/azure/governance/policy/tutorials/create-custom-policy-definition).

### Apply resource tags

+ **Apply resource tags**: Categorize search services by environment, data sensitivity, cost center, or compliance requirements for improved governance. See [Use tags to organize Azure resources](/azure/azure-resource-manager/management/tag-resources).

## Security checklist

Use this checklist to ensure you've configured appropriate security controls:

**Network security:**
- [ ] Configured IP firewall rules, private endpoint, or network security perimeter
- [ ] Restricted inbound access to known clients or networks
- [ ] Configured secure outbound connections using managed identities

**Authentication and authorization:**
- [ ] Enabled role-based access control (or justified key-based authentication)
- [ ] Assigned appropriate roles to users and applications
- [ ] Implemented admin key rotation schedule (if using keys)
- [ ] Configured index-level permissions (if required)

**Data protection:**
- [ ] Enabled diagnostic logging
- [ ] Configured document-level access control (if required)
- [ ] Implemented customer-managed key encryption (if required)
- [ ] Applied resource tags for governance

**Monitoring and compliance:**
- [ ] Set up monitoring and alerts to identify anomalous activity
- [ ] Assigned Azure Policy for resource logging
- [ ] Reviewed compliance certifications against requirements
- [ ] Documented security configuration and responsibilities

## Related content

+ [Data, privacy, and built-in protections in Azure AI Search](search-security-built-in.md) - Microsoft-managed security features
+ [Azure security fundamentals](/azure/security/fundamentals/)
+ [Azure Security](https://azure.microsoft.com/overview/security)
+ [Microsoft Defender for Cloud](/azure/security-center/)
+ [Microsoft Trust Center](https://www.microsoft.com/trust-center)
+ [Shared responsibility in the cloud](/azure/security/fundamentals/shared-responsibility)

**Video resource**: [Azure Cognitive Search: What's new in security](/Shows/AI-Show/Azure-Cognitive-Search-Whats-new-in-security) covers CMK, IP firewalls, and private link features (note: video is several years old and doesn't cover newer features).

