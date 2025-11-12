---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
Create a `POST` request by using the following URL, headers, and JSON body to export your project.

### Request URL

Use the following URL when you create your API request. Replace the placeholder values with your own values.

```rest
{ENDPOINT}/language/authoring/analyze-conversations/projects/{PROJECT-NAME}/:export?stringIndexType=Utf16CodeUnit&api-version={API-VERSION}
```

|Placeholder  |Value  | Example |
|---------|---------|---------|
|`{ENDPOINT}`     | The endpoint for authenticating your API request.   | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
|`{PROJECT-NAME}`     | The name for your project. This value is case sensitive.   | `EmailApp` |
|`{API-VERSION}`     | The [version](../../../concepts/model-lifecycle.md#api-versions) of the API that you're calling. | `2023-04-01` |

### Headers

Use the following header to authenticate your request.

|Key|Value|
|--|--|
|`Ocp-Apim-Subscription-Key`| The key to your resource. Used for authenticating your API requests.|

After you send your API request, you receive a `202` response that indicates success. In the response headers, extract the `operation-location` value. The value is formatted like this example:

```rest
{ENDPOINT}/language/authoring/analyze-conversations/projects/{PROJECT-NAME}/jobs/{JOB-ID}?api-version={API-VERSION}
``` 

`JOB-ID` is used to identify your request because this operation is asynchronous. Use this URL to get the exported project JSON by using the same authentication method.
