---
title: Azure Content Understanding in Foundry Tools face overview (preview)
titleSuffix: Foundry Tools
description: Learn about Azure Content Understanding in Foundry Tools face solutions.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025-understanding-refresh
  - build-2025
---

# Azure Content Understanding in Foundry Tools face solutions (preview)

> [!IMPORTANT]
> Azure Content Understanding in Foundry Tools is available in preview. Preview releases provide early access to features that are in active development.
>
> Features, approaches, and processes can change or have limited capabilities before general availability (GA).
>
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure Content Understanding provides a cloud-based solution for face detection, enrollment, and recognition, enabling secure and intelligent applications. Developers can apply these capabilities to detect faces, organize them into a structured directory, and perform recognition tasks for identity verification and content management.

This service is ideal for building secure access systems, streamlining photo management, or implementing intelligent attendance and check-in solutions. It supports both standalone face records and structured person identity management, providing flexibility for various real-world scenarios.

## Key benefits

Content Understanding offers face recognition capabilities for secure, scalable, and intelligent applications:

* **Comprehensive face intelligence**: Detect, enroll, and recognize faces using a unified cloud-based service. It supports both standalone face records and structured person identity management.
* **Adaptable and scalable for diverse scenarios**: Enable secure access, streamlined check-ins, customer recognition, and efficient photo management with rapid, accurate face searches across extensive collections.

## Business use cases

Content Understanding enables a wide range of real-world applications, including face detection, verification, identification, and large-scale content processing.

### Detect faces in images

Automatically detect faces in an image and return their bounding boxes. This capability simplifies tasks like highlighting, blurring, or counting faces without manual review. Common use cases include:

* Cropping detected faces for ID photos, albums, or personalized content.
* Blurring faces to ensure privacy before sharing images publicly.
* Counting people in event photos, crowd scenes, or security footage.

### Verify if two faces match

Compare a face in one image with another face or an enrolled person and determine if they belong to the same individual. This comparison feature is ideal for identity verification scenarios such as photo ID checks or sign-ins. Common use cases include:

* Verifying if a driver's selfie matches their profile photo.
* Confirming a student's identity before starting an online exam.
* Comparing a live photo with an uploaded ID for identity confirmation.

### Identify a person from their face

Match a face in a photo to a saved list of people and identify them. Common use cases include:

* Matching a patient's face to hospital records during check-in.
* Identifying a student or employee from their face photo.
* Recognizing someone from a watch list entering a secure area.

### Save faces for faster future searches

Index faces from images to enable quicker searches later without needing to reprocess the original content. This feature is especially useful for recurring search scenarios. Common use cases include:

* Extracting and saving faces from group photos at events to recognize returning participants in future sessions.
* Processing images from school activities or sports events to easily identify students or athletes in subsequent searches.
* Matching a theme park visitor's face to recent records to personalize their experience during repeat visits.

## Face capabilities

Content Understanding offers robust face capabilities, including detection, quality analysis, identity enrollment, and search. Central to these features is the **person directory**—a scalable, structured repository for managing persons and faces.

### Person Directory

The person directory is a flexible system for organizing face data and identity profiles. Key features include:

* **Face enrollment**: Add detected faces as standalone entries or associate them with specific persons.
* **Person enrollment**: Create identity records that link to one or more enrolled faces.
* **Metadata management**: Update metadata, apply tags, and manage relationships between persons and faces.
* **Dynamic associations**: Associate or disassociate faces from persons without losing data, ensuring clean and maintainable identity management.

:::image type="content" source="../media/face/person-directory-overview.png" alt-text="Diagram illustrating the flow of the person directory.":::

### Search capabilities

The person directory enables powerful search and matching functionalities:

* **Identify candidate persons**: Match an input face to candidate persons in the directory.
* **Find similar faces**: Search for similar faces across the entire directory.



## Data, privacy, and security

Azure Content Understanding adheres to Microsoft's strict policies on customer data protection and privacy. Developers should review these policies to ensure compliance and understand how data is handled. For more details, visit the [Data, privacy, and security](/azure/ai-foundry/responsible-ai/content-understanding/data-privacy) page.

## Related content

* Learn how to build a [**person directory**](../tutorial/build-person-directory.md) (preview).
* Review code sample: [**person directory**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/notebooks).
