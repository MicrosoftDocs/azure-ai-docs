---
title: Get started with interactive training (preview) in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Clone the interactive-training samples and run a short reinforcement-learning recipe in Microsoft Foundry.
author: chillatom
ms.author: coreyhill
ms.reviewer: williamliang
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: quickstart
ms.date: 10/06/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Get started with interactive training (preview) in Microsoft Foundry

<a id="get-started"></a>
<a id="quickstart-train-a-lora-adapter-in-microsoft-foundry-preview"></a>
<a id="quickstart-train-a-lora-adapter-with-a-custom-training-loop-in-interactive-post-training-preview"></a>

[!INCLUDE [Feature preview](../../includes/feature-preview.md)]

[!INCLUDE [Interactive training preview access](../../includes/interactive-training-preview-access.md)]

In this quickstart, you clone the samples repository and run a reinforcement learning (RL) recipe on GSM8K math problems. The recipe generates responses, scores their correctness, and updates a low-rank adaptation (LoRA) adapter for Qwen3.8-27B in Microsoft Foundry.

You run the Python driver locally; Foundry runs the model operations. This short run checks that training, evaluation, and checkpoint saving work. It isn't a model-quality benchmark, and you don't need a local GPU.

If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free/).

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with approved interactive-training preview access and capacity for `Qwen/Qwen3.8-27B`. Check [supported models](../overview.md#supported-models) and [regions](../overview.md#supported-regions).
- The **Foundry User** role for training, or the **Foundry Owner** role if you also deploy the fine-tuned model. See [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md).
- Python 3.11 or later, Git, and a writable local directory.
- The [Azure CLI](/cli/azure/install-azure-cli) for the sign-in command below.
- Network access to download Python packages, the public dataset, and the model's tokenizer.
- An approved budget for model loading, training, sampling, and evaluation.

## Clone the samples repository

Clone [microsoft-foundry/fine-tuning](https://github.com/microsoft-foundry/fine-tuning) and open its interactive-training cookbook:

```bash
git clone https://github.com/microsoft-foundry/fine-tuning.git
cd fine-tuning/interactive_training
```

Keep this directory open for the remaining commands. It contains the cookbook's `pyproject.toml` and Python package.

## Install the cookbook

<a id="install-and-configure"></a>

Create a virtual environment and install the cookbook. The Linux and Windows commands use the CPU Torch package index for driver-side dependencies.

# [Linux or WSL](#tab/linux)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e . \
    --index-url https://pypi.org/simple \
    --extra-index-url https://download.pytorch.org/whl/cpu
```

# [macOS](#tab/macos)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e . --index-url https://pypi.org/simple
```

# [PowerShell](#tab/powershell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e . `
    --index-url https://pypi.org/simple `
    --extra-index-url https://download.pytorch.org/whl/cpu
```

---

Reference: [Cookbook installation](https://github.com/microsoft-foundry/fine-tuning/blob/main/interactive_training/README.md#install).

Check the installation without creating a remote session:

```bash
python -m pip check
python -m interactive_training.recipes.math_rl.train_azure --help
```

Expect no broken dependencies and recipe help that lists `project_endpoint`, `max_steps`, and `max_train_examples`.

## Configure your project and sign in

Sign in with the identity approved for your project, then select its subscription:

```azurecli
az login
az account set --subscription "<subscription-id>"
```

Reference: [Sign in with Azure CLI](/cli/azure/authenticate-azure-cli-interactively).

Copy the **project endpoint** from your Foundry project. Use the project URL, not a model deployment URL or only the account hostname. Replace `<account>` and `<project>` with your project values:

# [Bash](#tab/linux+macos)

```bash
export AZURE_AI_PROJECT_ENDPOINT=\
"https://<account>.services.ai.azure.com/api/projects/<project>"
```

# [PowerShell](#tab/powershell)

```powershell
$env:AZURE_AI_PROJECT_ENDPOINT = `
    "https://<account>.services.ai.azure.com/api/projects/<project>"
```

---

The recipe uses [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential) unless `AZURE_AI_API_KEY` is set. Other configured credentials can be selected before the CLI credential. If the key variable is set, it takes precedence over your Azure CLI sign-in.

## Run the recipe

<a id="create-a-session"></a>
<a id="connect-and-run-the-loop"></a>

Run the GSM8K recipe with two training iterations, 16 training examples, and eight held-out evaluation examples. The recipe creates a session, samples responses, computes rewards, updates the adapter, and saves checkpoints.

> [!WARNING]
> This command creates a remote training session and can incur charges. `max_steps=2` limits training iterations, not model-loading time, evaluation calls, total tokens, or cost. Proceed only with an approved budget.

# [Bash](#tab/linux+macos)

```bash
python -m interactive_training.recipes.math_rl.train_azure \
    project_endpoint="$AZURE_AI_PROJECT_ENDPOINT" \
    model_name="Qwen/Qwen3.8-27B" renderer_name=qwen3_8_low_reasoning \
    env=gsm8k learning_rate=2e-5 temperature=1.0 max_tokens=1200 \
    lora_rank=32 group_size=4 groups_per_batch=8 \
    loss_fn=importance_sampling seed=42 \
    max_steps=2 max_train_examples=16 max_test_examples=8 \
    eval_every=1 save_every=1 \
    log_path=./runs/first-math-check behavior_if_log_dir_exists=raise
```

# [PowerShell](#tab/powershell)

```powershell
python -m interactive_training.recipes.math_rl.train_azure `
    project_endpoint="$env:AZURE_AI_PROJECT_ENDPOINT" `
    model_name="Qwen/Qwen3.8-27B" renderer_name=qwen3_8_low_reasoning `
    env=gsm8k learning_rate=2e-5 temperature=1.0 max_tokens=1200 `
    lora_rank=32 group_size=4 groups_per_batch=8 `
    loss_fn=importance_sampling seed=42 `
    max_steps=2 max_train_examples=16 max_test_examples=8 `
    eval_every=1 save_every=1 `
    log_path=.\runs\first-math-check behavior_if_log_dir_exists=raise
```

---

Reference: [Math RL recipe quickstart](https://github.com/microsoft-foundry/fine-tuning/blob/main/interactive_training/docs/quickstart.md).

The recipe uses `key=value` arguments, not `--key value`. Keep the terminal and network connection open until the run finishes.

Each iteration uses eight prompts with four responses per prompt. `max_tokens=1200` provides a completion budget for reasoning and the final answer; responses can still be truncated.

Results go in the `first-math-check` directory under `runs`. The command refuses to overwrite an existing directory. Choose a new `log_path` for another independent run; don't delete your results to work around an error.

## Check what succeeded

<a id="inspect-the-results"></a>

Look in **`./runs/first-math-check/`**, relative to the cookbook directory:

| Stage | Evidence | What it proves |
| --- | --- | --- |
| Launcher setup | `run_meta.json` is written; session ID might initially be `null`. | Local setup starts, **not** that Azure admits the session. |
| Model loaded | Console `Session ready: session_id=...`; `azure.session_id` is updated. | Session creation completes. |
| Loop running | `config.json`, `metrics.jsonl`, training metrics, and trajectory HTML. | Sampling, grading, and update operations are progressing. |
| Saved state | `checkpoints.jsonl` has saved `state_path`/`sampler_path` entries. | Save operations complete; don't rely on a checkpoint name printed before the save finishes. |
| Normal completion | `final` ledger row after trained batches, final held-out metrics, and successful process exit. | The bounded workflow completes; inspect warnings and verify cleanup separately. |

For this fresh synchronous GSM8K run, the initial evaluation occurs before the first update; the final evaluation follows the final save. Check `test/env/all/correct` and `test/env/all/total_episodes`; inspect any dropped-evaluation warnings. A zero score can be a real failure of formatting or token budget even when infrastructure works. Missing metrics aren't a zero score.

There is **no required accuracy gain or promised runtime** for this two-step check. To claim improvement, use a fixed held-out set and the [evaluation guide](https://github.com/microsoft-foundry/fine-tuning/blob/main/interactive_training/docs/evaluation-and-inference.md).

View the local artifacts:

```bash
python dashboard_server.py --root ./runs
# Open http://127.0.0.1:8000/
```

Reference: [Run dashboard](https://github.com/microsoft-foundry/fine-tuning/blob/main/interactive_training/docs/dashboard.md).

Keep the dashboard on its default loopback address because it has no authentication and can display prompts and responses. Press **Ctrl+C** in the dashboard terminal to stop it; this doesn't unload your remote training session.

## Clean up resources

The recipe attempts to close its training session when the loop exits. Check for cleanup warnings; a printed `Session closed` message alone doesn't confirm that remote compute is released.

Use the recorded session ID and the [sample session-management guide](https://github.com/microsoft-foundry/fine-tuning/blob/main/interactive_training/docs/session-management.md#inspect-a-single-session) to inspect your session. If it remains active, preserve required checkpoints and unload only your owned session.

Keep your configuration, metrics, and checkpoint references for recovery. Deleting local files doesn't release remote compute. This recipe doesn't create a serving deployment.

## Try other recipes

After completing this quickstart, try other recipes in the [fine-tuning samples repository](https://github.com/microsoft-foundry/fine-tuning). The interactive-training cookbook includes examples for supervised fine-tuning, preference optimization, distillation, and other RL tasks.

Follow each recipe's setup and dataset instructions. Confirm model access and an approved budget before starting another run.

## Related content

- [Interactive training overview](overview.md).
- [Key concepts for interactive training](concepts.md).
- [SDK cheatsheet](sdk-cheatsheet.md).
- [Fine-tuning samples on GitHub](https://github.com/microsoft-foundry/fine-tuning).
