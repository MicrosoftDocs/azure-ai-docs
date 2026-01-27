---
title: Data and privacy for custom NER
titleSuffix: Foundry Tools
description: Data and privacy for custom named entity recognition
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 09/29/2021
---

# Data and privacy for custom named entity recognition

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

This article provides some high-level details regarding how data is processed by custom named entity recognition (NER). You're responsible for how you use and implement this technology, including complying with all laws and regulations that apply to you. For example, it's your responsibility to:

* Understand where your data is processed and stored by the custom NER service in order to meet regulatory obligations for your application.
    
* Ensure that you have all necessary licenses, proprietary rights, or other permissions required to the content in your dataset that is used as the basis for building your custom NER models and for your content evaluated upon deployment or use of custom NER in production.


## What data does custom NER process?

Custom NER processes the following data:

* **User’s dataset and tags file:** As a prerequisite to creating a custom NER project, users need to upload their dataset to their Azure Blob Storage container. A *tags file* is a [JSON-formatted file](/azure/ai-services/language-service/custom-named-entity-recognition/concepts/data-formats#json-file-format) that contains a reference to the user’s tagged entities. A *user’s dataset* includes train and test sets, which developers can predefine in the tags file, or which can be chosen at random during training. The train set and the tags file are processed during training to create the custom NER model. The test set is processed by the trained model later, to evaluate its performance.

* **Custom NER models:** Based on the user's request to train the model, custom NER processes the provided tagged data to output a trained model. The user can choose to train a new model or overwrite an existing one. The trained model is then stored on the service’s side and used for processing the model evaluation. After the developer is content with the model’s performance, they request to deploy the model for use. The deployed model will also be stored on the service’s side, which is used to process the user’s requests for prediction through the Analyze API.

* **Data sent for extraction:** This is the user's text, sent from a client application through [Analyze API](https://aka.ms/ct-runtime-swagger), to be processed for entity extraction by the custom NER model. Output of the processed data contains the extracted entities and their confidence scores. This is returned to the client’s application to perform an action to fulfill the user's request.

User's data uploaded for training, testing or extracting is customer data.  Custom NER does not use customer data to improve its general machine-learned models for product improvement purposes. We use aggregate telemetry, such as which APIs are used and the number of calls from each subscription and resource, for service monitoring purposes.

## How does custom NER process data?

The following diagram illustrates how your data is processed.

![Diagram that shows how data is processed.](media\custom-named-entity-recognition-rai-privacy-chart.png)

## How is data retained, and what customer controls are available?

Custom NER is a data processor for GDPR purposes. In compliance with GDPR policies, custom NER users have full control to view, export, or delete any customer data. Users can perform these actions either through [Language Studio](https://aka.ms/languageStudio), or programmatically by using Language APIs.  

Your data is only stored in your Azure storage account. Custom NER only has access to read from it during training and evaluation. Custom NER doesn't log or store any data sent by the customer for extraction tasks through the prediction API.

Customer controls include:

* Tagged data, provided by the user as a prerequisite to train the model, is saved in the customer’s Azure storage account that's connected to the project during creation. Customers can edit or remove tags whenever they want through the Language studio.

* Custom NER project metadata is stored on the service’s side, until the customer deletes the project. When you create your project, you fill in the metadata fields, such as the project name, description, language, the name of connected blob container, and the tags file location.

* Trained custom NER models are stored in the service’s Azure storage accounts until the customer deletes them. Models are overridden each time the user retrains them.

* Deployed custom NER models persist in the service’s Azure storage accounts until the customer deletes the deployment or deletes the model itself. The model is overridden each time the user deploys to the same deployment name.

## Security for customers' data

Azure services are implemented while maintaining appropriate technical and organizational measures to protect customer data in the cloud.

To learn about Microsoft's security commitments, see the [Microsoft Trust Center](https://www.microsoft.com/trust-center).


## Next steps

* [Introduction to custom NER](/azure/ai-services/language-service/custom-named-entity-recognition/overview)

* [Custom NER transparency note](custom-named-entity-recognition-transparency-note.md)

* [Guidance for integration and responsible use](custom-named-entity-recognition-guidance-integration-responsible-use.md)

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai?rtc=1&activetab=pivot1%3aprimaryr6)
