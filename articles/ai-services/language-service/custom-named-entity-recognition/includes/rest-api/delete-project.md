---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/05/2025
ms.author: lajanuar
---

When you no longer need your project, you can delete it with the following **DELETE** request. Replace the placeholder values with your own values.   

```rest
{Endpoint}/language/authoring/analyze-text/projects/{projectName}?api-version={API-VERSION}
```

|Placeholder  |Value  | Example |
|---------|---------|---------|
|`{ENDPOINT}`     | The endpoint for authenticating your API request.   | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
|`{PROJECT-NAME}`     | The name for your project. This value is case-sensitive.  | `myProject` |
<<<<<<< HEAD
|`{API-VERSION}`     | The version of the API you're calling. The value referenced is for the latest version released. For more information, *see* [Model lifecycle](../../../concepts/model-lifecycle.md#choose-the-model-version-used-on-your-data).| `2022-05-01` |
=======
|`{API-VERSION}`     | The version of the API you're calling. The value referenced here's for the latest version released. For more information, *see* [Model lifecycle](../../../concepts/model-lifecycle.md#choose-the-model-version-used-on-your-data).| `2022-05-01` |
>>>>>>> d843db8face108a14958aa31ff4bfac876de9b0e

### Headers

Use the following header to authenticate your request. 

|Key|Value|
|--|--|
|Ocp-Apim-Subscription-Key| The key to your resource. Used for authenticating your API requests.|


<<<<<<< HEAD
Once you send your API request, you receive a `202` response indicating success, which means your project is deleted. A successful call results with an Operation-Location header used to check the status of the job.
=======
Once you send your API request, your receive a `202` response indicating success, which means your project is deleted. A successful call results with an Operation-Location header used to check the status of the job.
>>>>>>> d843db8face108a14958aa31ff4bfac876de9b0e
