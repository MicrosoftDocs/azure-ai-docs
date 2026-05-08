---
title: How to evaluate Voice Live agents
titleSuffix: Foundry Tools
description: Learn how to evaluate the quality of your Voice Live voice agents using the evaluation harness and Microsoft Foundry built-in evaluators.
manager: nitinme
author: solarrezaei
ms.author: solarrezaei
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 05/08/2026
ms.custom: references_regions
# Customer intent: As a developer, I want to evaluate the quality of my Voice Live voice agent so I can measure conversational quality and identify areas for improvement.
---

# How to evaluate Voice Live agents (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

The Voice Live evaluation harness provides end-to-end quality evaluation for voice agents built on the [Voice Live API](./voice-live.md). It sends pre-recorded audio through Voice Live, collects transcriptions and responses, and scores the results using [Microsoft Foundry built-in evaluators](/azure/ai-foundry/concepts/built-in-evaluators).

**How it works:**

```
Audio Dataset  →  Voice Live API  →  Transcript + Response  →  Foundry Evaluators  →  Quality Scores
```

The harness supports two execution modes:

- **Python CLI** (code-first): Run evaluations locally with full control over configuration. The CLI sends audio through Voice Live, generates responses, and submits them to Foundry for scoring.
- **Foundry portal**: After the CLI generates evaluation output, you can view and compare results in the [Microsoft Foundry portal](/azure/ai-foundry/how-to/evaluate-generative-ai-app). Portal-native Voice Live audio evaluation isn't available yet.

> [!NOTE]
> The evaluation harness measures conversational quality (task completion, intent resolution, groundedness). It doesn't measure speech-specific metrics like MOS or WER, and isn't designed for competitive benchmarking.

For the full source code and developer documentation, see the [Voice Live evaluation harness on GitHub](https://github.com/microsoft-foundry/voicelive-evaluation).

## Prerequisites

- A [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) in a supported region. For current region availability, see [Evaluation regions and limits](/azure/ai-foundry/concepts/evaluation-regions-limits-virtual-network). Confirmed working for Voice Live evaluation: **Sweden Central** and **East US 2**.
- A [Foundry resource](../multi-service-resource.md) or [Azure Speech in Foundry Tools Services resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices) that supports Voice Live.
- **Cognitive Services User** role on the Voice Live resource (for API access) AND **Azure AI User** role on the Foundry project (for evaluation). For more information, see [Role-based access control for Microsoft Foundry](/azure/ai-foundry/concepts/rbac-foundry).
- An Azure OpenAI connection with a deployed GPT model that supports chat completion (for example, `gpt-5-mini`). Required for AI-assisted quality evaluators.
- Python 3.10 or later.
- Azure CLI authenticated (`az login`) for [Microsoft Entra](/azure/ai-services/authentication) credential-based authentication (recommended). Alternatively, you can use an API key.
- A test dataset with audio files and ground truth answers. See [Prepare your dataset](#prepare-your-dataset).

## Prepare your dataset

Your dataset is a JSONL file where each line represents one evaluation turn. Each turn includes an audio file and optional metadata that the evaluators use for scoring.

### Required and recommended fields

| Field | Required? | Description |
|-------|-----------|-------------|
| `WavPath` or `input_audio` | **Yes** | Path to a WAV audio file (16-bit PCM or float32, any sample rate — resampled automatically) or inline base64 audio data. Paths are relative to the JSONL file location. Audio should be clear speech with minimal background noise. |
| `Answer` or `expected_output` | **Strongly recommended** | Ground truth answer. Without this, factual evaluators (groundedness, relevance) have nothing to compare against. |
| `Question` | Recommended | Text of the user's question. Used for logging and evaluation context. |
| `system_prompt` | Recommended | System instructions for the Voice Live session. Must match the prompt your agent uses in production. |
| `conversationID` | For multi-turn | Groups turns into multi-turn conversations. All turns with the same ID are processed sequentially in one session. |
| `tool_definitions` | For tool calling | Function/tool definitions to register with the Voice Live session. Required if your scenario involves function calling. |

### Example dataset

```jsonl
{"WavPath": "audio/greeting.wav", "Answer": "Hello! How can I help you today?", "Question": "Hi there", "conversationID": "conv-001", "system_prompt": "You are a helpful customer support agent."}
{"WavPath": "audio/order_status.wav", "Answer": "Your order #12345 shipped yesterday and should arrive by Friday.", "Question": "Where is my order?", "conversationID": "conv-001"}
{"WavPath": "audio/weather.wav", "Answer": "The weather in Seattle is currently 65°F and partly cloudy.", "Question": "What's the weather like?", "conversationID": "conv-002", "system_prompt": "You are a weather assistant.", "tool_definitions": [{"type": "function", "name": "get_weather", "description": "Get current weather", "parameters": {"type": "object", "properties": {"location": {"type": "string"}}}}]}
```

> [!TIP]
> Dataset quality strongly affects evaluation scores. In testing, datasets with specific questions, matching ground truth, and aligned system prompts scored 4.0+ on average. Datasets with open-ended questions and no ground truth scored 2.0–3.0 with identical Voice Live configurations.

### Multi-turn conversations

Group related turns using `conversationID`. The harness processes all turns in a conversation sequentially within a single Voice Live session, maintaining conversation context across turns. The `system_prompt` and `tool_definitions` fields are set once per conversation from the first turn.

## Configure the evaluation

Voice Live session parameters control how audio is processed and how the agent responds. Configure these as a JSON config file or as CLI arguments.

### Recommended configurations

| Configuration | Model | VAD type | EOU detection | Best for |
|--------------|-------|----------|---------------|----------|
| **VAD + Realtime** (recommended) | `gpt-realtime` | `azure_semantic_vad_multilingual` | Enabled | Lowest latency. Recommended for most evaluations. |
| **VAD + Cascaded** | `gpt-5` | `azure_semantic_vad_multilingual` | Enabled | Broader model selection (GPT-5, GPT-4.1, Phi). |
| **PTT + Realtime** (experimental) | `gpt-realtime` | `server_vad` | Disabled | Testing client-controlled speech boundaries. |
| **PTT + Cascaded** (experimental) | `gpt-5` | `server_vad` | Disabled | Testing client-controlled speech with cascaded models. |

> [!IMPORTANT]
> VAD mode is recommended for all production evaluations. PTT mode is experimental and has a lower audio response rate (~83% vs ~100%) due to known platform limitations.

### Example config file

```json
{
    "model": "gpt-realtime",
    "voice": "en-US-Ava:DragonHDLatestNeural",
    "voice_type": "azure-standard",
    "noise_reduction": "azure_deep_noise_suppression",
    "echo_cancellation": "server_echo_cancellation",
    "vad_type": "azure_semantic_vad_multilingual",
    "use_eou_detection": true,
    "push_to_talk": false,
    "enable_barge_in": true
}
```

### Key parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `gpt-realtime` | Voice Live model. Options: `gpt-realtime`, `gpt-5`, `gpt-4.1`, `gpt-5-mini`, `phi4-mini`. |
| `voice` | string | `en-US-Ava:DragonHDLatestNeural` | Azure TTS voice. HD voices use the `:DragonHDLatestNeural` suffix. |
| `vad_type` | string | `azure_semantic_vad_multilingual` | Turn detection type. Options: `server_vad`, `azure_semantic_vad`, `azure_semantic_vad_multilingual`. |
| `use_eou_detection` | bool | `true` | Enable semantic end-of-utterance detection. |
| `noise_reduction` | string | `azure_deep_noise_suppression` | Noise reduction. Set to `none` to disable. |
| `push_to_talk` | bool | `false` | Enable push-to-talk mode instead of VAD. |

Pre-built sample configs are available in the [evaluation harness repository](https://github.com/microsoft-foundry/voicelive-evaluation/tree/main/evaluation_harness/configs).

> [!NOTE]
> The config file uses the **evaluation harness schema** (flat keys like `vad_type`, `noise_reduction`), not the raw Voice Live API session update format. For Voice Live API session parameters, see [How to use the Voice Live API](./voice-live-how-to.md).

## Run the evaluation

### CLI quickstart

```bash
# Clone the repository
git clone https://github.com/microsoft-foundry/voicelive-evaluation.git
cd voicelive-evaluation/evaluation_harness

# Install dependencies
pip install -r requirements.txt

# Set environment variables
# AZURE_VOICELIVE_ENDPOINT: base resource endpoint (the harness appends the path and API version)
export AZURE_VOICELIVE_ENDPOINT="wss://<your-resource>.services.ai.azure.com"
# PROJECT_ENDPOINT: Foundry project endpoint for evaluation submission
export PROJECT_ENDPOINT="https://<your-resource>.services.ai.azure.com/api/projects/<your-project>"

# Authenticate with Azure CLI (recommended)
az login

# Run evaluation with a config file
python voice_agent_audio_input_evaluation.py \
    -f datasets/my-dataset.jsonl \
    --config configs/sample_vad_realtime.json \
    -o output/my-eval-run
```

The harness authenticates using `DefaultAzureCredential` (Azure CLI login or managed identity). Alternatively, pass an API key with `--api-key` or set the `AZURE_VOICELIVE_API_KEY` environment variable.

The harness runs the full pipeline: sends audio to Voice Live, collects responses, and submits results to Foundry for evaluation scoring.

### View results in Foundry portal

After the CLI generates evaluation output and submits it to Foundry, you can view and compare results in the Foundry portal. For details, see [View evaluation results](/azure/ai-foundry/how-to/evaluate-results).

### Batch processing

For evaluating multiple datasets in parallel:

```bash
python batch_processor.py --test-files-folder datasets/ --max-workers 4
```

The batch processor spawns subprocesses that write to a shared aggregated evaluation JSONL file, then runs a single evaluation on the combined results.

## Understand your results

The evaluation harness uses Microsoft Foundry [built-in evaluators](/azure/ai-foundry/concepts/built-in-evaluators) to score Voice Live responses. Each evaluator measures a different aspect of conversational quality.

### Default evaluators

| Evaluator | Category | What it measures | Learn more |
|-----------|----------|------------------|------------|
| Intent Resolution | Agent | Whether the agent correctly identified the user's intent | [Agent evaluators](/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators) |
| Task Adherence | Agent | Whether the agent followed system instructions and rules | [Agent evaluators](/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators) |
| Task Completion | Agent | Whether the agent fully completed the requested task | [Agent evaluators](/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators) |
| Response Completeness | RAG | Whether the response covers all critical information from ground truth | [RAG evaluators](/azure/ai-foundry/concepts/evaluation-evaluators/rag-evaluators) |
| Tool Call Accuracy | Agent (tool) | Whether the agent made correct tool calls with correct parameters | [Agent evaluators](/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators) |
| Tool Selection | Agent (tool) | Whether the agent selected the correct tools | [Agent evaluators](/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators) |
| Tool Input Accuracy | Agent (tool) | Whether tool call parameters are correct | [Agent evaluators](/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators) |
| Tool Output Utilization | Agent (tool) | Whether tool results were used correctly in the response | [Agent evaluators](/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators) |

Additional evaluators available with `--evaluators all`: `groundedness`, `relevance`, `tool_call_success`, `fluency`, `coherence`. For details on each evaluator, see [Built-in evaluators reference](/azure/ai-foundry/concepts/built-in-evaluators).

### Score interpretation

Evaluators produce different output types depending on their category:

**Agent and tool evaluators** (task_adherence, task_completion, tool_selection, tool_input_accuracy, tool_call_success) produce **binary Pass/Fail** results. When aggregated across a dataset, these appear as a fraction (for example, 0.67 means 67% of turns passed).

**GPT-judge evaluators** (intent_resolution, response_completeness, groundedness, relevance, tool_call_accuracy, tool_output_utilization) produce scores on a **1–5 scale**, then converted to Pass/Fail based on a threshold:

| Score range | Interpretation |
|-------------|---------------|
| **4.0–5.0** | Strong — response matches ground truth and task requirements |
| **3.0–3.9** | Acceptable — mostly correct with minor gaps |
| **2.0–2.9** | Weak — partial or incomplete response |
| **1.0–1.9** | Poor — incorrect or off-topic response |

**Recommended primary metrics:** Focus on **response_completeness**, **groundedness**, and **relevance** as primary evaluation metrics.

**How many runs are enough?** GPT-judge evaluators show natural run-to-run variance of ±0.3–0.5 points. Always run at least 3 evaluations and average results before drawing conclusions. Note the evaluator model version used for reproducibility.

To view detailed results in the Foundry portal, see [View evaluation results](/azure/ai-foundry/how-to/evaluate-results).

### Troubleshooting low scores

If your evaluation scores are unexpectedly low, work through these steps before concluding there's a problem with your voice agent:

1. **Check your dataset quality.** Missing or mismatched ground truth is the most common cause of low scores. Verify that `Answer` fields are accurate and that `system_prompt` matches your agent's actual configuration.

1. **Distinguish evaluator issues from agent issues.** If the Voice Live transcription is accurate but evaluator scores are low, the problem might be in the evaluator or ground truth — not in Voice Live. Check the `response` field in the output JSONL to see what Voice Live actually produced.

1. **Run multiple evaluations.** A single run isn't sufficient to draw conclusions due to evaluator variance. Average at least 3 runs before comparing configurations.

1. **Try different session configs.** Different model and VAD configurations produce different response quality. Test VAD vs PTT mode, and try different models.

## Known issues

Some Foundry built-in evaluators have known issues that can affect Voice Live evaluation results. These issues are tracked with the Azure AI Evaluation team.

| Evaluator | Issue | Impact | Status |
|-----------|-------|--------|--------|
| **Task Adherence** | Re-introduction bug — forces the model to re-introduce itself every turn | Inflates scores for greetings; penalizes natural follow-ups | Being fixed by evaluation team |
| **Task Completion** | High variance across identical runs (for example, 0.67 vs 0.33 on the same input) | Makes run-to-run comparison unreliable for this metric | Under investigation |
| **Fluency / Coherence** | Consistently scores 5.0 regardless of actual response quality | Provides no useful signal. Consider excluding from your evaluation. | Consider removing from default set |
| **Response Completeness** | Known bug caused misleading scores when comparing certain model configurations | Validate results by inspecting raw Voice Live responses in the output JSONL | Mitigated |
| **All GPT-judge evaluators** | Scores vary across environments (local vs cloud) and drift 1–2% over time | Average multiple runs and pin evaluator model versions for reliable comparisons | Known |

For the complete list of known issues and workarounds, see the [evaluation harness README](https://github.com/microsoft-foundry/voicelive-evaluation/blob/main/evaluation_harness/README.md#known-evaluator-issues).

## Limitations

- **Text-based evaluators only.** Current evaluators assess conversational quality from transcribed text. Speech-specific metrics (MOS, WER, voice naturalness) aren't available.
- **Not a competitive benchmarking tool.** The harness evaluates Voice Live configurations, not comparisons against other platforms.
- **Regional availability.** The Foundry Evaluations API isn't available in all regions. For current availability, see [Evaluation regions and limits](/azure/ai-foundry/concepts/evaluation-regions-limits-virtual-network).
- **Current scope.** This is a Phase 1 release. Session logging, portal-native evaluation UX, and speech-specific evaluators are planned for future releases.

## Related content

- [Voice Live API overview](./voice-live.md)
- [Quickstart: Create a Voice Live real-time voice agent](./voice-live-quickstart.md)
- [How to use the Voice Live API](./voice-live-how-to.md)
- [Built-in evaluators reference](/azure/ai-foundry/concepts/built-in-evaluators)
- [Agent evaluators](/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators)
- [Run evaluations from the Microsoft Foundry portal](/azure/ai-foundry/how-to/evaluate-generative-ai-app)
- [View evaluation results](/azure/ai-foundry/how-to/evaluate-results)
- [Voice Live evaluation harness on GitHub](https://github.com/microsoft-foundry/voicelive-evaluation)
