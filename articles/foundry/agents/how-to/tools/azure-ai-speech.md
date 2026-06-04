---
title: "Connect Azure Speech in Foundry Tools to an agent"
description: "Connect Azure Speech in Foundry Tools to an agent by using an MCP server for speech-to-text and text-to-speech in Foundry Agent Service."
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 05/31/2026
author: PatrickFarley
ms.author: pafarley
ms.custom: 
- azure-ai-agents
- pilot-ai-workflow-jan-2026
- doc-kit-assisted
ai-usage: ai-assisted
keywords: Azure Speech, speech to text, text to speech, MCP, Model Context Protocol, Foundry Agent Service
---

# Connect Azure Speech in Foundry Tools to an agent
Azure Speech in Foundry Tools lets your agent convert speech to text and generate speech audio from text. You connect the tool by adding a remote Model Context Protocol (MCP) server to your agent in Foundry Agent Service.

> [!IMPORTANT]
> The Speech MCP tool doesn't support [Network-secured Microsoft Foundry](../../../agents/how-to/virtual-networks.md). For more information, see [Connect to Model Context Protocol servers](./model-context-protocol.md).

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Microsoft Foundry resource](../../../../ai-services/multi-service-resource.md) created in a [supported region](../../../../ai-services/speech-service/regions.md). Your Foundry resource includes speech capabilities and is used by the Speech MCP server.
- Your Foundry resource must support MCP tools in Foundry Agent Service. MCP tools require the Agent Service Enterprise tier. For the list of regions and models that support MCP tools, see [Tool support by region and model](../../concepts/tool-best-practice.md#tool-support-by-region-and-model).

> [!NOTE]
> If you receive the error `Invalid tool value(s): mcp. Use the Enterprise offerings to access these tool(s)` when you connect the tool, your resource doesn't support MCP. Create a new Foundry resource that supports the Enterprise tier in a supported region.

## Usage support

This article shows how to connect the tool in Foundry portal.

If you want to work with code, see [Connect to Model Context Protocol servers](./model-context-protocol.md) for SDK examples in Python, C#, and JavaScript.

## Security and privacy

Treat your Speech resource key and storage shared access signature (SAS) URLs as secrets:

- Don't paste keys or SAS URLs into agent prompts, chat transcripts, screenshots, or source control.
- Use the shortest practical SAS expiry time.
- Scope SAS URLs to the minimum required resource (for example, a single container).
- Rotate keys periodically as a security best practice, or immediately if you suspect they're exposed.

## Set up storage

You need an Azure Storage account to store input audio files for speech-to-text processing and receive output audio files from text-to-speech processing.

1. [Create an Azure Storage account](/azure/storage/common/storage-account-create?tabs=azure-portal) if you don't already have one.
1. Assign the **Storage Blob Data Contributor** role to your user account on the storage account so you can generate SAS URLs:
   1. In the [Azure portal](https://portal.azure.com), go to your storage account.
   1. Select **Access control (IAM)** > **Add** > **Add role assignment**.
   1. Select the **Storage Blob Data Contributor** role, assign it to your user account, and then select **Review + assign**.
1. Create one or more blob containers to store the input and output audio files. In your storage account, select **Containers** > **+ Container**, enter a name (for example, `speech-audio`), and then select **Create**.

## Create an agent

1. Go to [!INCLUDE [foundry-link](../../../includes/foundry-link.md)].
1. In the upper-right menu, select **Build**.
1. In the left pane, select **Agents**, and then select **Create agent**.
1. Enter a name and description.
1. Select a model that supports tool calling, such as `gpt-4o` or later. Models without tool-calling capability can't invoke the Speech MCP server.
1. Select **Create**.

Your agent appears in the **Agents** list. Select it to open the agent playground.

## Connect the Azure Speech tool to your agent

1. In your agent, open the agent playground.
1. Under **Tools**, select **Add** > **Add a new tool**.
1. In **Select a tool**, select the **Catalog** tab.
1. Search for **Azure Speech MCP Server**, select it, and then select **Create**.
1. On the setup page, fill in the following fields:  

   | Section | Field | Value |
   |---|---|---|
   | **Parameters** | `foundry-resource-name` | The name of the Foundry resource you created in the prerequisites. |
   | **Authorization** | `Bearer` (API key) | Either `KEY1` or `KEY2` from your Foundry resource's **Keys and Endpoint** page in the Azure portal. |
   | **Authorization** | `X-Blob-Container-Url` | A SAS URL for your storage container with **read** and **write** permissions. The service stores audio output files in this container. |

   To generate the container SAS URL: in the Azure portal, go to your storage container, select **Shared access tokens**, set **Permissions** to **Read** and **Write**, set the shortest practical expiry time, select **Generate SAS token and URL**, and then copy the **Blob SAS URL**.

1. Select **Connect** to add the remote Speech MCP server as a tool for your agent.

After connecting, the Speech tool appears in your agent's **Tools** list with a connected status. If it doesn't, see [Troubleshooting](#troubleshooting).

## Test the Azure Speech tool

In the agent playground chat, enter `What can you do?`.

The agent lists its available capabilities, including speech-to-text and text-to-speech. This confirms that the remote Speech MCP server is connected.

### Test speech-to-text

The Speech tool can convert an audio file to text. The audio file can be stored in Azure Blob Storage and accessed with a SAS URL, or it can be any publicly accessible URL to an audio file.

> [!NOTE]
> Supported audio formats include WAV, MP3, OGG, FLAC, and other common formats. For best results with speech recognition, use WAV files with 16 kHz sample rate and 16-bit depth.

1. Upload your audio file to your Azure blob storage container.
1. Generate a SAS URL for the file using one of the following methods:

   **Azure portal:**
   1. Select your uploaded audio file.
   1. In **Properties**, select **Generate SAS**.
   1. Under **Permissions**, select **Read**.
   1. Set the shortest practical expiry time, and then select **Generate SAS token and URL**.

   **Azure CLI:**

   ```azurecli
   az storage blob generate-sas \
       --account-name <your-storage-account> \
       --container-name <your-container> \
       --name <your-audio-file> \
       --permissions r \
       --expiry <expiry-datetime-utc> \
       --auth-mode login \
       --as-user \
       --full-uri -o tsv
   ```

1. Copy the SAS URL. Then use it in one of the following example prompts in the agent chat window: 
    - `Recognize this English audio file located in <blob SAS URL>` 
    - `Recognize the audio file located in <blob SAS URL> with these phrase hints: "Azure, OpenAI, Cognitive Services, Lucy" to improve accuracy.` 
    - `Convert this audio file located in <blob SAS URL> into text and summarize it for me.` 
    - `Recognize this French audio file located in <blob SAS URL> with detailed output format.` 
    - `Recognize this Hindi audio file located in <blob SAS URL> and remove profanity.` 
1. View the output text in the chat window.

### Test text-to-speech

Start a new chat in the agent playground, and use one of the following example prompts. Replace the placeholder with your own text:
- `Convert text to speech: <your text to speak>` 
- `Synthesize speech from "<your text to speak>"`
- `Generate speech audio from text "<your text to speak>"` 
- `Convert text to speech with Chinese language: <your text to speak>` 
- `Synthesize speech with voice en-US-JennyNeural from text <your text to speak>` 

The output audio is saved as a WAV file in your blob container. An audio link is displayed in the chat window. Select it to listen to the output.

## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| You can't find **Azure Speech MCP Server** in the tool catalog. | The tool isn't available for your tenant, region, or resource tier. | Confirm your Foundry resource is created in a supported region and supports MCP tools (Agent Service Enterprise tier). |
| **Connect** fails with `Invalid tool value(s): mcp. Use the Enterprise offerings to access these tool(s)`. | Your Foundry resource doesn't support MCP tools. | Create a new Foundry resource with the Enterprise Agent Service tier in a supported region. |
| **Connect** fails with authorization errors. | The API key is incorrect or expired. | Recopy `KEY1` or `KEY2` from your resource's **Keys and Endpoint** page. Rotate keys if needed. |
| Speech output audio link doesn't work. | The container SAS URL is invalid, expired, or missing permissions. | Regenerate the container SAS URL with **read** and **write** permissions and a valid expiry time. |
| Speech-to-text can't access the audio file. | The file SAS URL is invalid or expired. | Regenerate the file SAS URL with **read** permission and retry the prompt. |
| Agent doesn't list speech capabilities after you connect the tool. | The selected model doesn't support tool calling. | Select a tool-capable model (such as `gpt-4o` or later) in the agent configuration. |
| Audio upload fails with a permission error. | Your account lacks the **Storage Blob Data Contributor** role on the container. | Assign the **Storage Blob Data Contributor** role to your user account on the storage account. |

## Clean up resources

If you created resources only to test this tool, remove them to avoid ongoing costs:

- **Delete the agent:** In the Foundry portal, go to **Agents**, select your test agent, and then select **Delete**.
- **Delete the storage container** (optional): In the Azure portal, go to your storage container and select **Delete**.
- **Revoke SAS URLs:** SAS URLs expire automatically based on the expiry time you set. To revoke all SAS tokens immediately, rotate your storage account keys on the **Access keys** page.

## Next steps

- Learn more about MCP connections: [Connect to Model Context Protocol servers](./model-context-protocol.md).
- Review tool usage guidance: [Tool best practices](../../concepts/tool-best-practice.md).

[!INCLUDE [speech-in-foundry](../../../includes/speech-features-foundry.md)]