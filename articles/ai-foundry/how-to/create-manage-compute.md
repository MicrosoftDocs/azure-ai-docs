---
title: Create and manage compute instances
titleSuffix: Microsoft Foundry
description: Learn how to create and manage compute instances in Foundry portal to use prompt flow, create indexes, and access Visual Studio Code.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - hub-only
  - dev-focus
ms.topic: how-to
ms.date: 12/23/2025
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
---

# Create and manage compute instances

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

In this article, you learn how to create and manage a compute instance in Foundry portal. A compute instance is required to use prompt flow, create indexes, or access Visual Studio Code in Foundry portal for hub-based projects.

> [!IMPORTANT]
> Compute instances get the latest VM images when you provision them. Microsoft releases new VM images monthly. Once you deploy a compute instance, it doesn't get updates. You can query an instance's operating system version. 
> To keep current with the latest software updates and security patches, you can: Recreate a compute instance to get the latest OS image (recommended) or regularly update OS and Python packages on the compute instance to get the latest security patches.

## Prerequisites

[!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]


## Create a compute instance

To create a compute instance in Foundry portal:

1. [!INCLUDE [classic-sign-in](../includes/classic-sign-in.md)]
1. Select your project. If you don't have a project already, first create one.
1. Select **Management center** in the left pane. You might have to scroll to find it.
1. Under the **Hub** heading, select **Computes**. 
1. Select **New** to create a new compute instance.

    :::image type="content" source="../media/compute/compute-create.png" alt-text="Screenshot of the option to create a new compute instance from the manage page." lightbox="../media/compute/compute-create.png":::

1. Enter a custom name for your compute.

1. Select your virtual machine type and size and then select **Next**. 

    - Virtual machine type: Choose CPU or GPU. The type can't be changed after creation.
    - Virtual machine size: Supported virtual machine sizes might be restricted in your region. Check the [availability list](https://azure.microsoft.com/global-infrastructure/services/?products=virtual-machines)
    
    For more information on configuration details such as CPU and RAM, see [Azure Machine Learning pricing](https://azure.microsoft.com/pricing/details/machine-learning/) and [virtual machine sizes](/azure/virtual-machines/sizes).

1. On the **Scheduling** page under **Auto shut down**, note that idle shutdown is enabled by default.

    > [!IMPORTANT]
    > The compute can't be idle if you have [prompt flow compute sessions](./create-manage-compute-session.md) in **Running** status on the compute. Delete any active compute sessions before configuring idle shutdown.

    You can automatically shut down compute after the instance has been idle for a set amount of time. If you disable auto shutdown, costs continue to accrue during periods of inactivity. For more information, see [Configure idle shutdown](#configure-idle-shutdown).

    :::image type="content" source="../media/compute/compute-scheduling.png" alt-text="Screenshot of the option to enable idle shutdown and create a schedule." lightbox="../media/compute/compute-scheduling.png"::: 

1. You can update the schedule days and times to meet your needs. You can add additional schedules. For example, create a schedule to start at 9 AM and stop at 6 PM from Monday-Thursday, and a second schedule to start at 9 AM and stop at 4 PM for Friday. You can create a total of four schedules per compute instance.

    :::image type="content" source="../media/compute/compute-schedule-add.png" alt-text="Screenshot of the available new schedule options." lightbox="../media/compute/compute-schedule-add.png":::

1. On the **Security** page, optionally configure security settings such as SSH, virtual network, root access, and managed identity for your compute instance. Use this section to:
    - **Assign to another user**: Create a compute instance on behalf of another user. A compute instance can't be shared. It can only be used by a single assigned user. By default, it will be assigned to the creator and you can change this to a different user.
    - **Assign a managed identity**: Attach system assigned or user assigned managed identities to grant access to resources. The name of the created system managed identity will be in the format `/workspace-name/computes/compute-instance-name` in your Microsoft Entra ID.
    - **Enable SSH access**: Enter credentials for an administrator user account that will be created on each compute node. These can be used to SSH to the compute nodes.

1. On the **Tags** page you can add additional information to categorize the resources you create. Then select **Review + Create** or **Next** to review your settings.

    :::image type="content" source="../media/compute/compute-review-create.png" alt-text="Screenshot of the option to review before creating a new compute instance." lightbox="../media/compute/compute-review-create.png":::

1. After reviewing the settings, select **Create** to create the compute instance.

## Configure idle shutdown

To avoid getting charged for a compute instance that is switched on but inactive, configure when to shut down your compute instance due to inactivity.

The setting can be configured during compute instance creation or modified for existing compute instances.

For a new compute instance, configure idle shutdown during compute instance creation. For more information, see [Create a compute instance](#create-a-compute-instance) earlier in this article.

To configure idle shutdown for an existing compute instance follow these steps:

1. From the left menu, select **Management center**.
1. Under the **Hub** heading, select **Computes**. 
1. In the list, select the compute instance you want to update.
1. Select **Schedule and idle shutdown**.

    :::image type="content" source="../media/compute/compute-schedule-update.png" alt-text="Screenshot of the option to change the idle shutdown schedule for a compute instance." lightbox="../media/compute/compute-schedule-update.png":::

    > [!IMPORTANT]
    > The compute won't be idle if you have a [prompt flow compute session](./create-manage-compute-session.md) in **Running** status on the compute. You need to delete any active compute sessions to make the compute instance eligible for idle shutdown. 

1. Update or add to the schedule. You can have a total of four schedules per compute instance. Then select **Update** to save your changes.

## Start or stop a compute instance

You can start or stop a compute instance from the Foundry portal.

1. From the left menu, select **Management center**.
1. Under the **Hub** heading, select **Computes**.
1. In the list, select the compute instance you want to start or stop.
1. Select **Stop** to stop the compute instance. Select **Start** to start the compute instance. Only stopped compute instances can be started and only started compute instances can be stopped.

    :::image type="content" source="../media/compute/compute-start-stop.png" alt-text="Screenshot of the option to start or stop a compute instance." lightbox="../media/compute/compute-start-stop.png":::

## Next steps

- [Create and manage prompt flow compute session](./create-manage-compute-session.md)
- [Vulnerability management](../concepts/vulnerability-management.md)
