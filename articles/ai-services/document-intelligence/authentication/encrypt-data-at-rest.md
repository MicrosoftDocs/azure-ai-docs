---
title: Service encryption of data at rest - Document Intelligence 
titleSuffix: Foundry Tools
description: Microsoft offers Microsoft-managed encryption keys, and also lets you manage your Foundry Tools subscriptions with your own keys, called customer-managed keys (CMK). This article covers data encryption at rest for Document Intelligence, and how to enable and manage CMK.
author: erindormier
manager: venkyv
ms.service: azure-ai-document-intelligence
ms.topic: how-to
ms.date: 11/18/2025
monikerRange: '<=doc-intel-4.0.0'
---


# Encrypt data at rest

[!INCLUDE [applies to v4.0, v3.1, v3.0, and v2.1](../includes/applies-to-v40-v31-v30-v21.md)]

> [!IMPORTANT]
>
> * Earlier versions of customer managed keys (`CMK`) only encrypted your models.
> * Beginning with the  ```07/31/2023``` release, all new resources utilize customer-managed keys to encrypt both models and document results.
> * [Delete analyze response](/rest/api/aiservices/document-models/delete-analyze-result?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true&tabs=HTTP). the `analyze response` is stored for 24 hours from when the operation completes for retrieval. For scenarios where you want to delete the response sooner, use the delete analyze response API to delete the response.  
> * To upgrade an existing service to encrypt both the models and the data, disable and reenable the customer managed key.

Azure Document Intelligence in Foundry Tools automatically encrypts your data when persisting it to the cloud. Document Intelligence encryption protects your data to help you to meet your organizational security and compliance commitments.  

[!INCLUDE [cognitive-services-about-encryption](../../../ai-services/includes/cognitive-services-about-encryption.md)]

> [!IMPORTANT]
> * Customer-managed keys are only available resources created after May 11, 2020. To use customer-managed keys with Document Intelligence, you need to create a new Document Intelligence resource. Once the resource is created, you can use Azure Key Vault to set up your managed identity.
> * The scope for data encrypted with customer-managed keys includes the `analysis response` stored for 24 hours, allowing the operation results to be retrieved during that 24-hour time period.


[!INCLUDE [cognitive-services-cmk](../../../ai-services/includes/configure-customer-managed-keys.md)]

## Next steps

* [Learn more about Azure Key Vault](/azure/key-vault/general/overview)
