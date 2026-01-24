---
title: Secure your Azure Translator data and deployment
description: Learn how to secure Azure Translator, with best practices for protecting your data and deployment.
author: laujan
ms.author: lajanuar
ms.service: azure-ai-translator
ms.topic: best-practice
ms.custom: horz-security
ms.date: 11/18/2025
---

# Azure Translator in Foundry Tools security guidelines

Azure Translator in Foundry Tools is a powerful cloud-based service designed to deliver real-time translation capabilities for a wide range of scenarios, including applications, websites, and business workflows. When organizations integrate this service, they can enhance global communication and user engagement across multiple languages and dialects.

* **Security within Azure is grounded in a collaborative model, where the responsibility for protecting resources and data is shared between Microsoft and our customers.**

* **Microsoft is dedicated to securing the core infrastructure that underpins all Azure services, providing a reliable and robust foundation for cloud operations.** 

* **Our customers also play a crucial role in this security partnership by ensuring that Azure Translator is properly configured and managed, thereby protecting sensitive information and adhering to all relevant regulatory requirements.**

* **By clearly understanding and fulfilling their respective responsibilities, both Microsoft and our customers work together to achieve a comprehensive and resilient security posture in the Azure environment.** 

* For more information, *see* [**Shared responsibility in the cloud**](/azure/security/fundamentals/shared-responsibility)

This document offers detailed guidelines and practical recommendations for establishing and maintaining a secure environment when using Azure Translator. It's essential for users of any service to prioritize the protection of sensitive data, safeguard user privacy, and ensure deployment reliability. By adhering to these best practices, you help reduce risks and guarantee that your translation solutions remain secure and effective across all platforms.

 ## Service-specific security

Azure Translator requires careful consideration of specific security challenges and requirements to maintain the confidentiality and integrity of translation workflows. By taking a proactive approach to these security concerns, you can protect sensitive information during translation and reduce the risk of unauthorized access or data breaches.

* **Text translation**: For public-facing translation services, it's important to apply content filtering as necessary. Additionally, consider implementing extra filtering measures to prevent the translation of harmful or inappropriate content.<br> 
For more information, *see* [Prevent translation with the Translator](/azure/ai-services/translator/prevent-translation).

* **Document translation**: When translating documents, ensure secure workflows are established. Utilize secure storage containers with appropriate access controls and encryption to safeguard both the original documents and the translated outputs.<br>
For more information, *see* [What is Document Translation?](/azure/ai-services/translator/document-translation/how-to-guides/use-rest-api-programmatically).

* **Custom translation**: To ensure the security of proprietary terminology and domain-specific language, it's important to set up robust access controls for custom translation models. By restricting access to both the models and their underlying training data, organizations can effectively protect sensitive linguistic assets.<br>
For more information, *see* [Custom Translator for beginners](/azure/ai-services/translator/custom-translator/beginners-guide).

* **Azure Translator containers**: For scenarios that require high security or offline translation in isolated environments, consider deploying Translator containers. This deployment model is well-suited for safeguarding sensitive data and supporting translation workflows in controlled or disconnected environments.<br>
 For more information, *see* [Azure Translator features and development options](/azure/ai-services/translator/overview#azure-ai-translator-features-and-development-options).

## Identity and access management

Effectively overseeing identities and access permissions is crucial for protecting your Azure Translator deployments from unauthorized use and possible credential compromise. By enforcing secure access management, you guarantee that only approved users and devices are able to interact with your Translator resource. The following list identifies ways you can support secure access management:

* **Access**. To effectively manage user identities and securely control access permissions for your Azure Translator resources, enable Microsoft Entra ID. By integrating Microsoft Entra ID, you can streamline the administration of user accounts and ensure that only authorized individuals have access to your Azure Translator services.<br>
For more information, *see* [Enable Microsoft Entra ID authentication](/azure/ai-services/translator/how-to/microsoft-entra-id-auth)

* **Authorization**. Grant only the permissions that are essential for each role using role-based access control (RBAC). By utilizing RBAC-managed identities, you uphold the principle of least privilege, ensuring that users receive only the access required to perform their specific tasks. This approach greatly minimizes the possibility of unauthorized access to sensitive information or critical functions within your API.<br>
For more information, *see* [Managed identities: role-based access control](/azure/ai-services/translator/document-translation/how-to-guides/create-use-managed-identities)

* **Authentication**. Access to Translator data should be limited solely to entities that successfully complete authentication. This restriction requires users to successfully complete verification and receive authorization before they can view or modify Translator data. Only users with proper approval gain access or editing privileges. This approach provides a layer of security by making certain that unauthorized users can't access sensitive information or make changes that could impact the integrity of the data.<br>
For more information, *see* [Authentication and authorization](/azure/ai-services/translator/text-translation/reference/authentication)

* **Azure Key Vault**. Azure Key Vault offers a secure, centralized repository for application secrets like database connection strings, API keys, customer managed keys (CMK), passwords, and cryptographic keys. Using the key vault eliminates the need to hard-code sensitive information directly into application code or configuration files, reducing the risk of accidental exposure.<br>
For more information, *see* [About Azure Key Vault](/azure/key-vault/general/overview).<br>
For Custom Translator implementation, *see* [Encryption key management](/azure/ai-services/translator/custom-translator/concepts/encrypt-data-at-rest)<br><br>

   > [!TIP]
   > ✔️ **Rotate API keys regularly**: Keys in Azure Key Vault can be configured with rotation policies that automatically generate new key versions at specified frequencies. Regularly rotating your Translator API keys mitigates the risk of compromised credentials being used to access your services. For more information, *see* [Key autorotation](/azure/key-vault/general/autorotation).

## Network security

Azure Translator processes sensitive data from your applications. Therefore, it's essential to establish strong network isolation measures to prevent unauthorized access and ensure that translated content remains secure. The following list outlines key practices to help you manage secure access effectively:

* **Configure private endpoints**: Increase shielding by configuring private endpoints for API requests. This approach strengthens security and provides enhanced network isolation for your Azure Translator resources.<br>
For more information, *see* [Use private endpoints with Foundry Tools](/azure/ai-services/cognitive-services-virtual-networks#use-private-endpoints).

* **Implement virtual network service endpoints**: Augment safeguards by restricting network access to allow only traffic originating from your Azure virtual network. At the same time, ensure that you maintain optimal routing by utilizing the Microsoft backbone network for all communications.<br> 
For more information, *see* [Enable custom Translator through Azure Virtual Network](/azure/ai-services/translator/custom-translator/how-to/enable-vnet-service-endpoint).

* **Configure firewall rules**: Enhance security by designating specific IP addresses or ranges that are permitted to access your Translator resource. Restricting access in this way minimizes the likelihood of unauthorized connections from unfamiliar networks.<br>
For more information, *see* [Use Azure Translator behind firewalls](/azure/ai-services/translator/how-to/use-firewalls#configure-firewall).

* **Use region-specific endpoints**: Bolster security and compliance by utilizing geographic endpoints. This approach ensures your traffic remains within designated regions and supports adherence to data residency regulations. For more information, *see* [Use Azure Translator behind firewalls](/azure/ai-services/translator/how-to/use-firewalls).

## Data protection

Azure Translator processes sensitive text and document content. Because of the confidential nature of this information, implementing robust data protection measures is essential. These safeguards are vital not only to maintain the privacy and confidentiality of the data being processed but also to ensure compliance with relevant regulations and industry standards.

* **Enable data encryption at rest**: Ensure your data is automatically encrypted with Federal Information Processing Standard (FIPS) 140-2 compliant 256-bit Advanced Encryption Standard (AES) when stored by the service.<br>
For more information, *see* [Microsoft compliance](/compliance/regulatory/offering-fips-140-2).

* **Implement Customer-managed keys (CMK)**: To achieve enhanced control over encryption key management, configure customer-managed keys for Translator resources by integrating Azure Key Vault. This capability is accessible when selecting a pricing tier that includes support for customer-managed key functionality.<br>
For more information, *see* [Azure Translator encryption of data at rest](/azure/ai-services/translator/custom-translator/concepts/encrypt-data-at-rest).

* **Review details of the No-Trace policy**: Translator doesn't retain customer data submitted for text translation; it processes the data without storing it. For document translation, data is stored only temporarily during processing and isn't kept afterward.<br> 
For more information, *see* [Data, privacy, and security for Azure Translator](/azure/ai-foundry/responsible-ai/translator/data-privacy-security).

* **Follow data residency requirements**: To ensure that your deployment adheres to regional data residency regulations, select the designated geographical endpoints for your Translator. Use these endpoints to remain compliant with local requirements.<br>
For more information, *see* [Use Azure Translator behind firewalls](/azure/ai-services/translator/how-to/use-firewalls).

## Logging and monitoring

Establishing robust logging and monitoring is critical for identifying potential security threats and resolving issues within your Azure Translator deployment. By ensuring that all relevant activities and anomalies are thoroughly tracked, you can enhance your overall security posture and streamline troubleshooting processes throughout your cloud-based translation environment.

* **Enable diagnostic logging**: Configure Azure Monitor to collect and analyze logs from your Translator to identify potential security issues, track usage patterns, and troubleshoot problems.<br>
For more information, *see* [Azure Monitor for Foundry Tools](/azure/azure-monitor/platform/monitor-azure-resource).

* **Set up alerts for unusual activity**: Create Azure Monitor alerts to notify you of abnormal usage patterns, potential security breaches, or service disruptions affecting your Translator resources.<br>
For more information, *see* [Create, view, and manage metric alerts using Azure Monitor](/azure/azure-monitor/alerts/alerts-metric).

* **Configure audit logs**: Enable and review audit logs to monitor access and changes to your Translator resources. Audit logs ensure you know who is using your service and what actions are being performed.<br>
For more information, *see* [Resource logs in Azure Monitor](/azure/azure-monitor/platform/resource-logs).

* **Implement request rate monitoring**: Monitor API request rates to detect potential denial of service attacks or unauthorized usage, ensuring your service remains available for legitimate use.<br>
For more information, *see* [Service and request limits for Azure Translator](/azure/ai-services/translator/service-limits).

## Compliance and governance

To ensure the secure operation of Azure Translator services, you need to put a robust governance framework in place and consistently comply with all relevant standards. By establishing thorough policies and procedures, you can effectively protect your systems, maintain regulatory compliance, and minimize potential risks, ultimately delivering reliable and secure service.

* **Review Azure Policy for Foundry Tools**: Implement Azure Policy to enforce organization-wide security standards for your Foundry Tools, including network isolation requirements.<br>
For more information, *see* [Azure Policy Regulatory Compliance controls for Foundry Tools](/azure/ai-services/security-controls-policy#microsoft-cloud-security-benchmark).

* **Conduct regular security assessments**: Continuously assess the security status of your Translator deployments and ensure they align with industry standards and organizational policies. Promptly detect and address any potential vulnerabilities as they arise.<br>
For more information, *see* [Microsoft cloud security benchmark](/security/benchmark/azure/introduction).

* **Maintain regulatory compliance**: Configure your Translator to comply with all relevant laws and regulations that apply to your industry and geographic area. Make sure to pay special attention to any requirements related to data privacy and protection.<br> 
For more information, *see* [Azure Translator Transparency Note](/azure/ai-foundry/responsible-ai/translator/transparency-note).

* **Implement human oversight**: For sensitive translation scenarios, implement a human review workflow to verify translation accuracy. This process ensures that all content complies with organizational standards before wide distribution.<br>
For more information, *see* [Azure Translator Transparency Note](/azure/ai-foundry/responsible-ai/translator/transparency-note#evaluating-and-integrating-azure-ai-translator-for-your-use).




## Related content

* [Azure Translator documentation](/azure/ai-services/translator/)
* [Microsoft Cloud Security Benchmark – Foundry Tools](/security/benchmark/azure/baselines/azure-openai-security-baseline)
* [Well-Architected Framework – AI workloads](/azure/well-architected/ai/design-principles)
* [Security documentation for Foundry Tools](/azure/ai-services/security-features)
