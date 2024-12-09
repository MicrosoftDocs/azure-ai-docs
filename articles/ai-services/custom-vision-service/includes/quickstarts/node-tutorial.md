---
author: areddish
ms.author: areddish
ms.service: azure-ai-custom-vision
ms.date: 11/11/2024
ms.custom:
ms.topic: include
---

This guide provides instructions and sample code to help you get started using the Custom Vision client library for Node.js to build an image classification model. You can create a project, add tags, train the project, and use the project's prediction endpoint URL to programmatically test it. Use this example as a template for building your own image recognition app.

> [!NOTE]
> If you want to build and train a classification model _without_ writing code, see the [browser-based guidance](../../getting-started-build-a-classifier.md).

Use the Custom Vision client library for Node.js to:

* Create a new Custom Vision project
* Add tags to the project
* Upload and tag images
* Train the project
* Publish the current iteration
* Test the prediction endpoint

Reference documentation for [(training)](/javascript/api/@azure/cognitiveservices-customvision-training/) and [(prediction)](/javascript/api/@azure/cognitiveservices-customvision-prediction/) | Package (npm) for [(training)](https://www.npmjs.com/package/@azure/cognitiveservices-customvision-training) and [(prediction)](https://www.npmjs.com/package/@azure/cognitiveservices-customvision-prediction) | [Samples](/samples/browse/?products=azure&terms=custom%20vision&languages=javascript)

## Prerequisites

* An Azure subscription. You can [create one for free](https://azure.microsoft.com/free/cognitive-services/).
* The current version of [Node.js](https://nodejs.org).
* Once you have your Azure subscription, create a [Custom Vision resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesCustomVision) in the Azure portal to create a training and prediction resource.
    * You can use the free pricing tier (`F0`) to try the service, and upgrade later to a paid tier for production.

[!INCLUDE [create environment variables](../environment-variables.md)]

## Setting up

### Create a new Node.js application

In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it. 

```console
mkdir myapp && cd myapp
```

Run the `npm init` command to create a node application with a `package.json` file. Press ENTER multiple times to complete the process.

```console
npm init
```

### Install the client library

To write an image analysis app with Custom Vision for Node.js, you need the Custom Vision npm packages. To install them, run the following command in PowerShell:

```shell
npm install @azure/cognitiveservices-customvision-training
npm install @azure/cognitiveservices-customvision-prediction
```

Your app's `package.json` file is updated with the dependencies.

Create a file named `index.js` and import the following libraries:

[!code-javascript[](~/cognitive-services-quickstart-code/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js?name=snippet_imports)]


> [!TIP]
> Want to view the whole quickstart code file at once? You can find it on [GitHub](https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js), which contains the code examples in this quickstart.

Create variables for your resource's Azure endpoint and keys. 

[!code-javascript[](~/cognitive-services-quickstart-code/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js?name=snippet_creds)]

Also add fields for your project name and a timeout parameter for asynchronous calls.

[!code-javascript[](~/cognitive-services-quickstart-code/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js?name=snippet_vars)]


## Object model

|Name|Description|
|---|---|
|[TrainingAPIClient](/javascript/api/@azure/cognitiveservices-customvision-training/trainingapiclient) | This class handles the creation, training, and publishing of your models. |
|[PredictionAPIClient](/javascript/api/@azure/cognitiveservices-customvision-prediction/predictionapiclient)| This class handles the querying of your models for image classification predictions.|
|[Prediction](/javascript/api/@azure/cognitiveservices-customvision-prediction/)| This interface defines a single prediction on a single image. It includes properties for the object ID and name, and a confidence score.|

## Code examples

These code snippets show you how to do the following tasks with the Custom Vision client library for JavaScript:

* [Authenticate the client](#authenticate-the-client)
* [Create a new Custom Vision project](#create-a-new-custom-vision-project)
* [Add tags to the project](#add-tags-to-the-project)
* [Upload and tag images](#upload-and-tag-images)
* [Train the project](#train-the-project)
* [Publish the current iteration](#publish-the-current-iteration)
* [Test the prediction endpoint](#test-the-prediction-endpoint)

## Authenticate the client

Instantiate client objects with your endpoint and key. Create an **ApiKeyCredentials** object with your key, and use it with your endpoint to create a [TrainingAPIClient](/javascript/api/@azure/cognitiveservices-customvision-training/trainingapiclient) and [PredictionAPIClient](/javascript/api/@azure/cognitiveservices-customvision-prediction/predictionapiclient) object.

[!code-javascript[](~/cognitive-services-quickstart-code/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js?name=snippet_auth)]


## Create a new Custom Vision project

Start a new function to contain all of your Custom Vision function calls. Add the following code to create a new Custom Vision service project.


[!code-javascript[](~/cognitive-services-quickstart-code/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js?name=snippet_create)]


## Add tags to the project

To create classification tags to your project, add the following code to your function:

[!code-javascript[](~/cognitive-services-quickstart-code/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js?name=snippet_tags)]


## Upload and tag images

First, download the sample images for this project. Save the contents of the [sample Images folder](https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/CustomVision/ImageClassification/Images) to your local device.

To add the sample images to the project, insert the following code after the tag creation. This code uploads each image with its corresponding tag.

[!code-javascript[](~/cognitive-services-quickstart-code/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js?name=snippet_upload)]

> [!IMPORTANT]
> You need to change the path to the images (`sampleDataRoot`) based on where you downloaded the Azure AI services Python SDK Samples repo.

## Train the project

This code creates the first iteration of the prediction model. 

[!code-javascript[](~/cognitive-services-quickstart-code/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js?name=snippet_train)]

## Publish the current iteration

This code publishes the trained iteration to the prediction endpoint. The name given to the published iteration can be used to send prediction requests. An iteration isn't available in the prediction endpoint until it's published.

[!code-javascript[](~/cognitive-services-quickstart-code/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js?name=snippet_publish)]


## Test the prediction endpoint

To send an image to the prediction endpoint and retrieve the prediction, add the following code to your function. 

[!code-javascript[](~/cognitive-services-quickstart-code/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js?name=snippet_test)]

Then, close your Custom Vision function and call it.

[!code-javascript[](~/cognitive-services-quickstart-code/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js?name=snippet_function_close)]


## Run the application

Run the application with the `node` command on your quickstart file.

```console
node index.js
```

The output of the application should be similar to the following text:

```console
Creating project...
Adding images...
Training...
Training started...
Training status: Training
Training status: Training
Training status: Training
Training status: Completed
Results:
         Hemlock: 94.97%
         Japanese Cherry: 0.01%
```

You can then verify that the test image (found in *\<sampleDataRoot\>/Test/*) is tagged appropriately. You can also go back to the [Custom Vision website](https://customvision.ai) and see the current state of your newly created project.

[!INCLUDE [clean-ic-project](../../includes/clean-ic-project.md)]

## Related content

This guide shows how every step of the object detection process can be done in code. This sample executes a single training iteration, but often you'll need to train and test your model multiple times in order to make it more accurate.

> [!div class="nextstepaction"]
> [Test and retrain a model](../../test-your-model.md)

* [What is Custom Vision?](../../overview.md)
* The source code for this sample can be found on [GitHub](https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/javascript/CustomVision/ImageClassification/CustomVisionQuickstart.js)
* [SDK reference documentation (training)](/javascript/api/@azure/cognitiveservices-customvision-training/)
* [SDK reference documentation (prediction)](/javascript/api/@azure/cognitiveservices-customvision-prediction/)
