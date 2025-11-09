---
title: Bring Your Own Model (BYOM) with Voice Live API (Preview)
description: Learn how to integrate your own models with the Voice Live API using Bring Your Own Model (BYOM) capabilities in Azure AI Speech Service.
author: goergenj
ms.author: jagoerge
ms.date: 11/09/2025
ms.topic: how-to
ms.service: azure-ai-speech
ms.custom: ai-speech, voice-live, byom, preview
---

# Bring Your Own Model (BYOM) with Voice Live API (Preview)

[!INCLUDE [preview-generic](includes/previews/preview-generic.md)]

The Voice Live API provides Bring Your Own Model (BYOM) capabilities, allowing you to integrate your custom models into the voice interaction workflow. BYOM is useful for the following scenarios:

- **Fine-tuned models**: Use your custom Azure OpenAI or Azure Foundry models
- **Provisioned throughput**: Use your PTU (Provisioned Throughput Units) deployments for consistent performance
- **Content safety**: Apply customized content safety configurations with your LLM

> [!IMPORTANT]
> You can integrate any model that's deployed in the same Azure Foundry resource you're using to call the Voice Live API.

> [!TIP]
> When you use your own model deployment with Voice Live, we recommend you set its content filtering configuration to [Asynchronous filtering](/azure/ai-foundry/openai/concepts/content-streaming#asynchronous-filtering) to reduce latency. Content filtering settings can be configured in the [Azure AI Foundry portal](https://ai.azure.com/).

## Authentication setup

When using Microsoft Entra ID authentication with Voice Live API, in `byom-azure-openai-chat-completion` mode specifically, you need to configure proper permissions for your Foundry resource. Since tokens may expire during long sessions, the system-assigned managed identity of the Foundry resource requires access to model deployments for the `byom-azure-openai-chat-completion` BYOM mode.

Run the following Azure CLI commands to configure the necessary permissions:

```bash
export subscription_id=<your-subscription-id>
export resource_group=<your-resource-group>
export foundry_resource=<your-foundry-resource>

# Enable system-assigned managed identity for the foundry resource
az cognitiveservices account identity assign --name ${foundry_resource} --resource-group ${resource_group} --subscription ${subscription_id}

# Get the system-assigned managed identity object ID
identity_principal_id=$(az cognitiveservices account show --name ${foundry_resource} --resource-group ${resource_group} --subscription ${subscription_id} --query "identity.principalId" -o tsv)

# Assign the Azure AI User role to the system identity of the foundry resource
az role assignment create --assignee-object-id ${identity_principal_id} --role "Azure AI User" --scope /subscriptions/${subscription_id}/resourceGroups/${resource_group}/providers/Microsoft.CognitiveServices/accounts/${foundry_resource}
```

## Choose BYOM integration mode

The Voice Live API supports two BYOM integration modes:

| Mode     | Description           | Example Models |
| ------- | ------------------ | ------------- |
| `byom-azure-openai-realtime`        | Azure OpenAI realtime models for streaming voice interactions              | `gpt-realtime`, `gpt-realtime-mini` |
| `byom-azure-openai-chat-completion` | Azure OpenAI chat completion models for text-based interactions. Also applies to other Foundry models | `gpt-4.1`, `gpt-5-chat`, `grok-3`         |

## Integrate BYOM

#### [REST API call](#tab/rest)

Update the endpoint URL in your API call to include your BYOM configuration:

```curl
wss://<your-foundry-resource>.cognitiveservices.azure.com/voice-live/realtime?api-version=2025-10-01&profile=<your-byom-mode>&model=<your-model-deployment>
```

Get the `<your-model-deployment>` value from the AI Foundry portal. It corresponds to the name you gave the model at deployment time.

#### [Python SDK](#tab/sdk)

[!INCLUDE [Header](./includes/common/voice-live-python.md)]

Use the [Python SDK quickstart code](/azure/ai-services/speech-service/voice-live-quickstart?tabs=windows%2Ckeyless&pivots=programming-language-python) to start a voice conversation, and make the following changes to enable BYOM:

1. In the `parse_arguments()` function, add a new argument for the BYOM profile type:
   
   ```python
   parser.add_argument(
        "--byom",
        help="BYOM (Bring Your Own Model) profile type",
        type=str,
        choices=["byom-azure-openai-realtime", "byom-azure-openai-chat-completion"],
        default=os.environ.get("VOICELIVE_BYOM_MODE", "byom-azure-openai-chat-completion"),

    )
   ```

1. In the `main()` function, add the `byom` field when creating the voice assistant:

    ```python
    # Create and start voice assistant
    assistant = BasicVoiceAssistant(
    ...
    byom=args.byom,
    ...
    )
    ```
        
1. In the `BasicVoiceAssistant` class, add the `byom` field:

    ```python
    class BasicVoiceAssistant:
    """Basic voice assistant implementing the VoiceLive SDK patterns."""

    def __init__(
        self,
        endpoint: str,
        credential: Union[AzureKeyCredential, TokenCredential],
        model: str,
        voice: str,
        instructions: str,
        byom: Literal["byom-azure-openai-realtime", "byom-azure-openai-chat-completion"] | None = None
    ):

        self.endpoint = endpoint
        self.credential = credential
        self.model = model
        self.voice = voice
        self.instructions = instructions
        self.connection: Optional["VoiceLiveConnection"] = None
        self.audio_processor: Optional[AudioProcessor] = None
        self.session_ready = False
        self.conversation_started = False
        self.byom = byom

    async def start(self):
        """Start the voice assistant session."""
        try:
            logger.info(f"Connecting to VoiceLive API with model {self.model}")

            # Connect to VoiceLive WebSocket API
            async with connect(
                endpoint=self.endpoint,
                credential=self.credential,
                model=self.model,
                query={
                    "profile": self.byom
                } if self.byom else None
            ) as connection:
            ...
    ```
1. When you run the code, specify the `--byom` argument along with the `--model` argument to indicate the BYOM profile and model deployment you want to use. For example:

    ```shell
    python voice-live-quickstart.py --byom "byom-azure-openai-chat-completion" --model "gpt-4o"
    ```

---

