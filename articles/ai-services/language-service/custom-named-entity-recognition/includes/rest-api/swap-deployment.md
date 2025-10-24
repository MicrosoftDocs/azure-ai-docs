---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/05/2025
ms.author: lajanuar
---



Create a **POST** request using the following URL, headers, and JSON body to start a swap deployments job.


### Request URL

```rest
{ENDPOINT}/language/authoring/analyze-text/projects/{PROJECT-NAME}/deployments/:swap?api-version={API-VERSION}
```

|Placeholder  |Value  | Example |
|---------|---------|---------|
|`{ENDPOINT}`     | The endpoint for authenticating your API request.   | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
|`{PROJECT-NAME}`     | The name for your project. This value is case-sensitive.   | `myProject` |
<<<<<<< HEAD
|`{API-VERSION}`     | The version of the API you're calling. The value referenced is for the latest [model version](../../../concepts/model-lifecycle.md#choose-the-model-version-used-on-your-data) released. | `2022-05-01` |
=======
|`{API-VERSION}`     | The version of the API you're calling. The value referenced here's for the latest [model version](../../../concepts/model-lifecycle.md#choose-the-model-version-used-on-your-data) released. | `2022-05-01` |
>>>>>>> d843db8face108a14958aa31ff4bfac876de9b0e


### Headers

Use the following header to authenticate your request. 

|Key|Value|
|--|--|
|`Ocp-Apim-Subscription-Key`| The key to your resource. Used for authenticating your API requests.|


### Request Body

```json
{
  "firstDeploymentName": "{FIRST-DEPLOYMENT-NAME}",
  "secondDeploymentName": "{SECOND-DEPLOYMENT-NAME}"
}
```


|Key|Placeholder| Value| Example|
|--|--|--|--|
|firstDeploymentName |`{FIRST-DEPLOYMENT-NAME}`| The name for your first deployment. This value is case-sensitive.   | `production` |
|secondDeploymentName | `{SECOND-DEPLOYMENT-NAME}`|The name for your second deployment. This value is case-sensitive.   | `staging` |


<<<<<<< HEAD
Once you send your API request, you receive a `202` response indicating success.
=======
Once you send your API request, your receive a `202` response indicating success.
>>>>>>> d843db8face108a14958aa31ff4bfac876de9b0e
