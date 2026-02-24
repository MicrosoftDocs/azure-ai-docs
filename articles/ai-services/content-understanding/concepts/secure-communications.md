---
title: Secure your Content Understanding analyzers and data
titleSuffix: Foundry Tools
description: Configure security features such as customer-managed keys and managed identities to secure your data and applications.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ms.service: azure-ai-content-understanding
ms.topic: concept-article
ms.custom:
  - ignite-2025
ai-usage: ai-assisted
---

# Security features in Azure Content Understanding in Foundry Tools

Content Understanding is part of Microsoft Foundry and provides the same security and privacy features available to all Foundry services. These capabilities help protect your data and ensure compliance with Microsoft security standards.

## Virtual networks

As part of Foundry Tools, Content Understanding supports network-level isolation through [Azure Virtual Networks](/azure/virtual-network/virtual-networks-overview) (VNet) and private endpoints ([Azure Private Link](/azure/private-link/private-link-overview)) to enable secure, enterprise-grade deployments. 

:::image type="content" source="../media/overview/virtual-network.jpg" alt-text="Diagram showing virtual network architecture with Content Understanding, including network isolation, private endpoints, and secure access control layers.":::

Content Understanding uses a layered security model that allows you to restrict access to specific networks. When network rules are enabled, only traffic from specific IP addresses, IP ranges, or a list of VNets/subnets are allowed to reach your Foundry resources. Any application accessing a Foundry resource must also be authorized through  [Microsoft Entra ID](/azure/active-directory/fundamentals/active-directory-whatis) (including managed identities) or by using a valid API key.  

Additionally, you can use [private endpoints](/azure/private-link/private-endpoint-overview) for your Content Understanding Foundry resource to allow clients on a virtual network to securely access data over [Azure Private Link](/azure/private-link/private-link-overview). The private endpoint uses an IP address from the virtual network address space for your Content Understanding Foundry resource. Network traffic between the clients on the virtual network and the resource traverses the virtual network and a private link on the Microsoft Azure backbone network, which eliminates exposure from the public internet.

To use Content Understanding Studio from a virtual machine within a VNet, you need to allow outgoing connections to the required set of [service tags](/azure/virtual-network/service-tags-overview) for this virtual network. 

For more details on how to configure and leverage these networking controls, please refer to the guidance in [Configure Foundry Tools virtual networks](/azure/ai-services/cognitive-services-virtual-networks?tabs=portal).  

### Foundry Tools encryption

Content Understanding in Foundry Tools automatically encrypts your data when persisting it to the cloud. This encryption helps you meet your organizational security and compliance commitments.

By default, your subscription uses Microsoft-managed encryption keys. Data is encrypted and decrypted using FIPS 140-2-compliant 256-bit AES encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default. You don't need to modify your code or applications to take advantage of encryption.

### Customer managed keys
You can also manage your subscription with your own keys, which are called customer-managed keys. When you use customer-managed keys, you have greater flexibility in the way you create, rotate, disable, and revoke access controls. You can also audit the encryption keys you use to protect your data.

If customer-managed keys are configured for your subscription, double encryption is provided. With this second layer of protection, you can control the encryption key through your Azure Key Vault.

Learn more about configuring [customer managed keys for your resource](/azure/ai-foundry/concepts/encryption-keys-portal).

To learn more about configuring network security for your Foundry resource, see [Azure security baseline for Foundry](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline).

## Managed identities

Managed identities for Azure resources are service principals that create a Microsoft Entra identity and specific permissions for Azure managed resources.
Managed identities grant access to any resource that supports Microsoft Entra authentication, including your own applications. Unlike security keys and authentication tokens, managed identities eliminate the need for developers to manage credentials.

You can grant access to an Azure resource and assign an Azure role to a managed identity using Azure role-based access control (Azure RBAC). There's no added cost to use managed identities in Azure.

To learn more about configuring managed identities for your Foundry resource, see [Azure security baseline for Foundry](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline#identity-management).




## Next steps

* [Learn more about Foundry security](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline)
* [Learn more about Content Understanding analyzers](analyzer-reference.md)