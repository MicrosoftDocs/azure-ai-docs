---
title: 'How to use Azure AI Agent service Code Interpreter'
titleSuffix: Azure OpenAI
description: Learn how to use Azure AI Agent service Code Interpreter
services: cognitive-services
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 11/18/2024
author: aahill
ms.author: aahi
recommendations: false
zone_pivot_groups: selection-code-interpreter
---

# Azure AI Agent service Code Interpreter



::: zone pivot="overview"

Code Interpreter allows the agents to write and run Python code in a sandboxed execution environment. With Code Interpreter enabled, your agent can run code iteratively to solve more challenging code, math, and data analysis problems. When your Agent writes code that fails to run, it can iterate on this code by modifying and running different code until the code execution succeeds.

> [!IMPORTANT]
> Code Interpreter has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token based fees for Azure OpenAI usage. If your Agent calls Code Interpreter simultaneously in two different threads, two code interpreter sessions are created. Each session is active by default for one hour.

### Supported models

The [models page](../../quotas-limits.md) contains the most up-to-date information on regions/models where agents and code interpreter are supported.

We recommend using Agents with the latest models to take advantage of the new features, larger context windows, and more up-to-date training data.

::: zone-end

::: zone pivot="csharp-example"

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Azure.Core.TestFramework;
using NUnit.Framework;

namespace Azure.AI.Projects.Tests;

public partial class Sample_Agent_Basics : SamplesBase<AIProjectsTestEnvironment>
{
    [Test]
    public async Task BasicExample()
    {
        #region Snippet:OverviewCreateAgentClient
#if SNIPPET
        var connectionString = Environment.GetEnvironmentVariable("PROJECT_CONNECTION_STRING");
#else
        var connectionString = TestEnvironment.AzureAICONNECTIONSTRING;
#endif
        AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential());
        #endregion

        // Step 1: Create an agent
        #region Snippet:OverviewCreateAgent
        Response<Agent> agentResponse = await client.CreateAgentAsync(
            model: "gpt-4-1106-preview",
            name: "Math Tutor",
            instructions: "You are a personal math tutor. Write and run code to answer math questions.",
            tools: new List<ToolDefinition> { new CodeInterpreterToolDefinition() });
        Agent agent = agentResponse.Value;
        #endregion

        // Intermission: agent should now be listed

        Response<PageableList<Agent>> agentListResponse = await client.GetAgentsAsync();

        //// Step 2: Create a thread
        #region Snippet:OverviewCreateThread
        Response<AgentThread> threadResponse = await client.CreateThreadAsync();
        AgentThread thread = threadResponse.Value;
        #endregion

        // Step 3: Add a message to a thread
        #region Snippet:OverviewCreateMessage
        Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
            thread.Id,
            MessageRole.User,
            "I need to solve the equation `3x + 11 = 14`. Can you help me?");
        ThreadMessage message = messageResponse.Value;
        #endregion

        // Intermission: message is now correlated with thread
        // Intermission: listing messages will retrieve the message just added

        Response<PageableList<ThreadMessage>> messagesListResponse = await client.GetMessagesAsync(thread.Id);
        Assert.That(messagesListResponse.Value.Data[0].Id == message.Id);

        // Step 4: Run the agent
        #region Snippet:OverviewCreateRun
        Response<ThreadRun> runResponse = await client.CreateRunAsync(
            thread.Id,
            agent.Id,
            additionalInstructions: "Please address the user as Jane Doe. The user has a premium account.");
        ThreadRun run = runResponse.Value;
        #endregion

        #region Snippet:OverviewWaitForRun
        do
        {
            await Task.Delay(TimeSpan.FromMilliseconds(500));
            runResponse = await client.GetRunAsync(thread.Id, runResponse.Value.Id);
        }
        while (runResponse.Value.Status == RunStatus.Queued
            || runResponse.Value.Status == RunStatus.InProgress);
        #endregion

        #region Snippet:OverviewListUpdatedMessages
        Response<PageableList<ThreadMessage>> afterRunMessagesResponse
            = await client.GetMessagesAsync(thread.Id);
        IReadOnlyList<ThreadMessage> messages = afterRunMessagesResponse.Value.Data;

        // Note: messages iterate from newest to oldest, with the messages[0] being the most recent
        foreach (ThreadMessage threadMessage in messages)
        {
            Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
            foreach (MessageContent contentItem in threadMessage.ContentItems)
            {
                if (contentItem is MessageTextContent textItem)
                {
                    Console.Write(textItem.Text);
                }
                else if (contentItem is MessageImageFileContent imageFileItem)
                {
                    Console.Write($"<image from ID: {imageFileItem.FileId}");
                }
                Console.WriteLine();
            }
        }
        #endregion
    }
}
```

::: zone-end

::: zone pivot="python-example"

```python
"""
FILE: python-sample.py

DESCRIPTION:
    This sample demonstrates how to use agent operations with code interpreter from
    the Azure Agents service using a synchronous client.

USAGE:
    python python-sample.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set this environment variables with your own values:
    PROJECT_CONNECTION_STRING - the Azure AI Project connection string, as found in your AI Studio Project.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.ai.projects.models import FilePurpose
from azure.identity import DefaultAzureCredential
from pathlib import Path

# Create an Azure AI Client from a connection string, copied from your AI Studio project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:

    # upload a file and wait for it to be processed
    file = project_client.agents.upload_file_and_poll(
        file_path="../../data/nifty_500_quarterly_results.csv", purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded file, file ID: {file.id}")

    # instantiate the CodeInterpreterTool with the necessary files
    code_interpreter = CodeInterpreterTool(file_ids=[file.id])

    # notice that CodeInterpreter must be enabled in the agent creation, otherwise the agent will not be able to see the file attachment
    agent = project_client.agents.create_agent(
        model="gpt-4o-mini",
        name="my-agent",
        instructions="You are helpful agent",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    print(f"Created agent, agent ID: {agent.id}")

    # create a thread
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # create a message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Could you please create bar chart in the TRANSPORTATION sector for the operating profit from the uploaded csv file and provide file to me?",
    )
    print(f"Created message, message ID: {message.id}")

    # create and execute a run
    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    # delete the original file from the agent to free up space (note: this does not delete your version of the file)
    project_client.agents.delete_file(file.id)
    print("Deleted file")

    # print the messages from the agent
    messages = project_client.agents.get_messages(thread_id=thread.id)
    print(f"Messages: {messages}")

    # get the most recent message from the assistant
    last_msg = messages.get_last_text_message_by_sender("assistant")
    if last_msg:
        print(f"Last Message: {last_msg.text.value}")

    # save the newly created file
    for image_content in messages.image_contents:
        print(f"Image File ID: {image_content.image_file.file_id}")
        file_name = f"{image_content.image_file.file_id}_image_file.png"
        project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
        print(f"Saved image file to: {Path.cwd() / file_name}")
    
    # iterates through file_path_annotations in messages and prints details for each annotation
    for file_path_annotation in messages.file_path_annotations:
        print(f"File Paths:")
        print(f"Type: {file_path_annotation.type}")
        print(f"Text: {file_path_annotation.text}")
        print(f"File ID: {file_path_annotation.file_path.file_id}")
        print(f"Start Index: {file_path_annotation.start_index}")
        print(f"End Index: {file_path_annotation.end_index}")

    # delete the agent once done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

::: zone-end

::: zone pivot="supported-filetypes"


### Supported file types

|File format|MIME Type|
|---|---|
|`.c`| `text/x-c` |
|`.cpp`|`text/x-c++` |
|`.csv`|`application/csv`|
|`.docx`|`application/vnd.openxmlformats-officedocument.wordprocessingml.document`|
|`.html`|`text/html`|
|`.java`|`text/x-java`|
|`.json`|`application/json`|
|`.md`|`text/markdown`|
|`.pdf`|`application/pdf`|
|`.php`|`text/x-php`|
|`.pptx`|`application/vnd.openxmlformats-officedocument.presentationml.presentation`|
|`.py`|`text/x-python`|
|`.py`|`text/x-script.python`|
|`.rb`|`text/x-ruby`|
|`.tex`|`text/x-tex`|
|`.txt`|`text/plain`|
|`.css`|`text/css`|
|`.jpeg`|`image/jpeg`|
|`.jpg`|`image/jpeg`|
|`.js`|`text/javascript`|
|`.gif`|`image/gif`|
|`.png`|`image/png`|
|`.tar`|`application/x-tar`|
|`.ts`|`application/typescript`|
|`.xlsx`|`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`|
|`.xml`|`application/xml` or `text/xml`|
|`.zip`|`application/zip`|

::: zone-end


## See also

* Learn more [about agents](../../overview.md).
