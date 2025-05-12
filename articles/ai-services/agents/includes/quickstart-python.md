---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 11/13/2024
---


| [Reference documentation](https://aka.ms/azsdk/azure-ai-projects/python/reference) | [Samples](https://aka.ms/azsdk/azure-ai-projects/python/samples/) | [Library source code](https://aka.ms/azsdk/azure-ai-projects/python/code) | [Package (PyPi)](https://aka.ms/azsdk/azure-ai-projects/python/package) |

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).
* [Python 3.8 or later](https://www.python.org/)
* Ensure that the individual deploying the template has the **Azure AI Developer** role assigned at the resource group level where the template is being deployed.
* Additionally, to deploy the template, you need to have the preset **Role Based Access Administrator** role at the subscription level.
   * The **Owner** role at the subscription level satisfies this requirement.
   * The specific admin role that is needed is `Microsoft.Authorization/roleAssignments/write`
* Ensure that each team member who wants to use the Agent Playground or SDK to create or edit agents has been assigned the built-in **Azure AI Developer** [RBAC role](../../../ai-foundry/concepts/rbac-azure-ai-foundry.md) for the project.
    * Note: assign these roles after the template has been deployed
    * The minimum set of permissions required is: `agents/*/read`, `agents/*/action`, `agents/*/delete`
* Install [the Azure CLI and the machine learning extension](/azure/machine-learning/how-to-configure-cli). If you have the CLI already installed, make sure it's updated to the latest version.



## Configure and run an agent

| Component | Description                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent     | Custom AI that uses AI models in conjunction with tools.                                                                                                                                                                                  |
| Tool      | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information.               |
| Thread    | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context.                                                                                     |
| Message   | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread.                                                                                                 |
| Run       | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. |
| Run Step  | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during its run. Examining Run Steps allows you to understand how the agent is getting to its results.                                |

Run the following commands to install the python packages.

```console
pip install azure-ai-projects
pip install azure-identity
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

Set this connection string as an environment variable named `PROJECT_ENDPOINT`.


```python
import os
import os, time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from pathlib import Path

# Retrieve the project endpoint from environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
    api_version="latest",
)

# Initialize the FunctionTool with user-defined functions
functions = FunctionTool(functions=user_functions)

with project_client:
    # Create an agent with custom functions
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent",
        instructions="You are a helpful agent"
    )
    print(f"Created agent, ID: {agent.id}")

# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Create a message in the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",  # Role of the message sender
    content="When was Microsoft founded?",  # Message content
)
print(f"Created message, ID: {message['id']}")

# Create and process an agent run in the thread
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

# Check if the run failed
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch and log all messages from the thread
messages = project_client.agents.messages.list(thread_id=thread.id)
for message in messages.data:
    print(f"Role: {message.role}, Content: {message.content}")

# Delete the agent after use
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
```
