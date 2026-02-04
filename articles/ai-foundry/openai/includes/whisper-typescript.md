---
ms.topic: include
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 10/22/2024
ms.author: pafarley
author: PatrickFarley
---

[Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- [LTS versions of Node.js](https://github.com/nodejs/release#release-schedule)
- [TypeScript](https://www.typescriptlang.org/download/)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI resource with a speech to text model deployed in a [supported region](../../foundry-models/concepts/models-sold-directly-by-azure.md?tabs=standard-audio). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.
## Set up

1. Create a new folder `whisper-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir whisper-quickstart && cd whisper-quickstart
    ```
    
1. Create the `package.json` with the following command:

    ```shell
    npm init -y
    ```

1. Update the `package.json` to ECMAScript with the following command: 

    ```shell
    npm pkg set type=module
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

## Create a sample application

#### [Microsoft Entra ID](#tab/typescript-keyless)

1. Create the `index.ts` file with the following code:
    
    ```typescript
    import { createReadStream } from "fs";
    import { AzureOpenAI } from "openai";
    import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

    // You will need to set these environment variables or edit the following values
    const audioFilePath = "<audio file path>";
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-08-01-preview";
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "whisper";

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
    
    export async function main() {
      console.log("== Transcribe Audio Sample ==");
    
      const client = getClient();
      const result = await client.audio.transcriptions.create({
        model: "",
        file: createReadStream(audioFilePath),
      });
    
      console.log(`Transcription: ${result.text}`);
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    ```

1. Create the `tsconfig.json` file to transpile the TypeScript code and copy the following code for ECMAScript.

    ```json
    {
        "compilerOptions": {
          "module": "NodeNext",
          "target": "ES2022", // Supports top-level await
          "moduleResolution": "NodeNext",
          "skipLibCheck": true, // Avoid type errors from node_modules
          "strict": true // Enable strict type-checking options
        },
        "include": ["*.ts"]
    }
    ```

1. Transpile from TypeScript to JavaScript.

    ```shell
    tsc
    ```
    
1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the code with the following command:

    ```shell
    node index.js
    ```


#### [API key](#tab/typescript-key)

1. Create the `index.ts` file with the following code:
    
    ```typescript
    import { createReadStream } from "fs";
    import { AzureOpenAI } from "openai";
    
    // You will need to set these environment variables or edit the following values
    const audioFilePath = "<audio file path>";
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const apiKey = process.env.AZURE_OPENAI_API_KEY || "Your API key";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-08-01-preview";
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "whisper";
    
    function getClient(): AzureOpenAI {
      return new AzureOpenAI({
        endpoint,
        apiKey,
        apiVersion,
        deployment: deploymentName,
      });
    }
    
    export async function main() {
      console.log("== Transcribe Audio Sample ==");
    
      const client = getClient();
      const result = await client.audio.transcriptions.create({
        model: "",
        file: createReadStream(audioFilePath),
      });
    
      console.log(`Transcription: ${result.text}`);
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    ```

1. Create the `tsconfig.json` file to transpile the TypeScript code and copy the following code for ECMAScript.

    ```json
    {
        "compilerOptions": {
          "module": "NodeNext",
          "target": "ES2022", // Supports top-level await
          "moduleResolution": "NodeNext",
          "skipLibCheck": true, // Avoid type errors from node_modules
          "strict": true // Enable strict type-checking options
        },
        "include": ["*.ts"]
    }
    ```

1. Transpile from TypeScript to JavaScript.

    ```shell
    tsc
    ```
    
1. Run the code with the following command:

    ```shell
    node index.js
    ```

---

You can get sample audio files, such as *wikipediaOcelot.wav*, from the [Azure Speech in Foundry Tools SDK repository at GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/sampledata/audiofiles).

[!INCLUDE [Azure Key Vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

## Output

```json
{"text":"The ocelot, Lepardus paradalis, is a small wild cat native to the southwestern United States, Mexico, and Central and South America. This medium-sized cat is characterized by solid black spots and streaks on its coat, round ears, and white neck and undersides. It weighs between 8 and 15.5 kilograms, 18 and 34 pounds, and reaches 40 to 50 centimeters 16 to 20 inches at the shoulders. It was first described by Carl Linnaeus in 1758. Two subspecies are recognized, L. p. paradalis and L. p. mitis. Typically active during twilight and at night, the ocelot tends to be solitary and territorial. It is efficient at climbing, leaping, and swimming. It preys on small terrestrial mammals such as armadillo, opossum, and lagomorphs."}
```
