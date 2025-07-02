---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 06/30/2025
ms.author: lajanuar
---

Use this **POST** request to start a text classification task.

```rest
{ENDPOINT}/language/analyze-text/jobs?api-version={API-VERSION}
```

|Placeholder  |Value  | Example |
|---------|---------|---------|
|`{ENDPOINT}`     | The endpoint for authenticating your API request.   | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
|`{API-VERSION}`     | The version of the API you are calling. The value referenced here is for the latest version released. See [Model lifecycle](../../../concepts/model-lifecycle.md#choose-the-model-version-used-on-your-data) to learn more about other available API versions.  | `2022-05-01` |

#### Headers

|Key|Value|
|--|--|
|Ocp-Apim-Subscription-Key| Your key that provides access to this API.|

#### Body

# [Multi label classification](#tab/multi-classification)

```json
{
  "displayName": "Classifying documents",
  "analysisInput": {
    "documents": [
      {
        "id": "1",
        "language": "{LANGUAGE-CODE}",
        "text": "Text1"
      },
      {
        "id": "2",
        "language": "{LANGUAGE-CODE}",
        "text": "Text2"
      }
    ]
  },
  "tasks": [
     {
      "kind": "CustomMultiLabelClassification",
      "taskName": "Multi Label Classification",
      "parameters": {
        "projectName": "{PROJECT-NAME}",
        "deploymentName": "{DEPLOYMENT-NAME}"
      }
    }
  ]
}
```

|Key  |Placeholder  |Value  | Example |
|---------|---------|----------|--|
| `displayName` | `{JOB-NAME}` | Your job name. | `MyJobName` |
| `documents` | [{},{}] | List of documents to run tasks on. | `[{},{}]` |
| `id` | `{DOC-ID}` | Document name or ID. | `doc1`|
| `language` | `{LANGUAGE-CODE}` |  A string specifying the language code for the document. If this key isn't specified, the service will assume the default language of the project that was selected during project creation. See [language support](../../language-support.md) for a list of supported language codes. |`en-us`|
| `text` | `{DOC-TEXT}` | Document task to run the tasks on. | `Lorem ipsum dolor sit amet` |
|`tasks`| | List of tasks we want to perform.|`[]`|
| `taskName`|CustomMultiLabelClassification|The task name|CustomMultiLabelClassification|
|`parameters`| |List of parameters to pass to the task.| |
| `project-name` |`{PROJECT-NAME}` | The name for your project. This value is case-sensitive.  | `myProject` |
| `deployment-name` |`{DEPLOYMENT-NAME}` | The name of your deployment. This value is case-sensitive.  | `prod` |

# [Single label classification](#tab/single-classification)

```json
{
  "displayName": "Classifying documents",
  "analysisInput": {
    "documents": [
      {
        "id": "1",
        "language": "{LANGUAGE-CODE}",
        "text": "Text1"
      },
      {
        "id": "2",
        "language": "{LANGUAGE-CODE}",
        "text": "Text2"
      }
    ]
  },
  "tasks": [
    {
      "kind": "CustomSingleLabelClassification",
      "taskName": "Single Classification Label",
      "parameters": {
        "projectName": "{PROJECT-NAME}",
        "deploymentName": "{DEPLOYMENT-NAME}"
      }
    }
  ]
}
```

|Key  |Placeholder  |Value  | Example |
|---------|---------|----------|--|
| displayName | `{JOB-NAME}` | Your job name. | `MyJobName` |
| documents | | List of documents to run tasks on. |  |
| `id` | `{DOC-ID}` | Document name or ID. | `doc1`|
| `language` | `{LANGUAGE-CODE}` |  A string specifying the language code for the document. If this key isn't specified, the service will assume the default language of the project that was selected during project creation. See [language support](../../language-support.md) for a list of supported language codes. |`en-us`|
| `text` | `{DOC-TEXT}` | Document task to run the tasks on. | `Lorem ipsum dolor sit amet` |
| `taskName`|CustomSingleLabelClassification|The task name|CustomSingleLabelClassification|
|`tasks`|[] | Array of tasks we want to perform.|[] |
|`parameters`| |List of parameters to pass to the task.| |
| `project-name` |`{PROJECT-NAME}` | The name for your project. This value is case-sensitive.  | `myProject` |
| `deployment-name` |`{DEPLOYMENT-NAME}` | The name of your deployment. This value is case-sensitive.  | `prod` |

---

#### Response

You will receive a 202 response indicating success. In the response **headers**, extract `operation-location`.
`operation-location` is formatted like this:

`{ENDPOINT}/language/analyze-text/jobs/{JOB-ID}?api-version={API-VERSION}`

You can use this URL to query the task completion status and get the results when task is completed.
