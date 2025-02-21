---
title: Azure AI Content Safety Service encryption of data at rest
description: Learn how Azure AI Content Safety encrypts your data when it's persisted to the cloud.
titleSuffix: Azure AI services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom: build-2023
ms.topic: conceptual
ms.date: 01/29/2025
ms.author: pafarley
---


# Azure AI Content Safety encryption of data at rest

Azure AI Content Safety automatically encrypts your data when it's persisted to the cloud. The encryption protects your data and helps you meet your organizational security and compliance commitments. This article covers how Azure AI Content Safety handles encryption of data at rest. 

[!INCLUDE [cognitive-services-about-encryption](../../includes/cognitive-services-about-encryption.md)]

[!INCLUDE [cognitive-services-cmk](../../includes/configure-customer-managed-keys.md)]

When you previously enabled customer managed keys this also enabled a system assigned managed identity, a feature of Microsoft Entra ID. Once the system assigned managed identity is enabled, this resource is registered with Microsoft Entra ID. After being registered, the managed identity will be given access to the Key Vault selected during customer managed key setup. You can learn more about [Managed Identities](/azure/active-directory/managed-identities-azure-resources/overview).

## Next step

> [!div class="nextstepaction"]
> [Content Safety overview](../overview.md)