---
title: "Use a screen reader with Microsoft Foundry"
description: "This quickstart guides you in how to get oriented and navigate Microsoft Foundry with a screen reader."
author: sdgilley
ms.author: sgilley
ms.reviewer: ailsaleen
ms.date: 12/09/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - build-aifnd
  - build-2025
  - doc-kit-assisted
---

# Use a screen reader with Microsoft Foundry
This article is for people who use screen readers such as [Microsoft's Narrator](https://support.microsoft.com/windows/complete-guide-to-narrator-e4397a0d-ef4f-b386-d8ae-c172f109bdb1#WindowsVersion=Windows_11), JAWS, NVDA, or Apple's VoiceOver. In this article, you learn the basic structure of Microsoft Foundry and how to navigate efficiently.

## Prerequisites

[!INCLUDE [screen-reader-prereqs](../includes/screen-reader-prereqs.md)]

## Get oriented in Foundry portal

Most [!INCLUDE [foundry-link](../includes/foundry-link.md)] (new) pages have the following landmark structure: 

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

For efficient navigation, you can use landmarks to move between these sections on the page.

## Switch between portal experiences

You can switch between the classic and new Foundry portal experiences using the **New Foundry** toggle in the top banner.

To switch back to the classic experience:
1. In the top banner, press <kbd>Tab</kbd> until focus reaches the **New Foundry** toggle.
1. Select the toggle to switch to the classic experience.
1. The page reloads with the classic portal interface.

> [!NOTE]
> The toggle preserves your current context, such as the project you're working in, when switching between experiences.

## Projects

You enter the portal with a selected project. The navigation sections **Home**, **Discover**, and **Build** display content for your selected project. The **Operate** section is different - it shows information for all your projects.

To create or switch projects:
1. In [!INCLUDE [foundry-link](../includes/foundry-link.md)], on the top banner, select **Foundry**.
1. Press <kbd>Tab</kbd> until you hear a project name.
1. Use the down-arrow to scroll through the list of recent projects.
1. At the end of the list of recent projects, you find options to **View all projects**, **Create new project**, and **View legacy resources**.
1. If you don't hear a project name, return focus to the top banner and select **Foundry** again to reopen the project list.

## Navigation

In the new Foundry experience, use landmarks and headings to move between these areas:

- Top banner navigation: **Home**, **Discover**, **Build**, **Operate**, and **Docs**.
- Left pane navigation for the selected top-level area.
- Page tabs, when available, as a third navigation level.

To move quickly to feature areas:

1. Use landmark navigation to move to the left pane.
1. Press the down-arrow to move through navigation items.
1. Select a section such as **Build** to access model and tool workflows.
1. If the left pane isn't available, move focus back to the top banner and reselect the project.

## Using playgrounds

After you select a project:

1. In the top banner navigation, select **Build**.
1. Move to the left navigation landmark.
1. Select **Model** or **Agent**.
1. Select the model or agent you want to interact with.
1. Use heading navigation to move between configuration and interaction areas.
1. If **Model** or **Agent** isn't announced in the left pane, confirm that you're in a project and still in the **Build** section.

When you send a prompt in a chat-style experience, your screen reader should announce new content when the model response is received.
If you don't hear a response announcement, move to the chat history region by heading navigation and read the most recent message.

## Evaluations

To create an evaluation in the new Foundry experience:

1. Move to the top navigation landmark and select **Build**.
1. Select **Evaluation**.
1. Select **Create** and complete the dialog fields.
1. Return to the evaluations list and open a run to review details.

To export results:

1. Open an evaluation run.
1. Navigate to **Raw JSON** and select it.
1. Select **Copy JSON** to copy.
1. Select **Close** to close the dialog.

## Verify your navigation setup

After you complete the steps in this article, verify the following outcomes:

- You can move between major page landmarks, such as banner, navigation, and main content.
- You can identify your current portal experience (new or classic) and switch experiences if needed.
- You can return to your previous location after switching views or opening dialogs.
- You can locate your selected project and move to key areas such as **Home**, **Discover**, **Build**, **Operate**, and **Docs**.

## Troubleshoot screen reader navigation

[!INCLUDE [screen-reader-troubleshoot](../includes/screen-reader-troubleshoot.md)]

## Technical support for customers with disabilities

[!INCLUDE [screen-reader-tech-support](../includes/screen-reader-tech-support.md)]

## Related content

* Learn how to build generative AI applications in the [Foundry](../what-is-foundry.md).
* Get answers to frequently asked questions in the [Azure AI FAQ article](../../foundry-classic/faq.yml).
