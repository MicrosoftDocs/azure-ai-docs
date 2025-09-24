---
title: Secure your Azure AI Translator data and deployment
description: Learn how to secure Azure AI Translator, with best practices for protecting your data and deployment.
author: laujan
ms.author: lajanuar
ms.service: translator
ms.topic: conceptual
ms.custom: horz-security
ms.date: 09/24/2025
ai-usage: ai-assisted
---

# Secure your Azure AI Translator data and deployment

Azure AI Translator is a cloud-based neural machine translation solution designed for fast, accurate translation of text and documents across multiple languages. To ensure the safety of your information and systems when implementing this service, it's essential to adhere to established security protocols.

This guide outlines the recommended steps and considerations for securing your Azure AI Translator deployment. It covers strategies for safeguarding your data and sensitive information, maintaining secure configurations, and protecting the integrity of your cloud infrastructure.


## Network security

Azure AI Translator processes sensitive content from your applications, so implementing proper network isolation is critical to prevent unauthorized access and protect your translations.

- **Configure private endpoints**: Eliminate public internet exposure by routing traffic through your virtual network with Azure Private Link, ensuring secure communication between your applications and the Translator service. See [Use private endpoints with Azure AI services](/azure/ai-services/cognitive-services-virtual-networks#use-private-endpoints).

- **Implement virtual network service endpoints**: Secure your Translator resources by restricting network access to traffic from your Azure virtual network, while maintaining optimal routing through the Microsoft backbone network. See [Enable Azure AI Custom Translator through Azure Virtual Network](/azure/ai-services/translator/custom-translator/how-to/enable-vnet-service-endpoint).

- **Configure firewall rules**: Restrict access to your Translator resource by specifying allowed IP addresses or address ranges, reducing the risk of unauthorized access from unknown networks. See [Use Azure AI Translator behind firewalls](/azure/ai-services/translator/how-to/use-firewalls#configure-firewall).

- **Use region-specific endpoints**: Improve security and compliance by using geographical endpoints that keep your traffic within specific regions, helping meet data residency requirements. See [Use Azure AI Translator behind firewalls](/azure/ai-services/translator/how-to/use-firewalls).

## Identity and access management

Properly managing identities and access controls is essential for securing your Azure AI Translator deployments against unauthorized usage and potential credential theft.

- **Secure API keys and credentials**: Store your Translator service API keys and credentials in Azure Key Vault to prevent exposure in application code or configuration files. See [Use Azure AI Translator APIs](/azure/ai-services/translator/text-translation/how-to/use-rest-api).

- **Implement role-based access control (RBAC)**: Limit access to your Translator resources by assigning the minimum necessary permissions to users and service principals following the principle of least privilege. See [Azure security features for AI services](/azure/ai-services/security-features).

- **Create and Use managed identities**: Authenticate to Translator services using managed identities instead of storing credentials in your code or configuration files, eliminating the need to manage service principals and API keys. See [Create and use managed identities](ai-services/translator/document-translation/how-to-guides/create-use-managed-identities).

- **Rotate API keys regularly**: Establish a process for regularly rotating your Translator service API keys to mitigate the risk of compromised credentials being used to access your services. See [Keys and Endpoint](/azure/ai-services/translator/create-translator-resource#authentication-keys-and-endpoint-url).

## Data protection

Azure AI Translator processes sensitive text and document content, making data protection measures crucial for maintaining confidentiality and compliance.

- **Enable data encryption at rest**: Ensure your data is automatically encrypted with FIPS 140-2 compliant 256-bit AES encryption when stored by the service. See [Azure AI Translator encryption of data at rest](/azure/ai-services/translator/custom-translator/concepts/encrypt-data-at-rest).

- **Implement Customer-managed keys (CMK)**: For additional control over encryption keys, configure customer-managed keys using Azure Key Vault for Translator resources when using a pricing tier that supports this feature. See [Azure AI Translator encryption of data at rest](/azure/ai-services/translator/custom-translator/concepts/encrypt-data-at-rest).

- **Understand the No-Trace policy**: Be aware that Translator doesn't persist customer data submitted for translation - text translation processes data at rest without storage, and document translation only temporarily stores data during processing. See [Data, privacy, and security for Azure AI Translator](/azure/ai-foundry/responsible-ai/translator/data-privacy-security).

- **Follow data residency requirements**: Configure your deployment to comply with regional data residency requirements by using the appropriate geographical endpoints for your Translator service. See [Use Azure AI Translator behind firewalls](/azure/ai-services/translator/how-to/use-firewalls).

## Logging and monitoring

Implementing comprehensive logging and monitoring is essential for detecting potential security threats and troubleshooting issues with your Azure AI Translator deployment.

- **Enable diagnostic logging**: Configure Azure Monitor to collect and analyze logs from your Translator service to identify potential security issues, track usage patterns, and troubleshoot problems. See [Azure Monitor for Azure AI services](/azure/ai-services/monitor-cognitive-services).

- **Set up alerts for unusual activity**: Create Azure Monitor alerts to notify you of abnormal usage patterns, potential security breaches, or service disruptions affecting your Translator resources. See [Create, view, and manage metric alerts using Azure Monitor](/azure/azure-monitor/alerts/alerts-metric).

- **Configure audit logs**: Enable and review audit logs to track access and changes to your Translator resources, providing visibility into who is accessing your service and what operations they're performing. See [Azure resource logs](/azure/azure-monitor/essentials/resource-logs).

- **Implement request rate monitoring**: Monitor API request rates to detect potential denial of service attacks or unauthorized usage, ensuring your service remains available for legitimate use. See [Service and request limits for Azure AI Translator](/azure/ai-services/translator/service-limits).

## Compliance and governance

Establishing proper governance and ensuring compliance with relevant standards is crucial for the secure operation of Azure AI Translator services.

- **Review Azure Policy for AI services**: Implement Azure Policy to enforce organization-wide security standards for your AI services, including network isolation requirements. See [Azure Policy Regulatory Compliance controls for Azure AI services](/azure/ai-services/security-controls-policy#microsoft-cloud-security-benchmark).

- **Conduct regular security assessments**: Regularly evaluate the security posture of your Translator deployments against industry standards and company policies to identify and remediate potential vulnerabilities. See [Microsoft cloud security benchmark](/security/benchmark/azure/introduction).

- **Maintain regulatory compliance**: Configure your Translator service in accordance with applicable regulations for your industry and region, particularly regarding data privacy and protection. See [Azure AI Translator Transparency Note](/azure/ai-foundry/responsible-ai/translator/transparency-note).

- **Implement human oversight**: For sensitive translation scenarios, establish a human review process to validate translation quality and ensure content meets organizational standards before broad distribution. See [Azure AI Translator Transparency Note](/azure/ai-foundry/responsible-ai/translator/transparency-note#evaluating-and-integrating-azure-ai-translator-for-your-use).

## Service-specific security

Azure AI Translator has unique security considerations that should be addressed to ensure the confidentiality and integrity of your translation workflows.

- **Secure custom translation models**: Protect proprietary terminology and domain-specific language by implementing proper access controls for custom translation models and training data. See [Azure AI Custom Translator for beginners](/azure/ai-services/translator/custom-translator/beginners-guide).

- **Implement secure workflows for document translation**: For document translation, use secure storage containers with proper access controls and encryption to protect source documents and translation outputs. See [What is Azure AI Translator?](/azure/ai-services/translator/overview#azure-ai-translator-features-and-development-options).

- **Apply content filtering as needed**: For public-facing translation services, consider implementing additional content filtering mechanisms to prevent translation of harmful or inappropriate content. See [Prevent translation with the Translator service](/azure/ai-services/translator/prevent-translation).

- **Use containerized deployments for sensitive environments**: Consider using Translator containers for scenarios requiring high security or offline translation capabilities in disconnected environments. See [Azure AI Translator features and development options](/azure/ai-services/translator/overview#azure-ai-translator-features-and-development-options).

## Learn more

- [Microsoft Cloud Security Benchmark – Azure AI services](/security/benchmark/azure/baselines/azure-openai-security-baseline)
- [Well-Architected Framework – AI workloads](/azure/well-architected/ai/design-principles)
- [Security documentation for Azure AI services](/azure/ai-services/security-features)
- [Azure AI Translator documentation](/azure/ai-services/translator/)