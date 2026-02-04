---
ms.topic: include
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 2/1/2024
ms.author: pafarley
author: PatrickFarley
---

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource with a speech to text model deployed in a [supported region](../../foundry-models/concepts/models-sold-directly-by-azure.md?tabs=standard-audio). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).
- Be sure that you are assigned at least the [Cognitive Services Contributor](../how-to/role-based-access-control.md#cognitive-services-contributor) role for the Azure OpenAI resource.
- A sample audio file. You can get sample audio, such as *wikipediaOcelot.wav*, from the [Azure Speech in Foundry Tools SDK repository at GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/sampledata/audiofiles).

## Setup

### Retrieve key and endpoint

To successfully make a call against Azure OpenAI, you need an *endpoint* and a *key*.

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_OPENAI_ENDPOINT`               | The service endpoint can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. Alternatively, you can find the endpoint via the **Deployments** page in Microsoft Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`.|
| `AZURE_OPENAI_API_KEY` | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|

Go to your resource in the Azure portal. The **Endpoint and Keys** can be found in the **Resource Management** section. Copy your endpoint and access key as you need both for authenticating your API calls. You can use either `KEY1` or `KEY2`. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot of the overview UI for an Azure OpenAI resource in the Azure portal with the endpoint & access keys location circled in red." lightbox="../media/quickstarts/endpoint.png":::

### Environment variables

Create and assign persistent environment variables for your key and endpoint.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

# [Command Line](#tab/command-line)

```CMD
setx AZURE_OPENAI_API_KEY "REPLACE_WITH_YOUR_KEY_VALUE_HERE" 
```

```CMD
setx AZURE_OPENAI_ENDPOINT "REPLACE_WITH_YOUR_ENDPOINT_HERE" 
```

# [PowerShell](#tab/powershell)

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_API_KEY', 'REPLACE_WITH_YOUR_KEY_VALUE_HERE', 'User')
```

```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_OPENAI_ENDPOINT', 'REPLACE_WITH_YOUR_ENDPOINT_HERE', 'User')
```

# [Bash](#tab/bash)

```Bash
echo export AZURE_OPENAI_API_KEY="REPLACE_WITH_YOUR_KEY_VALUE_HERE" >> /etc/environment && source /etc/environment
```

```Bash
echo export AZURE_OPENAI_ENDPOINT="REPLACE_WITH_YOUR_ENDPOINT_HERE" >> /etc/environment && source /etc/environment
```
---

## Create a REST API request and response

In a bash shell, run the following command. You need to replace `YourDeploymentName` with the deployment name you chose when you deployed the Whisper model. The deployment name isn't necessarily the same as the model name. Entering the model name results in an error unless you chose a deployment name that's identical to the underlying model name.

```bash
curl $AZURE_OPENAI_ENDPOINT/openai/deployments/YourDeploymentName/audio/transcriptions?api-version=2024-02-01 \
 -H "api-key: $AZURE_OPENAI_API_KEY" \
 -H "Content-Type: multipart/form-data" \
 -F file="@./wikipediaOcelot.wav"
```

The first line of the preceding command with an example endpoint would appear as follows:

```bash
curl https://aoai-docs.openai.azure.com/openai/deployments/{YourDeploymentName}/audio/transcriptions?api-version=2024-02-01 \
```


> [!IMPORTANT]
> For production, store and access your credentials using a secure method, such as [Azure Key Vault](/azure/key-vault/general/overview). For more information, see [credential security](../../../ai-services/security-features.md).

## Output

```bash
{"text":"The ocelot, Lepardus paradalis, is a small wild cat native to the southwestern United States, Mexico, and Central and South America. This medium-sized cat is characterized by solid black spots and streaks on its coat, round ears, and white neck and undersides. It weighs between 8 and 15.5 kilograms, 18 and 34 pounds, and reaches 40 to 50 centimeters 16 to 20 inches at the shoulders. It was first described by Carl Linnaeus in 1758. Two subspecies are recognized, L. p. paradalis and L. p. mitis. Typically active during twilight and at night, the ocelot tends to be solitary and territorial. It is efficient at climbing, leaping, and swimming. It preys on small terrestrial mammals such as armadillo, opossum, and lagomorphs."}
```
