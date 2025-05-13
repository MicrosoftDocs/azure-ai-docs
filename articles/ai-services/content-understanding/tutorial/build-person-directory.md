---
title: Build a person directory with Azure AI Content Understanding Face APIs
titleSuffix: Azure AI services
description: Learn to build a person directory with Content Understanding Face APIs
author: lajanuar
ms.author: quentinm
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: tutorial
ms.date: 05/07/2025
---

# Tutorial: Build a person directory
A Person Directory is a structured way to store face data for recognition tasks. You can add individual faces to the directory and later search for visually similar faces. You can also create person profiles, associate faces to them, and match new face images to known individuals. This setup supports both flexible face matching and identity recognition across images and videos.

:::image type="content" source="../media/face/person-directory-processes.png" alt-text="Diagraom of the person directory enrollment and search processes.":::

## Data storage recommendation
It is recommended to store all face images in Azure Blob Storage for secure and scalable access. Face URLs in your API calls should point to these stored images.

## Enroll

Enrollment comprises:
* Create an empty person directory.
* Add persons.
* Add faces and associate with a person.

### Step 1: Create an empty person directory
Create a new directory to store faces and persons.

**Sample request**

PUT {endpoint}/contentunderstanding/personDirectories/{personDirectoryId}?api-version=2025-05-01-preview
Content-Type: application/json

```json
{
  "description": "...",
  "tags": { ... },
}
```
---

* The `personDirectoryId` is user-defined and should be unique within the system.

### Step 2: (Optional) Add persons
If you want to recognize or manage individuals, create a person first. You can later associate faces to this person.

**Sample request**

POST {endpoint}/contentunderstanding/personDirectories/{personDirectoryId}/persons?api-version=2025-05-01-preview
Content-Type: application/json

```json
{
  "tags": {
    "name": "Alice",
    "age": "20"
  }
}
```
---

* The `personDirectoryId` must match the one created in Step 1.
* The API returns a `personId`.

### Step 3: Add faces (Optional: Associate with a person)
Add a face to the directory. You can either associate it to an existing person or leave it as a standalone face. The API accepts either an image URL or base64-encoded image data.

**Sample request**

POST {endpoint}/contentunderstanding/personDirectories/{personDirectoryId}/faces?api-version=2025-05-01-preview
Content-Type: application/json

```json
{
  "faceSource": {
    "url": "https://mystorageaccount.blob.core.windows.net/images/container1/file1.jpg",
    "base64": "<base64 data>",
    "targetBoundingBox": [l, t, w, h], // Optional
    "imageReferenceId": "file1.jpg" // Optional, user-provided 
  },
  "qualityThreshold": "medium", // Optional, default is "medium",
  "personId": "{personId}"  // Optional — associate to existing person if needed
}
```
---

* The `personDirectoryId` must match the one created in Step 1.
* The `personId` is a person identifier obtained from Step 2.
* Each face entry requires a url (file path) referencing an image stored in the Blob Storage container.
* The `targetBoundingBox` field (optional) provides bounding box coordinates ([`left, top, width, height`]) to specify the face location. > If no `targetBoundingBox`, the API automatically detects and uses the largest face in the image.
* `qualityThreshold` (optional) allows filtering of face quality (low, medium, or high). The default is medium, meaning only medium or high-quality faces are stored; low-quality faces are rejected.
* `imageReferenceId` (optional) allows users to provide a reference ID for the image. It is recommended to use this field to store the actual image path for future use or mapping.
* The API returns a `faceId`.

## Search
After building your person directory with face images and optional person associations, you can use it to you can use it to perform face recognition from images or videos.

### Image input
Identify persons or find similar faces in an image.

#### Search within persons
Identify the most likely person candidates by comparing the input face against enrolled persons.

**Sample request**

POST {endpoint}/contentunderstanding/personDirectory/{personDirectoryId}/persons:identify?api-version=2025-05-01-preview
Content-Type: application/json

```json
{
  "faceSource": {
  	"url": "https://mystorageaccount.blob.core.windows.net/images/container1/file.jpg",   
    "targetBoundingBox": [l,t,w,h]
  }
}
```
---

**Sample response**

```json
{
   "detectedFace": {
    "boundingBox": [ ... ]  // The bounding box of the input face used for identification
  },    
  "personCandidates": [
    {
      "personId": "{personId1}",
      "tags": {
        "name": "Alice",
        "age": "20"
      },
      "confidence": 0.92
    }
  ]
}
```
---

#### Search within faces
Find visually similar individual faces from all stored face entries.

**Sample request**

POST {endpoint}/personDirectory/{personDirectoryId}/faces:find?api-version=2025-05-01-preview
Content-Type: application/json

```json
{
  "faceSource": {
  	"url": "https://mystorageaccount.blob.core.windows.net/images/container1/file.jpg",   
    "targetBoundingBox": [l,t,w,h] // Optional
  }
  "maxSimilarFaces": 10   // Optional, default is 1000, max allowed is 1000
}
```
---

**Sample response**

```json
{
   "detectedFace": {
     "boundingBox": [ ... ]
   }, 
  "similarFaces": [
   {
	 "faceId": "{faceId}"
     "boundingBox": {'left': l, 'top': t, 'width': w, 'height': h},
     "confidence": 0.92,
     "imageReferenceId": "file1.jpg" 
   }
  ], ...
}
```
---

### Video input
Identify people appearing in video content. See: [Azure AI Content Understanding video solutions (preview)](../video/overview.md)


## Next steps