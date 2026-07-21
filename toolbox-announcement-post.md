---
ai-usage: ai-assisted
---

# What's new in Foundry Toolbox: Tool Search, 1,000+ connectors, guardrails, and more

A month ago, we shipped Foundry Toolbox. Since then, teams have been building — and building fast.

When adoption takes off, you learn things quickly. Catalogs that started with five tools are growing to fifty. Teams want to pull in Microsoft 365 signals and Fabric analytics. Security teams are asking for content filtering on tool outputs. And developers are looking for connectors that weren't in the catalog yet.

The foundation held. The asks kept coming.

Today we're sharing what we built in response: **Tool Search** for large catalogs, **Work IQ and Fabric IQ** integrations, **1,000+ managed MCP servers** from the connector catalog, and **bring-your-own guardrails** at the toolbox layer.

---

## Discover more: Tool Search scales toolboxes to hundreds of tools

Here's a problem that sneaks up on you: toolboxes grow. You start with five tools. Six months later, you have 50. A year in, you have 200.

At 200 tools, every agent turn pays a tax you didn't sign up for. Every tool definition — its name, description, parameters — flows into the model's context window whether the model needs it or not. At scale, that's thousands of tokens burned per turn on tools the model won't touch. Context fills up. Accuracy drops. The model picks semantically adjacent but wrong tools, or misses the right one buried in the noise.

**Tool Search** fixes this with a runtime discovery layer that keeps cost flat and quality high, regardless of how large the catalog grows.

When Tool Search is enabled on a toolbox, the model doesn't see a wall of tool definitions. It sees two meta-tools:

- **`tool_search`** — call it with a natural-language description of what you need; get back the most relevant tools, ranked by relevance.
- **`call_tool`** — invoke any discovered tool by name.

That's it. Everything else is hidden until the model asks for it.

Here's what this looks like for a customer support agent with 200 tools spanning CRM, email, ticketing, analytics, and admin systems:

```
User: "Show me all open tickets for acme@company.com and draft a follow-up email"

1. Model calls tool_search("open tickets customer email")
   → Returns: GetTickets, DraftEmail, ListCustomers, SendEmail

2. Model calls call_tool("GetTickets", { "email": "acme@company.com" })
   → Returns the open ticket data

3. Model calls call_tool("DraftEmail", { "subject": "Follow-up on your tickets", ... })
   → Returns the composed draft

4. Model synthesizes the final response
```

Instead of 200 definitions in the prompt, the model processes 2 meta-tools plus the handful of results that matter for this turn. Cost stays flat whether the toolbox has 20 tools or 2,000.

We validated this pattern across 55 natural-language queries spanning 11 enterprise categories, running against 35 registered tools. With GPT-4o, agents followed the `tool_search → call_tool → answer` path **98% of the time**. It works across frameworks — LangGraph, Microsoft Agent Framework, and direct Chat Completions — without any framework changes.

Enabling Tool Search is one line. Add `{"type": "toolbox_search"}` to your toolbox version's tools list:

```python
toolbox_version = client.beta.toolboxes.create_version(
    name="my-toolbox",
    description="Large toolbox with tool search enabled",
    tools=[
        {"type": "toolbox_search"},   # ← this is all it takes
        {
            "type": "mcp",
            "server_label": "github",
            "server_url": "https://api.githubcopilot.com/mcp",
            "require_approval": "never",
            "project_connection_id": "github-mcp-conn",
        },
        # ... your other tools
    ],
)
```

One addition. Your agent handles 200 tools as cleanly as it handles 5. Token cost doesn't change.

→ [Enable tool search in a toolbox](/azure/foundry/agents/how-to/tools/tool-search)

---

## More tools, more reach

The original Toolbox launch supported MCP servers, OpenAPI tools, Azure AI Search, code interpreter, and Bing web search. We've added four new categories that unlock some of the most frequently requested integration scenarios.

### Work IQ: bring Microsoft 365 into your agents

Your agents can now tap into Microsoft 365 — documents, emails, meetings, chats, and workflows — through Work IQ. It's a Microsoft 365 MCP server that connects to your agent's toolbox using identity passthrough: the tool acts on behalf of the signed-in user, so the data your agent sees reflects exactly what that user can access. No standing service accounts. No over-provisioned permissions.

The connection uses `UserEntraToken` auth. Set it up in your `agent.yaml`:

```yaml
resources:
  - kind: connection
    name: workiq-mail-conn
    category: RemoteTool
    authType: UserEntraToken
    audience: <entra-app-id>
    target: https://agent365.svc.cloud.microsoft/agents/servers/mcp_MailTools
  - kind: toolbox
    name: workiq-tools
    tools:
      - type: mcp
        server_label: workiq
        project_connection_id: workiq-mail-conn
```

→ [Work IQ overview](/microsoft-365-copilot/extensibility/workiq-overview)

### Fabric IQ: reason over your enterprise analytics

Agents can now query enterprise data in Microsoft Fabric — OneLake, Power BI semantic models, and Fabric data agents — directly from a toolbox. Like Work IQ, Fabric IQ uses identity passthrough via the On-Behalf-Of flow: every query runs under the requesting user's credentials, so row-level security and access controls are preserved automatically.

One command to wire it up:

```bash
azd ai agent connection create my-fabric-connection \
  --project-endpoint $PROJECT_ENDPOINT \
  --kind remote-tool \
  --target https://api.fabric.microsoft.com/v1/mcp/fabricaihub/integrations/m365 \
  --auth-type user-entra-token \
  --audience https://analysis.windows.net/powerbi/api
```

Point your agent at that connection, and it can answer questions about your business data the same way it answers questions about anything else.

→ [Fabric IQ overview](/fabric/iq/overview)

### Browser Automation: agents that can browse

Sometimes the tool you need doesn't have an API. Sometimes the data you need lives behind a form, a login page, or a multi-step web workflow. Browser Automation gives your agent the ability to navigate, click, fill forms, and extract content from live web pages.

It's built on Microsoft Playwright Workspaces, which provisions isolated, sandboxed browser sessions — one per conversation turn. The agent takes a screenshot, decides what to do next, acts, takes another screenshot, and repeats until the task is done. It works for multi-turn flows: a user can refine a request mid-session and the agent adapts in place.

> **Security note.** Browser Automation carries real risk. An agent browsing external sites can encounter prompt injection attacks or inadvertently exfiltrate data. Enable it only on low-privilege machines, scope it carefully, and review the security guidance before going to production.

→ [Automate browser tasks with the Browser Automation tool](/azure/foundry/agents/how-to/tools/browser-automation)

### 1,000+ managed MCP servers from the Connector Catalog

This is the big one. The Foundry Tools Catalog now surfaces over 1,000 connectors — pre-built integrations to SaaS services, databases, and line-of-business systems. When you add a connector to your agent, Foundry provisions a **managed MCP server** for it in your account's Connector Namespace: an MCP server that Foundry hosts, maintains, and scales. You don't write server code. You don't manage infrastructure. You connect once and call tools.

The configuration flow in the Foundry portal is four steps:

1. **Browse** — find the connector in the Tools Catalog (GitHub, SharePoint, Salesforce, Databricks, and hundreds more).
2. **Connect** — authenticate via OAuth2 or API key. Foundry manages the token exchange.
3. **Select actions** — pick which connector actions to expose as tools. Less is more: narrow the set to what the agent actually needs.
4. **Add tool** — Foundry creates the managed MCP server and wires it to your agent.

Publisher tiers in the catalog range from first-party Microsoft services to verified third-party publishers to community-contributed connectors. Check the **By:** field on the connector's detail page and review the data-handling implications before connecting — especially for third-party and independent publishers.

→ [Add managed MCP servers powered by connector namespaces](/azure/foundry/agents/how-to/tools/connectors)

---

## Govern more: bring your own guardrail

The original Toolbox shipped with Azure AI Gateway policies baked in — rate limiting, token quotas, identity verification. Those defaults are still there. Now you can add your own [Responsible AI content filter](/azure/foundry/guardrails/guardrails-overview) on top.

The guardrail runs at the toolbox layer, on tool inputs *and* outputs, independently of the model-level content filter. That matters: not all tool calls go through the main response stream. A guardrail on the toolbox catches what model-level filters miss.

Set it up by referencing a named RAI policy you've already configured in the Foundry portal under **Guardrails**:

```python
toolbox_version = project.beta.toolboxes.create_toolbox_version(
    toolbox_name="my-toolbox",
    description="Toolbox with guardrail",
    tools=[...],
    policies={
        "rai_config": {
            "rai_policy_name": "/subscriptions/<sub>/resourceGroups/<rg>/providers/"
                               "Microsoft.CognitiveServices/accounts/<account>/"
                               "raiPolicies/<policy-name>"
        }
    },
)
```

The same `policies.rai_config.rai_policy_name` field is available in the REST API, .NET SDK, JavaScript SDK, and azd `agent.yaml`. Create the policy in the portal once; reference it by ARM resource ID everywhere you need it.

→ [Configure guardrails for a toolbox](/azure/foundry/agents/how-to/tools/toolbox#configure-guardrails)

---

## Extend: agent routines

Routines let agents compose structured sub-workflows — handing off a scoped task to another agent, or running a named procedure against a toolbox — without losing control of the outer conversation. It's the extensibility story that makes multi-agent coordination feel deliberate rather than improvised.

[TO VERIFY: Add concrete capability description and code example once PR #12257 is published.]

→ [Use routines (preview)](/azure/foundry/agents/how-to/use-routines) *(documentation in progress)*

---

## Coming soon: skills in the toolbox

Tools tell an agent what it can do. Skills tell it **HOW** to do the job.

Right now, teams manage skills and tools through separate pipelines. Skills — the SKILL.md files and script bundles that give agents domain knowledge, behavioral guidance, and task patterns — live outside the toolbox, scattered across repos, container images, or custom init code. There's no versioning, no shared distribution story, and no way to know which agents are running which version of a skill.

We're changing that by bringing skills directly into the toolbox: when you build a toolbox, you attach versioned, immutable skills alongside the tools. Toolbox becomes your managed organizational skills catalog. The toolbox exposes them as standard MCP resources, discoverable via `resources/list` and downloadable via `resources/read`. At startup, any MCP client — GitHub Copilot, Claude Code, or your own agent harness — calls `resources/list` once, downloads all skills to its local context, and is ready to work. No Foundry SDK required. No custom wiring.

Skills from two places flow through the same surface:

- **First-party skills** you author and manage via the Foundry Skills API — versioned, curated, attached to a specific toolbox definition.
- **Third-party skills** shipped by the remote MCP servers already in your toolbox — passed through as MCP resources, just as the originating server publishes them.

The result: your toolbox becomes a single delivery mechanism for both what your agent can do and how it's expected to behave. Configure once, consume from any harness — the same endpoint, the same MCP protocol.

*Skills in Toolbox is in active development. Details will be published when the feature is available.*

---

## Try it now

Every feature in this post is available in the Foundry portal today.

- **Tool Search** → add `{"type": "toolbox_search"}` to any toolbox version
- **Work IQ / Fabric IQ** → `UserEntraToken` connections in the Tools Catalog
- **Browser Automation** → provision a Playwright Workspace and connect it in the portal
- **Connector Catalog** → browse 1,000+ managed MCP servers in the Tools Catalog
- **Guardrails** → set `policies.rai_config.rai_policy_name` on any toolbox version

**Docs:**
[Toolbox overview](/azure/foundry/agents/how-to/tools/toolbox) · [Tool Search](/azure/foundry/agents/how-to/tools/tool-search) · [Connectors](/azure/foundry/agents/how-to/tools/connectors) · [Browser Automation](/azure/foundry/agents/how-to/tools/browser-automation)

**Portal:** [ai.azure.com/nextgen](https://ai.azure.com/nextgen)

Drop questions and feedback in the comments — the team reads them.

