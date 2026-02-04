---
title: Bring Your Own Model (BYOM) with Voice Live API
description: Learn how to integrate your own models with the Voice Live API using Bring Your Own Model (BYOM) capabilities in Azure Speech in Foundry Tools.
author: PatrickFarley
ms.author: pafarley
ms.date: 11/09/2025
ms.topic: how-to
ms.service: azure-ai-speech
ms.custom: ai-speech, voice-live, byom
ai-usage: ai-assisted
---

# Bring Your Own Model (BYOM) with Voice Live API

The Voice Live API provides Bring Your Own Model (BYOM) capabilities, allowing you to integrate your custom models into the voice interaction workflow. BYOM is useful for the following scenarios:

- **Fine-tuned models**: Use your custom Azure OpenAI or Azure Foundry models
- **Provisioned throughput**: Use your PTU (Provisioned Throughput Units) deployments for consistent performance
- **Content safety**: Apply customized content safety configurations with your LLM

> [!IMPORTANT]
> You can integrate any model that was deployed in the same Azure Foundry resource you're using to call the Voice Live API.

> [!TIP]
> When you use your own model deployment with Voice Live, we recommend you set its content filtering configuration to [Asynchronous filtering](/azure/ai-foundry/openai/concepts/content-streaming#asynchronous-filtering) to reduce latency. Content filtering settings can be configured in the [Microsoft Foundry portal](https://ai.azure.com/).

## Authentication setup

When using Microsoft Entra ID authentication with Voice Live API, in `byom-azure-openai-chat-completion` mode specifically, you need to configure proper permissions for your Foundry resource. Since tokens expire during long sessions, the system-assigned managed identity of the Foundry resource requires access to model deployments for the `byom-azure-openai-chat-completion` BYOM mode.

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

Get the `<your-model-deployment>` value from the Foundry portal. It corresponds to the name you gave the model at deployment time.

#### [Python SDK](#tab/python)

[!INCLUDE [Header](./includes/common/voice-live-python.md)]

Use the [Python SDK quickstart code](./voice-live-quickstart.md?tabs=windows%2Ckeyless&pivots=programming-language-python) to start a voice conversation, and make the following changes to enable BYOM:

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
    python voice-live-quickstart.py --byom "byom-azure-openai-chat-completion" --model "your-model-name"
    ```

#### [C# SDK](#tab/csharp)

[!INCLUDE [Header](./includes/common/voice-live-csharp.md)]

Use the [C# VoiceLive SDK quickstart code](./voice-live-quickstart.md?tabs=windows%2Ckeyless&pivots=programming-language-csharp) to start a voice conversation, and make the following changes to enable BYOM:

1. Add the `System.Web` and `System.Runtime.InteropServices` using statements at the top of the file:

    ```csharp
    using System.Web;
    using System.Runtime.InteropServices;
    ```

1. In the `CreateRootCommand` function, replace it with the following code to add "byomOption":

    ```csharp
    private static RootCommand CreateRootCommand()
    {
        var rootCommand = new RootCommand("Basic Voice Assistant using Azure VoiceLive SDK");

        var apiKeyOption = new Option<string?>(
            "--api-key",
            "Azure VoiceLive API key. If not provided, will use AZURE_VOICELIVE_API_KEY environment variable.");

        var endpointOption = new Option<string>(
            "--endpoint",
            () => "wss://api.voicelive.com/v1",
            "Azure VoiceLive endpoint");

        var modelOption = new Option<string>(
            "--model",
            () => "gpt-4o",
            "VoiceLive model to use");

        var byomOption = new Option<string>(
            "--byom",
            () => "byom-azure-openai-chat-completion",
            "BYOM integration mode. Supported modes: byom-azure-openai-realtime, byom-azure-openai-chat-completion");

        var voiceOption = new Option<string>(
            "--voice",
            () => "en-US-AvaNeural",
            "Voice to use for the assistant");

        var instructionsOption = new Option<string>(
            "--instructions",
            () => "You are a helpful AI assistant. Respond naturally and conversationally. Keep your responses concise but engaging. Always start the conversation in English.",
            "System instructions for the AI assistant");

        var useTokenCredentialOption = new Option<bool>(
            "--use-token-credential",
            "Use Azure token credential instead of API key");

        var verboseOption = new Option<bool>(
            "--verbose",
            "Enable verbose logging");

        rootCommand.AddOption(apiKeyOption);
        rootCommand.AddOption(endpointOption);
        rootCommand.AddOption(modelOption);
        rootCommand.AddOption(byomOption);
        rootCommand.AddOption(voiceOption);
        rootCommand.AddOption(instructionsOption);
        rootCommand.AddOption(useTokenCredentialOption);
        rootCommand.AddOption(verboseOption);

        rootCommand.SetHandler(async (
            string? apiKey,
            string endpoint,
            string model,
            string byom,
            string voice,
            string instructions,
            bool useTokenCredential,
            bool verbose) =>
        {
            await RunVoiceAssistantAsync(apiKey, endpoint, model, byom, voice, instructions, useTokenCredential, verbose).ConfigureAwait(false);
        },
        apiKeyOption,
        endpointOption,
        modelOption,
        byomOption,
        voiceOption,
        instructionsOption,
        useTokenCredentialOption,
        verboseOption);

        return rootCommand;
    }
    ```
  
1. In function `RunVoiceAssistantAsync`, add "byom" parameter and configuration setup:

    ```csharp
    private static async Task RunVoiceAssistantAsync(
        string? apiKey,
        string endpoint,
        string model,
        string byom,
        string voice,
        string instructions,
        bool useTokenCredential,
        bool verbose)
    {
        // Setup configuration
        var configuration = new ConfigurationBuilder()
            .AddJsonFile("appsettings.json", optional: true)
            .AddEnvironmentVariables()
            .Build();
    
        // Override with command line values if provided
        apiKey ??= configuration["VoiceLive:ApiKey"] ?? Environment.GetEnvironmentVariable("AZURE_VOICELIVE_API_KEY");
        endpoint = configuration["VoiceLive:Endpoint"] ?? endpoint;
        model = configuration["VoiceLive:Model"] ?? model;
        byom = configuration["VoiceLive:Byom"] ?? byom;
        voice = configuration["VoiceLive:Voice"] ?? voice;
        instructions = configuration["VoiceLive:Instructions"] ?? instructions;
    ...  
    ```

1. In function `RunVoiceAssistantAsync` append the BYOM profile parameter to the endpoint URL before creating the client:

    ```csharp
    try
    {
        // Append BYOM profile parameter to the endpoint URL if provided
        if (!string.IsNullOrEmpty(byom))
        {
            var uriBuilder = new UriBuilder(endpoint);
            var query = HttpUtility.ParseQueryString(uriBuilder.Query);
            query["profile"] = byom;
            uriBuilder.Query = query.ToString();
            endpoint = uriBuilder.ToString();
            logger.LogInformation("BYOM profile parameter added to endpoint: profile={Profile}", byom);
        }

        // Create client with appropriate credential
        VoiceLiveClient client;
        var endpointUri = new Uri(endpoint);
        if (useTokenCredential)
        {
            var tokenCredential = new DefaultAzureCredential();
            client = new VoiceLiveClient(endpointUri, tokenCredential, new VoiceLiveClientOptions());
            logger.LogInformation("Using Azure token credential");
        }
        else
        {
            var keyCredential = new Azure.AzureKeyCredential(apiKey!);
            client = new VoiceLiveClient(endpointUri, keyCredential, new VoiceLiveClientOptions());
            logger.LogInformation("Using API key credential");
        }
    ...
    ```
    
1. In function `RunVoiceAssistantAsync`, add "byom" to the voice assistant setup:

    ```csharp
    ...
    // Create and start voice assistant
    using var assistant = new BasicVoiceAssistant(
        client,
        model,
        byom,
        voice,
        instructions,
        loggerFactory);
    ...
    ```

1. In class `BasicVoiceAssistant`, add the `_byom` field and update the constructor:

    ```csharp
    public class BasicVoiceAssistant : IDisposable
    {
        private readonly VoiceLiveClient _client;

        private readonly string _model;
        private readonly string _byom;
        private readonly string _voice;
        private readonly string _instructions;
        ...

        public BasicVoiceAssistant(
            VoiceLiveClient client,
            string model,
            string byom,
            string voice,
            string instructions,
            ILoggerFactory loggerFactory)
        {
            _client = client ?? throw new ArgumentNullException(nameof(client));
            _model = model ?? throw new ArgumentNullException(nameof(model));
            _byom = byom ?? throw new ArgumentNullException(nameof(byom));
            _voice = voice ?? throw new ArgumentNullException(nameof(voice));
            _instructions = instructions ?? throw new ArgumentNullException(nameof(instructions));
            _loggerFactory = loggerFactory ?? throw new ArgumentNullException(nameof(loggerFactory));
            _logger = loggerFactory.CreateLogger<BasicVoiceAssistant>();
        }
    ...
    ```

1. In function `StartAsync` update the logging and session start call (BYOM profile is already in the endpoint):

    ```csharp
    public async Task StartAsync(CancellationToken cancellationToken = default)
    {
        try
        {
            _logger.LogInformation("Connecting to VoiceLive API with model {Model} and BYOM mode {Byom}", _model, _byom);

            // Start VoiceLive session (BYOM profile is already in the client endpoint)
            _session = await _client.StartSessionAsync(_model, cancellationToken).ConfigureAwait(false);
    ...
    ```

1. When you run the code, specify the `--byom` argument along with the `--model` argument to indicate the BYOM profile and model deployment you want to use. For example:

    ```shell
    dotnet run --byom "byom-azure-openai-chat-completion" --model "your-model-name"
    ```

---

## Related content

- Try the [Voice Live quickstart](./voice-live-quickstart.md)
- Learn more about [How to use the Voice Live API](./voice-live-how-to.md)
- See the [Voice Live API reference](./voice-live-api-reference-2025-10-01.md)
