---
title: Detect liveness in faces
description: In this Tutorial, you learn how to Detect liveness in faces, using both server-side code and a client-side mobile application.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.custom:
  - ignite-2023
ms.topic: tutorial
ms.date: 03/26/2025
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Tutorial: Detect liveness in faces

In this tutorial, you learn how to detect liveness in faces, using a combination of server-side code and a client-side mobile application. 

> [!TIP]
> For general information about face liveness detection, see the [conceptual guide](../concept-face-liveness-detection.md).

This tutorial demonstrates how to operate a frontend application and an app server to perform liveness detection, including the optional step of [face verification](#perform-liveness-detection-with-face-verification), across various platforms and languages.


[!INCLUDE [liveness-sdk-gate](../includes/liveness-sdk-gate.md)]

> [!TIP]
> After you complete the prerequisites, you can try the iOS liveness experience from [TestFlight](https://aka.ms/face/liveness/demo/ios) and the web-liveness experience from [Vision Studio](https://portal.vision.cognitive.azure.com/demo/face-liveness-detection). Moreover, you can also build and run a complete frontend sample (either on iOS, Android, or Web) from the [Samples](https://github.com/Azure-Samples/azure-ai-vision-sdk/tree/main?tab=readme-ov-file#samples) section.

## Prerequisites

- Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services/)
- Your Azure account must have a **Cognitive Services Contributor** role assigned in order for you to agree to the responsible AI terms and create a resource. To get this role assigned to your account, follow the steps in the [Assign roles](/azure/role-based-access-control/role-assignments-steps) documentation, or contact your administrator. 
- Once you have your Azure subscription, <a href="https://portal.azure.com/#create/Microsoft.CognitiveServicesFace"  title="Create a Face resource"  target="_blank">create a Face resource</a> in the Azure portal to get your key and endpoint. After it deploys, select **Go to resource**. 
    - You need the key and endpoint from the resource you create to connect your application to the Face service.
    - You can use the free pricing tier (`F0`) to try the service, and upgrade later to a paid tier for production.
- Access to the Azure AI Vision Face Client SDK for Mobile (IOS and Android) and Web. To get started, you need to apply for the [Face Recognition Limited Access features](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUQjA5SkYzNDM4TkcwQzNEOE1NVEdKUUlRRCQlQCN0PWcu) to get access to the SDK. For more information, see the [Face Limited Access](/azure/ai-foundry/responsible-ai/computer-vision/limited-access-identity?context=%2Fazure%2Fcognitive-services%2Fcomputer-vision%2Fcontext%2Fcontext) page.
- Familiarity with the Face liveness detection feature. See the [conceptual guide](../concept-face-liveness-detection.md).

## Prepare SDKs

We provide SDKs in different languages to simplify development on frontend applications and app servers:

### Download SDK for frontend application

Follow instructions in the [azure-ai-vision-sdk](https://github.com/Azure-Samples/azure-ai-vision-sdk) GitHub repository to integrate the UI and the code into your native mobile application. The liveness SDK supports Java/Kotlin for Android mobile applications, Swift for iOS mobile applications and JavaScript for web applications:
- For Swift iOS, follow the instructions in the [iOS sample](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-ios-readme) 
- For Kotlin/Java Android, follow the instructions in the [Android sample](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-android-readme) 
- For JavaScript Web, follow the instructions in the [Web sample](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-web-readme) 

Once you've added the code into your application, the SDK handles starting the camera, guiding the end-user in adjusting their position, composing the liveness payload, and calling the Azure AI Face cloud service to process the liveness payload.

You can monitor the [Releases section](https://github.com/Azure-Samples/azure-ai-vision-sdk/releases) of the SDK repo for new SDK version updates.

### Download Azure AI Face client library for app server

The app server/orchestrator is responsible for controlling the lifecycle of a liveness session. The app server has to create a session before performing liveness detection, and then it can query the result and delete the session when the liveness check is finished. We offer a library in various languages for easily implementing your app server. Follow these steps to install the package you want:
- For C#, follow the instructions in the [dotnet readme](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/face/Azure.AI.Vision.Face/README.md)
- For Java, follow the instructions in the [Java readme](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/face/azure-ai-vision-face/README.md)
- For Python, follow the instructions in the [Python readme](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/face/azure-ai-vision-face/README.md)
- For JavaScript, follow the instructions in the [JavaScript readme](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/face/ai-vision-face-rest/README.md)

> [!IMPORTANT]
> To create environment variables for your Azure Face service key and endpoint, see the [quickstart](../quickstarts-sdk/identity-client-library.md)


## Perform liveness detection

The high-level steps involved in liveness orchestration are illustrated below:  

:::image type="content" source="../media/liveness/liveness-diagram.jpg" alt-text="Diagram of the liveness workflow in Azure AI Face." lightbox="../media/liveness/liveness-diagram.jpg":::

1. The frontend application starts the liveness check and notifies the app server. 

1. The app server creates a new liveness session with Azure AI Face Service. The service creates a liveness-session and responds back with a session-authorization-token. More information regarding each request parameter involved in creating a liveness session is referenced in [Liveness Create Session Operation](https://aka.ms/face-api-reference-createlivenesssession).

    #### [C#](#tab/csharp)
    ```csharp
    var endpoint = new Uri(System.Environment.GetEnvironmentVariable("FACE_ENDPOINT"));
    var credential = new AzureKeyCredential(System.Environment.GetEnvironmentVariable("FACE_APIKEY"));

    var sessionClient = new FaceSessionClient(endpoint, credential);

    var createContent = new CreateLivenessSessionContent(LivenessOperationMode.Passive)
    {
        DeviceCorrelationId = "723d6d03-ef33-40a8-9682-23a1feb7bccd",
        EnableSessionImage = true,
    };

    var createResponse = await sessionClient.CreateLivenessSessionAsync(createContent);
    var sessionId = createResponse.Value.SessionId;
    Console.WriteLine($"Session created.");
    Console.WriteLine($"Session id: {sessionId}");
    Console.WriteLine($"Auth token: {createResponse.Value.AuthToken}");
    ```

    #### [Java](#tab/java)
    ```java
    String endpoint = System.getenv("FACE_ENDPOINT");
    String accountKey = System.getenv("FACE_APIKEY");

    FaceSessionClient sessionClient = new FaceSessionClientBuilder()
        .endpoint(endpoint)
        .credential(new AzureKeyCredential(accountKey))
        .buildClient();

    CreateLivenessSessionContent parameters = new CreateLivenessSessionContent(LivenessOperationMode.PASSIVE)
        .setDeviceCorrelationId("723d6d03-ef33-40a8-9682-23a1feb7bccd")
        .setEnableSessionImage(true);

    CreateLivenessSessionResult creationResult = sessionClient.createLivenessSession(parameters);
    System.out.println("Session created.");
    System.out.println("Session id: " + creationResult.getSessionId());
    System.out.println("Auth token: " + creationResult.getAuthToken());
    ```

    #### [Python](#tab/python)
    ```python
    endpoint = os.environ["FACE_ENDPOINT"]
    key = os.environ["FACE_APIKEY"]

    face_session_client = FaceSessionClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    created_session = await face_session_client.create_liveness_session(
        CreateLivenessSessionContent(
            liveness_operation_mode=LivenessOperationMode.PASSIVE,
            device_correlation_id="723d6d03-ef33-40a8-9682-23a1feb7bccd",
            enable_session_image=True,
        )
    )
    print("Session created.")
    print(f"Session id: {created_session.session_id}")
    print(f"Auth token: {created_session.auth_token}")
    ```

    #### [JavaScript](#tab/javascript)
    ```javascript
    const endpoint = process.env['FACE_ENDPOINT'];
    const apikey = process.env['FACE_APIKEY'];

    const credential = new AzureKeyCredential(apikey);
    const client = createFaceClient(endpoint, credential);

    const createLivenessSessionResponse = await client.path('/detectLiveness-sessions').post({
        body: {
            livenessOperationMode: 'Passive',
            deviceCorrelationId: '723d6d03-ef33-40a8-9682-23a1feb7bccd',
            enableSessionImage: true,
        },
    });

    if (isUnexpected(createLivenessSessionResponse)) {
        throw new Error(createLivenessSessionResponse.body.error.message);
    }

    console.log('Session created.');
    console.log(`Session ID: ${createLivenessSessionResponse.body.sessionId}`);
    console.log(`Auth token: ${createLivenessSessionResponse.body.authToken}`);
    ```

    #### [REST API (Windows)](#tab/cmd)
    ```console
    curl --request POST --location "%FACE_ENDPOINT%/face/v1.2/detectLiveness-sessions" ^
    --header "Ocp-Apim-Subscription-Key: %FACE_APIKEY%" ^
    --header "Content-Type: application/json" ^
    --data ^
    "{ ^
        ""livenessOperationMode"": ""passive"", ^
        ""deviceCorrelationId"": ""723d6d03-ef33-40a8-9682-23a1feb7bccd"", ^
        ""enableSessionImage"": ""true"" ^
    }"
    ```

    #### [REST API (Linux)](#tab/bash)
    ```bash
    curl --request POST --location "${FACE_ENDPOINT}/face/v1.2/detectLivenesswithVerify-sessions" \
    --header "Ocp-Apim-Subscription-Key: ${FACE_APIKEY}" \
    --header "Content-Type: application/json" \
    --data \
    '{
        "livenessOperationMode": "passive",
        "deviceCorrelationId": "723d6d03-ef33-40a8-9682-23a1feb7bccd",
        "enableSessionImage": "true"
    }'
    ```

    ---

    An example of the response body:
    ```json 
    {
        "sessionId": "a6e7193e-b638-42e9-903f-eaf60d2b40a5",
        "authToken": "<session-authorization-token>",
        "status": "NotStarted",
        "modelVersion": "2024-11-15",
        "results": {
            "attempts": []
        }
    }
    ```

1. The app server provides the session-authorization-token back to the frontend application. 

1. The frontend application uses the session-authorization-token to start the face-liveness-detector which will kick off the liveness flow.

    #### [Android](#tab/mobile-kotlin)
    ```kotlin
        FaceLivenessDetector(
            sessionAuthorizationToken = FaceSessionToken.sessionToken,
            verifyImageFileContent = FaceSessionToken.sessionSetInClientVerifyImage,
            deviceCorrelationId = "null",
            onSuccess = viewModel::onSuccess,
            onError = viewModel::onError
        )
    ```

    #### [iOS](#tab/mobile-swift)
    ```swift
    struct HostView: View {
       @State var livenessDetectionResult: LivenessDetectionResult? = nil
       var token: String
       var body: some View {
           if livenessDetectionResult == nil {
               FaceLivenessDetectorView(result: $livenessDetectionResult,
                                        sessionAuthorizationToken: token)
           } else if let result = livenessDetectionResult {
               VStack {
                   switch result { 
                       case .success(let success):
                       /// <#show success#>
                       case .failure(let error):
                       /// <#show failure#>
                   }
               }
           }
       }
    }
    ```

    #### [Web](#tab/web-javascript)
    ```javascript
    faceLivenessDetector = document.createElement("azure-ai-vision-face-ui");
    document.getElementById("container").appendChild(faceLivenessDetector);
    faceLivenessDetector.start(session.authToken)
    ```

    ---

1. The SDK then starts the camera, guides the user to position correctly, and then prepares the payload to call the liveness detection service endpoint. 
 
1. The SDK calls the Azure AI Vision Face service to perform the liveness detection. Once the service responds, the SDK notifies the frontend application that the liveness check has been completed.

1. The frontend application relays the liveness check completion to the app server. 

1. The app server can now query for the liveness detection result from the Azure AI Vision Face service. 

    #### [C#](#tab/csharp)
    ```csharp
    var getResultResponse = await sessionClient.GetLivenessSessionResultAsync(sessionId);

    var sessionResult = getResultResponse.Value;
    Console.WriteLine($"Session id: {sessionResult.Id}");
    Console.WriteLine($"Session status: {sessionResult.Status}");
    Console.WriteLine($"Liveness detection decision: {sessionResult.Result?.Response.Body.LivenessDecision}");
    ```

    #### [Java](#tab/java)
    ```java
    LivenessSession sessionResult = sessionClient.getLivenessSessionResult(creationResult.getSessionId());
    System.out.println("Session id: " + sessionResult.getId());
    System.out.println("Session status: " + sessionResult.getStatus());
    System.out.println("Liveness detection decision: " + sessionResult.getResult().getResponse().getBody().getLivenessDecision());
    ```

    #### [Python](#tab/python)
    ```python
    liveness_result = await face_session_client.get_liveness_session_result(
        created_session.session_id
    )
    print(f"Session id: {liveness_result.id}")
    print(f"Session status: {liveness_result.status}")
    print(f"Liveness detection decision: {liveness_result.result.response.body.liveness_decision}")
    ```

    #### [JavaScript](#tab/javascript)
    ```javascript
    const getLivenessSessionResultResponse = await client.path('/detectLiveness/singleModal/sessions/{sessionId}', createLivenessSessionResponse.body.sessionId).get();

    if (isUnexpected(getLivenessSessionResultResponse)) {
        throw new Error(getLivenessSessionResultResponse.body.error.message);
    }

    console.log(`Session id: ${getLivenessSessionResultResponse.body.id}`);
    console.log(`Session status: ${getLivenessSessionResultResponse.body.status}`);
    console.log(`Liveness detection request id: ${getLivenessSessionResultResponse.body.result?.requestId}`);
    console.log(`Liveness detection received datetime: ${getLivenessSessionResultResponse.body.result?.receivedDateTime}`);
    console.log(`Liveness detection decision: ${getLivenessSessionResultResponse.body.result?.response.body.livenessDecision}`);
    console.log(`Session created datetime: ${getLivenessSessionResultResponse.body.createdDateTime}`);
    console.log(`Auth token TTL (seconds): ${getLivenessSessionResultResponse.body.authTokenTimeToLiveInSeconds}`);
    console.log(`Session expired: ${getLivenessSessionResultResponse.body.sessionExpired}`);
    console.log(`Device correlation id: ${getLivenessSessionResultResponse.body.deviceCorrelationId}`);
    ```

    #### [REST API (Windows)](#tab/cmd)
    ```console
    curl --request GET --location "%FACE_ENDPOINT%/face/v1.2/detectLiveness-sessions/<session-id>" ^
    --header "Ocp-Apim-Subscription-Key: %FACE_APIKEY%"
    ```

    #### [REST API (Linux)](#tab/bash)
    ```bash
    curl --request GET --location "${FACE_ENDPOINT}/face/v1.2/detectLiveness-sessions/<session-id>" \
    --header "Ocp-Apim-Subscription-Key: ${FACE_APIKEY}"
    ```

    ---

    An example of the response body:
    ```json
    {
        "sessionId": "0acf6dbf-ce43-42a7-937e-705938881d62",
        "authToken": "",
        "status": "Succeeded",
        "modelVersion": "2024-11-15",
        "results": {
            "attempts": [
            {
                "attemptId": 1,
                "attemptStatus": "Succeeded",
                "result": {
                "livenessDecision": "realface",
                "targets": {
                    "color": {
                    "faceRectangle": {
                        "top": 763,
                        "left": 320,
                        "width": 739,
                        "height": 938
                    }
                    }
                },
                "digest": "517A0E700859E42107FA47E957DD12F54211C1A021A969CD391AC38BB88295A2",
                "sessionImageId": "Ab9tzwpDzqdCk35wWTiIHWJzzPr9fBCNSqBcXnJmDjbI"
                }
            }
            ]
        }
    }
    ```

1. The app server can delete the session once all session-results have been queried.

    #### [C#](#tab/csharp)
    ```csharp
    await sessionClient.DeleteLivenessSessionAsync(sessionId);
    Console.WriteLine($"The session {sessionId} is deleted.");
    ```

    #### [Java](#tab/java)
    ```java
    sessionClient.deleteLivenessSession(creationResult.getSessionId());
    System.out.println("The session " + creationResult.getSessionId() + " is deleted.");
    ```

    #### [Python](#tab/python)
    ```python
    await face_session_client.delete_liveness_session(
        created_session.session_id
    )
    print(f"The session {created_session.session_id} is deleted.")
    await face_session_client.close()
    ```

    #### [JavaScript](#tab/javascript)
    ```javascript
    const deleteLivenessSessionResponse = await client.path('/detectLiveness/singleModal/sessions/{sessionId}', createLivenessSessionResponse.body.sessionId).delete();
    if (isUnexpected(deleteLivenessSessionResponse)) {
        throw new Error(deleteLivenessSessionResponse.body.error.message);
    }
    console.log(`The session ${createLivenessSessionResponse.body.sessionId} is deleted.`);
    ```

    #### [REST API (Windows)](#tab/cmd)
    ```console
    curl --request DELETE --location "%FACE_ENDPOINT%/face/v1.2/detectLiveness-sessions/<session-id>" ^
    --header "Ocp-Apim-Subscription-Key: %FACE_APIKEY%"
    ```

    #### [REST API (Linux)](#tab/bash)
    ```bash
    curl --request DELETE --location "${FACE_ENDPOINT}/face/v1.2/detectLiveness-sessions/<session-id>" \
    --header "Ocp-Apim-Subscription-Key: ${FACE_APIKEY}"
    ```

    ---

## Perform liveness detection with face verification

Combining face verification with liveness detection enables biometric verification of a particular person of interest with an added guarantee that the person is physically present in the system. 

:::image type="content" source="../media/liveness/liveness-verify-diagram.jpg" alt-text="Diagram of the liveness-with-face-verification workflow of Azure AI Face." lightbox="../media/liveness/liveness-verify-diagram.jpg":::

There are two parts to integrating liveness with verification:

### Step 1 - Select a reference image

Follow the tips listed in the [composition requirements for ID verification scenarios](../overview-identity.md#input-requirements) to ensure that your input images give the most accurate recognition results.


### Step 2 - Set up the orchestration of liveness with verification.

The high-level steps involved in liveness with verification orchestration are illustrated below:
1. Providing the verification reference image by either of the following two methods:
    - The app server provides the reference image when creating the liveness session. More information regarding each request parameter involved in creating a liveness session with verification is referenced in [Liveness With Verify Create Session Operation](https://aka.ms/face-api-reference-createlivenesswithverifysession).

        #### [C#](#tab/csharp)
        ```csharp
        var endpoint = new Uri(System.Environment.GetEnvironmentVariable("FACE_ENDPOINT"));
        var credential = new AzureKeyCredential(System.Environment.GetEnvironmentVariable("FACE_APIKEY"));

        var sessionClient = new FaceSessionClient(endpoint, credential);

        var createContent = new CreateLivenessWithVerifySessionContent(LivenessOperationMode.Passive)
        {
            DeviceCorrelationId = "723d6d03-ef33-40a8-9682-23a1feb7bccd",
            EnableSessionImage = true,
        };
        using var fileStream = new FileStream("test.png", FileMode.Open, FileAccess.Read);

        var createResponse = await sessionClient.CreateLivenessWithVerifySessionAsync(createContent, fileStream);

        var sessionId = createResponse.Value.SessionId;
        Console.WriteLine("Session created.");
        Console.WriteLine($"Session id: {sessionId}");
        Console.WriteLine($"Auth token: {createResponse.Value.AuthToken}");
        Console.WriteLine("The reference image:");
        Console.WriteLine($"  Face rectangle: {createResponse.Value.VerifyImage.FaceRectangle.Top}, {createResponse.Value.VerifyImage.FaceRectangle.Left}, {createResponse.Value.VerifyImage.FaceRectangle.Width}, {createResponse.Value.VerifyImage.FaceRectangle.Height}");
        Console.WriteLine($"  The quality for recognition: {createResponse.Value.VerifyImage.QualityForRecognition}");
        ```

        #### [Java](#tab/java)
        ```java
        String endpoint = System.getenv("FACE_ENDPOINT");
        String accountKey = System.getenv("FACE_APIKEY");

        FaceSessionClient sessionClient = new FaceSessionClientBuilder()
            .endpoint(endpoint)
            .credential(new AzureKeyCredential(accountKey))
            .buildClient();

        CreateLivenessWithVerifySessionContent parameters = new CreateLivenessWithVerifySessionContent(LivenessOperationMode.PASSIVE)
            .setDeviceCorrelationId("723d6d03-ef33-40a8-9682-23a1feb7bccd")
            .setEnableSessionImage(true);

        Path path = Paths.get("test.png");
        BinaryData data = BinaryData.fromFile(path);
        CreateLivenessWithVerifySessionResult creationResult = sessionClient.createLivenessWithVerifySession(parameters, data);

        System.out.println("Session created.");
        System.out.println("Session id: " + creationResult.getSessionId());
        System.out.println("Auth token: " + creationResult.getAuthToken());
        System.out.println("The reference image:");
        System.out.println("  Face rectangle: " + creationResult.getVerifyImage().getFaceRectangle().getTop() + " " + creationResult.getVerifyImage().getFaceRectangle().getLeft() + " " + creationResult.getVerifyImage().getFaceRectangle().getWidth() + " " + creationResult.getVerifyImage().getFaceRectangle().getHeight());
        System.out.println("  The quality for recognition: " + creationResult.getVerifyImage().getQualityForRecognition());        
        ```

        #### [Python](#tab/python)
        ```python
        endpoint = os.environ["FACE_ENDPOINT"]
        key = os.environ["FACE_APIKEY"]

        face_session_client = FaceSessionClient(endpoint=endpoint, credential=AzureKeyCredential(key))

        reference_image_path = "test.png"
        with open(reference_image_path, "rb") as fd:
            reference_image_content = fd.read()

        created_session = await face_session_client.create_liveness_with_verify_session(
            CreateLivenessWithVerifySessionContent(
                liveness_operation_mode=LivenessOperationMode.PASSIVE,
                device_correlation_id="723d6d03-ef33-40a8-9682-23a1feb7bccd",
                enable_session_image=True,
            ),
            verify_image=reference_image_content,
        )
        print("Session created.")
        print(f"Session id: {created_session.session_id}")
        print(f"Auth token: {created_session.auth_token}")
        print("The reference image:")
        print(f"  Face rectangle: {created_session.verify_image.face_rectangle}")
        print(f"  The quality for recognition: {created_session.verify_image.quality_for_recognition}")
        ```

        #### [JavaScript](#tab/javascript)
        ```javascript
        const endpoint = process.env['FACE_ENDPOINT'];
        const apikey = process.env['FACE_APIKEY'];

        const credential = new AzureKeyCredential(apikey);
        const client = createFaceClient(endpoint, credential);

        const createLivenessSessionResponse = await client.path('/detectLivenesswithVerify-sessions').post({
            contentType: 'multipart/form-data',
            body: [
                {
                    name: 'VerifyImage',
                    // Note that this utilizes Node.js API.
                    // In browser environment, please use file input or drag and drop to read files.
                    body: readFileSync('test.png'),
                },
                {
                    name: 'Parameters',
                    body: {
                        livenessOperationMode: 'Passive',
                        deviceCorrelationId: '723d6d03-ef33-40a8-9682-23a1feb7bccd',
                        enableSessionImage: true,
                    },
                },
            ],
        });

        if (isUnexpected(createLivenessSessionResponse)) {
            throw new Error(createLivenessSessionResponse.body.error.message);
        }

        console.log('Session created:');
        console.log(`Session ID: ${createLivenessSessionResponse.body.sessionId}`);
        console.log(`Auth token: ${createLivenessSessionResponse.body.authToken}`);
        console.log('The reference image:');
        console.log(`  Face rectangle: ${createLivenessSessionResponse.body.verifyImage.faceRectangle}`);
        console.log(`  The quality for recognition: ${createLivenessSessionResponse.body.verifyImage.qualityForRecognition}`)
        ```

        #### [REST API (Windows)](#tab/cmd)
        ```console
        curl --request POST --location "%FACE_ENDPOINT%/face/v1.2/detectLivenesswithVerify-sessions" ^
        --header "Ocp-Apim-Subscription-Key: %FACE_APIKEY%" ^
        --form "Parameters=""{\\\""livenessOperationMode\\\"": \\\""passive\\\"", \\\""deviceCorrelationId\\\"": \\\""723d6d03-ef33-40a8-9682-23a1feb7bccd\\\"", ""enableSessionImage"": ""true""}""" ^
        --form "VerifyImage=@""test.png"""
        ```

        #### [REST API (Linux)](#tab/bash)
        ```bash
        curl --request POST --location "${FACE_ENDPOINT}/face/v1.2/detectLivenesswithVerify-sessions" \
        --header "Ocp-Apim-Subscription-Key: ${FACE_APIKEY}" \
        --form 'Parameters="{
            \"livenessOperationMode\": \"passive\",
            \"deviceCorrelationId\": \"723d6d03-ef33-40a8-9682-23a1feb7bccd\"
        }"' \
        --form 'VerifyImage=@"test.png"'
        ```

        ---

        An example of the response body:
        ```json
        {
            "sessionId": "3847ffd3-4657-4e6c-870c-8e20de52f567",
            "authToken": "<session-authorization-token>",
            "status": "NotStarted",
            "modelVersion": "2024-11-15",
            "results": {
                "attempts": [],
                "verifyReferences": [
                {
                    "referenceType": "image",
                    "faceRectangle": {
                    "top": 98,
                    "left": 131,
                    "width": 233,
                    "height": 300
                    },
                    "qualityForRecognition": "high"
                }
                ]
            }
        }
        ```

    - The frontend application provides the reference image when initializing the SDK. This scenario is not supported in the web solution.

        #### [Android](#tab/mobile-kotlin)
        ```kotlin
            FaceLivenessDetector(
                sessionAuthorizationToken = FaceSessionToken.sessionToken,
                verifyImageFileContent = FaceSessionToken.sessionSetInClientVerifyImage,
                deviceCorrelationId = "null",
                onSuccess = viewModel::onSuccess,
                onError = viewModel::onError
            )
        ```

        #### [iOS](#tab/mobile-swift)
        ```swift
        struct HostView: View {
            @State var livenessDetectionResult: LivenessDetectionResult? = nil
            var token: String
            var body: some View {
                if livenessDetectionResult == nil {
                    FaceLivenessDetectorView(result: $livenessDetectionResult,
                                                sessionAuthorizationToken: token)
                } else if let result = livenessDetectionResult {
                    VStack {
                        switch result { 
                            case .success(let success):
                            /// <#show success#>
                            case .failure(let error):
                            /// <#show failure#>
                        }
                    }
                }
            }
        }
        ```

        #### [Web](#tab/web-javascript)
        ```javascript
        Not supported.
        ```

        ---

1. The app server can now query for the verification result in addition to the liveness result.

    #### [C#](#tab/csharp)
    ```csharp
    var getResultResponse = await sessionClient.GetLivenessWithVerifySessionResultAsync(sessionId);
    var sessionResult = getResultResponse.Value;
    Console.WriteLine($"Session id: {sessionResult.Id}");
    Console.WriteLine($"Session status: {sessionResult.Status}");
    Console.WriteLine($"Liveness detection decision: {sessionResult.Result?.Response.Body.LivenessDecision}");
    Console.WriteLine($"Verification result: {sessionResult.Result?.Response.Body.VerifyResult.IsIdentical}");
    Console.WriteLine($"Verification confidence: {sessionResult.Result?.Response.Body.VerifyResult.MatchConfidence}");
    ```

    #### [Java](#tab/java)
    ```java
    LivenessWithVerifySession sessionResult = sessionClient.getLivenessWithVerifySessionResult(creationResult.getSessionId());
    System.out.println("Session id: " + sessionResult.getId());
    System.out.println("Session status: " + sessionResult.getStatus());
    System.out.println("Liveness detection decision: " + sessionResult.getResult().getResponse().getBody().getLivenessDecision());
    System.out.println("Verification result: " + sessionResult.getResult().getResponse().getBody().getVerifyResult().isIdentical());
    System.out.println("Verification confidence: " + sessionResult.getResult().getResponse().getBody().getVerifyResult().getMatchConfidence());
    ```

    #### [Python](#tab/python)
    ```python
    liveness_result = await face_session_client.get_liveness_with_verify_session_result(
        created_session.session_id
    )
    print(f"Session id: {liveness_result.id}")
    print(f"Session status: {liveness_result.status}")
    print(f"Liveness detection decision: {liveness_result.result.response.body.liveness_decision}")
    print(f"Verification result: {liveness_result.result.response.body.verify_result.is_identical}")
    print(f"Verification confidence: {liveness_result.result.response.body.verify_result.match_confidence}")
    ```

    #### [JavaScript](#tab/javascript)
    ```javascript
    const getLivenessSessionResultResponse = await client.path('/detectLivenesswithVerify/singleModal/sessions/{sessionId}', createLivenessSessionResponse.body.sessionId).get();
    if (isUnexpected(getLivenessSessionResultResponse)) {
        throw new Error(getLivenessSessionResultResponse.body.error.message);
    }

    console.log(`Session id: ${getLivenessSessionResultResponse.body.id}`);
    console.log(`Session status: ${getLivenessSessionResultResponse.body.status}`);
    console.log(`Liveness detection request id: ${getLivenessSessionResultResponse.body.result?.requestId}`);
    console.log(`Verification result: ${getLivenessSessionResultResponse.body.result?.response.body.verifyResult.isIdentical}`);
    console.log(`Verification confidence: ${getLivenessSessionResultResponse.body.result?.response.body.verifyResult.matchConfidence}`);
    ```

    #### [REST API (Windows)](#tab/cmd)
    ```console
    curl --request GET --location "%FACE_ENDPOINT%/face/v1.2/detectLivenesswithVerify-sessions/<session-id>" ^
    --header "Ocp-Apim-Subscription-Key: %FACE_APIKEY%"
    ```

    #### [REST API (Linux)](#tab/bash)
    ```bash
    curl --request GET --location "${FACE_ENDPOINT}/face/v1.2/detectLivenesswithVerify-sessions/<session-id>" \
    --header "Ocp-Apim-Subscription-Key: ${FACE_APIKEY}"
    ```

    ---

    An example of the response body:
    ```json
    {
        "sessionId": "93fd6f13-4161-41df-8a22-80a38ef53836",
        "authToken": "",
        "status": "Succeeded",
        "modelVersion": "2024-11-15",
        "results": {
            "attempts": [
                {
                    "attemptId": 1,
                    "attemptStatus": "Succeeded",
                    "result": {
                    "livenessDecision": "realface",
                    "targets": {
                        "color": {
                            "faceRectangle": {
                                "top": 669,
                                "left": 203,
                                "width": 646,
                                "height": 724
                            }
                        }
                    },
                    "digest": "EE664438FDF0535C6344A468181E4DDD4A34AC89582D4FD6E9E8954B843C7AA7",
                    "verifyResult": {
                            "matchConfidence": 0.08172279,
                            "isIdentical": false
                        }
                    }
                }
            ],
            "verifyReferences": [
            {
                "faceRectangle": {
                    "top": 98,
                    "left": 131,
                    "width": 233,
                    "height": 300
                    },
                "qualityForRecognition": "high"
            }
            ]
        }
    }
    ```

1. The app server can delete the session if you don't query its result anymore.

    #### [C#](#tab/csharp)
    ```csharp
    await sessionClient.DeleteLivenessWithVerifySessionAsync(sessionId);
    Console.WriteLine($"The session {sessionId} is deleted.");
    ```

    #### [Java](#tab/java)
    ```java
    sessionClient.deleteLivenessWithVerifySession(creationResult.getSessionId());
    System.out.println("The session " + creationResult.getSessionId() + " is deleted.");
    ```

    #### [Python](#tab/python)
    ```python
    await face_session_client.delete_liveness_with_verify_session(
        created_session.session_id
    )
    print(f"The session {created_session.session_id} is deleted.")
    await face_session_client.close()
    ```

    #### [JavaScript](#tab/javascript)
    ```javascript
    const deleteLivenessSessionResponse = await client.path('/detectLivenesswithVerify/singleModal/sessions/{sessionId}', createLivenessSessionResponse.body.sessionId).delete();
    if (isUnexpected(deleteLivenessSessionResponse)) {
        throw new Error(deleteLivenessSessionResponse.body.error.message);
    }
    console.log(`The session ${createLivenessSessionResponse.body.sessionId} is deleted.`);
    ```

    #### [REST API (Windows)](#tab/cmd)
    ```console
    curl --request DELETE --location "%FACE_ENDPOINT%/face/v1.2/detectLivenesswithVerify-sessions/<session-id>" ^
    --header "Ocp-Apim-Subscription-Key: %FACE_APIKEY%"
    ```

    #### [REST API (Linux)](#tab/bash)
    ```bash
    curl --request DELETE --location "${FACE_ENDPOINT}/face/v1.2/detectLivenesswithVerify-sessions/<session-id>" \
    --header "Ocp-Apim-Subscription-Key: ${FACE_APIKEY}"
    ```
    ---


## Perform other face operations after liveness detection

Optionally, you can do further face operations after the liveness check, such as face analysis (to get face attributes, for example) and/or face identity operations.
1. To enable this, you'll need to set the "enableSessionImage" parameter to "true" during the [Session-Creation step](#perform-liveness-detection).  
1. After the session completes, you can extract the "sessionImageId" from the [Session-Get-Result step](#perform-liveness-detection).
1. You can now either download the session-image (referenced in [Liveness Get Session Image Operation API](/rest/api/face/liveness-session-operations/get-session-image)), or provide the "sessionImageId" in the [Detect from Session Image ID API](/rest/api/face/face-detection-operations/detect-from-session-image-id) operation to continue to perform other face analysis or face identity operations. 
For more information on these operations, see [Face detection concepts](../concept-face-detection.md) and [Face Recognition concepts](../concept-face-recognition.md). 


## Support options

In addition to using the main [Azure AI services support options](../../cognitive-services-support-options.md), you can also post your questions in the [issues](https://github.com/Azure-Samples/azure-ai-vision-sdk/issues) section of the SDK repo. 


## Related content

To learn how to integrate the liveness solution into your existing application, see the Azure AI Vision SDK reference.

- [Kotlin (Android)](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-android-readme)
- [Swift (iOS)](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-ios-readme)
- [JavaScript (Web)](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-web-readme)

To learn more about the features available to orchestrate the liveness solution, see the Session REST API reference.

- [Liveness Session Operations](/rest/api/face/liveness-session-operations)

