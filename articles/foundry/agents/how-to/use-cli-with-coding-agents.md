---
title: "Use azd ai with coding agents and scripts"
description: "Run azd ai predictably from coding agents, CI jobs, MCP servers, and scripts that automate Microsoft Foundry project tasks."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/15/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Use azd ai with coding agents and scripts

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use `azd ai` from coding agents and scripts with the same behavior that humans get at a terminal. You set standalone context, disable prompts, parse JSON output, and invoke direct agent endpoints for reliable automation.

## Prerequisites

- The [azd Foundry extensions installed](install-cli-foundry-extensions.md).
- An authenticated `azd` session.
- A Microsoft Foundry project endpoint for the commands you want to run. For more information, see [Set the azd project context](cli-project-context.md).
- Optional: a deployed hosted agent when you need to invoke an agent endpoint. For setup, see [Deploy a hosted agent](deploy-hosted-agent.md).

## Start with the Microsoft Foundry Skill

Coding agents work best when they already know the `azd ai` conventions. The [Microsoft Foundry Skill](../../how-to/develop/use-microsoft-foundry-skill.md) gives a coding agent that knowledge: it generates correct `azd ai` commands and Foundry wiring, and it applies the practices in this article -- setting the project context, passing `--no-prompt`, and requesting `--output json` for structured results. Point your coding agent at the skill first, then use the patterns in the rest of this article to review and harden what it produces.

## Set the project context once

Every resource command, such as `connection`, `toolbox`, `skill`, or `routine`, needs a Foundry project endpoint to target. In automation, set that endpoint once per session, CI job, or coding-agent invocation, and then use it for the rest of the run.

There are two patterns.

### Pin once with `azd ai project set`

When you want the context to persist across shells without exporting an environment variable, set it in global config:

```bash
azd ai project set https://my-project.services.ai.azure.com/api/projects/my-project --no-prompt
azd ai project show
```

`azd ai project set <endpoint>` is fully non-interactive when you already know the URL. `azd ai project show` confirms which source resolved the active endpoint. Use it at the top of a session if you aren't sure what state the host is in.

### Set an environment variable

Set `FOUNDRY_PROJECT_ENDPOINT` in the environment where your script or coding agent runs. Every `azd ai` command automatically picks it up after the in-project azd environment and the global config.  

```bash
export FOUNDRY_PROJECT_ENDPOINT="https://my-project.services.ai.azure.com/api/projects/my-project"
azd ai connection list --output json
```

This pattern fits CI well because secrets and configuration usually arrive as environment variables already, and there's no global state to clean up between jobs.  

For the full explanation of how the CLI resolves the endpoint, including the precedence order, see [Set the azd project context](cli-project-context.md).

## Disable prompts

Every `azd ai` command accepts `--no-prompt`. When you set it, the command fails fast instead of blocking on interactive input. A missing required argument or a `delete` confirmation that would otherwise wait for a keypress becomes an immediate error with structured output.  

Always set `--no-prompt` in CI and in coding-agent invocations.

```bash
azd ai connection create my-search \
  --kind cognitive-search \
  --target https://my-search.search.windows.net \
  --auth-type api-key \
  --key "$KEY" \
  --no-prompt
```

> [!TIP]
> `--no-prompt` also implies "skip the `delete` confirmation prompt", so you don't need `--force` just to suppress that one prompt.

## Get JSON output

Most `azd ai` commands support `--output json`, including the `connection`, `toolbox`, `skill`, and `routine` resource commands and `azd ai agent show`. Use it to parse the result reliably with `jq`, `ConvertFrom-Json`, or your language's JSON parser instead of scraping the human-readable text output. The `azd ai agent invoke` command uses `--output raw` for the unmodified server response.

```bash
# List connections, extract names with jq
azd ai connection list --output json | jq -r '.[].name'

# Show a single resource as JSON
azd ai routine show daily-digest --output json | jq '.trigger'
```

```powershell
# PowerShell example
$conn = azd ai connection show my-search --output json | ConvertFrom-Json
Write-Host $conn.target
```

The text output is for humans and may change between releases. The JSON shape is the stable contract.

## Create resources idempotently

`create` isn't an upsert. If the named resource already exists, a re-run fails. This default works well for shared, project-scoped resources because it prevents one caller from silently overwriting another caller's state.

For automation that must succeed regardless of prior state, the `connection` commands accept `--force` to replace the existing resource.

```bash
azd ai connection create my-search \
  --kind cognitive-search \
  --target https://my-search.search.windows.net \
  --auth-type api-key \
  --key "$KEY" \
  --force --no-prompt
```

> [!WARNING]
> `--force` REPLACES the connection (an ARM PUT), it doesn't merge. Use it carefully on shared resources because another caller's edits to the same resource might be lost.

If you only need to change a few fields and want to preserve everything else, use `update`. Or, use the dedicated collection subcommands like `tool`, `tag`, `metadata`, and `key`.

## Create a toolbox from a file

For a multientry toolbox that bundles built-in tools, connections, and skills, put the full definition in a YAML file and pass `--from-file` to `azd ai toolbox create`. The file uses the corresponding [AgentSchema](https://github.com/microsoft/AgentSchema) shape.

```bash
azd ai toolbox create research --from-file ./resources/research-toolbox.yaml --no-prompt
```

`--from-file` is one-shot input read at invocation time. The CLI doesn't track or re-read the file, so future edits to the YAML have no effect until you rerun the command. Create connections with explicit flags (`--kind`, `--target`, `--auth-type`, and the matching credential flags), then reference them by name from the toolbox file.

## Invoke a deployed agent without an azd project

When a coding agent or script needs to call a deployed agent that lives outside its working directory, use `--agent-endpoint` to target it directly. This approach bypasses both `azure.yaml` and the active azd env. The URL alone is enough.

```bash
azd ai agent invoke \
  --agent-endpoint https://my-project.services.ai.azure.com/api/projects/my-project/agents/release-summarizer/versions/3 \
  "Summarize today's release notes." \
  --no-prompt
```

Use this shape when one repository's CI needs to call an agent owned by a different repository, or when an MCP server fronts several agents and only knows their endpoint URLs. For the full set of `invoke` options, see [Invoke a hosted agent](invoke-hosted-agent.md).

## Pass secrets to a local run

To start the agent locally with secrets, set them as `azd` environment variables and reference them in `agent.yaml`. The values live in `.azure/<env>/.env`, which is gitignored by default.

```bash
azd env set OPENAI_KEY "$AZURE_OPENAI_KEY"
```

```yaml
# agent.yaml
environment_variables:
  - name: OPENAI_KEY
    value: ${OPENAI_KEY}
```

For secrets that shouldn't live in a local `.env` file, store them in a Foundry project connection and reference them with a `${{connections.<name>.credentials.<field>}}` placeholder. See [Run a hosted agent locally](run-hosted-agent-locally.md) for the full local-run surface.

## Script a short setup

This bash script combines the patterns above. It pins the project context, creates a connection and a toolbox idempotently, wires a tool into the toolbox, and verifies the result by parsing JSON.

```bash
#!/usr/bin/env bash
set -euo pipefail

azd ai project set "$FOUNDRY_PROJECT_ENDPOINT" --no-prompt

# A 'remote-tool' connection holds the URL and credentials for the MCP server.
azd ai connection create tavily \
  --kind remote-tool \
  --target https://mcp.tavily.com/mcp \
  --auth-type custom-keys \
  --custom-key "x-api-key=$TAVILY_KEY" \
  --force --no-prompt

# Create the toolbox with the connection wired in, in a single shot
cat > research-toolbox.yaml <<'EOF'
description: Research tools
connections:
  - name: tavily
EOF

azd ai toolbox create research --from-file ./research-toolbox.yaml --no-prompt

echo "Toolbox state:"
azd ai toolbox connection list research --output json | jq .
```

`set -euo pipefail` ensures the script fails fast if any step errors out. Combined with `--no-prompt`, that gives you a deterministic exit code suitable for CI gates.

## Review endpoint resolution

Coding agents can predict which Foundry project a command will target by walking this priority order. The first source that yields a value wins; later sources aren't consulted.

1. `--project-endpoint` (or `-p`) flag (always wins).
1. Inside an azd project: the active azd env value.
1. Global config (set by `azd ai project set`).
1. `FOUNDRY_PROJECT_ENDPOINT` environment variable.
1. Error with a structured suggestion to run `azd ai project set` or pass `--project-endpoint`.

For the full explanation, including how the standalone context interacts with in-project work, see [Set the azd project context](cli-project-context.md).

## Apply coding agent tips

- Always pass `--no-prompt`, and add `--output json` on commands that support it. Together, they give you a predictable exit code plus a parseable result.
- Verify the resolved context with `azd ai project show` at the start of a session if you're uncertain what state the host is in. It's a cheap, read-only call.
- On failure, prefer parsing the structured suggestion in the error output to deciding next steps. For example, a "No Foundry project endpoint resolved" error implies you should run `azd ai project set`, or set `FOUNDRY_PROJECT_ENDPOINT`, before retrying.
- Use `--debug` only when diagnosing a problem. It produces verbose, multi-line output that's hard to parse and was never meant to be a programmatic interface.
- Treat `create` failures with "already exists" as recoverable. Rerun with `--force` if the resource is yours to replace, or switch to `update` and the collection subcommands if you only need to change part of it.

## Related content

- [Set the azd project context](cli-project-context.md) to understand how the CLI resolves the Foundry project endpoint.
- [Set up CI/CD for hosted agents with the Azure Developer CLI](set-up-ci-cd-cli.md) for patterns that run `azd ai` in pipelines.
- [Invoke a hosted agent](invoke-hosted-agent.md) for full `azd ai agent invoke` options, including `--agent-endpoint`.
