---
title: Custom Vision encryption of data at rest
titleSuffix: Foundry Tools
description: Learn how to enable and manage customer-managed keys (CMK) for data encryption at rest in Azure AI Custom Vision.
author: erindormier
manager: venkyv

ms.service: azure-ai-custom-vision
ms.topic: how-to
ms.date: 01/29/2025
ms.author: egeaney
ms.custom: cogserv-non-critical-vision
#Customer intent: As a user of the Face service, I want to learn how encryption at rest works.
---

# Custom Vision encryption of data at rest

Azure AI Custom Vision automatically encrypts your data when persisting it to the cloud. That encryption helps you to meet your organizational security and compliance commitments.

[!INCLUDE [cognitive-services-about-encryption](../includes/cognitive-services-about-encryption.md)]

> [!IMPORTANT]
> Customer-managed keys are only available resources created after 11 May 2020. To use CMK with Custom Vision, you need to create a new Custom Vision resource. Once the resource is created, you can use Azure Key Vault to set up your managed identity.

[!INCLUDE [cognitive-services-cmk](../includes/configure-customer-managed-keys.md)]

## Related content


* For a full list of services that support CMK, see [Customer-Managed Keys for Foundry Tools](../encryption/cognitive-services-encryption-keys-portal.md)
* [What is Azure Key Vault](/azure/key-vault/general/overview)?

