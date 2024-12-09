---
title: How to specify a detection model - Face
titleSuffix: Azure AI services
description: This article shows you how to choose which face detection model to use with your Azure AI Face application.
#services: cognitive-services
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.topic: how-to
ms.date: 06/10/2024
ms.author: pafarley
ms.devlang: csharp
ms.custom: devx-track-csharp
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Specify a face detection model

This guide shows you how to specify a face detection model for the Azure AI Face service.

The Face service uses machine learning models to perform operations on human faces in images. We continue to improve the accuracy of our models based on customer feedback and advances in research, and we deliver these improvements as model updates. Developers can specify which version of the face detection model they'd like to use; they can choose the model that best fits their use case.

Read on to learn how to specify the face detection model in certain face operations. The Face service uses face detection whenever it converts an image of a face into some other form of data.

If you aren't sure whether you should use the latest model, skip to the [Evaluate different models](#evaluate-different-models) section to evaluate the new model and compare results using your current data set.

## Prerequisites

You should be familiar with the concept of AI face detection. If you aren't, see the face detection conceptual guide or how-to guide:

* [Face detection concepts](../concept-face-detection.md)
* [Call the detect API](identity-detect-faces.md)


## Evaluate different models

The different face detection models are optimized for different tasks. See the following table for an overview of the differences.

| Model | Description | Performance notes | Landmarks |
|-------|-------------|-------------------|-----------|
|**detection_01** | Default choice for all face detection operations. | Not optimized for small, side-view, or blurry faces. | Returns face landmarks if they're specified in the detect call. |
|**detection_02** | Released in May 2019 and available optionally in all face detection operations. | Improved accuracy on small, side-view, and blurry faces. | Doesn't return face landmarks. |
|**detection_03** | Released in February 2021 and available optionally in all face detection operations. | Further improved accuracy, including on smaller faces (64x64 pixels) and rotated face orientations. | Returns face landmarks if they're specified in the detect call. |

Attributes are a set of features that can optionally be detected if they're specified in the detect call:

| Model | accessories | blur | exposure | glasses | headPose | mask | noise | occlusion | qualityForRecognition |
|-------|:-----------:|:----:|:--------:|:-------:|:--------:|:----:|:-----:|:---------:|:---------------------:|
|**detection_01** | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | | ✔️ | ✔️ | ✔️ (for recognition_03 or 04) |
|**detection_02** | | | | | | | | | |
|**detection_03** | | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | | ✔️ | ✔️ (for recognition_03 or 04) |

The best way to compare the performances of the detection models is to use them on a sample dataset. We recommend calling the [Detect] API on a variety of images, especially images of many faces or of faces that are difficult to see, using each detection model. Pay attention to the number of faces that each model returns.

## Detect faces with specified model

Face detection finds the bounding-box locations of human faces and identifies their visual landmarks. It extracts the face's features and stores them for later use in [recognition](../concept-face-recognition.md) operations.

When you use the [Detect] API, you can assign the model version with the `detectionModel` parameter. The available values are:

* `detection_01`
* `detection_02`
* `detection_03`

A request URL for the [Detect] REST API looks like this:

`https://westus.api.cognitive.microsoft.com/face/v1.0/detect?detectionModel={detectionModel}&recognitionModel={recognitionModel}&returnFaceId={returnFaceId}&returnFaceAttributes={returnFaceAttributes}&returnFaceLandmarks={returnFaceLandmarks}&returnRecognitionModel={returnRecognitionModel}&faceIdTimeToLive={faceIdTimeToLive}`

If you are using the client library, you can assign the value for `detectionModel` by passing in an appropriate string. If you leave it unassigned, the API uses the default model version (`detection_01`). See the following code example for the .NET client library.

```csharp
string imageUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg";
var response = await faceClient.DetectAsync(new Uri(imageUrl), FaceDetectionModel.Detection03, FaceRecognitionModel.Recognition04, returnFaceId: false, returnFaceLandmarks: false);
var faces = response.Value;
```

## Add face to Person with specified model

The Face service can extract face data from an image and associate it with a **Person** object through the [Add Person Group Person Face] API. In this API call, you can specify the detection model in the same way as in [Detect].

See the following .NET code example.

```csharp
// Create a PersonGroup and add a person with face detected by "detection_03" model
string personGroupId = "mypersongroupid";
using (var content = new ByteArrayContent(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(new Dictionary<string, object> { ["name"] = "My Person Group Name", ["recognitionModel"] = "recognition_04" }))))
{
    content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
    await httpClient.PutAsync($"{ENDPOINT}/face/v1.0/persongroups/{personGroupId}", content);
}

string? personId = null;
using (var content = new ByteArrayContent(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(new Dictionary<string, object> { ["name"] = "My Person Name" }))))
{
    content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
    using (var response = await httpClient.PostAsync($"{ENDPOINT}/face/v1.0/persongroups/{personGroupId}/persons", content))
    {
        string contentString = await response.Content.ReadAsStringAsync();
        personId = (string?)(JsonConvert.DeserializeObject<Dictionary<string, object>>(contentString)?["personId"]);
    }
}

string imageUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg";
using (var content = new ByteArrayContent(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(new Dictionary<string, object> { ["url"] = imageUrl }))))
{
    content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
    await httpClient.PostAsync($"{ENDPOINT}/face/v1.0/persongroups/{personGroupId}/persons/{personId}/persistedfaces?detectionModel=detection_03", content);
}
```

This code creates a **PersonGroup** with ID `mypersongroupid` and adds a **Person** to it. Then it adds a Face to this **Person** using the `detection_03` model. If you don't specify the *detectionModel* parameter, the API uses the default model, `detection_01`.

> [!NOTE]
> You don't need to use the same detection model for all faces in a **Person** object, and you don't need to use the same detection model when detecting new faces to compare with a **Person** object (in the [Identify From Person Group] API, for example).

## Add face to FaceList with specified model

You can also specify a detection model when you add a face to an existing **FaceList** object. See the following .NET code example.

```csharp
using (var content = new ByteArrayContent(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(new Dictionary<string, object> { ["name"] = "My face collection", ["recognitionModel"] = "recognition_04" }))))
{
    content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
    await httpClient.PutAsync($"{ENDPOINT}/face/v1.0/facelists/{faceListId}", content);
}

string imageUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg";
using (var content = new ByteArrayContent(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(new Dictionary<string, object> { ["url"] = imageUrl }))))
{
    content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
    await httpClient.PostAsync($"{ENDPOINT}/face/v1.0/facelists/{faceListId}/persistedfaces?detectionModel=detection_03", content);
}
```

This code creates a **FaceList** called `My face collection` and adds a Face to it with the `detection_03` model. If you don't specify the *detectionModel* parameter, the API uses the default model, `detection_01`.

> [!NOTE]
> You don't need to use the same detection model for all faces in a **FaceList** object, and you don't need to use the same detection model when detecting new faces to compare with a **FaceList** object.


## Next steps

In this article, you learned how to specify the detection model to use with different Face APIs. Next, follow a quickstart to get started with face detection and analysis.

* [Face .NET SDK](../quickstarts-sdk/identity-client-library.md?pivots=programming-language-csharp)
* [Face Python SDK](../quickstarts-sdk/identity-client-library.md?pivots=programming-language-python)
* [Face Java SDK](../quickstarts-sdk/identity-client-library.md?pivots=programming-language-java)
* [Face JavaScript SDK](../quickstarts-sdk/identity-client-library.md?pivots=programming-language-javascript)

[Detect]: /rest/api/face/face-detection-operations/detect
[Identify From Person Group]: /rest/api/face/face-recognition-operations/identify-from-person-group
[Add Person Group Person Face]: /rest/api/face/person-group-operations/add-person-group-person-face
