---
title: "Add guardrails to a hosted agent"
description: "Attach Responsible AI content safety and network egress guardrail policies to a hosted agent in Microsoft Foundry by using the Azure Developer CLI, the Python SDK, or the REST API."
author: amitbhave
ms.author: amitbhave
ms.manager: pranavp
ms.date: 09/21/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: references_regions, dev-focus
ai-usage: ai-assisted
# customer intent: As a developer, I want to attach content safety and network egress guardrails to my hosted agent so that the platform screens prompts and responses and governs the agent's outbound connections.
---

# Add guardrails to a hosted agent

This article shows you how to attach guardrails to a hosted agent in Microsoft Foundry. Define guardrails in a Responsible AI (RAI) policy that you reference from the agent definition. The platform applies these guardrails at runtime. This article covers two kinds of guardrails:

- **Content safety controls** screen the prompts your agent receives and the responses it returns, so harmful content is filtered according to your organization's safety configuration.
- **Network egress controls (preview)** govern the outbound connections your agent makes, so it reaches only the destinations you allow.

You reference the guardrail by its RAI policy resource ID on the agent definition. You can attach it when you deploy by using the Azure Developer CLI (`azd`), the Python SDK, or the REST API. The same attach steps apply to both kinds of guardrails. To learn what guardrails are, the risks they detect, and how to create one, see [Guardrails and controls overview](../../guardrails/guardrails-overview.md).

If your agent uses the `invocations` protocol, attaching a policy isn't enough on its own. You also declare where the text to screen lives in your request and response bodies. See [Add a guardrail to an agent that uses the invocations protocol](#add-a-guardrail-to-an-agent-that-uses-the-invocations-protocol).

## Prerequisites

* A [Microsoft Foundry project](../../how-to/create-projects.md).
* A hosted agent, or a container image ready to deploy as one. See [Deploy a hosted agent](deploy-hosted-agent.md).
* A guardrail (RAI policy) on the Foundry resource, and its full Azure Resource Manager (ARM) resource ID. To create one in the Foundry portal, see [Configure guardrails and controls](../../guardrails/how-to-create-guardrails.md). For a network egress guardrail, you can also [create the policy with `azd provision`](#add-egress-rules-by-using-the-azure-developer-cli). The ARM resource ID has this form:

    ```text
    /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account>/raiPolicies/<policy-name>
    ```

* For the Azure Developer CLI method: the `azd ai agent` extension, version 1.0.0-beta.1 or later. To configure moderation for the `invocations` protocol, use version 1.0.0-beta.12 or later.
* For the Python SDK method: the [Azure AI Projects client library](/python/api/overview/azure/ai-projects-readme) for Python, version 2.2.0 or later:

    ```bash
    pip install "azure-ai-projects>=2.2.0"
    ```

    To configure moderation for the `invocations` protocol, use version 2.7.0 or later:

    ```bash
    pip install "azure-ai-projects>=2.7.0"
    ```

## How guardrails apply to hosted agents

A hosted agent definition has an optional `rai_config` setting with a `rai_policy_name` field. Set `rai_policy_name` to the full ARM resource ID of your guardrail's RAI policy. The platform applies that policy to the agent's prompts and responses.

When you omit `rai_config`, the agent runs without a content safety guardrail. When you include `rai_config` but omit `rai_policy_name`, the platform applies the default policy, `Microsoft.DefaultV2`. Provide a custom policy when you need stricter or organization-specific filtering.

Always use the full ARM resource ID for `rai_policy_name`, not the bare policy name.

> [!WARNING]
> Don't rely on deploy-time validation to catch a bad policy ID. On many subscriptions an agent that references a policy that doesn't exist is created successfully and reports `active`, but **no content filtering is applied** - the guardrail fails open and harmful prompts reach the agent. Confirm the policy exists on the account, then [test the guardrail](#test-content-safety-filtering) before you rely on the agent's content safety.

`rai_config` is the shape the Foundry API accepts, so the Python SDK and REST examples in this article set it directly. The Azure Developer CLI doesn't expose `rai_config` in `azure.yaml`; it uses a `policies` list instead and maps it to `rai_config` when it deploys.

### Protocol differences

How much configuration a guardrail needs depends on the protocol your agent exposes:

| Protocol | Configuration |
| --- | --- |
| `responses` | Set `rai_policy_name`. The platform knows the request and response shapes, so it locates the text to screen on its own. |
| `invocations` | Set `rai_policy_name` **and** `invocations_moderation`. Request and response bodies are defined by your agent, so you declare where the text lives. |
| `invocations_ws` | Content safety moderation isn't available. |

> [!IMPORTANT]
> On the `invocations` protocol, a policy attached without `invocations_moderation` is inert. The platform has no way to find the text in your custom body shapes, so it doesn't screen anything and requests pass through unfiltered. The agent still deploys and returns `HTTP 200`, which makes the gap easy to miss.

## Add a guardrail with the Azure Developer CLI

When you use `azd`, declare the guardrail in the `policies` list on the `azure.ai.agent` service in `azure.yaml`. Add an entry with `type: rai_policy` and set `raiPolicyName` to the full ARM resource ID of the RAI policy. When you deploy, `azd` maps that entry to `rai_config.rai_policy_name` on the agent definition it sends to Foundry.

1. In your `azure.yaml`, add a `policies` list to the agent service:

    ```yaml
    services:
      my-agent:
        host: azure.ai.agent
        project: src/my-agent
        kind: hosted
        name: my-hosted-agent
        description: A hosted agent with a content safety guardrail
        policies:
          - type: rai_policy
            # Full ARM resource ID of the RAI policy on the Foundry resource.
            raiPolicyName: /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account>/raiPolicies/<policy-name>
        protocols:
          - protocol: responses
            version: "2.0.0"
    ```

1. Deploy the agent:

    ```bash
    azd deploy
    ```

The platform attaches the guardrail when it creates the agent version.

> [!NOTE]
> In `azure.yaml` the field is camelCased as `raiPolicyName`. The deprecated standalone `agent.yaml` uses the snake_case `rai_policy_name`. Both map to `rai_config.rai_policy_name` on the agent version. Don't declare the guardrail in `agent.manifest.yaml` - `azd` reads that file only during `azd ai agent init` and ignores it at deploy time.

## Add a guardrail with the Python SDK

When you create an agent version with the SDK, pass a `RaiConfig` to the `rai_config` parameter of `HostedAgentDefinition`.

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentEndpointProtocol,
    ContainerConfiguration,
    HostedAgentDefinition,
    ProtocolVersionRecord,
    RaiConfig,
)
from azure.identity import DefaultAzureCredential

# Format: "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>"
PROJECT_ENDPOINT = "your_project_endpoint"

# Full ARM resource ID of the RAI policy.
RAI_POLICY_ID = (
    "/subscriptions/<subscription-id>/resourceGroups/<resource-group>"
    "/providers/Microsoft.CognitiveServices/accounts/<account>"
    "/raiPolicies/<policy-name>"
)

credential = DefaultAzureCredential()
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=credential,
    allow_preview=True,
)

agent = project.agents.create_version(
    agent_name="my-agent",
    definition=HostedAgentDefinition(
        cpu="1",
        memory="2Gi",
        container_configuration=ContainerConfiguration(
            image="your-registry.azurecr.io/your-image:tag",
        ),
        protocol_versions=[
            ProtocolVersionRecord(
                protocol=AgentEndpointProtocol.RESPONSES, version="2.0.0"
            )
        ],
        rai_config=RaiConfig(rai_policy_name=RAI_POLICY_ID),
    ),
)

print(f"Agent created: {agent.name}, version: {agent.version}")
```

Reference: [HostedAgentDefinition](/python/api/azure-ai-projects/azure.ai.projects.models.hostedagentdefinition), [ContainerConfiguration](/python/api/azure-ai-projects/azure.ai.projects.models.containerconfiguration), and [RaiConfig](/python/api/azure-ai-projects/azure.ai.projects.models.raiconfig).

## Add a guardrail with the .NET SDK

When you create an agent version with the .NET SDK, set the `ContentFilterConfiguration` property on `HostedAgentDefinition`. Install the prerelease package with `dotnet add package Azure.AI.Projects.Agents --prerelease`.

```csharp
using System;
using Azure.AI.Projects.Agents;
using Azure.Identity;

// Format: "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>"
var projectEndpoint = "your_project_endpoint";

// Full ARM resource ID of the RAI policy.
var raiPolicyId =
    "/subscriptions/<subscription-id>/resourceGroups/<resource-group>"
    + "/providers/Microsoft.CognitiveServices/accounts/<account>/raiPolicies/<policy-name>";

AgentAdministrationClient agentsClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

var definition = new HostedAgentDefinition(
    versions: new[] { new ProtocolVersionRecord(ProjectsAgentProtocol.Responses, "2.0.0") },
    cpu: "1",
    memory: "2Gi")
{
    ContainerConfiguration = new ContainerConfiguration("your-registry.azurecr.io/your-image:tag"),
    ContentFilterConfiguration = new ContentFilterConfiguration(raiPolicyName: raiPolicyId),
};
ProjectsAgentVersion agent = agentsClient.CreateAgentVersion(
    agentName: "my-agent",
    options: new ProjectsAgentVersionCreationOptions(definition));
Console.WriteLine($"Agent created: {agent.Name}, version: {agent.Version}");
```

## Add a guardrail with the JavaScript/TypeScript SDK

When you create an agent version with the SDK, add an `rai_config` object with a `rai_policy_name` field to the hosted agent definition.

```bash
npm install @azure/ai-projects @azure/identity
```

```typescript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";

// Format: "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>"
const projectEndpoint =
  process.env["FOUNDRY_PROJECT_ENDPOINT"] || "your_project_endpoint";

// Full ARM resource ID of the RAI policy.
const raiPolicyId =
  "/subscriptions/<subscription-id>/resourceGroups/<resource-group>" +
  "/providers/Microsoft.CognitiveServices/accounts/<account>" +
  "/raiPolicies/<policy-name>";

const project = new AIProjectClient(
  projectEndpoint,
  new DefaultAzureCredential(),
);

const agent = await project.agents.createVersion("my-agent", {
  kind: "hosted",
  cpu: "1",
  memory: "2Gi",
  container_configuration: {
    image: "your-registry.azurecr.io/your-image:tag",
  },
  protocol_versions: [{ protocol: "responses", version: "2.0.0" }],
  rai_config: { rai_policy_name: raiPolicyId },
});

console.log(`Agent created: ${agent.name}, version: ${agent.version}`);
```

Reference: [AIProjectClient](/javascript/api/overview/azure/ai-projects-readme)

## Add a guardrail with the REST API

When you create the agent over REST, include a `rai_config` object in the `definition`.

```bash
BASE_URL="https://{account}.services.ai.azure.com/api/projects/{project}"
API_VERSION="v1"
TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)

curl -X POST "$BASE_URL/agents?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-agent",
    "definition": {
      "kind": "hosted",
      "image": "myacr.azurecr.io/my-agent:v1",
      "cpu": "1",
      "memory": "2Gi",
      "container_protocol_versions": [
        {"protocol": "responses", "version": "2.0.0"}
      ],
      "rai_config": {
        "rai_policy_name": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account>/raiPolicies/<policy-name>"
      }
    }
  }'
```

## Verify the guardrail is applied

Get the agent version and confirm that `rai_config.rai_policy_name` holds your policy ID.

```bash
curl -s -X GET "$BASE_URL/agents/my-agent/versions/1?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" | jq '.definition.rai_config'
```

The response includes the policy you set:

```json
{
  "rai_policy_name": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account>/raiPolicies/<policy-name>"
}
```

## Test content safety filtering

To confirm that the guardrail filters content, send a prompt that violates your safety policy to the agent's Responses endpoint. The platform screens the prompt at the input stage and rejects it before the agent runs.

```bash
curl -i -X POST "$BASE_URL/agents/my-agent/endpoint/protocols/openai/responses?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input":"<a prompt that your policy is configured to block>","store":true}'
```

A blocked prompt returns `HTTP 400` with a `content_filter` error:

```json
{
  "error": {
    "code": "content_filter",
    "message": "The request was blocked due to content safety policy violation at input stage.",
    "type": "content_safety_error"
  }
}
```

A prompt that passes the policy returns `HTTP 200` with the agent's response. If a harmful prompt isn't blocked, check in this order:

1. The policy named by `rai_policy_name` **actually exists** on the account. A nonexistent policy fails open with no error. List the policies on the account and confirm the final segment of `rai_policy_name` matches one of them:

    ```bash
    az rest --method get \
      --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account>/raiPolicies?api-version=2024-10-01" \
      --query "value[].name" -o tsv
    ```

1. The policy is configured to filter the relevant content category and severity.

The guardrail applies to streaming requests too. By using `"stream": true`, a violating prompt is rejected with the same `HTTP 400` before any event is emitted.

## Add a guardrail to an agent that uses the invocations protocol

On the `responses` protocol, the platform knows the request and response shapes, so `rai_policy_name` is all you need. The `invocations` protocol accepts request and response bodies that your agent defines, so the platform can't tell which fields hold user or agent text. Add an `invocations_moderation` object to `rai_config` that declares where the text lives.

Until you do, the policy is attached but screens nothing.

### Moderation settings

| Setting | Required | Description |
| --- | --- | --- |
| `response_mode` | Yes | The response shapes your agent can produce: `non_streaming`, `streaming`, or `both`. |
| `input_content_type` | No | How to parse the request body: `json` (default) or `text`. |
| `output_content_type` | No | How to parse the response body: `json` (default) or `text`. |
| `input_paths` | When `input_content_type` is `json` | Path expressions that select the user text in the request body. |
| `output_paths` | When `response_mode` is `non_streaming` or `both`, and `output_content_type` is `json` | Path expressions that select the agent text in a buffered response body. |
| `stream_selectors` | When `response_mode` is `streaming` or `both`, and `output_content_type` is `json` | Pairs of `event_type` and `text_field` that locate text in streamed events. |

Set `input_content_type` or `output_content_type` to `text` when that body is plain text. The platform then screens the body itself and you don't provide paths for that direction.

You can attach only one RAI policy to an agent, so `invocations_moderation` applies to that single policy.

#### Path expressions

`input_paths` and `output_paths` accept `$` for the document root, dot notation for members, array indexes, and `[*]` wildcards. For example, `$.messages[*].content` selects the `content` field of every element in the `messages` array. When a path selects several values, the platform joins them and screens them together.

#### Stream selectors

For a streamed response, the platform reads the `type` field of each event and compares it to `event_type`. On a match, it reads the field named by `text_field` and screens that text.

Both `event_type` and `text_field` are exact, case-sensitive matches against top-level properties of the event's JSON payload. You can't select a nested field.

`text_field` is a field name, not a path expression. Use `content`, not `$.content`.

An event whose `type` matches no selector, or whose `text_field` names no property, contributes no text. That event's content goes unscreened, and if no selector ever yields text, the response isn't screened at all. When you omit `text_field`, the platform uses `delta`.

#### Response modes

`response_mode` declares the shapes your agent can return. It applies only to output: input screening runs regardless of the value you set. For output, the platform inspects the response `Content-Type` and runs one check, using the streaming check for `text/event-stream` and the buffered check otherwise.

Declare every shape your agent can return. A successful response that carries content in a shape you didn't declare is rejected with `HTTP 502` rather than skipping moderation. Use `both` only when your agent genuinely answers both ways.

Output screening applies to successful responses that carry content. The platform doesn't screen error responses from your container or empty acknowledgments.

#### Limits

Content safety screening has bounds that affect large payloads:

| Limit | Behavior |
| --- | --- |
| Request body larger than 2 MB | Forwarded to your agent without input screening. |
| Buffered response body larger than 1 MB | Rejected with `HTTP 502`. The response never reaches the client. |
| Text longer than 10,000 characters in a single check | Truncated before analysis. |

The platform also forwards a request unscreened when it can't parse the body as JSON or when `input_paths` selects nothing. Confirm your paths match your real request bodies rather than assuming a deployed policy is screening them.

### Add moderation with the Azure Developer CLI

Add an `invocationsModeration` block to the `rai_policy` entry in `azure.yaml`. These settings use camel case, and `azd` maps them to the snake case names that the API accepts.

1. In your `azure.yaml`, add `invocationsModeration` to the `rai_policy` entry. This example screens the `message` field of the request. The agent streams events shaped like `{"type": "token", "content": "..."}` and a final `{"type": "done", "full_text": "..."}`.

    ```yaml
    services:
      my-agent:
        host: azure.ai.agent
        project: src/my-agent
        kind: hosted
        name: my-hosted-agent
        policies:
          - type: rai_policy
            raiPolicyName: /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account>/raiPolicies/<policy-name>
            invocationsModeration:
              responseMode: streaming
              inputPaths:
                - $.message
              streamSelectors:
                - eventType: token
                  textField: content
                - eventType: done
                  textField: full_text
        protocols:
          - protocol: invocations
            version: "2.0.0"
    ```

1. Deploy the agent:

    ```bash
    azd deploy
    ```

    The platform applies the moderation settings when it creates the agent version.

`azd` checks the block before it deploys, so a structural mistake fails locally instead of at runtime. For example, declaring moderation on an agent that doesn't expose the `invocations` protocol returns:

```output
policies[0] invocationsModeration is only supported for agents that expose the 'invocations' protocol; add it to 'protocols' or remove the moderation block
```

These checks cover structure, not meaning. `azd` can't tell whether your paths and field names match the bodies your agent actually sends, so verify that yourself with the test in [Test the moderation settings](#test-the-moderation-settings).

### Add moderation with the Python SDK

> [!NOTE]
> `invocations_moderation` requires `azure-ai-projects` version 2.7.0 or later.

Pass a `RaiInvocationModeration` object to the `invocations_moderation` parameter of `RaiConfig`.

```python
from azure.ai.projects.models import (
    RaiConfig,
    RaiInvocationMode,
    RaiInvocationModeration,
    RaiSseTextSelector,
)

rai_config = RaiConfig(
    rai_policy_name=RAI_POLICY_ID,
    invocations_moderation=RaiInvocationModeration(
        response_mode=RaiInvocationMode.STREAMING,
        input_paths=["$.message"],
        stream_selectors=[
            RaiSseTextSelector(event_type="token", text_field="content"),
            RaiSseTextSelector(event_type="done", text_field="full_text"),
        ],
    ),
)
```

Pass `rai_config` to `HostedAgentDefinition` as shown in [Add a guardrail with the Python SDK](#add-a-guardrail-with-the-python-sdk), and set `protocol_versions` to the `invocations` protocol.

### Add moderation with the REST API

Include `invocations_moderation` in the `rai_config` object of the agent definition.

```json
{
  "name": "my-agent",
  "definition": {
    "kind": "hosted",
    "image": "myacr.azurecr.io/my-agent:v1",
    "cpu": "1",
    "memory": "2Gi",
    "container_protocol_versions": [
      {"protocol": "invocations", "version": "2.0.0"}
    ],
    "rai_config": {
      "rai_policy_name": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account>/raiPolicies/<policy-name>",
      "invocations_moderation": {
        "response_mode": "streaming",
        "input_paths": ["$.message"],
        "stream_selectors": [
          {"event_type": "token", "text_field": "content"},
          {"event_type": "done", "text_field": "full_text"}
        ]
      }
    }
  }
}
```

To confirm the settings were applied, get the agent version and inspect `definition.rai_config.invocations_moderation`:

```bash
curl -s -X GET "$BASE_URL/agents/my-agent/versions/1?api-version=$API_VERSION" \
  -H "Authorization: ******" | jq '.definition.rai_config.invocations_moderation'
```

### What a blocked invocation looks like

The response to a blocked request depends on which stage the platform blocks and whether your agent streams.

A blocked request returns `HTTP 400` before your agent runs. The message ends with the request ID, which you can use when you file a support request:

```json
{
  "error": {
    "code": "content_filter",
    "message": "The request was blocked due to content safety policy violation at input stage. [Request ID: <request-id>]",
    "type": "content_safety_error"
  }
}
```

A blocked buffered response also returns `HTTP 400`, with a message that names the output stage.

A blocked streamed response is different. The platform sends response headers before it screens the agent's output, so the status stays `HTTP 200`. The platform discards the events it was holding, sends a single error event, and ends the stream:

```text
event: error
data: {"type":"error","code":"content_filter","message":"The response was blocked due to content safety policy violation."}
```

Handle this event in your client. Treat it as terminal. Earlier events might already have reached the client, so the user could see partial output before the block. A `200` status alone doesn't mean the response passed the policy.

### Test the moderation settings

To confirm your settings screen the right fields, send a request that your policy is configured to block and check that the platform blocks it:

```bash
curl -i -X POST "$BASE_URL/agents/my-agent/endpoint/protocols/invocations?api-version=$API_VERSION" \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{"message":"<a prompt that your policy is configured to block>"}'
```

If the request isn't blocked, check that:

- `input_paths` matches the field that holds the user text. A path that selects nothing means nothing is screened.
- Each `text_field` is a field name, such as `content`, rather than a path such as `$.content`.
- Each `event_type` matches the `type` value your agent sends in its streamed events.
- Your `event_type` and `text_field` values match your agent's casing exactly, and name top-level properties rather than nested ones.
- The policy filters the relevant content category and severity.

If requests fail with `HTTP 502` instead, `response_mode` probably doesn't match what your agent returns. Set it to `both` if your agent answers both ways.

## Network egress controls (preview)

> [!IMPORTANT]
> Network egress controls are in preview. They apply to hosted agents only and don't affect prompt-based agents or model deployments. Configure them by using the `2026-05-15-preview` API version of the RAI policy. Preview features are provided without a service-level agreement and are not intended to be used in production or in a live operating environment. This feature consists of tooling only. Customers are responsible for understanding the data handling practices of any endpoints receiving data.

Content safety controls screen prompts and responses. *Network egress controls* govern the **outbound** connections your hosted agent makes. You define ordered rules that allow, deny, transform, or rewrite outbound requests by destination host, and the platform enforces them inside the agent's sandbox before traffic leaves the runtime. Egress rules are stored in the same RAI policy you attach in the previous sections, so the `azd`, Python SDK, and REST API attach steps apply them automatically.

### How egress rules are evaluated

- The system evaluates rules in order, from top to bottom. The first matching rule wins.
- If no rule matches, the policy's default action applies. Set the default action to **Deny** for an allow list (recommended) or **Allow** for a deny list.
- When you apply an egress policy, the agent runtime automatically allow lists foundational domains it needs to function. A **Deny** default action doesn't block this required platform connectivity, so you don't need to add rules for it.
- Each rule matches on the request host. Wildcards such as `*.contoso.com` are supported.
- Rule actions are **Allow**, **Deny**, **Transform** (allow the request and modify its headers), and **Rewrite** (redirect the request to another destination).
- Evaluation is fail-closed: if the policy can't be evaluated, the request is denied.

### Rule limits

You can add a maximum of **480 egress rules** per policy. This limit applies to all egress rule actions: **Allow**, **Deny**, **Transform**, and **Rewrite**. To request an increase to this limit, [create an Azure support request](/azure/azure-portal/supportability/how-to-create-azure-support-request).

### Choose an enforcement mode

| Mode | Behavior | When to use |
| --- | --- | --- |
| **Audit** | Outbound traffic flows normally. Requests that *would* be denied are logged but not blocked. | Observe what your agent calls before you enforce. |
| **Enforce** | Matching rules are applied, and denied requests are blocked. | Production enforcement after you validate rules in Audit mode. |

Deploy in **Audit** mode first, review the egress decisions, refine your rules, and then switch to **Enforce**.

> [!NOTE]
> Audit mode changes only how **Deny** actions behave: a request that would be denied is logged instead of blocked. **Transform** and **Rewrite** actions are applied in both Audit and Enforce modes, so header transforms and redirects still take effect while you audit.

### Add egress rules by using the Azure Developer CLI

Add the RAI policy ARM resource to your `azd` project's Bicep infrastructure. The `azd provision` command deploys the resource through ARM.

1. Add the following Bicep to the resource-group-scoped infrastructure for the resource group that contains your Foundry resource:

    ```bicep
    @description('Name of the existing Foundry resource.')
    param accountName string

    resource account 'Microsoft.CognitiveServices/accounts@2026-05-15-preview' existing = {
      name: accountName
    }

    resource egressPolicy 'Microsoft.CognitiveServices/accounts/raiPolicies@2026-05-15-preview' = {
      parent: account
      name: 'allow-contoso'
      properties: {
        mode: 'Blocking'
        basePolicyName: 'Microsoft.DefaultV2'
        egressPolicy: {
          mode: 'Enforced'
          defaultAction: 'Deny'
          rules: [
            {
              name: 'allow-contoso'
              ruleType: 'Fqdn'
              match: {
                host: '*.contoso.com'
              }
              action: {
                actionType: 'Allow'
              }
            }
          ]
        }
      }
    }

    output RAI_POLICY_ID string = egressPolicy.id
    ```

    Reference: [Microsoft.CognitiveServices accounts/raiPolicies](/azure/templates/microsoft.cognitiveservices/2026-05-15-preview/accounts/raipolicies).

1. Provision the policy:

    ```bash
    azd provision
    ```

The command creates or updates the `Microsoft.CognitiveServices/accounts/raiPolicies` child resource. Use the `RAI_POLICY_ID` output as the full policy resource ID when you attach the guardrail to a hosted agent.

### Add egress rules by using the REST API

An RAI policy stores egress rules in the `egressPolicy` property. Create or update the policy by using the Azure Resource Manager **RAI Policies - Create Or Update** operation with the `2026-05-15-preview` API version:

```bash
TOKEN=$(az account get-access-token --resource "https://management.azure.com" --query accessToken -o tsv)

curl -X PUT \
  "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account>/raiPolicies/<policy-name>?api-version=2026-05-15-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "mode": "Blocking",
      "basePolicyName": "Microsoft.DefaultV2",
      "egressPolicy": {
        "mode": "Enforced",
        "defaultAction": "Deny",
        "rules": [
          {
            "name": "allow-contoso",
            "ruleType": "Fqdn",
            "match": { "host": "*.contoso.com" },
            "action": { "actionType": "Allow" }
          }
        ]
      }
    }
  }'
```

- Set `egressPolicy.mode` to `Enforced` to block traffic, or `Audit` to log would-deny events without blocking.
- Set `egressPolicy.defaultAction` to `Deny` for an allow list or `Allow` for a deny list.
- Set each rule's `action.actionType` to `Allow`, `Deny`, `Transform`, or `Rewrite`.

To review the configured rules, send a GET request to the same URL and inspect `properties.egressPolicy`.

For a complete request body that combines a default action with several rule types, see the [`PutRaiPolicyWithEgress.json`](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/CognitiveServices.Management/examples/2026-05-15-preview/PutRaiPolicyWithEgress.json) example in the Azure REST API specs.

### Transform request headers

When a rule's `action.actionType` is `Transform` (or `Rewrite`), you can modify the headers of the outbound request by using an `action.headers` array. Each entry describes one header operation:

```json
{
  "name": "allow-and-tag-contoso",
  "ruleType": "Fqdn",
  "match": { "host": "*.contoso.com" },
  "action": {
    "actionType": "Transform",
    "headers": [
      { "operation": "Set",    "name": "X-Trace-Source", "value": "hosted-agent" },
      { "operation": "Insert", "name": "X-Request-Id",   "value": "default-id" },
      { "operation": "Remove", "name": "User-Agent" }
    ]
  }
}
```

Each header object supports the following fields:

| Field | Required | Description |
| --- | --- | --- |
| `operation` | Yes | The header operation: `Set`, `Insert`, or `Remove`. Operation names are case-insensitive. If you omit it, `Set` is used. |
| `name` | Yes | The name of the header to modify. |
| `value` | For `Set` and `Insert` | The static header value. Not used for `Remove`. |

You must include `headers` when `actionType` is `Transform`. You can omit `headers` when `actionType` is `Rewrite`. Header transforms apply only to requests that match the rule.

> [!NOTE]
> During preview, header transforms support **static `value`** only. Dynamic value references (`valueRef`) that inject a **managed identity** token or a **secret** are **coming soon** and aren't enforced yet. A rule that uses `valueRef` is accepted but the header isn't injected at runtime.

#### Header operations

The three operations differ only in how they treat a header that's already present on the outbound request:

| Operation | Header already present | Header not present |
| --- | --- | --- |
| `Set` | Overwrites the existing value. | Adds the header. |
| `Insert` | Leaves the existing value unchanged. | Adds the header. |
| `Remove` | Removes the header. | No effect. |

Use `Set` to force a header to a specific value regardless of what the agent sent. Use `Insert` to supply a default only when the agent didn't already set the header. Use `Remove` to strip a header before the request leaves the runtime.

### Add egress rules in the portal

You can also author egress rules in the Foundry portal as a **Network** control on a guardrail:

1. In the Foundry portal, create or edit a guardrail, and then expand the **Network** control.

   :::image type="content" source="../media/add-hosted-agent-guardrails/network-egress-control.png" alt-text="Screenshot of the Network control in a guardrail showing the Egress rules row and the Outbound requests default action." lightbox="../media/add-hosted-agent-guardrails/network-egress-control.png":::

1. Select **Egress rules**, and set the **Outbound requests** default action to **Deny** or **Allow**.
1. Select **Add rules**, choose a **Mode** (**Audit** or **Enforce**), enter a **Host match** and an **Action**, and then select **Add**. Reorder rules as needed; the first match wins. For a **Transform** action, use a **Static value** for the header. (**Managed identity** and **Secret reference** value sources appear in the dialog but aren't enforced yet - see [Preview limitations](#preview-limitations-and-whats-coming-next).)

   :::image type="content" source="../media/add-hosted-agent-guardrails/egress-rule-list.png" alt-text="Screenshot of the Create egress rules dialog with Audit and Enforce modes, a host match field, and an action list." lightbox="../media/add-hosted-agent-guardrails/egress-rule-list.png":::

1. Select **Create**, and then assign the guardrail to your hosted agent.

For details about creating and assigning guardrails in the portal, see [Configure guardrails and controls](../../guardrails/how-to-create-guardrails.md).

### Certificate handling

To inspect HTTPS traffic, the hosted-agent runtime injects the egress proxy's certificate authority (CA) into the sandbox trust bundle. The proxy CA is infrastructure-specific: it can differ across hosted-agent clusters and regions, and it rotates over time (currently about every 30 days). Treat the CA bundle as runtime configuration. Don't pin, copy, or persist it.

Configure TLS clients to read the runtime-provided CA bundle from the standard environment variables that are already present in the sandbox:

| Environment variable | Use |
| --- | --- |
| `SSL_CERT_FILE` | Generic PEM CA bundle path for OpenSSL-style TLS clients. |
| `REQUESTS_CA_BUNDLE` | Python `requests` and compatible HTTP clients. |
| `GRPC_DEFAULT_SSL_ROOTS_FILE_PATH` | gRPC clients that support the default roots file override. |
| `NODE_EXTRA_CA_CERTS` | Node.js additional CA file, read when the process starts. |

For example, with Python `requests`:

```python
import os
import requests

response = requests.get(
    "https://example.com",
    verify=os.environ["REQUESTS_CA_BUNDLE"],
)
```

Keep these constraints in mind:

- Don't pin the CA subject, public key, thumbprint, or file contents. Any of these values can change on rotation or differ by cluster.
- Don't persist the injected CA to a container image, persistent volume, snapshot, or source control. The CA is runtime infrastructure, not application configuration.
- Rotation can happen while a sandbox is running. Long-running processes might need to reload their TLS configuration or restart.
- If you must build a single custom bundle (for example, to combine enterprise roots with the runtime roots), build it at process startup from the current runtime bundle and treat it as temporary:

  ```bash
  cat "$SSL_CERT_FILE" /app/custom-roots.pem > /tmp/runtime-ca-bundle.pem
  export SSL_CERT_FILE=/tmp/runtime-ca-bundle.pem
  export REQUESTS_CA_BUNDLE=/tmp/runtime-ca-bundle.pem
  ```

### View egress decisions

The agent sends network egress decisions to your project's Application Insights and trace monitoring tools. You can view these decisions in the Foundry portal playground and in Application Insights to confirm that network egress behavior aligns with your configured policy.

#### In the Foundry portal playground

To view egress decisions in the trace timeline:

1. Sign in to [Microsoft Foundry](https://ai.azure.com) and open your project's playground.
1. Run or select an agent invocation to open its trace.
1. Select the **Trajectories** tab to see the full trace timeline.
1. Expand the trace nodes until you see a span named **Network egress decision**. It appears next to the request that triggered it.
1. Select the span to review the decision details.

:::image type="content" source="../media/add-hosted-agent-guardrails/network-egress-decision-trace.png" alt-text="Screenshot of the Trajectories tab in the Foundry portal playground, showing a Network egress decision span in the trace timeline." lightbox="../media/add-hosted-agent-guardrails/network-egress-decision-trace.png":::

The span details show the information you need to understand why a request was allowed or denied:

| Field | Description |
|-------|-------------|
| Decision | The outcome of the policy evaluation, for example `Allow` or `Deny`. |
| Reason | A human-readable explanation, such as "Request matched allow rule" or "No egress policy rule allowed this destination." |
| Matched rule | The name of the rule that determined the outcome, if one matched. |
| Rule source | The origin of the matched rule, such as a connector or policy definition. |
| Enforcement | Whether the policy was enforced or run in audit mode. |
| Destination | The method and URL of the outbound request. |
| Default action | The action applied when no rule matches, for example `Deny`. |

Allowed requests appear with a success status, and denied requests appear with a failure status, so you can spot blocked calls without leaving the trace view.

#### In Application Insights

To review egress decisions in Application Insights logs:

1. Locate your project's Application Insights resource:
   1. Go to the Foundry portal.
   1. Select the **Operate** tab.
   1. Select **Admin**.
   1. Search for and select your project.
   1. Open the **Connected resources** tab.
   1. Find the **AppInsights** connected resource and copy its **Target URI**.

   Each project should have a single Application Insights connection. If Application Insights isn't configured, select **Add connection** and add an Application Insights resource for the project.

2. Open the Application Insights resource in the Azure portal and go to **Logs**. Run the following query to view recent network egress decisions:

```kusto
traces
| where timestamp > ago(1h)
| where message == "Network egress decision"
```

Each event includes details such as the destination host, matched rule, decision, and enforcement mode.

### What a blocked request looks like

When a rule denies an outbound call, the egress proxy returns an `HTTP 403` response to the agent's network client. The agent handles the error with its own logic. For example, if the blocked call was a tool call, the agent typically reports that the tool call failed and tries a different approach. Policy internals aren't exposed to end users.

### Preview limitations and what's coming next

Network egress controls are an additive feature. During preview:

- Egress controls apply to hosted agents only.
- Enforcement happens inside the Foundry-managed agent sandbox. Egress controls complement your own network controls, such as Azure Firewall, rather than replace them. They don't delegate enforcement to a customer-managed firewall, and they aren't centrally enforced through Azure Policy.
- In the portal, rules match on host.

The following capabilities aren't available yet and are planned for future updates:

- **Dynamic header values** — injecting a header value from a **managed identity** or a **secret** (`valueRef`). During preview, use a static `value`.
- Rule types such as Azure service tags and IP address ranges.
- MCP tool policies, PII and data-loss-prevention inspection, and custom webhook hooks.

## Related content

- [Guardrails and controls overview](../../guardrails/guardrails-overview.md) — what guardrails are, the risks they detect, and where they intervene.
- [Configure guardrails and controls](../../guardrails/how-to-create-guardrails.md) — create the RAI policy you reference here.
- [Networking options for Foundry Agent Service](../concepts/networking-options.md) — how egress controls fit with virtual network and private networking options.
- [Deploy a hosted agent](deploy-hosted-agent.md) — the full deployment workflow for hosted agents.
