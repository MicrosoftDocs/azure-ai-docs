---
title: Secure your Azure AI Search deployment
description: Learn how to secure Azure AI Search, with best practices for protecting your deployment.
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: conceptual
ms.custom: horz-security
ms.date: 03/19/2024
ai-usage: ai-assisted
---

# Secure your Azure AI Search deployment

Azure AI Search provides a managed search service that enables rich search experiences across content stored in Azure data sources. When deploying this service, it's important to follow security best practices to protect data, configurations, and infrastructure.

This article provides guidance on how to best secure your Azure AI Search deployment.

## Network security

Azure AI Search is a PaaS service with a public endpoint by default. Properly securing network access is essential to protect your search service from unauthorized access and potential data breaches.

- **Configure IP firewall rules**: Restrict access to your search service by allowing only specific IP addresses or IP address ranges. This prevents unauthorized access from unrecognized networks. See [Configure IP firewall in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/service-configure-firewall).

- **Implement private endpoints**: Establish a private connection between your virtual network and Azure AI Search using Private Link to eliminate exposure to the public internet. This enables secure access to your search service from within your virtual network. See [Configure a private endpoint for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/service-create-private-endpoint).

- **Use virtual networks with service endpoints**: Secure your search service by limiting access to specific virtual networks and subnets, providing network isolation and enhanced security. See [Configure a service endpoint for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/service-configure-network-security).

- **Deploy into Azure China or Azure Government clouds**: For scenarios requiring higher levels of isolation and compliance, deploy Azure AI Search in sovereign clouds. This provides additional network isolation and compliance with regional requirements. See [Azure AI Search in sovereign clouds](https://learn.microsoft.com/en-us/azure/search/search-security-overview#azure-cognitive-search-in-sovereign-clouds).

## Identity and access management

Controlling who can access and manage your Azure AI Search service is critical for maintaining security and compliance. Proper authentication and authorization mechanisms help prevent unauthorized access to your search data.

- **Implement Azure role-based access control (RBAC)**: Assign specific roles to users, groups, and applications to grant appropriate levels of access to your search service. This ensures the principle of least privilege is applied. See [Azure role-based access control for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-security-rbac).

- **Use managed identities for data source connections**: Connect to data sources securely without storing credentials by using managed identities. This eliminates the need to manage and rotate connection credentials manually. See [Configure a connection to a data source using a managed identity](https://learn.microsoft.com/en-us/azure/search/search-howto-managed-identities-data-sources).

- **Implement API key management**: Rotate admin and query API keys regularly and use separate query keys with appropriate permissions for different client applications. This limits the impact if a key is compromised. See [Create and manage API keys for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-security-api-keys).

- **Configure Azure Active Directory authentication**: Enable AAD authentication for search operations to leverage centralized identity management, conditional access policies, and multi-factor authentication. See [Configure Azure Active Directory authentication for client applications](https://learn.microsoft.com/en-us/azure/search/search-security-overview#azure-active-directory).

## Data protection

Azure AI Search indexes may contain sensitive information that requires protection both at rest and in transit. Implementing proper data protection measures is essential to maintain confidentiality and integrity of your search content.

- **Enable customer-managed keys**: Use your own encryption keys stored in Azure Key Vault to encrypt your search service data. This gives you control over key rotation and revocation. See [Configure customer-managed keys for encryption in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-security-manage-encryption-keys).

- **Use secure connections (TLS/SSL)**: Enforce HTTPS connections to your search service to ensure data in transit is encrypted. This prevents eavesdropping and man-in-the-middle attacks. See [Enforce TLS requirements for connections to Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-security-overview#encryption-in-transit).

- **Implement row-level security**: Filter search results based on user identity or group membership to ensure users only see data they're authorized to access. This provides granular access control at the document level. See [Security filters for trimming results in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search).

- **Use field-level security**: Exclude sensitive fields from search results by controlling which fields are retrieved in queries. This prevents unauthorized access to sensitive data. See [Secure content through strategic index design](https://learn.microsoft.com/en-us/azure/search/search-security-overview#secure-content-through-strategic-index-design).

## Logging and monitoring

Comprehensive logging and monitoring are crucial for detecting and responding to security incidents, as well as maintaining an audit trail of actions taken against your search service.

- **Enable diagnostic logging**: Configure Azure Monitor Logs to collect and analyze operational logs from your search service for audit and troubleshooting purposes. This provides visibility into service operations and potential security issues. See [Collect and analyze log data for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-monitor-logs).

- **Set up alerts for suspicious activities**: Create Azure Monitor alerts based on metrics and logs to detect unusual patterns or potential security breaches. This enables prompt response to security incidents. See [Set up alerts in Azure Monitor for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-monitor-usage).

- **Monitor service health and performance**: Track resource utilization, query latency, and throttling metrics to ensure service availability and optimize performance. This helps identify potential security-related performance issues. See [Monitor query metrics in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-monitor-queries).

- **Enable audit logging for management operations**: Track administrative actions performed on your search service through Azure Activity Log. This provides accountability and helps in forensic analysis. See [View activity logs to audit operations in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-monitor-logs#view-activity-logs).

## Compliance and governance

Adhering to compliance requirements and implementing proper governance controls helps ensure that your Azure AI Search deployment meets organizational and regulatory standards.

- **Apply Azure Policy definitions**: Enforce organizational standards and assess compliance for your Azure AI Search resources using Azure Policy. This helps maintain consistent security configurations across your environment. See [Azure Policy built-in definitions for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-security-overview#compliance).

- **Implement resource locks**: Prevent accidental deletion or modification of your search service by applying resource locks. This safeguards against unintended changes that could impact security. See [Apply resource locks to prevent accidental deletion](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources).  
  See also: [General guidance – Apply Azure resource locks](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources).

- **Use tags for security classification**: Apply metadata tags to categorize search services based on data sensitivity and compliance requirements. This facilitates proper governance and security controls. See [Use tags to organize your Azure resources](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources).  
  See also: [General guidance – Organize Azure resources using tags](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources).

- **Review compliance documentation**: Regularly review Azure AI Search compliance certifications and documentation to ensure alignment with your regulatory requirements. See [Azure compliance documentation](https://learn.microsoft.com/en-us/azure/compliance/).

## Backup and recovery

Implementing robust backup and recovery strategies ensures business continuity and data protection in case of service disruptions or data corruption.

- **Create index replicas**: Maintain multiple replicas of your indexes to ensure high availability and protect against data loss. This provides redundancy and improves resilience. See [High availability for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-performance-optimization#high-availability).

- **Implement index snapshots**: Periodically save the state of your indexes to restore them in case of corruption or accidental deletion. This provides a recovery point for your search data. See [Import and export index snapshots](https://learn.microsoft.com/en-us/azure/search/search-howto-index-backup-restore).

- **Design for disaster recovery**: Deploy search services across multiple regions and implement a strategy for rebuilding indexes when needed. This ensures business continuity during regional outages. See [Disaster recovery for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-performance-optimization#disaster-recovery).

- **Document indexer definitions**: Maintain documentation of indexer configurations to facilitate quick rebuilding of indexes from data sources if necessary. This expedites recovery operations. See [Indexers in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-indexer-overview).

## Service-specific security

Azure AI Search has unique security considerations related to search operations, data indexing, and AI enrichment that require specific attention.

- **Implement synonym maps with caution**: Carefully review and secure synonym maps to prevent potential security issues with query expansion. Improperly configured synonyms could lead to information disclosure. See [Create synonym maps in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-synonyms).

- **Secure AI enrichment pipelines**: When using AI enrichment with Azure AI Services, implement proper authentication and network security for the cognitive services resources. This protects sensitive data during the enrichment process. See [Security considerations for AI enrichment](https://learn.microsoft.com/en-us/azure/search/cognitive-search-concept-security).

- **Validate input data for indexing**: Implement proper validation for data being indexed to prevent injection attacks or indexing of malicious content. This ensures the integrity of your search index. See [Validate input data for indexing](https://learn.microsoft.com/en-us/azure/search/search-security-overview#secure-content-through-strategic-index-design).

- **Control search suggestions**: Configure suggestion modes and filtering to prevent exposure of sensitive information in typeahead experiences. This reduces the risk of information leakage through autocomplete suggestions. See [Add suggestions to client apps](https://learn.microsoft.com/en-us/azure/search/index-add-suggesters).

## Learn more

- [Microsoft Cloud Security Benchmark – Search](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/azure-cognitive-search-security-baseline)
- [Well-Architected Framework – Search considerations](https://learn.microsoft.com/en-us/azure/architecture/framework/services/search/azure-cognitive-search/azure-cognitive-search-security)
- [Security overview for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-security-overview)  
  See also: [Azure Security Documentation](https://learn.microsoft.com/en-us/azure/security/).
