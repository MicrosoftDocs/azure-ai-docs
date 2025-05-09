---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 03/28/2025
---

| [Reference documentation](/dotnet/api/overview/azure/ai.projects-readme) | [Samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects/tests/Samples) | [Library source code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.Projects/) |

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).
* [The latest version of .NET](https://dotnet.microsoft.com/en-us/download)
* Ensure that the individual deploying the template has the **Azure AI Developer** role assigned at the resource group level where the template is being deployed.
* Additionally, to deploy the template, you need to have the preset **Role Based Access Administrator** role at the subscription level.
   * The **Owner** role at the subscription level satisfies this requirement.
   * The specific admin role that is needed is `Microsoft.Authorization/roleAssignments/write`
* Ensure that each team member who wants to use the Agent Playground or SDK to create or edit agents has been assigned the built-in **Azure AI Developer** [RBAC role](../../../ai-foundry/concepts/rbac-azure-ai-foundry.md) for the project.
    * Note: assign these roles after the template has been deployed
    * The minimum set of permissions required is: **agents/*/read**, **agents/*/action**, **agents/*/delete**  
* Install [the Azure CLI and the machine learning extension](/azure/machine-learning/how-to-configure-cli). If you have the CLI already installed, make sure it's updated to the latest version.

[!INCLUDE [bicep-setup](bicep-setup.md)]

## Configure and run an agent

| Component | Description                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent     | Custom AI that uses AI models in conjunction with tools.                                                                                                                                                                                  |
| Tool      | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information.               |
| Thread    | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context.                                                                                     |
| Message   | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread.                                                                                                 |
| Run       | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. |
| Run Step  | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during its run. Examining Run Steps allows you to understand how the agent is getting to its results.                                |

Create a .NET Console project.

```console
dotnet new console
```

Install the .NET package to your project. For example if you're using the .NET CLI, run the following command.

>[!Note]
> Azure.AI.Projects is only available as a prelease version. Please use the "-prerelease" flag to add the package until a release version becomes available.

```console
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.Identity
```

Next, to authenticate your API requests and run the program, use the [az login](/cli/azure/authenticate-azure-cli-interactively) command to sign into your Azure subscription.

```azurecli
az login
```

Use the following code to create and run an agent. To run this code, you will need to get the endpoint for your project. This string is in the format:

`https://<AIFoundryResourceName>.services.ai.azure.com/api/projects/<ProjectName>`

[!INCLUDE [endpoint-string-portal](endpoint-string-portal.md)]

For example, your connection string may look something like:

`https://myresource.services.ai.azure.com/api/projects/myproject`

Set this connection string as an environment variable named `ENDPOINT_STRING`.


```csharp
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

#nullable disable

using Azure.Identity;

namespace Azure.AI.Projects.Tests;

public class Sample_Agent
{
    static async Task Main()
    {
        var connectionString = Environment.GetEnvironmentVariable("ENDPOINT_STRING");

        AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential());

        // Step 1: Create an agent
        Response<Agent> agentResponse = await client.CreateAgentAsync(
            model: "gpt-4o-mini",
            name: "My Agent",
            instructions: "You are a helpful agent.",
            tools: new List<ToolDefinition> { new CodeInterpreterToolDefinition() });
        Agent agent = agentResponse.Value;

        // Intermission: agent should now be listed

        Response<PageableList<Agent>> agentListResponse = await client.GetAgentsAsync();

        //// Step 2: Create a thread
        Response<AgentThread> threadResponse = await client.CreateThreadAsync();
        AgentThread thread = threadResponse.Value;

        // Step 3: Add a message to a thread
        Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
            thread.Id,
            MessageRole.User,
            "I need to solve the equation `3x + 11 = 14`. Can you help me?");
        ThreadMessage message = messageResponse.Value;

        // Intermission: message is now correlated with thread
        // Intermission: listing messages will retrieve the message just added

        Response<PageableList<ThreadMessage>> messagesListResponse = await client.GetMessagesAsync(thread.Id);
        //Assert.That(messagesListResponse.Value.Data[0].Id == message.Id);

        // Step 4: Run the agent
        Response<ThreadRun> runResponse = await client.CreateRunAsync(
            thread.Id,
            agent.Id,
            additionalInstructions: "");
        ThreadRun run = runResponse.Value;

        do
        {
            await Task.Delay(TimeSpan.FromMilliseconds(500));
            runResponse = await client.GetRunAsync(thread.Id, runResponse.Value.Id);
        }
        while (runResponse.Value.Status == RunStatus.Queued
            || runResponse.Value.Status == RunStatus.InProgress);

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
    }
}
```
