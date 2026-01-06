---
title: 'How to use connected agents'
titleSuffix: Microsoft Foundry
description: Learn how to create multi-agentic systems using connected agents in the Foundry Agent Service.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/17/2025
author: aahill
ms.author: aahi
recommendations: false
ms.custom: azure-ai-agents-code
zone_pivot_groups: selection-connected-agents
---

# Build collaborative, multi-agent systems with Connected Agents

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

> [!NOTE]
> This tool is only available in `2025-05-15-preview` API. We highly recommend you to migrate to use the `2025-11-15-preview` API version [workflows](../../default/agents/concepts/workflow.md) for multi-agent orchestration.

Connected agents in Foundry Agent Service let you break down complex tasks into coordinated, specialized roles—without the need for a custom orchestrator or hand-coded routing logic. With this capability, you can design systems where a primary agent intelligently delegates to purpose-built subagents, streamlining workflows like customer support, market research, legal summarization, and financial analysis.

Rather than overloading one agent with too many skills, you can build focused, reusable agents that collaborate seamlessly—scaling both performance and maintainability.

## Features

* **Simplified workflow design**: Break down complex tasks across specialized agents to reduce complexity and improve clarity.
* **No custom orchestration required**: The main agent uses natural language to route tasks, eliminating the need for hardcoded logic.
* **Easy extensibility**: Add new connected agents (for example, translation or risk scoring) without modifying the main agent.
* **Improved reliability and traceability**: Assign focused responsibilities to each agent for easier debugging and better auditability.
* **Flexible setup options**: Configure agents using a no-code interface in the Foundry portal or programmatically via the Python SDK.

## Example: building a modular contract review agent with connected agents

As your use cases grow in complexity, you can scale your AI solution by assigning specific responsibilities to multiple connected agents. This lets each agent specialize in a narrow task while the main agent coordinates the overall workflow. This modular design enhances accuracy, maintainability, and traceability—especially for document-heavy domains like legal, compliance, and procurement.
Let’s walk through a real-world example of how to build a **Contract Review Assistant** using connected agents.

### Architecture Overview

**Main agent – contract orchestrator**

Acts as the central interface. It interprets user prompts (such as "summarize clauses," "compare drafts," or "check compliance"), determines the task type, and delegates it to the appropriate connected agent.

* **Tools Used**: None directly
* **Responsibilities**: Intent classification and delegation
* **Example Agent Description**:

    "You are a contract review assistant. Depending on the user query, determine if the task involves clause summarization, document comparison, or compliance checking, and route accordingly."

**Connected agent 1: clause summarizer**

Extracts key sections (like Termination, Indemnity, or Confidentiality) from a contract and summarizes them in plain language.

* **Tools Used**:
    * File Search to retrieve the uploaded contract
    * Code Interpreter to scan the document for clause headings and summarize the content
* **Responsibilities**: Information extraction and summarization
* **Example agent description**:

    "Extract and summarize the 'Termination,' 'Payment terms,' and 'Indemnity' clauses from the provided contract."

**Connected agent 2: compliance validator**

Checks the contract against internal standards or uploaded guidelines to identify risky or noncompliant language.

* **Tools Used**:
    * File Search to access internal policy documents or contract templates
    * OpenAPI Tool to call an internal compliance rules API
    * Azure Function or Azure Logic Apps to run simple logic checks (for example required clause presence or threshold validations)

* **Responsibilities**: Policy matching and risk flagging
* **Example Prompt Instruction**:
    
    "Review this document against company compliance guidelines and flag any deviations from the approved template."

## Limitations

* Connected agents cannot call local functions using the function calling tool. We recommend using the [OpenAPI tool](tools\openapi-spec.md) or [Azure Functions](tools\azure-functions.md) instead.
*  It is currently not possible to guarantee citations will be passed from connected agents. You can try using prompt engineering combined with different models to try and improve the possibility that citations will be outputted by the main agent, but results are subject to variability.
* Connected agents have a maximum depth of 2. A parent agent can have multiple subagent siblings, but subagents cannot have their own subagents. Exceeding this depth results in an `Assistant Tool Call Depth Error`. 

:::zone pivot="portal"


## Creating a multi-agent setup

1. Navigate to the **Agents** page in the portal
2. Select an existing agent from the list or create a new one.
3. Scroll down to the **Connected agents** section in the agent's set up panel and select **Add +**.

:::image type="content" source="../media\connected-agents\connected-agents-foundry.png" alt-text="A screenshot of the agents page in the Microsoft Foundry." lightbox="../media\connected-agents\connected-agents-foundry.png":::

4. In the dialog that appears, choose an agent for the main agent to delegate tasks to, and describe:
   - Select an **existing agent** from the dropdown. This is the connected agent that the main agent will delegate tasks to.
   - Enter a **unique name** for the connected agent (letters and underscores only). This name is used for API-level function calling. Keep it descriptive and machine-readable to maximize recall accuracy (for example, `summarize_text`, `lookup_product_info`).
   - Add a clear **description** of when and why the connected agent should be invoked. This helps guide the main agent’s decision-making on when to hand off tasks to connected agents during runtime.
5. Select **Add +**
6. Repeat steps 3–5 to add additional specialized agents to the main agent.
7. Once the connected agents appear in the setup panel, scroll up and select **Try in Playground**
8. Use test prompts in the Agent Playground to validate that the main agent correctly routes tasks to the connected agents when applicable. For example, if you’ve created a main agent called `research_agent`, which doesn't have any tools configured, and connected an agent named `stock_price_bot`, try a prompt like:

    **"What is the current stock price of Microsoft?"**

    The `research_agent` should delegate this request to `stock_price_bot` based on the routing description you defined.

:::image type="content" source="../media\connected-agents\connected-agents-foundry-2.png" alt-text="A screenshot of the connected agents screen" lightbox="../media\connected-agents\connected-agents-foundry-2.png":::

::: zone-end

:::zone pivot="csharp"

## Use the .NET SDK 

> [!NOTE]
> This shows a synchronous usage. You can find an asynchronous example on [GitHub](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Agents.Persistent/samples/Sample23_PersistentAgents_Connected_Agent.md) 

To enable your Agent to use a connected agent, you use `ConnectedAgentToolDefinition` along with the agent ID, name, and a description.

1. First we need to create agent client and read the environment variables, which will be used in the next steps.
    
    ```csharp
    var projectEndpoint = configuration["ProjectEndpoint"];
    var modelDeploymentName = configuration["ModelDeploymentName"];

    PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());
    ```

2. Next we will create the main agent `mainAgent`, and the connected `stockAgent` agent using the agent client. This connected agent will be used to initialize the `ConnectedAgentToolDefinition`.
    
    ```csharp
    PersistentAgent stockAgent = client.Administration.CreateAgent(
            model: modelDeploymentName,
            name: "stock_price_bot",
            instructions: "Your job is to get the stock price of a company. If you don't know the realtime stock price, return the last known stock price."
            // tools: [...] tools that would be used to get stock prices
        );
    ConnectedAgentToolDefinition connectedAgentDefinition = new(new ConnectedAgentDetails(stockAgent.Id, stockAgent.Name, "Gets the stock price of a company"));

    PersistentAgent mainAgent = client.Administration.CreateAgent(
            model: modelDeploymentName,
            name: "stock_price_bot",
            instructions: "Your job is to get the stock price of a company, using the available tools.",
            tools: [connectedAgentDefinition]
        );

    
    ```
    
4. Now we will create the thread, add the message, containing a question for agent and start the run.
    
    ```csharp
    PersistentAgentThread thread = client.Threads.CreateThread();

    // Create message to thread
    PersistentThreadMessage message = client.Messages.CreateMessage(
        thread.Id,
        MessageRole.User,
        "What is the stock price of Microsoft?");

    // Run the agent
    ThreadRun run = client.Runs.CreateRun(thread, agent);
    do
    {
        Thread.Sleep(TimeSpan.FromMilliseconds(500));
        run = client.Runs.GetRun(thread.Id, run.Id);
    }
    while (run.Status == RunStatus.Queued
        || run.Status == RunStatus.InProgress);

    // Confirm that the run completed successfully
    if (run.Status != RunStatus.Completed)
    {
        throw new Exception("Run did not complete successfully, error: " + run.LastError?.Message);
    }
    ```
    
5. Print the agent messages to console in chronological order.
    
    ```csharp
    Pageable<PersistentThreadMessage> messages = client.Messages.GetMessages(
        threadId: thread.Id,
        order: ListSortOrder.Ascending
    );

    foreach (PersistentThreadMessage threadMessage in messages)
    {
        Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
        foreach (MessageContent contentItem in threadMessage.ContentItems)
        {
            if (contentItem is MessageTextContent textItem)
            {
                string response = textItem.Text;
                if (textItem.Annotations != null)
                {
                    foreach (MessageTextAnnotation annotation in textItem.Annotations)
                    {
                        if (annotation is MessageTextUriCitationAnnotation urlAnnotation)
                        {
                            response = response.Replace(urlAnnotation.Text, $" [{urlAnnotation.UriCitation.Title}]({urlAnnotation.UriCitation.Uri})");
                        }
                    }
                }
                Console.Write($"Agent response: {response}");
            }
            else if (contentItem is MessageImageFileContent imageFileItem)
            {
                Console.Write($"<image from ID: {imageFileItem.FileId}");
            }
            Console.WriteLine();
        }
    }
    ```
    
6. Clean up resources by deleting thread and agent.
    
    ```csharp
    agentClient.DeleteThread(threadId: thread.Id);
    agentClient.DeleteAgent(agentId: agent.Id);
    agentClient.DeleteAgent(agentId: connectedAgent.Id);
    ```

::: zone-end

:::zone pivot="python"


## Creating a multi-agent setup

To create a multi-agent setup, follow these steps:

1. Initialize the client object.

    ```python
    import os
    from azure.ai.projects import AIProjectClient
    from azure.ai.agents.models import ConnectedAgentTool, MessageRole
    from azure.identity import DefaultAzureCredential
    
    
    project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
    )
    ```

1. Create an agent that will be connected to a "main" agent.

    ```python
    stock_price_agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="stock_price_bot",
        instructions="Your job is to get the stock price of a company. If you don't know the realtime stock price, return the last known stock price.",
        #tools=... # tools to help the agent get stock prices
    )
    ```
   
1. Initialize the connected agent tool with the agent ID, name, and description
    
    ```python
    connected_agent = ConnectedAgentTool(
        id=stock_price_agent.id, name=stock_price_agent.name, description="Gets the stock price of a company"
    )
    ```

1. Create the "main" agent that will use the connected agent.

    ```python
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent",
        instructions="You are a helpful agent, and use the available tools to get stock prices.",
        tools=connected_agent.definitions,
    )
    
    print(f"Created agent, ID: {agent.id}")
    ```

1. Create a thread and add a message to it.
    
    ```python
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")
    
    # Create message to thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content="What is the stock price of Microsoft?",
    )
    print(f"Created message, ID: {message.id}")
    
    ```
    
1. Create a run and wait for it to complete. 
    
    ```python
    
    # Create and process Agent run in thread with tools
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")
    
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    
    # Delete the Agent when done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
    
    # Delete the connected Agent when done
    project_client.agents.delete_agent(stock_price_agent.id)
    print("Deleted connected agent")
    ```

1. Print the agent's response. The main agent will compile the responses from the connected agents and provide the response. connected agent responses are only visible to the main agent, and not to the end user.
    
    ```python
    # Print the Agent's response message with optional citation
    response_message = project_client.agents.messages.list(thread_id=thread.id).get_last_message_by_role(
        MessageRole.AGENT
    )
    if response_message:
        for text_message in response_message.text_messages:
            print(f"Agent response: {text_message.text.value}")
        for annotation in response_message.url_citation_annotations:
            print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")
    ```

::: zone-end

## Publish connected agents to Azure

After testing your connected agents, you can publish them to Azure for production use. The publishing process for connected agents has one key difference from publishing individual agents: **both the main agent and all connected agents must be published separately** as Agent Applications.

### Connected agents-specific considerations

* **Publish each agent individually**: Publish the connected agents first, then the main agent. Each receives its own stable endpoint and Agent Identity.
* **Routing continues to work**: After publishing, the main agent automatically routes to the published connected agents using their Agent IDs in the `ConnectedAgentToolDefinition`. No code changes are needed.
* **Identity management**: Published connected agents receive their own Agent Identity. Reconfigure permissions for any Azure resources that your connected agents access, as the shared development identity permissions don't transfer.

For complete publishing instructions, including how to publish agents through the portal or REST API, authentication configuration, and consuming published agents, see [Publish and share agents in Microsoft Foundry](../../default/agents/how-to/publish-agent.md).

## Related content

* [Publish and share agents in Microsoft Foundry](../../default/agents/how-to/publish-agent.md)
* [Agent identity concepts](../../default/agents/concepts/agent-identity.md)
* [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md)
