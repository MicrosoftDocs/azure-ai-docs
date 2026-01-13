---
title: "Use prediction endpoint to programmatically test images with classifier - Custom Vision"
titleSuffix: Foundry Tools
description: Learn how to use the API to programmatically test images with your Custom Vision Service classifier.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-custom-vision
ms.topic: how-to
ms.date: 11/14/2024
ms.author: pafarley
ms.devlang: csharp
ms.custom: devx-track-csharp
---

# Call the Prediction API

[!INCLUDE [custom-vision-retirement](includes/custom-vision-retirement.md)]

After you train your model, you can test it programmatically by submitting images to the Prediction API endpoint. In this guide, you'll learn how to call the Prediction API to score an image. You'll learn the different ways you can configure the behavior of this API to meet your needs.

> [!NOTE]
> This document demonstrates use of the .NET client library for C# to submit an image to the Prediction API. For more information and examples, see the [Prediction API reference](/rest/api/customvision/predictions).

## Setup

### Publish your trained iteration

From the [Custom Vision website](https://customvision.ai), select your project and then select the __Performance__ tab.

To submit images to the Prediction API, you first need to publish your iteration for prediction, which can be done by selecting __Publish__ and specifying a name for the published iteration. This makes your model accessible to the Prediction API of your Custom Vision Azure resource.

:::image type="content" source="media/use-prediction-api/unpublished-iteration.png" alt-text="Screenshot showing the performance tab, with a red rectangle surrounding the Publish button.":::

Once your model is successfully published, the **Published** label appears next to your iteration in the left-hand sidebar, and its name appears in the description of the iteration.

:::image type="content" source="media/use-prediction-api/published-iteration.png" alt-text="Screenshot of the performance tab, with a red rectangle surrounding the Published label and the name of the published iteration.":::

### Get the URL and prediction key

Once your model is published, you can retrieve the required information by selecting __Prediction URL__. A dialog box opens up with information for using the Prediction API, including the __Prediction URL__ and __Prediction-Key__.

:::image type="content" source="media/use-prediction-api/published-iteration-prediction-url.png" alt-text="Screenshot of the performance tab, with a red rectangle surrounding the Prediction URL button.":::

:::image type="content" source="media/use-prediction-api/prediction-api-info.png" alt-text="Screenshot of the performance tab, with a red rectangle surrounding the Prediction URL value for using an image file and the Prediction-Key value.":::

## Submit data to the service

This guide assumes that you already constructed a **[CustomVisionPredictionClient](/dotnet/api/microsoft.azure.cognitiveservices.vision.customvision.prediction.customvisionpredictionclient)** object, named `predictionClient`, with your Custom Vision prediction key and endpoint URL. For instructions on how to set up this feature, follow one of the [quickstarts](quickstarts/image-classification.md).

In this guide, you use a local image, so download an image you'd like to submit to your trained model. The following code prompts the user to specify a local path and gets the bytestream of the file at that path.

```csharp
Console.Write("Enter image file path: ");
string imageFilePath = Console.ReadLine();
byte[] byteData = GetImageAsByteArray(imageFilePath);
```

Include the following helper method:

```csharp
private static byte[] GetImageAsByteArray(string imageFilePath)
{
    FileStream fileStream = new FileStream(imageFilePath, FileMode.Open, FileAccess.Read);
    BinaryReader binaryReader = new BinaryReader(fileStream);
    return binaryReader.ReadBytes((int)fileStream.Length);
}
```

The **[ClassifyImageAsync](/dotnet/api/microsoft.azure.cognitiveservices.vision.customvision.prediction.customvisionpredictionclientextensions.classifyimageasync#Microsoft_Azure_CognitiveServices_Vision_CustomVision_Prediction_CustomVisionPredictionClientExtensions_ClassifyImageAsync_Microsoft_Azure_CognitiveServices_Vision_CustomVision_Prediction_ICustomVisionPredictionClient_System_Guid_System_String_System_IO_Stream_System_String_System_Threading_CancellationToken_)** method takes the project ID and the locally stored image, and scores the image against the given model.

```csharp
// Make a prediction against the new project
Console.WriteLine("Making a prediction:");
var result = predictionApi.ClassifyImageAsync(project.Id, publishedModelName, byteData);
```

## Determine how to process the data

You can optionally configure how the service does the scoring operation by choosing alternate methods. For details, see the **[CustomVisionPredictionClient](/dotnet/api/microsoft.azure.cognitiveservices.vision.customvision.prediction.customvisionpredictionclient)** method.

You can use a nonasync version of the preceding method for simplicity, but it might cause the program to lock up for a noticeable amount of time.

The `-WithNoStore` methods require that the service doesn't retain the prediction image after prediction is complete. Normally, the service retains these images so you have the option of adding them as training data for future iterations of your model.

The `-WithHttpMessages` methods return the raw HTTP response of the API call.

## Get results from the service

The service returns results in the form of an **[ImagePrediction](/dotnet/api/microsoft.azure.cognitiveservices.vision.customvision.prediction.models.imageprediction)** object. The `Predictions` property contains a list of **[PredictionModel](/dotnet/api/microsoft.azure.cognitiveservices.vision.customvision.prediction.models.predictionmodel)** objects, which each represents a single object prediction. They include the name of the label and the bounding box coordinates where the object was detected in the image. Your app can then parse this data to, for example, display the image with labeled object fields on a screen. 

## Next step

In this guide, you learned how to submit images to your custom image classifier/detector and receive a response programmatically with the C# SDK. Next, learn how to complete end-to-end scenarios with C#, or get started using a different language SDK.

* [Quickstart: Custom Vision SDK](quickstarts/image-classification.md)
