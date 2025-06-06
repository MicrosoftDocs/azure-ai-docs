---
title: Use a screen reader with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: This quickstart guides you in how to get oriented and navigate Azure AI Foundry with a screen reader.
author: sdgilley
ms.author: sgilley
manager: scottpolly
ms.reviewer: ailsaleen
ms.date: 05/02/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - ignite-2023
  - build-2024
  - build-aifnd
  - build-2025
---

# Use a screen reader with Azure AI Foundry

This article is for people who use screen readers such as [Microsoft's Narrator](https://support.microsoft.com/windows/complete-guide-to-narrator-e4397a0d-ef4f-b386-d8ae-c172f109bdb1#WindowsVersion=Windows_11), JAWS, NVDA, or Apple's Voiceover. In this quickstart, you're introduced to the basic structure of Azure AI Foundry and discover how to navigate around efficiently. 

## Getting oriented in Azure AI Foundry portal 

Most [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) pages are composed of the following landmark structure: 

- Banner (contains Azure AI Foundry app title, settings, and profile information)
    - Might sometimes contain a breadcrumb navigation element 
- Navigation - There are three different states:
    - Outside a project - there's no left navigation until you are in a project. The page is divided into sections.  Once you have projects, the top section is a list of recent projects.
    - In a project - the left navigation is the same for all parts of a project, until you move to the **Management center**.
    - The left navigation in the Management center has two sections.  In a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]. the sections are for the **resource** the project is in, then a section for the **project** itself.  In a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)], the sections are for the **hub** that the project is in, then a section for the **project** itself.

For efficient navigation, it might be helpful to navigate by landmarks to move between these sections on the page.


## Navigation

The navigation is list of links divided into different sections. 

If you haven't yet created or selected a project, you can still explore models listed on the home page.  This takes you to the **Model catalog**.  
* When you ask to use a model, you'll be prompted to create a project.
* Once you select a project: 
    * You can access more capabilities such as Model catalog, Playgrounds, and AI Services. 
    * You can also use the **Recent resource picker** button within the navigation breadcrumbs to change to a different project or resource at any time.

### Customize the navigation

Once you select a project, you can access more capabilities such as Model catalog, Playgrounds, and AI Services. Then there are collapsible sections for **Build and customize** (includes Code, Fine-tuning, Prompt-flow), **Assess and improve** (includes Tracing, Evaluation, and Guardrails & controls) and **My assets** (includes Models + endpoints, Data + indexes, and Web apps). 

The left pane is customizable for each project or resource. 

 * There are collapsible sections for **Build and customize** (includes Code, Fine-tuning, Prompt-flow), **Assess and improve** (includes Tracing, Evaluation, and Safety + security) and **My assets** (includes Models + endpoints, Data + indexes, and Web apps). 
* At the bottom of the list is a **...More** link that allows you to pin and unpin items onto the navigation.  
* At the top of the **More** list is a shortcut to **Pin all**.  If all items are already pinned, the option changes to **Unpin all**.
* The **Management center** is always available at the bottom of the left pane.  It cannot be unpinned.

For more information about the navigation, see [What is Azure AI Foundry](../what-is-azure-ai-foundry.md).

## Projects 

To work within the Azure AI Foundry portal, you must first [create a project](../how-to/create-projects.md): 
1. In [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs), select **Azure AI Foundry** from the top breadcrumbs.
1. Press the **Tab** key until you hear *Start building* and select this button. This will create a project for use with an agent.
1. Enter the information requested in the **Create a project** dialog. 
1. When the project is ready, you'll be prompted to select a model to use for your agent.
1. Once the model is deployed, you'll be in the agent playground for that project.

If you already have some projects, you can also create a new project without also creating an agent.

1. In [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs), select **Azure AI Foundry** from the top breadcrumbs.
1. Press the **Tab** key until you hear *+ Create new*.  This path creates a project but does not go on to deploy a model as well.
1. When the project is created, you'll be in the project home page.

## Using the playground 

The playground is where you can interact with models and experiment with different prompts and parameters. Different playgrounds are available depending on which model you would like to interact with. 

Once you select a project, go to the navigation landmark. Press the down arrow until you hear *Playgrounds*.

### Chat playground structure 

In this mode, the playground is composed of the command toolbar and two main sections: one for configuring your system message and other parameters, and the other for chatting to the model. If you added your own data in the playground, the **Add your data** pane also appears. 

### Chat session pane  

The chat session pane is where you can chat to the model and test out your assistant. 
- After you send a message, the model might take some time to respond, especially if the response is long. You hear a screen reader announcement "Message received from the chatbot" when the model finishes composing a response. 

## Distinguishing project types

Azure AI Foundry has two different project types - see [What is Azure AI Foundry?](../what-is-azure-ai-foundry.md#project-types).  The type appears in the  **Type** column in the **All resources** view. In the recent resources picker, the type is in a second line under the project name.

- Listen for either **(AI Foundry)** or **Foundry project** for a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)].  
- Listen for **(Hub)** for a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)].


## Using prompt flow 

Prompt flow is available only in a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)].  

Prompt flow is a tool to create executable flows, linking LLMs, prompts, and Python tools through a visualized graph. You can use this to prototype, experiment, and iterate on your AI applications before deploying. 

Once you select a project, go to the navigation landmark. Press the down arrow until you hear *Prompt flow* and select this link.

The prompt flow UI in Azure AI Foundry portal is composed of the following main sections: the command toolbar, flow (includes list of the flow nodes), files, and graph view. The flow, files, and graph sections each have their own H2 headings that can be used for navigation.

### Flow 

- This is the main working area where you can edit your flow, for example adding a new node, editing the prompt, selecting input data 
- You can also choose to work in code instead of the editor by navigating to the **Raw file mode** toggle button to view the flow in code. 
- Each node has its own H3 heading, which can be used for navigation. 

### Files 

- This section contains the file structure of the flow. Each flow has a folder that contains a flow.dag.yaml file, source code files, and system folders. 
- You can export or import a flow easily for testing, deployment, or collaborative purposes by navigating to the **Add** and **Zip and download all files** buttons.

### Graph view 

- The graph is a visual representation of the flow. This view isn't editable or interactive. 
- You hear the following alt text to describe the graph: "Graph view of [flow name] – for visualization only." We don't currently provide a full screen reader description for this graphical chart. To get all equivalent information, you can read and edit the flow by navigating to Flow, or by toggling on the Raw file view.  

 
## Evaluations  

Evaluation is a tool to help you evaluate the performance of your generative AI application. You can use this to prototype, experiment, and iterate on your applications before deploying.

### Creating an evaluation 

To review evaluation metrics, you must first create an evaluation. 

1. Once you select a project, go to the navigation landmark. Press the down arrow until you hear *Evaluation* and select this link.
1. Press the Tab key until you hear *new evaluation* and select this button. 
1. Enter the information requested in the **Create a new evaluation** dialog. Once complete, your focus is returned to the evaluations list. 

### Viewing evaluations 

Once you create an evaluation, you can access it from the list of evaluations. 

Evaluation runs are listed as links within the Evaluations grid. Selecting a link takes you to a dashboard view with information about your specific evaluation run. 

You might prefer to export the data from your evaluation run so that you can view it in an application of your choosing. To do this, select your evaluation run link, then navigate to the **Export result** button and select it. 

There's also a dashboard view provided to allow you to compare evaluation runs. From the main Evaluations list page, navigate to the **Switch to dashboard view** button. 

 
## Technical support for customers with disabilities 

Microsoft wants to provide the best possible experience for all our customers. If you have a disability or questions related to accessibility, contact the Microsoft Disability Answer Desk for technical assistance. The Disability Answer Desk support team is trained in using many popular assistive technologies. They can offer assistance in English, Spanish, French, and American Sign Language. Go to the Microsoft Disability Answer Desk site to find out the contact details for your region. 

If you're a government, commercial, or enterprise customer, contact the enterprise Disability Answer Desk. 

## Related content

* Learn how you can build generative AI applications in the [Azure AI Foundry](../what-is-azure-ai-foundry.md).
* [Build a custom knowledge retrieval (RAG) app with the Azure AI Foundry SDK](copilot-sdk-create-resources.md)
* Get answers to frequently asked questions in the [Azure AI FAQ article](../faq.yml).
