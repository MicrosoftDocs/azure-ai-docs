---
title: "Find similar faces using Foundry Tools"
titleSuffix: Foundry Tools
description: Learn how to use the Azure Face service to find similar faces in a set of images, performing face search by image for various applications.
#customer intent: As a developer, I want to find similar faces in images so that I can perform face recognition tasks.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.update-cycle: 90-days
ms.topic: how-to
ms.date: 01/30/2026
ms.author: pafarley
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Find similar faces

[!INCLUDE [Gate notice](../includes/identity-gate-notice.md)]

The [Find Similar](/rest/api/face/face-recognition-operations/find-similar) operation does face matching between a target face and a set of candidate faces, finding a smaller set of faces that look similar to the target face. This is useful for doing a face search by image.

This guide demonstrates how to use the Find Similar feature in the different language SDKs. The following sample code assumes you have already authenticated a Face client object. For details on how to do this, follow a [quickstart](../quickstarts-sdk/identity-client-library.md).


## Detect faces for comparison

You need to detect faces in images before you can compare them. In this guide, the following remote image, called *findsimilar.jpg*, will be used as the source:

![Photo of a man who is smiling.](../media/quickstarts/find-similar.jpg) 

#### [C#](#tab/csharp)

This guide uses remote images that are accessed by URL. Save a reference to the base URL string. All of the images accessed in this guide are located at that URL path.

```csharp
string baseUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/";
```

The following face detection method is optimized for comparison operations. It doesn't extract detailed face attributes, and it uses an optimized recognition model.

[!Code-csharp[](~/cognitive-services-quickstart-code/dotnet/Face/FindSimilar.cs?name=snippet_face_detect_recognize)]

The following code uses the above method to get face data from a series of images.

[!Code-csharp[](~/cognitive-services-quickstart-code/dotnet/Face/FindSimilar.cs?name=snippet_loadfaces)]


#### [REST API](#tab/rest)

Copy the following cURL command and insert your key and endpoint where appropriate. Then run the command to detect one of the target faces.

:::code language="shell" source="~/cognitive-services-quickstart-code/curl/face/detect.sh" ID="detect_for_similar":::

Find the `"faceId"` value in the JSON response and save it to a temporary location. Then, call the above command again for these other image URLs, and save their face IDs as well. You'll use these IDs as the target group of faces from which to find a similar face.

:::code source="~/cognitive-services-quickstart-code/curl/face/detect.sh" ID="similar_group":::

Finally, detect the single source face that you'll use for matching, and save its ID. Keep this ID separate from the others.

:::code source="~/cognitive-services-quickstart-code/curl/face/detect.sh" ID="similar_matcher":::

---

## Find and print matches

In this guide, the face detected in the *Family1-Dad1.jpg* image should be returned as the face that's similar to the source image face.

![Photo of a man who is smiling; this is the same person as the previous image.](../media/quickstarts/family-1-dad-1.jpg)

#### [C#](#tab/csharp)

The following code calls the Find Similar API on the saved list of faces.

[!Code-csharp[](~/cognitive-services-quickstart-code/dotnet/Face/FindSimilar.cs?name=snippet_find_similar)]

The following code prints the match details to the console:

[!Code-csharp[](~/cognitive-services-quickstart-code/dotnet/Face/FindSimilar.cs?name=snippet_find_similar_print)]


#### [REST API](#tab/rest)

Copy the following cURL command and insert your key and endpoint where appropriate.

:::code language="shell" source="~/cognitive-services-quickstart-code/curl/face/detect.sh" ID="similar":::

Paste in the following JSON content for the `body` value:

:::code language="JSON" source="~/cognitive-services-quickstart-code/curl/face/detect.sh" ID="similar_body":::

Then, copy over the source face ID value to the `"faceId"` field. Then copy the other face IDs, separated by commas, as terms in the `"faceIds"` array.

Run the command, and the returned JSON should show the correct face ID as a similar match.

---

## Next step

In this guide, you learned how to call the Find Similar API to do a face search by similarity in a larger group of faces. Next, learn more about the different recognition models available for face comparison operations.

> [!div class="nextstepaction"]
> [Specify a face recognition model](./specify-recognition-model.md)
