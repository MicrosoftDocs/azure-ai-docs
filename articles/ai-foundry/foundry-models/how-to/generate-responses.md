---
title: How to generate text responses with Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Learn how to prompt Microsoft Foundry Models to generate text, using the Responses API.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/07/2026
ms.author: mopeakande
author: msakande
ms.reviewer: achand
reviewer: achandmsft
ms.custom: generated
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# How to generate text responses with Microsoft Foundry Models

[!INCLUDE [version-banner](../../includes/version-banner.md)]

This article explains how to generate text responses for Foundry Models, such as Microsoft AI, DeepSeek, and Grok models, by using the Responses API. For a full list of the Foundry Models that support use of the Responses API, see [Supported Foundry Models](#supported-foundry-models). 

## Prerequisites

To use the Responses API with deployed models in your application, you need:

- An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Microsoft Foundry Models](../how-to/quickstart-github-models.md) if that's your case.

- A Foundry project. This kind of project is managed under a Foundry resource. If you don't have a Foundry project, see [Create a project for Microsoft Foundry](../../how-to/create-projects.md).

- Your Foundry project's endpoint URL, which is of the form `https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME`.

- A deployment of a Foundry Model, such as the `MAI-DS-R1` model used in this article. If you don't have a deployment already, see [Add and configure Foundry Models](create-model-deployments.md) to a model deployment to your resource.

## Use the Responses API to generate text

Use the code in this section to make Responses API calls for Foundry Models. In the code samples, you create the client to consume the model and then send it a basic request. 

> [!NOTE]
> Use keyless authentication with **Microsoft Entra ID**. To learn more about keyless authentication, see [What is Microsoft Entra authentication?](/entra/identity/authentication/overview-authentication) and [DefaultAzureCredential](/azure/developer/python/sdk/authentication/overview#defaultazurecredential).


# [Python](#tab/python)

1. Install libraries, including the Azure Identity client library:

    ```bash
    pip install azure-identity
    pip install openai
    pip install --pre azure-ai-projects>=2.0.0b1 
    ```

1. Use the following code to configure the OpenAI client object in the project route, specify your deployment, and generate responses. 
   
    ```python
    import os
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    
    project_client = AIProjectClient(
        endpoint="https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME",
        credential=DefaultAzureCredential(),
    )
    
    openai_client = project_client.get_openai_client()
    
    response = openai_client.responses.create(
        model="MAI-DS-R1", # Replace with your deployment name, not the model ID 
        input="What is the capital/major city of France?",
    )
    
    print(response.model_dump_json(indent=2)) 
    ```

# [C#](#tab/dotnet)

1. Install the Azure Identity client library:

    ```dotnetcli
    dotnet add package Azure.Identity
    ```

1. Use the following code to configure the OpenAI client object in the project route, specify your deployment, and generate responses. 

    ```csharp
    using Azure.Identity;
    using Azure.AI.Projects; 
    using Azure.AI.Projects.OpenAI;
    using OpenAI.Responses;

    #pragma warning disable OPENAI001

    const string deploymentName = "MAIDSR1"; // Replace with your deployment name, not the model ID 
    const string endpoint = "https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME";
    
    AIProjectClient projectClient = new(new Uri(endpoint), new DefaultAzureCredential());
    
    ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForModel(deploymentName);
    
    ResponseResult response = responseClient.CreateResponse("What is the capital/major city of France?");
    
    Console.WriteLine($"[ASSISTANT]: {response.GetOutputText()}");
    ```

# [JavaScript](#tab/javascript)

[JavaScript v1 examples](../../openai/supported-languages.md)

1. Install the Azure Identity client library before you can use DefaultAzureCredential:

    ```bash
    npm install @azure/identity
    ```

1. Use the following code to configure the OpenAI client object in the project route, specify your deployment, and generate responses.  

    ```javascript
    import { AIProjectClient } from "@azure/ai-projects";
    import { DefaultAzureCredential } from "@azure/identity";
    
    const endpoint = "https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME";
    const deploymentName = "MAI-DS-R1"; // Replace with your deployment name, not the model ID 
    
    async function main() {
        const projectClient = new AIProjectClient(endpoint, new DefaultAzureCredential());
        const openAIClient = await projectClient.getOpenAIClient();
    
        const response = await openAIClient.responses.create({
            model: deploymentName,
            input: "What is the capital/major city of France?"
        });
        console.log(response.output_text);
    }
    
    main();
    ```


# [Java](#tab/Java)

Authentication with Microsoft Entra ID requires some initial setup. First, install the Azure Identity client library. For more options on how to install this library, see [Azure Identity client library for Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/identity/azure-identity/README.md#include-the-package).


1. Add the Azure Identity client library:

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
        <version>1.18.0</version>
    </dependency>
    ```

    After setup, choose which type of credential from `azure.identity` to use. For example, use `DefaultAzureCredential` to authenticate the client. Authentication is easiest with `DefaultAzureCredential`, as it finds the best credential to use in its running environment.

1. Use the following code to configure the OpenAI client object in the project route, specify your deployment, and generate responses.  

    ```java
    import com.azure.ai.agents;
    import com.azure.core.util.Configuration;
    import com.azure.identity.DefaultAzureCredentialBuilder;
    import com.openai.models.responses.Response;
    import com.openai.models.responses.ResponseCreateParams;
    
    public class Sample {
        public static void main(String[] args) {
            String endpoint = "https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME";
            String deploymentName = "MAI-DS-R1"; // Replace with your deployment name, not the model ID
            
            ResponsesClient responsesClient = new AgentsClientBuilder()
                    .credential(new DefaultAzureCredentialBuilder().build())
                    .endpoint(endpoint)
                    .serviceVersion(AgentsServiceVersion.V2025_11_15_PREVIEW)
                    .buildResponsesClient();
    
            ResponseCreateParams responseRequest = new ResponseCreateParams.Builder()
                    .input("What is the capital/major city of France?")
                    .model(deploymentName)
                    .build();
    
            Response response = responsesClient.getResponseService().create(responseRequest);
        }
    }
   ```


# [REST](#tab/rest)

```bash
curl -X POST https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME/openai/responses?api-version={{API_VERSION}} \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \

-d '{
    "model": "MAI-DS-R1",
    "input": "What is the capital/major city of France?"
}'
```

---

## Supported Foundry Models

A selection of Foundry Models are supported for use with the Responses API.

#### View supported models in the Foundry portal

[!INCLUDE [agent-service-view-models-in-portal](../../agents/includes/agent-service-view-models-in-portal.md)]

#### List of supported models

This section lists some of the Foundry Models that are supported for use with the Responses API. For the Azure OpenAI models that are supported, see [Available Azure OpenAI models](../../agents/concepts/model-region-support.md#available-models).

[!INCLUDE [agent-service-models-support-list](../../agents/includes/agent-service-models-support-list.md)]

## Related content

- [Migrate from Azure AI Inference SDK to OpenAI SDK](../../how-to/model-inference-to-openai-migration.md)
- [Azure OpenAI supported programming languages](../../openai/supported-languages.md)
- [Switch between OpenAI and Azure OpenAI endpoints](/azure/developer/ai/how-to/switching-endpoints)
- [Generate chat completions with Foundry Models, using the OpenAI v1 chat completions API ](../../openai/api-version-lifecycle.md#model-support)




