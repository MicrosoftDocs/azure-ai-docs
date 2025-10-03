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

#[C#](#tab/csharp)

#[Python](#tab/python)

Create `requirements.txt`:

:::code language="txt" source="~/foundry-samples-main/samples/microsoft/python/developer-journey-stage-1-idea-to-prototype/requirements.txt":::

#[Java](#tab/java)

#[TypeScript](#tab/typescript)

---

## Step 2: Build the Modern Workplace Assistant

The `main.py` file demonstrates a complete business scenario combining internal policies with external technical guidance:

<!-- Code section: imports_and_setup -->
```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import SharepointTool, McpTool, ToolResources
from dotenv import load_dotenv

load_dotenv()

# Initialize Azure AI Foundry client
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

def create_workplace_assistant():
    """Create an AI agent with SharePoint and Microsoft Learn integration"""
    
    print("🤖 Creating Modern Workplace Assistant...")
    
    # Configure SharePoint tool for internal knowledge
    sharepoint_resource_name = os.environ["SHAREPOINT_RESOURCE_NAME"]
    sharepoint_site_url = os.getenv("SHAREPOINT_SITE_URL")
    
    try:
        sharepoint_conn = project_client.connections.get(name=sharepoint_resource_name)
        sharepoint_tool = SharepointTool(connection_id=sharepoint_conn.id)
        print(f"✅ SharePoint connected: {sharepoint_resource_name}")
    except Exception as e:
        print(f"⚠️  SharePoint connection not found: {e}")
        sharepoint_tool = None
    
    # Configure Microsoft Learn MCP tool for technical guidance
    mcp_tool = McpTool(
        server_label="microsoft_learn",
        server_url=os.environ["MCP_SERVER_URL"],
        allowed_tools=[]
    )
    mcp_tool.set_approval_mode("never")  # Enable seamless experience
    
    # Create dynamic instructions based on available tools
    if sharepoint_tool:
        instructions = """You are a Modern Workplace Assistant for Contoso Corp.

Your capabilities:
- Search SharePoint for company policies, procedures, and internal documents
- Access Microsoft Learn for current Azure and Microsoft 365 technical guidance
- Provide comprehensive answers combining internal policies with implementation guidance

When responding:
- For policy questions: Search SharePoint for company documents
- For technical questions: Use Microsoft Learn for current Azure/M365 guidance  
- For implementation questions: Combine both sources to show policy requirements AND technical steps
- Always cite your sources and provide actionable guidance"""
    else:
        instructions = """You are a Technical Assistant with access to Microsoft Learn documentation.

Your capabilities:
- Access Microsoft Learn for current Azure and Microsoft 365 technical guidance
- Provide detailed technical implementation steps and best practices

Note: SharePoint integration is not configured. You can only provide technical guidance from Microsoft Learn.
When users ask about company policies, explain that SharePoint integration needs to be configured."""

    # Create the agent
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="Modern Workplace Assistant",
        instructions=instructions,
        tools=(sharepoint_tool.definitions if sharepoint_tool else []) + mcp_tool.definitions,
    )
    
    print(f"✅ Agent created: {agent.id}")
    return agent, mcp_tool

def demo_business_scenarios(agent, mcp_tool):
    """Demonstrate key business scenarios combining internal and external knowledge"""
    
    scenarios = [
        {
            "title": "📋 Policy Question 1/3",
            "question": "What is our remote work policy regarding security requirements?",
            "context": "Should search SharePoint for company policies"
        },
        {
            "title": "🔧 Technical Question 2/3", 
            "question": "How do I set up Azure Active Directory conditional access?",
            "context": "Should use Microsoft Learn documentation"
        },
        {
            "title": "🔄 Implementation Question 3/3",
            "question": "Our security policy requires multi-factor authentication - how do I implement this in Azure AD?",
            "context": "Should combine internal policy with Azure implementation guidance"
        }
    ]
    
    print("\n🏢 Modern Workplace Assistant Demo")
    print("=" * 50)
    
    for scenario in scenarios:
        print(f"\n{scenario['title']}")
        print(f"❓ {scenario['question']}")
        print(f"💡 {scenario['context']}")
        print("-" * 50)
        
        response, status = chat_with_assistant(agent.id, mcp_tool, scenario['question'])
        print(f"🤖 {response[:200]}...")
        print("-" * 50)
    
    print("\n✅ Demo completed! The assistant successfully handled 3 business scenarios.")

if __name__ == "__main__":
    # Create and demonstrate the Modern Workplace Assistant
    agent, mcp_tool = create_workplace_assistant()
    demo_business_scenarios(agent, mcp_tool)
```

This implementation shows:

- **Robust error handling** for missing connections
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

The `evaluate.py` script tests realistic business scenarios combining SharePoint policies with Microsoft Learn technical guidance.

### Evaluation questions (`questions.jsonl`)

```jsonl
{"question": "What is our remote work policy regarding security requirements?", "source": "sharepoint", "keywords": ["remote", "security", "policy"]}
{"question": "How do I set up Azure Active Directory conditional access?", "source": "mcp", "keywords": ["conditional access", "azure", "setup"]}
{"question": "Our policy requires MFA - how do I implement this in Azure AD?", "source": "both", "keywords": ["mfa", "azure", "implement"]}
{"question": "What are our data governance requirements for Azure resources?", "source": "sharepoint", "keywords": ["data", "governance", "azure"]}
```

### Evaluation framework (`evaluate.py`)

<!-- Code section: evaluation_framework -->
```python
import json
import os
from main import project_client, create_workplace_assistant, chat_with_assistant

def load_test_questions():
    """Load business-focused test questions"""
    with open("questions.jsonl", "r") as f:
        return [json.loads(line) for line in f]

def evaluate_response(response, keywords):
    """Simple keyword-based evaluation"""
    response_lower = response.lower()
    matches = sum(1 for keyword in keywords if keyword.lower() in response_lower)
    return matches >= len(keywords) * 0.5  # Pass if 50%+ keywords found

def run_evaluation():
    """Run comprehensive business evaluation"""
    print("🧪 Starting Business Evaluation")
    print("=" * 40)
    
    # Create agent
    agent, mcp_tool = create_workplace_assistant()
    questions = load_test_questions()
    
    results = []
    for i, q in enumerate(questions, 1):
        print(f"\n📝 Question {i}/{len(questions)}")
        print(f"❓ {q['question']}")
        print(f"📊 Expected source: {q['source']}")
        
        # Get response
        response, status = chat_with_assistant(agent.id, mcp_tool, q['question'])
        passed = evaluate_response(response, q['keywords'])
        
        result = {
            "question": q["question"],
            "source": q["source"], 
            "keywords": q["keywords"],
            "response_length": len(response),
            "status": status,
            "passed": passed
        }
        results.append(result)
        
        print(f"✅ Response: {len(response)} chars, Status: {status}")
        print(f"🎯 Result: {'PASS' if passed else 'FAIL'}")
    
    # Summary
    passed_count = sum(1 for r in results if r["passed"])
    print(f"\n📊 EVALUATION SUMMARY")
    print(f"✅ Passed: {passed_count}/{len(results)}")
    print(f"📈 Success Rate: {passed_count/len(results)*100:.1f}%")
    
    # Save results
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    run_evaluation()
```

This evaluation framework tests:

- **SharePoint integration** for company policy questions
- **MCP integration** for technical guidance questions  
- **Combined scenarios** requiring both internal and external knowledge
- **Response quality** using keyword matching and length analysis
```

## Step 4: Batch evaluation

Create `questions.jsonl`:

```jsonl
{"question": "What's our remote work policy?", "expected": "policy"}
{"question": "Get current weather data", "expected": "weather"}
{"question": "Summarize Q3 performance", "expected": "performance"}
{"question": "Research market trends", "expected": "research"}
```

Create `eval.py`:

<!-- Code section: batch_evaluation -->
```python
import json
from agent import project_client, chat_with_agent

def run_evaluation(agent_id):
    """Run simple batch evaluation locally"""
    with open("questions.jsonl", "r") as f:
        questions = [json.loads(line) for line in f]
    
    results = []
    for q in questions:
        response = chat_with_agent(agent_id, q["question"])
        contains_expected = q["expected"].lower() in response.lower()
        results.append({
            "question": q["question"],
            "response": response[:100] + "..." if len(response) > 100 else response,
            "contains_expected": contains_expected
        })
    
    # Print summary
    passed = sum(1 for r in results if r["contains_expected"])
    print(f"Evaluation: {passed}/{len(results)} passed")
    
    return results

if __name__ == "__main__":
    import sys
    agent_id = sys.argv[1] if len(sys.argv) > 1 else input("Agent ID: ")
    results = run_evaluation(agent_id)
    print(json.dumps(results, indent=2))
```

## Step 5: Run the complete sample

### Setup and run

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

This demonstrates:
- SharePoint connection diagnostics  
- Agent creation with dynamic instructions
- Three business scenarios (policy, technical, combined)
- Interactive mode for testing

3. **Run business evaluation**:

```bash
python evaluate.py
```

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
