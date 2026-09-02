---
title: How to manage compute sessions
titleSuffix: Azure Machine Learning
description: Use the session management panel to manage the active notebook and terminal sessions running on a compute instance.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.service: azure-machine-learning
ms.subservice: compute
ms.topic: how-to
ms.date: 08/31/2026
# Customer intent: As a data scientist, I want to manage the notebook and terminal sessions on my compute instance for optimal performance.
---

# Manage notebook and terminal sessions

Notebook and terminal sessions run on your compute instance and keep your current working state. When you reopen a notebook or reconnect to a terminal session, you can resume the previous state, including command history, execution history, and defined variables.

Keeping too many sessions open can slow down the performance of your compute. If your notebook cells feel slower to type in, or terminal commands take longer to run, close the sessions you no longer need.

Use the session management panel in Azure Machine Learning studio to review your active sessions and keep only the ones you need right now. To open the panel, select **Manage active sessions** in the compute toolbar from either a notebook tab or a terminal tab.

> [!NOTE]
> We recommend keeping only the sessions you actively need. A lower session count often improves responsiveness, especially on shared or resource-constrained compute instances.

:::image type="content" source="media/how-to-manage-compute-sessions/compute-session-management-panel.png" alt-text="Screenshot of compute session management panel." lightbox="media/how-to-manage-compute-sessions/compute-session-management-panel.png":::

## Manage active sessions

1. Open the session management panel from the notebook or terminal toolbar.
2. Review the list of active notebook and terminal sessions.
3. Reopen a session if you want to resume its previous state.
4. Shut down any sessions you no longer need.

This workflow helps keep your compute responsive while preserving the sessions you still want to return to later.

## Notebook sessions

In the session management pane, select a notebook name to reopen it and resume its previous state. Notebook sessions remain active after you close the notebook tab in Azure Machine Learning studio, so reopening a notebook restores the previously defined variables and execution state.

This behavior is useful when you want to continue work in the same notebook without restarting the kernel. If you no longer need a notebook session, close it from the session management pane to free resources on your compute.

The following image shows the session count indicator for active notebook sessions.

:::image type="content" source="media/how-to-manage-compute-sessions/notebook-sessions-button.png" alt-text="Screenshot of notebooks sessions button in toolbar." lightbox="media/how-to-manage-compute-sessions/notebook-sessions-button.png":::

## Terminal sessions

In the session management pane, select a terminal link to reopen a terminal tab connected to that previous session. Terminal sessions typically end when you close the terminal tab. If you leave Azure Machine Learning studio without closing a terminal tab, the session might remain active until the session ends or is cleaned up.

To optimize compute performance, shut down any terminal sessions you no longer need by using the session management pane. The following image shows the session count indicator for active terminal sessions.

:::image type="content" source="media/how-to-manage-compute-sessions/terminal-sessions-button.png" alt-text="Screenshot of terminal sessions button in toolbar." lightbox="media/how-to-manage-compute-sessions/terminal-sessions-button.png":::

## Next steps

* [How to create and manage files in your workspace](how-to-manage-files.md)
* [Run Jupyter notebooks in your workspace](how-to-run-jupyter-notebooks.md)
* [Access a compute instance terminal in your workspace](how-to-access-terminal.md)
