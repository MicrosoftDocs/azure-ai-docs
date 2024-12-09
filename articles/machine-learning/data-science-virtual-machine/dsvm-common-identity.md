---
title: Set up a common identity
titleSuffix: Azure Data Science Virtual Machine 
description: Learn how to create common user accounts that can be used across multiple Data Science Virtual Machines. You can use Microsoft Entra ID or an on-premises Active Directory to authenticate users to the Data Science Virtual Machine.
keywords: deep learning, AI, data science tools, data science virtual machine, geospatial analytics, team data science process
services: machine-learning
ms.service: azure-data-science-virtual-machines
author: fbsolo-ms1
ms.author: franksolomon
ms.topic: conceptual
ms.reviewer: vijetaj
ms.date: 10/28/2024
---

# Set up a common identity on a Data Science Virtual Machine

On a Microsoft Azure Virtual Machine (VM), or a Data Science Virtual Machine (DSVM), you create local user accounts while provisioning the VM. Users then authenticate to the VM with credentials for those user accounts. If you have multiple VMs and your users need to access them, credential management can become difficult. To solve the problem, you can deploy common user accounts and manage those accounts through a standards-based identity provider. You can then use a single set of credentials to access multiple resources on Azure, including multiple DSVMs.

Active Directory is a popular identity provider. Azure supports it both as a cloud service and as an on-premises directory. You can use Microsoft Entra ID or on-premises Active Directory to authenticate users on a standalone DSVM, or a cluster of DSVMs, in an Azure virtual machine scale set. To do this, you join the DSVM instances to an Active Directory domain.

If you already have Active Directory, you can use it as your common identity provider. If you don't have Active Directory, you can run a managed Active Directory instance on Azure through [Microsoft Entra Domain Services](/azure/active-directory-domain-services/).

The [Microsoft Entra ID](/azure/active-directory/) documentation provides detailed [management instructions](/azure/active-directory/hybrid/whatis-hybrid-identity), including guidance about how to connect Microsoft Entra ID to your on-premises directory, if you have one.

This article describes how to set up a fully managed Active Directory domain service on Azure, using Microsoft Entra Domain Services. You can then join your DSVMs to the managed Active Directory domain. This approach allows users to access a pool of DSVMs (and other Azure resources) through a common user account and credentials.

## Set up a fully managed Active Directory domain on Azure

Microsoft Entra Domain Services makes it simple to manage your identities. It provides a fully managed service on Azure. On this Active Directory domain, you manage users and groups. To set up an Azure-hosted Active Directory domain and user accounts in your directory, follow these steps:

1. In the Azure portal, add the user to Active Directory:

   1. Sign in to the [Azure portal](https://portal.azure.com) as a Privileged Role Administrator
    
   1. Browse to **Microsoft Entra ID** > **Users** > **All users**
    
   1. Select **New user**
   
        The **User** pane opens, as shown in this screenshot:

        :::image type="content" source="./media/dsvm-common-identity/add-user.png" alt-text="Screenshot showing the add user pane." lightbox="./media/dsvm-common-identity/add-user.png":::
    
   1. Enter information about the user, such as **Name** and **User name**. The domain name portion of the user name must be either the initial default domain name "[domain name].onmicrosoft.com" or a verified, nonfederated [custom domain name](/azure/active-directory/fundamentals/add-custom-domain) such as "contoso.com."
    
   1. Copy or otherwise note the generated user password. You must provide this password to the user after this process is complete
    
   1. Optionally, you can open and fill out the information in **Profile**, **Groups**, or **Directory role** for the user
    
   1. Under **User**, select **Create**
    
   1. Securely distribute the generated password to the new user so that the user can sign in

1. Create a Microsoft Entra Domain Services instance. In the [Enable Microsoft Entra Domain Services using the Azure portal](/azure/active-directory-domain-services/tutorial-create-instance) resource, visit the **Create an instance and configure basic settings** section for more information. You need to update the existing user passwords in Active Directory to sync the password in Microsoft Entra Domain Services. You must also add DNS to Microsoft Entra Domain Services, as described under **Complete the fields in the Basics window of the Azure portal to create a Microsoft Entra Domain Services instance** in that section.

1. In the **Create and configure the virtual network** section of the preceding step, create a separate DSVM subnet in the virtual network you created
1. Create one or more DSVM instances in the DSVM subnet
1. Follow the [instructions](/azure/active-directory-domain-services/join-ubuntu-linux-vm) to add the DSVM to Active Directory
1. Mount an Azure Files share to host your home or notebook directory, so that your workspace can be mounted on any machine. If you need tight file-level permissions, you need Network File System [NFS] running on one or more VMs

   1. [Create an Azure Files share](/azure/storage/files/storage-how-to-create-file-share).
    
   2.  Mount this share on the Linux DSVM. When you select **Connect** for the Azure Files share in your storage account in the Azure portal, the command to run in the bash shell on the Linux DSVM appears. The command looks like this:
   
   ```
   sudo mount -t cifs //[STORAGEACCT].file.core.windows.net/workspace [Your mount point] -o vers=3.0,username=[STORAGEACCT],password=[Access Key or SAS],dir_mode=0777,file_mode=0777,sec=ntlmssp
   ```
1. For example, assume that you mounted your Azure Files share in the **/data/workspace** directory. Now, create directories for each of your users in the share:
    - /data/workspace/user1
    - /data/workspace/user2
    - etc.

   Create a `notebooks` directory in the workspace of each user
1. Create symbolic links for `notebooks` in `$HOME/userx/notebooks/remote`

You now have the users in your Active Directory instance, which is hosted in Azure. With Active Directory credentials, users can sign in to any DSVM (SSH or JupyterHub) that is joined to Microsoft Entra Domain Services. Because an Azure Files share hosts the user workspace, users can access their notebooks and other work from any DSVM when they use JupyterHub.

For autoscaling, you can use a virtual machine scale set to create a pool of VMs that are all joined to the domain in this fashion, and with the shared disk mounted. Users can sign in to any available machine in the virtual machine scale set, and can access the shared disk where their notebooks are saved.

## Next steps

* [Securely store credentials to access cloud resources](dsvm-secure-access-keys.md)