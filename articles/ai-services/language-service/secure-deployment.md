---
title: Secure your Azure Language data and deployment
titleSuffix: Foundry Tools
description: Learn how to secure Azure Language, with best practices for protecting your data and deployment.
author: laujan
manager: mcleans
ms.service: azure-language-foundry-tools
ms.topic: best-practice
ms.date: 07/16/2026
ms.author: lajanuar
ms.custom: horz-security
---

<!-- markdownlint-disable MD025 -->
# Secure your Azure Language data and deployment

Azure Language in Foundry Tools is a cloud-based service that provides Natural Language Processing (NLP) capabilities for understanding and analyzing text across applications, workflows, and business processes. When organizations integrate this service, they can extract insights, classify content, and detect sensitive information across many languages.

- **Security within Azure is grounded in a collaborative model, where Microsoft and customers share the responsibility for protecting resources and data.**

- **Microsoft is dedicated to securing the core infrastructure that underpins all Azure services, providing a reliable and robust foundation for cloud operations.**

- **Customers play a crucial role in this security partnership by ensuring that Azure Language is properly configured and managed, thereby protecting sensitive information and adhering to all relevant regulatory requirements.**

- **By clearly understanding and fulfilling their respective responsibilities, both Microsoft and customers work together to achieve a comprehensive and resilient security posture in the Azure environment.**

For more information, *see* [**Shared responsibility in the cloud**](/azure/security/fundamentals/shared-responsibility).

This document offers detailed guidelines and practical recommendations for establishing and maintaining a secure environment when using Azure Language. It's essential for users of any service to prioritize the protection of sensitive data, safeguard user privacy, and ensure deployment reliability. By adhering to these best practices, you help reduce risks and guarantee that your language solutions remain secure and effective across all platforms.

## Service-specific security

Azure Language requires careful consideration of specific security challenges and requirements to maintain the confidentiality and integrity of natural language processing workflows. By taking a proactive approach to these security concerns, you can protect sensitive information during processing and reduce the risk of unauthorized access or data breaches. The following guidance is organized by [core capabilities](overview.md#core-capabilities), which are recommended for new development, and [legacy capabilities](overview.md#legacy-capabilities), which are supported for existing implementations.

### Core capabilities

- **Personally identifiable information (PII) detection**: For workflows that process sensitive content, use PII detection to identify and redact personal data before storing, sharing, or displaying text and conversations. Redacting sensitive values reduces the risk of unintended exposure downstream. To narrow output to protected health information, set the `domain=phi` parameter. By default, the service temporarily stores and encrypts submitted input for up to 48 hours to support troubleshooting. Set `loggingOptOut=true` to prevent this temporary storage. For more information, *see* [What is personally identifiable information (PII) detection](personally-identifiable-information/overview.md).
- **Language detection**: When routing or preprocessing untrusted input based on detected language, validate and sanitize the text before passing it to downstream systems to avoid propagating malicious content. For more information, *see* [What is language detection](language-detection/overview.md).
- **Named entity recognition (NER)**: Prebuilt NER can surface sensitive entities such as names, locations, and organizations from unstructured text. Apply appropriate access controls to both the input text and the extracted results, and consider pairing NER with PII detection when handling confidential content. When redacting, use the `piiCategories` parameter to explicitly specify which entity categories to detect, so that sensitive values you intend to redact aren't inadvertently left exposed. For more information, *see* [What is named entity recognition (NER)](named-entity-recognition/overview.md).
- **Custom NER**: To ensure the security of proprietary schemas, labels, and domain-specific language, set up robust access controls for custom NER projects. Your labeled training data is stored in your own Azure Blob Storage account, and trained models are retained by the service until you delete them, so restrict access to that storage account and remove models you no longer need. Text submitted for extraction isn't stored by the service. For more information, *see* [What is custom named entity recognition](custom-named-entity-recognition/overview.md).
- **Text analytics for health**: When processing clinical or health-related text, protect any protected health information (PHI) surfaced during extraction. Establish secure handling and access controls for both source text and results. Temporary input logging is disabled by default (`loggingOptOut=true`) for health processing, and the capability can run in a container for on-premises or isolated environments. For more information, *see* [What is Text Analytics for health](text-analytics-for-health/overview.md).

### Legacy capabilities

- **Conversational language understanding (CLU)**: Restrict access to CLU projects, models, and training utterances, which can contain sensitive intents and domain-specific language. Apply least-privilege access controls to protect these proprietary assets. For more information, *see* [What is conversational language understanding](conversational-language-understanding/overview.md).
- **Custom text classification**: Protect the classes, labels, and training documents that define your custom classification models by restricting access to both the models and their underlying training data. Your labeled dataset is stored in your own Azure Blob Storage account, and the service retains trained models until you delete them, so secure that storage account and remove unused models. The service doesn't store text submitted for classification. For more information, *see* [What is custom text classification](custom-text-classification/overview.md).
- **Entity linking**: When disambiguating entities and returning external links, validate and sanitize returned content before displaying it to end users to avoid surfacing untrusted references. For more information, *see* [What is entity linking](entity-linking/overview.md).
- **Key phrase extraction**: Apply appropriate access controls to input text and extracted key phrases, which can reveal the substance of confidential documents. For more information, *see* [What is key phrase extraction](key-phrase-extraction/overview.md).
- **Orchestration workflow**: Because orchestration connects CLU and custom question answering projects, secure each connected project and enforce consistent access controls across the workflow. For more information, *see* [What is orchestration workflow](orchestration-workflow/overview.md).
- **Question answering**: Secure the knowledge bases and source content that power question answering, and apply access controls to prevent unauthorized users from viewing or modifying answers. Knowledge bases and chat logs are stored in your own Azure resources (Azure AI Search and, when diagnostic logging is enabled, Azure Monitor), so apply role-based access control to those resources and enable chat logging only when needed. For more information, *see* [What is question answering](question-answering/overview.md).
- **Sentiment analysis and opinion mining**: Apply access controls to the text you analyze and to the sentiment results, which can reveal sensitive customer or business information. For more information, *see* [What is sentiment analysis and opinion mining](sentiment-opinion-mining/overview.md).
- **Summarization**: When summarizing text or conversations, protect both the source content and the generated summaries, which can retain sensitive information. For more information, *see* [What is summarization](summarization/overview.md).

### Deployment considerations

The following options apply across core and legacy capabilities:

- **Native document support**: When processing documents, ensure secure workflows are established. Use secure storage containers with appropriate access controls and encryption to safeguard both the original documents and the processed outputs. For more information, *see* [Native document support for Azure Language](native-document-support/overview.md).
- **Azure Language containers**: For scenarios that require high security or offline processing in isolated environments, consider deploying Language containers. This deployment model is well-suited for safeguarding sensitive data and supporting processing workflows in controlled or disconnected environments. For more information, *see* [Configure Language docker containers](concepts/configure-containers.md).

## Identity and access management

Effectively overseeing identities and access permissions is crucial for protecting your Azure Language deployments from unauthorized use and possible credential compromise. By enforcing secure access management, you guarantee that only approved users and devices can interact with your Language resource. The following list identifies ways you can support secure access management:

- **Access**. To effectively manage user identities and securely control access permissions for your Azure Language resources, enable Microsoft Entra ID. By integrating Microsoft Entra ID, you can streamline the administration of user accounts and ensure that only authorized individuals have access to your Azure Language services. For more information, *see* [Enable Microsoft Entra authentication](concepts/role-based-access-control.md#enable-microsoft-entra-authentication).
- **Authorization**. Grant only the permissions that are essential for each role using role-based access control (RBAC). By utilizing RBAC-managed identities, you uphold the principle of least privilege, ensuring that users receive only the access required to perform their specific tasks. This approach greatly minimizes the possibility of unauthorized access to sensitive information or critical functions within your resource. For more information, *see* [Language role-based access control](concepts/role-based-access-control.md).
- **Authentication**. Access to Language data should be limited solely to entities that successfully complete authentication. This restriction requires users to complete verification and receive authorization before they can view or modify Language data. This approach provides a layer of security by making certain that unauthorized users can't access sensitive information or make changes that could impact the integrity of the data. For more information, *see* [Authenticate requests to Foundry Tools](/azure/ai-services/authentication).
- **Azure Key Vault**. Azure Key Vault offers a secure, centralized repository for application secrets like database connection strings, API keys, customer-managed keys (CMK), passwords, and cryptographic keys. Using the key vault eliminates the need to hard-code sensitive information directly into application code or configuration files, reducing the risk of accidental exposure. For more information, *see* [About Azure Key Vault](/azure/key-vault/general/overview). For Language encryption key management, *see* [Language service encryption of data at rest](concepts/encryption-data-at-rest.md).

    > [!TIP]
    > ✔️ **Rotate API keys regularly**: Keys in Azure Key Vault can be configured with rotation policies that automatically generate new key versions at specified frequencies. Regularly rotating your Language API keys mitigates the risk of compromised credentials being used to access your services. For more information, *see* [Key autorotation](/azure/key-vault/general/autorotation).

## Network security

Azure Language processes sensitive data from your applications. Therefore, it's essential to establish strong network isolation measures to prevent unauthorized access and ensure that content remains secure. The following list outlines key practices to help you manage secure access effectively:

- **Configure private endpoints**: Increase shielding by configuring private endpoints for API requests. This approach strengthens security and provides enhanced network isolation for your Azure Language resources. For more information, *see* [Use private endpoints with Foundry Tools](/azure/ai-services/cognitive-services-virtual-networks#use-private-endpoints).
- **Implement virtual network service endpoints**: Augment safeguards by restricting network access to allow only traffic originating from your Azure virtual network. At the same time, ensure that you maintain optimal routing by utilizing the Microsoft backbone network for all communications. For more information, *see* [Configure virtual networks for Foundry Tools](/azure/ai-services/cognitive-services-virtual-networks).
- **Configure firewall rules**: Enhance security by designating specific IP addresses or ranges that are permitted to access your Language resource. Restricting access in this way minimizes the likelihood of unauthorized connections from unfamiliar networks. For more information, *see* [Configure Foundry Tools virtual networks](/azure/ai-services/cognitive-services-virtual-networks#grant-access-from-an-internet-ip-range).

## Data protection

Azure Language processes sensitive text and document content. Because of the confidential nature of this information, implementing robust data protection measures is essential. These safeguards are vital not only to maintain the privacy and confidentiality of the data being processed but also to ensure compliance with relevant regulations and industry standards.

- **Enable data encryption at rest**: Ensure your data is automatically encrypted with Federal Information Processing Standard (FIPS) 140-2 compliant 256-bit Advanced Encryption Standard (AES) when stored by the service. For more information, *see* [Language service encryption of data at rest](concepts/encryption-data-at-rest.md).
- **Implement customer-managed keys (CMK)**: To achieve enhanced control over encryption key management, configure customer-managed keys for Language resources by integrating Azure Key Vault. This capability is accessible when selecting a pricing tier that includes support for customer-managed key functionality. For more information, *see* [Customer-managed keys with Azure Key Vault](concepts/encryption-data-at-rest.md#customer-managed-keys-with-azure-key-vault).
- **Review data retention and privacy details**: Understand how Azure Language handles the data you submit, including what's retained during processing and how customer data is protected. For more information, *see* [Data, privacy, and security for Azure Language](/azure/ai-foundry/responsible-ai/language-service/data-privacy).
- **Follow data residency requirements**: To ensure that your deployment adheres to regional data residency regulations, select the designated region for your Language resource. Use supported regions to remain compliant with local requirements. For more information, *see* [Region support for Azure Language](concepts/regional-support.md).

## Logging and monitoring

Establishing robust logging and monitoring is critical for identifying potential security threats and resolving issues within your Azure Language deployment. By ensuring that all relevant activities and anomalies are thoroughly tracked, you can enhance your overall security posture and streamline troubleshooting processes throughout your cloud-based language environment.

- **Enable diagnostic logging**: Configure Azure Monitor to collect and analyze logs from your Language resource to identify potential security issues, track usage patterns, and troubleshoot problems. For more information, *see* [Monitor Azure resources with Azure Monitor](/azure/azure-monitor/platform/monitor-azure-resource).
- **Set up alerts for unusual activity**: Create Azure Monitor alerts to notify you of abnormal usage patterns, potential security breaches, or service disruptions affecting your Language resources. For more information, *see* [Create, view, and manage metric alerts using Azure Monitor](/azure/azure-monitor/alerts/alerts-metric).
- **Configure audit logs**: Enable and review audit logs to monitor access and changes to your Language resources. Audit logs ensure you know who is using your service and what actions are being performed. For more information, *see* [Resource logs in Azure Monitor](/azure/azure-monitor/platform/resource-logs).
- **Implement request rate monitoring**: Monitor API request rates to detect potential denial of service attacks or unauthorized usage, ensuring your service remains available for legitimate use. For more information, *see* [Service limits for Azure Language](concepts/data-limits.md).

## Compliance and governance

To ensure the secure operation of Azure Language services, put a robust governance framework in place and consistently comply with all relevant standards. By establishing thorough policies and procedures, you can effectively protect your systems, maintain regulatory compliance, and minimize potential risks. This approach helps you deliver a reliable and secure service.

- **Review Azure Policy for Foundry Tools**: Implement Azure Policy to enforce organization-wide security standards for your Foundry Tools, including network isolation requirements. For more information, *see* [Azure Policy Regulatory Compliance controls for Foundry Tools](/azure/ai-services/security-controls-policy#microsoft-cloud-security-benchmark).
- **Conduct regular security assessments**: Continuously assess the security status of your Language deployments and ensure they align with industry standards and organizational policies. Promptly detect and address any potential vulnerabilities as they arise. For more information, *see* [Microsoft cloud security benchmark](/security/benchmark/azure/introduction).
- **Maintain regulatory compliance**: Configure your Language resource to comply with all relevant laws and regulations that apply to your industry and geographic area. Pay special attention to any requirements related to data privacy and protection. For more information, *see* [Transparency note for Azure Language](/azure/ai-foundry/responsible-ai/language-service/transparency-note).
- **Implement human oversight**: For sensitive scenarios, implement a human review workflow to verify output accuracy. This process ensures that all content complies with organizational standards before wide distribution. For more information, *see* [Guidance for integration and responsible use](/azure/ai-foundry/responsible-ai/language-service/guidance-integration-responsible-use).

## Related content

- [Microsoft Cloud Security Benchmark – Foundry Tools](/security/benchmark/azure/baselines/azure-openai-security-baseline)
- [Well-Architected Framework – AI workloads](/azure/well-architected/ai/design-principles)
- [Security documentation for Foundry Tools](/azure/ai-services/security-features)
