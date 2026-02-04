---
title: Use the Computer Use Tool for Agents
titleSuffix: Microsoft Foundry
description: Learn to use the computer use tool in Microsoft Foundry agents to automate UI interactions. Includes Python, C#, and JavaScript samples.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 01/19/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: references_regions, dev-focus, pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
zone_pivot_groups: selection-computer-use
---

# Computer use tool for agents (Preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!WARNING]
> The computer use tool comes with significant security and privacy risks, including prompt injection attacks. For more information about intended uses, capabilities, limitations, risks, and considerations when choosing a use case, see the [Azure OpenAI transparency note](../../../../responsible-ai/openai/transparency-note.md#risk-and-limitations-of-computer-use-preview).

This article explains how to work with the computer use tool in Foundry Agent Service. Computer use is a specialized AI tool that uses a specialized model to perform tasks by interacting with computer systems and applications through their user interfaces. By using computer use, you can create an agent that handles complex tasks and makes decisions by interpreting visual elements and taking action based on on-screen content. 

Use the computer use tool in Foundry Agent Service when you want an agent to interpret screenshots and propose UI actions (for example, clicking a button or typing text). This guide shows how to integrate the tool into an application loop (screenshot -> action -> screenshot) by using the Python, C#, and TypeScript SDKs.

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | - | - | ✔️ | ✔️ |

## Prerequisites

- A [basic or standard agent environment](../../../../agents/environment-setup.md).
- The latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.
- Access to the `computer-use-preview` model. See [Request access](#request-access) below.
- A virtual machine or sandboxed environment for safe testing. Don't run on machines with access to sensitive data.

### Environment variables

Set these environment variables before running the samples:

| Variable | Description |
| --- | --- |
| `FOUNDRY_PROJECT_ENDPOINT` | Your Foundry project endpoint URL. |
| `FOUNDRY_MODEL_DEPLOYMENT_NAME` | Your `computer-use-preview` model deployment name. |

### Quick verification

Verify your authentication and project connection before running the full samples:

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

load_dotenv()

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=credential) as project_client,
):
    print("Connected to project.")
    # Verify you can access the OpenAI client
    openai_client = project_client.get_openai_client()
    print("OpenAI client ready.")
```

If this code runs without errors, your credentials and project endpoint are configured correctly.

## Run the maintained SDK samples (recommended)

The code snippets in this article focus on the agent and Responses API integration. For an end-to-end runnable sample that includes helper code and sample screenshots, use the SDK samples on GitHub.

- Python: https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/agents/tools
- JavaScript: https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentComputerUse.js
- .NET (computer use tool sample): https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Agents.Persistent/samples/Sample33_Computer_Use.md

## Request access 

To access the `computer-use-preview` model, you need to register. Microsoft grants access based on eligibility criteria. If you have access to other limited access models, you still need to request access for this model. 

To request access, see the [application form](https://aka.ms/oai/cuaaccess).

After Microsoft grants access, you need to create a deployment for the model. 


## Code samples

> [!WARNING] 
> Use the computer use tool on virtual machines with no access to sensitive data or critical resources. For more information about the intended uses, capabilities, limitations, risks, and considerations when choosing a use case, see the [Azure OpenAI transparency note](../../../../responsible-ai/openai/transparency-note.md#risk-and-limitations-of-computer-use-preview).

To run this code, you need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

:::zone pivot="python"
### Screenshot initialization for computer use tool execution

The following code sample demonstrates how to create an agent version with the computer use tool, send an initial request with a screenshot, and perform multiple iterations to complete a task.

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentReference, PromptAgentDefinition, ComputerUsePreviewTool

# Import shared helper functions
from computer_use_util import (
    SearchState,
    load_screenshot_assets,
    handle_computer_action_and_take_screenshot,
    print_final_output,
)

load_dotenv()

"""Main function to demonstrate Computer Use Agent functionality."""
# Initialize state machine
current_state = SearchState.INITIAL

# Load screenshot assets
try:
    screenshots = load_screenshot_assets()
    print("Successfully loaded screenshot assets")
except FileNotFoundError:
    print("Failed to load required screenshot assets. Use the maintained SDK sample on GitHub to get the helper file and images.")
    exit(1)
```

### Create an agent version with the tool

```python
project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

computer_use_tool = ComputerUsePreviewTool(display_width=1026, display_height=769, environment="windows")

with project_client:
    agent = project_client.agents.create_version(
        agent_name="ComputerUseAgent",
        definition=PromptAgentDefinition(
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
            instructions="""
            You are a computer automation assistant. 
            
            Be direct and efficient. When you reach the search results page, read and describe the actual search result titles and descriptions you can see.
            """,
            tools=[computer_use_tool],
        ),
        description="Computer automation agent with screen interaction capabilities.",
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```

### One iteration for the tool to process the screenshot and take the next step

```python
    openai_client = project_client.get_openai_client()

    # Initial request with screenshot - start with Bing search page
    print("Starting computer automation session (initial screenshot: cua_browser_search.png)...")
    response = openai_client.responses.create(
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "I need you to help me search for 'OpenAI news'. Please type 'OpenAI news' and submit the search. Once you see search results, the task is complete.",
                    },
                    {
                        "type": "input_image",
                        "image_url": screenshots["browser_search"]["url"],
                        "detail": "high",
                    },  # Start with Bing search page
                ],
            }
        ],
        extra_body={"agent": AgentReference(name=agent.name).as_dict()},
        truncation="auto",
    )

    print(f"Initial response received (ID: {response.id})")
```

### Perform multiple iterations

Make sure you review each iteration and action. The following code sample shows a basic API request. After you send the initial API request, perform a loop where your application code carries out the specified action. Send a screenshot with each turn so the model can evaluate the updated state of the environment. For an example integration for a similar API, see the [Azure OpenAI documentation](../../../../openai/how-to/computer-use.md#playwright-integration).

```python

max_iterations = 10  # Allow enough iterations for completion
iteration = 0

while True:
    if iteration >= max_iterations:
        print(f"\nReached maximum iterations ({max_iterations}). Stopping.")
        break

    iteration += 1
    print(f"\n--- Iteration {iteration} ---")

    # Check for computer calls in the response
    computer_calls = [item for item in response.output if item.type == "computer_call"]

    if not computer_calls:
        print_final_output(response)
        break

    # Process the first computer call
    computer_call = computer_calls[0]
    action = computer_call.action
    call_id = computer_call.call_id

    print(f"Processing computer call (ID: {call_id})")

    # Handle the action and get the screenshot info
    screenshot_info, current_state = handle_computer_action_and_take_screenshot(action, current_state, screenshots)

    print(f"Sending action result back to agent (using {screenshot_info['filename']})...")

    # Regular response with just the screenshot
    response = openai_client.responses.create(
        previous_response_id=response.id,
        input=[
            {
                "call_id": call_id,
                "type": "computer_call_output",
                "output": {
                    "type": "computer_screenshot",
                    "image_url": screenshot_info["url"],
                },
            }
        ],
        extra_body={"agent": AgentReference(name=agent.name).as_dict()},
        truncation="auto",
    )

    print(f"Follow-up response received (ID: {response.id})")
```

### Clean up

```python
project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
print("Agent deleted")
```

### Expected output

The following example shows the expected output when running the previous code sample:

```console
Successfully loaded screenshot assets
Agent created (id: ..., name: ComputerUseAgent, version: 1)
Starting computer automation session (initial screenshot: cua_browser_search.png)...
Initial response received (ID: ...)
--- Iteration 1 ---
Processing computer call (ID: ...)
  Typing text "OpenAI news" - Simulating keyboard input
  -> Action processed: type
Sending action result back to agent (using cua_search_typed.png)...
Follow-up response received (ID: ...)
--- Iteration 2 ---
Processing computer call (ID: ...)
    Click at (512, 384) - Simulating click on UI element
    -> Assuming click on Search button when search field was populated, displaying results.
    -> Action processed: click
Sending action result back to agent (using cua_search_results.png)...
Follow-up response received (ID: ...)
OpenAI news - Latest Updates
Agent deleted
```
:::zone-end

:::zone pivot="csharp"
## Sample for use of an Agent with Computer Use tool

The following C# code sample demonstrates how to create an agent version with the computer use tool, send an initial request with a screenshot, and perform multiple iterations to complete a task. To enable your Agent to use the Computer Use tool, you need to use `ComputerTool` while creating `PromptAgentDefinition`. This example uses synchronous code. For asynchronous usage, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample10_ComputerUse.md) example in the Azure SDK for .NET repository on GitHub.

```csharp
class ComputerUseDemo
{
    

    // Read image files using `ReadImageFile` method.
    private static BinaryData ReadImageFile(string name, [CallerFilePath] string pth = "")
    {
        var dirName = Path.GetDirectoryName(pth) ?? "";
        return new BinaryData(File.ReadAllBytes(Path.Combine(dirName, name)));
    }

    // Create a helper method to parse the ComputerTool outputs and to respond
    // to Agents queries with new screenshots. Note that throughout
    // this sample the media type for image is set. Agents support `image/jpeg`,
    // `image/png`, `image/gif` and `image/webp` media types.
    private static string ProcessComputerUseCall(ComputerCallResponseItem item, string oldScreenshot)
    {
        string currentScreenshot = "browser_search";
        switch (item.Action.Kind)
        {
            case ComputerCallActionKind.Type:
                Console.WriteLine($"  Typing text \"{item.Action.TypeText}\" - Simulating keyboard input");
                currentScreenshot = "search_typed";
                break;
            case ComputerCallActionKind.KeyPress:
                HashSet<string> codes = new(item.Action.KeyPressKeyCodes);
                if (codes.Contains("Return") || codes.Contains("ENTER"))
                {
                    // If we have typed the value to the search field, go to search results.
                    if (string.Equals(oldScreenshot, "search_typed"))
                    {
                        Console.WriteLine("  -> Detected ENTER key press, when search field was populated, displaying results.");
                        currentScreenshot = "search_results";
                    }
                    else
                    {
                        Console.WriteLine("  -> Detected ENTER key press, on results or unpopulated search, do nothing.");
                        currentScreenshot = oldScreenshot;
                    }
                }
                else
                {
                    Console.WriteLine($"  Key press: {item.Action.KeyPressKeyCodes.Aggregate("", (agg, next) => agg + "+" + next)} - Simulating key combination");
                }
                break;
            case ComputerCallActionKind.Click:
                Console.WriteLine($"  Click at ({item.Action.ClickCoordinates.Value.X}, {item.Action.ClickCoordinates.Value.Y}) - Simulating click on UI element");
                if (string.Equals(oldScreenshot, "search_typed"))
                {
                    Console.WriteLine("  -> Assuming click on Search button when search field was populated, displaying results.");
                    currentScreenshot = "search_results";
                }
                else
                {
                    Console.WriteLine("  -> Assuming click on Search on results or when search was not populated, do nothing.");
                    currentScreenshot = oldScreenshot;
                }
                break;
            case ComputerCallActionKind.Drag:
                string pathStr = item.Action.DragPath.ToArray().Select(p => $"{p.X}, {p.Y}").Aggregate("", (agg, next) => $"{agg} -> {next}");
                Console.WriteLine($"  Drag path: {pathStr} - Simulating drag operation");
                break;
            case ComputerCallActionKind.Scroll:
                Console.WriteLine($"  Scroll at ({item.Action.ScrollCoordinates.Value.X}, {item.Action.ScrollCoordinates.Value.Y}) - Simulating scroll action");
                break;
            case ComputerCallActionKind.Screenshot:
                Console.WriteLine("  Taking screenshot - Capturing current screen state");
                break;
            default:
                break;
        }
        Console.WriteLine($"  -> Action processed: {item.Action.Kind}");

        return currentScreenshot;
    }

    public static void Main()
    {
        // Create project client and read the environment variables, which will be used in the next steps.
        var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
        var modelDeploymentName = System.Environment.GetEnvironmentVariable("FOUNDRY_MODEL_DEPLOYMENT_NAME");
        AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

        // Read in three example screenshots and place them into a dictionary.
        Dictionary<string, BinaryData> screenshots = new() {
            { "browser_search", ReadImageFile("Assets/cua_browser_search.png")},
            { "search_typed", ReadImageFile("Assets/cua_search_typed.png")},
            { "search_results", ReadImageFile("Assets/cua_search_results.png")},
        };

        // Create a PromptAgentDefinition with ComputerTool.
        PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
        {
            Instructions = "You are a computer automation assistant.\n\n" +
                            "Be direct and efficient. When you reach the search results page, read and describe the actual search result titles and descriptions you can see.",
            Tools = {
                ResponseTool.CreateComputerTool(
                    environment: new ComputerToolEnvironment("windows"),
                    displayWidth: 1026,
                    displayHeight: 769
                ),
            }
        };
        AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
            agentName: "myAgent",
            options: new(agentDefinition)
        );
        // Create an `ResponseResult` using `ResponseItem`, containing two `ResponseContentPart`:
        // one with the image and another with the text. In the loop, request Agent
        // while it is continuing to browse web. Finally, print the tool output message.
        ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);
        CreateResponseOptions responseOptions = new()
        {
            TruncationMode = ResponseTruncationMode.Auto,
            InputItems =
            {
                ResponseItem.CreateUserMessageItem(
                [
                    ResponseContentPart.CreateInputTextPart("I need you to help me search for 'OpenAI news'. Please type 'OpenAI news' and submit the search. Once you see search results, the task is complete."),
                    ResponseContentPart.CreateInputImagePart(imageBytes: screenshots["browser_search"], imageBytesMediaType: "image/png", imageDetailLevel: ResponseImageDetailLevel.High)
                ]),
            },
        };
        bool computerUseCalled = false;
        string currentScreenshot = "browser_search";
        int limitIteration = 10;
        ResponseResult response;
        do
        {
            response = responseClient.CreateResponse(responseOptions);
            computerUseCalled = false;
            responseOptions.InputItems.Clear();
            responseOptions.PreviousResponseId = response.Id;
            foreach (ResponseItem responseItem in response.OutputItems)
            {
                responseOptions.InputItems.Add(responseItem);
                if (responseItem is ComputerCallResponseItem computerCall)
                {
                    currentScreenshot = ProcessComputerUseCall(computerCall, currentScreenshot);
                    responseOptions.InputItems.Add(ResponseItem.CreateComputerCallOutputItem(callId: computerCall.CallId, output: ComputerCallOutput.CreateScreenshotOutput(screenshotImageBytes: screenshots[currentScreenshot], screenshotImageBytesMediaType: "image/png")));
                    computerUseCalled = true;
                }
            }
            limitIteration--;
        } while (computerUseCalled && limitIteration > 0);
        Console.WriteLine(response.GetOutputText());

        // Clean up resources by deleting Agent.
        projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
    }
}
```

### Expected output

The following example shows the expected output when running the previous code sample:

```console
Agent created (id: ..., name: myAgent, version: 1)
Starting computer automation session (initial screenshot: cua_browser_search.png)...
Initial response received (ID: ...)
--- Iteration 1 ---
Processing computer call (ID: ...)
  Typing text "OpenAI news" - Simulating keyboard input
  -> Action processed: Type
Sending action result back to agent (using cua_search_typed.png)...
Follow-up response received (ID: ...)
--- Iteration 2 ---
Processing computer call (ID: ...)
  Click at (512, 384) - Simulating click on UI element
  -> Assuming click on Search button when search field was populated, displaying results.
  -> Action processed: Click
Sending action result back to agent (using cua_search_results.png)...
Follow-up response received (ID: ...)
OpenAI news - Latest Updates
Agent deleted
```

:::zone-end

:::zone pivot="typescript"
## Sample for use of an Agent with Computer Use tool

The following TypeScript code sample demonstrates how to create an agent version with the computer use tool, send an initial request with a screenshot, and perform multiple iterations to complete a task. For a JavaScript example, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentComputerUse.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";
import {
  SearchState,
  loadScreenshotAssets,
  handleComputerActionAndTakeScreenshot,
  printFinalOutput,
  type ComputerAction,
} from "./computerUseUtil.js";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName =
    process.env["FOUNDRY_MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";

export async function main(): Promise<void> {
  // Initialize state machine
  let currentState = SearchState.INITIAL;

  // Load screenshot assets
  const screenshots = loadScreenshotAssets();
  console.log("Successfully loaded screenshot assets");

  // Create AI Project client
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  console.log("Creating Computer Use Agent...");
  const agent = await project.agents.createVersion("ComputerUseAgent", {
    kind: "prompt" as const,
    model: deploymentName,
    instructions: `
You are a computer automation assistant.

Be direct and efficient. When you reach the search results page, read and describe the actual search result titles and descriptions you can see.
    `.trim(),
    tools: [
      {
        type: "computer_use_preview",
        display_width: 1026,
        display_height: 769,
        environment: "windows" as const,
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Initial request with screenshot - start with Bing search page
  console.log(
    "Starting computer automation session (initial screenshot: cua_browser_search.png)...",
  );
  let response = await openAIClient.responses.create(
    {
      input: [
        {
          role: "user" as const,
          content: [
            {
              type: "input_text",
              text: "I need you to help me search for 'OpenAI news'. Please type 'OpenAI news' and submit the search. Once you see search results, the task is complete.",
            },
            {
              type: "input_image",
              image_url: screenshots.browser_search.url,
              detail: "high",
            },
          ],
        },
      ],
      truncation: "auto",
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
    },
  );

  console.log(`Initial response received (ID: ${response.id})`);

  // Main interaction loop with deterministic completion
  const maxIterations = 10; // Allow enough iterations for completion
  let iteration = 0;

  while (iteration < maxIterations) {
    iteration++;
    console.log(`\n--- Iteration ${iteration} ---`);

    // Check for computer calls in the response
    const computerCalls = response.output.filter((item) => item.type === "computer_call");

    if (computerCalls.length === 0) {
      printFinalOutput({
        output: response.output,
        status: response.status ?? "",
      });
      break;
    }

    // Process the first computer call
    const computerCall = computerCalls[0];
    const action: ComputerAction = computerCall.action;
    const callId: string = computerCall.call_id;

    console.log(`Processing computer call (ID: ${callId})`);

    // Handle the action and get the screenshot info
    const [screenshotInfo, updatedState] = handleComputerActionAndTakeScreenshot(
      action,
      currentState,
      screenshots,
    );
    currentState = updatedState;

    console.log(`Sending action result back to agent (using ${screenshotInfo.filename})...`);
    // Regular response with just the screenshot
    response = await openAIClient.responses.create(
      {
        previous_response_id: response.id,
        input: [
          {
            call_id: callId,
            type: "computer_call_output",
            output: {
              type: "computer_screenshot",
              image_url: screenshotInfo.url,
            },
          },
        ],
        truncation: "auto",
      },
      {
        body: { agent: { name: agent.name, type: "agent_reference" } },
      },
    );

    console.log(`Follow-up response received (ID: ${response.id})`);
  }

  if (iteration >= maxIterations) {
    console.log(`\nReached maximum iterations (${maxIterations}). Stopping.`);
  }

  // Clean up resources
  console.log("\nCleaning up...");
  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  console.log("\nComputer Use Agent sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

The following example shows the expected output when running the previous code sample:

```console
Successfully loaded screenshot assets
Creating Computer Use Agent...
Agent created (id: ..., name: ComputerUseAgent, version: 1)
Starting computer automation session (initial screenshot: cua_browser_search.png)...
Initial response received (ID: ...)
--- Iteration 1 ---
Processing computer call (ID: ...)
  Typing text "OpenAI news" - Simulating keyboard input
  -> Action processed: type
Sending action result back to agent (using cua_search_typed.png)...
Follow-up response received (ID: ...)
--- Iteration 2 ---
Processing computer call (ID: ...)
    Click at (512, 384) - Simulating click on UI element
    -> Assuming click on Search button when search field was populated, displaying results.
    -> Action processed: click
Sending action result back to agent (using cua_search_results.png)...
Follow-up response received (ID: ...)
OpenAI news - Latest Updates
Cleaning up...
Agent deleted
Computer Use Agent sample completed!
```
:::zone-end

## What you can do with the computer use tool

After you integrate the request-and-response loop (screenshot -> action -> screenshot), the computer use tool can help an agent:

- Propose UI actions such as clicking, typing, scrolling, and requesting a new screenshot.
- Adapt to UI changes by re-evaluating the latest screenshot after each action.
- Work across browser and desktop UI, depending on how you host your sandboxed environment.

The tool doesn't directly control a device. Your application executes each requested action and returns an updated screenshot.

## Differences between browser automation and computer use

The following table lists some of the differences between the computer use tool and [browser automation](../../../../agents/how-to/tools/browser-automation.md) tool.

| Feature                        | Browser Automation          | Computer use tool          |
|--------------------------------|-----------------------------|----------------------------|
| Model support                  | All GPT models              | `Computer-use-preview` model only |
| Can I visualize what's happening?     | No                          | Yes                        |
| How it understands the screen  | Parses the HTML or XML pages into DOM documents | Raw pixel data from screenshots |
| How it acts                    | A list of actions provided by the model | Virtual keyboard and mouse |
| Is it multistep?                    | Yes                         | Yes                        |
| Interfaces                     | Browser                     | Computer and browser       |
| Do I need to bring my own resource?    | Your own Playwright resource with the keys stored as a connection. | No additional resource required but we highly recommend running this tool in a sandboxed environment.          |

## Regional support 

To use the computer use tool, you need a [computer use model](../../../../foundry-models/concepts/models-sold-directly-by-azure.md#computer-use-preview) deployment. The computer use model is available in the following regions: 
* `eastus2` 
* `swedencentral` 
* `southindia` 

## Understanding the computer use integration 

When working with the computer use tool, integrate it into your application by performing the following steps: 

1. Send a request to the model that includes a call to the computer use tool, the display size, and the environment. You can also include a screenshot of the initial state of the environment in the first API request. 
1. Receive a response from the model. If the response has action items, those items contain suggested actions to make progress toward the specified goal. For example, an action might be `screenshot` so the model can assess the current state with an updated screenshot, or `click` with X/Y coordinates indicating where the mouse should be moved. 
1. Execute the action by using your application code on your computer or browser environment. 
1. After executing the action, capture the updated state of the environment as a screenshot. 
1. Send a new request with the updated state as a `tool_call_output`, and repeat this loop until the model stops requesting actions or you decide to stop. 

   > [!NOTE]
   > Before using the tool, set up an environment that can capture screenshots and execute the recommended actions by the agent. For safety reasons, use a sandboxed environment, such as Playwright.

## Manage conversation history

Use the `previous_response_id` parameter to link the current request to the previous response. Use this parameter when you don't want to send the full conversation history with each call.

If you don't use this parameter, make sure to include all the items returned in the response output of the previous request in your inputs array. This requirement includes reasoning items if present. 

## Safety checks and security considerations

> [!WARNING] 
> Computer use carries substantial security and privacy risks and user responsibility. Both errors in judgment by the AI and the presence of malicious or confusing instructions on web pages, desktops, or other operating environments that the AI encounters might cause it to execute commands you or others don't intend. These risks could compromise the security of your or other users’ browsers, computers, and any accounts to which AI has access, including personal, financial, or enterprise systems.
> 
> Use the computer use tool on virtual machines with no access to sensitive data or critical resources. For more information about the intended uses, capabilities, limitations, risks, and considerations when choosing a use case, see the [Azure OpenAI transparency note](../../../../responsible-ai/openai/transparency-note.md#risk-and-limitations-of-computer-use-preview).

The API has safety checks to help protect against prompt injection and model mistakes. These checks include: 

**Malicious instruction detection**: The system evaluates the screenshot image and checks if it contains adversarial content that might change the model's behavior. 

**Irrelevant domain detection**: The system evaluates the `current_url` parameter (if provided) and checks if the current domain is relevant given the conversation history. 

**Sensitive domain detection**: The system checks the `current_url` parameter (if provided) and raises a warning when it detects the user is on a sensitive domain. 

If one or more of the preceding checks are triggered, the model raises a safety check when it returns the next `computer_call` by using the `pending_safety_checks` parameter. 

```json
"output": [ 
    { 
        "type": "reasoning", 
        "id": "rs_67cb...", 
        "summary": [ 
            { 
                "type": "summary_text", 
                "text": "Exploring 'File' menu option." 
            } 
        ] 
    }, 
    { 
        "type": "computer_call", 
        "id": "cu_67cb...", 
        "call_id": "call_nEJ...", 
        "action": { 
            "type": "click", 
            "button": "left", 
            "x": 135, 
            "y": 193 
        }, 
        "pending_safety_checks": [ 
            { 
                "id": "cu_sc_67cb...", 
                "code": "malicious_instructions", 
                "message": "We've detected instructions that may cause your application to perform malicious or unauthorized actions. Please acknowledge this warning if you'd like to proceed." 
            } 
        ], 
        "status": "completed" 
    } 
]
```

You need to pass the safety checks back as `acknowledged_safety_checks` in the next request to proceed. 

```json
"input":[ 
        { 
            "type": "computer_call_output", 
            "call_id": "<call_id>", 
            "acknowledged_safety_checks": [ 
                { 
                    "id": "<safety_check_id>", 
                    "code": "malicious_instructions", 
                    "message": "We've detected instructions that may cause your application to perform malicious or unauthorized actions. Please acknowledge this warning if you'd like to proceed." 
                } 
            ], 
            "output": { 
                "type": "computer_screenshot", 
                "image_url": "<image_url>" 
            } 
        } 
    ]
```

## Safety check handling 

In all cases where `pending_safety_checks` are returned, hand over actions to the end user to confirm proper model behavior and accuracy. 

`malicious_instructions` and `irrelevant_domain`: End users should review model actions and confirm that the model behaves as intended. 

`sensitive_domain`: Ensure an end user actively monitors the model actions on these sites. The exact implementation of this "watch mode" can vary by application, but a potential example could be collecting user impression data on the site to make sure there's active end user engagement with the application. 

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| You don't see a `computer_call` in the response. | The agent isn't configured with the computer use tool, the deployment isn't a computer use model, or the prompt doesn't require UI interaction. | Confirm the agent has a `computer_use_preview` tool, your deployment is the `computer-use-preview` model, and your prompt requires a UI action (type, click, or screenshot). |
| The sample code fails with missing helper files or screenshots. | The snippets reference helper utilities and sample images that aren't part of this documentation repo. | Run the maintained SDK samples in the "Run the maintained SDK samples" section, or copy the helper file and sample images from the SDK repo into your project. |
| The loop stops at the iteration limit. | The task needs more turns, or the app isn't applying the actions the model requests. | Increase the iteration limit, and verify that your code executes the requested action and sends a new screenshot after each turn. |
| You receive `pending_safety_checks`. | The service detected a potential security risk (for example, prompt injection or a sensitive domain). | Pause automation, require an end user to review the request, and only continue after you send `acknowledged_safety_checks` with the next `computer_call_output`. |
| The model repeats "take a screenshot" without making progress. | The screenshot isn't updating, is low quality, or doesn't show the relevant UI state. | Send a fresh screenshot after each action and use a higher-detail image when needed. Ensure the screenshot includes the relevant UI. |
| Access denied when requesting `computer-use-preview` model. | You haven't registered for access or access hasn't been granted. | Submit the [application form](https://aka.ms/oai/cuaaccess) and wait for approval. Check your email for confirmation. |
| Screenshot encoding errors. | Image format not supported or base64 encoding issue. | Use PNG or JPEG format. Ensure proper base64 encoding without corruption. Check image dimensions match `display_width` and `display_height`. |
| Actions execute on wrong coordinates. | Screen resolution mismatch between screenshot and actual display. | Ensure `display_width` and `display_height` in `ComputerUsePreviewTool` match your actual screen resolution. |
| Model hallucinates UI elements. | Screenshot quality too low or UI changed between turns. | Use higher resolution screenshots. Send fresh screenshots immediately after each action. Reduce delay between action and screenshot. |

## Related content

[Follow tool best practices](../../concepts/tool-best-practice.md)

[Compare with browser automation](browser-automation.md)

[Computer use risk and limitations](../../../../responsible-ai/openai/transparency-note.md#risk-and-limitations-of-computer-use-preview)
