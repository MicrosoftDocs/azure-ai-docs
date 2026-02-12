---
title: Codex with Azure OpenAI in Microsoft Foundry Models
description: Learn how to use the Codex CLI and the Codex extension for Visual Studio Code with Azure OpenAI in Microsoft Foundry Models.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 12/04/2025
author: mrbullwinkle    
ms.author: mbullwin
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---


# Codex with Azure OpenAI in Microsoft Foundry Models

OpenAI’s [Codex CLI](https://github.com/openai/codex) is the same coding agent that powers ChatGPT’s Codex. You can run this coding agent entirely on Azure infrastructure, while keeping your data inside your compliance boundary with the added advantages of enterprise-grade security, private networking, role-based access control, and predictable cost management. Codex is more than a chat with your code agent – it's an asynchronous coding agent that can be triggered from your terminal, VS Code, or from a GitHub Actions runner. Codex allows you to automatically open pull requests, refactor files, and write tests with the credentials of your Foundry project and Azure OpenAI deployments.

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- Contributor permissions in [Microsoft Foundry](https://ai.azure.com/).
- `homebrew` (macOS) or Node.js with `npm` for installing the Codex CLI. See [Downloading and installing Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).
- For Windows, install and configure WSL2. See [Install WSL](https://learn.microsoft.com/windows/wsl/install).

| Requirements      | Details      |
|-------------------|--------------|
| Operating systems |macOS 12+, Ubuntu 20.04+/Debian 10+, or Windows 11 via WSL2 |
| Git (optional, recommended) | 2.23+ for built-in pull request helpers |
| RAM | 4-GB minimum (8-GB recommended) |

## Deploy a model in Foundry

1. Go to [Foundry](https://ai.azure.com) and create a new project.
2. From the [model catalog](https://ai.azure.com/catalog/) select a [reasoning model](./reasoning.md) such as `gpt-5.1-codex-max`, `gpt-5.1-codex`, `gpt-5.1-codex-mini`, [`gpt-5-codex`](https://ai.azure.com/catalog/models/gpt-5-codex), [`gpt-5`](https://ai.azure.com/catalog/models/gpt-5), [`gpt-5-mini`](https://ai.azure.com/catalog/models/gpt-5-mini), or [`gpt-5-nano`](https://ai.azure.com/catalog/models/gpt-5-nano).
3. To deploy the model from the model catalog select **Use this model**, or if using the Azure OpenAI **Deployments** pane select **deploy model**.
4. Copy the endpoint **URL** and the **API Key**.

## Install the Codex CLI

From the terminal, run the following commands to install [Codex CLI](https://github.com/openai/codex)

# [npm](#tab/npm)

```bash
npm install -g @openai/codex
codex --version # verify installation
```

# [brew](#tab/brew)

```bash
brew install --cask codex
codex --version # verify installation
```

If Homebrew can't find the package, follow the latest installation instructions in the [Codex CLI repository](https://github.com/openai/codex).

---

## Create and configure config.toml

1. In order to use Codex CLI with Azure, you need to create and set up a `config.toml` file.

    The config.toml file needs to be stored in the `~/.codex` directory. Create a `config.toml` file inside this directory or edit the existing file if it already exists:

    ```bash
    cd ~/.codex
    nano config.toml
    ```

2. Copy the text below to use the [v1 Responses API](./responses.md). With the [v1 API](../api-version-lifecycle.md) you no longer need to pass api-version, but you must include /v1 in the `base_url` path. You can't pass your API key as a string directly to `env_key`. `env_key` must point to an environment variable. Update your `base_url` with your resource name:

    ```text
    model = "gpt-5-codex"  # Replace with your actual Azure model deployment name
    model_provider = "azure"
    model_reasoning_effort = "medium"
    
    [model_providers.azure]
    name = "Azure OpenAI"
    base_url = "https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1"
    env_key = "AZURE_OPENAI_API_KEY"
    wire_api = "responses"
    ```

3. Once you have saved the updates to your `config.toml` file return to the terminal and create an instance of the environment variable that is referenced in your config file.  

    ```bash
    # Linux, macOS, or WSL 
    export AZURE_OPENAI_API_KEY="<your-api-key>"
    ```

4. Now run one of the following commands in the terminal to test if your Codex CLI configuration was successful:

    |Command| Purpose|
    |----|----|
    | codex | Launch interactive Terminal User Interface (TUI) |
    | codex "Initial prompt" | Launch TUI with an initial prompt |
    | codex exec "Initial prompt" | Launch TUI in non-interactive "automation mode" |

## Use codex in Visual Studio Code

You can also use Codex directly inside Visual Studio Code when using the [OpenAI Codex extension](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt)

1. If you don't already have Visual Studio Code, you can install it for [macOS](https://code.visualstudio.com/docs/setup/mac) and [Linux](https://code.visualstudio.com/docs/setup/linux).
2. Install the [OpenAI Codex extension](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt). The extension relies on your `config.toml` file that was configured for Codex CLI.
3. If you are in a new terminal session setup the environment variable for `AZURE_OPENAI_API_KEY`:

    ```bash
    export OPENAI_API_KEY="<your-azure-api-key-here>"
    ```

    > [!NOTE]
    > If you use WSL, also set the same environment variable on the Windows host so the extension can read it when needed.

4. Launch VS Code from the same Terminal session. (Launching from an app launcher can result in your API key environment variable not being available to the Codex extension.)

    ```bash
    code .
    ```

5. You'll now be able to use Codex in Visual Studio Code to chat, edit, and preview changes while toggling between three approval modes.

### Approval modes

Approval modes determine how much autonomy and interaction you want to have with Codex.

| Approval mode | Description |
|---------------|-------------|
| Chat          | To chat and plan with the model. |
| Agent         | Codex can read files, make edits, and run commands in the working directory automatically. Codex will need approval for activities outside the working directory or to access the internet. |
| Agent (full access) | All the capabilities of Agent mode without the need for step-by-step approval. Full access mode shouldn't be used without full understanding of the potential risks as well as implementing additional guardrails such as running in a controlled sandbox environment. |

> [!IMPORTANT]
> We recommend reviewing OpenAI's guidance on [Codex security](https://developers.openai.com/codex/security).

## Persistent guidance with AGENTS.md

You can give Codex extra instructions and guidance using `AGENTS.md` files. Codex looks for `AGENTS.md` files in the following places and merges them top-down, giving it context about your personal preferences, project-specific details, and the current task:

- `~/.codex/AGENTS.md`– personal global guidance.
- `AGENTS.md` at your repository’s root – shared project notes.
- `AGENTS.md` in the current working directory – subfolder/feature specifics.

For example, to help Codex understand how to write code for Foundry Agents, you could create an `AGENTS.md` in your project root with the following content, derived from the Azure AI Agents SDK documentation:

```markdown
# Instructions for working with Foundry Agents

You are an expert in the Azure AI Agents client library for Python.

## Key Concepts

- **Client Initialization**: Always start by creating an `AIProjectClient` or `AgentsClient`. The recommended way is via `AIProjectClient`.
- **Authentication**: Use `DefaultAzureCredential` from `azure.identity`.
- **Agent Creation**: Use `agents_client.create_agent()`. Key parameters are `model`, `name`, and `instructions`.
- **Tools**: Agents use tools to perform actions like file search, code interpretation, or function calls.
  - To use tools, they must be passed to `create_agent` via the `tools` and `tool_resources` parameters or a `toolset`.
  - Example: `file_search_tool = FileSearchTool(vector_store_ids=[...])`
  - Example: `code_interpreter = CodeInterpreterTool(file_ids=[...])`
  - Example: `functions = FunctionTool(user_functions)`

## Example: Creating a basic agent

\`\`\`python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# 1. Create Project Client
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# 2. Get Agents Client
with project_client:
    agents_client = project_client.agents

    # 3. Create Agent
    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-helpful-agent",
        instructions="You are a helpful agent that can answer questions.",
    )
    print(f"Created agent with ID: {agent.id}")
\`\`\`

```

In the previous example backticks in the Python code block are escaped to allow proper rendering. The `\`'s can be removed.

## Experiment with Codex CLI

Launch codex with the following initial prompt:

```bash
codex "write a python script to create an Azure AI Agent with file search capabilities"
```

Other suggested tests:

```markdown
# generate a unit test for src/utils/date.ts
```

```markdown
# refactor this agent to use the Code Interpreter tool instead
```

## Codex in GitHub Actions

Codex can execute as part of your continuous integration (CI) pipeline. Store your API key in the repository’s secret store as `AZURE_OPENAI_KEY` and add a job like this to automatically update your changelog before a release:

```yaml
jobs:
  update_changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Update changelog via Codex
        run: |
          npm install -g @openai/codex
          export AZURE_OPENAI_API_KEY="${{ secrets.AZURE_OPENAI_KEY }}" 
          codex -p azure exec --full-auto "update CHANGELOG for next release"
```

## Troubleshooting

|Symptom | Solution  |
|--------|-----------|
| `401 Unauthorized` or `403 Forbidden` | Export your AZURE_OPENAI_API_KEY environment variable correctly. Confirm that your key has project/deployment access. <br> Make sure you aren't passing the API Key as a string directly to the `env_key` in the `config.toml` file. You must pass a valid environment variable.    |
| `ENOTFOUND`, `DNS error`, or `404 Not Found` |Verify `base_url` in `config.toml` uses your resource name, correct domain, and contains `/v1`. <br> For example, `base_url = "https://<your-resource>.openai.azure.com/openai/v1"`.|
| CLI ignores Azure settings | Open `~/.codex/config.toml` and ensure: <br> - `model_provider = "azure"` is set. <br> - The `[model_providers.azure]` section exists. <br> - `env_key = "AZURE_OPENAI_API_KEY"` matches your environment variable name. |
| Entra ID support | Entra ID support is currently not available for Codex. |
| `401 Unauthorized` only with the WSL + VS Code Codex extension | When running VS Code from inside WSL with the Codex extension the extension may check for the API key environment variable on the local windows host rather than within the terminal shell that launched VS Code. To mitigate this issue, set the environment variable on the local windows host as well, then launch a new terminal from WSL and launch VS Code with `code .`.|
