---
title: How to get started with Azure AI Foundry SDK
titleSuffix: Azure AI Foundry
description: This article provides an overview of the Azure AI Foundry SDK and how to get started using it.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 03/27/2025
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
zone_pivot_groups: programming-languages-sdk-overview
# customer intent: I want to learn how to use the Azure AI Foundry SDK to build AI applications on Azure.
---

# The Azure AI Foundry SDK

The [Azure AI Foundry](https://ai.azure.com) SDK is a comprehensive toolchain designed to simplify the development of AI applications on Azure. It enables developers to:

- Access popular models from various model providers through a single interface
- Easily combine together models, data, and AI services to build AI-powered applications
- Evaluate, debug, and improve application quality & safety across development, testing, and production environments
 
The Azure AI Foundry SDK is a set of packages and services designed to work together. You can use the [Azure AI Projects client library](/python/api/overview/azure/ai-projects-readme) to easily use multiple services through a single project client and connection string. You can also use services and SDKs on their own and connect directly to your services.

If you want to jump right in and start building an app, check out:

- [Create a chat app](../../quickstarts/get-started-code.md)
- [Create a custom RAG app](../../tutorials/copilot-sdk-create-resources.md)

## Prerequisites

* An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
* [Create a project](../create-projects.md) if you don't have one already.
* Sign in with the Azure CLI using the same account that you use to access your AI Project:

    ```bash
    az login
    ```

## Install everything

Install all the Azure AI Foundry SDK packages as shown here, or install only the packages you need in the following sections.

::: zone pivot="programming-language-python"

1. Create a file named **requirements.txt**. Add the following packages to the file:

    ```txt
    azure-ai-projects 
    azure-identity 
    openai 
    azure-ai-inference 
    azure-search-documents 
    azure-ai-evaluation 
    azure-monitor-opentelemetry
    ```

1. Install the packages:

    ```bash
    pip install -r requirements.txt
    ```

---

::: zone-end

::: zone pivot="programming-language-csharp"

```dotnet
dotnet add package Azure.AI.Projects
dotnet add package Azure.Identity
dotnet add package Azure.AI.OpenAI
dotnet add package Azure.AI.Inference
dotnet add package Azure.Search.Documents
```

Add using statements:

```csharp
using Azure.Identity;
using Azure.AI.Projects;
using OpenAI.Chat;
using Azure.AI.OpenAI;
using Azure.AI.Inference;
using Azure.Search.Documents;
using Azure.Search.Documents.Models;
```

---

::: zone-end


## Get started with projects

The best way to get started using the Azure AI Foundry SDK is by using a project. AI projects connect together different data, assets, and services you need to build AI applications. The AI project client allows you to easily access these project components from your code by using a single connection string.

Install the Azure AI projects client library:

::: zone pivot="programming-language-python"

```bash
pip install azure-ai-projects azure-identity
```

Create a project client in code:

# [Sync](#tab/sync)

```Python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
 
project_connection_string="your_connection_string"

project = AIProjectClient.from_connection_string(
  conn_str=project_connection_string,
  credential=DefaultAzureCredential())
```

# [Async](#tab/async)

```Python
from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects.aio import AIProjectClient
 
project_connection_string="your_connection_string"

project = await AIProjectClient.from_connection_string(
  conn_str=project_connection_string,
  credential=DefaultAzureCredential())
```

---

::: zone-end

::: zone pivot="programming-language-csharp"

```dotnet
dotnet add package Azure.AI.Projects
dotnet add package Azure.Identity
```

Add using statements:

```csharp
using Azure.Identity;
using Azure.AI.Projects;
```

Create a project client in code:

# [Sync](#tab/sync)

```csharp
var connectionString = "<your_connection_string>";
var projectClient = new AIProjectClient(connectionString, new DefaultAzureCredential());
```

# [Async](#tab/async)

Not yet available in C#.

::: zone-end

Copy the **Project connection string** from the **Overview** page of the project and update the connections string value above.

Once you create the project client, you can use the client for the capabilities in the following sections.

::: zone pivot="programming-language-python"

Be sure to check out the [reference](https://aka.ms/aifoundrysdk/reference) and [samples](https://aka.ms/azsdk/azure-ai-projects/python/samples).

::: zone-end

::: zone pivot="programming-language-csharp"

Be sure to check out the [reference](https://aka.ms/aifoundrysdk/reference) and [samples](https://aka.ms/aifoundrysdk/dotnetsamples).

::: zone-end

## Azure OpenAI in Foundry Models

The [Azure OpenAI in Azure AI Foundry Models](../../../ai-services/openai/overview.md) provides access to OpenAI's models including the GPT-4o, GPT-4o mini, GPT-4, GPT-4 Turbo with Vision, DALLE-3, Whisper, and Embeddings model series with the data residency, scalability, safety, security, and enterprise capabilities of Azure.

If you have code that uses the OpenAI SDK, you can easily target your code to use Azure OpenAI in Foundry Models. First, install the OpenAI SDK:

::: zone pivot="programming-language-python"

```bash
pip install openai
```

If you have existing code that uses the OpenAI SDK, you can use the project client to create an `AzureOpenAI` client that uses your project's Azure OpenAI connection:

```Python
openai = project.inference.get_azure_openai_client(api_version="2024-06-01")
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful writing assistant"},
        {"role": "user", "content": "Write me a poem about flowers"},
    ]
)

print(response.choices[0].message.content)
```

::: zone-end

::: zone pivot="programming-language-csharp"

```dotnet
dotnet add package Azure.AI.OpenAI
```

Add using statements:

```csharp
using OpenAI.Chat;
using Azure.AI.OpenAI;
```

If you have existing code that uses the OpenAI SDK, you can use the project client to create an `AzureOpenAI` client that uses your project's Azure OpenAI connection:

```csharp
var connections = projectClient.GetConnectionsClient();
ConnectionResponse connection = connections.GetDefaultConnection(ConnectionType.AzureOpenAI, withCredential: true);
var properties = connection.Properties as ConnectionPropertiesApiKeyAuth;

if (properties == null) {
    throw new Exception("Invalid auth type, expected API key auth");
}

// Create and use an Azure OpenAI client
AzureOpenAIClient azureOpenAIClient = new(
    new Uri(properties.Target),
    new AzureKeyCredential(properties.Credentials.Key));

// This must match the custom deployment name you chose for your model
ChatClient chatClient = azureOpenAIClient.GetChatClient("gpt-4o-mini");

ChatCompletion completion = chatClient.CompleteChat(
    [
        new SystemChatMessage("You are a helpful assistant that talks like a pirate."),
        new UserChatMessage("Does Azure OpenAI support customer managed keys?"),
        new AssistantChatMessage("Yes, customer managed keys are supported by Azure OpenAI"),
        new UserChatMessage("Do other Azure AI services support this too?")
    ]);

Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");
```

::: zone-end

If you're already using the [Azure OpenAI SDK](../../../ai-services/openai/chatgpt-quickstart.md) directly against Azure OpenAI, the project provides a convenient way to use Azure OpenAI's capabilities alongside the rest of the Azure AI Foundry capabilities.

## Azure AI Foundry Models service

The [Foundry Models](/azure/ai-studio/ai-services/model-inference) offers access to powerful models from leading providers like OpenAI, Microsoft, Meta, and more. These models support tasks such as content generation, summarization, and code generation. 

To use the model inference service, first ensure that your project has an AI Services connection (in the management center).

Install the `azure-ai-inference` client library:

::: zone pivot="programming-language-python"

```bash
pip install azure-ai-inference
```

You can use the project client to get a configured and authenticated `ChatCompletionsClient` or `EmbeddingsClient`:

```Python
# get an chat inferencing client using the project's default model inferencing endpoint
chat = project.inference.get_chat_completions_client()

# run a chat completion using the inferencing client
response = chat.complete(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful writing assistant"},
        {"role": "user", "content": "Write me a poem about flowers"},
    ]
)

print(response.choices[0].message.content)
```

::: zone-end

::: zone pivot="programming-language-csharp"

```dotnet
dotnet add package Azure.AI.Inference
```

Add using statements:

```csharp
using Azure.AI.Inference;
```

You can use the project client to get a configured and authenticated `ChatCompletionsClient` or `EmbeddingsClient`:

```csharp
var connectionString = Environment.GetEnvironmentVariable("AIPROJECT_CONNECTION_STRING");
var projectClient = new AIProjectClient(connectionString, new DefaultAzureCredential());

ChatCompletionsClient chatClient = projectClient.GetChatCompletionsClient();

var requestOptions = new ChatCompletionsOptions()
{
    Messages =
        {
            new ChatRequestSystemMessage("You are a helpful assistant."),
            new ChatRequestUserMessage("How many feet are in a mile?"),
        },
    Model = "gpt-4o-mini"
};

Response<ChatCompletions> response = chatClient.Complete(requestOptions);
Console.WriteLine(response.Value.Content);
```

::: zone-end

You can change the model name to any model that you deployed to the inference service or to Azure OpenAI.

To learn more about using the Azure AI inferencing client, check out the [Azure AI model inferencing reference](/azure/ai-studio/reference/reference-model-inference-api).

::: zone pivot="programming-language-python"

## Prompt templates

The inferencing client supports creating prompt messages from templates. The template allows you to dynamically generate prompts using inputs that are available at runtime.

To use prompt templates, install the `azure-ai-inference` package:

```bash
pip install azure-ai-inference
```

You can render a prompt template from an inline string:

```Python
from azure.ai.inference.prompts import PromptTemplate

# create a prompt template from an inline string (using mustache syntax)
prompt_template = PromptTemplate.from_string(prompt_template="""
    system:
    You are a helpful writing assistant.
    The user's first name is {{first_name}} and their last name is {{last_name}}.
    
    user:
    Write me a poem about flowers
    """)
    
# generate system message from the template, passing in the context as variables
messages = prompt_template.create_messages(first_name="Jane", last_name="Doe")
print(messages)
```

> [!NOTE]
> Leading whitespace is automatically trimmed from input strings.

This code outputs messages that you can then pass to a chat completion call:

```text
[
  {'role': 'system', 'content': "You are a helpful writing assistant.\nThe user's first name is Jane and their last name is Doe."}
  {'role': 'user', 'content': 'Write me a poem about flowers'}
]
```

You can also load prompts from a [`Prompty`](https://prompty.ai) file, enabling you to also load the model name and parameters from the `.prompty` file:

```Python
from azure.ai.inference.prompts import PromptTemplate

prompt_template = PromptTemplate.from_prompty("myprompt.prompty")
messages = prompt_template.create_messages(first_name="Jane", last_name="Doe")

response = chat.complete(
    messages=messages,
    model=prompt_template.model_name,
    **prompt_template.parameters,
)
```

::: zone-end

## Azure AI Search

If you have an Azure AI Search resource connected to your project, you can also use the project client to create an Azure AI Search client using the project connection.

Install the Azure AI Search client library:

::: zone pivot="programming-language-python"

```bash
pip install azure-search-documents
```

Instantiate the search and/or search index client as desired:

```Python
from azure.core.credentials import AzureKeyCredential
from azure.ai.projects.models import ConnectionType
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

# use the project client to get the default search connection
search_connection = project.connections.get_default(
    connection_type=ConnectionType.AZURE_AI_SEARCH,
    with_credentials=True)

# Create a client to create and manage search indexes
index_client = SearchIndexClient(
    endpoint=search_connection.endpoint_url,
    credential=AzureKeyCredential(key=search_connection.key)
)

# Create a client to run search queries
search_client = SearchClient(
    index_name="your_index_name",
    endpoint=search_connection.endpoint_url,
    credential=AzureKeyCredential(key=search_connection.key)
)
```

::: zone-end

::: zone pivot="programming-language-csharp"

```dotnet
dotnet add package Azure.Search.Documents
```

Add using statements:

```csharp
using Azure.Search.Documents;
using Azure.Search.Documents.Models;
```

Instantiate the search and/or search index client as desired:

```csharp
var connections = projectClient.GetConnectionsClient();
var connection = connections.GetDefaultConnection(ConnectionType.AzureAISearch, withCredential: true).Value;

var properties = connection.Properties as ConnectionPropertiesApiKeyAuth;
if (properties == null) {
    throw new Exception("Invalid auth type, expected API key auth");
}

SearchClient searchClient = new SearchClient(
    new Uri(properties.Target),
    "products",
    new AzureKeyCredential(properties.Credentials.Key));
```


::: zone-end

To learn more about using Azure AI Search, check out [Azure AI Search documentation](/azure/search/).

## Azure AI Foundry Agent Service

Azure AI Foundry Agent Service is a fully managed service designed to empower developers to securely build, deploy, and scale high-quality, and extensible AI agents. To enable building agents for a wide range of generative AI use cases, [Azure AI Foundry Agent Service](/azure/ai-services/agents) uses an extensive ecosystem of models, tools and capabilities from OpenAI, Microsoft, and third-party providers.

## Evaluation

::: zone pivot="programming-language-python"

You can use the project client to easily connect to the Azure AI evaluation service, and models needed for running your evaluators.


```
pip install azure-ai-evaluation
```

Using the `project.scope` parameter, we can instantiate a `ViolenceEvaluator`:

```Python
from azure.ai.evaluation import ViolenceEvaluator
from azure.identity import DefaultAzureCredential

# Initializing Violence Evaluator with project information
violence_eval = ViolenceEvaluator(
    azure_ai_project=project.scope,
    credential=DefaultAzureCredential())

# Running Violence Evaluator on single input row
violence_score = violence_eval(query="what's the capital of france", response="Paris")
print(violence_score)
```

NOTE: to run violence evaluators your project needs to be in East US 2, Sweden Central, US North Central, France Central.

To learn more, check out [Evaluation using the SDK](evaluate-sdk.md).

::: zone-end

::: zone pivot="programming-language-csharp"

An Azure AI evaluation package isn't yet available for C#. For a sample on how to use Prompty and Semantic Kernel for evaluation, see the [contoso-chat-csharp-prompty](https://github.com/Azure-Samples/contoso-chat-csharp-prompty/blob/main/src/ContosoChatAPI/ContosoChat.Evaluation.Tests/Evalutate.cs) sample.

::: zone-end


## Tracing

::: zone pivot="programming-language-python"

To enable tracing, first ensure your project has an attached Application Insights resource. Go to the **Tracing** page of your project and follow instructions to create or attach Application Insights.

Install the Azure Monitor OpenTelemetry package:

```
pip install azure-monitor-opentelemetry
```

Use the following code to enable instrumentation of the Azure AI Inference SDK and logging to your AI project:

```Python
from azure.monitor.opentelemetry import configure_azure_monitor

# Enable instrumentation of AI packages (inference, agents, openai, langchain)
project.telemetry.enable()

# Log traces to the project's application insights resource
application_insights_connection_string = project.telemetry.get_connection_string()
if application_insights_connection_string:
    configure_azure_monitor(connection_string=application_insights_connection_string)
```

::: zone-end

::: zone pivot="programming-language-csharp"

Tracing isn't yet integrated into the projects package. For instructions on how to instrument and log traces from the Azure AI Inferencing package, see [azure-sdk-for-dotnet](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Inference/samples/Sample8_ChatCompletionsWithOpenTelemetry.md).

::: zone-end

## Other services and frameworks

The following sections provide helpful links to other services and frameworks that you can use with the Azure AI Foundry SDK.

### Azure AI Services

* Client libraries:

    * [Azure AI services SDKs](../../../ai-services/reference/sdk-package-resources.md?context=/azure/ai-studio/context/context)
    * [Azure AI services REST APIs](../../../ai-services/reference/rest-api-resources.md?context=/azure/ai-studio/context/context) 

* Management libraries:

    * [Azure AI Services Python Management Library](/python/api/overview/azure/mgmt-cognitiveservices-readme)
    * [Azure AI Search Python Management Library](/python/api/azure-mgmt-search/azure.mgmt.search)

### Frameworks

* Azure Machine Learning

    * [Azure Machine Learning Python SDK (v2)](/python/api/overview/azure/ai-ml-readme)
    * [Azure Machine Learning CLI (v2)](/azure/machine-learning/how-to-configure-cli)
    * [Azure Machine Learning REST API](/rest/api/azureml) 

* Prompt flow

    * [Prompt flow SDK](https://microsoft.github.io/promptflow/how-to-guides/quick-start.html)
    * [pfazure CLI](https://microsoft.github.io/promptflow/reference/pfazure-command-reference.html)
    * [pfazure Python library](https://microsoft.github.io/promptflow/reference/python-library-reference/promptflow-azure/promptflow.azure.html)

* Semantic Kernel
    * [Semantic Kernel Overview](/semantic-kernel/overview/)

* Agentic frameworks

    * [LlamaIndex](llama-index.md)
