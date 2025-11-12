---
title: 'How to use custom code interpreter with agents'
titleSuffix: Microsoft Foundry
description: Learn how to use the custom code interpreter tool.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/12/2025
author: aahill
ms.author: aahi
---

# Custom code interpreter tool for agents

With a Custom code interpreter for your agent, you can customize the resources, available Python packages, and Container Apps environment that is used to run the Python code that the agent writes. The code interpreter container is exposed via a Model Context Protocol (MCP) server.

## Prerequisites

- [A basic or standard agent environment](../../../../agents/environment-setup.md)
- A deployed model in the agent environment (the examples in this article use `gpt-4o-mini`)
- [A 'Consumption' plan Azure Container Apps environment](/azure/container-apps/environment)
- The [Azure CLI](/cli/azure/install-azure-cli)
- The latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

## Code samples

### Create a dynamic session pool with a code interpreter image

```ARM
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environmentName": {
      "type": "string",
      "minLength": 3,
      "metadata": {
        "description": "The name of the Container Apps Environment to use"
      }
    },
    "sessionPoolName": {
      "type": "string",
      "minLength": 3,
      "metadata": {
        "description": "The name of the custom container session pool to create"
      }
    },
    "cpu": {
      "type": "int",
      "minValue": 1,
      "maxValue": 16,
      "defaultValue": 1,
      "metadata": {
        "description": "The amount of CPU to provide to each container instance, in vCPU counts"
      }
    },
    "memory": {
      "type": "int",
      "minValue": 1,
      "maxValue": 16,
      "defaultValue": 2,
      "metadata": {
        "description": "The amount of RAM to provide to each container instance, in GiB"
      }
    },
    "location": {
      "type": "string",
      "defaultValue": "northcentralus(stage)",
      "allowedValues": [
        "eastus2euap",
        "northcentralus(stage)"
      ],
      "metadata": {
        "description": "Location of all ACA resources."
      }
    },
    "image": {
      "type": "string",
      "defaultValue": "mcr.microsoft.com/k8se/services/codeinterpreter:0.9.18-python3.12",
      "metadata": {
        "description": "An image that implements the code interpreter HTTP API"
      }
    }
  },
  "resources": [
    {
      "type": "Microsoft.App/sessionPools",
      "apiVersion": "2025-10-02-preview",
      "name": "[parameters('sessionPoolName')]",
      "location": "[resource(resourceId('Microsoft.App/managedEnvironment', parameters('environmentName')), '2024-10-02-preview').location]",
      "properties": {
        "environmentId": "[resourceId('Microsoft.App/managedEnvironments', parameters('environmentName'))]",
        "poolManagementType": "Dynamic",
        "containerType": "CustomContainer",
        "scaleConfiguration": {
          "maxConcurrentSessions": 10,
          "readySessionInstances": 5
        },
        "dynamicPoolConfiguration": {
          "lifecycleConfiguration": {
            "cooldownPeriodInSeconds": 600,
            "lifecycleType": "Timed"
          }
        },
        "customContainerTemplate": {
          "containers": [
            {
              "name": "jupyterpython",
              "image": "[parameters('image')]",
              "env": [
                {
                  "name": "SYS_RUNTIME_SANDBOX",
                  "value": "AzureContainerApps-DynamicSessions"
                },
                {
                  "name": "AZURE_CODE_EXEC_ENV",
                  "value": "AzureContainerApps-DynamicSessions-Py3.12"
                },
                {
                  "name": "AZURECONTAINERAPPS_SESSIONS_SANDBOX_VERSION",
                  "value": "7758"
                },
                {
                  "name": "JUPYTER_TOKEN",
                  "value": "AzureContainerApps-DynamicSessions"
                }
              ],
              "resources": {
                "cpu": "[parameters('cpu')]",
                "memory": "[concat(parameters('memory'), 'Gi')]"
              },
              "probes": [
                {
                  "type": "Liveness",
                  "httpGet": {
                    "path": "/health",
                    "port": 6000
                  },
                  "failureThreshold": 4
                },
                {
                  "type": "Startup",
                  "httpGet": {
                    "path": "/health",
                    "port": 6000
                  },
                  "failureThreshold": 30,
                  "periodSeconds": 2
                }
              ]
            }
          ],
          "ingress": {
            "targetPort": 6000
          }
        },
        "mcpServerSettings": {
          "isMCPServerEnabled": true
        },
        "sessionNetworkConfiguration": {
          "status": "egressEnabled"
        }
      }
    }
  ],
  "outputs": {
    "CODE_INTERPRETER_MCP_ENDPOINT": {
      "type": "string",
      "metadata": {
        "description": "Custom code interpreter MCP endpoint"
      },
      "value": "[reference(resourceId('Microsoft.App/sessionPools', parameters('sessionPoolName')), '2025-10-02-preview').properties.mcpServerSettings.mcpServerEndpoint]"
    },
    "AZURE_SESSION_POOL_ID": {
      "type": "string",
      "metadata": {
        "description": "Resource ID for the dynamic session pool"
      },
      "value": "[resourceId('Microsoft.App/sessionPools', parameters('sessionPoolName'))]"
    }
  }
}
```

### Get an API token for the MCP server

```bash
az rest --method POST --uri {AZURE_SESSION_POOL_ID}/fetchMCPServerCredentials?api-version=2025-02-02-preview
```

### Use the Custom Code Interpreter in an agent

Set the `AZURE_AI_PROJECT_ENDPOINT`, `CODE_INTERPRETER_MCP_ENDPOINT`, and `CODE_INTERPRETER_MCP_API_KEY` environment variables, and then run the below script.

```python
import os

import dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool
from azure.identity import DefaultAzureCredential

dotenv.load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()

tools = [
    MCPTool(
        server_label="python_tool",
        server_url=os.environ["CODE_INTERPRETER_MCP_ENDPOINT"],
        require_approval=False,
        headers={
            'x-ms-apikey': os.environ["CODE_INTERPRETER_MCP_API_KEY"],
        },
        allowed_tools=[
            'launchShell',
            'runPythonCodeInRemoteEnvironment',
        ],
    ),
]

# You must use URLs to data files
EXAMPLE_DATA_FILE_URL="https://path/to/my/data/sample.csv"

with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model='gpt-4o-mini,
            instructions="""\
You are a helpful agent that can use a Python code interpreter to assist users. Use the `python_tool` MCP
server to perform any calculations or numerical analyses. ALWAYS call the `launchShell` tool first before
calling the `runPythonCodeInRemoteEnvironment` tool. If you need to display any non-text output to the
user, return it as a data URI. NEVER provide a path to a file in the remote environment to the user.
""",
            temperature=0,
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    response = openai_client.responses.create(
        input=f"Please analyze the CSV file at {EXAMPLE_DATA_FILE_URL} and graph the grade distribution as a histogram. Calculate the mean, median, and standard deviation as well.",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    print(f"Response: {response.output_text}")

    # Clean up resources by deleting the agent version
    # This prevents accumulation of unused agent versions in your project
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
```

## Limitations

File input/output and use of file stores are not directly supported in APIs, so you must use URLs (such as data URLs for small files and Azure Blob Service SAS URLs for large ones) to get data in and out.

## References

- [Azure Container Apps Dynamic Sessions](/azure/container-apps/sessions)
- [Session Pools with Custom Containers](/azure/container-apps/session-pool#custom-container-pool)