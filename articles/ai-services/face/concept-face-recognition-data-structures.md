---
title: "Face recognition data structures - Face"
titleSuffix: Foundry Tools
description: Learn about the Face recognition data structures, which store data on faces and persons.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.update-cycle: 90-days
ms.topic: concept-article
ms.date: 01/30/2026
ms.author: pafarley
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Face recognition data structures

This article explains the data structures used in the Face service for face recognition operations. These data structures hold data on faces and persons.

[!INCLUDE [Gate notice](./includes/identity-gate-notice.md)]

## Data structures used with Identify 

The Face Identify API uses container data structures to the hold face recognition data in the form of **Person** objects. There are three types of containers for this purpose, listed from oldest to newest. We recommend you always use the newest one. 

### PersonGroup 

**PersonGroup** is the smallest container data structure.
- You need to specify a recognition model when you create a **PersonGroup**. When any faces are added to that **PersonGroup**, it uses that model to process them. This model must match the model version with Face ID from detect API.
- You must call the Train API to make any new face data reflect in the Identify API results. This includes adding/removing faces and adding/removing persons.
- For the free tier subscription, it can hold up to 1,000 Persons. For S0 paid subscription, it can have up to 10,000 Persons.  

 **PersonGroupPerson** represents a person to be identified. It can hold up to 248 faces.

### Large Person Group 

**LargePersonGroup** is a later data structure introduced to support up to 1 million entities (for S0 tier subscription). It is optimized to support large-scale data. It shares most of **PersonGroup** features: A recognition model needs to be specified at creation time, and the Train API must be called before use.



### Person Directory 

**PersonDirectory** is the newest data structure of this kind. It supports a larger scale and higher accuracy. Each Azure Face resource has a single default **PersonDirectory** data structure. It's a flat list of **PersonDirectoryPerson** objects - it can hold up to 20 million.

**PersonDirectoryPerson** represents a person to be identified. Based on the older **PersonGroupPerson** model, it allows you to add faces from different recognition models to the same person. However, the Identify operation can only match faces obtained with the same recognition model. 

**DynamicPersonGroup** is a lightweight data structure that allows you to dynamically reference a **PersonDirectoryPerson**. It doesn't require the Train operation: once the data is updated, it's ready to be used with the Identify API.

You can also use an **in-place person ID list** for the Identify operation. This lets you specify a more narrow group to identify from. You can do this manually to improve identification performance in large groups. 

The above data structures can be used together. For example: 
- In an access control system, The **PersonDirectory** might represent all employees of a company, but a smaller **DynamicPersonGroup** could represent just the employees that have access to a single floor of the building.
- In a flight onboarding system, the **PersonDirectory** could represent all customers of the airline company, but the **DynamicPersonGroup** represents just the passengers on a particular flight. An **in-place person ID list** could represent the passengers who made a last-minute change.

For more details, please refer to the [PersonDirectory how-to guide](./how-to/use-persondirectory.md). A quick comparison between **LargePersonGroup** and **PersonDirectory**:

| Detail | LargePersonGroup | PersonDirectory |
| --- | --- | --- |
| Capacity | A **LargePersonGroup** can hold up to 1 million **PersonGroupPerson** objects. | The collection can store up to 20 millions **PersonDirectoryPerson** identities. |
| PersonURI | `/largepersongroups/{groupId}/persons/{personId}` | `(/v1.0-preview-or-above)/persons/{personId}` |
| Ownership | The **PersonGroupPerson** objects are exclusively owned by the **LargePersonGroup** they belong to. If you want a same identity kept in multiple groups, you'll have to [Create Large Person Group Person](/rest/api/face/person-group-operations/create-large-person-group-person) and [Add Large Person Group Person Face](/rest/api/face/person-group-operations/add-large-person-group-person-face) for each group individually, ending up with a set of person IDs in several groups. | The **PersonDirectoryPerson** objects are directly stored inside the **PersonDirectory**, as a flat list. You can use an in-place person ID list to [Identify From Person Directory](/rest/api/face/face-recognition-operations/identify-from-person-directory), or optionally [Create Dynamic Person Group](/rest/api/face/person-directory-operations/create-dynamic-person-group) and hybridly include a person into the group. A created **PersonDirectoryPerson** object can be referenced by multiple **DynamicPersonGroup** without duplication. |
| Model | The recognition model is determined by the **LargePersonGroup**. New faces for all **PersonGroupPerson** objects become associated with this model when they're added to it. | The **PersonDirectoryPerson** object prepares separated storage per recognition model. You can specify the model when you add new faces, but the Identify API can only match faces obtained with the same recognition model, that is associated with the query faces. |
| Training | You must call the Train API to make any new face/person data reflect in the Identify API results. | There's no need to make Train calls, but API such as [Add Person Face](/rest/api/face/person-directory-operations/add-person-face) becomes a long running operation, which means you should use the response header "Operation-Location" to check if the update completes. |
| Cleanup | [Delete Large Person Group](/rest/api/face/person-group-operations/delete-large-person-group) will also delete the all the **PersonGroupPerson** objects it holds, along with their face data. | [Delete Dynamic Person Group](/rest/api/face/person-directory-operations/delete-dynamic-person-group) will only unreference the **PersonDirectoryPerson**. To delete actual person and the face data, see [Delete Person](/rest/api/face/person-directory-operations/delete-person). |


## Data structures used with Find Similar 

Unlike the Identify API, the Find Similar API is used in applications where the enrollment of a **Person** is hard to set up (for example, face images captured from video analysis, or from a photo album analysis).

### FaceList 

**FaceList** represents a flat list of persisted faces. It can hold up 1,000 faces.

### LargeFaceList 

**LargeFaceList** is a later version which can hold up to 1,000,000 faces.

## Next step

Now that you're familiar with the face data structures, write a script that uses them in the Identify operation.

> [!div class="nextstepaction"]
> [Face quickstart](./quickstarts-sdk/identity-client-library.md)
