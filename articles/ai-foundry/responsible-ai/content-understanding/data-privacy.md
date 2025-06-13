---
title: Data, privacy, and security for Content Understanding
titleSuffix: Azure AI services
description: This document details issues for data, privacy, and security for Content Understanding.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: article
ms.date: 11/17/2024
---

# Data, privacy, and security for Content Understanding 

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Content Understanding builds upon the functionality of Document Intelligence, Speech to Text, Image Analysis, Face, Video and Azure OpenAI, each designed with compliance, privacy, and security at its core. This combined service processes various types of customer-provided data, such as documents, audio, images, biometric data (face),text, and video to deliver powerful analysis and intelligence capabilities. Importantly, users are responsible for ensuring that their use of this service complies with all applicable laws and regulations in their jurisdiction, including data protection, privacy, and communications laws, as well as any specific requirements around biometric data when leveraging facial recognition features. It is essential to acquire all necessary permissions, licenses, or third-party rights for the content and data submitted for processing. 

Since the data processed in this integrated service may involve personal or sensitive information, including biometric identifiers and human speech content, users must follow all jurisdictional requirements related to data protection. For instance, when using biometric technologies, it is crucial to provide clear, conspicuous disclosure to individuals, particularly in regions with strict biometric data governance. Data provided to the Azure OpenAI service is stored and processed to monitor compliance with product terms, and [Microsoft’s Products and Services Data Protection Addendum](https://go.microsoft.com/fwlink/?linkid=2131539) applies to all data handling within the Azure OpenAI framework. By combining these technologies, our service offers robust insights while ensuring users maintain responsibility for adhering to legal and regulatory standards. 

## What data does Content Understanding process? 

Content Understanding can process audio input or voice audio, image files, document files and video files. Each input type has different file limits, such as file type, size, length and resolution. The limits are outlined in the [service quotas and limits documentation](/azure/ai-services/content-understanding/service-limits#image). 


## How does Content Understanding process data? 

### Authenticate 

Content Understanding first requires users to authenticate access to Content Understanding API by using Azure AI services API key. Each request to the service URL must include an authentication header. This header passes along an API key (or token if applicable), which is used to validate your subscription for a service. Apart from authenticating access with API Key, Content Understanding also supports AAD and Entra ID Authentication. For more information, see [Authenticate requests to Azure AI services](/azure/ai-services/authentication?tabs=powershell), which has additional information on AAD, Entra ID, and authorizing access to managed identities. 

### Secure data in transit 

All Azure AI services endpoints use HTTPS URLs for encrypting data during transit. The client operating system needs to support Transport Layer Security (TLS) 1.2 for calling the end points. For more information, see [Transport Layer Security](/azure/ai-services/security-features?tabs=command-line%2Ccsharp#transport-layer-security-tls). The incoming data is processed in the same region where the Azure resource was created. 

 

### Encrypts input data for processing 

The incoming data is processed in the same region where the Content Understanding resource was created. When you submit your files to a Content Understanding operation, it starts the process of analyzing the input. Your data and results are then temporarily encrypted and stored in Azure Storage before it is sent to Azure OpenAI for further processing. 

 

### Retrieve the results 

The "Get Result" operation is authenticated against the same API key that was used to call the "Analyze" operation to ensure no other customer can access your data. It returns the analysis job completion status, When the status shows as succeeded, the operation also returns the extracted results in JSON format. 

 

### Data retention 

For all the input, they are processed data as soon as possible, and the input files are not retained or stored in the service after processing. Analaysis result may be stored for up to 24 hours. The name of the analyzers will be logged for reporting and debugging. 

 

### Regional Process 

Data does not get stored outside the designated region that the user selected for the Content Understanding resource, even temporarily. However, based on OpenAI availability, we may route traffic to another region within the same geo moving forward. 

 

### Face 

Face is a gated feature as it processes biometric data. We detect faces in the input files and group them by their similarity. All intermediate data do not persist beyond the processing of the request. The face groupings associated with analysis results are persisted for 48 hours unless the user explicitly deletes face data. For more information, please refer to the [Data and Privacy for Face documentation](/azure/ai-foundry/responsible-ai/face/data-privacy-security). 

 

### Azure OpenAI 

Content Understanding also utilizes Azure OpenAI model once each modality input is processed through the underlying AI services. Please refer to the [Azure OpenAI Data, privacy, and security documentation](/azure/ai-foundry/responsible-ai/openai/data-privacy?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=azure-portal) for more information. 
