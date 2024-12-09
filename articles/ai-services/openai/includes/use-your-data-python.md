---
#services: cognitive-services
manager: nitinme
author: mrbullwinkle #travisw
ms.author: mbullwin #travisw
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/07/2024
---

[!INCLUDE [Set up required variables](./use-your-data-common-variables.md)]

## Create a Python environment

1. Create a new folder named *openai-python* for your project and a new Python code file named *main.py*. Change into that directory:

```cmd
mkdir openai-python
cd openai-python
```

2. Install the following Python Libraries:

# [OpenAI Python 1.x](#tab/python-new)

```console
pip install openai
pip install python-dotenv
```

# [OpenAI Python 0.28.1](#tab/python)

[!INCLUDE [Deprecation](../includes/deprecation.md)]

```console
pip install openai==0.28.1
pip install python-dotenv
```

---
  
## Create the Python app

1. From the project directory, open the *main.py* file and add the following code:

# [OpenAI Python 1.x](#tab/python-new)

```python
import os
import openai
import dotenv

dotenv.load_dotenv()

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID")

client = openai.AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-01",
)

completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": "What are my available health plans?",
        },
    ],
    extra_body={
        "data_sources":[
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": os.environ["AZURE_AI_SEARCH_ENDPOINT"],
                    "index_name": os.environ["AZURE_AI_SEARCH_INDEX"],
                    "authentication": {
                        "type": "api_key",
                        "key": os.environ["AZURE_AI_SEARCH_API_KEY"],
                    }
                }
            }
        ],
    }
)

print(completion.model_dump_json(indent=2))
```

# [OpenAI Python 0.28.1](#tab/python)

   ```python
   import os
   import openai
   import dotenv
   import requests

   dotenv.load_dotenv()

   openai.api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")

   # Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version
   openai.api_version = "2023-08-01-preview"
   openai.api_type = 'azure'
   openai.api_key = os.environ.get("AZURE_OPENAI_API_KEY")

   def setup_byod(deployment_id: str) -> None:
       """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.
    
       :param deployment_id: The deployment ID for the model to use with your own data.

       To remove this configuration, simply set openai.requestssession to None.
       """

       class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)

       session = requests.Session()

       # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
       session.mount(
           prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
           adapter=BringYourOwnDataAdapter()
       )

       openai.requestssession = session

   aoai_deployment_id = os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID")
   setup_byod(aoai_deployment_id)

   completion = openai.ChatCompletion.create(
       messages=[{"role": "user", "content": "What are my available health plans?"}],
       deployment_id=os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID"),
       dataSources=[  # camelCase is intentional, as this is the format the API expects
           {
               "type": "AzureCognitiveSearch",
               "parameters": {
                   "endpoint": os.environ.get("AZURE_AI_SEARCH_ENDPOINT"),
                   "key": os.environ.get("AZURE_AI_SEARCH_API_KEY"),
                   "indexName": os.environ.get("AZURE_AI_SEARCH_INDEX"),
               }
           }
       ]
   )
   print(completion)
   ```

---

> [!IMPORTANT]
> For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see the Azure AI services [security](../../security-features.md) article.

2. Execute the following command:

```cmd
python main.py
```

The application prints the response in a JSON format suitable for use in many scenarios. It includes both answers to your query and citations from your uploaded files.
