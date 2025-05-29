---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 03/28/2025
ms.custom: devx-track-ts
---


| [Reference documentation](/javascript/api/overview/azure/ai-projects-readme) | [Samples](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/README.md) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-projects) | [Package (npm)](https://www.npmjs.com/package/@azure/ai-projects) |

## Prerequisites

[!INCLUDE [universal-prerequisites](universal-prerequisites.md)]



## Configure and run an agent

| Component | Description                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent     | Custom AI that uses AI models with tools.                                                                                                                                                                                  |
| Tool      | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information.               |
| Thread    | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context.                                                                                     |
| Message   | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread.                                                                                                 |
| Run       | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. |
| Run Step  | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during its run. Examining Run Steps allows you to understand how the agent is getting to its results.                                |

Key objects in this code include: 

* [AgentsClient](/javascript/api/@azure/ai-agents/agentsclient)
* [ToolUtility](/javascript/api/@azure/ai-agents/toolutility)

First, initialize a new project by running:

```console
npm init -y
```

Run the following commands to install the npm packages required.

```console
npm install @azure/ai-agents @azure/identity
npm install dotenv
```

Next, to authenticate your API requests and run the program, use the [az login](/cli/azure/authenticate-azure-cli-interactively) command to sign into your Azure subscription.

```azurecli
az login
```

Use the following code to create and run an agent which uploads [a CSV file](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-agents/data/nifty500QuarterlyResults.csv) of data then generates a bar chart from that data. To run this code, you'll need to get the endpoint for your project. This string is in the format:

`https://<AIFoundryResourceName>.services.ai.azure.com/api/projects/<ProjectName>`

[!INCLUDE [endpoint-string-portal](endpoint-string-portal.md)]

For example, your endpoint looks something like:

`https://myresource.services.ai.azure.com/api/projects/myproject`

Set this endpoint as an environment variable named `PROJECT_ENDPOINT` in a `.env` file.

> [!IMPORTANT] 
> * This quickstart code uses environment variables for sensitive configuration. Never commit your `.env` file to version control by making sure `.env` is listed in your `.gitignore` file.
> * _Remember: If you accidentally commit sensitive information, consider those credentials compromised and rotate them immediately._


Next, create an `index.js` file and paste in the following code:

```typescript
// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

/**
 * This sample demonstrates how to use agent operations with code interpreter from the Azure Agents service.
 *
 * @summary demonstrates how to use agent operations with code interpreter.
 */
// @ts-nocheck
import type {
  MessageDeltaChunk,
  MessageDeltaTextContent,
  MessageImageFileContent,
  MessageTextContent,
  ThreadRun,
} from "@azure/ai-agents";
import {
  RunStreamEvent,
  MessageStreamEvent,
  DoneEvent,
  ErrorEvent,
  AgentsClient,
  isOutputOfType,
  ToolUtility,
} from "@azure/ai-agents";
import { DefaultAzureCredential } from "@azure/identity";

import * as fs from "fs";
import path from "node:path";
import "dotenv/config";

const projectEndpoint = process.env["PROJECT_ENDPOINT"] || "<project endpoint>";
const modelDeploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "gpt-4o";

export async function main(): Promise<void> {
  // Create an Azure AI Client
  const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());

  // Upload file and wait for it to be processed
  const filePath = "./data/nifty500QuarterlyResults.csv";
  const localFileStream = fs.createReadStream(filePath);
  const localFile = await client.files.upload(localFileStream, "assistants", {
    fileName: "myLocalFile",
  });

  console.log(`Uploaded local file, file ID : ${localFile.id}`);

  // Create code interpreter tool
  const codeInterpreterTool = ToolUtility.createCodeInterpreterTool([localFile.id]);

  // Notice that CodeInterpreter must be enabled in the agent creation, otherwise the agent will not be able to see the file attachment
  const agent = await client.createAgent(modelDeploymentName, {
    name: "my-agent",
    instructions: "You are a helpful agent",
    tools: [codeInterpreterTool.definition],
    toolResources: codeInterpreterTool.resources,
  });
  console.log(`Created agent, agent ID: ${agent.id}`);

  // Create a thread
  const thread = await client.threads.create();
  console.log(`Created thread, thread ID: ${thread.id}`);

  // Create a message
  const message = await client.messages.create(
    thread.id,
    "user",
    "Could you please create a bar chart in the TRANSPORTATION sector for the operating profit from the uploaded CSV file and provide the file to me?",
  );

  console.log(`Created message, message ID: ${message.id}`);

  // Create and execute a run
  const streamEventMessages = await client.runs.create(thread.id, agent.id).stream();

  for await (const eventMessage of streamEventMessages) {
    switch (eventMessage.event) {
      case RunStreamEvent.ThreadRunCreated:
        console.log(`ThreadRun status: ${(eventMessage.data as ThreadRun).status}`);
        break;
      case MessageStreamEvent.ThreadMessageDelta:
        {
          const messageDelta = eventMessage.data as MessageDeltaChunk;
          messageDelta.delta.content.forEach((contentPart) => {
            if (contentPart.type === "text") {
              const textContent = contentPart as MessageDeltaTextContent;
              const textValue = textContent.text?.value || "No text";
              console.log(`Text delta received:: ${textValue}`);
            }
          });
        }
        break;

      case RunStreamEvent.ThreadRunCompleted:
        console.log("Thread Run Completed");
        break;
      case ErrorEvent.Error:
        console.log(`An error occurred. Data ${eventMessage.data}`);
        break;
      case DoneEvent.Done:
        console.log("Stream completed.");
        break;
    }
  }

  // Delete the original file from the agent to free up space (note: this does not delete your version of the file)
  await client.files.delete(localFile.id);
  console.log(`Deleted file, file ID : ${localFile.id}`);

  // Print the messages from the agent
  const messagesIterator = client.messages.list(thread.id);
  const messagesArray = [];
  for await (const m of messagesIterator) {
    messagesArray.push(m);
  }
  console.log("Messages:", messagesArray);

  // Get most recent message from the assistant
// Get most recent message from the assistant
  const assistantMessage = messagesArray.find((msg) => msg.role === "assistant");
  if (assistantMessage) {
    // Look for an image file in the assistant's message
    const imageFileOutput = assistantMessage.content.find(content => 
      content.type === "image_file" && content.imageFile?.fileId);
    
    if (imageFileOutput) {
      try {
        // Save the newly created file
        console.log(`Saving new files...`);
        const imageFile = imageFileOutput.imageFile.fileId;
        const imageFileName = path.resolve(
          "./data/" + (await client.files.get(imageFile)).filename + "ImageFile.png",
        );
        console.log(`Image file name : ${imageFileName}`);

        const fileContent = await client.files.getContent(imageFile).asNodeStream();
        if (fileContent && fileContent.body) {
          const chunks = [];
          for await (const chunk of fileContent.body) {
            chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
          }
          const buffer = Buffer.concat(chunks);
          fs.writeFileSync(imageFileName, buffer);
          console.log(`Successfully saved image to ${imageFileName}`);
        } else {
          console.error("No file content available in the response");
        }
      } catch (error) {
        console.error("Error saving image file:", error);
      }
    } else {
      console.log("No image file found in assistant's message");
    }
  } else {
    console.log("No assistant message found");
  }

  // Iterate through messages and print details for each annotation
  console.log(`Message Details:`);
  messagesArray.forEach((m) => {
    console.log(`File Paths:`);
    console.log(`Type: ${m.content[0].type}`);
    if (isOutputOfType<MessageTextContent>(m.content[0], "text")) {
      const textContent = m.content[0] as MessageTextContent;
      console.log(`Text: ${textContent.text.value}`);
    }
    console.log(`File ID: ${m.id}`);
    // firstId and lastId are properties of the paginator, not the messages array
    // Removing these references as they don't exist in this context
  });

  // Delete the agent once done
  await client.deleteAgent(agent.id);
  console.log(`Deleted agent, agent ID: ${agent.id}`);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```


Run the code using `node index.js`. This code generated a bar chart in the TRANSPORTATION sector for the operating profit from the uploaded CSV file and provided the file to you. Open the PNG file. Full [sample source code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-agents/samples/v1-beta/typescript/src/codeInterpreterWithStreaming.ts) available.

:::image type="content" source="https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-agents/data/image_file.png" alt-text="Screenshot of generated image which shows bar chart in the TRANSPORTATION sector for the operating profit from the uploaded CSV file":::