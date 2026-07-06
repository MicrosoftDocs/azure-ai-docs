---
title: Interact with your jobs (debug and monitor)
titleSuffix: Azure Machine Learning
description: Debug or monitor your Machine Learning job as it runs on Azure Machine Learning compute with your training application of choice.
services: machine-learning
ms.author: scottpolly
author: s-polly
ms.reviewer: sooryar
ms.service: azure-machine-learning
ms.subservice: automl
ms.topic: how-to

ms.date: 06/29/2026
ms.custom:
  - devplatv2
  - sdkv2
  - cliv2
  - sfi-image-nochange
  - ai-usage:ai-assisted
#Customer intent: I'm a data scientist with ML knowledge in the machine learning space, looking to build ML models using data in Azure Machine Learning with full control of the model training including debugging and monitoring of live jobs.
---

# Debug jobs and monitor training progress

Machine learning model training is an iterative process that requires significant experimentation. By using the Azure Machine Learning interactive job experience, data scientists can use the Azure Machine Learning Python SDK, Azure Machine Learning CLI, or Azure Machine Learning studio to access the container where their job is running. Once users access the job container, they can iterate on training scripts, monitor training progress, and debug the job remotely, just as they typically do on their local machines. You can interact with jobs through different training applications, including JupyterLab, TensorBoard, VS Code, or by connecting to the job container directly via SSH.  

Azure Machine Learning supports interactive training on **Azure Machine Learning Compute Clusters** and **Azure Arc-enabled Kubernetes Cluster**.

## Prerequisites

- Review [getting started with training on Azure Machine Learning](./how-to-train-model.md).
- For more information, see [VS Code](how-to-setup-vs-code.md) to set up the Azure Machine Learning extension.
- Make sure your job environment has the `openssh-server` and `ipykernel ~=6.0` packages installed. All Azure Machine Learning curated training environments have these packages installed by default.
- You can't enable interactive applications on distributed training runs where the distribution type is anything other than PyTorch, TensorFlow, or MPI. Custom distributed training setup (configuring multinode training without using the preceding distribution frameworks) isn't currently supported.
- To use SSH, you need an SSH key pair. Use the `ssh-keygen -f "<filepath>"` command to generate a public and private key pair.
- To attach a debugger to a running job, install `debugpy` in your job environment. See [Attach a debugger to a job](#attach-a-debugger-to-a-job).
   
## Interact with your job container

By specifying interactive applications at job creation, you can connect directly to the container on the compute node where your job is running. Once you have access to the job container, you can test or debug your job in the exact same environment where it runs. You can also use VS Code to attach to the running process and debug as you would locally. 

### Enable during job submission
# [Azure Machine Learning studio](#tab/ui)
1. Create a new job from the left pane in the studio portal.


1. Select **Compute cluster** or **Attached compute** (Kubernetes) as the compute type. Select the compute target, and specify how many nodes you need in `Instance count`. 
  
  :::image type="content" source="./media/interactive-jobs/select-compute.png" alt-text="Screenshot of selecting a compute location for a job.":::

1. Follow the wizard to choose the environment you want to start the job.
  

1. In the **Training script** step, add your training code (and input/output data) and reference it in your command to make sure it's mounted to your job.
  
  :::image type="content" source="./media/interactive-jobs/sleep-command.png" alt-text="Screenshot of reviewing a drafted job and completing the creation.":::

  To specify the amount of time you want to reserve the compute resource, add `sleep <specific time>` at the end of your command. The format follows: 
  * `sleep 1s`
  * `sleep 1m`
  * `sleep 1h`
  * `sleep 1d`

  You can also use the `sleep infinity` command that keeps the job alive indefinitely. 
    
  > [!NOTE]
  > If you use `sleep infinity`, you must manually [cancel the job](./how-to-interactive-jobs.md#end-job) to release the compute resource and stop billing. 

1. In **Compute** settings, expand the option for **Training applications**. Select at least one training application you want to use to interact with the job. If you don't select an application, the debug feature isn't available. 

  :::image type="content" source="./media/interactive-jobs/select-training-apps.png" alt-text="Screenshot of selecting a training application for the user to use for a job.":::

1. Review and create the job.

# [Python SDK](#tab/python)
1. Define the interactive services you want to use for your job. Replace `your compute name` with your own value. If you want to use your own custom environment, see [this tutorial](how-to-manage-environments-v2.md) to create a custom environment. 

   Import the interactive service classes you need from `azure.ai.ml.entities`. The available classes are `JupyterLabJobService`, `VsCodeJobService`, `TensorBoardJobService`, and `SshJobService`.

   ```python
   from azure.ai.ml import command
   from azure.ai.ml.entities import JupyterLabJobService, SshJobService, TensorBoardJobService, VsCodeJobService

   command_job = command(...
       code="./src",  # local path where the code is stored
       command="python main.py", # you can add a command like "sleep 1h" to reserve the compute resource is reserved after the script finishes running
       environment="AzureML-tensorflow-2.12-cuda11@latest",
       compute="<name-of-compute>",
       services={
         "My_jupyterlab": JupyterLabJobService(
           nodes="all" # For distributed jobs, use the `nodes` property to pick which node you want to enable interactive services on. If `nodes` are not selected, by default, interactive applications are only enabled on the head node. Values are "all", or compute node index (for ex. "0", "1" etc.)
         ),
         "My_vscode": VsCodeJobService(
           nodes="all"
         ),
         "My_tensorboard": TensorBoardJobService(
           nodes="all",
           log_dir="output/tblogs"  # relative path of Tensorboard logs (same as in your training script)         
         ),
         "My_ssh": SshJobService(
           ssh_public_keys="<add-public-key>",
           nodes="all"  
         ),
       }
   )
   
   # submit the command
   returned_job = ml_client.jobs.create_or_update(command_job)
   ```

   The `services` section specifies the training applications you want to interact with.  

   To specify the amount of time you want to reserve the compute resource, add `sleep <specific time>` at the end of your command. The format follows: 
   * `sleep 1s`
   * `sleep 1m`
   * `sleep 1h`
   * `sleep 1d`

   You can also use the `sleep infinity` command that keeps the job alive indefinitely. 
   
   > [!NOTE]
   > If you use `sleep infinity`, you must manually [cancel the job](./how-to-interactive-jobs.md#end-job) to release the compute resource and stop billing. 

1. Submit your training job. For more details on how to train with the Python SDK, see [Train a model](./how-to-train-model.md).

# [Azure CLI](#tab/azurecli)

1. Create a job YAML file named `job.yaml` using the sample content. Replace `your compute name` with your own value. If you want to use a custom environment, see [this tutorial](how-to-manage-environments-v2.md) for examples on how to create a custom environment. 
   ```yaml
   code: src 
   command: 
     python train.py 
     # you can add a command like "sleep 1h" to reserve the compute resource is reserved after the script finishes running.
   environment: azureml:AzureML-tensorflow-2.12-cuda11@latest
   compute: azureml:<your compute name>
   services:
       my_vs_code:
         type: vs_code
         nodes: all # For distributed jobs, use the `nodes` property to pick which node you want to enable interactive services on. If `nodes` are not selected, by default, interactive applications are only enabled on the head node. Values are "all", or compute node index (for ex. "0", "1" etc.)
       my_tensor_board:
         type: tensor_board
         log_dir: "output/tblogs" # relative path of Tensorboard logs (same as in your training script)
         nodes: all
       my_jupyter_lab:
         type: jupyter_lab
         nodes: all
       my_ssh:
         type: ssh
         ssh_public_keys: <paste the entire pub key content>
         nodes: all
   ```

   The `services` section specifies the training applications you want to interact with.  

   To specify the amount of time you want to reserve the compute resource, add `sleep <specific time>` at the end of the command. The format follows: 
   * `sleep 1s`
   * `sleep 1m`
   * `sleep 1h`
   * `sleep 1d`

   You can also use the `sleep infinity` command that keeps the job alive indefinitely. 

   > [!NOTE]
   > If you use `sleep infinity`, you must manually [cancel the job](./how-to-interactive-jobs.md#end-job) to release the compute resource and stop billing. 

1. Run the command `az ml job create --file <path to your job yaml file> --workspace-name <your workspace name> --resource-group <your resource group name> --subscription <sub-id>` to submit your training job. For more details on running a job via CLI, see [this article](./how-to-train-model.md). 

---
### Connect to endpoints
# [Azure Machine Learning studio](#tab/ui)
To interact with your running job, select **Debug and monitor** on the job details page. 

:::image type="content" source="media/interactive-jobs/debug-and-monitor.png" alt-text="Screenshot of interactive jobs debug and monitor panel location.":::








































When you select the applications in the panel, you open a new tab for the applications. You can access the applications only when they're in **Running** status and only the **job owner** is authorized to access the applications. If you're training on multiple nodes, you can pick the specific node you want to interact with.

:::image type="content" source="media/interactive-jobs/interactive-jobs-application-list.png" alt-text="Screenshot of interactive jobs right panel information. Information content varies depending on the user's data.":::

It might take a few minutes to start the job and the training applications specified during job creation.

# [Python SDK](#tab/python)
- After you submit the job, use `ml_client.jobs.show_services("<job name>", node_index=<compute node index>)` to view the interactive service endpoints.
    
- To connect via SSH to the container where the job is running, run the command `az ml job connect-ssh --name <job-name> --node-index <compute node index> --private-key-file-path <path to private key> --resource-group <your resource group name> --workspace-name <your workspace name>`. To set up the Azure Machine Learning CLI, follow this [guide](./how-to-configure-cli.md). 
  
For reference documentation, see [JobOperations](https://learn.microsoft.com/python/api/azure-ai-ml/azure.ai.ml.operations.joboperations?view=azure-python).

You can access the applications only when they're in **Running** status and only the **job owner** is authorized to access the applications. If you're training on multiple nodes, you can pick the specific node you want to interact with by passing in the node index.

# [Azure CLI](#tab/azurecli)
- When the job is **running**, run the command `az ml job show-services --name <job name> --node-index <compute node index> --resource-group <your resource group name> --workspace-name <your workspace name>` to get the URL to the applications. The endpoint URL shows under `services` in the output. For VS Code, you must copy and paste the provided URL in your browser. 

- To connect via SSH to the container where the job is running, run the command `az ml job connect-ssh --name <job-name> --node-index <compute node index> --private-key-file-path <path to private key> --resource-group <your resource group name> --workspace-name <your workspace name>`. 

For reference documentation, see [az ml job](/cli/azure/ml/job).

You can access the applications only when they're in **Running** status and only the **job owner** is authorized to access the applications. If you're training on multiple nodes, you can pick the specific node you want to interact with by passing in the node index.

---
### Interact with the applications
When you select the endpoints to interact with your job, you're taken to the user container under your working directory. You can access your code, inputs, outputs, and logs. If you run into any issues while connecting to the applications, you can find the interactive capability and applications logs in **system_logs->interactive_capability** under the **Outputs + logs** tab.

:::image type="content" source="./media/interactive-jobs/interactive-logs.png" alt-text="Screenshot of interactive jobs interactive logs panel location.":::

- You can open a terminal from Jupyter Lab and start interacting within the job container. You can also directly iterate on your training script by using Jupyter Lab. 

  :::image type="content" source="./media/interactive-jobs/jupyter-lab.png" alt-text="Screenshot of interactive jobs Jupyter lab content panel.":::

- You can also interact with the job container within VS Code. To attach a debugger to a job during job submission and pause execution, [navigate here](./how-to-interactive-jobs.md#attach-a-debugger-to-a-job).

  > [!NOTE]
  > Private link-enabled workspaces aren't currently supported when interacting with the job container by using VS Code.

  :::image type="content" source="./media/interactive-jobs/vs-code-open.png" alt-text="Screenshot of interactive jobs VS Code panel when first opened. This shows the sample python file that was created to print two lines.":::

- If you log TensorFlow events for your job, you can use TensorBoard to monitor the metrics while your job is running.

  :::image type="content" source="./media/interactive-jobs/tensorboard-open.png" alt-text="Screenshot of interactive jobs tensorboard panel when first opened. This information varies depending upon customer data":::

### End job
When you're done with the interactive training, you can go to the job details page to cancel the job. Canceling the job releases the compute resource. Alternatively, use `az ml job cancel --name <your job name> --resource-group <your resource group name> --workspace-name <your workspace name>` in the CLI or `ml_client.jobs.begin_cancel("<job name>")` in the SDK. 

:::image type="content" source="./media/interactive-jobs/cancel-job.png" alt-text="Screenshot of interactive jobs cancel job option and its location for user selection":::

## Attach a debugger to a job
To submit a job with a debugger attached and the execution paused, use debugpy and VS Code. You must install `debugpy` in your job environment. 

> [!NOTE]
> Private link-enabled workspaces aren't currently supported when attaching a debugger to a job in VS Code.

1. During job submission (either through the UI, the CLI, or the SDK), use the debugpy command to run your Python script. For example, the following screenshot shows a sample command that uses debugpy to attach the debugger for a TensorFlow script (`tfevents.py` can be replaced with the name of your training script).
   
:::image type="content" source="./media/interactive-jobs/use-debugpy.png" alt-text="Screenshot of interactive jobs configuration of debugpy":::

1. After you submit the job, [connect to the VS Code](./how-to-interactive-jobs.md#connect-to-endpoints) and select the built-in debugger.
   
   :::image type="content" source="./media/interactive-jobs/open-debugger.png" alt-text="Screenshot of interactive jobs location of open debugger on the left side panel":::

1. Use the **Remote Attach** debug configuration to attach to the submitted job and pass in the path and port you configured in your job submission command. You can also find this information on the job details page.
   
   :::image type="content" source="./media/interactive-jobs/debug-path-and-port.png" alt-text="Screenshot of interactive jobs completed jobs":::

   :::image type="content" source="./media/interactive-jobs/remote-attach.png" alt-text="Screenshot of interactive jobs add a remote attach button":::

1. Set breakpoints and walk through your job execution as you would in your local debugging workflow. 
   
    :::image type="content" source="./media/interactive-jobs/set-breakpoints.png" alt-text="Screenshot of location of an example breakpoint that is set in the Visual Studio Code editor":::

> [!NOTE]
> If you use debugpy to start your job, your job **doesn't** execute unless you attach the debugger in VS Code and execute the script. If you don't attach the debugger, the compute is reserved until the job is [cancelled](./how-to-interactive-jobs.md#end-job).

## Next steps

+ Learn more about [how and where to deploy a model](./how-to-deploy-online-endpoints.md).
