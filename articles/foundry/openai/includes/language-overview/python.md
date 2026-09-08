---
title: Azure OpenAI Python support
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Azure OpenAI Python support.
author: alvinashcraft
manager: mcleans
ms.author: aashcraft
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.date: 07/20/2026
ms.custom: include, classic-and-new, doc-kit-assisted
ai-usage: ai-assisted
---

[Source code](https://github.com/openai/openai-python) | [Package](https://pypi.org/project/openai/) | [API reference](https://github.com/openai/openai-python/blob/main/api.md)

The examples require Python 3.9 or later. They were tested with `openai` 2.46.0 and `azure-identity` 1.25.3. Use `openai` 1.106.0 or later when you pass a Microsoft Entra token provider as `api_key`.

## Install the packages

Install the OpenAI and Azure Identity packages:

```bash
pip install openai azure-identity
```

The command installs both packages in the active Python environment.

## Create a response with Microsoft Entra ID

Use `DefaultAzureCredential` and `get_bearer_token_provider` to authenticate without storing an API key. The token provider refreshes the access token when needed.

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)
openai = OpenAI(base_url=endpoint, api_key=token_provider)

response = openai.responses.create(
    model="gpt-5-mini",
    input="Explain the purpose of an API in one sentence.",
)
print(response.output_text)
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`OpenAI` client](https://github.com/openai/openai-python) and [`get_bearer_token_provider`](/python/api/azure-identity/azure.identity?view=azure-python&preserve-view=true#azure-identity-get-bearer-token-provider)

## Create a response with an API key

API keys aren't recommended for production use. Store the key in the `AZURE_OPENAI_API_KEY` environment variable instead of placing it in source code.

```bash
export AZURE_OPENAI_API_KEY="<your-api-key>"
```

Then create the client and request:

```python
import os
from openai import OpenAI

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
api_key = os.environ["AZURE_OPENAI_API_KEY"]
openai = OpenAI(base_url=endpoint, api_key=api_key)

response = openai.responses.create(
    model="gpt-5-mini",
    input="Explain the purpose of an API in one sentence.",
)
print(response.output_text)
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`responses.create`](https://github.com/openai/openai-python/blob/main/README.md#usage)

## Use Chat Completions

For new applications, use the Responses API. Use Chat Completions when you need its message-based interface or are maintaining an existing application.

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)
openai = OpenAI(base_url=endpoint, api_key=token_provider)

completion = openai.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain the purpose of an API."},
    ],
)
print(completion.choices[0].message.content)
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`chat.completions.create`](https://github.com/openai/openai-python/blob/main/README.md#chat-completions)

## Stream a response

Set `stream` to `True`, and process text delta events as the model generates them:

```python
import os
from openai import OpenAI

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
openai = OpenAI(
    base_url=endpoint,
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

# Stream text as the model generates it.
stream = openai.responses.create(
    model="gpt-5-mini",
    input="Explain the purpose of an API in one sentence.",
    stream=True,
)
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
```

The following streamed output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`responses.create` streaming](https://github.com/openai/openai-python#streaming-responses)

## Handle errors and retries

The SDK automatically retries connection errors, timeouts, HTTP 408, 409, 429, and 5xx responses twice with exponential backoff. Set `max_retries` on the `OpenAI` client to change this behavior. Catch `openai.APIStatusError` to inspect the HTTP status, request ID, and response for a failed request.

The following example sets four retries and records the request ID for successful and failed requests:

```python
import os
import openai as openai_sdk
from openai import OpenAI

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
openai = OpenAI(
    base_url=endpoint,
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    max_retries=4,
)

try:
    # Send the request and record its request ID.
    response = openai.responses.create(
        model="gpt-5-mini",
        input="Explain the purpose of an API in one sentence.",
    )
    print(response.output_text)
    print(f"Request ID: {response._request_id}")
except openai_sdk.APIStatusError as error:
    print(f"Status: {error.status_code}; Request ID: {error.request_id}")
    raise
```

For a successful request, the following output is representative. The response text and request ID vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
Request ID: <request-id>
```

Reference: [Request IDs, errors, and retries](https://github.com/openai/openai-python#request-ids)

## More SDK examples

- [Use the Responses API](../../how-to/responses.md)
- [Generate embeddings](../../how-to/embeddings.md)
- [Analyze images](../../how-to/gpt-with-vision.md)
- [Fine-tune a model](../../how-to/fine-tuning.md)
