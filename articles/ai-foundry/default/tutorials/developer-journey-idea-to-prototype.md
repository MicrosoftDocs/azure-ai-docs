---
title: "Tutorial: Idea to prototype - Build and evaluate an enterprise agent"
description: "Prototype an enterprise agent: build a single agent with SharePoint grounding and Model Context Protocol (MCP) tools, run batch evaluation, extend to multi-agent, and deploy to Microsoft Foundry."
ms.service: azure-ai-foundry
ms.topic: tutorial
ms.date: 11/18/2025
ms.author: jburchel
author: jonburchel
ms.reviewer: dantaylo
ai.usage: ai-assisted
#customer intent: As a developer I want to quickly prototype an enterprise-grade agent with real data, tools, evaluation, and a deployment path so I can validate feasibility before scaling.
---

# Tutorial: Idea to prototype - Build and evaluate an enterprise agent


This tutorial covers the first stage of the Microsoft Foundry developer journey: from an initial idea to a working prototype. You build a **modern workplace assistant** that combines internal company knowledge with external technical guidance by using the Microsoft Foundry SDK.

**Business scenario**: Create an AI assistant that helps employees by combining:

- **Company policies** (from SharePoint documents)
- **Technical implementation guidance** (from Microsoft Learn via MCP)
- **Complete solutions** (combining both sources for business implementation)
- **Batch evaluation** to validate agent performance on realistic business scenarios

**Tutorial outcome**: By the end you have a running Modern Workplace Assistant that can answer policy, technical, and combined implementation questions; a repeatable batch evaluation script; and clear extension points (other tools, multi‑agent patterns, richer evaluation).

> [!div class="checklist"]
> **You will:**
> - Build a Modern Workplace Assistant with SharePoint and MCP integration.
> - Demonstrate real business scenarios combining internal and external knowledge.
> - Implement robust error handling and graceful degradation.
> - Create evaluation framework for business-focused testing.
> - Prepare foundation for governance and production deployment.

This minimal sample demonstrates enterprise-ready patterns with realistic business scenarios.


[!INCLUDE [code-preview](../includes/code-preview.md)] 


## Prerequisites 

- Azure subscription and CLI authentication (`az login`)
- Azure CLI 2.67.0 or later (check with `az version`)
- A Foundry **project** with a deployed model (for example, `gpt-4o-mini`). If you don't have one: [Create a project](../../how-to/create-projects.md) and then deploy a model (see model overview: [Model catalog](../../concepts/foundry-models-overview.md)). 
- Python 3.10 or later
- SharePoint connection configured in your project ([SharePoint tool documentation](../../agents/how-to/tools/sharepoint.md))

  > [!NOTE]
  > To configure your Foundry project for SharePoint connectivity, see the [SharePoint tool documentation](../../agents/how-to/tools/sharepoint.md).

- (Optional) Git installed for cloning the sample repository


## Step 1: Get the sample code

<!-- Instead of navigating a large repository tree, use one of these approaches:

#### Option A (clone entire samples repo)

[!INCLUDE [agent-v2](../includes/agent-v2.md)]

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
-->

Download the repository ZIP, extract it to your local environment, and go to the tutorial folder.

> [!IMPORTANT]
> For production adoption, use a standalone repository. This tutorial uses the shared samples repo. Sparse checkout minimizes local noise.
> [!div class="nextstepaction"] 
> [Download the Python code now](https://github.com/azure-ai-foundry/foundry-samples/tree/nov25-updates/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype)

The minimal structure contains only essential files:

```text
enterprise-agent-tutorial/
└── 1-idea-to-prototype/
    ├── main.py                          # Modern Workplace Assistant
    ├── evaluate.py                      # Business evaluation framework
    ├── questions.jsonl                  # Business test scenarios (4 questions)
    ├── requirements.txt                 # Python dependencies
    ├── .env.template                    # Environment variables template
    ├── README.md                        # Complete setup instructions
    ├── MCP_SERVERS.md                   # MCP server configuration guide
    ├── sharepoint-sample-data           # Sample business documents for SharePoint
        └── collaboration-standards.docx # Sample content for policies
        └── remote-work-policy.docx      # Sample content for policies
        └── security-guidelines.docx     # Sample content for policies
        └── data-governance-policy.docx  # Sample content for policies
```

## Step 2: Run the sample immediately

Start by running the agent so you see working functionality before diving into implementation details.

### Environment setup and virtual environment

1. Install the required language runtimes, global tools, and VS Code extensions as described in [Prepare your development environment](../../how-to/develop/install-cli-sdk.md).

1. Install dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)] 
1. Configure `.env`.

   Copy `.env.template` to `.env` and configure:
  
   ```bash
   # Foundry Configuration  
   PROJECT_ENDPOINT=https://<your-project>.aiservices.azure.com
   MODEL_DEPLOYMENT_NAME=gpt-4o-mini
   AI_FOUNDRY_TENANT_ID=<your-tenant-id>
   
   # The Microsoft Learn MCP Server (public authoritative Microsoft docs index)
   MCP_SERVER_URL=https://learn.microsoft.com/api/mcp
   
   # SharePoint Integration (Optional - requires connection setup)
   SHAREPOINT_RESOURCE_NAME=your-sharepoint-connection
   SHAREPOINT_SITE_URL=https://<your-company>.sharepoint.com/teams/your-site
   ```
   
   > [!TIP]
   > To get your **tenant ID**, run:
   > 
   > ```bash
   > # Get tenant ID
   > az account show --query tenantId -o tsv
   > ```
   > 
   > To get your **project endpoint**, open your project in the [Foundry portal](https://ai.azure.com) and copy the value shown there.

### Run agent and evaluation

```bash
python main.py
python evaluate.py
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

Now that you have a working agent, the next sections explain how it works. You don't need to take any action while reading these sections—they're for explanation.


## Step 3: Set up sample SharePoint business documents

1. Go to your SharePoint site (configured in the connection).
1. Create document library "Company Policies" (or use existing "Documents").
1. Upload the four sample Word documents provided in the `sharepoint-sample-data` folder:
   - `remote-work-policy.docx`
   - `security-guidelines.docx`  
   - `collaboration-standards.docx`
   - `data-governance-policy.docx`

### Sample structure

```text
📁 Company Policies/
├── remote-work-policy.docx      # VPN, MFA, device requirements
├── security-guidelines.docx     # Azure security standards
├── collaboration-standards.docx # Teams, SharePoint usage
└── data-governance-policy.docx  # Data classification, retention
```

## Step 4: Understand the assistant implementation

This section explains the core code in `main.py`. You already ran the agent; this section is conceptual and requires no changes. After reading it, you can:
- Add new internal and external data tools.
- Extend dynamic instructions.
- Introduce multi-agent orchestration.
- Enhance observability and diagnostics.

The code breaks down into the following main sections, ordered as they appear in the full sample code:

1. [Configure imports and authentication](#imports-and-authentication-setup)
1. [Configure authentication to Azure](#configure-authentication-in-azure)
1. [Configure the SharePoint tool](#create-the-sharepoint-tool-for-the-agent)
1. [Configure MCP tool](#create-the-mcp-tool-for-the-agent)
1. [Create the agent and connect the tools](#create-the-agent-and-connect-the-tools)
1. [Converse with the agent](#converse-with-the-agent)

[!INCLUDE [code-preview](../includes/code-preview.md)] 

### Imports and authentication setup

The code uses several client libraries from the Microsoft Foundry SDK to create a robust enterprise agent.

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="imports_and_includes":::

### Configure authentication in Azure

Before you create your agent, set up authentication to the Foundry.

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="agent_authentication":::

### Create the SharePoint tool for the agent

The agent uses SharePoint and can access company policy and procedure documents stored there. Set up the connection to SharePoint in your code.

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="sharepoint_tool_setup":::

### Create the MCP tool for the agent

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="mcp_tool_setup":::

### Create the agent and connect the tools

Now, create the agent and connect the SharePoint and MCP tools.

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="create_agent_with_tools":::

### Converse with the agent

Finally, implement an interactive loop to converse with the agent.

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="agent_conversation":::

### Expected output from agent sample code (main.py)

When you run the agent, you see output similar to the following example. The output shows successful tool configuration and agent responses to business scenarios:

```bash
$ python main.py
✅ Connected to Foundry
🚀 Foundry - Modern Workplace Assistant
Tutorial 1: Building Enterprise Agents with Agent SDK v2
======================================================================
🤖 Creating Modern Workplace Assistant...
📁 Configuring SharePoint integration...
   Connection name: ContosoCorpPoliciesProcedures
   🔍 Resolving connection name to ARM resource ID...
   ✅ Resolved
✅ SharePoint tool configured successfully
📚 Configuring Microsoft Learn MCP integration...
   Server URL: https://learn.microsoft.com/api/mcp
✅ MCP tool configured successfully
🛠️  Creating agent with model: gpt-4o-mini
   ✓ SharePoint tool added
   ✓ MCP tool added
   Total tools: 2
✅ Agent created successfully

======================================================================
🏢 MODERN WORKPLACE ASSISTANT - BUSINESS SCENARIO DEMONSTRATION
======================================================================
This demonstration shows how AI agents solve real business problems
using the Azure AI Agents SDK v2.
======================================================================

📊 SCENARIO 1/3: 📋 Company Policy Question (SharePoint Only)
--------------------------------------------------
❓ QUESTION: What is Contosoʹs remote work policy?
🎯 BUSINESS CONTEXT: Employee needs to understand company-specific remote work requirements
🎓 LEARNING POINT: SharePoint tool retrieves internal company policies
--------------------------------------------------
🤖 ASSISTANT RESPONSE:
✅ SUCCESS: Contosoʹs remote work policy, effective January 2024, outlines the following key points:

### Overview
Contoso Corp supports flexible work arrangements, including remote work, to enhance employee productivity and work-life balance.

### Eligibility
- **Full-time Employees**: Must have completed a 90...
   📏 Full response: 1530 characters
📈 STATUS: completed
--------------------------------------------------

📊 SCENARIO 2/3: 📚 Technical Documentation Question (MCP Only)
--------------------------------------------------
❓ QUESTION: According to Microsoft Learn, what is the correct way to implement Azure AD Conditional Access policies? Please include reference links to the official documentation.
🎯 BUSINESS CONTEXT: IT administrator needs authoritative Microsoft technical guidance
🎓 LEARNING POINT: MCP tool accesses Microsoft Learn for official documentation with links
--------------------------------------------------
🤖 ASSISTANT RESPONSE:
✅ SUCCESS: To implement Azure AD Conditional Access policies correctly, follow these key steps outlined in the Microsoft Learn documentation:

### 1. Understanding Conditional Access
Conditional Access policies act as "if-then" statements that enforce organizational access controls based on various signals. Th...
   📏 Full response: 2459 characters
📈 STATUS: completed
--------------------------------------------------

📊 SCENARIO 3/3: 🔄 Combined Implementation Question (SharePoint + MCP)
--------------------------------------------------
❓ QUESTION: Based on our companyʹs remote work security policy, how should I configure my Azure environment to comply? Please include links to Microsoft documentation showing how to implement each requirement.
🎯 BUSINESS CONTEXT: Need to map company policy to technical implementation with official guidance
🎓 LEARNING POINT: Both tools work together: SharePoint for policy + MCP for implementation docs
--------------------------------------------------
🤖 ASSISTANT RESPONSE:
✅ SUCCESS: To configure your Azure environment in compliance with Contoso Corpʹs remote work security policy, you need to focus on several key areas, including enabling Multi-Factor Authentication (MFA), utilizing Azure Security Center, and implementing proper access management. Below are specific steps and li...
   📏 Full response: 3436 characters
📈 STATUS: completed
--------------------------------------------------

✅ DEMONSTRATION COMPLETED!
🎓 Key Learning Outcomes:
   • Agent SDK v2 usage for enterprise AI
   • Proper thread and message management
   • Real business value through AI assistance
   • Foundation for governance and monitoring (Tutorials 2-3)

🎯 Try interactive mode? (y/n): n

🎉 Sample completed successfully!
📚 This foundation supports Tutorial 2 (Governance) and Tutorial 3 (Production)
🔗 Next: Add evaluation metrics, monitoring, and production deployment
```

## Step 5: Evaluate the assistant in a batch

The evaluation framework code tests realistic business scenarios that combine SharePoint policies with Microsoft Learn technical guidance. This approach demonstrates batch evaluation capabilities for validating agent performance across multiple test cases. The evaluation uses a keyword-based approach to assess whether the agent provides relevant responses that incorporate the expected information sources.

This evaluation framework tests:

- **SharePoint integration** for company policy questions
- **MCP integration** for technical guidance questions  
- **Combined scenarios** that require both internal and external knowledge
- **Response quality** by using keyword matching and length analysis

The code breaks down into the following main sections:

1. [Load evaluation data](#load-evaluation-data).
1. [Run batch evaluation](#run-batch-evaluation).
1. [Compile evaluation results](#compile-evaluation-results).

### Load evaluation data

In this section, the evaluation framework loads test questions from `questions.jsonl`. The file contains business scenarios that test different aspects of the agent:

:::code language="jsonl" source="~/foundry-samples-main/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/questions.jsonl":::

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/evaluate.py" id="load_test_data":::

### Run batch evaluation

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/evaluate.py" id="run_batch_evaluation":::

### Compile evaluation results

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/enterprise-agent-tutorial/1-idea-to-prototype/evaluate.py" id="evaluation_results":::

### Expected output from evaluation sample code (evaluate.py)

When you run the evaluation script, you see output similar to the following example. The output shows successful execution of business test scenarios and generation of evaluation metrics:

```bash
python evaluate.py
✅ Connected to Foundry
🧪 Modern Workplace Assistant - Evaluation (Agent SDK v2)
======================================================================
🤖 Creating Modern Workplace Assistant...
📁 Configuring SharePoint integration...
   Connection name: ContosoCorpPoliciesProcedures
   🔍 Resolving connection name to ARM resource ID...
   ✅ Resolved
✅ SharePoint tool configured successfully
📚 Configuring Microsoft Learn MCP integration...
   Server URL: https://learn.microsoft.com/api/mcp
✅ MCP tool configured successfully
🛠️  Creating agent with model: gpt-4o-mini
   ✓ SharePoint tool added
   ✓ MCP tool added
   Total tools: 2
✅ Agent created successfully
   Model: gpt-4o-mini
   Name: Modern Workplace Assistant
======================================================================
🧪 Running evaluation with 12 test questions...
======================================================================

📝 Question 1/12 [SHAREPOINT_ONLY]
   What is Contosoʹs remote work policy?...
✅ Status: completed | Tool check: Contoso-specific content: True

...

📝 Question 5/12 [MCP_ONLY]
   According to Microsoft Learn documentation, what is the correct way to set up Az...
✅ Status: completed | Tool check: Microsoft Learn links: True

...

📝 Question 12/12 [HYBRID]
   What Azure security services should I implement to align with Contosoʹs incident...
✅ Status: completed | Tool check: Contoso content: True, Learn links: True

======================================================================
📊 EVALUATION SUMMARY BY TEST TYPE:
======================================================================
✅ SHAREPOINT_ONLY: 4/4 passed (100.0%)
✅ MCP_ONLY: 4/4 passed (100.0%)
✅ HYBRID: 4/4 passed (100.0%)

📊 Overall Evaluation Results: 12/12 questions passed (100.0%)
💾 Results saved to evaluation_results.json
```

### Additional evaluation assets

The evaluation generates `evaluation_results.json` with metrics for each question (keyword hits, length heuristic). You can extend this file to:
- Use model-based scoring prompts.
- Introduce structured output validation.
- Record latency and token usage.

Here's a sample of the JSON output structure:

```json
[
  {
    "question": "What is Contoso's remote work policy?",
    "response": "Contoso's remote work policy includes the following key components: <...>",
    "status": "completed",
    "passed": true,
    "validation_details": "Contoso-specific content: True",
    "test_type": "sharepoint_only",
    "expected_source": "sharepoint",
    "explanation": "Forces SharePoint tool usage - answer must contain Contoso-specific policy details"
  },
  {
    "question": "What are Contoso's security protocols for remote employees?",
    "response": ...

    ...

  }
]
```


## Summary

You now have:
- A working single-agent prototype grounded in internal and external knowledge.
- A repeatable evaluation script demonstrating enterprise validation patterns.
- Clear upgrade path: more tools, multi-agent orchestration, richer evaluation, deployment.

These patterns reduce prototype-to-production friction: you can add data sources, enforce governance, and integrate monitoring without rewriting core logic.


## Next steps

This tutorial demonstrates **Stage 1** of the developer journey - from idea to prototype. This minimal sample provides the foundation for enterprise AI development. To continue your journey, explore the next stages:

### Suggested additional enhancements
- Add more data sources ([Azure AI Search](../../agents/how-to/tools/azure-ai-search.md), [other sources](../../how-to/connections-add.md)).
- Implement advanced evaluation methods ([AI-assisted evaluation](../../how-to/develop/evaluate-sdk.md)).
- Create [custom tools](../agents/how-to/private-tool-catalog.md) for business-specific operations.
- Add [conversation memory and personalization](/azure/cosmos-db/gen-ai/azure-agent-service).

### Stage 2: Prototype to production

- [Implement safety assessment with red-team testing](../../how-to/develop/run-scans-ai-red-teaming-agent.md).
- [Create comprehensive evaluation datasets with quality metrics](../fine-tuning/data-generation.md).
- [Apply organization-wide governance policies and model comparison](../../how-to/built-in-policy-model-deployment.md).
- [Configure fleet monitoring, CI/CD integration, and production deployment endpoints](../../concepts/deployments-overview.md).

### Stage 3: Production to adoption

- [Collect trace data and user feedback from production deployments](../observability/how-to/trace-agent-framework.md).
- [Fine-tune models and generate evaluation insights for continuous improvement](../../openai/how-to/fine-tuning.md).
- [Integrate Azure API Management gateway with continuous quality monitoring](../configuration/enable-ai-api-management-gateway-portal.md).
- [Implement fleet governance, compliance controls, and cost optimization](/azure/cloud-adoption-framework/scenarios/ai/platform/governance).

## Related content

- [Foundry Agent Service overview](../../agents/overview.md)
- [SharePoint tool documentation](../../agents/how-to/tools/sharepoint.md)
- [MCP tool integration](../../agents/how-to/tools/model-context-protocol.md)
- [Multi-agent patterns](../../agents/how-to/connected-agents.md)
