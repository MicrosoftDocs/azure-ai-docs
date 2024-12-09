---
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/21/2024
ms.author: jboback
---

Create a **POST** request using the following URL, headers, and JSON body to export your project.

### Request URL

Use the following URL when creating your API request. Replace the placeholder values below with your own values. 

```rest
{ENDPOINT}/language/authoring/analyze-text/projects/{PROJECT-NAME}/:export?stringIndexType=Utf16CodeUnit&api-version={API-VERSION}
```

|Placeholder  |Value  | Example |
|---------|---------|---------|
|`{ENDPOINT}`     | The endpoint for authenticating your API request.   | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
|`{PROJECT-NAME}`     | The name for your project. This value is case-sensitive.   | `MyProject` |
|`{API-VERSION}`     | The version of the API you are calling. The value referenced here is the latest [model version](../../../concepts/model-lifecycle.md#choose-the-model-version-used-on-your-data) released.  | `2022-05-01` |

### Headers

Use the following header to authenticate your request. 

|Key|Value|
|--|--|
|`Ocp-Apim-Subscription-Key`| The key to your resource. Used for authenticating your API requests.|

#### Body

Use the following JSON in your request body specifying that you want to export all the assets.

```json
{
  "assetsToExport": ["*"]
}
```

Once you send your API request, you’ll receive a `202` response indicating that the job was submitted correctly. In the response headers, extract the `operation-location` value. It will be formatted like this: 

```rest
{ENDPOINT}/language/authoring/analyze-text/projects/{PROJECT-NAME}/export/jobs/{JOB-ID}?api-version={API-VERSION}
``` 

`{JOB-ID}` is used to identify your request, since this operation is asynchronous. You’ll use this URL to get the export job status.
