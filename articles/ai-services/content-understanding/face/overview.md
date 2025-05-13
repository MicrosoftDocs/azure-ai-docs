---
title: Azure AI Content Understanding face overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding face solutions.
author: lajanuar
ms.author: quentinm
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 05/07/2025
ms.custom: build-2025-understanding-refresh
---

# Azure AI Content Understanding face solutions (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure AI Content Understanding offers cloud-based face detection, enrollment, and recognition services to enable secure and intelligent applications. It allows developers to detect faces, enroll persons and faces into a structured directory, and perform face recognition tasks for identity verification and content management.

Whether you're building a secure access system, enhancing photo management, or creating intelligent attendance or check-in solutions, Content Understanding supports both individual face records and structured person identity management.

## Business use cases

Content Understanding enables various real-world applications across detection verification, identification, and large-scale content processing scenarios.

**Find faces in images**: Automatically detect faces in an image and return the bounding boxes of each detected face. It helps customers find, highlight, blur, or count faces without manually reviewing every photo. Common applications:
* Crop detected faces for ID photos, albums, or personalization.
* Blur faces to protect privacy before sharing images publicly.
* Count the number of people in event photos, crowds, or security footage.

**Check if two faces match**: Compare a face in an image with either another face image or an enrolled person to see if they belong to the same individual. Useful for confirming identity in scenarios like photo ID checks, sign-ins, or verifying someone against a known profile. Common applications:
* Check if a driver’s selfie matches their profile photo.
* Confirm a student’s face before starting an online exam.
* Compare a live photo with an uploaded ID to confirm identity.

**Find out who the person is from their face**: Look at a face in a photo and check if it matches someone in your saved list of people. Useful when you want to find out who someone is without needing their name, ID, or other input. Common applications:
* Match a patient’s face to hospital records during check-in.
* Look up a student or employee from their face photo.
* Spot someone from a watchlist entering a secure area.

## Face capabilities

Our system provides comprehensive face capabilities, from detection and quality analysis to identity enrollment and search. At the core of these capabilities is the Person Directory—a scalable and structured container for managing Persons and Faces.

### Person Directory

The Person Directory is designed to store and organize face data and identity profiles. It supports:
* **Face enrollment**: Add detected faces either as standalone entries or associate them to specific persons.
* **Person enrollment**: Create identity records that can be associated with one or more enrolled faces.
* **Metadata management**: Update Face/Person metadata, modify tags, and manage associations between Persons and Faces.
* **Flexible association**: Faces can be associated or disassociated from Persons without data loss, supporting clean, maintainable identity management.

:::image type="content" source="../media/face/person-directory-overview.png" alt-text="Diagram of person directory flow.":::

### Search capabilities

Once enrolled, both Persons and Faces within the Person Directory can be searched and matched:
* **Identify within Persons**: Match the input face against identities represented by Persons (aggregated face vectors).
* **Find similar within Faces**: Find the most similar individual faces across the entire Person Directory.

## Key benefits

Azure AI Content Understanding Face delivers powerful face capabilities designed for secure, scalable, and intelligent applications:
* **End-to-end face intelligence**: Detect, enroll, and recognize faces using a cloud-based service that supports both standalone face records and structured person identity management—all in one unified platform.
* **Flexible and scalable for real-world scenarios**: Supports secure access, check-ins, customer recognition, and photo management with fast, accurate face searching across large collections.

## Input requirements

We support multiple input file formats, including BMP, JPEG, PNG, WebP, ICO, and GIF. You can provide the image input in either of the following forms:
* **Base64-encoded string**: The image must be provided as a Base64 string (not a byte array). Learn more about [converting to Base64](https://learn.microsoft.com/en-us/dotnet/api/system.convert.tobase64string?view=net-9.0)
* **Image URL**: You can provide a publicly accessible URL pointing to the image. This can be:
    * A URL from Azure Blob Storage with a valid SAS token. Learn how to Create SAS tokens for Azure Blob Storage.
    * A custom domain URL that supports direct access to the image.

## Supported regions

For a detailed list of supported languages and regions, visit our [Language and region support](../language-region-support.md) page.

## Data privacy and security

As with all the Azure AI services, developers using the Content Understanding service should be aware of Microsoft's policies on customer data. See our [Data, protection and privacy](https://www.microsoft.com/trust-center/privacy) page to learn more.

## Next steps

* Learn to build a [**person directory**](../quickstart/use-ai-foundry.md).
* Review code sample: [**person directory**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/zhizho/face/notebooks/face).