---
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/21/2024
ms.author: jboback
---

Use the following **GET** request to get the status of exporting your project assets. Replace the placeholder values below with your own values. 

### Request URL

```rest
{ENDPOINT}/language/authoring/analyze-text/projects/{PROJECT-NAME}/export/jobs/{JOB-ID}?api-version={API-VERSION}
``` 

|Placeholder  |Value  | Example |
|---------|---------|---------|
|`{ENDPOINT}`     | The endpoint for authenticating your API request.   | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
|`{PROJECT-NAME}`     | The name of your project. This value is case-sensitive.   | `myProject` |
|`{JOB-ID}`     | The ID for locating your model's training status. This is in the `location` header value you received in the previous step.  | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxx` |
|`{API-VERSION}`     | The version of the API you are calling. The value referenced here is for the latest version released. See [Model lifecycle](../../../concepts/model-lifecycle.md#choose-the-model-version-used-on-your-data) to learn more about other available API versions.  | `2022-05-01` |

### Headers

Use the following header to authenticate your request. 

|Key|Value|
|--|--|
|`Ocp-Apim-Subscription-Key`| The key to your resource. Used for authenticating your API requests.|

### Response body

```json
{
  "resultUrl": "{RESULT-URL}",
  "jobId": "string",
  "createdDateTime": "2021-10-19T23:24:41.572Z",
  "lastUpdatedDateTime": "2021-10-19T23:24:41.572Z",
  "expirationDateTime": "2021-10-19T23:24:41.572Z",
  "status": "unknown",
  "errors": [
    {
      "code": "unknown",
      "message": "string"
    }
  ]
}
```

Use the URL from the `resultUrl` key in the body to view the exported assets from this job.

### Get export results

Submit a **GET** request using the `{RESULT-URL}` you received from the previous step to view the results of the export job.

#### Headers

Use the following header to authenticate your request. 

|Key|Value|
|--|--|
|`Ocp-Apim-Subscription-Key`| The key to your resource. Used for authenticating your API requests.|
