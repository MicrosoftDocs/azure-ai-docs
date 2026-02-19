---
title: Custom question answering encryption of data at rest
titleSuffix: Foundry Tools
description: Microsoft offers Microsoft-managed encryption keys, and also lets you manage your Azure AI services subscriptions with your own keys, called customer-managed keys (CMK). This article covers data encryption at rest for custom question answering, and how to enable and manage CMK.
author: erindormier
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 12/15/2025
ms.author: egeaney
ms.custom: language-service-question-answering
---
# Custom question answering encryption of data at rest

Custom question answering automatically encrypts your data when persisted to the cloud, helping to meet your organizational security and compliance goals.

## About encryption key management

By default, your subscription uses Microsoft-managed encryption keys. There's also the option to manage your resource with your own keys called customer-managed keys (CMK). CMK offers greater flexibility to create, rotate, disable, and revoke access controls. You can also audit the encryption keys used to protect your data. If CMK is configured for your subscription, double encryption is provided, which offers a second layer of protection, while allowing you to control the encryption key through your Azure Key Vault.

Custom question answering uses CMK support from Azure search, and associates the provided CMK to encrypt the data stored in Azure search index. Follow the steps listed in [this article](/azure/search/search-security-manage-encryption-keys) and configure Key Vault access for the Azure search service.

> [!NOTE]
> Whenever the CMK is being rotated, ensure that there's a period of overlap between the old and new versions of the key. During this time, both versions should be enabled and not expired.

> [!IMPORTANT]
> Your Azure Search service resource must be created after January 2019 and can't be in the free (shared) tier. There's no support to configure customer-managed keys in the Azure portal.

## Enable customer-managed keys

Follow these steps for enabling CMKs:

1.    Go to the **Encryption** tab of your language resource with custom question answering enabled.
2.    Select the **Customer Managed Keys** option. Provide the details of your [customer-managed keys](/azure/storage/common/customer-managed-keys-configure-key-vault?tabs=portal) and select **Save**.

> [!div class="mx-imgBorder"]
> ![Custom question answering CMK](../media/encrypt-data-at-rest/question-answering-cmk.png)
   
3.    On a successful save, the CMK is used to encrypt the data stored in the Azure Search Index.

> [!IMPORTANT]
> We recommend that you set your CMK in a fresh Azure AI Search service before any projects are created. If you set CMK in a language resource with existing projects, you might lose access to them. Read more about [working with encrypted content](/azure/search/search-security-manage-encryption-keys#work-with-encrypted-content) in Azure AI Search.

## Regional availability

Customer-managed keys are available in all Azure Search regions.

## Encryption of data in transit

Every action triggers a direct call to the respective Foundry Tools API. Hence, custom question answering is compliant for data in transit.

## Next steps

* [Encryption in Azure Search using CMKs in Azure Key Vault](/azure/search/search-security-manage-encryption-keys)
* [Data encryption at rest](/azure/security/fundamentals/encryption-atrest)
* [Learn more about Azure Key Vault](/azure/key-vault/general/overview)
