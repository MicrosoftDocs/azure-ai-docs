---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
Submit a `POST` request by using the following URL, headers, and JSON body to import your project.

### Request URL

Use the following URL when you create your API request. Replace the placeholder values with your own values.

```rest
{ENDPOINT}/language/authoring/analyze-conversations/projects/{PROJECT-NAME}/:import?api-version={API-VERSION}
```

|Placeholder  |Value  | Example |
|---------|---------|---------|
|`{ENDPOINT}`     | The endpoint for authenticating your API request. | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
|`{PROJECT-NAME}`     | The name for your project. This value is case sensitive and must match the project name in the JSON file that you're importing. | `EmailAppDemo` |
|`{API-VERSION}`     | The [version](../../../concepts/model-lifecycle.md#api-versions) of the API that you're calling. | `2023-04-01` |

### Headers

Use the following header to authenticate your request.

|Key|Value|
|--|--|
|`Ocp-Apim-Subscription-Key`| The key to your resource. Used for authenticating your API requests.|

### Body

The JSON body you send is similar to the following example. For more information about the JSON object, see the [reference documentation](/rest/api/language/2023-04-01/conversational-analysis-authoring/import?tabs=HTTP#successful-import-project).

```json
{
  "projectFileVersion": "{API-VERSION}",
  "stringIndexType": "Utf16CodeUnit",
  "metadata": {
    "projectKind": "Conversation",
    "settings": {
      "confidenceThreshold": 0.7
    },
    "projectName": "{PROJECT-NAME}",
    "multilingual": true,
    "description": "Trying out CLU",
    "language": "{LANGUAGE-CODE}"
  },
  "assets": {
    "projectKind": "Conversation",
    "intents": [
      {
        "category": "intent1"
      },
      {
        "category": "intent2"
      }
    ],
    "entities": [
      {
        "category": "entity1"
      }
    ],
    "utterances": [
      {
        "text": "text1",
        "dataset": "{DATASET}",
        "intent": "intent1",
        "entities": [
          {
            "category": "entity1",
            "offset": 5,
            "length": 5
          }
        ]
      },
      {
        "text": "text2",
        "language": "{LANGUAGE-CODE}",
        "dataset": "{DATASET}",
        "intent": "intent2",
        "entities": []
      }
    ]
  }
}

```

|Key  |Placeholder  |Value  | Example |
|---------|---------|----------|--|
|`{API-VERSION}`     | The [version](../../../concepts/model-lifecycle.md#api-versions) of the API that you're calling. | `2023-04-01` |
| `projectName` | `{PROJECT-NAME}` | The name of your project. This value is case sensitive. | `EmailAppDemo` |
| `language` | `{LANGUAGE-CODE}` |  A string that specifies the language code for the utterances used in your project. If your project is a multilingual project, choose the [language code](../../language-support.md) of most of the utterances. |`en-us`|
| `multilingual` | `true`| A Boolean value that enables you to have documents in multiple languages in your dataset. When your model is deployed, you can query the model in any [supported language](../../language-support.md#multi-lingual-option), including languages that aren't included in your training documents. | `true`|
| `dataset` | `{DATASET}` |  For information on how to split your data between a testing and training set, see [Label your utterances in Foundry](../../how-to/tag-utterances.md). Possible values for this field are `Train` and `Test`. |`Train`|

After a successful request, the API response contains an `operation-location` header with a URL that you can use to check the status of the import job. The header is formatted like this example:

```http
{ENDPOINT}/language/authoring/analyze-conversations/projects/{PROJECT-NAME}/import/jobs/{JOB-ID}?api-version={API-VERSION}
``` 
