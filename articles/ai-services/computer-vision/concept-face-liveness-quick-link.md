---
title: "Face liveness quick link - Face"
titleSuffix: Azure AI services
description: This article explains the concept of Face liveness quick link, its usage flow, and related concepts. 
author: JinyuID
manager: nitinme

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.custom:
ms.topic: conceptual
ms.date: 05/15/2025
ms.author: pafarley
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Face Liveness Quick Link (Preview)

This article explains the concept of Face liveness quick link, its usage flow, and related concepts.

## Introduction

Azure Liveness Quick Link is an optional integration path for [Face liveness detection](concept-face-liveness-detection.md). It exchanges a liveness session’s session-authorization-token for a single use URL that hosts the capture experience on an Azure operated page. The service returns to a developer supplied callback endpoint after finishing the operation. 

Azure Liveness Quick Link provides multiple benefits to customers: 
- No need to embed the liveness client SDK. Easier integration in application side.
- No need to keep track of liveness client SDK updates. Azure operated websites always use the latest and greatest version of liveness detection.

## How it works

You can utilize the liveness quick link website liveness.face.azure.com to turn a liveness session into a shareable, single use link:

:::image type="content" source="media/liveness/liveness-quick-link-diagram.png" alt-text="A diagram illustrates liveness quick link work flow":::

1.	Start a session server side. Your backend asks Face API for a new liveness session and receives a short lived authorization token that represents that session.
2.	Swap the token for a link. Your backend sends the token to the Quick Link service, which creates a one time URL tied to the session. here are examples to post request:

    #### [C#](#tab/csharp)
    ```csharp
    var client = new HttpClient();
    var request = new HttpRequestMessage
    {
        Method = HttpMethod.Post,
        RequestUri = new Uri("https://liveness.face.azure.com/api/s"),
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
        .uri(URI.create("https://liveness.face.azure.com/api/s"))
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
    
    conn.request("POST", "/api/s", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    print(data.decode("utf-8"))
        
    ```
    
    #### [JavaScript](#tab/javascript)
    ```javascript
    fetch("https://liveness.face.azure.com/api/s", {
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
      --url https://liveness.face.azure.com/api/s ^
      --header 'authorization: Bearer <session-authorization-token>'
    ```
    
    #### [REST(Linux)](#tab/bash)
    ```bash
    curl --request POST \
      --url https://liveness.face.azure.com/api/s \
      --header 'authorization: Bearer <session-authorization-token>'
    ```    

An example response:
```json
{
  "url": "/?s=60c3980c-d9f6-4b16-a7f5-f1f4ad2b506f"
}
```
Compose the returned url after liveness quick link web site `https://liveness.face.azure.com/?s=60c3980c-d9f6-4b16-a7f5-f1f4ad2b506f`

3.	Send the link to the user. You can redirect the browser, show a button, or display a QR code—anything that gets the user to open the link on a camera enabled device.
4.	Azure hosts the capture. When the link opens, the Azure operated page guides the user through the liveness check sequence using the latest Liveness Web Client.
5.	Get the outcome callback. As soon as the check finishes—or if the user abandons or times out—Quick Link notify to your callback endpoint so your application can decide what happens next.
