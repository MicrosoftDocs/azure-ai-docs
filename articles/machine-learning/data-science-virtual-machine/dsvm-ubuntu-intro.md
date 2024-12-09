---
title: 'Quickstart: Create an Ubuntu Data Science Virtual Machine'
titleSuffix: Azure Data Science Virtual Machine
description: Configure and create a Data Science Virtual Machine for Linux (Ubuntu) to do analytics and machine learning.
ms.service: azure-data-science-virtual-machines
author: fbsolo-ms1 
ms.author: franksolomon 
ms.topic: quickstart
ms.reviewer: jeffshep
ms.date: 10/14/2024
ms.custom: mode-other, linux-related-content
#Customer intent: As a data scientist, I want to learn how to provision the Linux DSVM so that I can move my existing workflow to the cloud.
---

# Quickstart: Set up the Data Science Virtual Machine for Linux (Ubuntu)

Get up and running with the Ubuntu 20.04 Data Science Virtual Machine (DSVM) and the Azure DSVM for PyTorch.

## Prerequisites

You need an Azure subscription to create either an Ubuntu 20.04 Data Science Virtual Machine or an Azure DSVM for PyTorch. [Try Azure for free](https://azure.com/free).

Azure free accounts don't support GPU-enabled virtual machine (VM) SKUs.

## Create your Data Science Virtual Machine for Linux

To create an instance of either the Ubuntu 20.04 DSVM or the Azure DSVM for PyTorch:

1. Go to the [Azure portal](https://portal.azure.com). You might get a prompt to sign in to your Azure account if you didn't yet sign in.
1. Find the VM listing by entering **data science virtual machine**. Then select **Data Science Virtual Machine- Ubuntu 20.04** or **Azure DSVM for PyTorch**.

1. Select **Create**.

1. On the **Create a virtual machine** pane, fill in the **Basics** tab:

      * **Subscription**: If you have more than one subscription, select the one on which the machine is created and billed. You must have resource creation privileges for this subscription.
      * **Resource group**: Create a new group or use an existing one.
      * **Virtual machine name**: Enter the name of the VM. This name is used in your Azure portal.
      * **Region**: Select the datacenter that's most appropriate. For fastest network access, the datacenter that hosts most of your data or is located closest to your physical location is the best choice. For more information, visit [Azure regions](https://azure.microsoft.com/global-infrastructure/regions/).
      * **Image**: Don't change the default value.
      * **Size**: This option should autopopulate with an appropriate size for general workloads. For more information, visit [Linux VM sizes in Azure](/azure/virtual-machines/sizes).
      * **Authentication type**: For quicker setup, select **Password**.

         > [!NOTE]
         > If you plan to use JupyterHub, be sure to select **Password** because JupyterHub is *not* configured to use Secure Shell (SSH) Protocol public keys.

      * **Username**: Enter the administrator username. You use this username to sign in to your VM. It doesn't need to match your Azure username. Don't use capital letters.

         > [!IMPORTANT]
         > If you use capital letters in your username, JupyterHub won't work, and you'll encounter a 500 internal server error.

      * **Password**: Enter the password you plan to use to sign in to your VM.

1. Select **Review + create**.
1. On the **Review + create** pane:
      * Verify that all the information you entered is correct.
      * Select **Create**.

    The provisioning process takes about 5 minutes. You can view the status of your VM in the Azure portal.

## Access the Ubuntu Data Science Virtual Machine

You can access the Ubuntu DSVM in one of four ways:

  * SSH for terminal sessions
  * xrdp for graphical sessions
  * X2Go for graphical sessions
  * JupyterHub and JupyterLab for Jupyter notebooks

### SSH

If you configured your VM with SSH authentication, you can sign in with the account credentials that you created in the **Basics** section of step 4 for the text shell interface. For more information, visit [Learn more about connecting to a Linux VM](/azure/virtual-machines/linux-vm-connect).

### xrdp
The standard tool for accessing Linux graphical sessions is xrdp. While the distribution doesn't include this tool by default, [these instructions](/azure/virtual-machines/linux/use-remote-desktop) explain how to install it.

### X2Go
> [!NOTE]
> In testing, the X2Go client performed better than X11 forwarding. We recommend use of the X2Go client for a graphical desktop interface.

The Linux VM is already provisioned with X2Go Server and is ready to accept client connections. To connect to the Linux VM graphical desktop, complete the following procedures on your client:

1. Download and install the X2Go client for your client platform from [X2Go](https://wiki.x2go.org/doku.php/doc:installation:x2goclient).
1. Note the public IP address of the VM. In the Azure portal, open the VM you created to find this information.

   :::image type="content" source="./media/dsvm-ubuntu-intro/ubuntu-ip-address.png" alt-text="Screenshot that shows the public IP address of the VM." lightbox= "./media/dsvm-ubuntu-intro/ubuntu-ip-address.png":::

1. Run the X2Go client. If the **New Session** pane doesn't automatically open, select **Session** > **New Session**.

1. On the resulting configuration pane, enter these configuration parameters:
   * **Session**:
     * **Host**: Enter the IP address of your VM, which you noted earlier.
     * **Login**: Enter the username on the Linux VM.
     * **SSH port**: Leave it at the default value **22**.
     * **Session type**: Change the value to **XFCE**. Currently, the Linux VM supports only the XFCE desktop.
   * **Media**: You can turn off sound support and client printing if you don't need to use them.
   * **Shared folders**: Use this tab to add the client machine directory that you want to mount on the VM.

   :::image type="content" source="./media/dsvm-ubuntu-intro/x2go-ubuntu.png" alt-text="Screenshot that shows preferences for a new X2Go session." lightbox= "./media/dsvm-ubuntu-intro/x2go-ubuntu.png":::
1. Select **OK**.
1. To bring up the sign-in pane for your VM, select the box in the right pane of the X2Go pane.
1. Enter the password for your VM.
1. Select **OK**.
1. You might need to give X2Go permission to bypass your firewall to finish the connection process.
1. You should now see the graphical interface for your Ubuntu DSVM.

### JupyterHub and JupyterLab

The Ubuntu DSVM runs [JupyterHub](https://github.com/jupyterhub/jupyterhub), which is a multiuser Jupyter server. To connect, follow these steps:

   1. Note the public IP address of your VM. To find this value, search for and select your VM in the Azure portal, as shown in this screenshot.

      :::image type="content" source="./media/dsvm-ubuntu-intro/ubuntu-ip-address.png" alt-text="Screenshot that shows the public IP address of your VM." lightbox= "./media/dsvm-ubuntu-intro/ubuntu-ip-address.png":::

   1. From your local machine, open a web browser and go to `https://your-vm-ip:8000`. Replace **your-vm-ip** with the IP address you noted earlier.
   1. Your browser will probably prevent you from opening the pane directly. It might tell you that there's a certificate error. The DSVM provides security with a self-signed certificate. Most browsers will allow you to select through after this warning. Many browsers will continue to provide some kind of visual warning about the certificate throughout your web session.

      If you see the `ERR_EMPTY_RESPONSE` error message in your browser, be sure you access the machine by explicit use of the *HTTPS* protocol. *HTTP* or just the web address don't work for this step. If you enter the web address without `https://` in the address line, most browsers default to `http` and the error will appear.

   1. Enter the username and password that you used to create the VM and sign in, as shown in this screenshot.

      :::image type="content" source="./media/dsvm-ubuntu-intro/jupyter-login.png" alt-text="Screenshot that shows the JupyterHub sign-in pane." lightbox= "./media/dsvm-ubuntu-intro/jupyter-login.png":::

      If you receive a **500** error at this stage, you probably used capital letters in your username. This issue is a known interaction between JupyterHub and the PAM authenticator it uses.
   
      If you receive a **Can't reach this page** error, it's likely that your network security group (NSG) permissions need adjustment. In the Azure portal, find the NSG resource within your resource group. To access JupyterHub from the public internet, you must have port 8000 open. (The image shows that this VM is configured for just-in-time access, which we highly recommend. For more information, visit [Secure your management ports with just-in time access](/azure/security-center/security-center-just-in-time).)
      >
      > :::image type="content" source="./media/dsvm-ubuntu-intro/nsg-permissions.png" alt-text="Screenshot that shows NSG configuration values." lightbox= "./media/dsvm-ubuntu-intro/nsg-permissions.png":::

   1. Browse the available sample notebooks.

JupyterLab, the next generation of Jupyter notebooks and JupyterHub, is also available. To access it, sign in to JupyterHub. Then browse to the URL `https://your-vm-ip:8000/user/your-username/lab`. Replace **your-username** with the username you chose when you configured the VM. Again, potential certificate errors might initially block you from accessing the site.

To set JupyterLab as the default notebook server, add this line to `/etc/jupyterhub/jupyterhub_config.py`:

```python
c.Spawner.default_url = '/lab'
```

## Next steps

* Visit the [Data science on the Data Science Virtual Machine for Linux](linux-dsvm-walkthrough.md) walkthrough to learn how to do several common data science tasks with the Linux DSVM provisioned here.
* Try out the tools this article describes to explore the various data science tools on the DSVM. You can also run `dsvm-more-info` on the shell within the VM for a basic introduction and pointers to more information about the tools installed on the VM.
* Learn how to systematically build analytical solutions with the [Team Data Science Process](/azure/architecture/data-science-process/overview).
* Visit the appropriate [reference documentation](./reference-ubuntu-vm.md) for this VM.
