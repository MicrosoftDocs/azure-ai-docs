---
title: "Quickstart: Use a blocklist with the REST API"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 02/22/2025
ms.author: pafarley
ai-usage: ai-assisted
---

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) 
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.
* [cURL](https://curl.haxx.se/) installed

## Create a blocklist 

The following section walks through a sample request with cURL. Paste the command below into a text editor, and make the following changes.

1. Replace `<endpoint>` with the endpoint URL associated with your resource.
1. Replace `<your_subscription_key>` with one of the keys that come with your resource.
1. Replace `<your_blocklist_name>` with a name for your blocklist.
1. Optionally, replace the `"description"` field in the body with your own description of the list.

```shell
curl --location --request PATCH '<endpoint>/contentsafety/text/blocklists/<your_blocklist_name>?api-version=2024-09-01' --header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' --header 'Content-Type: application/json' --data-raw '{"description": "This is a violence list"}'
```

The below fields must be included in the url:

| Name      |Required  |  Description | Type   |
| :------- |-------- |:--------------- | ------ |
| **API Version** |Required |This is the API version to be checked. The current version is: api-version=2024-09-01. Example: `<endpoint>/contentsafety/text:analyze?api-version=2024-09-01` | String |

See the following sample request body:

```json
{
  "description": "Test Blocklist"
}
```

Open a command prompt window, paste in the edited cURL command, and run it.

### Output

You should see the results displayed as JSON data in the console output. For example:

```json
{
  "blocklistName": "TestBlocklist",
  "description": "Test Blocklist"
}
```


## Add items to a blocklist 

The following section walks through a sample request with cURL. Paste the command below into a text editor, and make the following changes.

1. Replace `<endpoint>` with the endpoint URL associated with your resource.
1. Replace `<your_subscription_key>` with one of the keys that come with your resource.
1. Replace `<your_blocklist_name>` with a name for your blocklist.
1. Optionally, replace the `"description"` and `"text"` fields in the body with your own blocklist item and description.

```shell
curl --request POST <endpoint>/contentsafety/text/blocklists/<your_blocklist_name>:addOrUpdateBlocklistItems?api-version=2024-09-01 --header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' --header 'Content-Type: application/json' --data-raw '{"blocklistItems": [{"description": "string", "text": "bleed"}]}'
```

The below fields must be included in the url:

| Name      |Required  |  Description | Type   |
| :------- |-------- |:--------------- | ------ |
| **API Version** |Required |This is the API version to be checked. The current version is: api-version=2024-09-01. Example: `<endpoint>/contentsafety/text:analyze?api-version=2024-09-01` | String |

See the following sample request body:

```json
{
  "blocklistItems": [
    {
      "description": "Hate word",
      "text": "hate"
    },
    {
      "description": "A regular expression that matches harmful words.",
      "text": "b[i1][a@][s\\$]",
      "isRegex": true
    }
  ]
}
```

Open a command prompt window, paste in the edited cURL command, and run it.

### Output

You should see the results displayed as JSON data in the console output. For example:

```json
{
  "blocklistItems": [
    {
      "blocklistItemId": "9511969e-f1e3-4604-9127-05ee16c509ec",
      "description": "Hate word",
      "text": "hate",
      "isRegex": false
    },
    {
      "blocklistItemId": "d9b2d63d-a233-4123-847a-7d1b5b3b8a8e",
      "description": "A regular expression that matches harmful words.",
      "text": "b[i1][a@][s\\$]",
      "isRegex": true
    }
  ]
}
```


## Analyze text against a blocklist

> [!NOTE]
> After you edit a blocklist, it can take a few minutes before text analysis reflects the changes. If you don't see matches right away, retry the analyze call after a short delay.

The following section walks through a sample request with cURL. Paste the command below into a text editor, and make the following changes.

1. Replace `<endpoint>` with the endpoint URL associated with your resource.
1. Replace `<your_subscription_key>` with one of the keys that come with your resource.
1. Replace `<your_blocklist_name>` with a name for your blocklist.
1. Replace `<sample_text>` with the text you want to analyze against the blocklist.

```shell
curl --request POST '<endpoint>/contentsafety/text:analyze?api-version=2024-09-01' --header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' --header 'Content-Type: application/json' --data-raw '{  "text": "<sample_text>", "categories": [   "Hate",  "Sexual",  "SelfHarm",  "Violence" ], "blocklistNames":["<your_blocklist_name>"], "haltOnBlocklistHit": false,"outputType": "FourSeverityLevels"}'
```

The below fields must be included in the url:

| Name      |Required  |  Description | Type   |
| :------- |-------- |:--------------- | ------ |
| **API Version** |Required |This is the API version to be checked. The current version is: api-version=2024-09-01. Example: `<endpoint>/contentsafety/text:analyze?api-version=2024-09-01` | String |

See the following sample request body:

```json
{
  "text": "<sample_text>",
  "categories": [
    "Hate",
    "Sexual",
    "SelfHarm",
    "Violence"
  ],
  "blocklistNames": [
    "<your_blocklist_name>"
  ],
  "haltOnBlocklistHit": false,
  "outputType": "FourSeverityLevels"
}
```

Open a command prompt window, paste in the edited cURL command, and run it.

### Output

You should see the analyze results displayed as JSON data in the console output. For example:

```json
{
  "blocklistsMatch": [
    {
      "blocklistName": "my-list",
      "blocklistItemId": "877bd6a0-236d-40f5-b6c2-07a6a1886ab1",
      "blocklistItemText": "bleed"
    }
  ],
  "categoriesAnalysis": [
    {
      "category": "Hate",
      "severity": 2
    },
    {
      "category": "Sexual",
      "severity": 0
    },
    {
      "category": "SelfHarm",
      "severity": 0
    },
    {
      "category": "Violence",
      "severity": 4
    }
  ]
}
```
