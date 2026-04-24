---
title: Best Practices for Security
description: Learn how to configure security features in Azure AI Search to protect endpoints, content, and operations. This article provides best practices for network security, authentication, and data protection.
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: how-to
ms.date: 03/30/2026
ai-usage: ai-assisted
ms.custom: horz-security
---

# Secure an Azure AI Search service

This article provides security best practices to help protect your Azure AI Search service. You're responsible for implementing these customer-configurable security controls. For information about Microsoft's built-in protections, such as network architecture, encryption, and compliance certifications, see [Data, privacy, and built-in protections in Azure AI Search](search-security-built-in.md).

As a solutions architect, you should configure security controls across three domains:

- **Network security**: Control inbound and outbound traffic to your search service.
- **Authentication and authorization**: Define how, who, and what can access your search service and data.
- **Data protection**: Implement encryption, access controls, and monitoring.

[!INCLUDE [Security horizontal Zero Trust statement](~/reusable-content/ce-skilling/azure/includes/security/zero-trust-security-horizontal.md)]

## Understand network traffic patterns

Before you configure network security, understand the three network traffic patterns in Azure AI Search:

+ **Inbound traffic**: Requests from clients to your search service, such as queries, indexing, and management operations. This traffic is configurable by customers.

+ **Outbound traffic**: Requests from your search service to external resources, such as indexers that connect to data sources, vectorizers, and custom skills. This traffic is configurable by customers.

+ **Internal traffic**: Service-to-service calls over the Microsoft backbone network. This traffic is managed by Microsoft and isn't configurable by customers. For more information, see [Internal traffic protection](search-security-built-in.md#internal-traffic-protection).

## Configure network security

Use one of the following approaches to restrict inbound access to your search service. These approaches are listed from least secure to most secure:

+ [Create IP firewall rules](#create-ip-firewall-rules)
+ [Create a private endpoint](#create-a-private-endpoint)
+ [Join a network security perimeter](#join-a-network-security-perimeter)

### Create IP firewall rules

Create inbound firewall rules to admit requests only from specific IP addresses or address ranges. All client connections must be made through an allowed IP address. Otherwise, the connection is denied.

:::image type="content" source="media/search-security-overview/inbound-firewall-ip-restrictions.png" alt-text="Sample architecture diagram for IP restricted access.":::

**When to use**: Basic protection scenarios where you need to restrict access to known IP addresses.

**How to get started**: See [Configure network access and firewall rules for Azure AI Search](service-configure-firewall.md).

### Create a private endpoint

Create a private endpoint for Azure AI Search to allow clients on a virtual network to securely access data in a search index over a Private Link. The private endpoint uses an IP address from your virtual network address space.

Network traffic between the client and the search service traverses over the virtual network and a private link on the Microsoft backbone network, eliminating exposure from the public internet.

:::image type="content" source="media/search-security-overview/inbound-private-link-azure-cog-search.png" alt-text="Sample architecture diagram for private endpoint access.":::

**When to use**: High-security scenarios requiring complete network isolation from the public internet.

**How to get started**: See [Create a private endpoint for Azure AI Search](service-create-private-endpoint.md).

### Join a network security perimeter

Create a network security perimeter around your platform-as-a-service (PaaS) resources deployed outside of a virtual network to establish a logical network boundary. This establishes a perimeter that controls public network access through explicit access rules.

Inbound client connections and service-to-service connections occur within the boundary, simplifying defenses against unauthorized access. In Azure AI Search, it's common for solutions to use multiple Azure resources.

**When to use**: Solutions using multiple Azure PaaS resources that need coordinated network boundary protection.

**How to get started**:

+ Start by joining Azure AI Search to a network security perimeter. See [Add a search service to a network security perimeter](search-security-network-security-perimeter.md).

+ Add related services, such as [Azure OpenAI](/azure/ai-foundry/openai/how-to/network-security-perimeter), [Azure Storage](/azure/storage/common/storage-network-security-perimeter), and [Azure Monitor](/azure/azure-monitor/fundamentals/network-security-perimeter), to the same perimeter.

## Configure authentication and authorization

Azure AI Search supports two authentication approaches. You can use one approach and disable the other, or you can use both with appropriate controls.

### (Recommended) Enable role-based access control

Use Microsoft Entra authentication to establish the *caller*, rather than the *request*, as the authenticated identity. Azure role assignments determine authorization, providing centralized identity management, conditional access policies, and comprehensive audit trails.

The workflow for role-based access control is:

1. **Enable role-based access control**: Configure your search service to accept Microsoft Entra ID authentication instead of (or in addition to) API keys. See [Enable or disable role-based access control in Azure AI Search](search-security-enable-roles.md).

1. **Assign roles to users and groups**: Grant least-privilege access using built-in roles (Search Service Contributor, Search Index Data Contributor, and Search Index Data Reader) to control who can manage and query indexes. See [Connect to Azure AI Search using roles](search-security-rbac.md).

1. **Connect your application using identities**: Authenticate without API keys by using `DefaultAzureCredential`, which supports managed identities, developer credentials, and other token-based flows. See [Connect your app to Azure AI Search using identities](search-security-rbac-client-code.md).

### Configure API key authentication

With key-based authentication, each request must include an admin or query API key to prove it originates from a trusted source. This approach is suitable for development environments, backward compatibility with existing applications, or scenarios where Microsoft Entra ID isn't available.

The workflow for key-based authentication is:

1. **Provide an API key in each request**: Admin keys grant full access to all operations. Query keys grant read-only access to the documents collection of an index. See [Connect to Azure AI Search using keys](search-security-api-keys.md).

1. **Rotate admin keys on a schedule**: Reduce the risk of key compromise by regularly regenerating admin keys. Search services support two admin keys for zero-downtime rotation. See [Regenerate admin keys](search-security-api-keys.md#regenerate-admin-keys).

### Authorize control plane operations

Control plane operations (service creation, configuration, and deletion) are authorized through Azure Resource Manager role-based access control, the same model used across all Azure services. API keys don't apply to control plane operations. Three built-in Azure roles govern access:

| Role | Permissions |
| ---- | ----------- |
| Owner | Full control, including access management. |
| Contributor | Full control except for access management. |
| Reader | View-only access. |

The workflow for authorizing control plane operations is:

1. **Assign administrative roles**: Use built-in Azure roles (Owner, Contributor, and Reader) to grant least-privilege access and control who can create, configure, or delete search services. See [Assign roles for service administration](search-security-rbac.md#assign-roles-for-service-administration).

1. **Apply resource locks**: Prevent accidental deletion of production search services by applying `CanNotDelete` or `ReadOnly` locks. See [Lock your Azure resources to protect your infrastructure](/azure/azure-resource-manager/management/lock-resources).

### Authorize data plane operations

Data plane operations target content hosted on a search service, such as index creation, document loading, and queries. Authorization is available through role-based access control, API keys, or both. For configuration steps, see the previous sections on [role-based access control](#recommended-enable-role-based-access-control) and [API key authentication](#configure-api-key-authentication).

### Grant access to individual indexes

Restrict user access to individual indexes by creating custom role definitions. This approach is essential for multi-tenant scenarios where each tenant's data must be isolated at the index level. See [Grant access to a single index](search-security-rbac.md#grant-access-to-a-single-index).

For solutions requiring security boundaries at the index level, see [Design patterns for multitenant SaaS applications and Azure AI Search](search-modeling-multitenant-saas-applications.md).

> [!NOTE]
> API keys provide service-level access only. Anyone with an [admin key](search-security-api-keys.md) can read, modify, or delete any index in the search service. For index-level isolation, use role-based access control or implement isolation in your application's middle tier.

## Configure outbound connections

Outbound requests originate from a search service to other applications, typically made by indexers, custom skills, and vectorizers. Configure these connections to use secure authentication and network access.

### (Recommended) Use a managed identity

Create a managed identity for your search service to authenticate to other Azure resources without storing credentials in your code. A managed identity eliminates the need to store and rotate connection strings with credentials.

The workflow for using a managed identity is:

1. **Configure a managed identity for the search service**: Choose between a system-assigned or user-assigned managed identity. See [Configure a search service to connect using a managed identity](search-how-to-managed-identities.md).

1. **Connect to external resources using the managed identity**: Supported connections include [Azure Storage](search-howto-managed-identities-storage.md), [Azure Cosmos DB](search-howto-managed-identities-cosmos-db.md), [Azure SQL Database](search-howto-managed-identities-sql.md), [SQL Managed Instance](search-how-to-index-sql-managed-instance-with-managed-identity.md), and [Azure Functions](search-howto-managed-identities-azure-functions.md).

### Secure access to external data

Configure secure connections based on how external resources are protected:

+ **Create firewall exceptions for the search service**: Allow indexer traffic through data source firewalls by adding the search service's outbound IP addresses to allowlists. See [Configure IP firewall rules to allow indexer connections from Azure AI Search](search-indexer-howto-access-ip-restricted.md).

+ **Create shared private links**: Connect indexers to data sources protected by Azure Private Link without exposing traffic to the public internet. See [Make outbound connections through a shared private link](search-indexer-howto-access-private.md).

+ **Use trusted service exception for same-region storage**: Enable indexer access to secured Azure Storage accounts in the same region without firewall configuration. See [Make indexer connections to Azure Storage as a trusted service](search-indexer-howto-access-trusted-service-exception.md).

+ **Configure resource instance rules**: Grant specific search services access to Azure Storage accounts protected by network rules. See [Grant access from Azure resource instances](/azure/storage/common/storage-network-security?tabs=azure-portal#grant-access-from-azure-resource-instances).

+ **Connect to SQL Managed Instance private endpoints**: Access SQL Managed Instance databases through private endpoints while maintaining network isolation. See [Create a shared private link for a SQL managed instance from Azure AI Search](search-indexer-how-to-access-private-sql.md).

> [!TIP]
> If Azure Storage and Azure AI Search are in the same region, network traffic is automatically routed through a private IP address over the Microsoft backbone network, eliminating the need for firewall configuration. For more information, see [Same-region Azure Storage and Azure AI Search](search-security-built-in.md#same-region-azure-storage-and-azure-ai-search).

### Secure connections for external AI processing

Outbound requests for AI enrichment and vectorization require special consideration:

| Operation | Configuration |
| --------- | ------------- |
| Indexers connecting to data sources | [Secure access to external data](search-indexer-securing-resources.md). |
| Custom skills calling external code | Secure connections to [Azure Functions, web apps, or other hosts](cognitive-search-custom-skill-interface.md#set-the-endpoint-and-timeout-interval). |
| Vectorization during indexing | Connect to [Azure OpenAI](vector-search-integrated-vectorization.md#secure-connections-to-vectorizers-and-models) or custom embedding models. |
| Azure Key Vault | Connect to Azure Key Vault for [customer-managed encryption keys](search-security-manage-encryption-keys.md). |

For basic retrieval-augmented generation (RAG) patterns where your client application calls a chat completion model, the connection uses the client or user identity, not the search service identity. For agentic retrieval using knowledge bases, the outbound request is made by the search service managed identity.

## Implement document-level access control

Document-level access control, also known as row-level security, restricts which documents a user can retrieve based on their identity. Permission metadata is captured during indexing and enforced at query time, which is essential for agentic AI systems, RAG applications, and enterprise search solutions that require authorization checks at the document level. For a comprehensive overview of all supported approaches, see [Document-level access control](search-document-level-access-overview.md).

### Use POSIX-like ACL and RBAC scopes (preview)

For Azure Data Lake Storage (ADLS) Gen2 content, configure indexers or knowledge sources to preserve POSIX-like ACL permissions and RBAC scopes during ingestion. At query time, results are filtered based on the caller's Microsoft Entra token. For more information, see [Index ADLS Gen2 permission metadata](search-indexer-access-control-lists-and-role-based-access.md).

### Use SharePoint in Microsoft 365 ACLs (preview)

Configure the SharePoint in Microsoft 365 indexer to extract document permissions directly from SharePoint ACLs during ingestion. At query time, results are filtered based on the caller's Microsoft Entra token. During this preview, ACLs are captured only during initial indexing, so you must reindex affected documents if source permissions change to avoid stale access. For more information, see [Index SharePoint permission metadata](search-indexer-sharepoint-access-control-lists.md).

### Use sensitivity labels (preview)

Configure an indexer to automatically detect Microsoft Purview sensitivity labels during indexing and apply label-based access controls when queries are executed. This capability aligns Azure AI Search authorization with your enterprise's Microsoft Information Protection model. For more information, see [Index Microsoft Purview sensitivity labels](search-indexer-sensitivity-labels.md).

### Use security filters

For scenarios where native ACL integration isn't viable, implement security filters to trim results based on user or group identities. Store identity information in a string field in your index, and then pass the caller's identity as a filter string at query time to exclude documents that don't match. This approach works with custom access models or non-Microsoft security frameworks. For more information, see [Security filters for trimming results](search-security-trimming-for-azure-search.md).

## Configure data encryption

Azure AI Search encrypts all data automatically using Microsoft-managed keys. For information about built-in encryption, see [Data encryption](search-security-built-in.md#data-encryption).

For enhanced data protection, you can implement the following encryption controls.

### (Optional) Add customer-managed key encryption

Add an extra encryption layer for indexes and synonym maps by managing your own encryption keys
in Azure Key Vault. Customer-managed keys (CMK) are for organizations with compliance requirements mandating
customer control over encryption keys or key revocation capabilities. See [Configure customer-managed keys for data encryption in Azure AI Search](search-security-manage-encryption-keys.md).

You can also configure the following options:

+ **Configure cross-tenant CMK**: Support multi-tenant scenarios where keys are stored in a different Microsoft Entra tenant than the search service. See [Configure customer-managed keys across different tenants](search-security-managed-encryption-cross-tenant.md).

+ **Find encrypted objects**: Identify which indexes and synonym maps use CMK encryption. See [Find encrypted objects and information](search-security-get-encryption-keys.md).

> [!IMPORTANT]
> + CMK encryption increases index size and can degrade query performance by 30-60%. Only enable for indexes that require it.
> + CMK on temporary disks requires services created after May 13, 2021. Earlier services support CMK on data disks only.

### Index encrypted blob content

Configure an indexer to process content from Azure Blob Storage that's encrypted at rest, which is separate
from CMK encryption of the search index. See [Tutorial: Index and enrich encrypted blobs](search-how-to-index-azure-blob-encrypted.md).

### (Optional) Enable confidential computing

[Confidential computing](/azure/confidential-computing/overview) protects data in use from unauthorized access, including from Microsoft, through hardware attestation and encryption. This compute type is only configurable during service creation. See [Choose a compute type](search-create-service-portal.md#choose-a-compute-type).

We only recommend confidential computing for organizations whose compliance or regulatory requirements necessitate data-in-use protection. For daily usage, the default compute type suffices.

| Compute type | Description | Limitations | Cost | Availability |
| ------------ | ----------- | ----------- | ---- | ------------ |
| Default | Standard VMs with built-in encryption for data at rest and in transit. No hardware-based isolation for data in use. | No limitations. | No change to the base cost of free or billable tiers. | Available in all regions. |
| Confidential | Confidential VMs (DCasv5 or DCesv5) in hardware-based trusted execution environment. Isolates computations and memory from the host operating system and other VMs. | Disables or restricts [agentic retrieval](agentic-retrieval-overview.md), [semantic ranker](semantic-search-overview.md), [query rewrite](semantic-how-to-query-rewrite.md), [skillset execution](cognitive-search-concept-intro.md), and indexers that run in the [multitenant environment](search-howto-run-reset-indexers.md#indexer-execution-environment) <sup>1</sup>. | Adds 10% surcharge to the base cost of billable tiers. For more information, see the [pricing page](https://azure.microsoft.com/pricing/details/search/). | Available in some regions. For more information, see the [list of supported regions](search-region-support.md). |

<sup>1</sup> When you enable this compute type, indexers can only run in the private execution environment, meaning they run from the search clusters hosted on confidential computing.

## Enable monitoring and logging

Track operations, detect anomalies, and support security audits by enabling logging and monitoring for your search service. For information about what Azure AI Search logs by default, see [Data logging](search-security-built-in.md#data-logging).

+ **Enable diagnostic logging**: Capture operations for security audits and anomaly detection by sending logs to Azure Monitor, Event Hubs, or Azure Storage. See [Configure diagnostic logging for Azure AI Search](search-monitor-enable-logging.md).

+ **Monitor queries**: Track search query activity, latency, and throttling to detect unusual patterns. See [Monitor query requests in Azure AI Search](search-monitor-queries.md).

+ **Monitor indexer operations**: Track indexing activity, errors, and data refresh operations. See [Monitor indexer status and results in Azure AI Search](search-monitor-indexers.md).

+ **Configure alerts for anomalous activity**: Create alert rules for query volume spikes, failed authentication attempts, and unusual access patterns. See [Create or edit a metric alert rule](/azure/azure-monitor/alerts/alerts-create-new-alert-rule).

+ **Visualize logs using Power BI**: Build dashboards to analyze search service activity and identify security trends. See [Visualize Azure AI Search logs and metrics with Power BI](search-monitor-logs-powerbi.md).

## Maintain compliance

For information about Azure AI Search compliance certifications and the shared responsibility model, see [Compliance and certifications](search-security-built-in.md#compliance-and-certifications).

### Use Azure Policy

+ **Review built-in policy definitions**: Use Azure Policy to audit and enforce security configurations such as diagnostic logging and private endpoint usage. See [Azure Policy Regulatory Compliance controls for Azure AI Search](security-controls-policy.md).

+ **Assign the resource logging policy**: Automatically identify search services missing diagnostic logging and remediate the configuration. See [Azure Policy overview](/azure/governance/policy/overview).

+ **Create custom policies**: Define organization-specific security requirements and enforce them across all search services. See [Tutorial: Create a custom policy definition](/azure/governance/policy/tutorials/create-custom-policy-definition).

### Apply resource tags

Apply resource tags to categorize search services by environment, data sensitivity, cost center, or compliance requirements for improved governance. See [Use tags to organize your Azure resources and management hierarchy](/azure/azure-resource-manager/management/tag-resources).

## Security checklist

Use this checklist to ensure you've configured appropriate security controls:

**Network security**:

- [ ] Configured IP firewall rules, private endpoint, or network security perimeter
- [ ] Restricted inbound access to known clients or networks
- [ ] Configured secure outbound connections using managed identities

**Authentication and authorization**:

- [ ] Enabled role-based access control
- [ ] Assigned appropriate roles to users and applications
- [ ] Implemented admin key rotation schedule (if using keys)
- [ ] Configured index-level permissions (if required)

**Data protection**:

- [ ] Configured document-level access control (if required):
  - [ ] POSIX-like ACLs for ADLS Gen2 content
  - [ ] SharePoint in Microsoft 365 ACLs
  - [ ] Microsoft Purview sensitivity labels
  - [ ] Security filters for custom scenarios
- [ ] Implemented CMK encryption (if required)
- [ ] Evaluated confidential computing requirements (if applicable)

**Monitoring and compliance**:

- [ ] Enabled diagnostic logging
- [ ] Set up monitoring and alerts to identify anomalous activity
- [ ] Applied resource tags for governance
- [ ] Assigned Azure Policy for resource logging
- [ ] Reviewed compliance certifications against requirements

## Related content

- [Data, privacy, and built-in protections in Azure AI Search](search-security-built-in.md)
- [Azure security fundamentals](/azure/security/fundamentals/)
- [Shared responsibility in the cloud](/azure/security/fundamentals/shared-responsibility)
