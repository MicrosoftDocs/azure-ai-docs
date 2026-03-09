---
title: Generate responses with a non-AOAI Foundry Model
description: Include file
author: msakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 03/09/2026
ms.custom: include
---

> [!TIP]
> When you deploy a model in the Foundry portal, you assign it a deployment name. Use this deployment name (not the model catalog ID) in the `model` parameter of your API calls.

> [!NOTE]
> Use keyless authentication with **Microsoft Entra ID**. To learn more about keyless authentication, see [What is Microsoft Entra authentication?](/entra/identity/authentication/overview-authentication) and [DefaultAzureCredential](/azure/developer/python/sdk/authentication/overview#defaultazurecredential).

# [Python](#tab/python)

1. Install libraries, including the Azure Identity client library:

    ```bash
    pip install azure-identity
    pip install -U openai
    ```

1. Use the following code to configure the OpenAI client object in the project route, specify your deployment, and generate responses. 
   
    ```python
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    from openai import OpenAI
    
    project_endpoint = "https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME"
    # Build the base URL: project_endpoint + /openai/v1 (no api-version needed)
    base_url = project_endpoint.rstrip("/") + "/openai/v1"

    # get_bearer_token_provider returns a callable; call it to get automatic refresh of the token string
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
    client = OpenAI(
        base_url=base_url,
        api_key=token_provider(),
    )   
   
    response = client.responses.create(
        model="DeepSeek-R1-0528", # Replace with your deployment name, not the model ID 
        input="What are the top 3 benefits of cloud computing? Be concise.",
        max_output_tokens=500,
    )
    
    print(f"Response: {response.output_text}")
    print(f"Status:   {response.status}")
    print(f"Output tokens: {response.usage.output_tokens}") 
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

    var deploymentName = "DeepSeek-R1-0528"; // Replace with your deployment name, not the model ID 
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

    // GetResponsesClient takes no parameter; model goes in CreateResponseOptions
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
        const deploymentName = "DeepSeek-R1-0528"; // Replace with your deployment name, not the model ID 

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

    After setup, choose which type of credential from `azure.identity` to use. For example, use `DefaultAzureCredential` to authenticate the client. `DefaultAzureCredential` is the easiest option because it finds the best credential to use in its running environment.

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
            String deploymentName = "DeepSeek-R1-0528"; // Replace with your deployment name, not the model ID
            
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
            System.out.printf("Response: %s%n", response.outputText());
            System.out.printf("Status:   %s%n", response.status());
            response.usage().ifPresent(u ->
                    System.out.printf("Output tokens: %d%n", u.outputTokens()));
        }
    }
   ```

# [Go](#tab/go)

1. Before running the sample, install the required Go modules.

    ```bash
    go get github.com/Azure/azure-sdk-for-go/sdk/azcore v1.21.0
    go get github.com/Azure/azure-sdk-for-go/sdk/azidentity v1.13.1
    go get github.com/openai/openai-go/v3 v3.22.0
    ```

1. Use the following code to configure the OpenAI client object in the project route, specify your deployment, and generate responses.

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
        deploymentName := "DeepSeek-R1-0528" // Replace with your deployment name, not the model ID
    
        ctx := context.Background()
    
        // Get EntraID token for keyless auth
        credential, err := azidentity.NewDefaultAzureCredential(nil)
        if err != nil {
            fmt.Fprintf(os.Stderr, "Failed to create credential: %v\n", err)
            os.Exit(1)
        }
        token, err := credential.GetToken(ctx, policy.TokenRequestOptions{
            Scopes: []string{"https://ai.azure.com/.default"},
        })
        if err != nil {
            fmt.Fprintf(os.Stderr, "Failed to get token: %v\n", err)
            os.Exit(1)
        }
    
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
        if err != nil {
            fmt.Fprintf(os.Stderr, "API error: %v\n", err)
            os.Exit(1)
        }
    
        fmt.Printf("Response: %s\n", resp.OutputText())
        fmt.Printf("Status:   %s\n", resp.Status)
        fmt.Printf("Output tokens: %d\n", resp.Usage.OutputTokens)
    }
    ```

---

The response includes the generated text along with model and usage metadata.