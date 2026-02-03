---
author: laujan
ms.author: lajanuar
ms.date: 11/18/2025
ms.service: azure-ai-language
ms.topic: include
ms.custom:
  - language-service-pii
  - ignite-2024
  - build-2025
ai-usage: ai-assisted
---
[Reference documentation](/python/api/azure-ai-textanalytics/azure.ai.textanalytics?view=azure-python&preserve-view=true) |  [More samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/textanalytics/azure-ai-textanalytics/samples) | [Package (PyPi)](https://pypi.org/project/azure-ai-textanalytics/5.2.0/) | [Library source code](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/textanalytics/azure-ai-textanalytics)

Use this quickstart to create a Personally Identifiable Information (PII) detection application with the client library for Python. In the following example, you'll create a Python application that can identify [recognized sensitive information](../../concepts/entity-categories.md) in text.


## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* Once you have your Azure subscription, [create a Foundry resource](../../../../../ai-services/multi-service-resource.md?pivots=azportal).
* [Python 3.8 or later](https://www.python.org/)

## Setting up

[!INCLUDE [Create an Azure resource](../../../includes/create-resource.md)]

[!INCLUDE [Get your key and endpoint](../../../includes/get-key-endpoint.md)]

[!INCLUDE [Create environment variables](../../../includes/environment-variables.md)]

### Install the client library

After installing Python, you can install the client library with:

```console
pip install azure-ai-textanalytics==5.2.0
```



## Code example

Create a new Python file and copy the below code. Then run the code.

```python
import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
language_key = os.environ.get("LANGUAGE_KEY")
language_endpoint = os.environ.get("LANGUAGE_ENDPOINT")

if not language_key or not language_endpoint:
        raise ValueError("Missing LANGUAGE_KEY or LANGUAGE_ENDPOINT environment variables")

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for detecting sensitive information (PII) from text 
def pii_recognition_example(client):
    documents = [
        "The employee's SSN is 859-98-0987.",
        "The employee's phone number is 555-555-5555."
    ]
    response = client.recognize_pii_entities(documents, language="en")
    result = [doc for doc in response if not doc.is_error]
    for doc in result:
        print("Redacted Text: {}".format(doc.redacted_text))
        for entity in doc.entities:
            print("Entity: {}".format(entity.text))
            print("\tCategory: {}".format(entity.category))
            print("\tConfidence Score: {}".format(entity.confidence_score))
            print("\tOffset: {}".format(entity.offset))
            print("\tLength: {}".format(entity.length))
pii_recognition_example(client)
```



## Output

```console
Redacted Text: The ********'s SSN is ***********.
Entity: employee
        Category: PersonType
        Confidence Score: 0.97
        Offset: 4
        Length: 8
Entity: 859-98-0987
        Category: USSocialSecurityNumber
        Confidence Score: 0.65
        Offset: 22
        Length: 11
Redacted Text: The ********'s phone number is ************.
Entity: employee
        Category: PersonType
        Confidence Score: 0.96
        Offset: 4
        Length: 8
Entity: 555-555-5555
        Category: PhoneNumber
        Confidence Score: 0.8
        Offset: 31
        Length: 12
```
