---
title: Data, privacy, and security for Document Intelligence
titleSuffix: Azure AI services
description: This document details issues for data, privacy, and security for Document Intelligence.
author: sanjeev3
ms.author: sajagtap
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: article
ms.date: 05/04/2021
---


# Data, privacy, and security for Document Intelligence

This article provides details regarding how Document Intelligence processes your data. Document Intelligence is designed with compliance, privacy, and security in mind. However, you are responsible for its use and the implementation of this technology. It's your responsibility to comply with all applicable laws and regulations in your jurisdiction.

## How does Document Intelligence process data?

### Authenticate (with subscription or API keys)

The most common way to authenticate access to Document Intelligence is by using the customer's Document Intelligence API key. Each request to the service URL must include an authentication header. This header passes along an API key (or token if applicable), which is used to validate your subscription for a service or group of services. For more information, see [Authenticate requests to Azure AI services](/azure/ai-services/authentication?tabs=powershell).

### Secure data in transit (for scanning)

All Azure AI services endpoints, including the Document Intelligence API URLs, use HTTPS URLs for encrypting data during transit. The client operating system needs to support Transport Layer Security (TLS) 1.2 for calling the endpoints. For more information, see [Azure AI services security](/azure/security/fundamentals/double-encryption).

### Encrypts input data for processing

The incoming data is processed in the same region where the Document Intelligence resource was created. When you submit your documents to a Document Intelligence operation, it starts the process of analyzing the document to extract all text and identify structure and key values in a document. Your data and results are then temporarily encrypted and stored in Azure Storage.

### Retrieve the results

The "Get Analyze Results" operation is authenticated against the same API key that was used to call the "Analyze" operation to ensure no other customer can access your data. It returns the analysis job completion status, When the status shows as completed, the operation also returns the extracted results in JSON format.

### Data stored by Document Intelligence

**For all analysis**: To facilitate asynchronous analysis and checking the completion status and returning the extracted results to the customer upon completion, the data and extracted results are stored temporarily in Azure Storage in the same region. All customers in the same region share the temporary storage. The customer’s data is logically isolated from other customers with their Azure subscription and API credentials.

**For customer trained models**: The Custom model feature allows customers to build custom models from training data stored in customer’s Azure blob storage locations. The interim outputs after analysis and labeling are stored in the same location. The trained custom models are stored in Azure storage in the same region and logically isolated with their Azure subscription and API credentials.

**Deletes data**: For all features, the input data and results are deleted within 24 hours and not used for any other purpose. For customer trained models, the customers can delete their models and associated metadata at any time by using the API.

To learn more about privacy and security commitments, see the [Microsoft Trust Center](https://www.microsoft.com/TrustCenter/CloudServices/Azure/default.aspx).
