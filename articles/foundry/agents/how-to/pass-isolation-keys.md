---
title: "Pass isolation keys to a hosted agent"
description: "Send Microsoft Foundry isolation keys with azd commands so hosted agent sessions, files, conversations, and logs stay partitioned."
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

# Pass isolation keys to a hosted agent


[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

You can configure Microsoft Foundry agents for header-based isolation. Each session, conversation, file, and log query must include one or more isolation header values. You learn what each azd isolation flag does and how to pass the keys through every `azd ai agent` subcommand that talks to a session.

## Prerequisites

- A deployed hosted agent that's configured for header-based isolation in Foundry. To deploy an agent, see [Deploy a hosted agent](deploy-hosted-agent.md).
- The azd Foundry extensions installed. For installation steps, see [Install the azd Foundry extensions](install-cli-foundry-extensions.md).
- An authenticated Azure Developer CLI session. Run `azd auth login` if needed.
- Isolation key values from the system or platform team that configured the agent.

> [!NOTE]
> Isolation keys are an opt-in feature of the agent. If your agent doesn't have isolation configured on the Foundry side, you can ignore these flags and every command works as before. The flags are no-ops when the agent doesn't require them.

## Understand isolation keys

A single deployed Foundry agent can serve many users from the same endpoint. Without isolation keys, every caller sees the same session catalog and the same files in `$HOME`. Isolation keys partition that state at the platform level. Requests with different keys see different sessions, different conversations, and different filesystems, even though they hit the same agent URL.

Typical scenarios include:

- **Multi-tenant SaaS.** Each tenant gets its own user isolation key. Sessions and files for tenant A are invisible to tenant B.
- **Per-user data planes.** A chat product mints a user key when a customer signs in. The customer's history and uploads are sandboxed to that key.
- **Per-thread isolation.** Within a single user, a chat key further partitions state per conversation thread, such as "support" versus "billing".

When a request omits a required isolation key, Foundry returns `403` or `404`. An existing session isn't visible to a caller without the key. The CLI surfaces this as a structured error with the platform's response code.

## Choose isolation flags

| CLI flag | HTTP header | Scope |
|----------|-------------|-------|
| `--isolation-key` | `x-session-isolation-key` | **Session ownership.** Only accepted by `sessions create` and `sessions delete`. Derived from your Entra token by default. |
| `--user-isolation-key` | `x-agent-user-isolation-key` | **Foundry user isolation.** Accepted on `invoke`, `sessions *`, `files *`, and `monitor`. Independent of session ownership. |
| `--chat-isolation-key` | `x-agent-chat-isolation-key` | **Foundry chat isolation.** Accepted on `invoke`, `sessions *`, `files *`, and `monitor`. Independent of session ownership. |

`--user-isolation-key` and `--chat-isolation-key` are passed through verbatim to Foundry. The CLI doesn't interpret their values. It only sets the headers on outgoing requests.

`--isolation-key` controls who owns the session and is therefore allowed to delete it. The CLI defaults this to a value derived from your Entra token, which is why most workflows don't need to set it explicitly. Pass it only when you create a session under a different owner, such as when scripting a per-tenant setup, and want the same caller to be able to delete it later.

> [!IMPORTANT]
> There is no generic `--header K=V` flag on `invoke`. The three flags above are the only custom headers the extension exposes. If you need to send other arbitrary headers, call the deployed endpoint with `curl` or a language SDK directly. See [Invoke a hosted agent with the Azure Developer CLI](invoke-hosted-agent.md) for the `--agent-endpoint` URL format.

## Invoke an agent with isolation headers

1. Pass the headers on every invoke. The keys can be anything your agent understands, such as a tenant ID, a hashed user ID, or a chat thread UUID:

   ```bash
   azd ai agent invoke \
     --user-isolation-key tenant-acme \
     --chat-isolation-key thread-42 \
     "Summarize the latest support tickets"
   ```

1. Pass just one key if your agent only configures one dimension of isolation:

   ```bash
   # User isolation only
   azd ai agent invoke --user-isolation-key tenant-acme "Hello"

   # Chat isolation only
   azd ai agent invoke --chat-isolation-key thread-42 "Hello"
   ```

Both flags work with every invoke mode: local (`--local`), remote, version-pinned (`--version`), and the project-free `--agent-endpoint` form.

```bash
azd ai agent invoke \
  --agent-endpoint https://my-acct.services.ai.azure.com/api/projects/my-proj/agents/my-agent/endpoint/protocols/openai/responses?api-version=v1 \
  --user-isolation-key tenant-acme \
  --chat-isolation-key thread-42 \
  "Hello!"
```

## Create and delete sessions with an ownership key

Session create and delete also accept `--isolation-key` for session ownership. By default, the CLI derives this value from your Entra token, so within a single developer's workflow you never need to set it. Set it explicitly when one identity creates a session that another identity must clean up.

```bash
# Create a session owned by a specific isolation key
azd ai agent sessions create \
  --agent-name my-agent \
  --version 3 \
  --isolation-key sk-tenant-acme

# Later, delete it with the same key
azd ai agent sessions delete sess_abc123 --isolation-key sk-tenant-acme
```

The user and chat isolation flags also apply to all four session subcommands, so a session that was created with a user key must be looked up with the same user key.

```bash
azd ai agent sessions list   --user-isolation-key tenant-acme
azd ai agent sessions show  sess_abc123 --user-isolation-key tenant-acme
```

## Use isolation keys with files and logs

The same `--user-isolation-key` and `--chat-isolation-key` flags work everywhere a session is implied. A session that lives behind isolation headers is only reachable from commands that pass the same headers.

```bash
# Upload a file into an isolated session's filesystem
azd ai agent files upload ./seed.json \
  --user-isolation-key tenant-acme \
  --chat-isolation-key thread-42

# List the files
azd ai agent files ls /data \
  --user-isolation-key tenant-acme \
  --chat-isolation-key thread-42

# Monitor that session's container logs in real time
azd ai agent monitor --follow \
  --user-isolation-key tenant-acme \
  --chat-isolation-key thread-42
```

If you forget the keys, the CLI looks at the default, unisolated session and reports "session not found" because it can't see the isolated state.

## Verify isolation headers

Use `--output raw` (`-o raw`) on `invoke` to dump the full HTTP response, including any echoed headers and the platform's response code. This is the fastest way to confirm a deployment is receiving and accepting the keys.

```bash
azd ai agent invoke \
  --user-isolation-key tenant-acme \
  --chat-isolation-key thread-42 \
  --output raw \
  "ping"
```

The output is the unmodified HTTP response, including the status line, response headers, and response body. Friendly summary lines like `Session:` and `Invocation:` are suppressed in raw mode.

Combine `--output raw` with `--debug` to also see the outgoing request being constructed, including request URL, request headers, and request body. The two flags together produce enough detail to reproduce the call with `curl`.

## Script isolation patterns

### Loop per tenant

The flags compose well with shell loops. The pattern below invokes the same prompt for every tenant in a list, sandboxing each call to that tenant's isolation key.

```bash
for tenant in acme contoso fabrikam; do
  echo "==> $tenant"
  azd ai agent invoke \
    --user-isolation-key "tenant-$tenant" \
    --output raw \
    "Daily digest" \
    > "out/$tenant.json"
done
```

### Wrap keys with environment variables

Many teams export the keys once per shell session, then let every `azd ai agent` invocation pick them up. Wrap the CLI behind a thin alias.

```bash
export USER_KEY="tenant-acme"
export CHAT_KEY="thread-42"

# A shell function that always passes the keys
function ai-invoke() {
  azd ai agent invoke \
    --user-isolation-key "$USER_KEY" \
    --chat-isolation-key "$CHAT_KEY" \
    "$@"
}

ai-invoke "Hello"
ai-invoke --new-session "Start fresh"
```

### Use keys in CI pipelines

Put the keys in CI secrets and reference them in the same way.

```yaml
- run: |
    azd ai agent invoke \
      --user-isolation-key "$USER_KEY" \
      --chat-isolation-key "$CHAT_KEY" \
      --no-prompt --output raw \
      "Run nightly summary"
  env:
    USER_KEY: ${{ secrets.AGENT_USER_KEY }}
    CHAT_KEY: ${{ secrets.AGENT_CHAT_KEY }}
```

## Troubleshoot isolation keys

| Symptom | Likely cause | What to try |
|---------|--------------|-------------|
| `403 Forbidden` on `invoke` | The agent requires isolation keys; none were passed. | Add `--user-isolation-key` and/or `--chat-isolation-key`. Confirm with `--output raw`. |
| `403 Forbidden` even though keys are set | The key values don't match the agent's isolation config. | Check the value with the platform team that configured the agent. Re-run with `--debug` to see the outgoing headers. |
| `session not found` on `monitor` / `files` / `sessions show` | Keys aren't the same as those used when the session was made. | Pass the same `--user-isolation-key` / `--chat-isolation-key` you used on the original `invoke` / `sessions create`. |
| `cannot delete session` after switching users | Session was created under a different `--isolation-key`. | Either delete from the originating shell, or recreate the session with the new owner's key. |
| Local invoke ignores the flags | Expected. Local agents don't enforce isolation. | Local mode (`--local`, `azd ai agent run`) is for development against a single user. Isolation enforcement is a remote/Foundry-side behavior. |

## Understand unsupported scenarios

- **Generic `--header K=V` flag.** Only the three isolation flags above are exposed. To send arbitrary headers, drop down to `curl` or an HTTP client targeting the URL from `azd ai agent show`.
- **Per-call isolation without the flags.** The CLI doesn't read isolation keys from env vars automatically. Pass the flags explicitly or wrap the CLI in a script as shown above.
- **Local enforcement.** `azd ai agent run` and `--local` invokes don't enforce isolation. That is a Foundry platform behavior. Test isolation with a deployed agent.

## Related content

- [Invoke a hosted agent with the Azure Developer CLI](invoke-hosted-agent.md) for every invoke variant and option.
- [Monitor hosted agent logs with the Azure Developer CLI](monitor-hosted-agent-logs.md) to stream isolated session logs.
- [Run a hosted agent locally with the Azure Developer CLI](run-hosted-agent-locally.md) to understand local behavior.
