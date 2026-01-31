---
title: Build a person directory with Azure Content Understanding in Foundry Tools Face APIs (preview)
titleSuffix: Foundry Tools
description: Learn how to build a person directory with Content Understanding Face APIs.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: tutorial
ms.custom:
  - build-2025
---

# Tutorial: Build a person directory (preview)

A person directory provides a structured approach to storing face data for recognition tasks. It allows you to add individual faces, search for visually similar faces, and create person profiles. You can associate faces with these profiles and match new face images to known individuals. This setup supports both flexible face matching and identity recognition across images and videos.

:::image type="content" source="../media/face/person-directory-enrollment.jpg" lightbox="../media/face/person-directory-enrollment.jpg" alt-text="Diagram illustrating the processes of enrollment and search in a person directory.":::

## Data storage recommendation

For secure and scalable access, store face images in Azure Blob Storage. When you make API calls, make sure the face URLs reference those stored images.

## Enrollment

Enrollment involves the following steps:

1. [Create an empty person directory](#create-an-empty-person-directory)
1. [Add persons](#add-persons)
1. [Add faces and associate them with a person](#add-faces-and-associate-with-a-person)
  
### Create an empty person directory

To create a new person directory, send a `PUT` request to the API endpoint. This directory serves as the container for storing faces and associated persons.

```http
PUT {endpoint}/contentunderstanding/personDirectories/{personDirectoryId}?api-version=2025-05-01-preview
Content-Type: application/json

{
  "description": "A brief description of the directory",
  "tags": {
    "project": "example-project",
    "owner": "team-name"
  }
}
```

* `personDirectoryId`: A unique, user-defined identifier for the directory within the resource.
* `description`: (Optional) A short description of the directory's purpose.
* `tags`: (Optional) Key-value pairs to help organize and manage the directory.

The API creates the directory and returns a confirmation response.

```json
200 OK

{
  "personDirectoryId": "{personDirectoryId}",
  "description": "A brief description of the directory",
  "createdAt": "2025-05-01T18:46:36.051Z",
  "lastModifiedAt": "2025-05-01T18:46:36.051Z",
  "tags": {
    "project": "example-project",
    "owner": "team-name"
  },
  "personCount": 0,
  "faceCount": 0
}
```

### Add persons

To recognize or manage individuals, you need to create a person profile. Once created, you can associate faces with this person.

```http
POST {endpoint}/contentunderstanding/personDirectories/{personDirectoryId}/persons?api-version=2025-05-01-preview
Content-Type: application/json

{
  "tags": {
    "name": "Alice",
    "employeeId": "E12345"
  }
}
```

* `personDirectoryId`: The unique identifier of the directory created in Step 1.
* `tags`: Key-value pairs to describe the person, such as their name or age.

The API returns a `personId` that uniquely identifies the created person.

```json
200 OK

{
  "personId": "4f66b612-e57d-4d17-9ef7-b951aea2cf0f",
  "tags": {
    "name": "Alice",
    "employeeId": "E12345"
  }
}
```

### Add faces and associate with a person

You can add a face to the directory and optionally associate it with an existing person. The API supports both image URLs and base64-encoded image data.

```http
POST {endpoint}/contentunderstanding/personDirectories/{personDirectoryId}/faces?api-version=2025-05-01-preview
Content-Type: application/json

{
  "faceSource": {
    "url": "https://mystorageaccount.blob.core.windows.net/container/face.jpg",
    // "data": "<base64 data>",
    "imageReferenceId": "face.jpg",
    "targetBoundingBox": {
      "left": 33,
      "top": 73,
      "width": 262,
      "height": 324
    }
  },
  "qualityThreshold": "medium",
  "personId": "{personId}"
}
```

- `personDirectoryId`: The unique identifier of the person directory created in Step 1.
- `faceSource`: Specifies the face image.
  - `url`: The file path of the image stored in Azure Blob Storage.
  - `data`: Base64-encoded image data as optional alternative to `url`.
  - `imageReferenceId`: (Optional) A user-defined identifier for the image. This identifier can be helpful for tracking the image's origin or for mapping it to other data.
  - `targetBoundingBox`: (Optional) Approximate location of the face in the image. If omitted, the API detects and uses the largest face.
- `qualityThreshold`: (Optional) Filters face quality (`low`, `medium`, or `high`). The default is `medium`, meaning only medium or high-quality faces are stored. Lower quality faces are rejected.
- `personId`: (Optional) The `personId` of an existing person to associate the face with.

The API returns a `faceId` that uniquely identifies the created face with the detected `boundingBox` of the face.

```json
{
  "faceId": "{faceId}",
  "personId": "{personId}",
  "imageReferenceId": "face.jpg",
  "boundingBox": {
    "left": 30,
    "top": 78,
    "width": 251,
    "height": 309
  }
}
```

## Use the person directory

After creating your person directory and adding face images with optional person associations, you can perform two key tasks:

1. **[Identify a person](#identify-a-person)**: Match a face image against enrolled persons in the directory and determine the most likely identity.
1. **[Find similar faces](#find-similar-faces)**: Search for visually similar faces across all stored face entries in the directory.

These capabilities enable robust face recognition and similarity matching for various applications.

:::image type="content" source="../media/face/person-directory-search.png" lightbox="../media/face/person-directory-search.png" alt-text="Diagram illustrating the processes of search in a person directory.":::

### Identify a person

Identify the most likely person matches by comparing the input face against enrolled persons in the directory.

```http
POST {endpoint}/contentunderstanding/personDirectory/{personDirectoryId}/persons:identify?api-version=2025-05-01-preview
Content-Type: application/json

{
  "faceSource": {
    "url": "https://mystorageaccount.blob.core.windows.net/container/unknown.jpg",
    "targetBoundingBox": { ... }
  },
  "maxPersonCandidates": 1
}
```

- `faceSource.url`: The URL of the input face image stored in Azure Blob Storage.
- `faceSource.targetBoundingBox`: (Optional) The approximate bounding box of the face in the image. If omitted, the API detects the largest face.
- `maxPersonCandidates`: (Optional) The maximum number of person candidates to return. Default is 1.

The API returns the detected bounding box of the face along with the top person candidates.

```json
{
  "detectedFace": {
    "boundingBox": { ... }
  },
  "personCandidates": [
    {
      "personId": "{personId1}",
      "tags": {
        "name": "Alice",
        "employeeId": "E12345"
      },
      "confidence": 0.92
    }
  ]
}
```

- `detectedFace.boundingBox`: The bounding box of the detected face in the input image.
- `personCandidates`: A list of potential matches, each with a `personId`, associated `tags`, and a `confidence` score indicating the likelihood of a match.

### Find similar faces

Find visually similar faces from all stored face entries in the directory.

```http
POST {endpoint}/personDirectory/{personDirectoryId}/faces:find?api-version=2025-05-01-preview
Content-Type: application/json

{
  "faceSource": {
    "url": "https://mystorageaccount.blob.core.windows.net/container/target.jpg",
    "targetBoundingBox": { ... }
  },
  "maxSimilarFaces": 10
}
```

- `faceSource.url`: The URL of the input face image stored in Azure Blob Storage.
- `faceSource.targetBoundingBox`: (Optional) The approximate bounding box of the face in the image. If omitted, the API detects the largest face.
- `maxSimilarFaces`: (Optional) The maximum number of similar faces to return. Defaults to 1000, with a maximum limit of 1000.

The API returns the detected bounding box of the face along with the most similar faces from the directory.

```json
{
  "detectedFace": {
    "boundingBox": { ... }
  },
  "similarFaces": [
    {
      "faceId": "{faceId}",
      "boundingBox": { ... },
      "confidence": 0.92,
      "imageReferenceId": "face.jpg"
    }
  ]
}
```

- `detectedFace.boundingBox`: The bounding box of the detected face in the input image.
- `similarFaces`: A list of similar faces, each with a `faceId`, `boundingBox`, `confidence` score, and an `imageReferenceId` indicating the source image.


## Next step

Explore how to identify individuals in video content using the [Azure Content Understanding in Foundry Tools video solutions (preview)](../video/overview.md).
