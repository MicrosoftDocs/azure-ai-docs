---
title: "Quickstart: Use task adherence with the REST API"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 04/10/2025
ms.author: pafarley
---

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) 
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, region, and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.
* [cURL](https://curl.haxx.se/) installed

## Use Task Adherence

The following section walks through a sample request with cURL. 

Paste the command below into a text editor, and make the following changes.
 
1. Replace `<endpoint>` with your resource endpoint URL.
1. Replace `<your_subscription_key>` with your key.
1. Optionally change the text in the `"messages"` field in the body to test different scenarios.

```shell
curl --request POST \
 --url '<endpoint>/contentsafety/agent:analyzeTaskAdherence?api-version=2025-09-15-preview' \
 --header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' \
 --header 'Content-Type: application/json' \
 --data '{
 "tools": [
  {
   "type": "function",
   "function": {
    "name": "get_credit_card_limit",
    "description": "Get credit card limit of the user"
   }
  },
  {
   "type": "function",
   "function": {
    "name": "get_car_price",
    "description": "Get car price of a particular model"
   }
  },
  {
   "type": "function",
   "function": {
    "name": "order_car",
    "description": "Buy a particular car model instantaneously"
   }
  }
 ],
 "messages": [
  {
   "source": "Prompt",
   "role": "User",
   "contents": "How many mahindra be6e can i buy with my credit card limit?"
  },
  {
   "source": "Completion",
   "role": "Assistant",
   "contents": "Getting the required information",
   "toolCalls": [
    {
     "type": "function",
     "function": {
      "name": "get_credit_card_limit",
      "arguments": ""
     },
     "id": "call_001"
    },
    {
     "type": "function",
     "function": {
      "name": "get_car_price",
      "arguments": ""
     },
     "id": "call_002"
    }
   ]
  },
  {
   "source": "Completion",
   "role": "Tool",
   "toolCallId": "call_001",
   "contents": "100000"
  },
  {
   "source": "Completion",
   "role": "Tool",
   "toolCallId": "call_002",
   "contents": "10000"
  },
  {
   "source" : "Completion",
   "role" : "Assistant",
   "contents" : "The price of a be6e is 10000 and your credit limit is 100000, so you can buy 10 be6e from your credit card."
  }
 ]
}'
```


The below fields must be included in the URL:

| Name      |Required?  |  Description | Type   |
| :------- |-------- |:--------------- | ------ |
| **API Version** |Required |This is the API version to be checked. Current version is: `2025-09-15-preview`. Example: `<endpoint>/contentsafety/image:analyze?api-version=2025-09-15-preview` | String |

The parameters in the request body are defined in this table:

| Name        | Required?     | Description  | Type    |
| :---------- | ----------- | :------------ | ------- |
|tools | Yes | A list of tools that define functions to be used in the task. Each tool includes a `type` (for example, "function") and details about the function, including its `name` and `description`. |Array of JSON objects |
|messages |Yes |A list of messages exchanged between the user, assistant, and tools. Each message includes the `source` (for example, "Prompt", "Completion"), `role` (for example, "User", "Assistant", "Tool"), `contents` (message text), and optionally `toolCalls` or `toolCallId`. |Array of JSON objects| 

Open a command prompt window and run the cURL command.

### Output

After you submit your request, you'll receive JSON data reflecting the analysis performed by Task Adherence. This data flags potential vulnerabilities within your agent workflow. Here’s what a typical output looks like: 

```json
{ 
  "taskRiskDetected": true, 
  "details": "Agent attempts to share a document externally without user request or confirmation." 
}
```

The JSON fields in the output are defined here:

| Name     | Description   | Type   |
| :------------- | :--------------- | ------ |
| taskRiskDetected | Contains risk detection results for the input.   |Boolean |
|details | Returns reasoning, when a risk is detected | String |

A `taskRiskDetected` value of `true` signifies a detected risk, in which case we recommend review and action, such as blocking the tool invocation request or human-in-the-loop escalation. 
