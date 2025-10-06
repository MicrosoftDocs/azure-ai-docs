---
title: "Developer journey stage 1: Idea to prototype - Build and evaluate an enterprise agent"
description: "Prototype an enterprise agent: build a single agent with SharePoint grounding and MCP tools, run batch evaluation, extend to multi-agent, and deploy to Azure AI Foundry."
ms.service: azure-ai-foundry
ms.topic: tutorial
ms.date: 09/26/2025
ms.author: jburchel
author: jonburchel
ms.reviewer: dantaylo
#customer intent: As a developer I want to quickly prototype an enterprise-grade agent with real data, tools, evaluation, and a deployment path so I can validate feasibility before scaling.
---

# Developer journey stage 1: Idea to prototype - Build and evaluate an enterprise agent

This tutorial covers the first stage of the Azure AI Foundry developer journey: from an initial idea to a working prototype. You build a **Modern Workplace Assistant** that combines internal company knowledge with external technical guidance using the Azure AI Foundry SDK.

**Business Scenario**: Create an AI assistant that helps employees by combining:

- **Company policies** (from SharePoint documents)
- **Technical implementation guidance** (from Microsoft Learn via MCP)
- **Complete solutions** (combining both sources for business implementation)

> [!div class="checklist"]
>
> - Build a Modern Workplace Assistant with SharePoint and MCP integration
> - Demonstrate real business scenarios combining internal and external knowledge
> - Implement robust error handling and graceful degradation
> - Create evaluation framework for business-focused testing
> - Prepare foundation for governance and production deployment

This ultra-minimal sample (10 files, 148 lines of core code) demonstrates enterprise-ready patterns with realistic business scenarios.

> [!NOTE]
> This tutorial uses preview versions of the Azure AI SDK to demonstrate SharePoint and MCP tool integration. These features will be generally available at Microsoft Ignite.

## Prerequisites

- An Azure AI Foundry **project** with a deployed model (e.g., `gpt-4o-mini`)
- Python 3.10 or later
- SharePoint connection configured in your project
- An MCP server endpoint
- Azure CLI authentication (`az login`)

## Step 1: Download the sample code

The complete sample is available in the Azure AI documentation repository. The ultra-minimal structure contains only essential files:

```text
simple-agent/
├── main.py                        # Modern Workplace Assistant (148 lines)
├── evaluate.py                    # Business evaluation framework (54 lines)
├── questions.jsonl                # Business test scenarios (4 questions)
├── requirements.txt               # Python dependencies
├── .env.template                  # Environment variables template
├── SAMPLE_SHAREPOINT_CONTENT.md   # Business documents to upload
├── README.md                      # Complete setup instructions
├── MCP_SERVERS.md                 # MCP server configuration guide
└── setup_sharepoint.py            # SharePoint diagnostic tool
```

### Environment setup

Copy `.env.template` to `.env` and configure your settings:

```bash
# Azure AI Foundry Configuration  
PROJECT_ENDPOINT=https://<your-project>.aiservices.azure.com
MODEL_DEPLOYMENT_NAME=gpt-4o-mini
AI_FOUNDRY_TENANT_ID=<your-ai-foundry-tenant-id>

# The Microsoft Learn MCP Server
# (This public MCP server indexes the latest up-to-date Microsoft documentation so your AI can give authoritative answers to questions about Microsoft products, including reference links.)
MCP_SERVER_URL=https://learn.microsoft.com/api/mcp

# SharePoint Integration (Optional - requires additional setup)
SHAREPOINT_RESOURCE_NAME=your-sharepoint-connection
SHAREPOINT_SITE_URL=https://your-company.sharepoint.com/teams/your-site
```

> [!NOTE]
> To configure your Azure AI Foundry project for SharePoint connectivity, refer to the [SharePoint tool documentation](../../agents/how-to/tools/sharepoint.md).

### Dependencies

# [C#](#tab/csharp)

Create and review the project file, then restore dependencies:

```bash
dotnet restore
```

The project file defines required Azure AI Foundry SDK packages and supporting libraries:

:::code language="xml" source="~/foundry-samples-main/samples/microsoft/csharp/developer-journey-stage-1-idea-to-prototype/ModernWorkplaceAssistant.csproj":::

> [!TIP]
> If you add new packages, re-run `dotnet restore`. Use `dotnet list package --outdated` to check for updates.

# [Python](#tab/python)

Create `requirements.txt`:

:::code language="txt" source="~/foundry-samples-main/samples/microsoft/python/developer-journey-stage-1-idea-to-prototype/requirements.txt":::

# [Java](#tab/java)

The Maven `pom.xml` declares all dependencies. Compile once to download them:

```bash
mvn -q clean compile
```

View the full dependency declarations:

:::code language="xml" source="~/foundry-samples-main/samples/microsoft/java/developer-journey-stage-1-idea-to-prototype/pom.xml":::

> [!NOTE]
> Use `mvn dependency:tree -Dincludes=com.azure` to inspect only Azure-related transitive dependencies.

# [TypeScript](#tab/typescript)

Install Node dependencies from `package.json` (supports npm, pnpm, or yarn):

```bash
npm install
# or
pnpm install
```

Project dependency manifest:

:::code language="json" source="~/foundry-samples-main/samples/microsoft/typescript/developer-journey-stage-1-idea-to-prototype/package.json":::

> [!TIP]
> After modifying dependencies, run `npm audit fix` (or the equivalent for your package manager) to address known vulnerabilities.

---

## Step 2: Build the Modern Workplace Assistant

The main file demonstrates a complete business scenario combining internal policies with external technical guidance:

### Imports and authentication setup

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/developer-journey-stage-1-idea-to-prototype/main.py" range="imports_and_setup":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/microsoft/csharp/developer-journey-stage-1-idea-to-prototype/Program.cs" range="imports_and_setup":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/microsoft/java/developer-journey-stage-1-idea-to-prototype/Main.java" range="imports_and_setup":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/microsoft/typescript/developer-journey-stage-1-idea-to-prototype/src/main.ts" range="imports_and_setup":::

---

### Create the workplace assistant

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/developer-journey-stage-1-idea-to-prototype/main.py" range="create_workplace_assistant":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/microsoft/csharp/developer-journey-stage-1-idea-to-prototype/Program.cs" range="create_workplace_assistant":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/microsoft/java/developer-journey-stage-1-idea-to-prototype/Main.java" range="create_workplace_assistant":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/microsoft/typescript/developer-journey-stage-1-idea-to-prototype/src/main.ts" range="create_workplace_assistant":::

---

This implementation shows:

- **Simplified connection handling** - Uses only the connection name, letting Azure AI Foundry handle URL configuration
- **Dynamic agent instructions** based on available tools  
- **Business-focused scenarios** combining internal and external knowledge
- **Clear diagnostic messages** for troubleshooting
- **Graceful degradation** when services are unavailable

## Step 3: Set up SharePoint business documents

To demonstrate the complete business scenario, upload sample documents to your SharePoint site using the provided `SAMPLE_SHAREPOINT_CONTENT.md`:

### Create business documents

1. **Navigate to your SharePoint site** (configured in your connection)

2. **Create document library** called "Company Policies" (or use existing "Documents")

3. **Upload sample documents** from `SAMPLE_SHAREPOINT_CONTENT.md`:
   - `remote-work-policy.docx` - Remote work security requirements
   - `security-guidelines.docx` - Azure security standards  
   - `collaboration-standards.docx` - Teams and communication policies
   - `data-governance-policy.docx` - Data handling requirements

4. **Copy content** from each section in `SAMPLE_SHAREPOINT_CONTENT.md` into the corresponding Word documents

### Sample document structure

The sample includes realistic Contoso Corp policies that demonstrate:

```text
📁 Company Policies/
├── 🏠 remote-work-policy.docx      # VPN, MFA, device requirements
├── 🔒 security-guidelines.docx     # Azure security standards
├── 🤝 collaboration-standards.docx # Teams, SharePoint usage
└── 📊 data-governance-policy.docx  # Data classification, retention
```

These documents reference Azure and Microsoft 365 technologies, creating realistic scenarios where employees need both internal policy information and external implementation guidance.

## Step 4: Business-focused evaluation

The `evaluate.py` script tests realistic business scenarios combining SharePoint policies with Microsoft Learn technical guidance. This demonstrates batch evaluation capabilities for validating agent performance across multiple test cases.

### Evaluation approach

The evaluation uses a keyword-based approach to assess whether the agent provides relevant responses that incorporate the expected information sources:

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/developer-journey-stage-1-idea-to-prototype/evaluate.py" range="evaluation_functions":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/microsoft/csharp/developer-journey-stage-1-idea-to-prototype/Evaluate.cs" range="evaluation_functions":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/microsoft/java/developer-journey-stage-1-idea-to-prototype/Evaluate.java" range="evaluation_functions":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/microsoft/typescript/developer-journey-stage-1-idea-to-prototype/src/evaluate.ts" range="evaluation_functions":::

---

### Test questions format

The `questions.jsonl` file contains business scenarios that test different aspects of the agent:

:::code language="jsonl" source="~/foundry-samples-main/samples/microsoft/python/developer-journey-stage-1-idea-to-prototype/questions.jsonl":::

This evaluation framework tests:

- **SharePoint integration** for company policy questions
- **MCP integration** for technical guidance questions  
- **Combined scenarios** requiring both internal and external knowledge
- **Response quality** using keyword matching and length analysis

## Step 5: Run the complete sample

### Setup and run

1. **Configure environment**:

# [Python](#tab/python)

```bash
cp .env.template .env
# Edit .env with your Azure AI Foundry project details
pip install -r requirements.txt
```

# [C#](#tab/csharp)

```bash
cp .env.template .env
# Edit .env with your Azure AI Foundry project details
dotnet restore
```

# [Java](#tab/java)

```bash
cp .env.template .env
# Edit .env with your Azure AI Foundry project details
mvn clean compile
```

# [TypeScript](#tab/typescript)

```bash
cp .env.template .env
# Edit .env with your Azure AI Foundry project details
npm install
```

---

2. **Run the Modern Workplace Assistant**:

# [Python](#tab/python)

```bash
python main.py
```

# [C#](#tab/csharp)

```bash
dotnet run
```

# [Java](#tab/java)

```bash
mvn exec:java -Dexec.mainClass="Main"
```

# [TypeScript](#tab/typescript)

```bash
npm run start
```

---

This demonstrates:
- SharePoint connection diagnostics  
- Agent creation with dynamic instructions
- Three business scenarios (policy, technical, combined)
- Interactive mode for testing

3. **Run business evaluation**:

# [Python](#tab/python)

```bash
python evaluate.py
```

# [C#](#tab/csharp)

```bash
dotnet run --project Evaluate.cs
```

# [Java](#tab/java)

```bash
mvn exec:java -Dexec.mainClass="Evaluate"
```

# [TypeScript](#tab/typescript)

```bash
npm run evaluate
```

---

This tests:
- Policy questions (SharePoint integration)
- Technical questions (MCP integration)  
- Combined scenarios (both sources)
- Generates `evaluation_results.json` with detailed metrics

### Expected output

**Successful run with SharePoint**:

```text
🤖 Creating Modern Workplace Assistant...
✅ SharePoint connected: YourConnection
✅ Agent created: asst_abc123

📋 Policy Question 1/3
❓ What is our remote work policy regarding security requirements?
🤖 According to our remote work policy, security requirements include...

🔧 Technical Question 2/3  
❓ How do I set up Azure Active Directory conditional access?
🤖 To set up Azure AD Conditional Access, follow these steps...

🔄 Implementation Question 3/3
❓ Our security policy requires MFA - how do I implement this in Azure AD?
🤖 Based on our security policy requirements and Azure documentation...
```

**Graceful degradation without SharePoint**:

```text
⚠️  SharePoint connection not found: Connection 'YourConnection' not found
✅ Agent created: asst_abc123

📋 Policy Question 1/3
❓ What is our remote work policy regarding security requirements?
🤖 I don't have access to your company's specific policies. SharePoint integration needs to be configured...
```

## Next steps

This ultra-minimal sample provides the foundation for enterprise AI development:

### Tutorial 2: Governance and Monitoring
- Implement content filtering and safety guardrails
- Add comprehensive evaluation metrics and monitoring  
- Set up continuous evaluation pipelines
- Apply governance policies and compliance controls

### Tutorial 3: Production Deployment
- Deploy agents to Azure AI Foundry with proper scaling
- Implement AI Gateway for cost and usage monitoring
- Add advanced observability and performance tracking
- Set up production-ready security and access controls

### Immediate enhancements
- Add more data sources (Azure AI Search, databases)
- Implement advanced evaluation methods (AI-assisted evaluation)
- Create custom tools for business-specific operations
- Add conversation memory and personalization

## Related content

- [Azure AI Foundry Agent Service overview](../../agents/overview.md)
- [SharePoint tool documentation](../../agents/how-to/tools/sharepoint.md)
- [MCP tool integration](../../agents/how-to/tools/model-context-protocol.md)
- [Multi-agent patterns](../../agents/how-to/connected-agents.md)
