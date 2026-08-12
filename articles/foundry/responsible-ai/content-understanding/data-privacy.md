---
title: "Data, privacy, and security for Content Understanding"
titleSuffix: Foundry Tools
description: "This document details issues for data, privacy, and security for Content Understanding."
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.service: azure-content-understanding-foundry-tools
ms.topic: concept-article
ms.date: 07/16/2026
ai-usage: ai-assisted
---

# Data, privacy, and security for Content Understanding
[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Content Understanding builds upon the functionality of Document Intelligence, Speech to Text, Image Analysis, Face, Video and Azure OpenAI, each designed with compliance, privacy, and security at its core. This combined service processes various types of customer-provided data, such as documents, audio, images, biometric data (face), text, and video to deliver powerful analysis and intelligence capabilities. Importantly, users are responsible for ensuring that their use of this service complies with all applicable laws and regulations in their jurisdiction, including data protection, privacy, and communications laws, as well as any specific requirements around biometric data when leveraging facial recognition features. It's essential to acquire all necessary permissions, licenses, or third-party rights for the content and data submitted for processing. 

Since the data processed in this integrated service may involve personal or sensitive information, including biometric identifiers and human speech content, users must follow all jurisdictional requirements related to data protection. For instance, when using biometric technologies, it's crucial to provide clear, conspicuous disclosure to individuals, particularly in regions with strict biometric data governance. Data provided to the Azure OpenAI service is stored and processed to monitor compliance with product terms, and [Microsoft’s Products and Services Data Protection Addendum](https://go.microsoft.com/fwlink/?linkid=2131539) applies to all data handling within the Azure OpenAI framework. By combining these technologies, our service offers robust insights while ensuring users maintain responsibility for adhering to legal and regulatory standards. 

## What data does Content Understanding process? 

Content Understanding can process audio input or voice audio, image files, document files, and video files. Each input type has different file limits, such as file type, size, length, and resolution. The limits are outlined in the [service quotas and limits documentation](/azure/ai-services/content-understanding/service-limits#image). 


## How does Content Understanding process data? 

### Authenticate 

Content Understanding requires you to authenticate API access by using a Foundry Tools resource key or a Microsoft Entra ID token. Each request to the service URL must include an authentication header that validates access to your subscription. For more information, see [Authentication in Foundry Tools](/azure/ai-services/authentication?tabs=powershell).

### Secure data in transit 

All Foundry Tools endpoints use HTTPS to encrypt data in transit. The client operating system must support Transport Layer Security (TLS) 1.2 or 1.3. For more information, see [Transport Layer Security](/azure/ai-services/security-features?tabs=command-line%2Ccsharp#transport-layer-security-tls).

### Encrypt input data for processing

When you submit your files to a Content Understanding operation, it starts the process of analyzing the input. Your data and results are then temporarily encrypted and stored in Azure Storage in the same region as your Content Understanding resource before being sent to Azure OpenAI for further processing. While compute resources aren't dedicated per customer, requests are processed in logically isolated, sandboxed containers to ensure workload separation and prevent cross-tenant data exposure. 

### Data at rest and processing locations 

Content Understanding stores customer data at rest in the same region as the Content Understanding resource.

Processing locations depend on the type of operation:

- **Analyzers `prebuilt-read` and `prebuilt-layout` only**: You can control where data is processed on a per-request basis using the `processingLocation` parameter. You can select a geography (for example, Japan or United States), a data zone (for example, Europe or United States), or a global setting (any geography).
- **Content extraction (document, audio, and video)**: You bring your own LLM instance and capacity, which Content Understanding uses to process the data. Customer data might be processed outside the resource region based on the LLM deployment type you choose: geography (for example, Japan or United States), data zone (for example, Europe or United States), or global (any geography).

### Retrieve the results 

The **Get Result** operation uses the same authentication credentials as the **Analyze** operation to ensure no other customer can access your data. It returns the analysis job completion status. When the status is `Succeeded`, the operation also returns the extracted results in JSON format.

 

### Data retention 

Input documents and intermediate representations are written to secure Microsoft-managed storage only for the duration of processing and are deleted once the operation completes. Output results are retained for up to 24 hours to support asynchronous retrieval, after which they're automatically deleted. The analyzer name is logged for reporting and debugging.

 



### Face 

Face is a gated feature as it processes biometric data. The service detects faces in the input files and groups them by their similarity. The service doesn't persist any intermediate data beyond the processing of the request. The face groupings associated with analysis results persist for 48 hours unless the user explicitly deletes face data. For more information, see the [Data and Privacy for Face documentation](/azure/ai-foundry/responsible-ai/face/data-privacy-security).

### Labeled data for custom analyzers

A Content Understanding Studio project can use an associated, customer-owned Azure Storage account to hold labeled sample documents for custom analyzer training. How the built analyzer uses this data depends on the API version.

| API version | Labeled data behavior |
| --- | --- |
| `2025-11-01` | The built analyzer retains the labeled training data and uses it at analysis time. |
| `2026-06-01-preview` | Training distills information from the labeled samples into the built analyzer. The analyzer doesn't retain the labeled documents or require access to them at analysis time. |

### Azure OpenAI 

Content Understanding also uses an Azure OpenAI model after the underlying Foundry Tools process each modality input. For more information, see [Data, privacy, and security for Azure OpenAI](/azure/ai-foundry/responsible-ai/openai/data-privacy).
