---
title: Face service encryption of data at rest
titleSuffix: Foundry Tools
description: Microsoft offers Microsoft-managed encryption keys, and also lets you manage your Foundry Tools subscriptions with your own keys, called customer-managed keys (CMK). This article covers data encryption at rest for Face, and how to enable and manage CMK. 
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.update-cycle: 90-days
ms.topic: how-to
ms.date: 01/30/2026
ms.author: pafarley
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
#Customer intent: As a user of the Face service, I want to learn how encryption at rest works.
---

# Face service encryption of data at rest

The Face service automatically encrypts your data when it's persisted to the cloud. That encryption protects your data and helps you meet your organizational security and compliance commitments.

[!INCLUDE [cognitive-services-about-encryption](../includes/cognitive-services-about-encryption.md)]

[!INCLUDE [cognitive-services-cmk](../includes/configure-customer-managed-keys.md)]

## Related content

* For a full list of services that support CMK, see [Customer-Managed Keys for Foundry Tools](../encryption/cognitive-services-encryption-keys-portal.md)
* [What is Azure Key Vault?](/azure/key-vault/general/overview)

