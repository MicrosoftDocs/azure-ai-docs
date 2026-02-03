---
title: Data, privacy, and security for Document Intelligence
titleSuffix: Foundry Tools
description: This document details issues for data, privacy, and security for Document Intelligence.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: concept-article
ms.date: 10/15/2025
---


# Data, privacy, and security for Document Intelligence

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

This article provides details regarding how Document Intelligence processes your data. Document Intelligence is designed with compliance, privacy, and security in mind. However, you are responsible for its use and the implementation of this technology. It's your responsibility to comply with all applicable laws and regulations in your jurisdiction.

## How does Document Intelligence process data?

### Authenticate (with subscription or API keys)

The most common way to authenticate access to Document Intelligence is by using the customer's Document Intelligence API key. Each request to the service URL must include an authentication header. This header passes along an API key (or token if applicable), which is used to validate your subscription for a service or group of services. For more information, see [Authenticate requests to Foundry Tools](/azure/ai-services/authentication?tabs=powershell).

### Secure data in transit (for scanning)

All Foundry Tools endpoints, including the Document Intelligence API URLs, use HTTPS URLs for encrypting data during transit. The client operating system needs to support Transport Layer Security (TLS) 1.3 for calling the endpoints. For more information, see [Foundry Tools security](/azure/security/fundamentals/double-encryption).

### Encrypts input data for processing

The incoming data is processed in the same region where the Document Intelligence resource was created. When you submit your documents to a Document Intelligence operation, it starts the process of analyzing the document to extract all text and identify structure and key values in a document. Your data and results are then temporarily encrypted and stored in Azure Storage.

### Retrieve the results

The "Get Analyze Results" operation is authenticated against the same API key that was used to call the "Analyze" operation to ensure no other customer can access your data. It returns the analysis job completion status, When the status shows as completed, the operation also returns the extracted results in JSON format.

### Data stored by Document Intelligence

**For all analysis**: To facilitate asynchronous analysis and checking the completion status and returning the extracted results to the customer upon completion, the data and extracted results are stored temporarily in Azure Storage in the same region. All customers in the same region share the temporary storage. The customer’s data is logically isolated from other customers with their Azure subscription and API credentials.

**For customer trained models**: The Custom model feature allows customers to build custom models from training data stored in customer’s Azure blob storage locations. The interim outputs after analysis and labeling are stored in the same location. The trained custom models are stored in Azure storage in the same region and logically isolated with their Azure subscription and API credentials.

**Deletes data**: Analyze response is stored for 24 hours from when the operation completes for retrieval. Customers can delete the analysis response at any time by utilizing the [**Delete Analyze Result**](/rest/api/aiservices/document-models/delete-analyze-result?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true&tabs=HTTP) API. After successfully retrieving the analysis results, calling the [**Delete Analyze Result**](/rest/api/aiservices/document-models/delete-analyze-result?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true&tabs=HTTP) API permanently purges those results. This action applies to all models.

To learn more about privacy and security commitments, see the [Microsoft Trust Center](https://www.microsoft.com/TrustCenter/CloudServices/Azure/default.aspx).
