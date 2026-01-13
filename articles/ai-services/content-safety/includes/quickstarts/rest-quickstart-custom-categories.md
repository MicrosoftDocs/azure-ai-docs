---
title: "Quickstart: Use a blocklist with the REST API"
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
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource</a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, [supported region](../../overview.md#region-availability), and supported pricing tier. Then select **Create**.
   * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. Copy the endpoint and either of the key values to a temporary location for later use.
* Also [create an Azure blob storage container](https://ms.portal.azure.com/#create/Microsoft.StorageAccount-ARM) where you'll keep your training annotation file.
* One of the following installed:
   * [cURL](https://curl.haxx.se/) for REST API calls.
   * [Python 3.x](https://www.python.org/) installed


## Prepare your training data

To train a custom category, you need example text data that represents the category you want to detect. In this guide, you can use sample data. The provided annotation file contains text prompts about survival advice in camping/wilderness situations. The trained model will learn to detect this type of content in new text data.

> [!TIP]
> For tips on creating your own data set, see the [How-to guide](../../how-to/custom-categories.md#prepare-your-training-data).

1. Download the [sample text data file](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/ContentSafety/survival-advice.jsonl) from the GitHub repository.
1. Upload the _.jsonl_ file to your Azure Storage account blob container. Then copy the blob URL to a temporary location for later use.

> [!IMPORTANT]
> **The user's storage account is set up as a hierarchical namespace account, which cannot be supported by Custom Categories. Please try using a regular storage account instead.**
For example, your blob URL cannot be split into two layers, such as example/example1/, and should only have one layer. For more details, refer to the documentation: [Azure Data Lake Storage hierarchical namespace - Azure Storage](/azure/storage/blobs/data-lake-storage-namespace).
>
### Grant storage access 

[!INCLUDE [storage-account-access](../storage-account-access.md)]

## Create and train a custom category

#### [cURL](#tab/curl)

In the command below, replace `<your_api_key>`, `<your_endpoint>`, and other necessary parameters with your own values. Then enter each command in a terminal window and run it.

### Create new category version

```bash
curl -X PUT "<your_endpoint>/contentsafety/text/categories/<your_category_name>?api-version=2024-09-15-preview" \
     -H "Ocp-Apim-Subscription-Key: <your_api_key>" \
     -H "Content-Type: application/json" \
     -d "{
            \"categoryName\": \"survival-advice\",
            \"definition\": \"text prompts about survival advice in camping/wilderness situations\",
            \"sampleBlobUrl\": \"https://<your-azure-storage-url>/example-container/survival-advice.jsonl\"
        }"
```

> [!TIP]
> Every time you change your category name, definition or samples, a new version will be created. You can use the version number to trace back to previous versions. Please remember this version number, as it will be required in the URL for the next step- training custom categories.


#### API Request

| Field        | Description      | Example Value    |
|--------|--------------|---------------------|
| `categoryName`   | The name of the category or topic the request relates to.              | survival-advice             |
| `definition`     | A brief description of the content type for the category.      | text prompts about survival advice in camping/wilderness situations           |
| `sampleBlobUrl`  | URL to access a sample JSONL file containing data examples for the category.    | Link      |



#### API Response

| Field     | Description    | Example Value    |
|------------------------|---|---------|
| `categoryName`         | The name of the category or topic the response relates to.     | survival-advice        |
| `definition`           | A brief description of the content type for the category.         | text prompts about survival advice in camping/wilderness situations                                                           |
| `sampleBlobUrl`        | URL to access a sample JSONL file containing data examples for the category.                     | Link                 |
| `sampleBlobSnapshotUrl`| Snapshot URL of the sample JSONL file, which provides access to a specific version of the data.  | Snapshot URL |
| `version`              | The version number of the category data.     | 1      |
| `createdTime`          | Timestamp when the category data was created.      | 2024-10-28T22:06:59.4626988Z         |
| `status`         | Current status of the category data processing.       | Succeeded         |


### Start the category build process

Replace <your_api_key> and <your_endpoint> with your own values, and also **append the version number in the url you obtained from the last step.** Allow enough time for model training: the end-to-end execution of custom category training can take from around five hours to ten hours. Plan your moderation pipeline accordingly. After you receive the response, store the operation ID (referred to as `id`) in a temporary location. This ID will be necessary for retrieving the build status using the **Get status** API in the next section.

```bash
curl -X POST "<your_endpoint>/contentsafety/text/categories/survival-advice:build?api-version=2024-09-15-preview&version={version}" \
     -H "Ocp-Apim-Subscription-Key: <your_api_key>" \
     -H "Content-Type: application/json"
```

#### API Response

| Field      | Description                                   | Example Value                                 |
|------------|-----------------------------------------------|-----------------------------------------------|
| `operation id`       | Unique identifier for retrieving the build status | b6c69dc1-2338-484e-85a5b-xxxxxxxxxxxx          |
| `status`   | Current status of the request                 | Succeeded                                     |


### Get the category build status

To retrieve the status, utilize the `id` obtained from the previous API response and place it in the path of the API below.

```bash
curl -X GET "<your_endpoint>/contentsafety/text/categories/operations/<id>?api-version=2024-09-15-preview" \
     -H "Ocp-Apim-Subscription-Key: <your_api_key>" \
     -H "Content-Type: application/json"
```

#### API Response

| Field      | Description                                   | Example Value                                 |
|------------|-----------------------------------------------|-----------------------------------------------|
| `operation id`       | Unique identifier for retrieving the build status | b6c69dc1-2338-484e-855b-xxxxxxxxxxxx          |
| `status`   | Current status of the request                 | Succeeded                                     |

## Analyze text with a customized category

Run the following command to analyze text with your customized category. Replace `<your_api_key>` and `<your_endpoint>` with your own values.

```bash
curl -X POST "<your_endpoint>/contentsafety/text:analyzeCustomCategory?api-version=2024-09-15-preview" \
     -H "Ocp-Apim-Subscription-Key: <your_api_key>" \
     -H "Content-Type: application/json" \
     -d "{
            \"text\": \"<Example text to analyze>\",
            \"categoryName\": \"survival-advice\", 
            \"version\": 1
        }"
```

#### API Request
| Field          | Description                                             |
|----------------|---------------------------------------------------------|
| `text`         | The text content or message intended for category detection |
| `categoryName` | The name of the category the text aims to be detected under |
| `version`      | Version number of the category                         |
#### API Response
| Field                    | Description                                             | Example Value |
|--------------------------|---------------------------------------------------------|---------------|
| `customCategoryAnalysis` | Object containing the analysis result for the category. | —             |
| `detected`               | Indicates whether the specified category was detected.  | false         |


#### [Python](#tab/python)

First, you need to install the required Python library:

```bash
pip install requests
```

Then, open a new Python script and define the necessary variables with your own Azure resource details:

```python
import requests

API_KEY = '<your_api_key>'
ENDPOINT = '<your_endpoint>'

headers = {
    'Ocp-Apim-Subscription-Key': API_KEY,
    'Content-Type': 'application/json'
}
```

### Create a new category

You can create a new category with *category name*, *definition* and *sample_blob_url*, and you'll get the autogenerated version number of this category.

```python
def create_new_category_version(category_name, definition, sample_blob_url):
    url = f"{ENDPOINT}/contentsafety/text/categories/{category_name}?api-version=2024-09-15-preview"
    data = {
        "categoryName": category_name,
        "definition": definition,
        "sampleBlobUrl": sample_blob_url
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Replace the parameters with your own values
category_name = "survival-advice"
definition = "text prompts about survival advice in camping/wilderness situations"
sample_blob_url = "https://<your-azure-storage-url>/example-container/survival-advice.jsonl"

result = create_new_category_version(category_name, definition, sample_blob_url)
print(result)
```

### Start the category build process

You can start the category build process with the *category name* and *version number*. Allow enough time for model training: the end-to-end execution of custom category training can take from around five hours to ten hours. Plan your moderation pipeline accordingly. After receiving the response, ensure that you store the operation ID (referred to as `id`) somewhere like your notebook. This ID will be necessary for retrieving the build status using the ‘get_build_status’ function in the next section.

```python
def trigger_category_build_process(category_name, version):
    url = f"{ENDPOINT}/contentsafety/text/categories/{category_name}:build?api-version=2024-09-15-preview&version={version}"
    response = requests.post(url, headers=headers)
    return response.status_code

# Replace the parameters with your own values
category_name = "survival-advice"
version = 1

result = trigger_category_build_process(category_name, version)
print(result)
```

### Get the category build status:

To retrieve the status, utilize the `id` obtained from the previous response.

```python
def get_build_status(id):
    url = f"{ENDPOINT}/contentsafety/text/categories/operations/{id}?api-version=2024-09-15-preview"
    response = requests.get(url, headers=headers)
    return response.status_code

# Replace the parameter with your own value
id = "your-operation-id"

result = get_build_status(id)
print(result)
```


## Analyze text with a customized category

You need to specify the *category name* and the *version number* (optional; the service uses the latest one by default) during inference. You can specify multiple categories if they're already defined.

```python
def analyze_text_with_customized_category(text, category_name, version):
    url = f"{ENDPOINT}/contentsafety/text:analyzeCustomCategory?api-version=2024-09-15-preview"
    data = {
        "text": text,
        "categoryName": category_name,
        "version": version
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Replace the parameters with your own values
text = "<Example text to analyze>"
category_name = "survival-advice"
version = 1

result = analyze_text_with_customized_category(text, category_name, version)
print(result)
```
---


## Other custom categories operations

Remember to replace the placeholders below with your actual values for the API key, endpoint, and specific content (category name, definition, and so on). These examples help you to manage the customized categories in your account.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

#### [cURL](#tab/curl)

### Get a customized category or a specific version of it

Replace the placeholders with your own values and run the following command in a terminal window:

```bash
curl -X GET "<endpoint>/contentsafety/text/categories/<your_category_name>?api-version=2024-09-15-preview&version=1" \
     -H "Ocp-Apim-Subscription-Key: <your_api_key>" \
     -H "Content-Type: application/json"
```

### List categories of their latest versions

Replace the placeholders with your own values and run the following command in a terminal window:

```bash
curl -X GET "<endpoint>/contentsafety/text/categories?api-version=2024-09-15-preview" \
     -H "Ocp-Apim-Subscription-Key: <your_api_key>" \
     -H "Content-Type: application/json"
```

### Delete a customized category or a specific version of it

Replace the placeholders with your own values and run the following command in a terminal window:

```bash
curl -X DELETE "<endpoint>/contentsafety/text/categories/<your_category_name>?api-version=2024-09-15-preview&version=1" \
     -H "Ocp-Apim-Subscription-Key: <your_api_key>" \
     -H "Content-Type: application/json"
```

#### [Python](#tab/python)

First, make sure you've installed the required Python library:

```bash
pip install requests
```

Then, set up the necessary configurations with your own AI resource details:

```python
import requests

API_KEY = '<your_api_key>'
ENDPOINT = '<your_endpoint>'

headers = {
    'Ocp-Apim-Subscription-Key': API_KEY,
    'Content-Type': 'application/json'
}
```

### Get a customized category or a specific version of it

Replace the placeholders with your own values and run the following code in your Python script:

```python
def get_customized_category(category_name, version=None):
    url = f"{ENDPOINT}/contentsafety/text/categories/{category_name}?api-version=2024-09-15-preview"
    if version:
        url += f"&version={version}"
    
    response = requests.get(url, headers=headers)
    return response.json()

# Replace the parameters with your own values
category_name = "DrugAbuse"
version = 1

result = get_customized_category(category_name, version)
print(result)
```

### List categories of their latest versions

```python
def list_categories_latest_versions():
    url = f"{ENDPOINT}/contentsafety/text/categories?api-version=2024-09-15-preview"
    response = requests.get(url, headers=headers)
    return response.json()

result = list_categories_latest_versions()
print(result)
```

### Delete a customized category or a specific version of it

Replace the placeholders with your own values and run the following code in your Python script:

```python
def delete_customized_category(category_name, version=None):
    url = f"{ENDPOINT}/contentsafety/text/categories/{category_name}?api-version=2024-09-15-preview"
    if version:
        url += f"&version={version}"
    
    response = requests.delete(url, headers=headers)
    return response.status_code

# Replace the parameters with your own values
category_name = "<your_category_name>"
version = 1

result = delete_customized_category(category_name, version)
print(result)
```

---