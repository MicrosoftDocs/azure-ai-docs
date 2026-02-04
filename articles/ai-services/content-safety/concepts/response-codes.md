---
title: "Content Safety error codes"
titleSuffix: Azure AI services
description: See the possible error codes and their corresponding suggestions for the Azure AI Content Safety APIs.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom: build-2023
ms.topic: error-reference
ms.date: 09/16/2025
ms.author: pafarley
---

# Azure AI Content Safety error codes 

The content APIs might return the following error codes:

| Error Code    | Possible reasons   | Suggestions           |
| ---------- | ------- | -------------------- |
| `InvalidRequestBody`  | One or more fields in the request body don't match the API definition. | Check the API version you specified in the API call. <br/>Check the corresponding API definition for the API version you selected. |
| `InvalidResourceName` | The resource name you specified in the URL doesn't meet the requirements, like the blocklist name, blocklist term ID, etc. | Check the API version you specified in the API call.  <br/>Check whether the given name has invalid characters according to the API definition. |
| `ResourceNotFound`    | The resource you specified in the URL might not exist, like the blocklist name. | Check the API version you specified in the API call. <br/>Double check the existence of the resource specified in the URL. |
| `InternalError`       | Some unexpected situations on the server side were triggered. | You might want to retry a few times after a small period and see it the issue happens again.  <br/>             Contact Azure Support if this issue persists. |
| `ServerBusy`          | The server side cannot process the request temporarily.      | You might want to retry a few times after a small period and see it the issue happens again.  <br/>Contact Azure Support if this issue persists. |
| `TooManyRequests`     | The current requests-per-second has exceeded the quota for your current tier. | Check the pricing table to understand the RPS quota.   <br/>Contact Azure Support if you need more QPS. |


## Azure AI Foundry error messages

If you encounter the error `Your account does not have access to this resource, please contact your resource owner to get access`, ensure your account is assigned the role of `Cognitive Services User` for the Content Safety resource or Azure AI Services resource you're using.

