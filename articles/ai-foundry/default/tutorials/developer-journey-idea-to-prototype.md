---
title: "Tutorial: Idea to prototype - Build and evaluate an enterprise agent"
description: "Prototype an enterprise agent: build a single agent with SharePoint grounding and Model Context Protocol (MCP) tools, run batch evaluation, extend to multi-agent, and deploy to Azure AI Foundry."
ms.service: azure-ai-foundry
ms.topic: tutorial
ms.date: 11/18/2025
ms.author: jburchel
author: jonburchel
ms.reviewer: dantaylo
ai.usage: ai-assisted
#customer intent: As a developer I want to quickly prototype an enterprise-grade agent with real data, tools, evaluation, and a deployment path so I can validate feasibility before scaling.
---

# Idea to prototype

This tutorial covers the first stage of the Azure AI Foundry developer journey: from an initial idea to a working prototype. You build a **modern workplace assistant** that combines internal company knowledge with external technical guidance by using the Azure AI Foundry SDK.

**Business scenario**: Create an AI assistant that helps employees by combining:

- **Company policies** (from SharePoint documents)
- **Technical implementation guidance** (from Microsoft Learn via MCP)
- **Complete solutions** (combining both sources for business implementation)
- **Batch evaluation** to validate agent performance on realistic business scenarios

**Tutorial outcome**: By the end you will have a running Modern Workplace Assistant that can answer policy, technical, and combined implementation questions; a repeatable batch evaluation script; and clear extension points (additional tools, multi‑agent patterns, richer evaluation).

> [!div class="checklist"]
> **You will achieve:**
> - Build a Modern Workplace Assistant with SharePoint and MCP integration.
> - Demonstrate real business scenarios combining internal and external knowledge.
> - Implement robust error handling and graceful degradation.
> - Create evaluation framework for business-focused testing.
> - Prepare foundation for governance and production deployment.

This ultra-minimal sample demonstrates enterprise-ready patterns with realistic business scenarios.

## Prerequisites 

- Azure subscription and CLI authentication (`az login`)
- Azure CLI 2.67.0 or later (check with `az version`)
- An Azure AI Foundry **project** with a deployed model (for example, `gpt-4o-mini`). If you do not have one: [Create a project](../../how-to/create-projects.md) and then deploy a model (see model overview: [Model catalog](../../concepts/foundry-models-overview.md)).
- Python 3.10 or later, .NET 7 SDK, or Java 17 SDK installed (depending on your chosen language)
- SharePoint connection configured in your project ([SharePoint tool documentation](../../agents/how-to/tools/sharepoint.md))
- (Optional) Git installed for cloning the sample repository

> [!NOTE]
> To configure your Azure AI Foundry project for SharePoint connectivity, see the [SharePoint tool documentation](../../agents/how-to/tools/sharepoint.md).

> [!TIP]
> Get your tenant ID quickly:
> ```bash
> az account show --query tenantId -o tsv
> ```

### Understanding portal endpoints

In the Azure AI Foundry portal you might see multiple endpoints (for example: resource endpoint, project endpoint, model endpoint). For this sample:
- Use the **Project endpoint** in `PROJECT_ENDPOINT`.
- Do NOT use the parent resource endpoint (for example the cognitive services account endpoint).
- Use the model deployment name (for example `gpt-4o-mini`) rather than a raw base model name.

If unsure, in the portal open your project, select **Deployments**, choose the deployment, and copy the **Endpoint** and **Deployment name**.

---

## Step 1: Obtain the sample code

Instead of navigating a large repository tree, use one of these approaches:

#### Option A (clone entire samples repo)

```bash
git clone --depth 1 https://github.com/azure-ai-foundry/foundry-samples.git
cd foundry-samples/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype
```

#### Option B (sparse checkout only this tutorial - reduced download)

```bash
git clone --no-checkout https://github.com/azure-ai-foundry/foundry-samples.git
cd foundry-samples
git sparse-checkout init --cone
git sparse-checkout set samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype
git checkout
cd samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype
```

Repeat the path for `csharp` or `java` variants as needed.

#### Option C (Download ZIP of repository)

Download repository ZIP, extract, and navigate to the tutorial folder.

> [!IMPORTANT]
> A standalone repository is recommended for production adoption. This tutorial uses the shared samples repo for now. Sparse checkout minimizes local noise.

# [Python](#tab/python)

> [!div class="nextstepaction"] 
> [Download the Python code now](https://github.com/azure-ai-foundry/foundry-samples/tree/nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype)

# [C#](#tab/csharp)

> [!div class="nextstepaction"] 
> [Download the C# code now](https://github.com/azure-ai-foundry/foundry-samples/tree/nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype)

# [Java](#tab/java)

> [!div class="nextstepaction"] 
> [Download the Java code now](https://github.com/azure-ai-foundry/foundry-samples/tree/nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype)

---


The ultra-minimal structure contains only essential files:

# [Python](#tab/python)

```text
enterprise-agent-tutorial/
└── 1-idea-to-prototype/
    ├── main.py                        # Modern Workplace Assistant
    ├── evaluate.py                    # Business evaluation framework
    ├── questions.jsonl                # Business test scenarios (4 questions)
    ├── requirements.txt               # Python dependencies
    ├── .env.template                  # Environment variables template
    ├── SAMPLE_SHAREPOINT_CONTENT.md   # Business documents (markdown source)
    ├── README.md                      # Complete setup instructions
    ├── MCP_SERVERS.md                 # MCP server configuration guide
    └── setup_sharepoint.py            # SharePoint diagnostic tool
```

# [C#](#tab/csharp)

```text
enterprise-agent-tutorial/
└── 1-idea-to-prototype/
    ├── ModernWorkplaceAssistant/
    │   ├── Program.cs                 # Modern Workplace Assistant
    │   └── ModernWorkplaceAssistant.csproj
    ├── Evaluate/
    │   ├── Program.cs                 # Business evaluation framework
    │   └── Evaluate.csproj
    ├── shared/
    │   ├── .env.template              # Environment variables template
    │   ├── questions.jsonl            # Business test scenarios (4 questions)
    │   ├── SAMPLE_SHAREPOINT_CONTENT.md # Business documents (markdown source)
    │   ├── MCP_SERVERS.md             # MCP server configuration guide
    │   └── README.md                  # SharePoint setup instructions
    └── README.md                      # Complete setup instructions
```

# [Java](#tab/java)

```text
enterprise-agent-tutorial/
└── 1-idea-to-prototype/
    ├── src/main/java/com/microsoft/azure/samples/
    │   ├── ModernWorkplaceAssistant.java  # Modern Workplace Assistant
    │   └── EvaluateAgent.java             # Business evaluation framework
    ├── pom.xml                        # Maven project configuration
    ├── .env.template                  # Environment variables template
    ├── questions.jsonl                # Business test scenarios (4 questions)
    ├── SAMPLE_SHAREPOINT_CONTENT.md   # Business documents (markdown source)
    ├── MCP_SERVERS.md                 # MCP server configuration guide
    └── README.md                      # Complete setup instructions
```

---

## Step 2: Run the sample immediately (quick win)

Start by running the agent so you see working functionality before diving into implementation details.

### Environment setup and virtual environment

# [Python](#tab/python)

```bash
cd samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype

# Create virtual environment (recommended)
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Copy environment template
cp .env.template .env

# Populate .env (see section below)
# Install dependencies
pip install -r requirements.txt
```

# [C#](#tab/csharp)

```bash
cd samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype
cp shared/.env.template .env
dotnet restore
```

# [Java](#tab/java)

```bash
cd samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype
cp .env.template .env
mvn clean compile
```

---

### Configure `.env`

Copy `.env.template` to `.env` and configure:

```bash
# Azure AI Foundry Configuration  
PROJECT_ENDPOINT=https://<your-project>.aiservices.azure.com
MODEL_DEPLOYMENT_NAME=gpt-4o-mini
AI_FOUNDRY_TENANT_ID=<your-tenant-id>  # Obtain with: az account show --query tenantId -o tsv

# The Microsoft Learn MCP Server (public authoritative Microsoft docs index)
MCP_SERVER_URL=https://learn.microsoft.com/api/mcp

# SharePoint Integration (Optional - requires connection setup)
SHAREPOINT_RESOURCE_NAME=your-sharepoint-connection
SHAREPOINT_SITE_URL=https://your-company.sharepoint.com/teams/your-site
```

> [!NOTE]
> If you are unsure of your project endpoint, open your project in the portal and copy the **Project endpoint** value (distinct from service resource endpoint).

### Run agent and evaluation

# [Python](#tab/python)

```bash
python main.py
python evaluate.py
```

# [C#](#tab/csharp)

```bash
dotnet run --project ModernWorkplaceAssistant
dotnet run --project Evaluate
```

# [Java](#tab/java)

```bash
mvn exec:java -Dexec.mainClass="com.microsoft.azure.samples.ModernWorkplaceAssistant"
mvn exec:java -Dexec.mainClass="com.microsoft.azure.samples.EvaluateAgent"
```

### Expected output (agent first run)

Successful run with SharePoint:

```text
🤖 Creating Modern Workplace Assistant...
✅ SharePoint connected: YourConnection
✅ Agent created: asst_abc123
```

Graceful degradation without SharePoint:

```text
⚠️  SharePoint connection not found: Connection 'YourConnection' not found
✅ Agent created: asst_abc123
```

Now that you have a working agent, the next sections explain how it is built. No additional action is required while reading—these are explanatory.

---

## Step 3: (Optional reading) Set up sample SharePoint business documents

You can create documents manually or generate them automatically.

### Option A: Manual upload (existing method)

1. Navigate to your SharePoint site (configured in the connection).
2. Create document library "Company Policies" (or use existing "Documents").
3. Create four Word documents:
   - `remote-work-policy.docx`
   - `security-guidelines.docx`  
   - `collaboration-standards.docx`
   - `data-governance-policy.docx`
4. Copy content from corresponding sections in `SAMPLE_SHAREPOINT_CONTENT.md`.

### Option B: Auto-generate documents (PowerShell)

```powershell
# Generates four markdown files from SAMPLE_SHAREPOINT_CONTENT.md
$src = "SAMPLE_SHAREPOINT_CONTENT.md"
$map = @{
  "remote-work-policy.md"      = "## Remote Work Policy"
  "security-guidelines.md"     = "## Security Guidelines"
  "collaboration-standards.md" = "## Collaboration Standards"
  "data-governance-policy.md"  = "## Data Governance Policy"
}
$md = Get-Content $src -Raw
foreach ($kv in $map.GetEnumerator()) {
  $file = $kv.Key; $header = $kv.Value
  $section = ($md -split "`n(?=## )") | Where-Object { $_.StartsWith($header) }
  $content = $section.Trim()
  Set-Content -Path $file -Value $content
}
Write-Host "Generated markdown policy documents. Upload these to SharePoint (open in Word and Save As .docx if required)."
```

### Sample structure

```text
📁 Company Policies/
├── 🏠 remote-work-policy.docx      # VPN, MFA, device requirements
├── 🔒 security-guidelines.docx     # Azure security standards
├── 🤝 collaboration-standards.docx # Teams, SharePoint usage
└── 📊 data-governance-policy.docx  # Data classification, retention
```

---

## Step 4: Understand the assistant implementation

This section explains the core code in `main.py` / `Program.cs` / `ModernWorkplaceAssistant.java`. You already ran the agent; this is conceptual and requires no changes. After reading you will be able to:
- Add new internal/external data tools.
- Extend dynamic instructions.
- Introduce multi-agent orchestration later.
- Enhance observability and diagnostics.

The code breaks down into the following main sections, ordered as they appear in the full sample code:

1. [Configure imports and authentication](#imports-and-authentication-setup)
2. [Configure authentication to Azure](#configure-authentication-in-azure)
3. [Configure the SharePoint tool](#create-the-sharepoint-tool-for-the-agent)
4. [Configure MCP tool](#create-the-mcp-tool-for-the-agent)
5. [Create the agent and connect the tools](#create-the-agent-and-connect-the-tools)
6. [Converse with the agent](#converse-with-the-agent)

### Imports and authentication setup

The code uses several client libraries from the Azure AI Foundry SDK to create a robust enterprise agent.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="imports_and_includes":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="imports_and_includes":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype/src/main/java/com/microsoft/azure/samples/ModernWorkplaceAssistant.java" id="imports_and_includes":::

---

### Configure authentication in Azure

Before you can create your agent, set up authentication to the Azure AI Foundry.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="agent_authentication":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="agent_authentication":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype/src/main/java/com/microsoft/azure/samples/ModernWorkplaceAssistant.java" id="agent_authentication":::

---

### Create the SharePoint tool for the agent

The agent uses SharePoint and can access company policy and procedure documents stored there. Set up the connection to SharePoint in your code.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="sharepoint_tool_setup":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="sharepoint_tool_setup":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype/src/main/java/com/microsoft/azure/samples/ModernWorkplaceAssistant.java" id="sharepoint_tool_setup":::

---

### Create the MCP tool for the agent

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="mcp_tool_setup":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="mcp_tool_setup":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype/src/main/java/com/microsoft/azure/samples/ModernWorkplaceAssistant.java" id="mcp_tool_setup":::

---

### Create the agent and connect the tools

Now, create the agent and connect the SharePoint and MCP tools.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="create_agent_with_tools":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="create_agent_with_tools":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype/src/main/java/com/microsoft/azure/samples/ModernWorkplaceAssistant.java" id="create_agent_with_tools":::

---

### Converse with the agent

Finally, implement an interactive loop to converse with the agent.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="agent_conversation":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="agent_conversation":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype/src/main/java/com/microsoft/azure/samples/ModernWorkplaceAssistant.java" id="agent_conversation":::

---

## Step 5: Evaluate the assistant in a batch

The evaluation framework code tests realistic business scenarios that combine SharePoint policies with Microsoft Learn technical guidance. This approach demonstrates batch evaluation capabilities for validating agent performance across multiple test cases. The evaluation uses a keyword-based approach to assess whether the agent provides relevant responses that incorporate the expected information sources.

This evaluation framework tests:

- **SharePoint integration** for company policy questions
- **MCP integration** for technical guidance questions  
- **Combined scenarios** that require both internal and external knowledge
- **Response quality** by using keyword matching and length analysis

The code breaks down into the following main sections:

1. [Load evaluation data](#load-evaluation-data)
2. [Run batch evaluation](#run-batch-evaluation)
3. [Compile evaluation results](#compile-evaluation-results)

### Load evaluation data

In this section, the evaluation framework loads test questions from `questions.jsonl`. The file contains business scenarios that test different aspects of the agent:

:::code language="jsonl" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/questions.jsonl":::

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/evaluate.py" id="load_test_data":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype/Evaluate/program.cs" id="load_test_data":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype/src/main/java/com/microsoft/azure/samples/EvaluateAgent.java" id="load_test_data":::

---

### Run batch evaluation

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/evaluate.py" id="run_batch_evaluation":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype/Evaluate/program.cs" id="run_batch_evaluation":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype/src/main/java/com/microsoft/azure/samples/EvaluateAgent.java" id="run_batch_evaluation":::

---

### Compile evaluation results

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/evaluate.py" id="evaluation_results":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype/Evaluate/program.cs" id="evaluation_results":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype/src/main/java/com/microsoft/azure/samples/EvaluateAgent.java" id="evaluation_results":::

---

### Additional evaluation assets

The evaluation generates `evaluation_results.json` with metrics for each question (keyword hits, length heuristic). You can extend this to:
- Use model-based scoring prompts.
- Introduce structured output validation.
- Record latency and token usage.

---

## Summary (So what?)

You now have:
- A working single-agent prototype grounded in internal and external knowledge.
- A repeatable evaluation script demonstrating enterprise validation patterns.
- Clear upgrade path: more tools, multi-agent orchestration, richer evaluation, deployment.

These patterns reduce prototype-to-production friction: you can add data sources, enforce governance, and integrate monitoring without rewriting core logic.

---

## Next steps

This ultra-minimal sample provides the foundation for enterprise AI development. To continue your journey, explore the next stages:

### Suggested additional enhancements
- Add more data sources ([Azure AI Search](), [databases]()).
- Implement advanced evaluation methods ([AI-assisted evaluation]()).
- Create [custom tools]() for business-specific operations.
- Add [conversation memory and personalization]().

### Stage 2: Prototype to production

- [Implement safety assessment with red-team testing]().
- [Create comprehensive evaluation datasets with quality metrics]().
- [Apply organization-wide governance policies and model comparison]().
- [Configure fleet monitoring, CI/CD integration, and production deployment endpoints]().

### Stage 3: Production to adoption

- [Collect trace data and user feedback from production deployments]().
- [Fine-tune models and generate evaluation insights for continuous improvement]().
- [Integrate Azure API Management gateway with continuous quality monitoring]().
- [Implement fleet governance, compliance controls, and cost optimization]().

## Related content

- [Azure AI Foundry Agent Service overview](../../agents/overview.md)
- [SharePoint tool documentation](../../agents/how-to/tools/sharepoint.md)
- [MCP tool integration](../../agents/how-to/tools/model-context-protocol.md)
- [Multi-agent patterns](../../agents/how-to/connected-agents.md)
