---
title: "Face liveness quick link - Face"
titleSuffix: Foundry Tools
description: This article explains the concept of Face liveness quick link, its usage flow, and related concepts. 
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

# Face Liveness quick link (preview)

This article explains the concept of Face liveness quick link, its usage flow, and related concepts.

## Introduction

Azure Face Liveness quick link is an optional integration path for [Face liveness detection](../concept-face-liveness-detection.md). It exchanges a liveness session’s session-authorization-token for a single-use URL that hosts the face capture experience on an Azure-operated page. The service returns to a developer-supplied callback endpoint after finishing the operation. 

Azure Liveness quick link provides multiple benefits to customers: 
- You don't need to embed the liveness client SDK. That allows for easier integration on the application side.
- You don't need to keep track of liveness client SDK updates. Azure-operated websites always use the latest version of liveness detection.

## How it works

You can use the liveness quick link website, `liveness.face.azure.com`, to turn a liveness session into a shareable, single use link:

:::image type="content" source="../media/liveness/liveness-quick-link-diagram.png" alt-text="A diagram illustrates liveness quick link work flow.":::

1.	Start a session with your server-side code. Your application backend requests a new liveness session from the Face API and receives a short-lived authorization token that represents that session.
2.	Swap the session token for a link. Your application backend sends the token to the quick link service, which creates a one-time URL connected to the session. Here are examples of the post request:

    #### [C#](#tab/csharp)
    ```csharp
    var client = new HttpClient();
    var request = new HttpRequestMessage
    {
        Method = HttpMethod.Post,
        RequestUri = new Uri("https://liveness.face.azure.com/api/quicklink"),
        Headers =
        {
            { "authorization", "Bearer  <session-authorization-token>" },
        },
    };
    using (var response = await client.SendAsync(request))
    {
        response.EnsureSuccessStatusCode();
        var body = await response.Content.ReadAsStringAsync();
        Console.WriteLine(body);
    }
    ```

    #### [Java](#tab/java)
    ```java
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://liveness.face.azure.com/api/quicklink"))
        .header("authorization", "Bearer <session-authorization-token>")
        .method("POST", HttpRequest.BodyPublishers.noBody())
        .build();
    HttpResponse<String> response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
    System.out.println(response.body());
    ```
    
    #### [Python](#tab/python)
    ```python
    import http.client
    
    conn = http.client.HTTPSConnection("liveness.face.azure.com")
    
    headers = {
        'authorization': "Bearer <session-authorization-token>"
        }
    
    conn.request("POST", "/api/quicklink", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    print(data.decode("utf-8"))
        
    ```
    
    #### [JavaScript](#tab/javascript)
    ```javascript
    fetch("https://liveness.face.azure.com/api/quicklink", {
      "method": "POST",
      "headers": {
        "authorization": "Bearer <session-authorization-token>"
      }
    })
    .then(response => {
      console.log(response);
    })
    .catch(err => {
      console.error(err);
    });
    ```

    #### [REST(Windows)](#tab/cmd)
    ```console
    curl --request POST ^
      --url https://liveness.face.azure.com/api/quicklink ^
      --header 'authorization: Bearer <session-authorization-token>'
    ```
    
    #### [REST(Linux)](#tab/bash)
    ```bash
    curl --request POST \
      --url https://liveness.face.azure.com/api/quicklink \
      --header 'authorization: Bearer <session-authorization-token>'
    ```

The following is an example response:
    
  ```json
  {
    "url": "/?s=60c3980c-d9f6-4b16-a7f5-f1f4ad2b506f"
  }
  ```

3. Compose the link and sent it to the user. Use the URL response value to construct the liveness quick link web page. Optionally you can also add a callback URL: `https://liveness.face.azure.com/?s=60c3980c-d9f6-4b16-a7f5-f1f4ad2b506f&&callbackUrl=<encoded url>` You can redirect the browser or show a button—anything that lets the user open the link on a device.
4. Azure hosts the capture experience. When the link opens, the Azure-operated page guides the user through the liveness check sequence using the latest Liveness web client.
5. Get the outcome callback. As soon as the check finishes—or if the user abandons or times out—the quick link service notifies your callback endpoint so your application can decide what happens next.

## Quick link URL handling

The URL returned by the quick link service is a bearer secret: anyone who possesses the link can initiate, complete, or cancel the associated liveness session. If a malicious party intercepts the link before the intended user opens it, they can consume or spoof the session and prevent the legitimate user from completing the check—creating a repudiation and impersonation risk. To minimize this risk, transmit the link only over protected channels, avoid persisting it in logs or analytics, and, when possible, lowering lifetime of the liveness session.
