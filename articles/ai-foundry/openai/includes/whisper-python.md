---
services: ai-services
author: mrbullwinkle
ms.author: mbullwin
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 11/21/2025
ai-usage: ai-assisted
---

## Prerequisites

- An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource with a speech to text model deployed in a [supported region](../../foundry-models/concepts/models-sold-directly-by-azure.md?tabs=standard-audio). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).
- [Python 3.8 or later](https://www.python.org)
- The [Azure CLI](/cli/azure/install-azure-cli).
- A sample audio file. You can get sample audio, such as *wikipediaOcelot.wav*, from the [Azure Speech in Foundry Tools SDK repository at GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/sampledata/audiofiles).

## Setup

### Retrieve key and endpoint

To successfully make a call against Azure OpenAI, you need an *endpoint* and a *key*.

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_OPENAI_ENDPOINT`               | The service endpoint can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. Alternatively, you can find the endpoint via the **Deployments** page in Microsoft Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`.|
| `AZURE_OPENAI_API_KEY` | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|

Go to your resource in the Azure portal. The **Endpoint and Keys** can be found in the **Resource Management** section. Copy your endpoint and access key as you'll need both for authenticating your API calls. You can use either `KEY1` or `KEY2`. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

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

> [!IMPORTANT]
> **Passwordless authentication is recommended**
>
> For passwordless authentication, you need to:
> 
> 1. Use the `azure-identity` package (`pip install azure-identity`).
> 1. Assign the `Cognitive Services User` role to your user account. This can be done in the Azure portal under **Access control (IAM)** > **Add role assignment**.
> 1. Sign in with the Azure CLI such as `az login`.


## Create a Python environment

Create a new directory for your project and navigate to it from a terminal or command prompt.

```Bash
mkdir whisper-quickstart; cd whisper-quickstart
```

Create and activate a virtual environment for this project.

# [Windows](#tab/windows)

```powershell
python -m venv .venv
.venv\Scripts\activate
```

# [macOS/Linux](#tab/unix)

```Bash
python3 -m venv .venv
source .venv/bin/activate
```

---

Install the OpenAI Python client library with:

# [OpenAI Python 1.x](#tab/python-new)

```console
pip install openai
```

# [OpenAI Python 0.28.1](#tab/python)

[!INCLUDE [Deprecation](../includes/deprecation.md)]

```console
pip install openai==0.28.1
```

---

## Create the Python app

1. Create a new Python file called *quickstart.py*. Then open it up in your preferred editor or IDE.

1. Replace the contents of *quickstart.py* with the following code. Modify the code to add your deployment name:

# [OpenAI Python 1.x](#tab/python-new)

```python
    import os
    from openai import AzureOpenAI
        
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version="2024-02-01",
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
    deployment_id = "YOUR-DEPLOYMENT-NAME-HERE" #This will correspond to the custom name you chose for your deployment when you deployed a model."
    audio_test_file = "./wikipediaOcelot.wav"
    
    result = client.audio.transcriptions.create(
        file=open(audio_test_file, "rb"),            
        model=deployment_id
    )
    
    print(result)
```

# [OpenAI Python 0.28.1](#tab/python)

```python
    import openai
    import time
    import os
    
    openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    openai.api_type = "azure"
    openai.api_version = "2024-02-01"
    
    model_name = "whisper"
    deployment_id = "YOUR-DEPLOYMENT-NAME-HERE" #This will correspond to the custom name you chose for your deployment when you deployed a model."
    audio_language="en"
    
    audio_test_file = "./wikipediaOcelot.wav"
    
    result = openai.Audio.transcribe(
                file=open(audio_test_file, "rb"),            
                model=model_name,
                deployment_id=deployment_id
            )
    
    print(result)
```

---

Run the application using the `python` command on your quickstart file:

```python
python quickstart.py
```

> [!IMPORTANT]
> For production, store and access your credentials using a secure method, such as [Azure Key Vault](/azure/key-vault/general/overview). For more information, see [credential security](../../../ai-services/security-features.md).

## Output

```python
{"text":"The ocelot, Lepardus paradalis, is a small wild cat native to the southwestern United States, Mexico, and Central and South America. This medium-sized cat is characterized by solid black spots and streaks on its coat, round ears, and white neck and undersides. It weighs between 8 and 15.5 kilograms, 18 and 34 pounds, and reaches 40 to 50 centimeters 16 to 20 inches at the shoulders. It was first described by Carl Linnaeus in 1758. Two subspecies are recognized, L. p. paradalis and L. p. mitis. Typically active during twilight and at night, the ocelot tends to be solitary and territorial. It is efficient at climbing, leaping, and swimming. It preys on small terrestrial mammals such as armadillo, opossum, and lagomorphs."}
```
