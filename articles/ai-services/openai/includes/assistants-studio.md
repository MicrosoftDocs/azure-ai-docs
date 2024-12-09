---
title: 'Quickstart: Use Azure OpenAI Assistants (Preview) via the Azure OpenAI Studio'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with Azure OpenAI Studio. 
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-openai
ms.topic: include
ms.date: 05/31/2024
---

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- An Azure OpenAI resource with a [compatible model in a supported region](../concepts/models.md#assistants-preview).
- We recommend reviewing the [Responsible AI transparency note](/legal/cognitive-services/openai/transparency-note?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=text) and other [Responsible AI resources](/legal/cognitive-services/openai/overview?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext) to familiarize yourself with the capabilities and limitations of the Azure OpenAI Service.

## Go to the Azure OpenAI Studio

Navigate to Azure OpenAI Studio at <a href="https://oai.azure.com/" target="_blank">https://oai.azure.com/</a> and sign-in with credentials that have access to your Azure OpenAI resource. During or after the sign-in workflow, select the appropriate directory, Azure subscription, and Azure OpenAI resource.

From the Azure OpenAI Studio landing page launch the Assistant's playground from the left-hand navigation **Playground** > **Assistants (Preview)**

:::image type="content" source="../media/quickstarts/assistants-studio.png" alt-text="Screenshot of the Azure OpenAI Studio landing page." lightbox="../media/quickstarts/assistants-studio.png":::

## Playground

The Assistants playground allows you to explore, prototype, and test AI Assistants without needing to run any code. From this page, you can quickly iterate and experiment with new ideas.

:::image type="content" source="../media/quickstarts/assistants-playground.png" alt-text="Screenshot of the Assistant configuration screen without all the values filled in." lightbox="../media/quickstarts/assistants-playground.png":::

### Assistant setup

Use the **Assistant setup** pane to create a new AI assistant or to select an existing assistant. 

| **Name** | **Description** |
|:---|:---|
| **Assistant name** | Your deployment name that is associated with a specific model. |
| **Instructions** | Instructions are similar to system messages this is where you give the model guidance about how it should behave and any context it should reference when generating a response. You can describe the assistant's personality, tell it what it should and shouldn't answer, and tell it how to format responses. You can also provide examples of the steps it should take when answering responses. |
| **Deployment** | This is where you set which model deployment to use with your assistant. |
| **Functions**| Create custom function definitions for the models to formulate API calls and structure data outputs based on your specifications |
| **Code interpreter** | Code interpreter provides access to a sandboxed Python environment that can be used to allow the model to test and execute code. |
| **Files** | You can upload up to 20 files, with a max file size of 512 MB to use with tools. You can upload up to 10,000 files using [AI Foundry portal](../assistants-quickstart.md?pivots=ai-foundry-portal). |

### Tools

An individual assistant can access up to 128 tools including `code interpreter`, as well as any custom tools you create via [functions](../how-to/assistant-functions.md).

### Chat session

Chat session also known as a *thread* within the Assistant's API is where the conversation between the user and assistant occurs. Unlike traditional chat completion calls there is no limit to the number of messages in a thread. The assistant will automatically compress requests to fit the input token limit of the model.

This also means that you are not controlling how many tokens are passed to the model during each turn of the conversation. Managing tokens is abstracted away and handled entirely by the Assistants API.

Select the **Clear chat** button to delete the current conversation history.

Underneath the text input box there are two buttons:

- Add a message without run.
- Add and run.

### Logs

Logs provide a detailed snapshot of what the assistant API activity.

### Show panels

By default there are three panels: assistant setup, chat session, and Logs. **Show panels** allows you to add, remove, and rearrange the panels. If you ever close a panel and need to get it back, use **Show panels** to restore the lost panel.

## Create your first assistant

1. From the assistant setup drop-down, select **New**
2. Give your Assistant a name
3. Enter the following instructions "You are an AI assistant that can write code to help answer math questions"
4. Select a deployment of `gpt-4 (1106-preview)`. The dropdown will display your custom deployment names so if your model/deployment names are different you should choose a deployment where the underlying model is equivalent to the 1106-preview model.
5. Select the toggle enabling code interpreter.
6. Select Save.

    :::image type="content" source="../media/quickstarts/assistant-configuration.png" alt-text="Screenshot of the assistant with configuration details entered." lightbox="../media/quickstarts/assistant-configuration.png":::

7. Enter a question for the assistant to answer: "I need to solve the equation `3x + 11 = 14`. Can you help me?"
8. Select the **Add and run button** :::image type="icon" source="../media/quickstarts/run.png":::

    ```output
    The solution to the equation (3x + 11 = 14) is (x = 1).
    ```

    While we can see that answer is correct, to confirm that the model used code interpreter to get to this answer, and that the code it wrote is valid rather than just repeating an answer from the model's training data we'll ask another question.

9. Enter the follow-up question: "Show me the code you ran to get this solution."

    ```output
    Certainly! Here's the Python code I ran to find the solution for the equation (3x + 11 = 14):
    ```

    ```python
    from sympy import symbols, Eq, solve  
      
    # Define the variable  
    x = symbols('x')  
      
    # Define the equation  
    equation = Eq(3*x + 11, 14)  
      
    # Solve the equation  
    solution = solve(equation, x)  
    solution  
    ```

:::image type="content" source="../media/quickstarts/assistant-session.png" alt-text="Screenshot of conversation session in the Assistant playground." lightbox="../media/quickstarts/assistant-session.png":::

You could also consult the logs in the right-hand panel to confirm that code interpreter was used and to validate the code that was run to generate the response. It is important to remember that while code interpreter gives the model the capability to respond to more complex math questions by converting the questions into code and running in a sandboxed Python environment, you still need to validate the response to confirm that the model correctly translated your question into a valid representation in code.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## See also

* Learn more about how to use Assistants with our [How-to guide on Assistants](../how-to/assistant.md).
* [Azure OpenAI Assistants API samples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/Assistants)

