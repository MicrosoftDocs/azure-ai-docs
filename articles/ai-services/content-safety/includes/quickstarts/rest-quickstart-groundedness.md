---
title: "Quickstart: Use groundedness detection with the REST API"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 04/29/2025
ms.author: pafarley
---



## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) 
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, [supported region](../../overview.md#region-availability), and supported pricing tier. Then select **Create**.
* The resource takes a few minutes to deploy. After it does, go to the new resource. In the left pane, under **Resource Management**, select **API Keys and Endpoints**. Copy one of the subscription key values and endpoint to a temporary location for later use.
* (Optional) If you want to use the _reasoning_ feature, create an Azure OpenAI in Azure AI Foundry Models resource with a GPT model deployed.
* [cURL](https://curl.haxx.se/) or [Python](https://www.python.org/downloads/) installed.

## Authentication

For enhanced security, you need to use Managed Identity (MI) to manage access to your resources, for more details, please refer to [Security](../../overview.md#security).

## Check groundedness without reasoning

In the simple case without the _reasoning_ feature, the Groundedness detection API classifies the ungroundedness of the submitted content as `true` or `false`.

#### [cURL](#tab/curl)

This section walks through a sample request with cURL. Paste the command below into a text editor, and make the following changes.

1. Replace `<endpoint>` with the endpoint URL associated with your resource.
1. Replace `<your_subscription_key>` with one of the keys for your resource.
1. Optionally, replace the `"query"` or `"text"` fields in the body with your own text you'd like to analyze.
    
    ```shell
    curl --location --request POST '<endpoint>/contentsafety/text:detectGroundedness?api-version=2024-09-15-preview' \
    --header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "domain": "Generic",
      "task": "QnA",
      "qna": {
        "query": "How much does she currently get paid per hour at the bank?"
      },
      "text": "12/hour",
      "groundingSources": [
        "I'm 21 years old and I need to make a decision about the next two years of my life. Within a week. I currently work for a bank that requires strict sales goals to meet. IF they aren't met three times (three months) you're canned. They pay me 10/hour and it's not unheard of to get a raise in 6ish months. The issue is, **I'm not a salesperson**. That's not my personality. I'm amazing at customer service, I have the most positive customer service \"reports\" done about me in the short time I've worked here. A coworker asked \"do you ask for people to fill these out? you have a ton\". That being said, I have a job opportunity at Chase Bank as a part time teller. What makes this decision so hard is that at my current job, I get 40 hours and Chase could only offer me 20 hours/week. Drive time to my current job is also 21 miles **one way** while Chase is literally 1.8 miles from my house, allowing me to go home for lunch. I do have an apartment and an awesome roommate that I know wont be late on his portion of rent, so paying bills with 20hours a week isn't the issue. It's the spending money and being broke all the time.\n\nI previously worked at Wal-Mart and took home just about 400 dollars every other week. So I know i can survive on this income. I just don't know whether I should go for Chase as I could definitely see myself having a career there. I'm a math major likely going to become an actuary, so Chase could provide excellent opportunities for me **eventually**."
      ],
      "reasoning": false
    }'
    ```

Open a command prompt and run the cURL command.


#### [Python](#tab/python)

Create a new Python file named _quickstart.py_. Open the new file in your preferred editor or IDE.

1. Replace the contents of _quickstart.py_ with the following code. Enter your endpoint URL and key in the appropriate fields. Optionally, replace the `"query"` or `"text"` fields in the body with your own text you'd like to analyze.
    
    ```Python
    import http.client
    import json

    endpoint = "<your_custom_subdomain>.cognitiveservices.azure.com"
    conn = http.client.HTTPSConnection(endpoint)
    payload = json.dumps({
      "domain": "Generic",
      "task": "QnA",
      "qna": {
        "query": "How much does she currently get paid per hour at the bank?"
      },
      "text": "12/hour",
      "groundingSources": [
        "I'm 21 years old and I need to make a decision about the next two years of my life. Within a week. I currently work for a bank that requires strict sales goals to meet. IF they aren't met three times (three months) you're canned. They pay me 10/hour and it's not unheard of to get a raise in 6ish months. The issue is, **I'm not a salesperson**. That's not my personality. I'm amazing at customer service, I have the most positive customer service \"reports\" done about me in the short time I've worked here. A coworker asked \"do you ask for people to fill these out? you have a ton\". That being said, I have a job opportunity at Chase Bank as a part time teller. What makes this decision so hard is that at my current job, I get 40 hours and Chase could only offer me 20 hours/week. Drive time to my current job is also 21 miles **one way** while Chase is literally 1.8 miles from my house, allowing me to go home for lunch. I do have an apartment and an awesome roommate that I know wont be late on his portion of rent, so paying bills with 20hours a week isn't the issue. It's the spending money and being broke all the time.\n\nI previously worked at Wal-Mart and took home just about 400 dollars every other week. So I know i can survive on this income. I just don't know whether I should go for Chase as I could definitely see myself having a career there. I'm a math major likely going to become an actuary, so Chase could provide excellent opportunities for me **eventually**."
      ],
      "reasoning": false
    })
    headers = {
      'Ocp-Apim-Subscription-Key': '<your_subscription_key>',
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/contentsafety/text:detectGroundedness?api-version=2024-09-15-preview", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    ```

    [!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/microsoft-entra-id-akv-expanded.md)]
    
1. Run the application with the `python` command:

    ```console
    python quickstart.py
    ````

    Wait a few moments to get the response.

---

To test a summarization task instead of a question answering (QnA) task, use the following sample JSON body:

```json
{
  "domain": "Medical",
  "task": "Summarization",
  "text": "Ms Johnson has been in the hospital after experiencing a stroke.",
  "groundingSources": [
    "Our patient, Ms. Johnson, presented with persistent fatigue, unexplained weight loss, and frequent night sweats. After a series of tests, she was diagnosed with Hodgkin’s lymphoma, a type of cancer that affects the lymphatic system. The diagnosis was confirmed through a lymph node biopsy revealing the presence of Reed-Sternberg cells, a characteristic of this disease. She was further staged using PET-CT scans. Her treatment plan includes chemotherapy and possibly radiation therapy, depending on her response to treatment. The medical team remains optimistic about her prognosis given the high cure rate of Hodgkin’s lymphoma."
  ],
  "reasoning": false
}
```

The following fields must be included in the URL:

| Name     | Required | Description | Type   |
| :-------------- | :-------- | :------ | :----- |
| **API Version** | Required  | This is the API version to be used. The current version is: api-version=2024-09-15-preview. Example: `<endpoint>/contentsafety/text:detectGroundedness?api-version=2024-09-15-preview` | String |

The parameters in the request body are defined in this table:

| Name  | Description     | Type    |
| :----------- | :--------- | ------- |
| **domain** | (Optional) `MEDICAL` or `GENERIC`. Default value: `GENERIC`. | Enum  |
| **task** | (Optional) Type of task: `QnA`, `Summarization`. Default value: `Summarization`. | Enum |
| **qna**       | (Optional) Holds QnA data when the task type is `QnA`.  | String  |
| - `query`       | (Optional) This represents the question in a QnA task. Character limit: 7,500. | String  |
| **text**   | (Required) The LLM output text to be checked. Character limit: 7,500. |  String  |
| **groundingSources**  | (Required) Uses an array of grounding sources to validate AI-generated text. See [Input requirements](../../overview.md#input-requirements) for limits. | String array    |
| **reasoning**  | (Optional) Specifies whether to use the reasoning feature. The default value is `false`. If `true`, you need to bring your own Azure OpenAI GPT-4o (versions 0513, 0806) to provide an explanation. Be careful: using reasoning increases the processing time.| Boolean   |

### Interpret the API response

After you submit your request, you'll receive a JSON response reflecting the Groundedness analysis performed. Here’s what a typical output looks like: 

```json
{
  "ungroundedDetected": true,
  "ungroundedPercentage": 1,
  "ungroundedDetails": [
    {
      "text": "12/hour."
    }
  ]
}
```

The JSON objects in the output are defined here:

| Name  | Description    | Type    |
| :------------------ | :----------- | ------- |
| **ungroundedDetected** | Indicates whether the text exhibits ungroundedness.  | Boolean    |
| **ungroundedPercentage** | Specifies the proportion of the text identified as ungrounded, expressed as a number between 0 and 1, where 0 indicates no ungrounded content and 1 indicates entirely ungrounded content. This is not a confidence level.| Float	 |
| **ungroundedDetails** | Provides insights into ungrounded content with specific examples and percentages.| Array |
| -**`text`**   |  The specific text that is ungrounded.  | String   |

## Check groundedness with reasoning

The Groundedness detection API provides the option to include _reasoning_ in the API response. With reasoning enabled, the response includes a `"reasoning"` field that details specific instances and explanations for any detected ungroundedness.

### Connect your own GPT deployment

> [!TIP]
> We only support Azure OpenAI GPT-4o (versions 0513, 0806) resources and don't support other models. You have the flexibility to deploy your Azure OpenAI GPT-4o (versions 0513, 0806) resources in any region. However, to minimize potential latency and avoid any geographical boundary data privacy and risk concerns, we recommend situating them in the same region as your Azure AI Content Safety resources. For comprehensive details on data privacy, refer to the [Data, privacy and security guidelines for Azure OpenAI](/azure/ai-foundry/responsible-ai/openai/data-privacy) and [Data, privacy, and security for Azure AI Content Safety](/azure/ai-foundry/responsible-ai/content-safety/data-privacy).

In order to use your Azure OpenAI GPT-4o (versions 0513, 0806) resource to enable the reasoning feature, use Managed Identity to allow your Content Safety resource to access the Azure OpenAI resource:

[!INCLUDE [openai-account-access](~/reusable-content/ce-skilling/azure/includes/ai-services/content-safety/includes/openai-account-access.md)]

### Make the API request

In your request to the Groundedness detection API, set the `"reasoning"` body parameter to `true`, and provide the other needed parameters:
    
```json

{
  "domain": "Medical",
  "task": "Summarization",
  "text": "The patient name is Kevin.",
  "groundingSources": [
    "The patient name is Jane."
  ],
  "reasoning": true,
  "llmResource": {
    "resourceType": "AzureOpenAI",
    "azureOpenAIEndpoint": "<your_OpenAI_endpoint>",
    "azureOpenAIDeploymentName": "<your_deployment_name>"
  }
}
```

#### [cURL](#tab/curl)

This section walks through a sample request with cURL. Paste the command below into a text editor, and make the following changes.

1. Replace `<endpoint>` with the endpoint URL associated with your Azure AI Content Safety resource.
1. Replace `<your_subscription_key>` with one of the keys for your resource.
1. Replace `<your_OpenAI_endpoint>` with the endpoint URL associated with your Azure OpenAI resource.
1. Replace `<your_deployment_name>` with the name of your Azure OpenAI deployment.
1. Optionally, replace the `"query"` or `"text"` fields in the body with your own text you'd like to analyze.
    
    
    ```shell
    curl --location --request POST '<endpoint>/contentsafety/text:detectGroundedness?api-version=2024-09-15-preview' \
    --header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "domain": "Generic",
      "task": "QnA",
      "qna": {
        "query": "How much does she currently get paid per hour at the bank?"
      },
      "text": "12/hour",
      "groundingSources": [
        "I'm 21 years old and I need to make a decision about the next two years of my life. Within a week. I currently work for a bank that requires strict sales goals to meet. If they aren't met three times (three months) you're canned. They pay me 10/hour and it's not unheard of to get a raise in 6ish months. The issue is, **I'm not a salesperson**. That's not my personality. I'm amazing at customer service, I have the most positive customer service \"reports\" done about me in the short time I've worked here. A coworker asked \"do you ask for people to fill these out? you have a ton\". That being said, I have a job opportunity at Chase Bank as a part time teller. What makes this decision so hard is that at my current job, I get 40 hours and Chase could only offer me 20 hours/week. Drive time to my current job is also 21 miles **one way** while Chase is literally 1.8 miles from my house, allowing me to go home for lunch. I do have an apartment and an awesome roommate that I know wont be late on his portion of rent, so paying bills with 20hours a week isn't the issue. It's the spending money and being broke all the time.\n\nI previously worked at Wal-Mart and took home just about 400 dollars every other week. So I know i can survive on this income. I just don't know whether I should go for Chase as I could definitely see myself having a career there. I'm a math major likely going to become an actuary, so Chase could provide excellent opportunities for me **eventually**."
      ],
      "reasoning": true,
      "llmResource": {
            "resourceType": "AzureOpenAI",
            "azureOpenAIEndpoint": "<your_OpenAI_endpoint>",
            "azureOpenAIDeploymentName": "<your_deployment_name>"
    }'
    ```
    
1. Open a command prompt and run the cURL command.


#### [Python](#tab/python)

Create a new Python file named _quickstart.py_. Open the new file in your preferred editor or IDE.

1. Replace the contents of _quickstart.py_ with the following code. Enter your endpoint URL and key in the appropriate fields. Also enter your Azure OpenAI endpoint and deployment name. Optionally, replace the `"query"` or `"text"` fields in the body with your own text you'd like to analyze.
    
    ```Python
    import http.client
    import json
    
    conn = http.client.HTTPSConnection("<endpoint>/contentsafety/text:detectGroundedness?api-version=2024-09-15-preview")
    payload = json.dumps({
      "domain": "Generic",
      "task": "QnA",
      "qna": {
        "query": "How much does she currently get paid per hour at the bank?"
      },
      "text": "12/hour",
      "groundingSources": [
        "I'm 21 years old and I need to make a decision about the next two years of my life. Within a week. I currently work for a bank that requires strict sales goals to meet. IF they aren't met three times (three months) you're canned. They pay me 10/hour and it's not unheard of to get a raise in 6ish months. The issue is, **I'm not a salesperson**. That's not my personality. I'm amazing at customer service, I have the most positive customer service \"reports\" done about me in the short time I've worked here. A coworker asked \"do you ask for people to fill these out? you have a ton\". That being said, I have a job opportunity at Chase Bank as a part time teller. What makes this decision so hard is that at my current job, I get 40 hours and Chase could only offer me 20 hours/week. Drive time to my current job is also 21 miles **one way** while Chase is literally 1.8 miles from my house, allowing me to go home for lunch. I do have an apartment and an awesome roommate that I know wont be late on his portion of rent, so paying bills with 20hours a week isn't the issue. It's the spending money and being broke all the time.\n\nI previously worked at Wal-Mart and took home just about 400 dollars every other week. So I know i can survive on this income. I just don't know whether I should go for Chase as I could definitely see myself having a career there. I'm a math major likely going to become an actuary, so Chase could provide excellent opportunities for me **eventually**."
      ],
      "reasoning": True
      "llmResource": {
       "resourceType": "AzureOpenAI",
       "azureOpenAIEndpoint": "<your_OpenAI_endpoint>",
       "azureOpenAIDeploymentName": "<your_deployment_name>"
      }
    })
    headers = {
      'Ocp-Apim-Subscription-Key': '<your_subscription_key>',
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/contentsafety/text:detectGroundedness?api-version=2024-09-15-preview", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    ```

1. Run the application with the `python` command:

    ```console
    python quickstart.py
    ````

    Wait a few moments to get the response.

---

The parameters in the request body are defined in this table:


| Name  | Description     | Type    |
| :----------- | :--------- | ------- |
| **domain** | (Optional) `MEDICAL` or `GENERIC`. Default value: `GENERIC`. | Enum  |
| **task** | (Optional) Type of task: `QnA`, `Summarization`. Default value: `Summarization`. | Enum |
| **qna**       | (Optional) Holds QnA data when the task type is `QnA`.  | String  |
| - `query`       | (Optional) This represents the question in a QnA task. Character limit: 7,500. | String  |
| **text**   | (Required) The LLM output text to be checked. Character limit: 7,500. |  String  |
| **groundingSources**  | (Required) Uses an array of grounding sources to validate AI-generated text. See [Input requirements](../../overview.md#input-requirements) for limits, | String array    |
| **reasoning**  | (Optional) Set to `true`, the service uses Azure OpenAI resources to provide an explanation. Be careful: using reasoning increases the processing time and incurs extra fees.| Boolean   |
| **llmResource**  | (Required) If you want to use your own Azure OpenAI GPT-4o (versions 0513, 0806) resource to enable reasoning, add this field and include the subfields for the resources used. | String   |
| - `resourceType `| Specifies the type of resource being used. Currently it only allows `AzureOpenAI`. We only support Azure OpenAI GPT-4o (versions 0513, 0806)  resources and do not support other models. | Enum|
| - `azureOpenAIEndpoint `| Your endpoint URL for Azure OpenAI service.  | String |
| - `azureOpenAIDeploymentName` | The name of the specific model deployment to use. | String|

### Interpret the API response

After you submit your request, you'll receive a JSON response reflecting the Groundedness analysis performed. Here’s what a typical output looks like: 

```json
{
  "ungroundedDetected": true,
  "ungroundedPercentage": 1,
  "ungroundedDetails": [
    {
      "text": "12/hour.",
      "offset": {
        "utf8": 0,
        "utf16": 0,
        "codePoint": 0
      },
      "length": {
        "utf8": 8,
        "utf16": 8,
        "codePoint": 8
      },
      "reason": "None. The premise mentions a pay of \"10/hour\" but does not mention \"12/hour.\" It's neutral. "
    }
  ]
}
```

The JSON objects in the output are defined here:

| Name  | Description    | Type    |
| :------------------ | :----------- | ------- |
| **ungroundedDetected** | Indicates whether the text exhibits ungroundedness.  | Boolean    |
| **ungroundedPercentage** | Specifies the proportion of the text identified as ungrounded, expressed as a number between 0 and 1, where 0 indicates no ungrounded content and 1 indicates entirely ungrounded content. This is not a confidence level.| Float	 |
| **ungroundedDetails** | Provides insights into ungrounded content with specific examples and percentages.| Array |
| -**`text`**   |  The specific text that is ungrounded.  | String   |
| -**`offset`**   |  An object describing the position of the ungrounded text in various encoding.  | String   |
| - `offset > utf8`       | The offset position of the ungrounded text in UTF-8 encoding.      | Integer   |
| - `offset > utf16`      | The offset position of the ungrounded text in UTF-16 encoding.       | Integer |
| - `offset > codePoint`  | The offset position of the ungrounded text in terms of Unicode code points. |Integer    |
| -**`length`**   |  An object describing the length of the ungrounded text in various encoding. (utf8, utf16, codePoint), similar to the offset. | Object   |
| - `length > utf8`       | The length of the ungrounded text in UTF-8 encoding.      | Integer   |
| - `length > utf16`      | The length of the ungrounded text in UTF-16 encoding.       | Integer |
| - `length > codePoint`  | The length of the ungrounded text in terms of Unicode code points. |Integer    |
| -**`reason`** |  Offers explanations for detected ungroundedness. | String  |


## Check groundedness with the correction feature

The groundedness detection API includes a correction feature that automatically corrects any detected ungroundedness in the text based on the provided grounding sources. When the correction feature is enabled, the response includes a `"correction Text"` field that presents the corrected text aligned with the grounding sources.

### Connect your own GPT deployment

> [!TIP]
> Currently, the correction feature supports only **Azure OpenAI GPT-4o (versions 0513, 0806)** resources. To minimize latency and adhere to data privacy guidelines, it's recommended to deploy your Azure OpenAI GPT-4o (versions 0513, 0806) in the same region as your Azure AI Content Safety resources. For more details on data privacy, refer to the [Data, privacy and security guidelines for Azure OpenAI](/azure/ai-foundry/responsible-ai/openai/data-privacy)
 and [Data, privacy, and security for Azure AI Content Safety](/azure/ai-foundry/responsible-ai/content-safety/data-privacy).

To use your Azure OpenAI GPT-4o (versions 0513, 0806) resource for enabling the correction feature, use Managed Identity to allow your Content Safety resource to access the Azure OpenAI resource. Follow the steps in the [earlier section](#connect-your-own-gpt-deployment) to set up the Managed Identity.


### Make the API request
In your request to the groundedness detection API, set the `"correction"` body parameter to `true`, and provide the other necessary parameters:

```json
{
  "domain": "Medical",
  "task": "Summarization",
  "text": "The patient name is Kevin.",
  "groundingSources": [
    "The patient name is Jane."
  ],
  "correction": true,
  "llmResource": {
    "resourceType": "AzureOpenAI",
    "azureOpenAIEndpoint": "<your_OpenAI_endpoint>",
    "azureOpenAIDeploymentName": "<your_deployment_name>"
  }
}
```

#### [cURL](#tab/curl)
This section demonstrates a sample request using cURL. Replace the placeholders as needed:
- Replace `<endpoint>` with your resource's endpoint URL.
- Replace `<your_subscription_key>` with your subscription key.
- Optionally, replace the "text" field with the text you want to analyze.


```shell
curl --location --request POST '<endpoint>/contentsafety/text:detectGroundedness?api-version=2024-09-15-preview' \
--header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "domain": "Generic",
  "task": "Summarization",
  "text": "The patient name is Kevin.",
  "groundingSources": [
    "The patient name is Jane."
  ],
  "correction": true,
  "llmResource": {
        "resourceType": "AzureOpenAI",
        "azureOpenAIEndpoint": "<your_OpenAI_endpoint>",
        "azureOpenAIDeploymentName": "<your_deployment_name>"
  }
}'
```
#### [Python](#tab/python)

Create a Python script named quickstart.py and include the following code. Update the endpoint URL and key as appropriate:
```Python

conn = http.client.HTTPSConnection("<endpoint>/contentsafety/text:detectGroundedness?api-version=2024-09-15-preview")
payload = json.dumps({
  "domain": "Generic",
  "task": "Summarization",
  "text": "The patient name is Kevin.",
  "groundingSources": [
    "The patient name is Jane."
  ],
  "correction": True,
  "llmResource": {
   "resourceType": "AzureOpenAI",
   "azureOpenAIEndpoint": "<your_OpenAI_endpoint>",
   "azureOpenAIDeploymentName": "<your_deployment_name>"
  }
})
headers = {
  'Ocp-Apim-Subscription-Key': '<your_subscription_key>',
  'Content-Type': 'application/json'
}
conn.request("POST", "/contentsafety/text:detectGroundedness?api-version=2024-09-15-preview", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```

---

The parameters in the request body are defined in this table:


| Name  | Description     | Type    |
| :----------- | :--------- | ------- |
| **domain** | (Optional) `MEDICAL` or `GENERIC`. Default value: `GENERIC`. | Enum  |
| **task** | (Optional) Type of task: `QnA`, `Summarization`. Default value: `Summarization`. | Enum |
| **qna**       | (Optional) Holds QnA data when the task type is `QnA`.  | String  |
| - `query`       | (Optional) This represents the question in a QnA task. Character limit: 7,500. | String  |
| **text**   | (Required) The LLM output text to be checked. Character limit: 7,500. |  String  |
| **groundingSources**  | (Required) Uses an array of grounding sources to validate AI-generated text. See [Input requirements](../../overview.md#input-requirements) for limits. | String Array    |
| **correction**  | (Optional) Set to `true`, the service uses Azure OpenAI resources to provide the corrected text, ensuring consistency with the grounding sources. Be careful: using correction increases the processing time and incurs extra fees.| Boolean   |
| **llmResource**  | (Required) If you want to use your own Azure OpenAI GPT-4o (versions 0513, 0806) resource to enable reasoning, add this field and include the subfields for the resources used. | String   |
| - `resourceType `| Specifies the type of resource being used. Currently it only allows `AzureOpenAI`. We only support Azure OpenAI GPT-4o (versions 0513, 0806) resources and do not support other models. | Enum|
| - `azureOpenAIEndpoint `| Your endpoint URL for Azure OpenAI service.  | String |
| - `azureOpenAIDeploymentName` | The name of the specific model deployment to use. | String|

### Interpret the API response

The response includes a `"correction Text"` field containing the corrected text, ensuring consistency with the provided grounding sources.

The correction feature detects that `Kevin` is ungrounded because it conflicts with the grounding source `Jane`. The API returns the corrected text: `"The patient name is Jane."`

```json
{
  "ungroundedDetected": true,
  "ungroundedPercentage": 1,
  "ungroundedDetails": [
    {
      "text": "The patient name is Kevin"
    }
  ],
  "correction Text": "The patient name is Jane"
}
```

The JSON objects in the output are defined here:


| Name  | Description    | Type    |
| :------------------ | :----------- | ------- |
| **ungroundedDetected** |	Indicates if ungrounded content was detected.|	Boolean|
| **ungroundedPercentage** |	The proportion of ungrounded content in the text. This is not a confidence level. |	Float|
| **ungroundedDetails** |	Details of ungrounded content, including specific text segments.|	Array|
| -**`text`**   |  The specific text that is ungrounded.  | String   |
| -**`offset`**   |  An object describing the position of the ungrounded text in various encoding.  | String   |
| - `offset > utf8`       | The offset position of the ungrounded text in UTF-8 encoding.      | Integer   |
| - `offset > utf16`      | The offset position of the ungrounded text in UTF-16 encoding.       | Integer |
| -**`length`**   |  An object describing the length of the ungrounded text in various encoding. (utf8, utf16, codePoint), similar to the offset. | Object   |
| - `length > utf8`       | The length of the ungrounded text in UTF-8 encoding.      | Integer   |
| - `length > utf16`      | The length of the ungrounded text in UTF-16 encoding.       | Integer |
| - `length > codePoint`  | The length of the ungrounded text in terms of Unicode code points. |Integer    |
| -**`correction Text`** |	The corrected text, ensuring consistency with the grounding sources.|String|


## Clean up resources

If you want to clean up and remove an Azure AI services subscription, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](/azure/ai-services/multi-service-resource?pivots=azportal#clean-up-resources)
- [Azure CLI](/azure/ai-services/multi-service-resource?pivots=azcli#clean-up-resources)
