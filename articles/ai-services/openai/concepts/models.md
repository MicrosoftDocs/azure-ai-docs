---
title: Azure OpenAI Service models
titleSuffix: Azure OpenAI
description: Learn about the different model capabilities that are available with Azure OpenAI.
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 10/09/2024
ms.custom: references_regions, build-2023, build-2023-dataai, refefences_regions
manager: nitinme
author: mrbullwinkle #ChrisHMSFT
ms.author: mbullwin #chrhoder
recommendations: false
---

# Azure OpenAI Service models

Azure OpenAI Service is powered by a diverse set of models with different capabilities and price points. Model availability varies by region and cloud. For Azure Government model availability, please refer to [Azure Government OpenAI Service](../azure-government.md).

| Models | Description |
|--|--|
| [o1-preview and o1-mini](#o1-preview-and-o1-mini-models-limited-access) | Limited access models, specifically designed to tackle reasoning and problem-solving tasks with increased focus and capability.  |
| [GPT-4o & GPT-4o mini & GPT-4 Turbo](#gpt-4o-and-gpt-4-turbo) | The latest most capable Azure OpenAI models with multimodal versions, which can accept both text and images as input. |
| [GPT-4o audio](#gpt-4o-audio) | A GPT-4o model that supports low-latency, "speech in, speech out" conversational interactions. |
| [GPT-4](#gpt-4) | A set of models that improve on GPT-3.5 and can understand and generate natural language and code. |
| [GPT-3.5](#gpt-35) | A set of models that improve on GPT-3 and can understand and generate natural language and code. |
| [Embeddings](#embeddings-models) | A set of models that can convert text into numerical vector form to facilitate text similarity. |
| [DALL-E](#dall-e-models) | A series of models that can generate original images from natural language. |
| [Whisper](#whisper-models) | A series of models in preview that can transcribe and translate speech to text. |
| [Text to speech](#text-to-speech-models-preview) (Preview) | A series of models in preview that can synthesize text to speech. |

## o1-preview and o1-mini models limited access

The Azure OpenAI `o1-preview` and `o1-mini` models are specifically designed to tackle reasoning and problem-solving tasks with increased focus and capability. These models spend more time processing and understanding the user's request, making them exceptionally strong in areas like science, coding, and math compared to previous iterations.

|  Model ID  | Description | Max Request (tokens) | Training Data (up to)  |
|  --- |  :--- |:--- |:---: |
|`o1-preview` (2024-09-12) | The most capable model in the o1 series, offering enhanced reasoning abilities.| Input: 128,000  <br> Output: 32,768 | Oct 2023 |
| `o1-mini` (2024-09-12) | A faster and more cost-efficient option in the o1 series, ideal for coding tasks requiring speed and lower resource consumption.| Input: 128,000  <br> Output: 65,536 | Oct 2023 |

### Availability

The `o1-preview` and `o1-mini` models are now available for API access and model deployment. **Registration is required, and access will be granted based on Microsoft's eligibility criteria**.

Request access: [limited access model application](https://aka.ms/oai/modelaccess)

Once access has been granted, you will need to create a deployment for each model.

### API support

Support for the **o1 series** models was added in API version `2024-09-01-preview`.

The `max_tokens` parameter has been deprecated and replaced with the new `max_completion_tokens` parameter. **o1 series** models will only work with the `max_completion_tokens` parameter.

### Usage

These models do not currently support the same set of parameters as other models that use the chat completions API. Only a very limited subset is currently supported, so common parameters like `temperature`, `top_p`, are not available and including them will cause your request to fail. `o1-preview` and `o1-mini` models will also not accept the system message role as part of the messages array.

# [Python (Microsoft Entra ID)](#tab/python-secure)

You may need to upgrade your version of the OpenAI Python library to take advantage of the new `max_completion_tokens` parameter.

```cmd
pip install openai --upgrade
```

If you are new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI Service with Microsoft Entra ID authentication](../how-to/managed-identity.md).

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2024-09-01-preview"
)

response = client.chat.completions.create(
    model="o1-preview-new", # replace with the model deployment name of your o1-preview, or o1-mini model
    messages=[
        {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
    ],
    max_completion_tokens = 5000

)

print(response.model_dump_json(indent=2))
```

# [Python (key-based auth)](#tab/python)

You may need to upgrade your version of the OpenAI Python library to take advantage of the new `max_completion_tokens` parameter.

```cmd
pip install openai --upgrade
```

```python

from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-09-01-preview"
)

response = client.chat.completions.create(
    model="o1-preview-new", # replace with the model deployment name of your o1-preview, or o1-mini model
    messages=[
        {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
    ],
    max_completion_tokens = 5000

)

print(response.model_dump_json(indent=2))
```

# [Output](#tab/python-output)

```json
{
  "id": "chatcmpl-AEj7pKFoiTqDPHuxOcirA9KIvf3yz",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "Writing your first Python API is an exciting step in developing software that can communicate with other applications. An API (Application Programming Interface) allows different software systems to interact with each other, enabling data exchange and functionality sharing. Here are the steps you should consider when creating your first Python API:\n\n1. **Define the Purpose and Requirements**\n\n   - **Identify the Functionality**: Clearly outline what your API is supposed to do. What data or services will it provide to the users?\n   - **Determine the Endpoints**: Plan the different URLs (endpoints) through which users can access the API functionalities.\n   - **Specify Request and Response Formats**: Decide on the data formats (usually JSON) for incoming requests and outgoing responses.\n\n2. **Choose the Right Framework**\n\n   Python offers several frameworks for building APIs. Two of the most popular are:\n\n   - **Flask**: A lightweight and flexible web framework, great for small to medium-sized APIs.\n   - **FastAPI**: A modern, high-performance framework for building APIs with Python 3.6+ types, offering automatic interactive documentation.\n\n   **Example**:\n   ```bash\n   pip install flask\n   ```\n   or\n   ```bash\n   pip install fastapi uvicorn\n   ```\n\n3. **Set Up the Development Environment**\n\n   - **Create a Virtual Environment**: Isolate your project dependencies using `venv` or `conda`.\n   - **Install Required Packages**: Ensure all necessary libraries and packages are installed.\n\n   **Example**:\n   ```bash\n   python -m venv env\n   source env/bin/activate  # On Windows use `env\\Scripts\\activate`\n   ```\n\n4. **Implement the API Endpoints**\n\n   - **Write the Code for Each Endpoint**: Implement the logic that handles requests and returns responses.\n   - **Use Decorators to Define Routes**: In frameworks like Flask, you use decorators to specify the URL endpoints.\n\n   **Example with Flask**:\n   ```python\n   from flask import Flask, request, jsonify\n\n   app = Flask(__name__)\n\n   @app.route('/hello', methods=['GET'])\n   def hello_world():\n       return jsonify({'message': 'Hello, World!'})\n\n   if __name__ == '__main__':\n       app.run(debug=True)\n   ```\n\n5. **Handle Data Serialization and Deserialization**\n\n   - **Parsing Incoming Data**: Use libraries to parse JSON or other data formats from requests.\n   - **Formatting Output Data**: Ensure that responses are properly formatted in JSON or XML.\n\n6. **Implement Error Handling**\n\n   - **Handle Exceptions Gracefully**: Provide meaningful error messages and HTTP status codes.\n   - **Validate Input Data**: Check for required fields and appropriate data types to prevent errors.\n\n   **Example**:\n   ```python\n   @app.errorhandler(404)\n   def resource_not_found(e):\n       return jsonify(error=str(e)), 404\n   ```\n\n7. **Add Authentication and Authorization (If Necessary)**\n\n   - **Secure Endpoints**: If your API requires, implement security measures such as API keys, tokens (JWT), or OAuth.\n   - **Manage User Sessions**: Handle user login states and permissions appropriately.\n\n8. **Document Your API**\n\n   - **Use Tools Like Swagger/OpenAPI**: Automatically generate interactive API documentation.\n   - **Provide Usage Examples**: Help users understand how to interact with your API.\n\n   **Example with FastAPI**:\n   FastAPI automatically generates docs at `/docs` using Swagger UI.\n\n9. **Test Your API**\n\n   - **Write Unit and Integration Tests**: Ensure each endpoint works as expected.\n   - **Use Testing Tools**: Utilize tools like `unittest`, `pytest`, or API testing platforms like Postman.\n\n   **Example**:\n   ```python\n   import unittest\n   class TestAPI(unittest.TestCase):\n       def test_hello_world(self):\n           response = app.test_client().get('/hello')\n           self.assertEqual(response.status_code, 200)\n   ```\n\n10. **Optimize Performance**\n\n    - **Improve Response Times**: Optimize your code and consider using asynchronous programming if necessary.\n    - **Manage Resource Utilization**: Ensure your API can handle the expected load.\n\n11. **Deploy Your API**\n\n    - **Choose a Hosting Platform**: Options include AWS, Heroku, DigitalOcean, etc.\n    - **Configure the Server**: Set up the environment to run your API in a production setting.\n    - **Use a Production Server**: Instead of the development server, use WSGI servers like Gunicorn or Uvicorn.\n\n    **Example**:\n    ```bash\n    uvicorn main:app --host 0.0.0.0 --port 80\n    ```\n\n12. **Monitor and Maintain**\n\n    - **Logging**: Implement logging to track events and errors.\n    - **Monitoring**: Use monitoring tools to track performance and uptime.\n    - **Update and Patch**: Keep dependencies up to date and patch any security vulnerabilities.\n\n13. **Consider Versioning**\n\n    - **Plan for Updates**: Use versioning in your API endpoints to manage changes without breaking existing clients.\n    - **Example**:\n      ```python\n      @app.route('/v1/hello', methods=['GET'])\n      ```\n\n14. **Gather Feedback and Iterate**\n\n    - **User Feedback**: Encourage users to provide feedback on your API.\n    - **Continuous Improvement**: Use the feedback to make improvements and add features.\n\n**Additional Tips**:\n\n- **Keep It Simple**: Start with a minimal viable API and expand functionality over time.\n- **Follow RESTful Principles**: Design your API according to REST standards to make it intuitive and standard-compliant.\n- **Security Best Practices**: Always sanitize inputs and protect against common vulnerabilities like SQL injection and cross-site scripting (XSS).\nBy following these steps, you'll be well on your way to creating a functional and robust Python API. Good luck with your development!",
        "refusal": null,
        "role": "assistant",
        "function_call": null,
        "tool_calls": null
      },
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "protected_material_code": {
          "filtered": false,
          "detected": false
        },
        "protected_material_text": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ],
  "created": 1728073417,
  "model": "o1-preview-2024-09-12",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_503a95a7d8",
  "usage": {
    "completion_tokens": 1843,
    "prompt_tokens": 20,
    "total_tokens": 1863,
    "completion_tokens_details": {
      "audio_tokens": null,
      "reasoning_tokens": 448
    },
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 0
    }
  },
  "prompt_filter_results": [
    {
      "prompt_index": 0,
      "content_filter_results": {
        "custom_blocklists": {
          "filtered": false
        },
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "jailbreak": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ]
}
```

---

### Region availability

Available for standard and global standard deployment in East US, East US2, North Central US, South Central US, Sweden Central, West US, and West US3 for approved customers.

## GPT-4o audio

The `gpt-4o-realtime-preview` model is part of the GPT-4o model family and supports low-latency, "speech in, speech out" conversational interactions. GPT-4o audio is designed to handle real-time, low-latency conversational interactions, making it a great fit for support agents, assistants, translators, and other use cases that need highly responsive back-and-forth with a user.

GPT-4o audio is available in the East US 2 (`eastus2`) and Sweden Central (`swedencentral`) regions. To use GPT-4o audio, you need to [create](../how-to/create-resource.md) or use an existing resource in one of the supported regions.

When your resource is created, you can [deploy](../how-to/create-resource.md#deploy-a-model) the GPT-4o audio model. If you are performing a programmatic deployment, the **model** name is `gpt-4o-realtime-preview`. For more information on how to use GPT-4o audio, see the [GPT-4o audio documentation](../realtime-audio-quickstart.md).

Details about maximum request tokens and training data are available in the following table.

|  Model ID  | Description | Max Request (tokens) | Training Data (up to)  |
|  --- |  :--- |:--- |:---: |
|`gpt-4o-realtime-preview` (2024-10-01-preview) <br> **GPT-4o audio** | **Audio model** for real-time audio processing |Input: 128,000  <br> Output: 4,096 | Oct 2023 |

## GPT-4o and GPT-4 Turbo

GPT-4o integrates text and images in a single model, enabling it to handle multiple data types simultaneously. This multimodal approach enhances accuracy and responsiveness in human-computer interactions. GPT-4o matches GPT-4 Turbo in English text and coding tasks while offering superior performance in non-English languages and vision tasks, setting new benchmarks for AI capabilities.

### How do I access the GPT-4o and GPT-4o mini models?

GPT-4o and GPT-4o mini are available for **standard** and **global-standard** model deployment.

You need to [create](../how-to/create-resource.md) or use an existing resource in a [supported standard](#gpt-4-and-gpt-4-turbo-model-availability) or [global standard](#global-standard-model-availability) region where the model is available.

When your resource is created, you can [deploy](../how-to/create-resource.md#deploy-a-model) the GPT-4o models. If you are performing a programmatic deployment, the **model** names are:

- `gpt-4o` **Version** `2024-08-06`
- `gpt-4o`, **Version**  `2024-05-13`
- `gpt-4o-mini` **Version** `2024-07-18`

### GPT-4 Turbo

GPT-4 Turbo is a large multimodal model (accepting text or image inputs and generating text) that can solve difficult problems with greater accuracy than any of OpenAI's previous models. Like GPT-3.5 Turbo, and older GPT-4 models GPT-4 Turbo is optimized for chat and works well for traditional completions tasks.

[!INCLUDE [GPT-4 Turbo](../includes/gpt-4-turbo.md)]

## GPT-4

GPT-4 is the predecessor to GPT-4 Turbo. Both the GPT-4 and GPT-4 Turbo models have a base model name of `gpt-4`. You can distinguish between the GPT-4 and Turbo models by examining the model version.

- `gpt-4` **Version** `0314`
- `gpt-4` **Version** `0613`
- `gpt-4-32k` **Version** `0613`

You can see the token context length supported by each model in the [model summary table](#model-summary-table-and-region-availability).

## GPT-4 and GPT-4 Turbo models

- These models can only be used with the Chat Completion API.

See [model versions](../concepts/model-versions.md) to learn about how Azure OpenAI Service handles model version upgrades, and [working with models](../how-to/working-with-models.md) to learn how to view and configure the model version settings of your GPT-4 deployments.

|  Model ID  | Description | Max Request (tokens) | Training Data (up to)  |
|  --- |  :--- |:--- |:---: |
|`gpt-4o` (2024-08-06) <br> **GPT-4o (Omni)** | **Latest large GA model** <br> - Structured outputs<br> - Text, image processing <br> - JSON Mode <br> - parallel function calling <br> - Enhanced accuracy and responsiveness <br> - Parity with English text and coding tasks compared to GPT-4 Turbo with Vision <br> - Superior performance in non-English languages and in vision tasks |Input: 128,000  <br> Output: 16,384 | Oct 2023 |
|`gpt-4o-mini` (2024-07-18) <br> **GPT-4o mini** | **Latest small GA model** <br> - Fast, inexpensive, capable model ideal for replacing GPT-3.5 Turbo series models. <br> - Text, image processing <br>- JSON Mode <br> - parallel function calling | Input: 128,000 <br> Output: 16,384  | Oct 2023 |
|`gpt-4o` (2024-05-13) <br> **GPT-4o (Omni)** | Text, image processing <br> - JSON Mode <br> - parallel function calling <br> - Enhanced accuracy and responsiveness <br> - Parity with English text and coding tasks compared to GPT-4 Turbo with Vision <br> - Superior performance in non-English languages and in vision tasks |Input: 128,000  <br> Output: 4,096| Oct 2023 |
| `gpt-4` (turbo-2024-04-09) <br>**GPT-4 Turbo with Vision** | **New GA model** <br> - Replacement for all previous GPT-4 preview models (`vision-preview`, `1106-Preview`, `0125-Preview`). <br> - [**Feature availability**](#gpt-4o-and-gpt-4-turbo) is currently different depending on method of input, and deployment type. | Input: 128,000  <br> Output: 4,096  | Dec 2023 |
| `gpt-4` (0125-Preview)*<br>**GPT-4 Turbo Preview** | **Preview Model** <br> -Replaces 1106-Preview <br>- Better code generation performance <br> - Reduces cases where the model doesn't complete a task <br> - JSON Mode <br> - parallel function calling <br> - reproducible output (preview) | Input: 128,000  <br> Output: 4,096           | Dec 2023         |
| `gpt-4` (vision-preview)<br>**GPT-4 Turbo with Vision Preview**  | **Preview model** <br> - Accepts text and image input. <br> - Supports enhancements <br> - JSON Mode <br> - parallel function calling <br> - reproducible output (preview) | Input: 128,000  <br> Output: 4,096              | Apr 2023       |
| `gpt-4` (1106-Preview)<br>**GPT-4 Turbo Preview** | **Preview Model** <br> - JSON Mode <br> - parallel function calling <br> - reproducible output (preview) | Input: 128,000  <br> Output: 4,096 | Apr 2023         |
| `gpt-4-32k` (0613) | **Older GA model** <br> - Basic function calling with tools  | 32,768               | Sep 2021         |
| `gpt-4` (0613)     | **Older GA model** <br> - Basic function calling with tools | 8,192                | Sep 2021         |
| `gpt-4-32k`(0314)  | **Older GA model** <br> - [Retirement information](./model-retirements.md#current-models) | 32,768               | Sep 2021         |
| `gpt-4` (0314) | **Older GA model** <br> - [Retirement information](./model-retirements.md#current-models)  | 8,192 | Sep 2021         |

> [!CAUTION]
> We don't recommend using preview models in production. We will upgrade all deployments of preview models to either future preview versions or to the latest stable GA version. Models designated preview do not follow the standard Azure OpenAI model lifecycle.

- GPT-4 version 0125-preview is an updated version of the GPT-4 Turbo preview previously released as version 1106-preview.  
- GPT-4 version 0125-preview completes tasks such as code generation more completely compared to gpt-4-1106-preview. Because of this, depending on the task, customers may find that GPT-4-0125-preview generates more output compared to the gpt-4-1106-preview.  We recommend customers compare the outputs of the new model.  GPT-4-0125-preview also addresses bugs in gpt-4-1106-preview with UTF-8 handling for non-English languages. 
- GPT-4 version `turbo-2024-04-09` is the latest GA release and replaces `0125-Preview`, `1106-preview`, and `vision-preview`.

> [!IMPORTANT]
> The GPT-4 (`gpt-4`) versions `1106-Preview`, `0125-Preview`, and `vision-preview` will be upgraded with a stable version of `gpt-4` in the future. 
> - Deployments of `gpt-4` versions `1106-Preview`, `0125-Preview`, and `vision-preview` set to "Auto-update to default" and "Upgrade when expired" will start to be upgraded after the stable version is released. For each deployment, a model version upgrade takes place with no interruption in service for API calls. Upgrades are staged by region and the full upgrade process is expected to take 2 weeks. 
> - Deployments of `gpt-4` versions  `1106-Preview`, `0125-Preview`, and `vision-preview` set to "No autoupgrade" will not be upgraded and will stop operating when the preview version is upgraded in the region. 
> See [Azure OpenAI model retirements and deprecations](./model-retirements.md) for more information on the timing of the upgrade.

## GPT-3.5

GPT-3.5 models can understand and generate natural language or code. The most capable and cost effective model in the GPT-3.5 family is GPT-3.5 Turbo, which has been optimized for chat and works well for traditional completions tasks as well. GPT-3.5 Turbo is available for use with the Chat Completions API. GPT-3.5 Turbo Instruct has similar capabilities to `text-davinci-003` using the Completions API instead of the Chat Completions API.  We recommend using GPT-3.5 Turbo and GPT-3.5 Turbo Instruct over [legacy GPT-3.5 and GPT-3 models](./legacy-models.md).


|  Model ID   | Description | Max Request (tokens) | Training Data (up to) |
|  --------- |:---|:------:|:----:|
| `gpt-35-turbo` (0125) **NEW** | **Latest GA Model** <br> - JSON Mode <br> - parallel function calling <br> - reproducible output (preview) <br> - Higher accuracy at responding in requested formats. <br> - Fix for a bug which caused a text encoding issue for non-English language function calls.  | Input: 16,385<br> Output: 4,096  | Sep 2021 |
| `gpt-35-turbo` (1106) | **Older GA Model** <br> - JSON Mode <br> - parallel function calling <br> - reproducible output (preview) | Input: 16,385<br> Output: 4,096 |  Sep 2021|
| `gpt-35-turbo-instruct` (0914) | **Completions endpoint only** <br> - Replacement for [legacy completions models](./legacy-models.md) | 4,097 |Sep 2021 |
| `gpt-35-turbo-16k` (0613) | **Older GA Model** <br> - Basic function calling with tools | 16,384 | Sep 2021 |
| `gpt-35-turbo` (0613) | **Older GA Model** <br> - Basic function calling with tools   | 4,096 | Sep 2021 |
| `gpt-35-turbo`**<sup>1</sup>** (0301) |  **Older GA Model**  <br> - [Retirement information](./model-retirements.md#current-models) | 4,096 | Sep 2021 |

To learn more about how to interact with GPT-3.5 Turbo and the Chat Completions API check out our [in-depth how-to](../how-to/chatgpt.md).

**<sup>1</sup>** This model will accept requests > 4,096 tokens. It is not recommended to exceed the 4,096 input token limit as the newer version of the model are capped at 4,096 tokens. If you encounter issues when exceeding 4,096 input tokens with this model this configuration is not officially supported.

## Embeddings

 `text-embedding-3-large` is the latest and most capable embedding model. Upgrading between embeddings models is not possible. In order to move from using `text-embedding-ada-002` to `text-embedding-3-large` you would need to generate new embeddings. 

- `text-embedding-3-large`
- `text-embedding-3-small`
- `text-embedding-ada-002`

In testing, OpenAI reports both the large and small third generation embeddings models offer better average multi-language retrieval performance with the [MIRACL](https://github.com/project-miracl/miracl) benchmark while still maintaining performance for English tasks with the [MTEB](https://github.com/embeddings-benchmark/mteb) benchmark.

|Evaluation Benchmark| `text-embedding-ada-002` | `text-embedding-3-small` |`text-embedding-3-large` |
|---|---|---|---|
| MIRACL average | 31.4 | 44.0 | 54.9 |
| MTEB average | 61.0 | 62.3 | 64.6 |

The third generation embeddings models support reducing the size of the embedding via a new `dimensions` parameter. Typically larger embeddings are more expensive from a compute, memory, and storage perspective. Being able to adjust the number of dimensions allows more control over overall cost and performance. The `dimensions` parameter is not supported in all versions of the OpenAI 1.x Python library, to take advantage of this parameter  we recommend upgrading to the latest version: `pip install openai --upgrade`.

OpenAI's MTEB benchmark testing found that even when the third generation model's dimensions are reduced to less than `text-embeddings-ada-002` 1,536 dimensions performance remains slightly better.

## DALL-E

The DALL-E models generate images from text prompts that the user provides. DALL-E 3 is generally available for use with the REST APIs. DALL-E 2 and DALL-E 3 with client SDKs are in preview.

## Whisper

The Whisper models can be used for speech to text.

You can also use the Whisper model via Azure AI Speech [batch transcription](../../speech-service/batch-transcription-create.md) API. Check out [What is the Whisper model?](../../speech-service/whisper-overview.md) to learn more about when to use Azure AI Speech vs. Azure OpenAI Service.

## Text to speech (Preview)

The OpenAI text to speech models, currently in preview, can be used to synthesize text to speech.

You can also use the OpenAI text to speech voices via Azure AI Speech. To learn more, see [OpenAI text to speech voices via Azure OpenAI Service or via Azure AI Speech](../../speech-service/openai-voices.md#openai-text-to-speech-voices-via-azure-openai-service-or-via-azure-ai-speech) guide. 

## Model summary table and region availability

> [!NOTE]
> This article primarily covers model/region availability that applies to all Azure OpenAI customers with deployment types of **Standard**. Some select customers have access to model/region combinations that are not listed in the unified table below. For more information on Provisioned deployments, see our [Provisioned guidance](./provisioned-throughput.md).

### Standard deployment model availability

[!INCLUDE [Standard Models](../includes/model-matrix/standard-models.md)]

This table doesn't include fine-tuning regional availability information.  Consult the [fine-tuning section](#fine-tuning-models) for this information.

For information on default quota, refer to the [quota and limits article](../quotas-limits.md).

### Provisioned deployment model availability

[!INCLUDE [Provisioned](../includes/model-matrix/provisioned-models.md)]

> [!NOTE]
> The provisioned version of `gpt-4` **Version:** `turbo-2024-04-09` is currently limited to text only.

For more information on Provisioned deployments, see our [Provisioned guidance](./provisioned-throughput.md).

### Global standard model availability

[!INCLUDE [Standard Global](../includes/model-matrix/standard-global.md)]

### Global provisioned managed model availability

[!INCLUDE [Provisioned Managed Global](../includes/model-matrix/provisioned-global.md)]

### Global batch model availability

[!INCLUDE [Global batch](../includes/model-matrix/global-batch.md)]

### GPT-4 and GPT-4 Turbo model availability

#### Public cloud regions

[!INCLUDE [GPT-4](../includes/model-matrix/standard-gpt-4.md)]

#### Select customer access

In addition to the regions above which are available to all Azure OpenAI customers, some select pre-existing customers have been granted access to versions of GPT-4 in additional regions:

| Model | Region |  
|---|:---|  
| `gpt-4` (0314) <br> `gpt-4-32k` (0314) | East US <br> France Central <br> South Central US <br> UK South |  
| `gpt-4` (0613) <br> `gpt-4-32k` (0613) | East US <br> East US 2 <br> Japan East <br> UK South |  

### GPT-3.5 models

> [!IMPORTANT]
> The NEW `gpt-35-turbo (0125)`  model has various improvements, including higher accuracy at responding in requested formats and a fix for a bug which caused a text encoding issue for non-English language function calls.

GPT-3.5 Turbo is used with the Chat Completion API. GPT-3.5 Turbo version 0301 can also be used with the Completions API, though this is not recommended.  GPT-3.5 Turbo versions 0613 and 1106 only support the Chat Completions API.

GPT-3.5 Turbo version 0301 is the first version of the model released.  Version 0613 is the second version of the model and adds function calling support.

See [model versions](../concepts/model-versions.md) to learn about how Azure OpenAI Service handles model version upgrades, and [working with models](../how-to/working-with-models.md) to learn how to view and configure the model version settings of your GPT-3.5 Turbo deployments.

### GPT-3.5-Turbo model availability

#### Public cloud regions

[!INCLUDE [GPT-35-Turbo](../includes/model-matrix/standard-gpt-35-turbo.md)]

### Embeddings models

These models can only be used with Embedding API requests.

> [!NOTE]
> `text-embedding-3-large` is the latest and most capable embedding model. Upgrading between embedding models is not possible. In order to migrate from using `text-embedding-ada-002` to `text-embedding-3-large` you would need to generate new embeddings.  

|  Model ID | Max Request (tokens) | Output Dimensions |Training Data (up-to)
|---|---| :---:|:---:|:---:|
| `text-embedding-ada-002` (version 2) |8,192 | 1,536 | Sep 2021 |
| `text-embedding-ada-002` (version 1) |2,046 | 1,536 | Sep 2021 |
| `text-embedding-3-large` | 8,192 | 3,072 |Sep 2021 |
| `text-embedding-3-small` | 8,192|  1,536 | Sep 2021 |

> [!NOTE]
> When sending an array of inputs for embedding, the max number of input items in the array per call to the embedding endpoint is 2048.

#### Public cloud regions

[!INCLUDE [Embeddings](../includes/model-matrix/standard-embeddings.md)]

### DALL-E models

|  Model ID  | Feature Availability | Max Request (characters) |
|  --- |  --- | :---: |
| dalle2 (preview) | East US | 1,000 |
| dall-e-3 | East US, Australia East, Sweden Central | 4,000 |

### Fine-tuning models

`babbage-002` and `davinci-002` are not trained to follow instructions. Querying these base models should only be done as a point of reference to a fine-tuned version to evaluate the progress of your training.

`gpt-35-turbo` - fine-tuning of this model is limited to a subset of regions, and is not available in every region the base model is available.  

|  Model ID  | Fine-Tuning Regions | Max Request (tokens) | Training Data (up to) |
|  --- | --- | :---: | :---: |
| `babbage-002` | North Central US <br> Sweden Central  <br> Switzerland West | 16,384 | Sep 2021 |
| `davinci-002` | North Central US <br> Sweden Central  <br> Switzerland West | 16,384 | Sep 2021 |
| `gpt-35-turbo` (0613) | East US2 <br> North Central US <br> Sweden Central <br> Switzerland West | 4,096 | Sep 2021 |
| `gpt-35-turbo` (1106) | East US2 <br> North Central US <br> Sweden Central <br> Switzerland West | Input: 16,385<br> Output: 4,096 |  Sep 2021|
| `gpt-35-turbo` (0125)  | East US2 <br> North Central US <br> Sweden Central <br> Switzerland West | 16,385 | Sep 2021 |
| `gpt-4` (0613) <sup>**1**</sup> | North Central US <br> Sweden Central | 8192 | Sep 2021 |
| `gpt-4o-mini` <sup>**1**</sup> (2024-07-18) | North Central US <br> Sweden Central | Input: 128,000 <br> Output: 16,384  <br> Training example context length: 64,536 | Oct 2023 |
| `gpt-4o` <sup>**1**</sup> (2024-08-06) | East US2 <br> North Central US <br> Sweden Central | Input: 128,000 <br> Output: 16,384  <br> Training example context length: 64,536 | Oct 2023 | 

**<sup>1</sup>** GPT-4, GPT-4o, and GPT-4o mini fine-tuning is currently in public preview. See our [GPT-4, GPT-4o,  & GPT-4o mini fine-tuning safety evaluation guidance](/azure/ai-services/openai/how-to/fine-tuning?tabs=turbo%2Cpython-new&pivots=programming-language-python#safety-evaluation-gpt-4-fine-tuning---public-preview) for more information.

### Whisper models

|  Model ID  | Model Availability | Max Request (audio file size) |
|  --- |  --- | :---: |
| `whisper` | East US 2 <br> North Central US <br> Norway East <br> South India <br> Sweden Central <br> West Europe | 25 MB |

### Text to speech models (Preview)

|  Model ID  | Model Availability |
|  --- |  --- | :---: |
| `tts-1` | North Central US <br> Sweden Central |
| `tts-1-hd` | North Central US <br> Sweden Central |

### Assistants (Preview)

For Assistants you need a combination of a supported model, and a supported region. Certain tools and capabilities require the latest models. The following models are available in the Assistants API, SDK, Azure AI Studio and Azure OpenAI Studio. The following table is for pay-as-you-go. For information on Provisioned Throughput Unit (PTU) availability, see [provisioned throughput](./provisioned-throughput.md). The listed models and regions can be used with both Assistants v1 and v2. You can use [global standard models](#global-standard-model-availability) if they are supported in the regions listed below. 

| Region | `gpt-35-turbo (0613)` | `gpt-35-turbo (1106)`| `fine tuned gpt-3.5-turbo-0125` | `gpt-4 (0613)` | `gpt-4 (1106)` | `gpt-4 (0125)` | `gpt-4o (2024-05-13)` | `gpt-4o-mini (2024-07-18)` |
|-----|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Australia East | ✅ | ✅ | | ✅ |✅ | | | |
| East US  | ✅ | | | | | ✅ | ✅ |✅|
| East US 2 | ✅ |  | ✅ | ✅ |✅ | |✅| |
| France Central  | ✅ | ✅ | | ✅ |✅ |  | | |
| Japan East | ✅ |  | | | | | | |
| Norway East | |  | | | ✅ |  | | |
| Sweden Central | ✅ |✅ | ✅ |✅ |✅| |✅| |
| UK South | ✅  | ✅ | | | ✅ | ✅ |  | |
| West US |  | ✅ | | | ✅ | |✅| |
| West US 3 |  |  | | |✅ | |✅| |

## Model retirement

For the latest information on model retirements, refer to the [model retirement guide](./model-retirements.md).

## Next steps

- [Model retirement and deprecation](./model-retirements.md)
- [Learn more about working with Azure OpenAI models](../how-to/working-with-models.md)
- [Learn more about Azure OpenAI](../overview.md)
- [Learn more about fine-tuning Azure OpenAI models](../how-to/fine-tuning.md)