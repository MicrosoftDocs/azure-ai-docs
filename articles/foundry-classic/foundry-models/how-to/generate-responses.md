---
title: "How to generate text responses with Microsoft Foundry Models (classic)"
description: "Learn how to generate text responses from Foundry Models, such as Microsoft AI and DeepSeek models, by using the Responses API. (classic)"
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/24/2026
ms.author: mopeakande
author: msakande
ms.reviewer: achand
reviewer: achandmsft
ms.custom:
  - generated, pilot-ai-workflow-jan-2026
  - classic-and-new
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# How to generate text responses with Microsoft Foundry Models (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/foundry-models/how-to/generate-responses.md)

This article explains how to generate text responses for Foundry Models, such as Microsoft AI, DeepSeek, and Grok models, by using the Responses API. For a full list of the Foundry Models that support use of the Responses API, see [Supported Foundry Models](#supported-foundry-models). 

## Prerequisites

To use the Responses API with deployed models in your application, you need:

- An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Microsoft Foundry Models](../how-to/quickstart-github-models.md) if that's your case.

- A Foundry project. This kind of project is managed under a Foundry resource. If you don't have a Foundry project, see [Create a project for Microsoft Foundry](../../how-to/create-projects.md).

- Your Foundry project's endpoint URL, which is of the form `https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME`.

- A deployment of a Foundry Model, such as the `DeepSeek-V3.1` model used in this article. If you don't have a deployment already, see [Add and configure Foundry Models](create-model-deployments.md) to a model deployment to your resource.

### Use the AI model starter kit

The code snippets in this article are from the [AI model starter kit](https://aka.ms/ai-model-start). Use this starter kit as a quick way to get started with complete cloud infrastructure and code needed to call Foundry Models, using a stable OpenAI library with the Responses API.

## Use the Responses API to generate text

Use the code in this section to make Responses API calls for Foundry Models. In the code samples, you create the client to consume the model and then send it a basic request. 

> [!TIP]
> When you deploy a model in the Foundry portal, you assign it a deployment name. Use this deployment name (not the model catalog ID) in the `model` parameter of your API calls.

> [!NOTE]
> Use keyless authentication with **Microsoft Entra ID**. To learn more about keyless authentication, see [What is Microsoft Entra authentication?](/entra/identity/authentication/overview-authentication) and [DefaultAzureCredential](/azure/developer/python/sdk/authentication/overview#defaultazurecredential).

# [Python](#tab/python)

1. Install libraries, including the Azure Identity client library:

    ```bash
    pip install azure-identity
    pip install openai
    ```

1. Use the following code to configure the OpenAI client object in the project route, specify your deployment, and generate responses. 
   
    ```python
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    from openai import OpenAI
    
    project_endpoint = "https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME"
    # Build the base URL: project_endpoint + /openai/v1 (no api-version needed)
    base_url = project_endpoint.rstrip("/") + "/openai/v1"

    # Use get_bearer_token_provider for automatic token refresh
    credential = DefaultAzureCredential()
    client = OpenAI(
        base_url=base_url,
        api_key=get_bearer_token_provider(credential, "https://ai.azure.com/.default"),
    )   
   
    response = client.responses.create(
        model="DeepSeek-V3.1", # Replace with your deployment name, not the model ID 
        input="What are the top 3 benefits of cloud computing? Be concise.",
        max_output_tokens=500,
    )
    
    print(response.model_dump_json(indent=2)) 
    ```

# [C#](#tab/dotnet)

1. Install the Azure Identity client library:

    ```dotnetcli
    dotnet add package Azure.Identity
    dotnet add package OpenAI
    ```

1. Use the following code to configure the OpenAI client object in the project route, specify your deployment, and generate responses. 

    ```csharp
    using Azure.Identity;
    using OpenAI;
    using OpenAI.Responses;

    var deploymentName = "DeepSeek-V3.1"; // Replace with your deployment name, not the model ID 
    var project_endpoint = "https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME";

    // Get EntraID token for keyless auth
    var credential = new DefaultAzureCredential();
    var token = await credential.GetTokenAsync(
        new Azure.Core.TokenRequestContext(["https://ai.azure.com/.default"])
    );

    // Standard OpenAI client — no AzureOpenAI wrapper (no api-version needed with /v1 path)
    var baseUrl = project_endpoint.TrimEnd('/') + "/openai/v1";
    var client = new OpenAIClient(
        new ApiKeyCredential(token.Token),
        new OpenAIClientOptions { Endpoint = new Uri(baseUrl) });    

    var responseClient = client.GetResponsesClient(deploymentName);
    var result = await responseClient.CreateResponseAsync(new CreateResponseOptions(
        [ResponseItem.CreateUserMessageItem("What are the top 3 benefits of cloud computing? Be concise.")])
        { MaxOutputTokenCount = 500 }
    );
    Console.WriteLine($"Response: {result.Value.GetOutputText()}");
    Console.WriteLine($"Status:   {result.Value.Status}");
    Console.WriteLine($"Output tokens: {result.Value.Usage.OutputTokenCount}");
    
    ```

# [JavaScript](#tab/javascript)

1. Install the Azure Identity client library before you can use `DefaultAzureCredential`:

    ```bash
    npm install @azure/identity
    npm install openai
    ```

1. Use the following code to configure the OpenAI client object in the project route, specify your deployment, and generate responses.  

    ```javascript
    import OpenAI from "openai";
    import { DefaultAzureCredential } from "@azure/identity";
    
    async function getToken(): Promise<string> {
      const credential = new DefaultAzureCredential();
      const tokenResponse = await credential.getToken(
        "https://ai.azure.com/.default"
      );
      return tokenResponse.token;
    }

    async function main() {
        const projectEndpoint = "https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME";
        const deploymentName = "DeepSeek-V3.1"; // Replace with your deployment name, not the model ID 

        const baseURL = projectEndpoint.replace(/\/+$/, "") + "/openai/v1";
        const token = await getToken();

        const client = new OpenAI({
            baseURL,
            apiKey: token,
          });

        const response = await client.responses.create({
            model: deploymentName,
            input: "What are the top 3 benefits of cloud computing? Be concise.",
            max_output_tokens: 500,
          });
    
        console.log(`Response: ${response.output_text}`);
        console.log(`Status:   ${response.status}`);
        console.log(`Output tokens: ${response.usage?.output_tokens}`);
    }
    
    main();
    ```

# [Java](#tab/java)

Authentication with Microsoft Entra ID requires some initial setup. First, install the Azure Identity client library. For more options on how to install this library, see [Azure Identity client library for Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/identity/azure-identity/README.md#include-the-package).

1. Add the Azure Identity client library:

    ```xml
    <dependencies>
        <dependency>
            <groupId>com.openai</groupId>
            <artifactId>openai-java</artifactId>
            <version>4.22.0</version>
        </dependency>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-identity</artifactId>
            <version>1.15.4</version>
        </dependency>
    </dependencies>
    ```

    After setup, choose which type of credential from `azure.identity` to use. For example, use `DefaultAzureCredential` to authenticate the client. Authentication is easiest with `DefaultAzureCredential`, as it finds the best credential to use in its running environment.

1. Use the following code to configure the OpenAI client object in the project route, specify your deployment, and generate responses.  

    ```java
    import com.azure.core.credential.TokenRequestContext;
    import com.azure.identity.DefaultAzureCredentialBuilder;
    import com.openai.client.OpenAIClient;
    import com.openai.client.okhttp.OpenAIOkHttpClient;
    import com.openai.models.responses.ResponseCreateParams;
    
    public class Sample {
        public static void main(String[] args) {
            String endpoint = "https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME";
            String deploymentName = "DeepSeek-V3.1"; // Replace with your deployment name, not the model ID
            
            // Get EntraID token for keyless auth
            var credential = new DefaultAzureCredentialBuilder().build();
            var context = new TokenRequestContext().addScopes("https://ai.azure.com/.default");
            String token = credential.getToken(context).block().getToken();

            // Standard OpenAI client — no Azure wrapper
            // Java SDK uses /openai/v1 path (no api-version needed; SDK manages versioning internally)
            String baseUrl = endpoint.replaceAll("/+$", "") + "/openai/v1";
            OpenAIClient client = OpenAIOkHttpClient.builder()
                    .baseUrl(baseUrl)
                    .apiKey(token)
                    .build();

            var response = client.responses().create(
                    ResponseCreateParams.builder()
                            .model(deploymentName)
                            .input("What are the top 3 benefits of cloud computing? Be concise.")
                            .maxOutputTokens(500)
                            .build()
            );
            System.out.printf("Response: %s%n", getOutputText(response));
            System.out.printf("Status:   %s%n", response.status());
            response.usage().ifPresent(u ->
                    System.out.printf("Output tokens: %d%n", u.outputTokens()));
        }
    }
   ```

# [Go](#tab/go)

```go
package main

import (
    "context"
    "fmt"
    "os"
    "strings"

    "github.com/Azure/azure-sdk-for-go/sdk/azcore/policy"
    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/openai/openai-go/v3"
    "github.com/openai/openai-go/v3/option"
    "github.com/openai/openai-go/v3/responses"
)

func main() {
    projectEndpoint := "https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME"
    deploymentName := "DeepSeek-V3.1" // Replace with your deployment name, not the model ID

    ctx := context.Background()

    // Get EntraID token for keyless auth
    credential, err := azidentity.NewDefaultAzureCredential(nil)
    token, err := credential.GetToken(ctx, policy.TokenRequestOptions{
        Scopes: []string{"https://ai.azure.com/.default"},
    })

    // Standard OpenAI client — no Azure wrapper (no api-version needed with /v1 path)
    baseURL := strings.TrimRight(projectEndpoint, "/") + "/openai/v1"
    client := openai.NewClient(
        option.WithBaseURL(baseURL),
        option.WithAPIKey(token.Token),
    )

    resp, err := client.Responses.New(ctx, responses.ResponseNewParams{
        Model: deploymentName,
        Input: responses.ResponseNewParamsInputUnion{
            OfString: openai.String("What are the top 3 benefits of cloud computing? Be concise."),
        },
        MaxOutputTokens: openai.Int(500),
    })

    fmt.Printf("Response: %s\n", resp.OutputText())
    fmt.Printf("Status:   %s\n", resp.Status)
    fmt.Printf("Output tokens: %d\n", resp.Usage.OutputTokens)
}
```

---

The response includes the generated text along with model and usage metadata.

## Supported Foundry Models

A selection of Foundry Models are supported for use with the Responses API.

### View supported models in the Foundry portal

[!INCLUDE [agent-service-view-models-in-portal](../../agents/includes/agent-service-view-models-in-portal.md)]

### List of supported models

This section lists some of the Foundry Models that are supported for use with the Responses API. For the Azure OpenAI models that are supported, see [Available Azure OpenAI models](../../agents/concepts/model-region-support.md#available-models).
[!INCLUDE [agent-service-models-support-list](../../../foundry/agents/includes/agent-service-models-support-list.md)]

## Troubleshoot common errors

| Error | Cause | Resolution |
| --- | --- | --- |
| 401 Unauthorized | Invalid or expired credential | Verify your `DefaultAzureCredential` has the **Cognitive Services OpenAI User** role assigned on the resource. |
| 404 Not Found | Wrong endpoint or deployment name | Confirm your endpoint URL includes `/api/projects/YOUR_PROJECT_NAME` and the deployment name matches your Foundry portal. |
| 400 Model not supported | Model doesn't support Responses API | Check the [supported models list](#supported-foundry-models) and verify your deployment uses a compatible model. |

## Related content

- [Migrate from Azure AI Inference SDK to OpenAI SDK](../../how-to/model-inference-to-openai-migration.md)
- [Azure OpenAI supported programming languages](../../openai/supported-languages.md)
- [Switch between OpenAI and Azure OpenAI endpoints](/azure/developer/ai/how-to/switching-endpoints)
- [Model support for v1 Azure OpenAI API](../../openai/api-version-lifecycle.md#model-support)

