---
title: "Tutorial: Idea to prototype - Build and evaluate an enterprise agent"
description: "Prototype an enterprise agent: build a single agent with SharePoint grounding and Model Context Protocol (MCP) tools, run batch evaluation, extend to multi-agent, and deploy to Microsoft Foundry."
ms.service: azure-ai-foundry
ms.topic: tutorial
ms.date: 02/10/2026
ms.author: jburchel
author: jonburchel
ms.reviewer: dantaylo
ai-usage: ai-assisted
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

- An Azure subscription. If you don't have one, [create one for free](https://azure.microsoft.com/free).
- Azure CLI 2.67.0 or later, authenticated with `az login` (check with `az version`)
- A Foundry **project** with a deployed model (for example, `gpt-4o-mini`). If you don't have one: [Create a project](../../how-to/create-projects.md) and then deploy a model (see model overview: [Model catalog](../../concepts/foundry-models-overview.md)). 
- Python 3.10 or later
- .NET SDK 8.0 or later (for the C# sample)
- SharePoint connection configured in your project ([SharePoint tool documentation](../agents/how-to/tools/sharepoint.md))

  > [!NOTE]
  > To configure your Foundry project for SharePoint connectivity, see the [SharePoint tool documentation](../agents/how-to/tools/sharepoint.md).

- (Optional) Git installed for cloning the sample repository


## Step 1: Get the sample code

Instead of navigating a large repository tree, use one of these approaches:

#### Option A (clone entire samples repo)

[!INCLUDE [agent-v2](../includes/agent-v2.md)]

# [Python](#tab/python)

```bash
git clone --depth 1 https://github.com/microsoft-foundry/foundry-samples.git
cd foundry-samples/samples/python/enterprise-agent-tutorial/1-idea-to-prototype
```

# [C#](#tab/csharp)

```bash
git clone --depth 1 https://github.com/azure-ai-foundry/foundry-samples.git
cd foundry-samples/samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype
```

---

#### Option B (sparse checkout only this tutorial - reduced download)

# [Python](#tab/python)

```bash
git clone --no-checkout https://github.com/microsoft-foundry/foundry-samples.git
cd foundry-samples
git sparse-checkout init --cone
git sparse-checkout set samples/python/enterprise-agent-tutorial/1-idea-to-prototype
git checkout
cd samples/python/enterprise-agent-tutorial/1-idea-to-prototype
```

# [C#](#tab/csharp)

```bash
git clone --no-checkout https://github.com/azure-ai-foundry/foundry-samples.git
cd foundry-samples
git sparse-checkout init --cone
git sparse-checkout set samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype
git checkout
cd samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype
```

---

#### Option C (Download ZIP of repository)

Download the repository ZIP, extract it to your local environment, and go to the tutorial folder.

> [!IMPORTANT]
> For production adoption, use a standalone repository. This tutorial uses the shared samples repo. Sparse checkout minimizes local noise.

# [Python](#tab/python)

> [!div class="nextstepaction"] 
> [Download the Python code now](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/enterprise-agent-tutorial/1-idea-to-prototype)

After you extract the ZIP, go to `samples/python/enterprise-agent-tutorial/1-idea-to-prototype`.

# [C#](#tab/csharp)

> [!div class="nextstepaction"] 
> [Download the C# code now](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype)

After you extract the ZIP, go to `samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype`.

---

The minimal structure contains only essential files:

# [Python](#tab/python)

```text
enterprise-agent-tutorial/
└── 1-idea-to-prototype/
   ├── .env                             # Create this file (local environment variables)
   ├── .gitkeep
   ├── evaluate.py                      # Business evaluation framework
   ├── evaluation_results.json
   ├── main.py                          # Modern Workplace Assistant
   ├── questions.jsonl                  # Business test scenarios (4 questions)
   ├── requirements.txt                 # Python dependencies
   └── sharepoint-sample-data/          # Sample business documents for SharePoint
      ├── collaboration-standards.docx
      ├── data-governance-policy.docx
      ├── remote-work-policy.docx
      └── security-guidelines.docx
```

# [C#](#tab/csharp)

```text
enterprise-agent-tutorial/
└── 1-idea-to-prototype/
   ├── ModernWorkplaceAssistant/        # Modern Workplace Assistant
   │   ├── Program.cs                   # Agent implementation with SharePoint + MCP
   │   ├── ModernWorkplaceAssistant.csproj
   │   └── .env                         # Environment variables (create this)
   ├── Evaluate/                        # Cloud evaluation framework
   │   ├── Program.cs                   # Cloud evaluation with built-in evaluators
   │   ├── Evaluate.csproj
   │   └── evaluation_results.json      # Example output (generated)
   ├── questions.jsonl                  # Business test scenarios
   └── README.md                        # Complete setup instructions
```

---

## Step 2: Run the sample immediately

Start by running the agent so you see working functionality before diving into implementation details.

### Environment setup and virtual environment

1. Install the required language runtimes, global tools, and VS Code extensions as described in [Prepare your development environment](../../how-to/develop/install-cli-sdk.md).

1. Verify that your `requirements.txt` uses these published package versions:

   ```text
   azure-ai-projects==2.0.0b3
   azure-identity
   python-dotenv
   openai
   ```

1. Install dependencies:

   # [Python](#tab/python)

   ```bash
   python -m pip install -r requirements.txt
   ```

   # [C#](#tab/csharp)

   ```bash
   cd ModernWorkplaceAssistant
   dotnet restore

   cd ../Evaluate
   dotnet restore
   ```
   ---

   Verify the install succeeded. You should see `Successfully installed azure-ai-projects-...` (Python) or `Restore completed` (.NET) with no errors.

1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)] 
1. Configure `.env`.

   Set the environment values required for your language.

# [Python](#tab/python)

Copy `.env.template` to `.env`.

# [C#](#tab/csharp)

Create a `.env` file in the `ModernWorkplaceAssistant` directory.

---

# [Python](#tab/python)

```dotenv
# Foundry configuration
PROJECT_ENDPOINT=https://<your-project>.aiservices.azure.com
MODEL_DEPLOYMENT_NAME=gpt-4o-mini

# The Microsoft Learn MCP Server (optional)
MCP_SERVER_URL=https://learn.microsoft.com/api/mcp

# SharePoint integration (optional - requires connection name)
SHAREPOINT_CONNECTION_NAME=<your-sharepoint-connection-name>
```

# [C#](#tab/csharp)

```dotenv
# Foundry configuration
PROJECT_ENDPOINT=https://<your-project>.aiservices.azure.com
MODEL_DEPLOYMENT_NAME=gpt-4o-mini

# SharePoint integration (optional - requires connection name)
SHAREPOINT_CONNECTION_NAME=<your-sharepoint-connection-name>

# The Microsoft Learn MCP Server (optional)
MCP_SERVER_URL=https://learn.microsoft.com/api/mcp
```

---

   Confirm `.env` contains valid values by opening the file and verifying that `PROJECT_ENDPOINT` starts with `https://` and `MODEL_DEPLOYMENT_NAME` matches the name of a deployed model in your project.

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

# [Python](#tab/python)

```bash
python main.py
python evaluate.py
```

# [C#](#tab/csharp)

```bash
cd ModernWorkplaceAssistant
dotnet restore
dotnet run

cd ../Evaluate
dotnet restore
dotnet run
```

---

### Expected output (agent first run)

Successful run with SharePoint:

```text
🤖 Creating Modern Workplace Assistant...
✅ SharePoint tool configured successfully
✅ Agent created successfully (name: Modern Workplace Assistant, version: 1)
```

Graceful degradation without SharePoint:

```text
📁 SharePoint integration skipped (SHAREPOINT_CONNECTION_NAME not set)
✅ Agent created successfully (name: Modern Workplace Assistant, version: 1)
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

1. Verify that four documents appear in the library before proceeding.

### Sample structure

```text
📁 Company Policies/
├── remote-work-policy.docx      # VPN, MFA, device requirements
├── security-guidelines.docx     # Azure security standards
├── collaboration-standards.docx # Teams, SharePoint usage
└── data-governance-policy.docx  # Data classification, retention
```

## Understand the assistant implementation

> [!NOTE]
> This section is for reference only — no action needed. It explains the code you already ran.

This section explains the core code in `main.py` (Python) or `ModernWorkplaceAssistant/Program.cs` (C#). You already ran the agent. After reading it, you can:
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

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="imports_and_includes":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="imports_and_includes":::

---

### Configure authentication in Azure

Before you create your agent, set up authentication to the Foundry.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="agent_authentication":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="agent_authentication":::

---

### Create the SharePoint tool for the agent

The agent uses SharePoint and can access company policy and procedure documents stored there. Set up the connection to SharePoint in your code.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="sharepoint_tool_setup":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="sharepoint_tool_setup":::

---

### Create the MCP tool for the agent

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="mcp_tool_setup":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="mcp_tool_setup":::

---

### Create the agent and connect the tools

Create the agent and connect the SharePoint and MCP tools.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="create_agent_with_tools":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="create_agent_with_tools":::

---

### Converse with the agent

Finally, implement an interactive loop to converse with the agent.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/enterprise-agent-tutorial/1-idea-to-prototype/main.py" id="agent_conversation":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype/ModernWorkplaceAssistant/Program.cs" id="agent_conversation":::

---

### Expected output from agent sample code

When you run the agent, you see output similar to the following example. The output shows successful tool configuration and agent responses to business scenarios:

```bash
✅ Connected to Foundry
🚀 Foundry - Modern Workplace Assistant
Tutorial 1: Building Enterprise Agents with Microsoft Foundry SDK
======================================================================
🤖 Creating Modern Workplace Assistant...
📁 Configuring SharePoint integration...
   Connection ID: /subscriptions/.../connections/ContosoCorpPoliciesProcedures
✅ SharePoint tool configured successfully
📚 Configuring Microsoft Learn MCP integration...
   Server URL: https://learn.microsoft.com/api/mcp
✅ MCP tool configured successfully
🛠️  Creating agent with model: gpt-4o-mini
   ✓ SharePoint tool added
   ✓ MCP tool added
   Total tools: 2
✅ Agent created successfully (name: Modern Workplace Assistant, version: 1)

======================================================================
🏢 MODERN WORKPLACE ASSISTANT - BUSINESS SCENARIO DEMONSTRATION
======================================================================
This demonstration shows how AI agents solve real business problems
using the Microsoft Foundry SDK.
======================================================================

📊 SCENARIO 1/3: 📋 Company Policy Question (SharePoint Only)
--------------------------------------------------
❓ QUESTION: What is Contosoʹs remote work policy?
🎯 BUSINESS CONTEXT: Employee needs to understand company-specific remote work requirements
🎓 LEARNING POINT: SharePoint tool retrieves internal company policies
--------------------------------------------------
🤖 AGENT RESPONSE:
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
🤖 AGENT RESPONSE:
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
🤖 AGENT RESPONSE:
✅ SUCCESS: To configure your Azure environment in compliance with Contoso Corpʹs remote work security policy, you need to focus on several key areas, including enabling Multi-Factor Authentication (MFA), utilizing Azure Security Center, and implementing proper access management. Below are specific steps and li...
   📏 Full response: 3436 characters
📈 STATUS: completed
--------------------------------------------------

✅ DEMONSTRATION COMPLETED!
🎓 Key Learning Outcomes:
   • Microsoft Foundry SDK usage for enterprise AI
   • Conversation management via the Responses API
   • Real business value through AI assistance
   • Foundation for governance and monitoring (Tutorials 2-3)

🎯 Try interactive mode? (y/n): n

🎉 Sample completed successfully!
📚 This foundation supports Tutorial 2 (Governance) and Tutorial 3 (Production)
🔗 Next: Add evaluation metrics, monitoring, and production deployment
```

## Step 4: Evaluate the assistant by using cloud evaluation

The evaluation framework tests realistic business scenarios by using the **cloud evaluation** capability of the Microsoft Foundry SDK. Instead of a custom local approach, this pattern uses the built-in evaluators (`builtin.violence`, `builtin.fluency`, `builtin.task_adherence`) and the `openai_client.evals` API to run scalable, repeatable evaluations in the cloud.

This evaluation framework demonstrates:

- **Agent targeting**: The evaluation runs queries directly against your agent by using `azure_ai_target_completions`.
- **Built-in evaluators**: Safety (violence detection), quality (fluency), and task adherence metrics.
- **Cloud-based execution**: Eliminates local compute requirements and supports CI/CD integration.
- **Structured results**: Pass/fail labels, scores, and reasoning for each test case.

The code breaks down into the following main sections:

1. [Configure the evaluation](#configure-the-evaluation).
1. [Run the cloud evaluation](#run-the-cloud-evaluation).
1. [Retrieve evaluation results](#retrieve-evaluation-results).

> [!TIP]
> For detailed guidance on cloud evaluations, see [Run evaluations in the cloud](../../how-to/develop/cloud-evaluation.md). To find a comprehensive list of built-in evaluators available in Foundry, see [Observability in generative AI](../../concepts/observability.md). 

> [!NOTE]
> The C# SDK uses **protocol methods** with `BinaryData` and `BinaryContent` instead of typed objects. This approach requires helper methods to parse JSON responses. See the [C# Evaluations SDK sample](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects/samples/Sample21_Evaluations.md) for the complete pattern.

### Configure the evaluation

First, create an evaluation object that defines your data schema and testing criteria. The evaluation uses built-in evaluators for violence detection, fluency, and task adherence.

In Python, use the OpenAI client directly. In C#, get an `EvaluationClient` from the project client:

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/enterprise-agent-tutorial/1-idea-to-prototype/evaluate.py" id="configure_evaluation":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype/Evaluate/Program.cs" id="configure_evaluation":::

---

The `testing_criteria` array specifies which evaluators to run:

- `builtin.violence`: Detects violent or harmful content in responses.
- `builtin.fluency`: Assesses response quality and readability (requires a model deployment).
- `builtin.task_adherence`: Evaluates whether the agent followed instructions correctly.

### Run the cloud evaluation

Create an evaluation run that targets your agent. The `azure_ai_target_completions` data source sends queries to your agent and captures responses for evaluation:

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/enterprise-agent-tutorial/1-idea-to-prototype/evaluate.py" id="run_cloud_evaluation":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype/Evaluate/Program.cs" id="run_cloud_evaluation":::

---

The `data_source` configuration:

- **type**: `azure_ai_target_completions` routes queries through your agent
- **source**: Inline content with test queries (you can also use a dataset file ID)
- **input_messages**: Template that formats each query for the agent
- **target**: Specifies the agent name and version to evaluate

### Retrieve evaluation results

Poll the evaluation run until it completes, then retrieve the detailed output items:

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/enterprise-agent-tutorial/1-idea-to-prototype/evaluate.py" id="retrieve_evaluation_results":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/enterprise-agent-tutorial/1-idea-to-prototype/Evaluate/Program.cs" id="retrieve_evaluation_results":::

---

Each output item includes:

- **Label**: Binary "pass" or "fail" result
- **Score**: Numeric score on the evaluator's scale
- **Reason**: Explanation of why the score was assigned (for LLM-based evaluators)

### Expected output from cloud evaluation (evaluate.py)

When you run the evaluation script, you see output similar to the following example. The output shows the evaluation object creation, run submission, and results retrieval:

```bash
python evaluate.py
Agent created (name: Modern_Workplace_Assistant, version: 1)
Evaluation created (id: eval_xyz789, name: Agent Evaluation)
Evaluation run created (id: run_def456)
Waiting for eval run to complete... current status: running
Waiting for eval run to complete... current status: running

✓ Evaluation run completed successfully!
Result Counts: {'passed': 2, 'failed': 0, 'errored': 0}

OUTPUT ITEMS (Total: 2)
------------------------------------------------------------
[OutputItem(id='item_1', 
            sample={'query': 'What is the largest city in France?', 
                    'output_text': 'The largest city in France is Paris...'},
            results=[{'name': 'violence_detection', 'passed': True, 'score': 0},
                     {'name': 'fluency', 'passed': True, 'score': 4, 
                      'reason': 'Response is clear and well-structured'},
                     {'name': 'task_adherence', 'passed': True, 'score': 5}]),
 OutputItem(id='item_2', ...)]
------------------------------------------------------------
Eval Run Report URL: https://ai.azure.com/...
Evaluation deleted
Agent deleted
```

### Understanding evaluation results

Cloud evaluations provide structured results that you can view in the Foundry portal or retrieve programmatically. Each output item includes:

| Field | Description |
| ------- | ------------- |
| **Label** | Binary "pass" or "fail" based on the threshold |
| **Score** | Numeric score (scale depends on evaluator type) |
| **Threshold** | The cutoff value that determines pass/fail |
| **Reason** | LLM-generated explanation for the score (when applicable) |

**Score scales by evaluator type:**

- **Quality evaluators** (fluency, coherence): 1-5 scale
- **Safety evaluators** (violence, self-harm): 0-7 severity scale (lower is safer)
- **Task evaluators** (task_adherence): 1-5 scale

You can also view detailed results in the Foundry portal by selecting **Evaluation** from your project and selecting the evaluation run. The portal provides visualizations, filtering, and export options.

> [!TIP]
> For production scenarios, consider running evaluations as part of your CI/CD pipeline. See [How to run an evaluation in Azure DevOps](../../how-to/evaluation-azure-devops.md), and [Continuously evaluate your AI agents](../../how-to/continuous-evaluation-agents.md) for integration patterns.

## Troubleshooting

| Symptom | Cause | Resolution |
|---------|-------|------------|
| `DefaultAzureCredential` authentication error | Azure CLI session expired or not signed in | Run `az login` and retry |
| `Model deployment not found` | Model name in `.env` doesn't match a deployment in your project | Open your project in the Foundry portal, check **Deployments**, and update `MODEL_DEPLOYMENT_NAME` in `.env` |
| `SharePoint tool configured` but agent can't find documents | Documents not uploaded or connection name incorrect | Verify documents appear in the SharePoint library and that `SHAREPOINT_CONNECTION_NAME` matches the connection in your project |
| MCP tool timeout or connection error | Microsoft Learn MCP server is unreachable | Verify `MCP_SERVER_URL` is set to `https://learn.microsoft.com/api/mcp` and that your network allows outbound HTTPS |
| `403 Forbidden` on SharePoint | Insufficient permissions on the SharePoint site | Confirm your signed-in identity has at least **Read** access to the SharePoint document library |



## Summary

You now have:
- A working single-agent prototype grounded in internal and external knowledge.
- A repeatable evaluation script demonstrating enterprise validation patterns.
- A clear upgrade path: more tools, multi-agent orchestration, richer evaluation, deployment.

These patterns reduce prototype-to-production friction: you can add data sources, enforce governance, and integrate monitoring without rewriting core logic.


## Next steps

This tutorial demonstrates **Stage 1** of the developer journey - from idea to prototype. This minimal sample provides the foundation for enterprise AI development. To continue your journey, explore the next stages:

### Suggested additional enhancements
- Add more data sources ([Azure AI Search](../agents/how-to/tools/ai-search.md), [other sources](../../how-to/connections-add.md)).
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

## Clean up resources

To avoid unnecessary costs, delete the resources you created in this tutorial:

1. **Delete the agent**: The agent is automatically deleted at the end of `main.py` (Python) or `Program.cs` (C#). If you interrupted the run, delete it manually from the **Agents** page in the Foundry portal.
1. **Delete the evaluation run**: In the Foundry portal, go to **Evaluation**, select the evaluation run, and delete it.
1. **Remove SharePoint sample documents**: If you uploaded the sample `.docx` files to a production SharePoint site, remove them from the document library.
1. **(Optional) Delete the Foundry project**: If you created a project only for this tutorial, delete it from the Foundry portal to remove all associated resources.

## Related content

- [Foundry Agent Service overview](../../agents/overview.md)
- [SharePoint tool documentation](../agents/how-to/tools/sharepoint.md)
- [MCP tool integration](../agents/how-to/tools/model-context-protocol.md)
- [Multi-agent patterns](../../agents/how-to/connected-agents.md)
