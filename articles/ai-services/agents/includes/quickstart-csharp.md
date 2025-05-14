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

[!INCLUDE [universal-prerequisites](universal-prerequisites.md)]

## Configure and run an agent

| Component | Description                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent     | Custom AI that uses AI models in conjunction with tools.                                                                                                                                                                                  |
| Tool      | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information.               |
| Thread    | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context.                                                                                     |
| Message   | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread.                                                                                                 |
| Run       | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. |

Create a .NET Console project.

```console
dotnet new console
```

Install the .NET package to your project. For example if you're using the .NET CLI, run the following command.

>[!Note]
> Azure.AI.Projects is only available as a prelease version. Please use the "-prerelease" flag to add the package until a release version becomes available.

```console
dotnet add package Azure.AI.Agents.Persistent --prerelease
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

Set this connection string in an appsetting variable named `ProjectEndpoint`.


```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using Microsoft.Extensions.Configuration;
using System.Diagnostics;

IConfigurationRoot configuration = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .Build();

var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];

//Create a PersistentAgentsClient and PersistentAgent.
PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());

//Give PersistentAgent a tool to execute code using CodeInterpreterToolDefinition.
PersistentAgent agent = client.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "My Test Agent",
    instructions: "You politely help with math questions. Use the code interpreter tool when asked to visualize numbers.",
    tools: [new CodeInterpreterToolDefinition()]
);

//Create a thread to establish a session between Agent and a User.
PersistentAgentThread thread = client.Threads.CreateThread();

//Ask a question of the Agent.
client.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "Hi, Agent! Draw a graph for a line with a slope of 4 and y-intercept of 9.");

//Have Agent beging processing user's question with some additional instructions associated with the ThreadRun.
ThreadRun run = client.Runs.CreateRun(
    thread.Id,
    agent.Id,
    additionalInstructions: "Please address the user as Jane Doe. The user has a premium account.");

//Poll for completion.
do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = client.Runs.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);

//Get the messages in the PersistentAgentThread. Includes Agent (Assistant Role) and User (User Role) messages.
Pageable<ThreadMessage> messages = client.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending);

//Display each message and open the image generated using CodeInterpreterToolDefinition.
foreach (ThreadMessage threadMessage in messages)
{
    foreach (MessageContent content in threadMessage.ContentItems)
    {
        switch (content)
        {
            case MessageTextContent textItem:
                Console.WriteLine($"[{threadMessage.Role}]: {textItem.Text}");
                break;
            case MessageImageFileContent imageFileContent:
                Console.WriteLine($"[{threadMessage.Role}]: Image content file ID = {imageFileContent.FileId}");
                BinaryData imageContent = client.Files.GetFileContent(imageFileContent.FileId);
                string tempFilePath = Path.Combine(AppContext.BaseDirectory, $"{Guid.NewGuid()}.png");
                File.WriteAllBytes(tempFilePath, imageContent.ToArray());
                client.Files.DeleteFile(imageFileContent.FileId);

                ProcessStartInfo psi = new()
                {
                    FileName = tempFilePath,
                    UseShellExecute = true
                };
                Process.Start(psi);
                break;
        }
    }
}

//Clean up test resources.
client.Threads.DeleteThread(threadId: thread.Id);
client.Administration.DeleteAgent(agentId: agent.Id);
```
