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

# Security Guidelines for Azure AI Translator

Azure AI Translator is a powerful cloud-based service that enables real-time translation for applications, websites, and workflows. To ensure the safety and privacy of your data and the integrity of your deployment, it is vital to follow security best practices. 

This document outlines essential guidelines to help you maintain a secure Azure AI Translator environment.

## Identity and access management

Properly managing identities and access controls is essential for securing your Azure AI Translator deployments against unauthorized usage and potential credential theft. Secure access management ensures that only authorized users and devices can access your Translator resource:

* **Access**. Enable Microsoft Entra ID to manage user identities and control access to your Azure AI Translator resources. For more information, *see* [Enable Microsoft Entra ID authentication](/azure/ai-services/translator/how-to/microsoft-entra-id-auth)

* **Authorization**. Assign only necessary permissions based on role-based access control (RBAC). RBAC managed identity enforces the principle of least privilege, meaning users are granted only the minimum necessary access to your resources and data. This security mechanism significantly reduces the risk of unauthorized access to sensitive data or functionality within your API. For more information, *see* [Managed identities: role-based access control](/azure/ai-services/translator/document-translation/how-to-guides/create-use-managed-identities)

* **Authentication**. By restricting access to authenticated entities, you ensure that only authorized parties can view or modify Translator data. For more information, *see* [Authentication and authorization](/azure/ai-services/translator/text-translation/reference/authentication)

* **Azure Key Vault**. Azure Key Vault offers a secure, centralized repository for application secrets like database connection strings, API keys, customer managed keys (CMK), passwords, and cryptographic keys. This eliminates the need to hard-code sensitive information directly into application code or configuration files, reducing the risk of accidental exposure. For more information, *see* [About Azure Key Vault](/azure/key-vault/general/overview). For Custom Translator, *see* [Encryption key management](/azure/ai-services/translator/custom-translator/concepts/encrypt-data-at-rest)

    **Rotate API keys regularly**: Keys in Azure Key Vault can be configured with rotation policies that automatically generate new key versions at specified frequencies.  Regularly rotating your Translator service API keys mitigates the risk of compromised credentials being used to access your services. For more information, *see* [Key autorotation](/azure/key-vault/general/autorotation).

## Network security

Azure AI Translator processes sensitive content from your applications, so implementing proper network isolation is critical to prevent unauthorized access and protect your translations.

- **Configure private endpoints**: Configuring private endpoints for API requests enhances security and network isolation for your Azure Ai Translator resources. For more information, *see* [Use private endpoints with Azure AI services](/azure/ai-services/cognitive-services-virtual-networks#use-private-endpoints).

- **Implement virtual network service endpoints**: Secure your Translator resources by restricting network access to traffic from your Azure virtual network, while maintaining optimal routing through the Microsoft backbone network. For more information, *see* [Enable Azure AI Custom Translator through Azure Virtual Network](/azure/ai-services/translator/custom-translator/how-to/enable-vnet-service-endpoint).

- **Configure firewall rules**: Restrict access to your Translator resource by specifying allowed IP addresses or address ranges, reducing the risk of unauthorized access from unknown networks. For more information, *see* [Use Azure AI Translator behind firewalls](/azure/ai-services/translator/how-to/use-firewalls#configure-firewall).

- **Use region-specific endpoints**: Improve security and compliance by using geographical endpoints that keep your traffic within specific regions, helping meet data residency requirements. For more information, *see* [Use Azure AI Translator behind firewalls](/azure/ai-services/translator/how-to/use-firewalls).





## Data protection

Azure AI Translator processes sensitive text and document content, making data protection measures crucial for maintaining confidentiality and compliance.

- **Enable data encryption at rest**: Ensure your data is automatically encrypted with FIPS 140-2 compliant 256-bit AES encryption when stored by the service. For more information, *see* [Azure AI Translator encryption of data at rest](/azure/ai-services/translator/custom-translator/concepts/encrypt-data-at-rest).

- **Implement Customer-managed keys (CMK)**: For more control over encryption keys, configure customer-managed keys using Azure Key Vault for Translator resources when using a pricing tier that supports this feature. For more information, *see* [Azure AI Translator encryption of data at rest](/azure/ai-services/translator/custom-translator/concepts/encrypt-data-at-rest).

- **Understand the No-Trace policy**: Translator doesn't persist customer data submitted for translation - text translation processes data at rest without storage, and document translation only temporarily stores data during processing. For more information, *see* [Data, privacy, and security for Azure AI Translator](/azure/ai-foundry/responsible-ai/translator/data-privacy-security).

- **Follow data residency requirements**: Configure your deployment to comply with regional data residency requirements by using the appropriate geographical endpoints for your Translator service. For more information, *see* [Use Azure AI Translator behind firewalls](/azure/ai-services/translator/how-to/use-firewalls).

## Logging and monitoring

Implementing comprehensive logging and monitoring is essential for detecting potential security threats and troubleshooting issues with your Azure AI Translator deployment.

- **Enable diagnostic logging**: Configure Azure Monitor to collect and analyze logs from your Translator service to identify potential security issues, track usage patterns, and troubleshoot problems. For more information, *see* [Azure Monitor for Azure AI services](/azure/ai-services/monitor-cognitive-services).

- **Set up alerts for unusual activity**: Create Azure Monitor alerts to notify you of abnormal usage patterns, potential security breaches, or service disruptions affecting your Translator resources. For more information, *see* [Create, view, and manage metric alerts using Azure Monitor](/azure/azure-monitor/alerts/alerts-metric).

- **Configure audit logs**: Enable and review audit logs to monitor access and changes to your Translator resources. This ensures you know who is using your service and what actions are being performed. For more information, *see* [Azure resource logs](/azure/azure-monitor/essentials/resource-logs).

- **Implement request rate monitoring**: Monitor API request rates to detect potential denial of service attacks or unauthorized usage, ensuring your service remains available for legitimate use. For more information, *see* [Service and request limits for Azure AI Translator](/azure/ai-services/translator/service-limits).

## Compliance and governance

Establishing proper governance and ensuring compliance with relevant standards is crucial for the secure operation of Azure AI Translator services.

- **Review Azure Policy for AI services**: Implement Azure Policy to enforce organization-wide security standards for your AI services, including network isolation requirements. For more information, *see* [Azure Policy Regulatory Compliance controls for Azure AI services](/azure/ai-services/security-controls-policy#microsoft-cloud-security-benchmark).

- **Conduct regular security assessments**: Regularly evaluate the security posture of your Translator deployments against industry standards and company policies to identify and remediate potential vulnerabilities. For more information, *see* [Microsoft cloud security benchmark](/security/benchmark/azure/introduction).

- **Maintain regulatory compliance**: Configure your Translator service in accordance with applicable regulations for your industry and region, particularly regarding data privacy and protection. For more information, *see* [Azure AI Translator Transparency Note](/azure/ai-foundry/responsible-ai/translator/transparency-note).

- **Implement human oversight**: For sensitive translation scenarios, establish a human review process to validate translation quality and ensure content meets organizational standards before broad distribution. For more information, *see* [Azure AI Translator Transparency Note](/azure/ai-foundry/responsible-ai/translator/transparency-note#evaluating-and-integrating-azure-ai-translator-for-your-use).

## Service-specific security

Azure AI Translator has unique security considerations that should be addressed to ensure the confidentiality and integrity of your translation workflows.

- **Secure custom translation models**: Protect proprietary terminology and domain-specific language by implementing proper access controls for custom translation models and training data. For more information, *see* [Azure AI Custom Translator for beginners](/azure/ai-services/translator/custom-translator/beginners-guide).

- **Implement secure workflows for document translation**: For document translation, use secure storage containers with proper access controls and encryption to protect source documents and translation outputs. For more information, *see* [What is Azure AI Translator?](/azure/ai-services/translator/overview#azure-ai-translator-features-and-development-options).

- **Apply content filtering as needed**: For public-facing translation services, consider implementing additional content filtering mechanisms to prevent translation of harmful or inappropriate content. For more information, *see* [Prevent translation with the Translator service](/azure/ai-services/translator/prevent-translation).

- **Use containerized deployments for sensitive environments**: Consider using Translator containers for scenarios requiring high security or offline translation capabilities in disconnected environments. For more information, *see* [Azure AI Translator features and development options](/azure/ai-services/translator/overview#azure-ai-translator-features-and-development-options).

## Learn more

- [Microsoft Cloud Security Benchmark – Azure AI services](/security/benchmark/azure/baselines/azure-openai-security-baseline)
- [Well-Architected Framework – AI workloads](/azure/well-architected/ai/design-principles)
- [Security documentation for Azure AI services](/azure/ai-services/security-features)
- [Azure AI Translator documentation](/azure/ai-services/translator/)