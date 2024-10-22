---
title: Quickstart:Azure AI Multimodal Intelligence REST APIs
titleSuffix: Azure AI services
description: Learn about Multimodal Intelligence REST APIs
author: tonyeiyalla
ms.author: tonyeiyalla
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 10/22/2024
---

# Quickstart: Azure AI Multimodal Intelligence REST APIs
Get started with the Azure AI MMI REST API or client libraries. The API provides you with AI algorithms for extracting content and data from images, videos, audios and documents and returning it as structured data. Follow these steps to install a package to your application and try out the sample code.

### Prerequisites
1.	You need an active Azure subscription. If you don't have an Azure subscription, you can [**create one for free**]().
2.	Once you have your Azure subscription, create an [**AI service resource**]() from the Azure portal home page. The Azure AI services multi-service resource is listed under Azure AI services → Azure AI services in the portal as shown here:
 :::image type="content" source="media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the multi-service resource page in the Azure portal.":::
  
    > [!IMPORTANT]
    > Azure provides more than one resource types named Azure AI services. Be sure to select the one that is listed under Azure AI services → Azure AI services with the logo as shown previously.
3.	After your resource deploys, select Go to resource and retrieve your key and endpoint. The Keys & Endpoint section can be found in the Resource Management section. 
4.	Copy one of the keys and your endpoint for use later in the Quickstart. 
5.	[**cURL**]() installed

# Analyze a document
A POST request is used to analyze all document types. A GET request is used to retrieve the result of a document analysis. The analyzerId is used with POST and resultId with GET operations.

# Analyze document (POST Request)
1.	Copy the following curl command into a text editor:
    > curl -v -i POST "{endpoint}/multimodalintelligence/analyzers/{analyzerId}:analyze?api-version=2024-12-01-preview" -H "Content-Type: application/json" -H "Ocp-Apim-Subscription-Key: {key}" --data-ascii "{'urlSource': '{your-document-url}'}"
2.	Make the following changes in the command where needed:
*	Replace {endpoint} with the endpoint value from your Azure portal AI service resource instance.
*	Replace {key} with the key value from your Azure portal AI Service resource instance.
3.	Open a command prompt window.
4.	Past your edited curl command from the text editor into the command prompt window, and then run the command.
5.	Using the following table as a reference, replace {analyzerID} and {your-document-url} with your desired values.
6.	You need a document file at a URL. For this quickstart, you can use the sample forms provided in the following table for each feature:

|Feature|{analyzerID}| {document-url}|
|--------|-------|-------|
|Audio|||
|Video|||
|Document|||
|Image|||
# Get analyze results (GET Request)
Call the Get analyze result API to get the status of the operation and the extracted data. 

### GET Request
> curl -v -X GET "{endpoint}/multimodalintelligence/analyzers/{analyzerId}/results/{resultId}api-version=2024-12-01-preview" -H "Ocp-Apim-Subscription-Key: {key}"

### Examine the response
You receive a 200 (Success) response with JSON output. The first field, "status", indicates the status of the operation. If the operation isn't complete, the value of "status" is "running" or "notStarted", and you should call the API again, either manually or through a script. We recommend an interval of one second or more between calls.

### Sample response
{
  "fileType": "pdf",
  "documents": [
    {
      // Generic properties
      "documentId": "myFile.pdf",
      "kind": "visualDocument",
      // Content representation
      "content": "{markdown representation of document}",

      // Semantic field extraction
      "type": "invoice",
      "confidence": 0.95,
      "fields": {
        "VendorName": {
          "type": "string",
          "content": "Contoso",
          "value": "Contoso",
          "spans": [ { "offset": 10, "length", 7 } ],
          "confidence": 0.98,
          "groundings": [ "VD({pageNumber}:{x1},{y1},{x2},{y2},{x3},{y3},{x4},{y4})" ]
        }
      },
    }
  ]
}
