---
title: Data, privacy, and security for optical character recognition (OCR) - Azure Vision in Foundry Tools
titleSuffix: Foundry Tools
description: This document details issues for data, privacy, and security for optical character recognition (OCR) of images and documents with printed and handwritten text using the Azure Vision in Foundry Tools API.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: concept-article
ms.date: 10/15/2025
---

# Data, privacy, and security for OCR

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

This article presents some high-level information about how the optical character recognition (OCR) service processes the data provided by customers. As an important reminder, you're responsible for the implementation of this technology and ensuring you have all necessary licenses or permissions to send data to this service. It's your responsibility to comply with all applicable laws and regulations in your jurisdiction.

## Data collection and processing

The [OCR service](/azure/ai-services/computer-vision/overview-ocr) processes the following types of data:

- The [OCR input data](/azure/ai-services/computer-vision/how-to/call-read-api#input-requirements) that includes images (PNG, JPG, and BMP) and documents (PDF and TIFF).
- The [OCR results](/azure/ai-services/computer-vision/how-to/call-read-api#sample-json-output) that includes the text extracted from customer documents and images in the form of text lines and words, and their locations, along with confidence scores.


## How does the OCR service process the data?

The following diagram illustrates how your data is processed.

:::image border type="content" source="./media/ocr/ocr-read-api-working.png" alt-text="Diagram that shows how the Azure Vision in Foundry Tools Read OCR API works.":::

**Authenticate (with subscription or API keys)**: The most common way to authenticate access to the Vision API and its Read OCR is by using the customer's Vision API key. Each request to the service URL must include an authentication header. This header passes along an API key (or token if applicable) that's used to validate your subscription for a service or group of services. [Learn more](/azure/ai-services/authentication?tabs=powershell).

**Secure data in transit (for scanning)**: All Foundry Tools endpoints, including the Vision Read API URLs, use HTTPS URLs for encrypting data during transit. The client operating system needs to support Transport Layer Security (TLS) 1.2 for calling the endpoints. [Learn more](/azure/ai-services/security-features).

**Encrypt input data for processing**: The incoming data is processed in the same region where the Vision resource was created. When you submit your documents to the Read operation, it starts the process of analyzing the document to extract all text. During this time, your data and results are temporarily encrypted and stored in a Microsoft internal Azure Storage resource.
 
**Retrieve the extracted text results**: You call the [Get Read Results](/azure/ai-services/computer-vision/how-to/call-read-api#get-results-from-the-service) operation to get the job completion status and optionally, the extracted text results if the job has succeeded. The other values of status tell you whether the operation has not started, is running, or has failed.

## Data stored by OCR

**Temporarily stores the results for customers to retrieve**: Recall that Read and Get Read Results are asynchronous calls. In other words, the service doesn't know when the customers will call the Get Read Results operation to fetch the extracted text results. To facilitate checking the completion status and returning the extracted results to the customer upon completion, the extracted text is stored temporarily in Azure Storage. This behavior allows customers to poll the asynchronous Get Read Results operation for job completion status and fetch the results upon completion.

**Deletes data**: The input data and results are deleted within 24 hours and not used for any other purpose.

To learn more about Microsoft privacy and security commitments, see the [Microsoft Trust Center](https://www.microsoft.com/trust-center).
