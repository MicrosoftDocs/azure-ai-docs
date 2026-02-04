---
title: Azure AI Content Safety Service encryption of data at rest
description: Learn how Azure AI Content Safety encrypts your data when it's persisted to the cloud.
titleSuffix: Azure AI services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: how-to
ms.date: 09/16/2025
ms.author: pafarley
ms.custom:
  - build-2023
  - sfi-image-nochange
---


# Azure AI Content Safety encryption of data at rest

Azure AI Content Safety automatically encrypts your data when it's persisted to the cloud. The encryption protects your data and helps you meet your organizational security and compliance commitments. This article covers how Azure AI Content Safety handles encryption of data at rest. 

[!INCLUDE [cognitive-services-about-encryption](../../includes/cognitive-services-about-encryption.md)]

[!INCLUDE [cognitive-services-cmk](../../includes/configure-customer-managed-keys.md)]

When you enable customer managed keys this also enables a system-assigned managed identity, a feature of Microsoft Entra ID. Once the system-assigned managed identity is enabled, your resource is registered with Microsoft Entra ID. After being registered, the managed identity will be given access to the Key Vault selected during customer managed key setup. Learn more about [Managed Identities](/azure/active-directory/managed-identities-azure-resources/overview).

## Next step

> [!div class="nextstepaction"]
> [Content Safety overview](../overview.md)