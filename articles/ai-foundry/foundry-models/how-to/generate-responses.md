---
title: How to generate text responses with Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Learn how to prompt Microsoft Foundry Models to generate text, using the Responses API.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 11/17/2025
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

This article explains how to generate text responses for Foundry Models sold directly by Azure, such as Microsoft AI, DeepSeek, and Grok models, using the Responses API 

## Prerequisites

To use the responses API with deployed models in your application, you need:

- An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Microsoft Foundry Models](../how-to/quickstart-github-models.md) if that's your case.

- A Foundry project. This kind of project is managed under a Foundry resource. If you don't have a Foundry project, see [Create a project for Microsoft Foundry](../../how-to/create-projects.md).

- The endpoint's URL.

- A deployment of a text generation Foundry Model, such as the `MAI-DS-R1` model used in this article. If you don't have a deployment already, see [Add and configure Foundry Models](create-model-deployments.md) to a model deployment to your resource.

## Use the Responses API to generate text

Use the code in this section to make Responses API calls for [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md), such as Microsoft AI, DeepSeek, and Grok models. In the code samples, you create the client to consume the model and then send it a basic request. 

> [!NOTE]
> Use keyless authentication with **Microsoft Entra ID**. To learn more about keyless authentication, see [What is Microsoft Entra authentication?](/entra/identity/authentication/overview-authentication) and [DefaultAzureCredential](/azure/developer/python/sdk/authentication/overview#defaultazurecredential).


# [Python](#tab/python)

1. Install the Azure Identity client library:

    ```bash
    pip install azure-identity
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
        model="MAI-DS-R1-0324", # Replace with your deployment name, not the model ID 
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
    using OpenAI;
    using OpenAI.Responses;
    using System.ClientModel.Primitives;

    #pragma warning disable OPENAI001

    const string deploymentName = "MAI-DS-R1-0324"; // Replace with your deployment name, not the model ID 
    const string endpoint = "https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME";
    
    AIProjectClient projectClient = new(new Uri(endpoint), new DefaultAzureCredential());
    
    OpenAIResponseClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForModel(deploymentName);
    
    OpenAIResponse response = responseClient.CreateResponse("What is the capital/major city of France?");
    
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
    const deploymentName = "MAI-DS-R1-0324"; // Replace with your deployment name, not the model ID 
    
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

Authentication with Microsoft Entra ID requires some initial setup. First install the Azure Identity client library. For more options on how to install this library, see [Azure Identity client library for Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/identity/azure-identity/README.md#include-the-package).


1. Add the Azure Identity client library:

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
        <version>1.18.0</version>
    </dependency>
    ```

    After setup, you can choose which type of credential from `azure.identity` to use. As an example, `DefaultAzureCredential` can be used to authenticate the client. Authentication is easiest using `DefaultAzureCredential`, as it finds the best credential to use in its running environment.

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
            String deploymentName = "MAI-DS-R1-0324"; // Replace with your deployment name, not the model ID
            
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


# [REST](#tab/rest)

```bash
curl -X POST https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME/openai/responses?api-version={{API_VERSION}} \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \

-d '{
    "model": "MAI-DS-R1-0324",
    "input": "What is the capital/major city of France?"
}'
```

---

## Related content

- [Azure OpenAI supported programming languages](../../openai/supported-languages.md)
- [Switch between OpenAI and Azure OpenAI endpoints](/azure/developer/ai/how-to/switching-endpoints)
- [Use embeddings models](use-embeddings.md)
- [Use image embeddings models](use-image-embeddings.md)
- [Use reasoning models](use-chat-reasoning.md)
- [Basic Microsoft Foundry chat reference architecture](/azure/architecture/ai-ml/architecture/basic-azure-ai-foundry-chat)

::: moniker range="foundry-classic"

- [Work with chat completions API](../../openai/how-to/chatgpt.md)

::: moniker-end

