---
title: "Diagnose a project with agent doctor"
description: "Run azd ai agent doctor to check Microsoft Foundry hosted agent project health before eval, optimize, deploy, or troubleshooting."
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

# Diagnose a project with agent doctor

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

`azd ai agent doctor` runs a sequence of local and remote checks against your current Microsoft Foundry azd project and reports the results. Use it to recover after losing terminal context, hitting a confusing error, or picking a project back up after a break.

## Prerequisites

- An initialized hosted agent project. To create one, see [Initialize an agent project](init-agent-project.md).
- The azd Foundry extensions installed. For installation steps, see [Install the azd Foundry extensions](install-cli-foundry-extensions.md).
- An authenticated Azure Developer CLI session. Run `azd auth login` if needed.
- For remote checks, an azd environment that resolves to a Foundry project endpoint. For context resolution, see [Understand azd project context](cli-project-context.md).

## Choose when to run doctor

Run `doctor` when:

- You came back to a project after a few days and forgot where you left off.
- A command failed with a confusing error and you want a structured view of what is set up versus missing.
- You want to confirm that azd, your Foundry project endpoint, your role assignments, and your deployed agent are all in a healthy state before kicking off a long-running operation such as eval, optimize, or deploy.

`doctor` doesn't change any state. It only reads.

## Review checked areas

Each invocation runs a set of checks, including but not limited to:

- **Local**: azd version; `agent.yaml` is present and parseable; `azure.yaml` declares an `azure.ai.agent` service; `.env` for the active azd env has the expected keys; container build prerequisites are present for container deploy; entry point and runtime are valid for code deploy.
- **Remote**: the Foundry project endpoint resolves and is reachable; required role assignments exist on the project; the deployed agent, if any, exists and can be invoked; the model deployment referenced by `agent.yaml` exists.

Each check reports `pass`, `fail`, or `skip`. When every executed check passes, the report also suggests the next command to run, such as `azd ai agent eval generate`.

## Interpret exit codes

| Exit code | Meaning |
|-----------|---------|
| `0` | At least one check passed and no checks failed. |
| `1` | At least one check failed. |
| `2` | All checks were skipped, for example when preconditions aren't met. |

These exit codes are stable enough to use in CI. A `doctor` step before `azd up` can fail fast if the runner is missing role assignments or environment variables.

## Choose useful flags

| Flag | Description |
|------|-------------|
| `--local-only` | Skip remote, network-dependent checks. Use when offline, behind a proxy, or for a fast local triage. |
| `--unredacted` | Show raw principal IDs, scope ARNs, and UPNs in the report. By default, sensitive identifiers are redacted in console output. |

## Run doctor

1. Run the full diagnostic, local plus remote:

   ```bash
   azd ai agent doctor
   ```

1. Run a fast triage while offline by skipping remote checks:

   ```bash
   azd ai agent doctor --local-only
   ```

1. Show raw identifiers in the report when sharing with support:

   ```bash
   azd ai agent doctor --unredacted
   ```

## Fix failures

Use this common loop when something is wrong:

1. Run `azd ai agent doctor` and read the failed checks.
1. Fix the first failed check, such as adding a missing role assignment, setting a missing environment variable, or rerunning `azd auth login`.
1. Rerun `azd ai agent doctor` until everything passes.
1. Follow the "next step" suggestion at the bottom of the report.

## Related content

- [Debug a hosted agent](debug-hosted-agent.md) for broader troubleshooting tactics.
- [Run a hosted agent locally with the Azure Developer CLI](run-hosted-agent-locally.md) to validate local startup.
- [Understand azd project context](cli-project-context.md) for endpoint resolution used by remote checks.
