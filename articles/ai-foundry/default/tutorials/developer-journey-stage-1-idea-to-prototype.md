---
title: "Developer journey stage 1: Idea to prototype - Build and evaluate an enterprise agent"
description: "Prototype an enterprise agent: build a single agent with SharePoint grounding and Model Context Protocol (MCP) tools, run batch evaluation, extend to multi-agent, and deploy to Azure AI Foundry."
ms.service: azure-ai-foundry
ms.topic: tutorial
ms.date: 11/11/2025
ms.author: jburchel
author: jonburchel
ms.reviewer: dantaylo
ai.usage: ai-assisted
#customer intent: As a developer I want to quickly prototype an enterprise-grade agent with real data, tools, evaluation, and a deployment path so I can validate feasibility before scaling.
---

# Idea to prototype

This tutorial covers the first stage of the Azure AI Foundry developer journey: from an initial idea to a working prototype. You build a **Modern Workplace Assistant** that combines internal company knowledge with external technical guidance by using the Azure AI Foundry SDK.

**Business scenario**: Create an AI assistant that helps employees by combining:

- **Company policies** (from SharePoint documents)
- **Technical implementation guidance** (from Microsoft Learn via MCP)
- **Complete solutions** (combining both sources for business implementation)
- **Batch evaluation** to validate agent performance on realistic business scenarios

> [!div class="checklist"]
>
> - Build a Modern Workplace Assistant with SharePoint and MCP integration
> - Demonstrate real business scenarios combining internal and external knowledge
> - Implement robust error handling and graceful degradation
> - Create evaluation framework for business-focused testing
> - Prepare foundation for governance and production deployment

This ultra-minimal sample demonstrates enterprise-ready patterns with realistic business scenarios.

## Prerequisites 

- Azure CLI authentication (`az login`)
- An Azure AI Foundry **project** with a deployed model (for example, `gpt-4o-mini`)
- Python 3.10 or later, .NET 7 SDK, or Java 17 SDK installed (depending on your chosen language)
- SharePoint connection configured in your project

> [!NOTE]
> To configure your Azure AI Foundry project for SharePoint connectivity, see the [SharePoint tool documentation](../../agents/how-to/tools/sharepoint.md).

## Step 1: Download and configure the sample code

You can find the complete sample in the Azure AI Foundry samples repository. The ultra-minimal structure contains only essential files:

# [Python](#tab/python)

```text
enterprise-agent-tutorial/
└── 1-idea-to-prototype/
    ├── main.py                        # Modern Workplace Assistant
    ├── evaluate.py                    # Business evaluation framework
    ├── questions.jsonl                # Business test scenarios (4 questions)
    ├── requirements.txt               # Python dependencies
    ├── .env.template                  # Environment variables template
    ├── SAMPLE_SHAREPOINT_CONTENT.md   # Business documents to upload
    ├── README.md                      # Complete setup instructions
    ├── MCP_SERVERS.md                 # MCP server configuration guide
    └── setup_sharepoint.py            # SharePoint diagnostic tool
```

> [!div class="nextstepaction"] 
> [Download the code now](https://github.com/azure-ai-foundry/foundry-samples/tree/nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype)

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
    │   ├── SAMPLE_SHAREPOINT_CONTENT.md # Business documents to upload
    │   ├── MCP_SERVERS.md             # MCP server configuration guide
    │   └── README.md                  # SharePoint setup instructions
    └── README.md                      # Complete setup instructions
```

> [!div class="nextstepaction"] 
> [Download the code now](https://github.com/azure-ai-foundry/foundry-samples/tree/nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype)

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
    ├── SAMPLE_SHAREPOINT_CONTENT.md   # Business documents to upload
    ├── MCP_SERVERS.md                 # MCP server configuration guide
    └── README.md                      # Complete setup instructions
```

> [!div class="nextstepaction"] 
> [Download the code now](https://github.com/azure-ai-foundry/foundry-samples/tree/nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype)

---

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

#### Set up SharePoint business documents for the sample

To demonstrate the complete business scenario, upload sample documents to your SharePoint site using the provided `SAMPLE_SHAREPOINT_CONTENT.md` file:

##### Create business documents

1. **Navigate to your SharePoint site** (configured in your connection)

1. **Create document library** called "Company Policies" (or use existing "Documents")

1. **Upload sample documents** from `SAMPLE_SHAREPOINT_CONTENT.md`:
   - `remote-work-policy.docx` - Remote work security requirements
   - `security-guidelines.docx` - Azure security standards  
   - `collaboration-standards.docx` - Teams and communication policies
   - `data-governance-policy.docx` - Data handling requirements

1. **Copy content** from each section in `SAMPLE_SHAREPOINT_CONTENT.md` into the corresponding Word documents

##### Sample document structure

The sample includes realistic Contoso Corp policies that demonstrate:

```text
📁 Company Policies/
├── 🏠 remote-work-policy.docx      # VPN, MFA, device requirements
├── 🔒 security-guidelines.docx     # Azure security standards
├── 🤝 collaboration-standards.docx # Teams, SharePoint usage
└── 📊 data-governance-policy.docx  # Data classification, retention
```

These documents reference Azure and Microsoft 365 technologies, creating realistic scenarios where employees need both internal policy information and external implementation guidance.

## Step 2: Build a modern workplace assistant

This sample implementation of a modern workplace assistant shows you how to:

- **Integrate multiple agent tools** (SharePoint and MCP) for comprehensive knowledge access.
- **Simplify connection handling** - Use only the connection name, and let Azure AI Foundry handle URL configuration.
- **Use dynamic agent instructions** based on available tools.
- **Combine business-focused scenarios** with internal and external knowledge.
- **Provide clear diagnostic messages** for troubleshooting.
- **Implement graceful degradation** when services are unavailable.

The code breaks down into the following main sections, ordered as they appear in the full sample code:

1. [Configure imports and authentication](#imports-and-authentication-setup).
1. [Configure authentication to Azure](#configure-authentication-in-azure).
1. [Configure the SharePoint tool](#create-the-sharepoint-tool-for-the-agent).
1. [Configure MCP tool](#create-the-mcp-tool-for-the-agent).
1. [Create the agent and connect the tools](#create-the-agent-and-connect-the-tools).
1. [Converse with the agent](#converse-with-the-agent).

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

## Step 3: Evaluate the assistant in a batch

The evaluation framework code in this sample tests realistic business scenarios that combine SharePoint policies with Microsoft Learn technical guidance. This approach demonstrates batch evaluation capabilities for validating agent performance across multiple test cases. The evaluation uses a keyword-based approach to assess whether the agent provides relevant responses that incorporate the expected information sources.

This evaluation framework tests:

- **SharePoint integration** for company policy questions
- **MCP integration** for technical guidance questions  
- **Combined scenarios** that require both internal and external knowledge
- **Response quality** by using keyword matching and length analysis

The code breaks down into the following main sections, ordered as they appear in the full sample code:

1. [Load evaluation data](#load-evaluation-data).
1. [Run batch evaluation](#run-batch-evaluation).
1. [Compile evaluation results](#compile-evaluation-results).

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

In this section, the evaluation framework runs the agent against each test question in a batch and evaluates the responses.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/evaluate.py" id="run_batch_evaluation":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype/Evaluate/program.cs" id="run_batch_evaluation":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype/src/main/java/com/microsoft/azure/samples/EvaluateAgent.java" id="run_batch_evaluation":::

---

### Compile evaluation results

Finally, the evaluation framework compiles and outputs the results of the batch evaluation.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/evaluate.py" id="evaluation_results":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-nov25-updates/samples/microsoft/csharp/enterprise-agent-tutorial/1-idea-to-prototype/Evaluate/program.cs" id="evaluation_results":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-nov25-updates/samples/microsoft/java/enterprise-agent-tutorial/1-idea-to-prototype/src/main/java/com/microsoft/azure/samples/EvaluateAgent.java" id="evaluation_results":::

---

## Step 4: Run the complete sample

After you set up the environment, dependencies, and code, you can run the complete sample.

### Set up and run

# [Python](#tab/python)

1. **Configure environment**:

```bash
cp .env.template .env
# Edit .env with your Azure AI Foundry project details
pip install -r requirements.txt
```

2. **Run the Modern Workplace Assistant**:

```bash
python main.py
```

3. **Run business evaluation**:

```bash
python evaluate.py
```

# [C#](#tab/csharp)

1. **Configure environment**:

```bash
cp .env.template .env
# Edit .env with your Azure AI Foundry project details
dotnet restore
```

2. **Run the Modern Workplace Assistant**:

```bash
dotnet run
```

3. **Run business evaluation**:

```bash
dotnet run --project Evaluate
```

# [Java](#tab/java)

1. **Configure environment**:

```bash
cp .env.template .env
# Edit .env with your Azure AI Foundry project details
mvn clean compile
```

2. **Run the Modern Workplace Assistant**:

```bash
mvn exec:java -Dexec.mainClass="Main"
```

3. **Run business evaluation**:

```bash
mvn exec:java -Dexec.mainClass="Evaluate"
```

---

This example demonstrates:
- SharePoint connection diagnostics  
- Agent creation with dynamic instructions
- Three business scenarios (policy, technical, combined)
- Interactive mode for testing

The evaluation tests:
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

### Tutorial 2: Governance and monitoring
- Implement content filtering and safety guardrails
- Add comprehensive evaluation metrics and monitoring  
- Set up continuous evaluation pipelines
- Apply governance policies and compliance controls

### Tutorial 3: Production deployment
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
