---
title: Use a screen reader with Microsoft Foundry
titleSuffix: Microsoft Foundry
description: This quickstart guides you in how to get oriented and navigate Microsoft Foundry with a screen reader.
author: sdgilley
ms.author: sgilley
ms.reviewer: ailsaleen
ms.date: 12/09/2025
ms.service: azure-ai-foundry
ms.topic: how-to
monikerRange: 'foundry-classic || foundry'
ms.custom:
  - ignite-2023
  - build-2024
  - build-aifnd
  - build-2025
---

# Use a screen reader with Microsoft Foundry

[!INCLUDE [version-banner](../includes/version-banner.md)]

This article is for people who use screen readers such as [Microsoft's Narrator](https://support.microsoft.com/windows/complete-guide-to-narrator-e4397a0d-ef4f-b386-d8ae-c172f109bdb1#WindowsVersion=Windows_11), JAWS, NVDA, or Apple's VoiceOver. In this quickstart, you learn about the basic structure of Microsoft Foundry and how to navigate around efficiently. 

## Get oriented in Foundry portal 



::: moniker range="foundry-classic"

Most [!INCLUDE [classic-link](../includes/classic-link.md)] (classic) pages have the following landmark structure: 

- Banner (has Foundry app title, settings, and profile information)
    - Sometimes has a breadcrumb navigation element 
- Navigation - Three different states:
    - Outside a project - there's no left navigation until you're in a project. The page is divided into sections. Once you have projects, the top section is a list of recent projects.
    - In a project - the left navigation is the same for all parts of a project until you move to the **Management center**.
    - The Management center left navigation has two sections. In a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)], the sections are for the **resource** the project is in, then a section for the **project** itself. In a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)], the sections are for the **hub** the project is in, then a section for the **project** itself.
::: moniker-end

::: moniker range="foundry"

Most [!INCLUDE [foundry-link](../default/includes/foundry-link.md)] (new) pages have the following landmark structure: 

- Banner has 
    - Foundry application title
    - Project selector
    - Search
    - Ask AI toggle
    - Main section navigation: Home, Discover, Build, Operate, Docs
    - Settings
    - Profile information
- Left pane has navigation for the section selected in the main navigation. The Home page has no left pane navigation. 
- Many pages also have tabs as a third level of navigation.

::: moniker-end

For efficient navigation, you can use landmarks to move between these sections on the page.

## Switch between portal experiences

You can switch between the classic and new Foundry portal experiences using the **New Foundry** toggle in the top banner.

::: moniker range="foundry-classic"

To switch to the new Foundry experience:
1. In the top banner, press <kbd>Tab</kbd> until you hear "New Foundry toggle button, not pressed".
1. Select the toggle to switch to the new Foundry experience.
1. The page reloads with the new portal interface.

> [!NOTE]
> The toggle attempts to preserve your current context, such as the project you're working in, when switching between experiences. If the resource or project you are editing is not available in the new experience, you'll be prompted to first select an available project.

::: moniker-end

::: moniker range="foundry"

To switch back to the classic experience:
1. In the top banner, press <kbd>Tab</kbd> until you hear "New Foundry toggle button, pressed".
1. Select the toggle to switch to the classic experience.
1. The page reloads with the classic portal interface.

> [!NOTE]
> The toggle preserves your current context, such as the project you're working in, when switching between experiences.

::: moniker-end



:::moniker range="foundry"
## Projects 

You enter the portal with a selected project. The navigation sections **Home**, **Discover**, and **Build** display content for your selected project. The **Operate** section is different - it shows information for all your projects.

To create or switch projects:
1. In [!INCLUDE [foundry-link](../default/includes/foundry-link.md)], on the top banner, select **Foundry**.
1. Press <kbd>Tab</kbd> until you hear a project name.
1. Use the down-arrow to scroll through the list of recent projects.
1. At the end of the list of recent projects, you find options to **View all projects**, **Create new project**, and **View legacy resources**.
::: moniker-end

:::moniker range="foundry-classic"

## Navigation

The navigation is a list of links divided into different sections. 

If you don't have a project, you can still explore models listed on the home page. This action takes you to the **Model catalog**. 
* When you ask to use a model, the portal prompts you to create a project.
* Once you select a project: 
    * You can access more capabilities such as Model catalog, Playgrounds, and Foundry Tools. 
    * You can also use the **Recent resource picker** button within the navigation breadcrumbs to change to a different project or resource at any time.

### Customize the navigation

After you select a project, you can access more capabilities such as Model catalog, Playgrounds, and Foundry Tools.

You can customize the left pane for each project or resource. 

* Collapsible sections contain different content depending on what resource is open. 
* At the bottom of the list is a **...More** link that lets you pin and unpin items onto the navigation. 
* At the top of the **More** list is a shortcut to **Pin all**. If all items are already pinned, the option changes to **Unpin all**.
* The **Management center** is always available at the bottom of the left pane and can't be unpinned.

For more information about the navigation, see [What is Foundry](../what-is-foundry.md).

## Projects 

To work in the Foundry portal, first [create a project](../how-to/create-projects.md): 
1. In [!INCLUDE [classic-link](../includes/classic-link.md)], select **Foundry** from the top breadcrumbs.
1. Press <kbd>Tab</kbd> until you hear *Create an agent*, then select this button. This action creates a project for use with an agent.
1. Enter the information requested in the **Create a project** dialog. 
1. When the project is ready, you're prompted to select a model to use for your agent.
1. Once the model is deployed, you are in the agent playground for that project.

If you already have some projects, you can also create a new project without creating an agent.

1. In [!INCLUDE [classic-link](../includes/classic-link.md)], select **Foundry** from the top breadcrumbs.
1. Press <kbd>Tab</kbd> until you hear *Create new*. This path creates a project but doesn't deploy a model.
1. When the project is created, you are in the project home page.

## Using the playground 

The playground is where you can interact with models and experiment with different prompts and parameters. Different playgrounds are available depending on which model you want to interact with. 

After you select a project, go to the navigation landmark. Press the down arrow until you hear *Playgrounds*.

### Chat playground structure 

In this mode, the playground consists of the command toolbar and two main sections: one section for configuring your system message and other parameters, and another section for chatting with the model. If you add your own data in the playground, the **Add your data** pane also appears. 

### Chat session pane  

The chat session pane is where you can chat with the model and test out your assistant. 
- After you send a message, the model might take some time to respond, especially if the response is long. When the model finishes composing a response, you hear a screen reader announcement "Message received from the chatbot". 

## Distinguishing project types

Foundry has two different project types—see [What is Foundry?](../what-is-foundry.md#types-of-projects). The **Type** column in the **All resources** view shows the project type. In the recent resources picker, the type appears on a second line under the project name.

- Look for either **(Foundry)** or **Foundry project** for a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]. 
- Look for **(Hub)** for a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)].


## Using prompt flow 

Prompt flow is available only in a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]. 

Prompt flow is a tool that creates executable flows by linking LLMs, prompts, and Python tools through a visualized graph. Use prompt flow to prototype, experiment, and iterate on your AI applications before you deploy them. 

After you select a project, go to the navigation landmark. Press the Down arrow until you hear *Prompt flow*, then select this link.

The prompt flow UI in Foundry portal is composed of the following main sections: the command toolbar, flow (includes list of the flow nodes), files, and graph view. The flow, files, and graph sections each have their own H2 headings that you can use for navigation.

### Flow section 

- This section is the main working area where you can edit your flow. For example, you can add a new node, edit the prompt, or select input data. 
- You can also work in code instead of the editor. To view the flow in code, select the **Raw file mode** toggle button. 
- Each node has its own H3 heading, which you can use for navigation. 

### Files section 

- This section contains the file structure of the flow. Each flow has a folder that contains a `flow.dag.yaml` file, source code files, and system folders. 
- You can export or import a flow easily for testing, deployment, or collaborative purposes by navigating to the **Add** and **Zip and download all files** buttons.

### Graph view section 

- The graph is a visual representation of the flow. This view isn't editable or interactive. 
- You hear the following alt text to describe the graph: "Graph view of [flow name]—for visualization only." We don't currently provide a full screen reader description for this graphical chart. To get all equivalent information, you can read and edit the flow by going to the Flow section or by selecting the **Raw file mode** toggle button.  

 
## Evaluations  

Evaluation is a tool that helps you assess the performance of your generative AI application. Use it to prototype, experiment, and iterate on your applications before deploying.

### Create an evaluation 

To review evaluation metrics, first create an evaluation. 

1. After you select a project, go to the navigation landmark. Press the down arrow until you hear *Evaluation* and select this link.
1. Press the Tab key until you hear *new evaluation* and select this button. 
1. Enter the information requested in the **Create a new evaluation** dialog. After you complete this step, your focus returns to the evaluations list.

### View evaluations 

After you create an evaluation, access it from the list of evaluations. 

Evaluation runs are listed as links within the Evaluations grid. Selecting a link takes you to a dashboard view with information about your specific evaluation run. 

To export the data from your evaluation run so you can view it in an application of your choosing, select your evaluation run link, then go to the **Export result** button and select it. 

You can also use a dashboard view to compare evaluation runs. From the main Evaluations list page, go to the **Switch to dashboard view** button. 

::: moniker-end
 
## Technical support for customers with disabilities 

Microsoft wants to provide the best possible experience for all customers. If you have a disability or have questions related to accessibility, contact the Microsoft Disability Answer Desk for technical assistance. The Disability Answer Desk support team is trained in using many popular assistive technologies. They can offer assistance in English, Spanish, French, and American Sign Language. Go to the Microsoft Disability Answer Desk site to find the contact details for your region. 

:::moniker range="foundry-classic"
If you're a government, commercial, or enterprise customer, contact the Enterprise Disability Answer Desk. 
:::moniker-end

## Related content

* Learn how to build generative AI applications in the [Foundry](../what-is-foundry.md).
* Get answers to frequently asked questions in the [Azure AI FAQ article](../faq.yml).
