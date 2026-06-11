---
title: How to evaluate Voice Live agents
titleSuffix: Foundry Tools
description: Learn how to evaluate the quality of your Voice Live voice agents using the evaluation harness and Microsoft Foundry built-in evaluators.
manager: mcleans
author: solarrezaei
ms.author: solarrezaei
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 05/19/2026
ms.custom: references_regions
# Customer intent: As a developer, I want to evaluate the quality of my Voice Live voice agent so I can measure conversational quality and identify areas for improvement.
---

# How to evaluate Voice Live agents (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Use the Voice Live evaluation harness to measure the quality of voice agents built on the [Voice Live API](./voice-live.md). The harness sends pre-recorded audio through Voice Live, collects transcriptions and responses, and then scores the results with [Microsoft Foundry built-in evaluators](/azure/ai-foundry/concepts/built-in-evaluators).

**How it works:**

```
Audio Dataset  →  Voice Live API  →  Transcript + Response  →  Foundry Evaluators  →  Quality Scores
```

The harness supports two modes:

- **Python CLI** (code-first) — Run evaluations locally with full control over configuration. The CLI sends audio through Voice Live, generates responses, and submits them to Foundry for scoring.
- **Foundry portal** — After the CLI generates evaluation output, you can view and compare results in the [Microsoft Foundry portal](/azure/ai-foundry/how-to/evaluate-generative-ai-app).

> [!NOTE]
> The evaluation harness measures conversational quality, such as task completion, intent resolution, and groundedness. It doesn't measure speech-specific metrics like Mean Opinion Score (MOS) or Word Error Rate (WER). It also isn't designed for competitive benchmarking.

For the full source code and developer reference, see the [Voice Live evaluation harness on GitHub](https://github.com/microsoft-foundry/voicelive-evaluation).

## Why evaluate your Voice Live agent?

Voice Live supports multiple models, voice activity detection (VAD) modes, voices, and session configurations. Evaluation helps you make data-driven decisions about which combination works best for your scenario. Common reasons to evaluate include:

- **Compare configurations.** Measure how different models (such as `gpt-realtime` versus `gpt-5`), VAD types, or voice settings affect response quality for your specific use case.
- **Catch regressions.** Run evaluations before and after configuration changes to confirm that updates improve quality and don't introduce new problems.
- **Identify weak points.** Find where your agent struggles, whether it's intent recognition, task completion, tool calling, or response accuracy, so you can improve prompts, tool definitions, or session settings.
- **Validate before deployment.** Establish a quality baseline across a representative dataset before you move a configuration to production.

## Prerequisites

- A [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) in a supported region. For current availability, see [Evaluation regions and limits](/azure/ai-foundry/concepts/evaluation-regions-limits-virtual-network). Confirmed regions: **Sweden Central** and **East US 2**.
- A [Foundry resource](../multi-service-resource.md) or [Azure Speech in Foundry Tools Services resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices) that supports Voice Live.
- The **Cognitive Services User** role on the Voice Live resource for API access. The **Azure AI User** role on the Foundry project for evaluation. For more information, see [Role-based access control for Microsoft Foundry](/azure/ai-foundry/concepts/rbac-foundry).
- An Azure OpenAI connection with a deployed GPT model that supports chat completion, such as `gpt-5-mini`. Voice Live uses this connection for the AI-assisted quality evaluators that score your agent's responses.
- Python 3.10 or later.
- Azure CLI with an authenticated session (`az login`) for [Microsoft Entra](/azure/ai-services/authentication) authentication (recommended). You can also use an API key.
- A test dataset with audio files and ground truth answers. For more information, see [Prepare your dataset](#prepare-your-dataset).

## Prepare your dataset

Your dataset is a JSON Lines (JSONL) file where each line represents one evaluation turn. Each turn includes an audio file and optional metadata for scoring.

### Required and recommended fields

| Field | Required? | Description |
|-------|-----------|-------------|
| `WavPath` or `input_audio` | **Yes** | Path to a WAV audio file (16-bit PCM or float32, any sample rate). The harness resamples automatically. You can also use inline base64 audio data. Paths are relative to the JSONL file location. Use clear speech with minimal background noise. |
| `Answer` or `expected_output` | **Strongly recommended** | The expected ground truth answer. Without this field, factual evaluators like groundedness and relevance have no baseline for comparison. |
| `Question` | Recommended | The text of the user's question. Used for logging and evaluation context. |
| `system_prompt` | Recommended | System instructions for the Voice Live session. These instructions must match the prompt your agent uses in production. |
| `conversationID` | For multi-turn | Groups turns into multi-turn conversations. The harness processes all turns with the same ID sequentially in one session. |
| `tool_definitions` | For tool calling | Function and tool definitions to register with the Voice Live session. Required if your scenario uses function calling. |

### Example dataset

```jsonl
{"WavPath": "audio/greeting.wav", "Answer": "Hello! How can I help you today?", "Question": "Hi there", "conversationID": "conv-001", "system_prompt": "You are a helpful customer support agent."}
{"WavPath": "audio/order_status.wav", "Answer": "Your order #12345 shipped yesterday and should arrive by Friday.", "Question": "Where is my order?", "conversationID": "conv-001"}
{"WavPath": "audio/weather.wav", "Answer": "The weather in Seattle is currently 65°F and partly cloudy.", "Question": "What's the weather like?", "conversationID": "conv-002", "system_prompt": "You are a weather assistant.", "tool_definitions": [{"type": "function", "name": "get_weather", "description": "Get current weather", "parameters": {"type": "object", "properties": {"location": {"type": "string"}}}}]}
```

> [!TIP]
> Dataset quality has a strong effect on evaluation scores. Datasets with specific questions, matching ground truth, and aligned system prompts typically produce higher scores. Datasets with open-ended questions and no ground truth typically produce lower scores, even with the same Voice Live configuration.

> [!TIP]
> The evaluation harness repository includes a helper script to download audio datasets from HuggingFace as evaluation-ready JSONL files. For details, see the [helper scripts documentation](https://github.com/microsoft-foundry/voicelive-evaluation/tree/main/helper_scripts).

### Multi-turn conversations

To create a multi-turn conversation, group related turns by using the same `conversationID`. The harness processes all turns in a conversation sequentially within a single Voice Live session and maintains conversation context across turns. The `system_prompt` and `tool_definitions` fields apply once per conversation, based on the first turn.

## Configure the evaluation

Voice Live session parameters control how the harness processes audio and how the agent responds. You can set these parameters in a JSON config file or as CLI arguments.

### Recommended configurations

| Configuration | Model | VAD type | EOU detection | Best for |
|--------------|-------|----------|---------------|----------|
| **VAD + Realtime** (recommended) | `gpt-realtime` | `azure_semantic_vad_multilingual` | Enabled | Lowest latency. Recommended for most evaluations. |
| **VAD + Cascaded** | `gpt-5` | `azure_semantic_vad_multilingual` | Enabled | Broader model selection (GPT-5, GPT-4.1, Phi). |
| **PTT + Realtime** (experimental) | `gpt-realtime` | `server_vad` | Disabled | Testing client-controlled speech boundaries. |
| **PTT + Cascaded** (experimental) | `gpt-5` | `server_vad` | Disabled | Testing client-controlled speech with cascaded models. |

> [!IMPORTANT]
> Use VAD mode for all production evaluations. PTT mode is experimental and has a lower audio response rate due to known platform limitations.

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
| `model` | string | `gpt-realtime` | The Voice Live model to use. Options include `gpt-realtime`, `gpt-5`, `gpt-4.1`, `gpt-5-mini`, and `phi4-mini`. |
| `voice` | string | `en-US-Ava:DragonHDLatestNeural` | The Azure text to speech voice. HD voices use the `:DragonHDLatestNeural` suffix. |
| `vad_type` | string | `azure_semantic_vad_multilingual` | The turn detection type. Options include `server_vad`, `azure_semantic_vad`, and `azure_semantic_vad_multilingual`. |
| `use_eou_detection` | bool | `true` | When set to `true`, enables semantic end-of-utterance detection. |
| `noise_reduction` | string | `azure_deep_noise_suppression` | The noise reduction type. Set to `none` to disable. |
| `push_to_talk` | bool | `false` | When set to `true`, enables push-to-talk mode instead of VAD. |

Pre-built sample configs are available in the [evaluation harness repository](https://github.com/microsoft-foundry/voicelive-evaluation/tree/main/evaluation_harness/configs).

> [!NOTE]
> The config file uses a simplified flat-key format for readability. For the full Voice Live API session parameters, see [How to use the Voice Live API](./voice-live-how-to.md).

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

The harness authenticates by using `DefaultAzureCredential`, which supports Azure CLI login and managed identity. You can also pass an API key with `--api-key` or set the `AZURE_VOICELIVE_API_KEY` environment variable.

The harness runs the full pipeline. It sends audio to Voice Live, collects responses, and submits results to Foundry for scoring.

### View results in Foundry portal

After the CLI generates evaluation output and submits it to Foundry, you can view and compare results in the Foundry portal. For details, see [View evaluation results](/azure/ai-foundry/how-to/evaluate-results).

### Batch processing

To evaluate multiple datasets in parallel, use the batch processor:

```bash
python batch_processor.py --test-files-folder datasets/ --max-workers 4
```

The batch processor creates subprocesses that write to a shared aggregated JSONL file. It then runs a single evaluation on the combined results.

## Understand your results

The evaluation harness uses Microsoft Foundry [built-in evaluators](/azure/ai-foundry/concepts/built-in-evaluators) to score Voice Live responses. Each evaluator measures a specific aspect of conversational quality.

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

### Selecting evaluators

By default, the harness runs the eight evaluators listed in the preceding table. You can customize evaluator selection with the `--evaluators` flag:

```bash
# Run all available evaluators (default + groundedness, relevance, fluency, coherence, tool_call_success)
python voice_agent_audio_input_evaluation.py -f dataset.jsonl --evaluators all

# Run only specific evaluators
python voice_agent_audio_input_evaluation.py -f dataset.jsonl --evaluators intent_resolution task_completion response_completeness
```

> [!NOTE]
> Custom evaluators aren't supported in this release. You can only select from the built-in evaluator set provided by Microsoft Foundry.

### Score interpretation

Evaluators produce different output types depending on their category.

**Agent and tool evaluators** like task_adherence, task_completion, tool_selection, tool_input_accuracy, and tool_call_success produce **binary Pass/Fail** results. When you aggregate these results across a dataset, they appear as a fraction. For example, 0.67 means 67% of turns passed.

**GPT-judge evaluators** like intent_resolution, response_completeness, groundedness, relevance, tool_call_accuracy, and tool_output_utilization produce scores on a **1 to 5 scale**. The system then converts these scores to Pass/Fail based on a threshold.

| Score range | Interpretation |
|-------------|---------------|
| **4.0–5.0** | Strong — response matches ground truth and task requirements |
| **3.0–3.9** | Acceptable — mostly correct with minor gaps |
| **2.0–2.9** | Weak — partial or incomplete response |
| **1.0–1.9** | Poor — incorrect or off-topic response |

**Recommended primary metrics:** Focus on **response_completeness**, **groundedness**, and **relevance** as primary evaluation metrics.

**How many runs are enough?** GPT-judge evaluators show natural run-to-run variance of 0.3 to 0.5 points. Run at least three evaluations and average the results before you draw conclusions. Record the evaluator model version for reproducibility.

To view detailed results in the Foundry portal, see [View evaluation results](/azure/ai-foundry/how-to/evaluate-results).

### Troubleshooting low scores

If your evaluation scores are unexpectedly low, complete these steps before you conclude there's a problem with your voice agent:

1. **Check your dataset quality.** Missing or mismatched ground truth is the most common cause of low scores. Verify that `Answer` fields are accurate and that `system_prompt` matches your agent's actual configuration.

1. **Separate evaluator issues from agent issues.** If the Voice Live transcription is accurate but evaluator scores are low, the problem might be in the evaluator or ground truth, not in Voice Live. Check the `response` field in the output JSONL to see what Voice Live produced.

1. **Run multiple evaluations.** A single run isn't enough to draw conclusions because of evaluator variance. Average at least three runs before you compare configurations.

1. **Try different session configurations.** Different model and VAD settings produce different response quality. Test VAD mode compared to PTT mode, and try different models.

## Evaluation data and output

The harness generates structured output at each stage of the pipeline that you can use for debugging and analysis.

### Local output

Each evaluation run produces an output folder with the following artifacts:

- **Output JSONL** — One line per evaluation turn, containing the original dataset fields, the Voice Live response, transcriptions, latency measurements, and evaluator scores.
- **Aggregated metrics** — Summary statistics across all turns, including per-evaluator averages.
- **Run metadata** — Configuration, timestamps, API version, and environment details for reproducibility.

### Data submitted to Foundry

When the harness submits results to Foundry for scoring, it sends the conversation transcripts, ground truth answers, and system prompts. Audio files aren't uploaded to Foundry. The evaluators score the text-based conversation data and return results to the local output.

### API version

The harness uses the Voice Live preview API. The API version is pinned in the harness source code and appended automatically to the endpoint URL. For the current API version, see the [harness repository configuration](https://github.com/microsoft-foundry/voicelive-evaluation).

> [!NOTE]
> Session-level logging and OpenTelemetry integration for Voice Live evaluation aren't available in this release. These capabilities are planned for a future update.

## Known issues

Some Foundry built-in evaluators have known issues that can affect Voice Live evaluation results.

| Evaluator | Issue | Impact | Status |
|-----------|-------|--------|--------|
| **Task Adherence** | May overemphasize agent self-introduction in multi-turn conversations. | Can inflate scores for greetings and penalize natural follow-ups. | Known limitation |
| **Task Completion** | Shows high variance across identical runs. | Run-to-run comparison is unreliable for this metric. Average multiple runs. | Known limitation |
| **Fluency / Coherence** | Tends to return the maximum score regardless of actual response quality. | Provides limited useful signal. Consider excluding these evaluators from analysis. | Known limitation |
| **Response Completeness** | A known issue can cause misleading scores when comparing certain model configurations. | Validate results by inspecting raw Voice Live responses in the output JSONL. | Mitigated |

For the complete list of known issues and workarounds, see the [evaluation harness README](https://github.com/microsoft-foundry/voicelive-evaluation/blob/main/evaluation_harness/README.md#known-evaluator-issues).

## Limitations

- **Text-based evaluators only.** Current evaluators assess conversational quality from transcribed text. Speech-specific metrics like MOS, WER, and voice naturalness aren't available.
- **Not a competitive benchmarking tool.** The harness evaluates Voice Live configurations. It doesn't support comparisons against other platforms.
- **Regional availability.** The Foundry Evaluations API isn't available in all regions. For current availability, see [Evaluation regions and limits](/azure/ai-foundry/concepts/evaluation-regions-limits-virtual-network).
- **Current scope.** This release covers Phase 1 functionality. Session logging, portal-native evaluation, and speech-specific evaluators are planned for future releases.

## Related content

- [Voice Live API overview](./voice-live.md)
- [Quickstart: Create a Voice Live real-time voice agent](./voice-live-quickstart.md)
- [How to use the Voice Live API](./voice-live-how-to.md)
- [Built-in evaluators reference](/azure/ai-foundry/concepts/built-in-evaluators)
- [Agent evaluators](/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators)
- [Run evaluations from the Microsoft Foundry portal](/azure/ai-foundry/how-to/evaluate-generative-ai-app)
- [View evaluation results](/azure/ai-foundry/how-to/evaluate-results)
- [Voice Live evaluation harness on GitHub](https://github.com/microsoft-foundry/voicelive-evaluation)

