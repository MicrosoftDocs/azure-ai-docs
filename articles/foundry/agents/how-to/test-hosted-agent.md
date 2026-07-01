---
title: "Test a hosted agent"
description: "Validate a Microsoft Foundry hosted agent with unit tests, local integration tests, deployed invoke tests, and structured azd evaluations."
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

# Test a hosted agent


[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Test your hosted agent at different levels, from unit testing individual components to end-to-end integration testing against a deployed Microsoft Foundry agent. You also learn when to use structured `azd ai agent eval` runs instead of ad hoc invoke testing.

## Prerequisites

- An initialized hosted agent project with agent code and tests. To create a project, see [Initialize an agent project](init-agent-project.md).
- The azd Foundry extensions installed. For installation steps, see [Install the azd Foundry extensions](install-cli-foundry-extensions.md).
- An authenticated Azure Developer CLI session. Run `azd auth login` if needed.
- Required test tooling for your language, such as pytest for Python or xUnit for .NET.
- For deployed integration tests and structured evaluations, a deployed hosted agent. To deploy one, see [Deploy a hosted agent](deploy-hosted-agent.md).

## Choose a testing level

| Level | What you test | Tools | Speed |
|-------|---------------|-------|-------|
| **Unit tests** | Agent logic, tool handlers, prompt formatting | pytest / xUnit | Fast (seconds) |
| **Local integration** | Full agent running locally against real models | `azd ai agent run` + `invoke --local` | Medium (seconds per request) |
| **Deployed integration** | Agent running on Foundry infrastructure | `azd ai agent invoke` | Slower (includes network round-trip) |
| **Structured eval** | Score the agent against a dataset with adaptive evaluators | `azd ai agent eval` | Slower (LRO) |

## Unit test agent logic

Test your agent's core logic without running the full server or calling external models.

### [Python](#tab/python)

```python
# test_agent.py
import pytest
from unittest.mock import MagicMock

def test_tool_handler_returns_expected_format():
    """Test that your tool handler returns valid output."""
    from my_agent.tools import weather_tool

    result = weather_tool("Seattle")
    assert "temperature" in result
    assert isinstance(result["temperature"], (int, float))

def test_system_prompt_includes_required_context():
    """Verify system prompt contains key instructions."""
    from my_agent.config import SYSTEM_PROMPT

    assert "helpful assistant" in SYSTEM_PROMPT.lower()
    assert "weather" in SYSTEM_PROMPT.lower()
```

```bash
pytest test_agent.py
```

### [C#](#tab/csharp)

```csharp
// AgentTests.cs
using Xunit;

public class AgentTests
{
    [Fact]
    public void ToolHandler_ReturnsExpectedFormat()
    {
        var result = WeatherTool.GetWeather("Seattle");
        Assert.Contains("temperature", result.Keys);
    }

    [Fact]
    public void SystemPrompt_IncludesRequiredContext()
    {
        Assert.Contains("helpful assistant",
            AgentConfig.SystemPrompt, StringComparison.OrdinalIgnoreCase);
    }
}
```

```bash
dotnet test
```

---

## Run local integration tests

Test your full agent locally, including model calls and protocol handling.

### Test manually with invoke

1. Start the agent in one terminal and send test messages in another:

   ```bash
   # Terminal 1: Start the agent
   azd ai agent run

   # Terminal 2: Send test messages
   azd ai agent invoke --local "What's the weather in Seattle?"
   azd ai agent invoke --local "Can you summarize this document?" -f test-doc.json
   ```

### Test with curl

1. For repeatable tests, use curl or any HTTP client:

   ```bash
   # Check the readiness probe (expects HTTP 200)
   curl -i http://localhost:8088/readiness

   # Test the responses protocol
   curl -s -X POST http://localhost:8088/responses \
     -H "Content-Type: application/json" \
     -d '{"input": "Hello, what can you do?"}' | jq .

   # Test with a specific session
   curl -s -X POST http://localhost:8088/responses \
     -H "Content-Type: application/json" \
     -d '{"input": "Follow up question", "metadata": {"session_id": "test-session-1"}}' | jq .
   ```

### Automate local tests

Wrap local integration tests in a script that starts the agent, runs tests, and cleans up.

```bash
#!/bin/bash
# test-integration.sh

# Start agent in background
azd ai agent run --port 9090 &
AGENT_PID=$!
sleep 5  # Wait for startup

# Run tests
RESPONSE=$(curl -s -X POST http://localhost:9090/responses \
  -H "Content-Type: application/json" \
  -d '{"input": "Say hello"}')

echo "$RESPONSE" | jq -e '.output' > /dev/null
if [ $? -eq 0 ]; then
  echo "[x] Basic invoke test passed"
else
  echo "[!] Basic invoke test failed"
  echo "$RESPONSE"
fi

# Cleanup
kill $AGENT_PID
```

## Run deployed integration tests

After deploying to Foundry, verify the agent works end to end.

```bash
# Deploy
azd up

# Test basic invoke
azd ai agent invoke "Hello, what can you do?"

# Test with a new session
azd ai agent invoke --new-session "Start a fresh conversation"

# Test with file input
azd ai agent invoke -f test-request.json
```

## Run structured evaluations

Once your agent does something interesting, ad hoc `invoke` calls stop being a reliable signal. You changed a prompt or swapped a tool, ran a couple of prompts, and now you need to decide whether that change was a net win. `azd ai agent eval` is the structured path beyond ad hoc invoke testing: it runs your agent against a fixed dataset and scores the responses with one or more evaluators, so the same change can be measured the same way every time.

### Choose structured evaluation

Use structured evaluation when:

- You changed a prompt, tool, or model and want to know whether the change helped or hurt.
- More than one person is editing the agent and informal smoke tests no longer cover enough surface area.
- You want a quality gate you can wire into CI to catch regressions automatically.

### Initialize evaluation assets

- Run this command once after the agent is deployed, typically right after your first `azd up`:

   ```bash
   azd ai agent eval generate
   ```

   This is a long-running operation that takes several minutes. It generates a tiny smoke dataset, a default adaptive evaluator scoped to your agent's behavior, and a runnable `eval.yaml`. Pass `--reset-defaults` to overwrite an existing config.

### Run an evaluation

- Once `eval.yaml` exists, run the eval and review the results:

   ```bash
   azd ai agent eval run
   azd ai agent eval show --eval-run-id <run-id>
   ```

   `eval run` resolves `eval.yaml` in the agent project root by default and reports per-evaluator scores so you can see exactly where the agent regressed. Use `--config <file>` to point at a specific recipe and `--no-wait` to submit and detach. Check run history and details with `eval show`.

### Promote to a shared suite

The recommended end state is to promote a working local recipe into a project-shared, versioned suite with `azd ai agent eval suites` and run that suite as a CI quality gate. That subcommand isn't yet generally available. Until it ships, version your `eval.yaml` in source control alongside the agent code, and run it from CI with `azd ai agent eval run --config eval.yaml`.

## Validate before production

Use this checklist when validating your agent before production:

- [ ] Agent starts without errors (`azd ai agent run`)
- [ ] Readiness probe returns 200 (`curl localhost:8088/readiness`)
- [ ] Basic invoke returns a valid response
- [ ] Agent handles invalid input gracefully (doesn't crash)
- [ ] Agent responds within acceptable time limits
- [ ] Session persistence works (multi-turn conversation)
- [ ] Deployed agent responds (`azd ai agent invoke` without `--local`)
- [ ] Logs show expected behavior (`azd ai agent monitor --follow`)

## Related content

- [Run a hosted agent locally with the Azure Developer CLI](run-hosted-agent-locally.md) for local development setup.
- [Debug a hosted agent](debug-hosted-agent.md) to diagnose issues when tests fail.
- [Monitor hosted agent logs with the Azure Developer CLI](monitor-hosted-agent-logs.md) to inspect runtime behavior.
