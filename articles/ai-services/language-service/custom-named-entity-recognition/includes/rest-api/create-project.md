---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
To start creating a custom named entity recognition model, you need to create a project. Creating a project lets you label data, train, evaluate, improve, and deploy your models.

> [!NOTE]
> The project name is case-sensitive for all operations.

Create a **PATCH** request using the following URL, headers, and JSON body to create your project.

### Request URL

Use the following URL to create a project. Replace the following placeholders with your own values. 

```rest
{Endpoint}/language/authoring/analyze-text/projects/{projectName}?api-version={API-VERSION}
```

|Placeholder  |Value  | Example |
|---------|---------|---------|
|`{ENDPOINT}`     | The endpoint for authenticating your API request.   | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
|`{PROJECT-NAME}`     | The name for your project. This value is case-sensitive.   | `myProject` |
|`{API-VERSION}`     | The version of the API you're calling. The value referenced is for the latest released version. For more information, for more information, *see* [Model lifecycle](../../../concepts/model-lifecycle.md#choose-the-model-version-used-on-your-data).| `2022-05-01` |


### Request headers

Use the following header to authenticate your request. 

|Key|Required|Type|Value|
|--|--|--|--|
|`Ocp-Apim-Subscription-Key`|True|string| The key to your resource. Used for authenticating your API requests.|
|`Content-Type`|True|string|**application/merge-patch+json**|

### Request body

Use the following JSON in your request. Replace the following placeholders with your own values.

```json
{
  "projectName": "{PROJECT-NAME}",
  "language": "{LANGUAGE-CODE}",
  "projectKind": "CustomEntityRecognition",
  "description": "Project description",
  "multilingual": "True",
  "storageInputContainerName": "{CONTAINER-NAME}"
}

```

|Key  |Placeholder|Value  | Example |
|---------|---------|---------|--|
| projectName | `{PROJECT-NAME}` | The name of your project. This value is case-sensitive. | `myProject` |
| language | `{LANGUAGE-CODE}` |  A string specifying the language code for the documents used in your project. If your project is a multilingual project, select the code for the language most frequently represented in the documents. See [language support](../../language-support.md) to learn more about supported language codes. |`en-us`|
| projectKind | `CustomEntityRecognition` | Your project kind. | `CustomEntityRecognition` |
| multilingual | `true`| A boolean value that enables you to have documents in multiple languages in your dataset and when your model is deployed you can query the model in any supported language (not necessarily included in your training documents). See [language support](../../language-support.md#multi-lingual-option) to learn more about multilingual support. | `true`|
| storageInputContainerName | `{CONTAINER-NAME` | The name of your Azure storage container your documents were uploaded.   | `myContainer` |

This request returns a 201 response, which means that the project is created.


This request returns an error if:
* The selected resource doesn't have proper permission for the storage account. 

