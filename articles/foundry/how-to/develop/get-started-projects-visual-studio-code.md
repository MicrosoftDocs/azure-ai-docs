---
title: "Microsoft Foundry Toolkit for Visual Studio Code overview"
description: "Learn how Microsoft Foundry Toolkit helps you discover models and build, test, deploy, evaluate, and monitor AI apps and agents in Visual Studio Code."
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-sdk
content_well_notification:
  - AI-contribution
ai-usage: ai-assisted
ms.topic: concept-article
ms.date: 08/20/2026
ms.reviewer: erichen
ms.author: rotabor
author: bobtabor-msft

# customer intent: As an AI app developer, I want to understand Microsoft Foundry Toolkit for Visual Studio Code so that I can use its model and agent development capabilities.
ms.custom:
  - classic-and-new
  - doc-kit-assisted
---

# Microsoft Foundry Toolkit for Visual Studio Code overview

Microsoft Foundry Toolkit for Visual Studio Code is an extension for building,
testing, deploying, evaluating, and monitoring AI apps and agents. Use it
locally or connect to Microsoft Foundry to manage your AI development workflow
without leaving Visual Studio Code.

Foundry Toolkit is the new name for AI Toolkit. It also includes the
capabilities previously provided by the separate Microsoft Foundry extension,
so you can work with local resources and Foundry resources in one extension.

## Who should use Foundry Toolkit

Foundry Toolkit supports different roles and levels of AI development
experience:

- **Application developers** can add generative AI features to web, desktop,
  and mobile apps.
- **AI and machine learning engineers** can compare, customize, optimize, and
  deploy models and agents.
- **Data scientists and researchers** can experiment with prompts, models,
  datasets, and evaluation criteria.
- **Educators and students** can explore generative AI concepts through
  interactive playgrounds and local models.

## How the Toolkit workspace is organized

Foundry Toolkit separates resources that you have from actions that you can
take. The extension has three main sections.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/foundry-toolkit-overview.png" alt-text="Screenshot of Foundry Toolkit in Visual Studio Code with My Resources, Developer Tools, and Help and Feedback sections." lightbox="../../media/how-to/get-started-projects-vs-code/foundry-toolkit-overview.png":::

| Section | Purpose |
| --- | --- |
| **My Resources** | View models, agents, tools, knowledge sources, evaluations, recent resources, local resources, and resources in your Foundry project. |
| **Developer Tools** | Discover models and tools. Build, debug, deploy, test, evaluate, and monitor AI apps and agents. |
| **Help And Feedback** | Ask Copilot, get started, open documentation and release information, report issues, or join the community. |

The exact tools and resource types can change as the extension evolves. Use the
Toolkit view to see the features in your installed version.

## Work with models

Foundry Toolkit provides an end-to-end model development workflow:

- Use the **Model Catalog** to discover models from Foundry and external
  providers, or use local models through ONNX, Ollama, and Foundry Local.
- Compare models and test prompts, parameters, images, and attachments in the
  **Model Playground**.
- Convert, quantize, optimize, and evaluate supported models for local Windows
  deployment.
- Fine-tune supported models locally with a GPU or remotely with Azure
  Container Apps.
- Profile CPU, GPU, and NPU usage for supported Windows machine learning
  workloads.

## Build and operate agents

Foundry Toolkit supports prompt agents and code-based hosted agents:

- Use **Agent Builder** to configure instructions, models, variables, structured
  outputs, and tools without creating an agent code project.
- Use the **Tool Catalog** to discover Foundry tools, Model Context Protocol
  (MCP) servers, and toolboxes, and then add them to agents.
- Scaffold a hosted agent project when you need custom code, frameworks, or
  orchestration logic.
- Use **Agent Inspector** to debug local agents, inspect streaming responses and
  tool calls, and visualize workflow execution.
- Deploy hosted agents to Foundry Agent Service from source code or a container
  image.
- Test deployed agents in the **Hosted Agent Playground**, inspect logs and
  traces, and manage versions.
- Evaluate models, prompts, and agents with datasets, built-in evaluators, or
  custom criteria.

Some Toolkit experiences are available in preview. Review the
[Foundry Toolkit changelog](https://microsoft.github.io/foundry-toolkit/) for
release details.

## Manage Foundry resources

Sign in to Azure and set a Foundry project to manage cloud resources from
Visual Studio Code. You can:

- Browse Foundry projects and the resources available to your account.
- Discover and deploy models from the Foundry model catalog.
- View model endpoints and authentication information.
- Create, deploy, test, and version prompt agents, workflows, and hosted agents.
- Browse tools and knowledge sources used by your agents.
- Open evaluations, conversations, logs, and traces during development.

For broader resource administration, use the
[Foundry portal](https://ai.azure.com/). To automate a workflow in application
code, use the [Microsoft Foundry SDKs](sdk-overview.md).

## Related content

- [Install Foundry Toolkit for Visual Studio Code](install-foundry-toolkit-visual-studio-code.md)
- [Set up a Foundry project in Visual Studio Code](set-up-foundry-project-visual-studio-code.md)
- [Report a Foundry Toolkit issue](https://aka.ms/AIToolkit/feedback)
- [Choose how to build with Microsoft Foundry](../../concepts/choose-build-approach.md)
