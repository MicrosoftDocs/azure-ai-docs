---
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/21/2024
ms.author: jboback
---

When you no longer need your project, you can delete it with the following **DELETE** request. Replace the placeholder values with your own values.   

```rest
{Endpoint}/language/authoring/analyze-text/projects/{projectName}?api-version={API-VERSION}
```

|Placeholder  |Value  | Example |
|---------|---------|---------|
|`{ENDPOINT}`     | The endpoint for authenticating your API request.   | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
|`{PROJECT-NAME}`     | The name for your project. This value is case-sensitive.  | `myProject` |
|`{API-VERSION}`     | The version of the API you are calling. The value referenced here is for the latest version released. See [Model lifecycle](../../../concepts/model-lifecycle.md#choose-the-model-version-used-on-your-data) to learn more about other available API versions.  | `2022-05-01` |

### Headers

Use the following header to authenticate your request. 

|Key|Value|
|--|--|
|Ocp-Apim-Subscription-Key| The key to your resource. Used for authenticating your API requests.|


Once you send your API request, you will receive a `202` response indicating success, which means your project has been deleted. A successful call results with an Operation-Location header used to check the status of the job.
