---
title: include file
description: include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/04/2026
ms.custom: include, doc-kit-assisted
ai-usage: ai-assisted
---

The shell tool runs commands in a full terminal environment as part of a **Responses API** call. Use it to run scripts, work with files, and execute programs. The shell tool supports two execution modes:

- **Hosted shell**: Azure OpenAI provisions and manages a sandboxed container for the request.
- **Local shell**: You execute the model's `shell_call` actions in your own runtime and return the results.

You can access the shell tool through the Responses API only. It's not available through the Chat Completions API.

> [!IMPORTANT]
> Running arbitrary shell commands can be dangerous. Always sandbox execution, apply allowlists or denylists where possible, and log tool activity for auditing.

> [!NOTE]
> The shell tool requires an Azure OpenAI API version that supports it, and a model deployment that supports the Responses API. Confirm support for your target API version before you deploy to production.

## Prerequisites

- An Azure OpenAI model deployed that supports the Responses API and the shell tool.
- An authentication method:
  - API key, or
  - Microsoft Entra ID.
- Install the client library for your language:
  - **Python**: `pip install openai azure-identity`
  - **JavaScript/TypeScript**: `npm install openai @azure/identity`
  - **Java**: Add `com.openai:openai-java` and `com.azure:azure-identity` to your project.
- For REST examples, set `AZURE_OPENAI_API_KEY` (API key flow) or `AZURE_OPENAI_AUTH_TOKEN` (Microsoft Entra ID flow).

## Run your first command with hosted shell

Hosted shell is the fastest way to get started. Set the environment to `container_auto` to let Azure OpenAI provision and manage a container for the request. The model decides whether to call the tool based on your prompt.

In the examples that follow, replace `gpt-5.5` with the name of your own model deployment.

# [Python](#tab/python)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

# Create the client against the Azure OpenAI v1 endpoint.
openai = OpenAI(base_url=endpoint, api_key=token_provider)

# Run a command in an auto-provisioned hosted container.
response = openai.responses.create(
    model="gpt-5.5",
    tools=[{"type": "shell", "environment": {"type": "container_auto"}}],
    input="Run: python --version && echo 'hello from the shell'",
)

print(response.output_text)
```

# [JavaScript](#tab/javascript)

```javascript
import { OpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);

// Create the client against the Azure OpenAI v1 endpoint.
const openai = new OpenAI({ baseURL: endpoint, apiKey: await tokenProvider() });

// Run a command in an auto-provisioned hosted container.
const response = await openai.responses.create({
  model: "gpt-5.5",
  tools: [{ type: "shell", environment: { type: "container_auto" } }],
  input: "Run: python --version && echo 'hello from the shell'",
});

console.log(response.output_text);
```

# [Java](#tab/java)

```java
import com.azure.identity.AuthenticationUtil;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.ContainerAuto;
import com.openai.models.responses.FunctionShellTool;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

public class ShellExample {
    public static void main(String[] args) {
        String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

        // Create the client against the Azure OpenAI v1 endpoint.
        OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
            .baseUrl(endpoint)
            .credential(BearerTokenCredential.create(
                AuthenticationUtil.getBearerTokenSupplier(
                    new DefaultAzureCredentialBuilder().build(),
                    "https://ai.azure.com/.default")))
            .build();

        // Run a command in an auto-provisioned hosted container.
        FunctionShellTool shellTool = FunctionShellTool.builder()
            .environment(ContainerAuto.builder().build())
            .build();

        ResponseCreateParams params = ResponseCreateParams.builder()
            .model("gpt-5.5")
            .input("Run: python --version && echo 'hello from the shell'")
            .addTool(shellTool)
            .build();

        Response response = openAIClient.responses().create(params);
        response.output().forEach(item -> item.message().ifPresent(msg ->
            msg.content().forEach(content -> content.outputText().ifPresent(
                t -> System.out.println(t.text())))));
    }
}
```

# [REST](#tab/rest)

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
    "model": "gpt-5.5",
    "tools": [
      { "type": "shell", "environment": { "type": "container_auto" } }
    ],
    "input": "Execute: ls -lah /mnt/data && python --version"
    }'
```

---

> [!TIP]
> These examples use Microsoft Entra ID. To use an API key instead, set `api_key` to your key value (Python and JavaScript), pass `AzureApiKeyCredential` when you build the client (Java), or send the `api-key` header instead of `Authorization: Bearer` (REST).

Reference: [Use the Azure OpenAI Responses API](../how-to/responses.md) | [OpenAI Python SDK](https://github.com/openai/openai-python) | [OpenAI Node SDK](https://github.com/openai/openai-node) | [OpenAI Java SDK](https://github.com/openai/openai-java)

## Hosted runtime details

The hosted container provides a managed Linux environment for each request or container session:

- The runtime is based on `Debian 12` and might change over time.
- The default working directory is `/mnt/data`. This directory is always present and is the supported path for user-downloadable artifacts.
- Python `3.11` is preinstalled.
- Hosted shell doesn't support interactive TTY sessions, and commands don't run with `sudo`.
- Hosted containers don't have outbound network access.

You can run services inside the container when your workflow needs them.

## Reuse a container across requests

For iterative workflows, create a container once and reference it in later Responses API calls. The container keeps files and state between requests while it's active.

First, create the container.

# [Python](#tab/python)

```python
# Create a reusable container.
container = openai.containers.create(
    name="analysis-container",
    expires_after={"anchor": "last_active_at", "minutes": 20},
)

print(container.id)
```

# [REST](#tab/rest)

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/containers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
    "name": "analysis-container",
    "expires_after": { "anchor": "last_active_at", "minutes": 20 }
    }'
```

---

Then reference the container by ID in a shell request.

# [Python](#tab/python)

```python
# Reference the existing container in a shell request.
response = openai.responses.create(
    model="gpt-5.5",
    tools=[{
        "type": "shell",
        "environment": {
            "type": "container_reference",
            "container_id": container.id,
        },
    }],
    input="List files in the container and show disk usage.",
)

print(response.output_text)
```

# [REST](#tab/rest)

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
    "model": "gpt-5.5",
    "tools": [
      {
        "type": "shell",
        "environment": {
          "type": "container_reference",
          "container_id": "<container_id>"
        }
      }
    ],
    "input": "List files in the container and show disk usage."
    }'
```

---

> [!NOTE]
> The JavaScript SDK uses the same pattern: call `openai.containers.create(...)`, then pass `{ type: "container_reference", container_id }` in the shell environment.

To continue work in the same container across turns, pass the same `container_id` and the `previous_response_id` from the prior response.

## Run commands in local shell mode

In local shell mode, you execute the model's commands in your own runtime instead of a hosted container. Use this mode when you need full control over the execution environment, filesystem access, or existing internal tooling.

Set the environment to `local`. The model returns `shell_call` items that describe the commands to run.

```python
response = openai.responses.create(
    model="gpt-5.5",
    instructions="The local shell environment is on Linux.",
    input="Find the largest PDF file in the current directory.",
    tools=[{"type": "shell", "environment": {"type": "local"}}],
)

print(response.model_dump_json(indent=2))
```

When you receive `shell_call` items, run the requested commands, capture the output, and return the results as `shell_call_output` in your next request. The following executor captures `stdout`, `stderr`, and the exit outcome, and handles timeouts.

```python
import subprocess
from dataclasses import dataclass

@dataclass
class CmdResult:
    stdout: str
    stderr: str
    exit_code: int | None
    timed_out: bool

def run_command(cmd: str, timeout: float = 60) -> CmdResult:
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    )
    try:
        out, err = process.communicate(timeout=timeout)
        return CmdResult(out, err, process.returncode, False)
    except subprocess.TimeoutExpired:
        process.kill()
        out, err = process.communicate()
        return CmdResult(out, err, process.returncode, True)
```

Reference: [Use the Azure OpenAI Responses API](../how-to/responses.md)

## Shell output in responses

Hosted shell and local shell use the same output item types. Each shell run is represented by a pair of items:

- `shell_call`: the commands the model requests.
- `shell_call_output`: the command output and exit outcome.

The model requests commands with a `shell_call` item:

```json
{
  "type": "shell_call",
  "call_id": "call_<id>",
  "action": {
    "commands": ["ls -l"],
    "timeout_ms": 120000,
    "max_output_length": 4096
  },
  "status": "in_progress"
}
```

You return results with a `shell_call_output` item:

```json
{
  "type": "shell_call_output",
  "call_id": "call_<id>",
  "max_output_length": 4096,
  "output": [
    {
      "stdout": "...",
      "stderr": "",
      "outcome": { "type": "exit", "exit_code": 0 }
    }
  ]
}
```

If a `shell_call` includes `max_output_length`, include the same value on the `shell_call_output`. If a command exceeds your execution timeout, return a `timeout` outcome and include any partial output you captured.

## Download artifacts

Hosted shell can produce downloadable files. To retrieve artifacts, write them under `/mnt/data`, then download them by using the same container and files APIs used by Code Interpreter.

## Data retention and container lifecycle

- A hosted container session ends after 20 minutes of idle time.
- A hosted container is deleted one hour after it's created. All data stored in the container is removed when the container is deleted.

Hosted containers might write temporary application state to the container filesystem (backed by ephemeral block storage) while the container is active. Container data is deleted when the container expires or you delete it.

## Handle common errors

- **Timeouts**: If a command exceeds your execution timeout, return a `timeout` outcome and include any partial output you captured.
- **Truncated output**: When `max_output_length` is present on a `shell_call`, set the same value on the `shell_call_output`.
- **Interactive commands**: Shell tool execution is non-interactive. Don't rely on commands that prompt for input.
- **Non-zero exits**: Preserve output from non-zero exits so the model can reason about recovery steps.

## Related content

- [Use skills with the Responses API](../how-to/skills.md)
- [Use the Azure OpenAI Responses API](../how-to/responses.md)
- [Web search with the Responses API](../how-to/web-search.md)
