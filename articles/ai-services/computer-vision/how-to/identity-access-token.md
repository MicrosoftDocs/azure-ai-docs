---
title: "Use limited access tokens - Face"
titleSuffix: Azure AI services
description: Learn how ISVs can manage the Face API usage of their clients by issuing access tokens that grant access to Face features which are normally gated.
#services: cognitive-services
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.topic: how-to
ms.date: 03/07/2024
ms.author: pafarley
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Use limited access tokens for Face

Independent software vendors (ISVs) can manage the Face API usage of their clients by issuing access tokens that grant access to Face features which are normally gated. This allows their client companies to use the Face API without having to go through the formal approval process.

This guide shows you how to generate the access tokens, if you're an approved ISV, and how to use the tokens if you're a client. 

The limited access token feature is a part of the existing Azure AI Services token service. We have added a new operation for the purpose of bypassing the Limited Access gate for approved scenarios. 

> [!IMPORTANT]
> Only ISVs that pass the gating requirements will be given access to this feature. To request approval, contact [azureface@microsoft.com](mailto:azureface@microsoft.com).

## Example use case

An example company sells software that uses the Azure AI Face service to operate door access security systems. Their clients, individual manufacturers of door devices, subscribe to the software and run it on their devices. These client companies want to make Face API calls from their devices to perform Limited Access operations like face identification. By relying on access tokens from the ISV, they can bypass the formal approval process for face identification. The ISV, which has already been approved, can grant the client just-in-time access tokens.

## Expectation of responsibility

The token-issuing ISV is responsible for ensuring that the tokens are used only for the approved purpose.

If the ISV learns that a client is using the LimitedAccessToken for non-approved purposes, the ISV should stop generating tokens for that customer. Microsoft can track the issuance and usage of LimitedAccessTokens, and we reserve the right to revoke an ISV's access to the **issueLimitedAccessToken** API if abuse is not addressed.

## Prerequisites

* [cURL](https://curl.se/) installed (or another tool that can make HTTP requests).
* The ISV needs to have either an [Azure AI Face](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/Face) resource or an [Azure AI services multi-service](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/AllInOne) resource.
* The client needs to have an [Azure AI Face](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/Face) resource.

## Step 1: ISV obtains client's Face resource ID

The ISV should set up a communication channel between their own secure cloud service (which will generate the access token) and their application running on the client's device. The client's Face resource ID must be known prior to generating the LimitedAccessToken.

The Face resource ID has the following format:

`/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.CognitiveServices/accounts/<face-resource-name>`

For example:

`/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/client-rg/providers/Microsoft.CognitiveServices/accounts/client-face-api`

## Step 2: ISV generates a token

The ISV's cloud service, running in a secure environment, calls the **issueLimitedAccessToken** API using their end customer's known Face resource ID.

To call the **issueLimitedAccessToken** API, copy the following cURL command to a text editor.

```bash
curl -X POST 'https://<isv-endpoint>/sts/v1.0/issueLimitedAccessToken?expiredTime=3600' \  
-H 'Ocp-Apim-Subscription-Key: <isv-face-key>' \  
-H 'Content-Type: application/json' \  
-d '{  
    "targetAzureResourceId": "/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.CognitiveServices/accounts/<face-resource-name>",  
    "featureFlags": ["Face.Identification", "Face.Verification"]  
}' 
```

Then, make the following changes:
1. Replace `<isv-endpoint>` with the endpoint of the ISV's resource. For example, **westus.api.cognitive.microsoft.com**.
1. Optionally set the `expiredTime` parameter to set the expiration time of the token in seconds. It must be between 60 and 86400. The default value is 3600 (one hour).
1. Replace `<isv-face-key>` with the key of the ISV's Face resource.
1. Replace `<subscription-id>` with the subscription ID of the client's Azure subscription.
1. Replace `<resource-group-name>` with the name of the client's resource group.
1. Replace `<face-resource-name>` with the name of the client's Face resource.
1. Set `"featureFlags"` to the set of access roles you want to grant. The available flags are `"Face.Identification"`, `"Face.Verification"`, and `"LimitedAccess.HighRisk"`. An ISV can only grant permissions that it has been granted itself by Microsoft. For example, if the ISV has been granted access to face identification, it can create a LimitedAccessToken for **Face.Identification** for the client. All token creations and uses are logged for usage and security purposes.

Then, paste the command into a terminal window and run it.

The API should return a `200` response with the token in the form of a JSON web token (`application/jwt`). If you want to inspect the LimitedAccessToken, you can do so using [JWT](https://jwt.io/).

## Step 3: Client application uses the token

The ISV's application can then pass the limited access token as an HTTP request header for future Face API requests on behalf of the client. This works independently of other authentication mechanisms, so no personal information of the client's is ever leaked to the ISV. 

> [!CAUTION]
> The client doesn't need to be aware of the token value, as it can be passed in the background. If the client were to use a web monitoring tool to intercept the traffic, they'd be able to view the LimitedAccessToken header. However, because the token expires after a short period of time, they are limited in what they can do with it. This risk is known and considered acceptable.
>
> It's for each ISV to decide how exactly it passes the token from its cloud service to the client application.

#### [REST API](#tab/rest)

An example Face API request using the access token looks like this:

```bash
curl -X POST 'https://<client-endpoint>/face/v1.0/identify' \  
-H 'Ocp-Apim-Subscription-Key: <client-face-key>' \  
-H 'LimitedAccessToken: Bearer <token>' \  
-H 'Content-Type: application/json' \  
-d '{  
  "largePersonGroupId": "sample_group",  
  "faceIds": [  
    "c5c24a82-6845-4031-9d5d-978df9175426",  
    "65d083d4-9447-47d1-af30-b626144bf0fb"  
  ],  
  "maxNumOfCandidatesReturned": 1,  
  "confidenceThreshold": 0.5  
}'
```

> [!NOTE]
> The endpoint URL and Face key belong to the client's Face resource, not the ISV's resource. The `<token>` is passed as an HTTP request header.

#### [C#](#tab/csharp)

The following code snippets show you how to use an access token with the [Face SDK for C#](https://aka.ms/azsdk-csharp-face-pkg).

The following class uses an access token to create a **HttpPipelineSynchronousPolicy** object that can be used to authenticate a Face API client object. It automatically adds the access token as a header in every request that the Face client will make.

```csharp
public class LimitedAccessTokenPolicy : HttpPipelineSynchronousPolicy
{
    /// <summary>
    /// Creates a new instance of the LimitedAccessTokenPolicy class
    /// </summary>
    /// <param name="limitedAccessToken">LimitedAccessToken to bypass the limited access program, requires ISV sponsership.</param>
    public LimitedAccessTokenPolicy(string limitedAccessToken)
    {
        _limitedAccessToken = limitedAccessToken;
    }

    private readonly string _limitedAccessToken;

    /// <summary>
    /// Add the authentication header to each outgoing request
    /// </summary>
    /// <param name="message">The outgoing message</param>
    public override void OnSendingRequest(HttpMessage message)
    {
        message.Request.Headers.Add("LimitedAccessToken", $"Bearer {_limitedAccessToken}");
    }
}
```

In the client-side application, the helper class can be used like in this example:

```csharp
static void Main(string[] args)
{
    // create Face client object
    var clientOptions = new AzureAIVisionFaceClientOptions();
    clientOptions.AddPolicy(new LimitedAccessTokenPolicy("<token>"), HttpPipelinePosition.PerCall);
    FaceClient faceClient = new FaceClient(new Uri("<client-endpoint>"), new AzureKeyCredential("<client-face-key>"), clientOptions);

    // use Face client in an API call
    using (var stream = File.OpenRead("photo.jpg"))
    {
        var response = faceClient.Detect(BinaryData.FromStream(stream), FaceDetectionModel.Detection03, FaceRecognitionModel.Recognition04, returnFaceId: true);

        Console.WriteLine(JsonConvert.SerializeObject(response.Value));
    }
}
```
---
