---
title: 'Quickstart: Use Azure OpenAI Service with the JavaScript SDK and the completions API'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the JavaScript SDK. 
#services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
author: mrbullwinkle
ms.author: mbullwin
ms.date: 10/22/2024
---

[Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

> [!NOTE]
> This article has been updated to use the [latest OpenAI npm package](https://www.npmjs.com/package/openai) which now fully supports Azure OpenAI. If you are looking for code examples for the legacy Azure OpenAI JavaScript SDK they are currently still [available in this repo](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples/v2-beta/javascript).

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- [LTS versions of Node.js](https://github.com/nodejs/release#release-schedule)
- [TypeScript](https://www.typescriptlang.org/download/)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI Service resource with the `gpt-35-turbo-instruct` model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).

> [!div class="nextstepaction"]
> [I ran into an issue with the prerequisites.](https://microsoft.qualtrics.com/jfe/form/SV_0Cl5zkG3CnDjq6O?PLanguage=JAVASCRIPT&Pillar=AOAI&&Product=gpt&Page=quickstart&Section=Prerequisites)

## Set up

[!INCLUDE [get-key-endpoint](get-key-endpoint.md)]

[!INCLUDE [environment-variables](environment-variables.md)]

In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it.

## Install the client library

Install the required packages for JavaScript with npm from within the context of your new directory:

```console
npm install openai @azure/identity
```

Your app's _package.json_ file will be updated with the dependencies.

> [!div class="nextstepaction"]
> [I ran into an issue with the setup.](https://microsoft.qualtrics.com/jfe/form/SV_0Cl5zkG3CnDjq6O?PLanguage=JAVASCRIPT&Pillar=AOAI&&Product=gpt&Page=quickstart&Section=Set-up-the-environment)

## Create a sample application

Open a command prompt where you created the new project, and create a new file named Completion.ts. Copy the following code into the Completion.ts file.

## [Microsoft Entra ID](#tab/typescript-keyless)

```typescript
import { 
  DefaultAzureCredential, 
  getBearerTokenProvider 
} from "@azure/identity";
import { AzureOpenAI } from "openai";
import { type Completion } from "openai/resources/index";

// You will need to set these environment variables or edit the following values
const endpoint = process.env["AZURE_OPENAI_ENDPOINT"] || "<endpoint>";

// Required Azure OpenAI deployment name and API version
const apiVersion = "2024-08-01-preview";
const deploymentName = "gpt-35-turbo-instruct";

// keyless authentication    
const credential = new DefaultAzureCredential();
const scope = "https://cognitiveservices.azure.com/.default";
const azureADTokenProvider = getBearerTokenProvider(credential, scope);

// Chat prompt and max tokens
const prompt = ["When was Microsoft founded?"];
const maxTokens = 128;

function getClient(): AzureOpenAI {
  return new AzureOpenAI({
    endpoint,
    azureADTokenProvider,
    apiVersion,
    deployment: deploymentName,
  });
}
async function getCompletion(
  client: AzureOpenAI,
  prompt: string[],
  max_tokens: number
): Promise<Completion> {
  return client.completions.create({
    prompt,
    model: "",
    max_tokens,
  });
}
async function printChoices(completion: Completion): Promise<void> {
  for (const choice of completion.choices) {
    console.log(choice.text);
  }
}
export async function main() {
  console.log("== Get completions Sample ==");

  const client = getClient();
  const completion = await getCompletion(client, prompt, maxTokens);
  await printChoices(completion);
}

main().catch((err) => {
  console.error("Error occurred:", err);
});
```

Build the script with the following command:

```cmd
tsc
```

Run the script with the following command:

```cmd
node.exe Completion.js
```

## [API key](#tab/typescript-key)

```typescript
import { AzureOpenAI } from "openai";
import { type Completion } from "openai/resources/index";

// You will need to set these environment variables or edit the following values
const endpoint = process.env["AZURE_OPENAI_ENDPOINT"] || "<endpoint>";
const apiKey = process.env["AZURE_OPENAI_API_KEY"] || "<api key>";

// Required Azure OpenAI deployment name and API version
const apiVersion = "2024-08-01-preview";
const deploymentName = "gpt-35-turbo-instruct";

// Chat prompt and max tokens
const prompt = ["When was Microsoft founded?"];
const maxTokens = 128;

function getClient(): AzureOpenAI {
  return new AzureOpenAI({
    endpoint,
    apiKey,
    apiVersion,
    deployment: deploymentName,
  });
}
async function getCompletion(
  client: AzureOpenAI,
  prompt: string[],
  max_tokens: number
): Promise<Completion> {
  return client.completions.create({
    prompt,
    model: "",
    max_tokens,
  });
}
async function printChoices(completion: Completion): Promise<void> {
  for (const choice of completion.choices) {
    console.log(choice.text);
  }
}
export async function main() {
  console.log("== Get completions Sample ==");

  const client = getClient();
  const completion = await getCompletion(client, prompt, maxTokens);
  await printChoices(completion);
}

main().catch((err) => {
  console.error("Error occurred:", err);
});
```

Build the script with the following command:

```cmd
tsc
```

Run the script with the following command:

```cmd
node.exe Completion.js
```

---

## Output

```output
== Get completions Sample ==

Microsoft was founded on April 4, 1975.
```

> [!NOTE]
> If your receive the error: *Error occurred: OpenAIError: The `apiKey` and `azureADTokenProvider` arguments are mutually exclusive; only one can be passed at a time.* You may need to remove a pre-existing environment variable for the API key from your system. Even though the Microsoft Entra ID code sample is not explicitly referencing the API key environment variable, if one is present on the system executing this sample, this error will still be generated.

> [!div class="nextstepaction"]
> [I ran into an issue when running the code sample.](https://microsoft.qualtrics.com/jfe/form/SV_0Cl5zkG3CnDjq6O?PLanguage=JAVASCRIPT&Pillar=AOAI&&Product=gpt&Page=quickstart&Section=Create-application)

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* [Azure OpenAI Overview](../overview.md)
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://aka.ms/AOAICodeSamples)
