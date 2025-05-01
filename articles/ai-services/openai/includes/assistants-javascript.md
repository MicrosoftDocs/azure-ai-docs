---
title: 'Quickstart: Use the Azure OpenAI Service via the JavaScript SDK'
titleSuffix: Azure OpenAI Service
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the JavaScript SDK. 
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-openai
ms.topic: include
ms.date: 10/28/2024
ms.custom: passwordless-ts, devex-track-js
---

<a href="/javascript/api/@azure/openai-assistants" target="_blank">Reference documentation</a> | <a href="https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai" target="_blank">Library source code</a> | <a href="https://www.npmjs.com/package/@azure/openai-assistants" target="_blank">Package (npm)</a> |

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>
- <a href="https://nodejs.org/" target="_blank">Node.js LTS or ESM support.</a>
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI. 
- An Azure OpenAI resource with a [compatible model in a supported region](../concepts/models.md#assistants-preview).
- We recommend reviewing the [Responsible AI transparency note](/legal/cognitive-services/openai/transparency-note?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=text) and other [Responsible AI resources](/legal/cognitive-services/openai/overview?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext) to familiarize yourself with the capabilities and limitations of the Azure OpenAI Service.
- An Azure OpenAI resource with the `gpt-4 (1106-preview)` model deployed was used testing this example. 

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up
 
1. Create a new folder `assistants-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir assistants-quickstart && cd assistants-quickstart
    ```
    

1. Create the `package.json` with the following command:

    ```shell
    npm init -y
    ```   

1. Install the OpenAI client library for JavaScript with:

    ```console
    npm install openai
    ```

1. For the **recommended** passwordless authentication:

    ```console
    npm install @azure/identity
    ```


## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

> [!CAUTION]
> To use the recommended keyless authentication with the SDK, make sure that the `AZURE_OPENAI_API_KEY` environment variable isn't set. 


## Create an assistant

In our code we're going to specify the following values:

| **Name** | **Description** |
|:---|:---|
| **Assistant name** | Your deployment name that is associated with a specific model. |
| **Instructions** | Instructions are similar to system messages this is where you give the model guidance about how it should behave and any context it should reference when generating a response. You can describe the assistant's personality, tell it what it should and shouldn't answer, and tell it how to format responses. You can also provide examples of the steps it should take when answering responses. |
| **Model** | This is the deployment name. |
| **Code interpreter** | Code interpreter provides access to a sandboxed Python environment that can be used to allow the model to test and execute code. |

### Tools

An individual assistant can access up to 128 tools including `code interpreter`, and any custom tools you create via [functions](../how-to/assistant-functions.md).
    
## Create a new JavaScript application

#### [Microsoft Entra ID](#tab/keyless)

1. Create the `index.js` file with the following code:

    ```javascript
    const { AzureOpenAI } = require("openai");
    const {
      DefaultAzureCredential,
      getBearerTokenProvider,
    } = require("@azure/identity");
    
    // Get environment variables
    const azureOpenAIEndpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const azureOpenAIDeployment = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "Your deployment name";
    const azureOpenAIVersion = process.env.OPENAI_API_VERSION || "A supported API version";
    
    // Check env variables
    if (!azureOpenAIEndpoint || !azureOpenAIDeployment || !azureOpenAIVersion) {
      throw new Error(
        "You need to set the endpoint, deployment name, and API version."
      );
    }
    
    // Get Azure SDK client
    const getClient = () => {
      const credential = new DefaultAzureCredential();
      const scope = "https://cognitiveservices.azure.com/.default";
      const azureADTokenProvider = getBearerTokenProvider(credential, scope);

      const assistantsClient = new AzureOpenAI({
        endpoint: azureOpenAIEndpoint,
        apiVersion: azureOpenAIVersion,
        azureADTokenProvider,
      });
      return assistantsClient;
    };
    
    const assistantsClient = getClient();
    
    const options = {
      model: azureOpenAIDeployment, // Deployment name seen in Azure AI Foundry portal
      name: "Math Tutor",
      instructions:
        "You are a personal math tutor. Write and run JavaScript code to answer math questions.",
      tools: [{ type: "code_interpreter" }],
    };
    const role = "user";
    const message = "I need to solve the equation `3x + 11 = 14`. Can you help me?";
    
    // Create an assistant
    const assistantResponse = await assistantsClient.beta.assistants.create(
      options
    );
    console.log(`Assistant created: ${JSON.stringify(assistantResponse)}`);
    
    // Create a thread
    const assistantThread = await assistantsClient.beta.threads.create({});
    console.log(`Thread created: ${JSON.stringify(assistantThread)}`);
    
    // Add a user question to the thread
    const threadResponse = await assistantsClient.beta.threads.messages.create(
      assistantThread.id,
      {
        role,
        content: message,
      }
    );
    console.log(`Message created:  ${JSON.stringify(threadResponse)}`);
    
    // Run the thread and poll it until it is in a terminal state
    const runResponse = await assistantsClient.beta.threads.runs.createAndPoll(
      assistantThread.id,
      {
        assistant_id: assistantResponse.id,
      },
      { pollIntervalMs: 500 }
    );
    console.log(`Run created:  ${JSON.stringify(runResponse)}`);
    
    // Get the messages
    const runMessages = await assistantsClient.beta.threads.messages.list(
      assistantThread.id
    );
    for await (const runMessageDatum of runMessages) {
      for (const item of runMessageDatum.content) {
        // types are: "image_file" or "text"
        if (item.type === "text") {
          console.log(`Message content: ${JSON.stringify(item.text?.value)}`);
        }
      }
    }
    ```

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the JavaScript file.

    ```shell
    node index.js
    ```

#### [API key](#tab/api-key)

1. Create the `index.js` file with the following code:

    ```javascript
    const { AzureOpenAI } = require("openai");
    
    // Get environment variables
    const azureOpenAIKey = process.env.AZURE_OPENAI_KEY || "Your API key";
    const azureOpenAIEndpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const azureOpenAIDeployment = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "Your deployment name";
    const azureOpenAIVersion = process.env.OPENAI_API_VERSION || "A supported API version";
    
    // Check env variables
    if (!azureOpenAIKey || !azureOpenAIEndpoint || !azureOpenAIDeployment || !azureOpenAIVersion) {
      throw new Error(
        "You need to set the endpoint, deployment name, and API version."
      );
    }
    
    // Get Azure SDK client
    const getClient = () => {
      const assistantsClient = new AzureOpenAI({
        endpoint: azureOpenAIEndpoint,
        apiVersion: azureOpenAIVersion,
        apiKey: azureOpenAIKey,
      });
      return assistantsClient;
    };
    
    const assistantsClient = getClient();
    
    const options = {
      model: azureOpenAIDeployment, // Deployment name seen in Azure AI Foundry portal
      name: "Math Tutor",
      instructions:
        "You are a personal math tutor. Write and run JavaScript code to answer math questions.",
      tools: [{ type: "code_interpreter" }],
    };
    const role = "user";
    const message = "I need to solve the equation `3x + 11 = 14`. Can you help me?";
    
    // Create an assistant
    const assistantResponse = await assistantsClient.beta.assistants.create(
      options
    );
    console.log(`Assistant created: ${JSON.stringify(assistantResponse)}`);
    
    // Create a thread
    const assistantThread = await assistantsClient.beta.threads.create({});
    console.log(`Thread created: ${JSON.stringify(assistantThread)}`);
    
    // Add a user question to the thread
    const threadResponse = await assistantsClient.beta.threads.messages.create(
      assistantThread.id,
      {
        role,
        content: message,
      }
    );
    console.log(`Message created:  ${JSON.stringify(threadResponse)}`);
    
    // Run the thread and poll it until it is in a terminal state
    const runResponse = await assistantsClient.beta.threads.runs.createAndPoll(
      assistantThread.id,
      {
        assistant_id: assistantResponse.id,
      },
      { pollIntervalMs: 500 }
    );
    console.log(`Run created:  ${JSON.stringify(runResponse)}`);
    
    // Get the messages
    const runMessages = await assistantsClient.beta.threads.messages.list(
      assistantThread.id
    );
    for await (const runMessageDatum of runMessages) {
      for (const item of runMessageDatum.content) {
        // types are: "image_file" or "text"
        if (item.type === "text") {
          console.log(`Message content: ${JSON.stringify(item.text?.value)}`);
        }
      }
    }
    ```

1. Run the JavaScript file.

    ```shell
    node index.js
    ```

---

## Output

```console
Assistant created: {"id":"asst_zXaZ5usTjdD0JGcNViJM2M6N","createdAt":"2024-04-08T19:26:38.000Z","name":"Math Tutor","description":null,"model":"daisy","instructions":"You are a personal math tutor. Write and run JavaScript code to answer math questions.","tools":[{"type":"code_interpreter"}],"fileIds":[],"metadata":{}}
Thread created: {"id":"thread_KJuyrB7hynun4rvxWdfKLIqy","createdAt":"2024-04-08T19:26:38.000Z","metadata":{}}
Message created:  {"id":"msg_o0VkXnQj3juOXXRCnlZ686ff","createdAt":"2024-04-08T19:26:38.000Z","threadId":"thread_KJuyrB7hynun4rvxWdfKLIqy","role":"user","content":[{"type":"text","text":{"value":"I need to solve the equation `3x + 11 = 14`. Can you help me?","annotations":[]},"imageFile":{}}],"assistantId":null,"runId":null,"fileIds":[],"metadata":{}}
Created run
Run created:  {"id":"run_P8CvlouB8V9ZWxYiiVdL0FND","object":"thread.run","status":"queued","model":"daisy","instructions":"You are a personal math tutor. Write and run JavaScript code to answer math questions.","tools":[{"type":"code_interpreter"}],"metadata":{},"usage":null,"assistantId":"asst_zXaZ5usTjdD0JGcNViJM2M6N","threadId":"thread_KJuyrB7hynun4rvxWdfKLIqy","fileIds":[],"createdAt":"2024-04-08T19:26:39.000Z","expiresAt":"2024-04-08T19:36:39.000Z","startedAt":null,"completedAt":null,"cancelledAt":null,"failedAt":null}
Message content: "The solution to the equation \\(3x + 11 = 14\\) is \\(x = 1\\)."
Message content: "Yes, of course! To solve the equation \\( 3x + 11 = 14 \\), we can follow these steps:\n\n1. Subtract 11 from both sides of the equation to isolate the term with x.\n2. Then, divide by 3 to find the value of x.\n\nLet me calculate that for you."
Message content: "I need to solve the equation `3x + 11 = 14`. Can you help me?"
```

It's important to remember that while the code interpreter gives the model the capability to respond to more complex queries by converting the questions into code and running that code iteratively in JavaScript until it reaches a solution, you still need to validate the response to confirm that the model correctly translated your question into a valid representation in code.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Sample code

* [Quickstart sample code](https://github.com/Azure-Samples/azure-typescript-e2e-apps/tree/main/quickstarts/azure-openai-assistants)

## See also

* Learn more about how to use Assistants with our [How-to guide on Assistants](../how-to/assistant.md).
* [Azure OpenAI Assistants API samples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/Assistants)

