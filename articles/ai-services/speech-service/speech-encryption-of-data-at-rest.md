---
title: Speech service encryption of data at rest
titleSuffix: Azure AI services
description: Microsoft offers Microsoft-managed encryption keys, and also lets you manage your Azure AI services subscriptions with your own keys, called customer-managed keys (CMK). This article covers data encryption at rest for Speech service.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: conceptual
ms.date: 9/24/2024
ms.author: eur
#Customer intent: As a developer, I want to learn about data encryption at rest for Speech service.
---

# Speech service encryption of data at rest

Speech service automatically encrypts your data when it's persisted it to the cloud. Speech service encryption protects your data and to help you to meet your organizational security and compliance commitments.

## About Azure AI services encryption

Data is encrypted and decrypted using [FIPS 140-2](https://en.wikipedia.org/wiki/FIPS_140-2) compliant [256-bit AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. Encryption and decryption are transparent, meaning encryption and access are managed for you. Your data is secure by default and you don't need to modify your code or applications to take advantage of encryption.

## About encryption key management

When you use custom speech and custom voice, Speech service might store the following data in the cloud:  

* Speech trace data - only if your turn the trace on for your custom endpoint
* Uploaded training and test data

By default, your data are stored in Microsoft's storage and your subscription uses Microsoft-managed encryption keys. You also have an option to prepare your own storage account. Access to the store is managed by the Managed Identity, and Speech service can't directly access to your own data, such as speech trace data, customization training data and custom models.

For more information about Managed Identity, see [What are managed identities](/azure/active-directory/managed-identities-azure-resources/overview).

## Bring your own storage (BYOS)

Bring your own storage (BYOS) is an Azure AI technology for customers, who have high requirements for data security and privacy. The core of the technology is the ability to associate an Azure Storage account, that the user owns and fully controls with the Speech resource. The Speech resource then uses this storage account for storing different artifacts related to the user data processing, instead of storing the same artifacts within the Speech service premises as it is done in the regular case. This approach allows using all set of security features of Azure Storage account, including encrypting the data with the Customer-managed keys, using Private endpoints to access the data, etc.

The Speech service doesn't currently support Customer Lockbox. However, customer data can be stored using BYOS, allowing you to achieve similar data controls to [Customer Lockbox](/azure/security/fundamentals/customer-lockbox-overview).

> [!IMPORTANT]
> Microsoft **does not** use customer data to improve its Speech models. Additionally, if endpoint logging is disabled and no customizations are used, then no customer data is stored. 

See detailed information on using BYOS-enabled Speech resource in [this article](bring-your-own-storage-speech-resource.md).

## Next steps

* [Set up the Bring your own storage (BYOS) Speech resource](bring-your-own-storage-speech-resource.md)
* [What are managed identities](/azure/active-directory/managed-identities-azure-resources/overview).
