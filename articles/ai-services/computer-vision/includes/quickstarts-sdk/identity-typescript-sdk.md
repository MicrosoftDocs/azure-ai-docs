---
title: "Quickstart: Face identification with TypeScript"
description: In this quickstart, get started using the Azure AI Face TypeScript SDK to detect and identify faces in images.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.topic: include
ms.date: 07/23/2025
ms.author: pafarley
---

Get started with facial recognition using the Face client library for TypeScript. Follow these steps to install the package and try out the example code for basic tasks. The Face service provides you with access to advanced algorithms for detecting and recognizing human faces in images. Follow these steps to install the package and try out the example code for basic face identification using remote images.



[Reference documentation](https://aka.ms/azsdk-javascript-face-ref) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/face/ai-vision-face-rest) | [Package (npm)](https://www.npmjs.com/package/@azure-rest/ai-vision-face) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/face/ai-vision-face-rest/samples)

## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* [Node.js LTS](https://nodejs.org/)
* [TypeScript](https://www.typescriptlang.org/)
* [Visual Studio Code](https://code.visualstudio.com/)
* Once you have your Azure subscription, [Create a Face resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesFace) in the Azure portal to get your key and endpoint. After it deploys, select **Go to resource**.
    * You'll need the key and endpoint from the resource you create to connect your application to the Face API.
    * You can use the free pricing tier (`F0`) to try the service, and upgrade later to a paid tier for production.

## Set up local development environment

1. Create a new directory for your project and navigate to it:

   ```console
   mkdir face-identification
   cd face-identification
   code .
   ```

1. Create a new package for ESM modules in your project directory:

   ```console
   npm init -y
   npm pkg set type=module
   ```

1. Install the required packages:

   ```console
   npm install @azure-rest/ai-vision-face
   ```

1. Install development dependencies:

   ```console
   npm install typescript @types/node --save-dev
   ```

1. Create a `tsconfig.json` file in your project directory:

   ```json
   {
     "compilerOptions": {
       "target": "es2022",
       "module": "esnext",
       "moduleResolution": "bundler",
       "rootDir": "./src",
       "outDir": "./dist/",
       "esModuleInterop": true,
       "forceConsistentCasingInFileNames": true,
       "strict": true,
       "skipLibCheck": true,
       "declaration": true,
       "sourceMap": true,
       "resolveJsonModule": true,
       "moduleDetection": "force",
       "allowSyntheticDefaultImports": true,
       "verbatimModuleSyntax": false
     },
     "include": [
       "src/**/*.ts"
     ],
     "exclude": [
       "node_modules/**/*",
       "**/*.spec.ts"
     ]
   }
   ```

1. Update `package.json` to include a script for building TypeScript files:

   ```json
   "scripts": {
     "build": "tsc",
     "start": "node dist/index.js"
   }
   ```

1. Create a `resources` folder and add sample images to it.

1. Create a `src` directory for your TypeScript code.

[!INCLUDE [create environment variables](../face-environment-variables.md)]

## Identify and verify faces

Create a new file in your `src` directory, `index.ts`, and paste in the following code. Replace the image paths and person group/person names as needed.

> [!NOTE]
> If you haven't received access to the Face service using the [intake form](https://aka.ms/facerecognition), some of these functions won't work.

```typescript
import { randomUUID } from "crypto";
import { AzureKeyCredential } from "@azure/core-auth";
import createFaceClient, {
  getLongRunningPoller,
  isUnexpected,
} from "@azure-rest/ai-vision-face";
import "dotenv/config";

/**
 * This sample demonstrates how to identify and verify faces using Azure Face API.
 *
 * @summary Face identification and verification.
 */

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const main = async () => {
  const endpoint = process.env["FACE_ENDPOINT"] ?? "<endpoint>";
  const apikey = process.env["FACE_APIKEY"] ?? "<apikey>";
  const credential = new AzureKeyCredential(apikey);
  const client = createFaceClient(endpoint, credential);

  const imageBaseUrl =
    "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/";
  const largePersonGroupId = randomUUID();

  console.log("========IDENTIFY FACES========\n");

  // Create a dictionary for all your images, grouping similar ones under the same key.
  const personDictionary: Record<string, string[]> = {
    "Family1-Dad": ["Family1-Dad1.jpg", "Family1-Dad2.jpg"],
    "Family1-Mom": ["Family1-Mom1.jpg", "Family1-Mom2.jpg"],
    "Family1-Son": ["Family1-Son1.jpg", "Family1-Son2.jpg"],
  };

  // A group photo that includes some of the persons you seek to identify from your dictionary.
  const sourceImageFileName = "identification1.jpg";

  // Create a large person group.
  console.log(`Creating a person group with ID: ${largePersonGroupId}`);
  const createGroupResponse = await client
    .path("/largepersongroups/{largePersonGroupId}", largePersonGroupId)
    .put({
      body: {
        name: largePersonGroupId,
        recognitionModel: "recognition_04",
      },
    });
  if (isUnexpected(createGroupResponse)) {
    throw new Error(createGroupResponse.body.error.message);
  }

  // Add faces to person group.
  console.log("Adding faces to person group...");
  await Promise.all(
    Object.keys(personDictionary).map(async (name) => {
      console.log(`Create a persongroup person: ${name}`);
      const createPersonResponse = await client
        .path("/largepersongroups/{largePersonGroupId}/persons", largePersonGroupId)
        .post({
          body: { name },
        });
      if (isUnexpected(createPersonResponse)) {
        throw new Error(createPersonResponse.body.error.message);
      }
      const { personId } = createPersonResponse.body;

      await Promise.all(
        personDictionary[name].map(async (similarImage) => {
          // Check if the image is of sufficient quality for recognition.
          const detectResponse = await client.path("/detect").post({
            contentType: "application/json",
            queryParameters: {
              detectionModel: "detection_03",
              recognitionModel: "recognition_04",
              returnFaceId: false,
              returnFaceAttributes: ["qualityForRecognition"],
            },
            body: { url: `${imageBaseUrl}${similarImage}` },
          });
          if (isUnexpected(detectResponse)) {
            throw new Error(detectResponse.body.error.message);
          }

          const sufficientQuality = detectResponse.body.every(
            (face: any) => face.faceAttributes?.qualityForRecognition === "high"
          );
          if (!sufficientQuality || detectResponse.body.length !== 1) {
            return;
          }

          // Quality is sufficient, add to group.
          console.log(
            `Add face to the person group person: (${name}) from image: (${similarImage})`
          );
          const addFaceResponse = await client
            .path(
              "/largepersongroups/{largePersonGroupId}/persons/{personId}/persistedfaces",
              largePersonGroupId,
              personId
            )
            .post({
              queryParameters: { detectionModel: "detection_03" },
              body: { url: `${imageBaseUrl}${similarImage}` },
            });
          if (isUnexpected(addFaceResponse)) {
            throw new Error(addFaceResponse.body.error.message);
          }
        })
      );
    })
  );
  console.log("Done adding faces to person group.");

  // Train the large person group.
  console.log(`\nTraining person group: ${largePersonGroupId}`);
  const trainResponse = await client
    .path("/largepersongroups/{largePersonGroupId}/train", largePersonGroupId)
    .post();
  if (isUnexpected(trainResponse)) {
    throw new Error(trainResponse.body.error.message);
  }
  const poller = await getLongRunningPoller(client, trainResponse);
  await poller.pollUntilDone();
  console.log(`Training status: ${poller.getOperationState().status}`);
  if (poller.getOperationState().status !== "succeeded") {
    return;
  }

  console.log("Pausing for 60 seconds to avoid triggering rate limit on free account...");
  await sleep(60000);

  // Detect faces from source image url and only take those with sufficient quality for recognition.
  const detectSourceResponse = await client.path("/detect").post({
    contentType: "application/json",
    queryParameters: {
      detectionModel: "detection_03",
      recognitionModel: "recognition_04",
      returnFaceId: true,
      returnFaceAttributes: ["qualityForRecognition"],
    },
    body: { url: `${imageBaseUrl}${sourceImageFileName}` },
  });
  if (isUnexpected(detectSourceResponse)) {
    throw new Error(detectSourceResponse.body.error.message);
  }
  const faceIds = detectSourceResponse.body
    .filter((face: any) => face.faceAttributes?.qualityForRecognition !== "low")
    .map((face: any) => face.faceId);

  // Identify the faces in a large person group.
  const identifyResponse = await client.path("/identify").post({
    body: { faceIds, largePersonGroupId },
  });
  if (isUnexpected(identifyResponse)) {
    throw new Error(identifyResponse.body.error.message);
  }

  await Promise.all(
    identifyResponse.body.map(async (result: any) => {
      try {
        const candidate = result.candidates[0];
        if (!candidate) {
          console.log(`No persons identified for face with ID ${result.faceId}`);
          return;
        }
        const getPersonResponse = await client
          .path(
            "/largepersongroups/{largePersonGroupId}/persons/{personId}",
            largePersonGroupId,
            candidate.personId
          )
          .get();
        if (isUnexpected(getPersonResponse)) {
          throw new Error(getPersonResponse.body.error.message);
        }
        const person = getPersonResponse.body;
        console.log(
          `Person: ${person.name} is identified for face in: ${sourceImageFileName} with ID: ${result.faceId}. Confidence: ${candidate.confidence}`
        );

        // Verification:
        const verifyResponse = await client.path("/verify").post({
          body: {
            faceId: result.faceId,
            largePersonGroupId,
            personId: person.personId,
          },
        });
        if (isUnexpected(verifyResponse)) {
          throw new Error(verifyResponse.body.error.message);
        }
        console.log(
          `Verification result between face ${result.faceId} and person ${person.personId}: ${verifyResponse.body.isIdentical} with confidence: ${verifyResponse.body.confidence}`
        );
      } catch (error: any) {
        console.log(
          `No persons identified for face with ID ${result.faceId}: ${error.message}`
        );
      }
    })
  );
  console.log();

  // Delete large person group.
  console.log(`Deleting person group: ${largePersonGroupId}`);
  const deleteResponse = await client
    .path("/largepersongroups/{largePersonGroupId}", largePersonGroupId)
    .delete();
  if (isUnexpected(deleteResponse)) {
    throw new Error(deleteResponse.body.error.message);
  }
  console.log();

  console.log("Done.");
};

main().catch(console.error);
```

## Build and run the sample

1. Compile the TypeScript code:

   ```console
   npm run build
   ```

1. Run the compiled JavaScript:

   ```console
   npm run start
   ```

## Output

```console
========IDENTIFY FACES========

Creating a person group with ID: a230ac8b-09b2-4fa0-ae04-d76356d88d9f
Adding faces to person group...
Create a persongroup person: Family1-Dad
Create a persongroup person: Family1-Mom
Create a persongroup person: Family1-Son
Add face to the person group person: (Family1-Dad) from image: (Family1-Dad1.jpg)
Add face to the person group person: (Family1-Mom) from image: (Family1-Mom1.jpg)
Add face to the person group person: (Family1-Son) from image: (Family1-Son1.jpg)
Add face to the person group person: (Family1-Dad) from image: (Family1-Dad2.jpg)
Add face to the person group person: (Family1-Mom) from image: (Family1-Mom2.jpg)
Add face to the person group person: (Family1-Son) from image: (Family1-Son2.jpg)
Done adding faces to person group.

Training person group: a230ac8b-09b2-4fa0-ae04-d76356d88d9f
Training status: succeeded
Pausing for 60 seconds to avoid triggering rate limit on free account...
No persons identified for face with ID 56380623-8bf0-414a-b9d9-c2373386b7be
Person: Family1-Dad is identified for face in: identification1.jpg with ID: c45052eb-a910-4fd3-b1c3-f91ccccc316a. Confidence: 0.96807
Person: Family1-Son is identified for face in: identification1.jpg with ID: 8dce9b50-513f-4fe2-9e19-352acfd622b3. Confidence: 0.9281
Person: Family1-Mom is identified for face in: identification1.jpg with ID: 75868da3-66f6-4b5f-a172-0b619f4d74c1. Confidence: 0.96902
Verification result between face c45052eb-a910-4fd3-b1c3-f91ccccc316a and person 35a58d14-fd58-4146-9669-82ed664da357: true with confidence: 0.96807
Verification result between face 8dce9b50-513f-4fe2-9e19-352acfd622b3 and person 2d4d196c-5349-431c-bf0c-f1d7aaa180ba: true with confidence: 0.9281
Verification result between face 75868da3-66f6-4b5f-a172-0b619f4d74c1 and person 35d5de9e-5f92-4552-8907-0d0aac889c3e: true with confidence: 0.96902

Deleting person group: a230ac8b-09b2-4fa0-ae04-d76356d88d9f

Done.
```

## Clean up resources

If you want to clean up and remove a Foundry Tools subscription, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

* [Azure portal](../../../multi-service-resource.md?pivots=azportal#clean-up-resources)
* [Azure CLI](../../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

In this quickstart, you learned how to use the Face client library for TypeScript to do basic face identification. Next, learn about the different face detection models and how to specify the right model for your use case.

> [!div class="nextstepaction"]
> [Specify a face detection model version](../../how-to/specify-detection-model.md)