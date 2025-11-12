---
titleSuffix: Foundry Tools
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
To get your project details, submit a `GET` request by using the following URL and headers. Replace the placeholder values with your own values.

```rest
{ENDPOINT}/language/authoring/analyze-conversations/projects/{PROJECT-NAME}?api-version={API-VERSION}
```

|Placeholder  |Value  | Example |
|---------|---------|---------|
|`{ENDPOINT}`     | The endpoint for authenticating your API request.   | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
|`{PROJECT-NAME}`     | The name for your project. This value is case sensitive.  | `myProject` |
|`{API-VERSION}`     | The [version](../../../concepts/model-lifecycle.md#api-versions) of the API that you're calling. | `2023-04-01` |

### Headers

Use the following header to authenticate your request.

|Key|Value|
|--|--|
|`Ocp-Apim-Subscription-Key`| The key to your resource. Used for authenticating your API requests.|

### Response body

After you send the request, you get the following response:

```json
{
  "createdDateTime": "2022-04-18T13:53:03Z",
  "lastModifiedDateTime": "2022-04-18T13:53:03Z",
  "lastTrainedDateTime": "2022-04-18T14:14:28Z",
  "lastDeployedDateTime": "2022-04-18T14:49:01Z",
  "projectKind": "Conversation",
  "projectName": "{PROJECT-NAME}",
  "multilingual": true,
  "description": "This is a sample conversation project.",
  "language": "{LANGUAGE-CODE}"
}
```

After you send your API request, you receive a `200` response that indicates success and includes a JSON response body with your project details.
