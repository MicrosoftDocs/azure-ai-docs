---
title: Detect liveness in faces
description: In this Tutorial, you learn how to Detect liveness in faces, using both server-side code and a client-side mobile application.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.update-cycle: 90-days
ms.topic: tutorial
ms.date: 11/21/2025
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Tutorial: Detect liveness in faces

Learn how to integrate face liveness detection into your workflow by using server-side logic and companion frontend client applications.

> [!TIP]
> For general information about face liveness detection, see the [conceptual guide](../concept-face-liveness-detection.md).

In this tutorial, you learn how to run a frontend application with an app server to perform liveness detection. You can also add [face verification](#perform-liveness-detection-with-face-verification) across various platforms and languages.

[!INCLUDE [liveness-sdk-gate](../includes/liveness-sdk-gate.md)]

## Prerequisites

- Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- Your Azure account must have a **Cognitive Services Contributor** role assigned so you can agree to the responsible AI terms and create a resource. To get this role assigned to your account, follow the steps in the [Assign roles](/azure/role-based-access-control/role-assignments-steps) documentation, or contact your administrator. 
- Once you have your Azure subscription, <a href="https://portal.azure.com/#create/Microsoft.CognitiveServicesFace"  title="Create a Face resource"  target="_blank">create a Face resource</a> in the Azure portal to get your key and endpoint. After it deploys, select **Go to resource**. 
    - You need the key and endpoint from the resource you create to connect your application to the Face service.
- Access to the gated artifacts required for Azure Vision in Foundry Tools Face Client SDK for Mobile (iOS and Android) and Web. 
    - To get started, you need to apply for the [Face Recognition Limited Access features](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUQjA5SkYzNDM4TkcwQzNEOE1NVEdKUUlRRCQlQCN0PWcu) to get access to the gated artifacts. For more information, see the [Face Limited Access](/azure/ai-foundry/responsible-ai/computer-vision/limited-access-identity) page.
- Familiarity with the Face liveness detection feature. See the [conceptual guide](../concept-face-liveness-detection.md).

> [!TIP]
> After completing the prerequisites, you can try the liveness experience on the following platforms:<br>
> - iOS: [iOS App Store](https://aka.ms/face/liveness/demo/ios) — tap the app screen 10 times after installation to enable developer mode.<br>
> - Android: [Google Play Store](https://aka.ms/face/liveness/demo/android) — tap the app screen 10 times after installation to enable developer mode.<br>
> - Web: Try it directly in [Vision Studio](https://portal.vision.cognitive.azure.com/demo/face-liveness-detection).<br>
>
> You can also build and run a complete frontend sample (iOS, Android, or Web) from the [Samples](https://github.com/Azure-Samples/azure-ai-vision-sdk/tree/main?tab=readme-ov-file#samples) section.<br>

## Prepare the frontend application

We provide SDKs in multiple languages to simplify integration with your frontend application. Refer to the README for your chosen SDK in the following sections to integrate both the UI and required code.

> [!IMPORTANT]
> Each frontend SDK requires access to a gated asset to successfully compile. See the following instructions to set up this access.

For Swift iOS:
- Artifacts: [Azure AI Face UI SDK for iOS](https://github.com/Azure/AzureAIVisionFaceUI)
- API reference: [AzureAIVisionFaceUI Reference](https://azure.github.io/azure-sdk-for-ios/AzureAIVisionFaceUI/index.html)
- Sample: [iOS sample](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-ios-readme) 

For Kotlin/Java Android:
- Artifacts: Maven Central: [com.azure:azure-ai-vision-face-ui](https://central.sonatype.com/artifact/com.azure/azure-ai-vision-face-ui/overview)
- API reference: [azure-ai-vision-face-ui Reference](https://azure.github.io/azure-sdk-for-android/azure-ai-vision-face-ui/index.html) 
- Sample: [Android sample](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-android-readme)  

For JavaScript Web:
- Artifacts: [@azure/ai-vision-face-ui - npm](https://www.npmjs.com/package/@azure/ai-vision-face-ui?activeTab=readme)
- API reference: [AzureAIVisionFaceUI Reference](https://orange-forest-0ea70d510.5.azurestaticapps.net/)
- Sample: [Web sample](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-web-readme) 
- Framework Support: Works with popular frameworks such as React (including Next.js), Vue.js, and Angular.

Once integrated into your frontend application, the SDK starts the camera, guides the user to adjust their position, composes the liveness payload, and sends it to the Azure AI Face service for processing.

Monitor the repository’s [Releases section](https://github.com/Azure-Samples/azure-ai-vision-sdk/releases) for new SDK version updates and enable automated dependency update alerts—such as GitHub Dependabot (for GitHub repos) or Renovate (GitHub, GitLab, Bitbucket, Azure Repos).

## Perform liveness detection

The following steps describe the liveness orchestration process:  

:::image type="content" source="../media/liveness/liveness-diagram.jpg" alt-text="Diagram of the liveness workflow in Azure AI Face." lightbox="../media/liveness/liveness-diagram.jpg":::

1. The frontend application starts the liveness check and notifies the app server. 

1. The app server creates a new liveness session with Azure AI Face Service. The service creates a liveness session and responds with a session authorization token. For more information about each request parameter involved in creating a liveness session, see [Liveness Create Session Operation](https://aka.ms/face-api-reference-createlivenesssession).

    #### [C#](#tab/csharp)
    ```csharp
    var endpoint = new Uri(System.Environment.GetEnvironmentVariable("FACE_ENDPOINT"));
    var key = new AzureKeyCredential(System.Environment.GetEnvironmentVariable("FACE_APIKEY"));

    var body = JsonSerializer.Serialize(new
    {
        livenessOperationMode = "PassiveActive",
        deviceCorrelationId = "723d6d03-ef33-40a8-9682-23a1feb7bccd",
        enableSessionImage = true
    });

    using var client = new HttpClient();
    client.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", key);

    var response = await client.PostAsync(
        $"{endpoint}/face/v1.2/detectLiveness-sessions",
        new StringContent(body, Encoding.UTF8, "application/json"));

    response.EnsureSuccessStatusCode();

    using var doc  = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
    var root       = doc.RootElement;

    Console.WriteLine("Session created");
    Console.WriteLine($"sessionId : {root.GetProperty("sessionId").GetString()}");
    Console.WriteLine($"authToken : {root.GetProperty("authToken").GetString()}");
    ```

    #### [Java](#tab/java)
    ```java
    String endpoint = System.getenv("FACE_ENDPOINT");
    String key = System.getenv("FACE_APIKEY");

    String body = """
    {
        "livenessOperationMode": "PassiveActive",
        "deviceCorrelationId": "723d6d03-ef33-40a8-9682-23a1feb7bccd",
        "enableSessionImage": true,
    }
    """;

    HttpRequest req = HttpRequest.newBuilder()
            .uri(URI.create(endpoint + "/face/v1.2/detectLiveness-sessions"))
            .header("Content-Type", "application/json")
            .header("Ocp-Apim-Subscription-Key", key)
            .POST(HttpRequest.BodyPublishers.ofString(body))
            .build();

    HttpResponse<String> res = HttpClient.newHttpClient()
            .send(req, HttpResponse.BodyHandlers.ofString());

    if (res.statusCode() != 200) throw new RuntimeException("HTTP error: " + res.statusCode());

    JsonNode json = new ObjectMapper().readTree(res.body());
    System.out.println("Session created");
    System.out.println("sessionId : " + json.get("sessionId").asText());
    System.out.println("authToken : " + json.get("authToken").asText());
    ```

    #### [Python](#tab/python)
    ```python
    endpoint = os.environ["FACE_ENDPOINT"]
    key = os.environ["FACE_APIKEY"]

    url  = f"{endpoint}/face/v1.2/detectLiveness-sessions"
    body = {
        "livenessOperationMode": "PassiveActive",
        "deviceCorrelationId":  "723d6d03-ef33-40a8-9682-23a1feb7bccd",
        "enableSessionImage":   True
    }

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    res = requests.post(url, headers=headers, data=json.dumps(body))
    res.raise_for_status()

    data = res.json()
    print("Session created")
    print("sessionId :", data["sessionId"])
    print("authToken :", data["authToken"])
    ```

    #### [JavaScript](#tab/javascript)
    ```javascript
    const endpoint = process.env['FACE_ENDPOINT'];
    const apikey = process.env['FACE_APIKEY'];

    const url  = `${endpoint}/face/v1.2/detectLiveness-sessions`;
    const body = {
        livenessOperationMode: "PassiveActive",
        deviceCorrelationId:  "723d6d03-ef33-40a8-9682-23a1feb7bccd",
        enableSessionImage:   true
    };

    const headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    };

    async function createLivenessSession() {
        const res = await fetch(url, {
            method: "POST",
            headers,
            body: JSON.stringify(body)
        });

        if (!res.ok) {
            throw new Error(`${res.status} ${await res.text()}`);
        }

        const data = await res.json();
        console.log("Session created");
        console.log("sessionId :", data.sessionId);
        console.log("authToken :", data.authToken);
    }
    ```

    #### [REST API (Windows)](#tab/cmd)
    ```console
    curl --request POST --location "%FACE_ENDPOINT%/face/v1.2/detectLiveness-sessions" ^
    --header "Ocp-Apim-Subscription-Key: %FACE_APIKEY%" ^
    --header "Content-Type: application/json" ^
    --data ^
    "{ ^
        ""livenessOperationMode"": ""passiveactive"", ^
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
        "livenessOperationMode": "passiveactive",
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
        "modelVersion": "2025-05-20",
        "results": {
            "attempts": []
        }
    }
    ```

1. The app server provides the session authorization token back to the frontend application. 

1. The frontend application uses the session authorization token to start the face liveness detector, which kicks off the liveness flow.

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

1. The SDK starts the camera, guides the user to position correctly, and then prepares the payload to call the liveness detection service endpoint. 
 
1. The SDK calls Azure Vision Face service to perform the liveness detection. Once the service responds, the SDK notifies the frontend application that the liveness check is complete. Note: The service response doesn't contain the liveness decision. You need to query this information from the app server.

1. The frontend application relays the liveness check completion to the app server. 

1. The app server queries for the liveness detection result from Azure Vision Face service. 

    #### [C#](#tab/csharp)
    ```csharp
    using var client = new HttpClient();
    client.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", key);

    var response = await client.GetAsync(
        $"{endpoint}/face/v1.2/livenessSessions/{sessionId}/result");

    response.EnsureSuccessStatusCode();

    using var doc = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
    var root = doc.RootElement;
    var attempts = root.GetProperty("results").GetProperty("attempts");
    var latestAttempt = attempts[attempts.GetArrayLength() - 1];
    var attemptStatus = latestAttempt.GetProperty("attemptStatus").GetString();

    Console.WriteLine($"Session id: {root.GetProperty("sessionId").GetString()}");
    Console.WriteLine($"Session status: {root.GetProperty("status").GetString()}");
    Console.WriteLine($"Latest attempt status: {attemptStatus}");

    if (attemptStatus == "Succeeded")
        Console.WriteLine($"Liveness detection decision: {latestAttempt.GetProperty("result").GetProperty("livenessDecision").GetString()}");
    else
    {
        var error = latestAttempt.GetProperty("error");
        Console.WriteLine($"Error: {error.GetProperty("code").GetString()} - {error.GetProperty("message").GetString()}");
    }
    ```

    #### [Java](#tab/java)
    ```java
    HttpRequest req = HttpRequest.newBuilder()
        .uri(URI.create(endpoint + "/face/v1.2/livenessSessions/" + sessionId + "/result"))
        .header("Ocp-Apim-Subscription-Key", key)
        .GET()
        .build();

    HttpResponse<String> res = HttpClient.newHttpClient()
        .send(req, HttpResponse.BodyHandlers.ofString());

    if (res.statusCode() != 200) throw new RuntimeException("HTTP error: " + res.statusCode());

    JsonNode root = new ObjectMapper().readTree(res.body());
    JsonNode attempts = root.path("results").path("attempts");
    JsonNode latestAttempt = attempts.get(attempts.size() - 1);

    String attemptStatus = latestAttempt.path("attemptStatus").asText();

    System.out.println("Session id: " + root.path("sessionId").asText());
    System.out.println("Session status: " + root.path("status").asText());
    System.out.println("Latest attempt status: " + attemptStatus);

    if ("Succeeded".equals(attemptStatus)) {
        System.out.println("Liveness detection decision: " +
            latestAttempt.path("result").path("livenessDecision").asText());
    } else {
        JsonNode error = latestAttempt.path("error");
        System.out.println("Error: " + error.path("code").asText() + " - " +
            error.path("message").asText());
    }
    ```

    #### [Python](#tab/python)
    ```python
    url = f"{endpoint}/face/v1.2/livenessSessions/{sessionId}/result"
    headers = { "Ocp-Apim-Subscription-Key": key }

    res = requests.get(url, headers=headers)
    res.raise_for_status()

    data = res.json()
    attempts = data["results"]["attempts"]
    latest_attempt = attempts[-1]
    attempt_status = latest_attempt.get("attemptStatus")

    print(f"Session id: {data['sessionId']}")
    print(f"Session status: {data['status']}")
    print(f"Latest attempt status: {attempt_status}")

    if attempt_status == "Succeeded":
        print(f"Liveness detection decision: {latest_attempt['result']['livenessDecision']}")
    else:
        err = latest_attempt.get("error", {})
        print(f"Error: {err.get('code')} - {err.get('message')}")
    ```

    #### [JavaScript](#tab/javascript)
    ```javascript
    const url = `${endpoint}/face/v1.2/livenessSessions/${sessionId}/result`;
    const headers = {
        "Ocp-Apim-Subscription-Key": apikey
    };

    async function getLivenessSessionResult() {
        const res = await fetch(url, { method: "GET", headers });
        if (!res.ok) {
            throw new Error(`${res.status} ${await res.text()}`);
        }

        const data = await res.json();
        const attempts = data.results.attempts;
        const latestAttempt = attempts[attempts.length - 1];
        const attemptStatus = latestAttempt.attemptStatus;

        console.log("Session id :", data.sessionId);
        console.log("Session status :", data.status);
        console.log("Latest attempt status :", attemptStatus);

        if (attemptStatus === "Succeeded") {
            console.log("Liveness detection decision :", latestAttempt.result.livenessDecision);
        } else {
                const err = latestAttempt.error || {};
                console.log(`Error: ${err.code} - ${err.message}`);
        }
    }
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
        "sessionId": "b12e033e-bda7-4b83-a211-e721c661f30e",
        "authToken": "eyJhbGciOiJFUzI1NiIsIm",
        "status": "NotStarted",
        "modelVersion": "2024-11-15",
        "results": {
            "attempts": [
                {
                    "attemptId": 2,
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
                    "digest": "B0A803BB7B26F3C8F29CD36030F8E63ED3FAF955FEEF8E01C88AB8FD89CCF761",
                    "sessionImageId": "Ae3PVWlXAmVAnXgkAFt1QSjGUWONKzWiSr2iPh9p9G4I"
                    }
                },
                {
                    "attemptId": 1,
                    "attemptStatus": "Failed",
                    "error": {
                    "code": "FaceWithMaskDetected",
                    "message": "Mask detected on face image.",
                    "targets": {
                            "color": {
                            "faceRectangle": {
                                "top": 669,
                                "left": 203,
                                "width": 646,
                                "height": 724
                            }
                            }
                        }
                    }
                }
            ]
        }
    }
    ```

1. The app server deletes the session after it queries all session results.

    #### [C#](#tab/csharp)
    ```csharp
    using var client = new HttpClient();
    client.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", key);

    await client.DeleteAsync($"{endpoint}/face/v1.2/livenessSessions/{sessionId}");
    Console.WriteLine($"Session deleted: {sessionId}");
    ```

    #### [Java](#tab/java)
    ```java
    HttpRequest req = HttpRequest.newBuilder()
        .uri(URI.create(endpoint + "/face/v1.2/livenessSessions/" + sessionId))
        .header("Ocp-Apim-Subscription-Key", key)
        .DELETE()
        .build();

    HttpClient.newHttpClient().send(req, HttpResponse.BodyHandlers.ofString());
    System.out.println("Session deleted: " + sessionId);
    ```

    #### [Python](#tab/python)
    ```python
    headers = { "Ocp-Apim-Subscription-Key": key }
    requests.delete(f"{endpoint}/face/v1.2/livenessSessions/{sessionId}", headers=headers)
    print(f"Session deleted: {sessionId}")
    ```

    #### [JavaScript](#tab/javascript)
    ```javascript
    const headers = { "Ocp-Apim-Subscription-Key": apikey };
    await fetch(`${endpoint}/face/v1.2/livenessSessions/${sessionId}`, { method: "DELETE", headers });
    console.log(`Session deleted: ${sessionId}`);
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

Integrating liveness detection with verification involves two parts:

### Step 1 - Select a reference image

To get the most accurate recognition results, follow the tips listed in the [composition requirements for ID verification scenarios](../overview-identity.md#input-requirements).


### Step 2 - Set up the orchestration of liveness with verification

The following high-level steps show how to orchestrate liveness with verification:
1. Provide the verification reference image by using one of the following two methods:
    - The app server provides the reference image when creating the liveness session. For more information about each request parameter involved in creating a liveness session with verification, see [Liveness With Verify Create Session Operation](https://aka.ms/face-api-reference-createlivenesswithverifysession).

        #### [C#](#tab/csharp)
        ```csharp
        var endpoint = new Uri(System.Environment.GetEnvironmentVariable("FACE_ENDPOINT"));
        var key      = System.Environment.GetEnvironmentVariable("FACE_APIKEY");

        // Create the JSON part
        var jsonPart = new StringContent(
            JsonSerializer.Serialize(new
            {
                livenessOperationMode = "PassiveActive",
                deviceCorrelationId = "723d6d03-ef33-40a8-9682-23a1feb7bcc",
                enableSessionImage = true
            }),
            Encoding.UTF8,
            "application/json"
        );
        jsonPart.Headers.ContentDisposition = new ContentDispositionHeaderValue("form-data")
        {
            Name = "CreateLivenessWithVerifySessionRequest"
        };

        // Create the file part
        using var fileStream = File.OpenRead("test.png");
        var filePart = new StreamContent(fileStream);
        filePart.Headers.ContentType = new MediaTypeHeaderValue("image/png");
        filePart.Headers.ContentDisposition = new ContentDispositionHeaderValue("form-data")
        {
            Name = "VerifyImage",
            FileName = "test.png"
        };

        // Build multipart form data
        using var formData = new MultipartFormDataContent();
        formData.Add(jsonPart);
        formData.Add(filePart);

        using var client = new HttpClient();
        client.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", key);

        var response = await client.PostAsync($"{endpoint}/face/v1.2/createLivenessWithVerifySession", formData);
        response.EnsureSuccessStatusCode();

        using var doc = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        var root = doc.RootElement;

        Console.WriteLine("Session created.");
        Console.WriteLine($"Session id: {root.GetProperty("sessionId").GetString()}");
        Console.WriteLine($"Auth token: {root.GetProperty("authToken").GetString()}");
        ```

        #### [Java](#tab/java)
        ```java
        String endpoint = System.getenv("FACE_ENDPOINT");
        String key      = System.getenv("FACE_APIKEY");

        String json = """
        {
        "livenessOperationMode": "PassiveActive",
        "deviceCorrelationId": "723d6d03-ef33-40a8-9682-23a1feb7bcc",
        "enableSessionImage": true
        }
        """;

        byte[] img = Files.readAllBytes(Path.of("test.png"));
        String boundary = "----faceBoundary" + java.util.UUID.randomUUID();

        var head =
            "--" + boundary + "\r\n" +
            "Content-Disposition: form-data; name=\"CreateLivenessWithVerifySessionRequest\"\r\n" +
            "Content-Type: application/json\r\n\r\n" +
            json + "\r\n" +
            "--" + boundary + "\r\n" +
            "Content-Disposition: form-data; name=\"VerifyImage\"; filename=\"test.png\"\r\n" +
            "Content-Type: image/png\r\n\r\n";

        var tail = "\r\n--" + boundary + "--\r\n";

        byte[] body = java.nio.ByteBuffer
            .allocate(head.getBytes(StandardCharsets.UTF_8).length + img.length + tail.getBytes(StandardCharsets.UTF_8).length)
            .put(head.getBytes(StandardCharsets.UTF_8))
            .put(img)
            .put(tail.getBytes(StandardCharsets.UTF_8))
            .array();

        HttpRequest req = HttpRequest.newBuilder()
            .uri(URI.create(endpoint + "/face/v1.2/createLivenessWithVerifySession"))
            .header("Ocp-Apim-Subscription-Key", key)
            .header("Content-Type", "multipart/form-data; boundary=" + boundary)
            .POST(HttpRequest.BodyPublishers.ofByteArray(body))
            .build();

        HttpResponse<String> res = HttpClient.newHttpClient().send(req, HttpResponse.BodyHandlers.ofString());
        if (res.statusCode() != 200) throw new RuntimeException("HTTP error: " + res.statusCode());

        JsonNode root = new ObjectMapper().readTree(res.body());
        System.out.println("Session created.");
        System.out.println("Session id: " + root.get("sessionId").asText());
        System.out.println("Auth token: " + root.get("authToken").asText());
        ```

        #### [Python](#tab/python)
        ```python
        endpoint = os.environ["FACE_ENDPOINT"]
        key      = os.environ["FACE_APIKEY"]

        url = f"{endpoint}/face/v1.2/createLivenessWithVerifySession"
        files = {
            "CreateLivenessWithVerifySessionRequest": (
                "request.json",
                json.dumps({
                    "livenessOperationMode": "PassiveActive",
                    "deviceCorrelationId": "723d6d03-ef33-40a8-9682-23a1feb7bcc",
                    "enableSessionImage": True
                }),
                "application/json"
            ),
            "VerifyImage": ("test.png", open("test.png", "rb"), "image/png")
        }
        headers = { "Ocp-Apim-Subscription-Key": key }

        res = requests.post(url, headers=headers, files=files)
        res.raise_for_status()

        data = res.json()
        print("Session created.")
        print("Session id:", data["sessionId"])
        print("Auth token:", data["authToken"])
        ```

        #### [JavaScript](#tab/javascript)
        ```javascript
        const endpoint = process.env["FACE_ENDPOINT"];
        const apikey   = process.env["FACE_APIKEY"];

        const form = new FormData();
        form.append(
            "CreateLivenessWithVerifySessionRequest",
            new Blob([JSON.stringify({
                livenessOperationMode: "PassiveActive",
                deviceCorrelationId: "723d6d03-ef33-40a8-9682-23a1feb7bcc",
                enableSessionImage: true
            })], { type: "application/json" }),
            "request.json"
        );
        // If your runtime doesn't support Blob here, you can use fs.createReadStream instead.
        form.append("VerifyImage", new Blob([fs.readFileSync("test.png")], { type: "image/png" }), "test.png");

        const res = await fetch(`${endpoint}/face/v1.2/createLivenessWithVerifySession`, {
            method: "POST",
            headers: { "Ocp-Apim-Subscription-Key": apikey },
            body: form
        });
        if (!res.ok) {
            throw new Error(`${res.status} ${await res.text()}`);
        }

        const data = await res.json();
        console.log("Session created.");
        console.log("Session id:", data.sessionId);
        console.log("Auth token:", data.authToken);
        ```

        #### [REST API (Windows)](#tab/cmd)
        ```console
        curl --request POST --location "%FACE_ENDPOINT%/face/v1.2/detectLivenesswithVerify-sessions" ^
        --header "Ocp-Apim-Subscription-Key: %FACE_APIKEY%" ^
        --form "Parameters=""{\\\""livenessOperationMode\\\"": \\\""passiveactive\\\"", \\\""deviceCorrelationId\\\"": \\\""723d6d03-ef33-40a8-9682-23a1feb7bccd\\\"", ""enableSessionImage"": ""true""}""" ^
        --form "VerifyImage=@""test.png"""
        ```

        #### [REST API (Linux)](#tab/bash)
        ```bash
        curl --request POST --location "${FACE_ENDPOINT}/face/v1.2/detectLivenesswithVerify-sessions" \
        --header "Ocp-Apim-Subscription-Key: ${FACE_APIKEY}" \
        --form 'Parameters="{
            \"livenessOperationMode\": \"passiveactive\",
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

    - The frontend application provides the reference image when initializing the mobile SDKs. This scenario isn't supported in the web solution.

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
    using var client = new HttpClient();
    client.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", key);

    var response = await client.GetAsync($"{endpoint}/face/v1.2/livenessSessions/{sessionId}/result");
    response.EnsureSuccessStatusCode();

    using var doc = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
    var root = doc.RootElement;

    var attempts = root.GetProperty("results").GetProperty("attempts");
    var latestAttempt = attempts[attempts.GetArrayLength() - 1];
    var attemptStatus = latestAttempt.GetProperty("attemptStatus").GetString();

    Console.WriteLine($"Session id: {root.GetProperty("sessionId").GetString()}");
    Console.WriteLine($"Session status: {root.GetProperty("status").GetString()}");
    Console.WriteLine($"Latest attempt status: {attemptStatus}");

    if (attemptStatus == "Succeeded")
    {
        var decision = latestAttempt.GetProperty("result").GetProperty("livenessDecision").GetString();
        var verify   = latestAttempt.GetProperty("verifyResult");
        Console.WriteLine($"Liveness detection decision: {decision}");
        Console.WriteLine($"Verify isIdentical: {verify.GetProperty("isIdentical").GetBoolean()}");
        Console.WriteLine($"Verify matchConfidence: {verify.GetProperty("matchConfidence").GetDouble()}");
    }
    else
    {
        var err = latestAttempt.GetProperty("error");
        Console.WriteLine($"Error: {err.GetProperty("code").GetString()} - {err.GetProperty("message").GetString()}");
    }
    ```

    #### [Java](#tab/java)
    ```java
    HttpRequest req = HttpRequest.newBuilder()
        .uri(URI.create(endpoint + "/face/v1.2/livenessSessions/" + sessionId + "/result"))
        .header("Ocp-Apim-Subscription-Key", key)
        .GET()
        .build();

    HttpResponse<String> res = HttpClient.newHttpClient().send(req, HttpResponse.BodyHandlers.ofString());
    if (res.statusCode() != 200) throw new RuntimeException("HTTP error: " + res.statusCode());

    ObjectMapper om = new ObjectMapper();
    JsonNode root = om.readTree(res.body());

    JsonNode attempts = root.path("results").path("attempts");
    JsonNode latest   = attempts.get(attempts.size() - 1);
    String attemptStatus = latest.path("attemptStatus").asText();

    System.out.println("Session id: " + root.path("sessionId").asText());
    System.out.println("Session status: " + root.path("status").asText());
    System.out.println("Latest attempt status: " + attemptStatus);

    if ("Succeeded".equals(attemptStatus)) {
        String decision = latest.path("result").path("livenessDecision").asText();
        JsonNode verify = latest.path("verifyResult");
        System.out.println("Liveness detection decision: " + decision);
        System.out.println("Verify isIdentical: " + verify.path("isIdentical").asBoolean());
        System.out.println("Verify matchConfidence: " + verify.path("matchConfidence").asDouble());
    } else {
        JsonNode err = latest.path("error");
        System.out.println("Error: " + err.path("code").asText() + " - " + err.path("message").asText());
    }
    ```

    #### [Python](#tab/python)
    ```python
    url = f"{endpoint}/face/v1.2/livenessSessions/{sessionId}/result"
    headers = {"Ocp-Apim-Subscription-Key": key}

    res = requests.get(url, headers=headers)
    res.raise_for_status()

    data = res.json()
    attempts = data["results"]["attempts"]
    latest = attempts[-1]
    attempt_status = latest.get("attemptStatus")

    print(f"Session id: {data['sessionId']}")
    print(f"Session status: {data['status']}")
    print(f"Latest attempt status: {attempt_status}")

    if attempt_status == "Succeeded":
        decision = latest["result"]["livenessDecision"]
        verify   = latest.get("verifyResult", {})
        print(f"Liveness detection decision: {decision}")
        print(f"Verify isIdentical: {verify.get('isIdentical')}")
        print(f"Verify matchConfidence: {verify.get('matchConfidence')}")
    else:
        err = latest.get("error", {})
        print(f"Error: {err.get('code')} - {err.get('message')}")
    ```

    #### [JavaScript](#tab/javascript)
    ```javascript
    const url = `${endpoint}/face/v1.2/livenessSessions/${sessionId}/result`;
    const headers = { "Ocp-Apim-Subscription-Key": apikey };

    async function getLivenessWithVerifyResult() {
    const res = await fetch(url, { method: "GET", headers });
    if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);

    const data = await res.json();
    const attempts = data.results.attempts;
    const latest = attempts[attempts.length - 1];
    const attemptStatus = latest.attemptStatus;

    console.log("Session id:", data.sessionId);
    console.log("Session status:", data.status);
    console.log("Latest attempt status:", attemptStatus);

    if (attemptStatus === "Succeeded") {
        console.log("Liveness detection decision:", latest.result.livenessDecision);
        console.log("Verify isIdentical:", latest.verifyResult?.isIdentical);
        console.log("Verify matchConfidence:", latest.verifyResult?.matchConfidence);
    } else {
        const err = latest.error || {};
        console.log(`Error: ${err.code} - ${err.message}`);
    }
    }
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
        "sessionId": "b12e033e-bda7-4b83-a211-e721c661f30e",
        "authToken": "eyJhbGciOiJFUzI1NiIsIm",
        "status": "NotStarted",
        "modelVersion": "2024-11-15",
        "results": {
            "attempts": [
            {
                "attemptId": 2,
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
                "verifyResult": {
                    "matchConfidence": 0.08871888,
                    "isIdentical": false
                },
                "digest": "B0A803BB7B26F3C8F29CD36030F8E63ED3FAF955FEEF8E01C88AB8FD89CCF761",
                "sessionImageId": "Ae3PVWlXAmVAnXgkAFt1QSjGUWONKzWiSr2iPh9p9G4I",
                "verifyImageHash": "43B7D8E8769533C3290DBD37A84D821B2C28CB4381DF9C6784DBC4AAF7E45018"
                }
            },
            {
                "attemptId": 1,
                "attemptStatus": "Failed",
                "error": {
                    "code": "FaceWithMaskDetected",
                    "message": "Mask detected on face image.",
                    "targets": {
                        "color": {
                        "faceRectangle": {
                                "top": 669,
                                "left": 203,
                                "width": 646,
                                "height": 724
                            }
                        }
                    }
                }
            }
            ],
            "verifyReferences": [
                {
                    "referenceType": "image",
                    "faceRectangle": {
                    "top": 316,
                    "left": 131,
                    "width": 498,
                    "height": 677
                    },
                    "qualityForRecognition": "high"
                }
            ]
            }
        }
    ```

1. The app server can delete the session if you don't need its result anymore.

    #### [C#](#tab/csharp)
    ```csharp
    using var client = new HttpClient();
    client.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", key);

    await client.DeleteAsync($"{endpoint}/face/v1.2/livenessWithVerifySessions/{sessionId}");
    Console.WriteLine($"Liveness-with-Verify session deleted: {sessionId}");
    ```

    #### [Java](#tab/java)
    ```java
    HttpRequest req = HttpRequest.newBuilder()
        .uri(URI.create(endpoint + "/face/v1.2/livenessWithVerifySessions/" + sessionId))
        .header("Ocp-Apim-Subscription-Key", key)
        .DELETE()
        .build();

    HttpClient.newHttpClient().send(req, HttpResponse.BodyHandlers.ofString());
    System.out.println("Liveness-with-Verify session deleted: " + sessionId);
    ```

    #### [Python](#tab/python)
    ```python
    headers = { "Ocp-Apim-Subscription-Key": key }
    requests.delete(f"{endpoint}/face/v1.2/livenessWithVerifySessions/{sessionId}", headers=headers)
    print(f"Liveness-with-Verify session deleted: {sessionId}")
    ```

    #### [JavaScript](#tab/javascript)
    ```javascript
    const headers = { "Ocp-Apim-Subscription-Key": apikey };
    await fetch(`${endpoint}/face/v1.2/livenessWithVerifySessions/${sessionId}`, { method: "DELETE", headers });
    console.log(`Liveness-with-Verify session deleted: ${sessionId}`);
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

Optionally, you can perform additional face operations after the liveness check, such as face analysis (to get face attributes) and face identity operations.
1. Set the `enableSessionImage` parameter to `true` during the [Session-Creation step](#perform-liveness-detection).  
1. Extract the `sessionImageId` from the [Session-Get-Result step](#perform-liveness-detection).
1. Download the session image (referenced in [Liveness Get Session Image Operation API](/rest/api/face/liveness-session-operations/get-session-image)), or provide the `sessionImageId` in the [Detect from Session Image ID API](/rest/api/face/face-detection-operations/detect-from-session-image-id) operation to continue with other face analysis or face identity operations. 
For more information on these operations, see [Face detection concepts](../concept-face-detection.md) and [Face Recognition concepts](../concept-face-recognition.md). 

## Support options

In addition to using the main [Foundry Tools support options](../../cognitive-services-support-options.md), you can also post your questions in the [issues](https://github.com/Azure-Samples/azure-ai-vision-sdk/issues) section of the SDK repo. 

## Related content

To learn how to integrate the liveness solution into your existing application, see the Azure Vision SDK reference.

- [Kotlin (Android)](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-android-readme)
- [Swift (iOS)](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-ios-readme)
- [JavaScript (Web)](https://aka.ms/azure-ai-vision-face-liveness-client-sdk-web-readme)

To learn more about the features available to orchestrate the liveness solution, see the Session REST API reference.

- [Liveness Session Operations](/rest/api/face/liveness-session-operations)