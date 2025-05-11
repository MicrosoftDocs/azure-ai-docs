---
title: 'Quickstart: Use the OpenAI Service via the Python SDK'
titleSuffix: Azure OpenAI Service
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the Python SDK. 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/26/2025
---

<a href="https://github.com/openai/openai-python" target="_blank">Library source code</a> | <a href="https://pypi.org/project/openai/" target="_blank">Package (PyPi)</a> |

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>
- The following Python libraries: os, requests, json
- An Azure OpenAI Service resource with a `gpt-35-turbo-instruct` model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).


## Set up

Install the OpenAI Python client library with:

```console
pip install openai
```

> [!NOTE]
> This library is maintained by OpenAI. Refer to the [release history](https://github.com/openai/openai-python/releases) to track the latest updates to the library.

## Retrieve key and endpoint

To successfully make a call against the Azure OpenAI Service, you'll need the following:

|Variable name | Value |
|--------------------------|-------------|
| `ENDPOINT`               | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. You can also find the endpoint via the **Deployments** page in Azure AI Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`.|
| `API-KEY` | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|
| `DEPLOYMENT-NAME` | This value will correspond to the custom name you chose for your deployment when you deployed a model. This value can be found under **Resource Management** > **Model Deployments** in the Azure portal or via the **Deployments** page in Azure AI Foundry portal.|

Go to your resource in the Azure portal. The **Keys and Endpoint** can be found in the **Resource Management** section. Copy your endpoint and access key as you'll need both for authenticating your API calls. You can use either `KEY1` or `KEY2`. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot of the overview blade for an Azure OpenAI resource in the Azure portal with the endpoint & access keys location circled in red." lightbox="../media/quickstarts/endpoint.png":::

[!INCLUDE [environment-variables](environment-variables.md)]


## Create a new Python application

1. Create a new Python file called quickstart.py. Then open it up in your preferred editor or IDE.

2. Replace the contents of quickstart.py with the following code. Modify the code to add your key, endpoint, and deployment name: 

# [Microsoft Entra ID](#tab/entra)

```python
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)
    
client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
    azure_ad_token_provider=token_provider,
    api_version="2024-10-21"
    )
    
deployment_name='REPLACE_WITH_YOUR_DEPLOYMENT_NAME' #This will correspond to the custom name you chose for your deployment when you deployed a model. Use a gpt-35-turbo-instruct deployment. 
    
# Send a completion call to generate an answer
print('Sending a test completion job')
start_phrase = 'Write a tagline for an ice cream shop. '
response = client.completions.create(model=deployment_name, prompt=start_phrase, max_tokens=10)
print(start_phrase+response.choices[0].text)
```

# [API Key](#tab/key)

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

```python
import os
from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-10-21",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
deployment_name='REPLACE_WITH_YOUR_DEPLOYMENT_NAME' #This will correspond to the custom name you chose for your deployment when you deployed a model. Use a gpt-35-turbo-instruct deployment. 
    
# Send a completion call to generate an answer
print('Sending a test completion job')
start_phrase = 'Write a tagline for an ice cream shop. '
response = client.completions.create(model=deployment_name, prompt=start_phrase, max_tokens=10)
print(start_phrase+response.choices[0].text)
```

---

> [!IMPORTANT]
> For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see this [security](../../security-features.md) article.

1. Run the application with the `python` command on your quickstart file:

    ```console
    python quickstart.py
    ```

## Output

The output will include response text following the `Write a tagline for an ice cream shop.` prompt. Azure OpenAI returned `The coldest ice cream in town!` in this example.

```console
Sending a test completion job
Write a tagline for an ice cream shop. The coldest ice cream in town!
```

Run the code a few more times to see what other types of responses you get as the response won't always be the same.

### Understanding your results

Since our example of `Write a tagline for an ice cream shop.` provides little context, it's normal for the model to not always return expected results. You can adjust the maximum number of tokens if the response seems unexpected or truncated.

Azure OpenAI also performs content moderation on the prompt inputs and generated outputs. The prompts or responses might be filtered if harmful content is detected. For more information, see the [content filter](../concepts/content-filter.md) article.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Learn more about how to generate the best completion in our [How-to guide on completions](../how-to/completions.md).
* For more examples check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
