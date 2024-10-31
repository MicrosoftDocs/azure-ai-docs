---
title: Get started building a chat app using the prompt flow SDK
titleSuffix: Azure AI Studio
description: This article provides instructions on how to build a custom chat app in Python using the prompt flow SDK.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom: build-2024, devx-track-azurecli, devx-track-python
ms.topic: how-to
ms.date: 10/31/2024
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
---

# Build a custom chat app in Python using Azure AI SDK

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this quickstart, we walk you through setting up your local development environment with the prompt flow SDK. We write a prompt, run it as part of your app code, trace the LLM calls being made, and run a basic evaluation on the outputs of the LLM.

## Prerequisites

> [!IMPORTANT]
> You must have the necessary permissions to add role assignments for storage accounts in your Azure subscription. Granting permissions (adding role assignment) is only allowed by the **Owner** of the specific Azure resources. You might need to ask your Azure subscription owner (who might be your IT admin) for help to [grant access to call Azure OpenAI Service using your identity](#grant-access-to-call-azure-openai-service-using-your-identity).

* Before you can follow this quickstart, complete the [AI Studio playground quickstart](../quickstarts/get-started-playground.md) to deploy a **gpt-4o-mini** model into a project.
* Use the same project and model from the quickstart here.

## Install the Azure CLI and sign in 

[!INCLUDE [Install the Azure CLI](../includes/install-cli.md)]

Now we create our app and call the Azure OpenAI Service from code.

## Create a new Python environment

[!INCLUDE [Install Python](../includes/install-python.md)]

## Install the Azure AI SDK

[!INCLUDE [Install the Azure AI SDK](../includes/install-ai-sdk.md)]

## Configure your environment variables

Your AI services endpoint and deployment name are required to call the Azure OpenAI service from your code. In this quickstart, you save these values in a `.env` file, which is a file that contains environment variables that your application can read. You can find these values in the AI Studio chat playground. 

1. Create a `.env` file, and paste the following code:

    ```text
    CONNECTION_STRING=<your-connection-string>
    @@Anything else?  Project name?  
    ```

1. Navigate to the somewhere and get the information you need to fill in the `.env` file.


> [!WARNING]
> Key based authentication is supported but isn't recommended by Microsoft. If you want to use keys you can add your key to the `.env`, but please ensure that your `.env` is in your `.gitignore` file so that you don't accidentally check it into your git repository.

## Create a basic chat prompt and app

First create a **Prompty** file, which is the prompt template format supported by prompt flow.

Create a `chat.prompty` file and copy the following code into it:

```yaml
---
name: Chat Prompt @@OLD CODE REPLACE THIS
description: A basic prompt that uses the chat API to answer questions
model:
    api: chat
    configuration:
        type: azure_openai
    parameters:
        max_tokens: 256
        temperature: 0.2
inputs:
    chat_input:
        type: string
    chat_history:
        type: list
        is_chat_history: true
        default: []
outputs:   
  response:
    type: string
sample:
    chat_input: What is the meaning of life?
---
system:
You are an AI assistant who helps people find information.

{% for item in history %}
{{item.role}}:
{{item.content}}
{% endfor %}

user:
{{chat_input}}
```

Now let's create a Python file that uses this prompt template. Create a `chat.py` file and paste the following code into it:

```Python
# @@OLD CODE REPLACE THIS
import os
from dotenv import load_dotenv
load_dotenv()

from promptflow.core import Prompty, AzureOpenAIModelConfiguration

model_config = AzureOpenAIModelConfiguration(
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

prompty = Prompty.load("chat.prompty", model={'configuration': model_config})
result = prompty(
    chat_history=[
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."}
    ],
    chat_input="Do other Azure AI services support this too?")

print(result)
```

Now from your console, run the Python code:

```bash
python chat.py
```

You should now see the output from running the prompty:

```terminal
Yes, other Azure AI services also support various capabilities and features. Some of the Azure AI services include Azure Cognitive Services, Azure Machine Learning, Azure Bot Service, and Azure Databricks. Each of these services offers different AI capabilities and can be used for various use cases. If you have a specific service or capability in mind, feel free to ask for more details.
```

## Trace the execution of your chat code

@@DO WE STILL  HAVE THIS? Or remove this section?

Now we take a look at how prompt flow tracing can provide insights into the various LLM calls that are happening in our Python scripts.

At the start of your `chat.py` file, add the following code to enable prompt flow tracing:

```Python
from promptflow.tracing import start_trace
start_trace()
```

Rerun your `chat.py` again:

```bash
python chat.py
```

This time you see a link in the output to view a prompt flow trace of the execution:

```terminal
Starting prompt flow service...
Start prompt flow service on port 23333, version: 1.10.1.
You can stop the prompt flow service with the following command:'pf service stop'.
Alternatively, if no requests are made within 1 hours, it will automatically stop.
You can view the trace detail from the following URL:
http://localhost:23333/v1.0/ui/traces/?#collection=aistudio-python-quickstart&uiTraceId=0x59e8b9a3a23e4e8893ec2e53d6e1e521
```

If you select that link, you'll then see the trace showing the steps of the program execution, what was passed to the LLM and the response output.

:::image type="content" source="../media/quickstarts/promptflow-sdk/promptflow-tracing.png" alt-text="Screenshot of the trace showing the steps of the program execution." lightbox="../media/quickstarts/promptflow-sdk/promptflow-tracing.png":::

Prompt flow tracing also allows you to trace specific function calls and log traces to AI Studio, for more information be sure to check out [How to use tracing in the prompt flow SDK](../how-to/develop/trace-local-sdk.md).

## Evaluate your prompt

Now let's show how we can use prompt flow evaluators to generate metrics that can score the quality of the conversation on a scale from 0 to 5. We run the prompt again but this time we store the results into an array containing the full conversation, and then pass that to a `ChatEvaluator` to score.

First, install the `promptflow-evals package`:

```bash
pip install promptflow-evals
```

Now copy the following code to an `evaluate.py` file:

```Python
import os
from dotenv import load_dotenv
load_dotenv()

from promptflow.core import Prompty, AzureOpenAIModelConfiguration
from promptflow.evals.evaluators import ChatEvaluator

model_config = AzureOpenAIModelConfiguration(
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

chat_history=[
    {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
    {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."}
]
chat_input="Do other Azure AI services support this too?"

prompty = Prompty.load("chat.prompty", model={'configuration': model_config})
response = prompty(chat_history=chat_history, chat_input=chat_input)

conversation = chat_history
conversation += [
    {"role": "user", "content": chat_input},
    {"role": "assistant", "content": response}
]

chat_eval = ChatEvaluator(model_config=model_config)
score = chat_eval(conversation=conversation)

print(score)
```

Run the `evaluate.py` script:

```bash
python evaluate.py
```

You should see an output that looks like this:

```terminal
{'gpt_coherence': 5.0, 'gpt_fluency': 5.0, 'evaluation_per_turn': {'gpt_coherence': {'score': [5.0, 5.0]}, 'gpt_fluency': {'score': [5.0, 5.0]}}}
```

Looks like we scored 5 for coherence and fluency of the LLM responses on this conversation! 

For more information on how to use prompt flow evaluators, including how to make your own custom evaluators and log evaluation results to AI Studio, be sure to check out [Evaluate your app using the prompt flow SDK](../how-to/develop/evaluate-sdk.md).


## Next step

> [!div class="nextstepaction"]
> [Add data and use retrieval augmented generation (RAG) to build a custom chat app](../tutorials/copilot-sdk-create-resources.md)
