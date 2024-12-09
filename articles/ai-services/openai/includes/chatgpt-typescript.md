---
title: 'Quickstart: Use Azure OpenAI Service with the JavaScript SDK'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first chat completions call with the JavaScript SDK. 
#services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
author: mrbullwinkle
ms.author: mbullwin
ms.date: 10/22
---

[Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

> [!NOTE]
> This article has been updated to use the [latest OpenAI npm package](https://www.npmjs.com/package/openai) which now fully supports Azure OpenAI. If you are looking for code examples for the legacy Azure OpenAI JavaScript SDK they are currently still [available in this repo](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples/v2-beta/javascript).

## Prerequisites


- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- [LTS versions of Node.js](https://github.com/nodejs/release#release-schedule)
- [TypeScript](https://www.typescriptlang.org/download/)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI Service resource with a `gpt-35-turbo` or `gpt-4` series models deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).



## Set up

[!INCLUDE [get-key-endpoint](get-key-endpoint.md)]

[!INCLUDE [environment-variables](environment-variables.md)]

## Create a Node application

In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it. 

## Install the client library

Install the required packages for JavaScript with npm from within the context of your new directory:

```console
npm install openai @azure/identity
```

Your app's _package.json_ file will be updated with the dependencies.


## Create a sample application

Open a command prompt where you want the new project, and create a new file named ChatCompletion.ts. Copy the following code into the ChatCompletion.ts file.

## [Microsoft Entra ID](#tab/typescript-keyless)

```typescript
import { AzureOpenAI } from "openai";
import { 
  DefaultAzureCredential, 
  getBearerTokenProvider 
} from "@azure/identity";
import type {
  ChatCompletion,
  ChatCompletionCreateParamsNonStreaming,
} from "openai/resources/index";

// You will need to set these environment variables or edit the following values
const endpoint = process.env["AZURE_OPENAI_ENDPOINT"] || "<endpoint>";

// Required Azure OpenAI deployment name and API version
const apiVersion = "2024-08-01-preview";
const deploymentName = "gpt-4o-mini"; //This must match your deployment name.

// keyless authentication    
const credential = new DefaultAzureCredential();
const scope = "https://cognitiveservices.azure.com/.default";
const azureADTokenProvider = getBearerTokenProvider(credential, scope);

function getClient(): AzureOpenAI {
  return new AzureOpenAI({
    endpoint,
    azureADTokenProvider,
    apiVersion,
    deployment: deploymentName,
  });
}

function createMessages(): ChatCompletionCreateParamsNonStreaming {
  return {
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      {
        role: "user",
        content: "Does Azure OpenAI support customer managed keys?",
      },
      {
        role: "assistant",
        content: "Yes, customer managed keys are supported by Azure OpenAI?",
      },
      { role: "user", content: "Do other Azure AI services support this too?" },
    ],
    model: "",
  };
}
async function printChoices(completion: ChatCompletion): Promise<void> {
  for (const choice of completion.choices) {
    console.log(choice.message);
  }
}
export async function main() {
  const client = getClient();
  const messages = createMessages();
  const result = await client.chat.completions.create(messages);
  await printChoices(result);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

Build the script with the following command:

```cmd
tsc
```

Run the script with the following command:

```cmd
node.exe ChatCompletion.js
```

## [API Key](#tab/typescript-key)

```typescript
import { AzureOpenAI } from "openai";
import type {
  ChatCompletion,
  ChatCompletionCreateParamsNonStreaming,
} from "openai/resources/index";

// You will need to set these environment variables or edit the following values
const endpoint = process.env["AZURE_OPENAI_ENDPOINT"] || "<endpoint>";
const apiKey = process.env["AZURE_OPENAI_API_KEY"] || "<api key>";

// Required Azure OpenAI deployment name and API version
const apiVersion = "2024-08-01-preview";
const deploymentName = "gpt-4o-mini"; //This must match your deployment name.

function getClient(): AzureOpenAI {
  return new AzureOpenAI({
    endpoint,
    apiKey,
    apiVersion,
    deployment: deploymentName,
  });
}

function createMessages(): ChatCompletionCreateParamsNonStreaming {
  return {
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      {
        role: "user",
        content: "Does Azure OpenAI support customer managed keys?",
      },
      {
        role: "assistant",
        content: "Yes, customer managed keys are supported by Azure OpenAI?",
      },
      { role: "user", content: "Do other Azure AI services support this too?" },
    ],
    model: "",
  };
}
async function printChoices(completion: ChatCompletion): Promise<void> {
  for (const choice of completion.choices) {
    console.log(choice.message);
  }
}
export async function main() {
  const client = getClient();
  const messages = createMessages();
  const result = await client.chat.completions.create(messages);
  await printChoices(result);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

Build the script with the following command:

```cmd
tsc
```

Run the script with the following command:

```cmd
node.exe ChatCompletion.js
```

---

## Output

```output
== Chat Completions Sample ==
{
  content: 'Yes, several other Azure AI services also support customer managed keys for enhanced security and control over encryption keys.',
  role: 'assistant'
}
```

---

> [!NOTE]
> If your receive the error: *Error occurred: OpenAIError: The `apiKey` and `azureADTokenProvider` arguments are mutually exclusive; only one can be passed at a time.* You may need to remove a pre-existing environment variable for the API key from your system. Even though the Microsoft Entra ID code sample is not explicitly referencing the API key environment variable, if one is present on the system executing this sample, this error will still be generated.


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* [Azure OpenAI Overview](../overview.md)
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://aka.ms/AOAICodeSamples)
