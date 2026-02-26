---
title: Prompt flow in Microsoft Foundry portal
titleSuffix: Microsoft Foundry
description: This article introduces prompt flow in Microsoft Foundry portal.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-prompt-flow
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - hub-only
ms.topic: concept-article
ms.date: 01/30/2026
ms.reviewer: none
ms.author: lagayhar
author: lgayhardt
ms.collection: ce-skilling-ai-copilot, ce-skilling-fresh-tier1
ms.update-cycle: 180-days
---

# Prompt flow in Microsoft Foundry portal

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Prompt flow is a development tool that streamlines the entire development cycle of AI applications powered by large language models (LLMs). Prompt flow provides a comprehensive solution that simplifies the process of prototyping, experimenting, iterating, and deploying your AI applications.

Prompt flow is available independently as an open-source project on [GitHub](https://github.com/microsoft/promptflow), with its own SDK and [VS Code extension](https://marketplace.visualstudio.com/items?itemName=prompt-flow.prompt-flow). Prompt flow is also available and recommended to use as a feature within both [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) and [Azure Machine Learning studio](https://ml.azure.com). This set of documentation focuses on prompt flow in Foundry portal.

[!INCLUDE [hub-only-prereq](../includes/uses-hub-only.md)]

Definitions:

- *Prompt flow* is a feature that you can use to generate, customize, or run a flow.
- A *flow* is an executable instruction set that implements the AI logic.​​ You can create or run flows through multiple tools, like a prebuilt canvas, LangChain, and others. You save iterations of a flow as assets. Once deployed, a flow becomes an API. Not all flows are prompt flows. Rather, prompt flow is one way to create a flow. 
- A *prompt* is a package of input sent to a model, consisting of the user input, system message, and any examples. User input is text submitted in the chat window. System message is a set of instructions to the model that scope its behaviors and functionality.
- A *sample flow* is a simple, prebuilt orchestration flow that shows how flows work, and can be customized. 
- A *sample prompt* is a defined prompt for a specific scenario that can be copied from a library and used as-is or modified in prompt design. 

## Benefits of prompt flow

By using prompt flow in Foundry portal, you can:

- Orchestrate executable flows with LLMs, prompts, and Python tools through a visualized graph.
- Debug, share, and iterate your flows with ease through team collaboration.
- Create prompt variants and compare their performance.

### Prompt engineering agility

- Interactive authoring experience: Prompt flow provides a visual representation of the flow's structure, so you can easily understand and navigate projects. 
- Variants for prompt tuning: You can create and compare multiple prompt variants, facilitating an iterative refinement process.
- Evaluation: Built-in evaluation flows enable you to assess the quality and effectiveness of your prompts and flows.
- Comprehensive resources: Prompt flow includes a library of built-in tools, samples, and templates that serve as a starting point for development, inspiring creativity, and accelerating the process.

### Enterprise readiness

- Collaboration: Prompt flow supports team collaboration, so multiple users can work together on prompt engineering projects, share knowledge, and maintain version control.
- All-in-one platform: Prompt flow streamlines the entire prompt engineering process, from development and evaluation to deployment and monitoring. You can effortlessly deploy your flows as Azure AI endpoints and monitor their performance in real-time, ensuring optimal operation and continuous improvement.
- Enterprise Readiness Solutions: Prompt flow applies robust Azure AI enterprise readiness solutions, providing a secure, scalable, and reliable foundation for the development, experimentation, and deployment of flows.

By using prompt flow in Foundry portal, you can unleash prompt engineering agility, collaborate effectively, and apply enterprise-grade solutions for successful LLM-based application development and deployment.

## Flow development lifecycle

Prompt flow offers a well-defined process that facilitates the seamless development of AI applications. By using it, you can effectively progress through the stages of developing, testing, tuning, and deploying flows, ultimately resulting in the creation of fully fledged AI applications.

The lifecycle consists of the following stages:

- Initialization: Identify the business use case, collect sample data, learn to build a basic prompt, and develop a flow that extends its capabilities.
- Experimentation: Run the flow against sample data, evaluate the prompt's performance, and iterate on the flow if necessary. Continuously experiment until satisfied with the results.
- Evaluation and refinement: Assess the flow's performance by running it against a larger dataset, evaluate the prompt's effectiveness, and refine as needed. Proceed to the next stage if the results meet the desired criteria.
- Production: Optimize the flow for efficiency and effectiveness, deploy it, monitor performance in a production environment, and gather usage data and feedback. Use this information to improve the flow and contribute to earlier stages for further iterations.

By following this structured and methodical approach, prompt flow empowers you to develop, rigorously test, fine-tune, and deploy flows with confidence, resulting in the creation of robust and sophisticated AI applications.

## Flow types

In Foundry portal, you can start a new flow by selecting a flow type or a template from the gallery. 

:::image type="content" source="../media/prompt-flow/type-or-gallery.png" alt-text="Screenshot of example flow types and templates from the gallery." lightbox="../media/prompt-flow/type-or-gallery.png":::

Here are some examples of flow types:

- **Standard flow**: Designed for general application development, the standard flow allows you to create a flow using a wide range of built-in tools for developing LLM-based applications. It provides flexibility and versatility for developing applications across different domains.
- **Chat flow**: Tailored for conversational application development, the Chat flow builds upon the capabilities of the standard flow and provides enhanced support for chat inputs and outputs and chat history management. By using native conversation mode and built-in features, you can seamlessly develop and debug your applications within a conversational context.
- **Evaluation flow**: Designed for evaluation scenarios, the evaluation flow enables you to create a flow that takes the outputs of previous flow runs as inputs. This flow type allows you to evaluate the performance of previous run results and output relevant metrics, facilitating the assessment and improvement of their models or applications.

## Flows

A flow in Prompt flow serves as an executable workflow that streamlines the development of your LLM-based AI application. It provides a comprehensive framework for managing data flow and processing within your application.

Within a flow, nodes take center stage, representing specific tools with unique capabilities. These nodes handle data processing, task execution, and algorithmic operations, with inputs and outputs. By connecting nodes, you establish a seamless chain of operations that guides the flow of data through your application.

To facilitate node configuration and fine-tuning, a visual representation of the workflow structure is provided through a DAG (Directed Acyclic Graph) graph. This graph showcases the connectivity and dependencies between nodes, providing a clear overview of the entire workflow.

:::image type="content" source="../media/prompt-flow/dag-graph-example.png" alt-text="Screenshot of an example directed acyclic graph in prompt flow editor." lightbox="../media/prompt-flow/dag-graph-example.png":::

By using the flow feature in Prompt flow, you can design, customize, and optimize the logic of your AI application. The cohesive arrangement of nodes ensures efficient data processing and effective flow management, empowering you to create robust and advanced applications.

## Prompt flow tools

Tools are the fundamental building blocks of a flow.

In Foundry portal, tool options include the [LLM tool](../how-to/prompt-flow-tools/llm-tool.md), [Prompt tool](../how-to/prompt-flow-tools/prompt-tool.md), [Python tool](../how-to/prompt-flow-tools/python-tool.md), and more.

:::image type="content" source="../media/prompt-flow/tool-options.png" alt-text="Screenshot of tool options in prompt flow editor." lightbox="../media/prompt-flow/tool-options.png":::

Each tool is a simple, executable unit with a specific function. By combining different tools, you can create a flow that accomplishes a wide range of goals. For example, you can use the LLM tool to generate text or summarize an article and the Python tool to process the text to inform the next flow component or result.

One of the key benefits of Prompt flow tools is their seamless integration with third-party APIs and Python open source packages. This integration not only improves the functionality of large language models but also makes the development process more efficient for developers.

If the prompt flow tools in Foundry portal don't meet your requirements, you can [develop your own custom tool and make it a tool package](https://microsoft.github.io/promptflow/how-to-guides/develop-a-tool/create-and-use-tool-package.html). To discover more custom tools developed by the open source community, visit [prompt flow custom tools](https://microsoft.github.io/promptflow/integrations/tools/index.html).

## Related content

- [Build with prompt flow in Foundry portal](../how-to/flow-develop.md)
- [Get started with prompt flow in VS Code](https://microsoft.github.io/promptflow/how-to-guides/quick-start.html)
