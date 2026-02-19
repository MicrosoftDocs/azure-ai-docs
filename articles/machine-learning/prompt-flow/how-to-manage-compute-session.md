---
title: Manage prompt flow compute session
titleSuffix: Azure Machine Learning
description: Learn how to manage prompt flow compute session in Azure Machine Learning studio.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: how-to
author: s-polly
ms.author: lagayhar
ms.reviewer: sooryar
ms.date: 08/25/2025
ms.custom:
  - build-2024
  - sfi-image-nochange
ms.update-cycle: 365-days
---

# Manage prompt flow compute session in Azure Machine Learning Studio

A prompt flow compute session provides the computing resources required for the application to run, including a Docker image with all necessary dependency packages. This reliable, scalable environment lets prompt flow efficiently execute tasks and functions, ensuring a seamless user experience.

## Permissions and roles for compute session management

To assign roles, you need `owner` or `Microsoft.Authorization/roleAssignments/write` permission on the resource.

For users of the compute session, assign the `AzureML Data Scientist` role in the workspace. To learn more, see [Manage access to an Azure Machine Learning workspace](../how-to-assign-roles.md?view=azureml-api-2&tabs=labeler&preserve-view=true).

Role assignment can take several minutes to take effect.

## Start a compute session in studio

Before using Azure Machine Learning studio to start a compute session, ensure that:

- You have the `AzureML Data Scientist` role in the workspace.
- The default data store (usually `workspaceblobstore`) in your workspace is of the blob type.
- The working directory (`workspaceworkingdirectory`) exists in the workspace.
- If you use a virtual network for prompt flow, you understand the considerations in [Network isolation in prompt flow](how-to-secure-prompt-flow.md).

### Start a compute session on a flow page

Each flow binds to a single compute session. Start a compute session on a flow page.

- Select **Start**. Start a compute session using the environment defined in `flow.dag.yaml` in the flow folder. It runs on the virtual machine (VM) size of serverless compute, provided you have enough quota in the workspace.

  :::image type="content" source="./media/how-to-manage-compute-session/start-compute-session.png" alt-text="Screenshot of prompt flow with default settings for starting a compute session on a flow page." lightbox = "./media/how-to-manage-compute-session/start-compute-session.png":::

- Select **Start with advanced settings**. In the advanced settings, you can:

  - Select compute type. You can choose between serverless compute and compute instance. 
    - If you choose serverless compute, you can set following settings:
        - Customize the VM size that the compute session uses. Opt for VM series D and above. For more information, see the section on [Supported VM series and sizes](../concept-compute-target.md#supported-vm-series-and-sizes)
        - Customize the idle time, which deletes the compute session automatically if it isn't in use for a while.
        - Set the user-assigned managed identity. The compute session uses this identity to pull a base image, auth with connection and install packages. Ensure the user-assigned managed identity has sufficient permissions. If you don't set this identity, the user identity is used by default. 

        :::image type="content" source="./media/how-to-manage-compute-session/start-compute-session-with-advanced-settings.png" alt-text="Screenshot of prompt flow with advanced settings using serverless compute for starting a compute session on a flow page." lightbox = "./media/how-to-manage-compute-session/start-compute-session-with-advanced-settings.png":::

        - You can use following CLI command to assign user assigned managed identity to workspace. [Learn more about how to create and update user-assigned identities for a workspace](../how-to-identity-based-service-authentication.md#to-create-a-workspace-with-multiple-user-assigned-identities-use-one-of-the-following-methods). 


        ```azurecli
        az ml workspace update -f workspace_update_with_multiple_UAIs.yml --subscription <subscription ID> --resource-group <resource group name> --name <workspace name>
        ```
        
        Where the contents of *workspace_update_with_multiple_UAIs.yml* are as follows:
        
        ```yaml
        identity:
           type: system_assigned, user_assigned
           user_assigned_identities:
            '/subscriptions/<subscription_id>/resourcegroups/<resource_group_name>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<uai_name>': {}
            '<UAI resource ID 2>': {}
        ```

        > [!TIP]
        > The following [Azure RBAC role assignments](/azure/role-based-access-control/role-assignments) are required on your user-assigned managed identity for your Azure Machine Learning workspace to access data on the workspace-associated resources.
        
        |Resource|Permission|
        |---|---|
        |Azure Machine Learning workspace|Contributor|
        |Azure Storage|Contributor (control plane) + Storage Blob Data Contributor + Storage File Data Privileged Contributor (data plane, consume flow draft in fileshare and data in blob)|
        |Azure Key Vault (when using [access policies permission model](/azure/key-vault/general/assign-access-policy))|Contributor + any access policy permissions besides **purge** operations, this is **default mode** for linked Azure Key Vault.|
        |Azure Key Vault (when using [RBAC permission model](/azure/key-vault/general/rbac-guide))|Contributor (control plane) + Key Vault Administrator (data plane)|
        |Azure Container Registry|Contributor|
        |Azure Application Insights|Contributor|
        
        > [!NOTE]
        > The job submitter needs `assign` permission on the user-assigned managed identity. Assign the `Managed Identity Operator` role, as each time a serverless compute session is created, the user-assigned managed identity is assigned to the compute.

    - If you choose compute instance as compute type, you can only set idle shutdown time. 
        - Since it runs on an existing compute instance, the VM size is fixed and can't be changed during the session.
        - Identity used for this session is also defined in compute instance, by default it uses the user identity. [Learn more about how to assign identity to compute instance](../how-to-create-compute-instance.md#assign-managed-identity)
        - For the idle shutdown time it's used to define life cycle of the compute session, if the session is idle for the time you set, it's deleted automatically. If idle shutdown is enabled on the compute instance, it takes effect at the compute level.

            :::image type="content" source="./media/how-to-manage-compute-session/start-compute-session-with-advanced-settings-compute-instance.png" alt-text="Screenshot of prompt flow with advanced settings using compute instance for starting a compute session on a flow page." lightbox = "./media/how-to-manage-compute-session/start-compute-session-with-advanced-settings-compute-instance.png":::
        - Learn more about [how to create and manage compute instance](../how-to-create-compute-instance.md)

## Use a compute session to submit a flow run in CLI/SDK

Besides using Studio, specify the compute session in CLI or SDK when submitting a flow run.

# [Azure CLI](#tab/cli)

Specify the instance type or compute instance name under the resource section. If the instance type or compute instance name isn't specified, Azure Machine Learning chooses an instance type (VM size) based on factors like quota, cost, performance, and disk size. Learn more about [serverless compute](../how-to-use-serverless-compute.md).

```yaml
$schema: https://azuremlschemas.azureedge.net/promptflow/latest/Run.schema.json
flow: <path_to_flow>
data: <path_to_flow>/data.jsonl

# specify identity used by serverless compute.
# default value
# identity:
#   type: user_identity 

# use workspace first UAI
# identity:
#   type: managed
  
# use specified client_id's UAI
# identity:
#   type: managed
#   client_id: xxx

column_mapping:
  url: ${data.url}

# define cloud resource

resources:
  instance_type: <instance_type> # serverless compute type
  # compute: <compute_instance_name> # use compute instance as compute type

```

Submit this run via CLI:

```sh
pfazure run create --file run.yml
```

# [Python SDK](#tab/python)

```python
# load flow
flow = "<path_to_flow>"
data = "<path_to_flow>/data.jsonl"


# create run
run = Run(
    # local flow file
    flow=flow,
    # remote data
    data=data,
    # to customize runtime instance type and compute instance, you can provide them in resources
    # resources={
    #     "instance_type": "STANDARD_DS11_V2",
    #     "compute": "my_compute_instance"
    # }
    # to customize identity, you can provide them in identity
    # identity={
    #     "type": "managed",
    # }
)

base_run = pf.runs.create_or_update(run=run)

```

Learn a complete end-to-end code-first example: [Integrate prompt flow with LLM-based application DevOps](./how-to-integrate-with-llm-app-devops.md).

---

  > [!NOTE]
  > The idle shutdown is one hour if you are using CLI/SDK to submit a flow run. You can go to compute page to release compute.

### Reference files outside of the flow folder
Sometimes, you might want to reference a `requirements.txt` file that is outside the flow folder. For example, you might have complex project that includes multiple flows, and they share the same `requirements.txt` file. To do this, add the `additional_includes` field to the `flow.dag.yaml`. The value of this field is a list of the relative file/folder path to the flow folder. For example, if requirements.txt is in the parent folder of the flow folder, you can add `../requirements.txt` to the `additional_includes` field.

```yaml
inputs:
  question:
    type: string
outputs:
  output:
    type: string
    reference: ${answer_the_question_with_context.output}
environment:
  python_requirements_txt: requirements.txt
additional_includes:
  - ../requirements.txt
...
```

The `requirements.txt` file is copied to the flow folder and used to start the compute session.

## Update a compute session on the studio flow page

On a flow page, use these options to manage a compute session:

- **Change compute session settings**: Change settings like VM size or the user-assigned managed identity for serverless compute. If you're using a compute instance, switch to another instance. 
- If you change the VM size, the compute session resets with the new VM size.
- **Install packages from requirements.txt**: Open `requirements.txt` in the prompt flow UI and add packages.
- **View installed packages**: Shows the packages installed in the compute session, including those in the base image and specified in the `requirements.txt` file in the flow folder.
- **Reset compute session** deletes the current compute session and creates a new one with the same environment. If you encounter a package conflict issue, you can try this option.
- **Stop compute session** deletes the current compute session. If there's no active compute session on the underlying compute, the serverless compute resource will also be deleted.

:::image type="content" source="./media/how-to-manage-compute-session/update-compute-session.png" alt-text="Screenshot of actions for a compute session on a flow page." lightbox = "./media/how-to-manage-compute-session/update-compute-session.png":::

You can also customize the environment that you use to run this flow by adding packages in the `requirements.txt` file in the flow folder. After you add more packages in this file, you can choose either of these options:

- **Save and install** triggers `pip install -r requirements.txt` in the flow folder. The process can take a few minutes, depending on the packages that you install.
- **Save only** just saves the `requirements.txt` file. You can install the packages later yourself.

:::image type="content" source="./media/how-to-manage-compute-session/save-install.png" alt-text="Screenshot of the option to save and install packages for a compute session on a flow page." lightbox = "./media/how-to-manage-compute-session/save-install.png":::

> [!NOTE]
> You can change the location and even the file name of `requirements.txt`, but be sure to also change it in the `flow.dag.yaml` file in the flow folder.
>
> Don't pin the versions of `promptflow` and `promptflow-tools` in `requirements.txt` because they are already included in the session base image.
> 
> `requirements.txt` won't support local wheel files.  Build them in your image and update the customized base image in `flow.dag.yaml`. Learn more about [how to build a custom base image](how-to-customize-session-base-image.md).

#### Add packages in a private feed in Azure DevOps

If you want to use a private feed in Azure DevOps, follow these steps:

1. Assign a managed identity to the workspace or compute instance.
    1. If you use serverless compute as the compute session, assign a user-assigned managed identity to the workspace.
        1. Create a user-assigned managed identity and add it to the Azure DevOps organization. To learn more, see [Use service principals and managed identities](/azure/devops/integrate/get-started/authentication/service-principal-managed-identity).

            > [!NOTE]
            > If the **Add Users** button isn't visible, you probably don't have the necessary permissions to perform this action.
        
        2. [Add or update user-assigned identities to a workspace](../how-to-identity-based-service-authentication.md#to-create-a-workspace-with-multiple-user-assigned-identities-use-one-of-the-following-methods).

            > [!NOTE]
            > Please make sure the user-assigned managed identity has `Microsoft.KeyVault/vaults/read` on the workspace linked keyvault.
  
    2. If you use a compute instance as the compute session, [assign a user-assigned managed identity to the compute instance](../how-to-create-compute-instance.md#assign-managed-identity).

2. Add `{private}` to your private feed URL. For example, if you want to install `test_package` from `test_feed` in Azure DevOps, add `-i https://{private}@{test_feed_url_in_azure_devops}` in `requirements.txt`:

   ```txt
   -i https://{private}@{test_feed_url_in_azure_devops}
   test_package
   ```

3. Specify using user-assigned managed identity in the compute session configuration. 
    1. If you're using serverless compute, specify the user-assigned managed identity in **Start with advanced settings** if compute session isn't running, or use the **Change compute session settings** button if compute session is running.

       :::image type="content" source="./media/how-to-manage-compute-session/compute-session-user-assigned-identity.png" alt-text="Screenshot that shows the toggle for using a workspace user-assigned managed identity. " lightbox = "./media/how-to-manage-compute-session/compute-session-user-assigned-identity.png":::
    2. If you're using compute instance, it uses the user-assigned managed identity that you assigned to the compute instance.


> [!NOTE]
> This approach mainly focuses on quick testing in flow develop phase, if you also want to deploy this flow as endpoint please build this private feed in your image and update customize base image in `flow.dag.yaml`. Learn more [how to build custom base image](how-to-customize-session-base-image.md)

#### Change the base image for compute session

By default, we use the latest prompt flow base image. If you want to use a different base image, you can [build a custom one](how-to-customize-session-base-image.md). 

- In studio, you can change the base image in base image settings under compute session settings. 

:::image type="content" source="./media/how-to-manage-compute-session/change-base-image.png" alt-text="Screenshot of changing base image of a compute session on a flow page." lightbox = "./media/how-to-manage-compute-session/change-base-image.png":::

- You can also specify the new base image under `environment` in the `flow.dag.yaml` file in the flow folder. 

    :::image type="content" source="./media/how-to-manage-compute-session/base-image-in-flow-dag.png" alt-text="Screenshot of actions for customizing a base image for a compute session on a flow page." lightbox = "./media/how-to-manage-compute-session/base-image-in-flow-dag.png":::
    
    ```yaml
    environment:
        image: <your-custom-image>
        python_requirements_txt: requirements.txt
    ```

To use the new base image, you need to reset the compute session. This process takes several minutes as it pulls the new base image and reinstalls packages.

## Manage serverless instance used by a compute session
Use serverless compute as a compute session to manage the serverless instance. View the serverless instance in the compute session list tab on the compute page. 

:::image type="content" source="./media/how-to-manage-compute-session/serverless-instance-list.png" alt-text="Screenshot of a list of serverless instances." lightbox = "./media/how-to-manage-compute-session/serverless-instance-list.png":::

Access flows and runs on the compute under the **Active flows and runs** tab. Deleting the instance impacts the flows and runs on it.

:::image type="content" source="./media/how-to-manage-compute-session/active-flows-runs-serverless-instance.png" alt-text="Screenshot of the compute detail page for a serverless instance." lightbox = "./media/how-to-manage-compute-session/active-flows-runs-serverless-instance.png":::

## Relationship between compute session, compute resource, flow, and user

- A single user can have multiple compute resources (serverless or compute instance). For example, a user might have compute resources with different VM sizes or user-assigned managed identities.
- A compute resource can only be used by a single user. It acts as a private development box for that user. Multiple users can't share the same compute resource. 
- A compute resource can host multiple compute sessions. A compute session is a container running on the underlying compute resource. For example, prompt flow authoring doesn't require many compute resources, so a single compute resource can host multiple compute sessions for the same user. 
- A compute session belongs to only one compute resource at a time. You can delete or stop a compute session and reallocate it to another compute resource.
- A flow can have only one compute session. Each flow is self-contained and defines the base image and required Python packages in the flow folder for the compute session.

## Switch runtime to compute session

Compute sessions offer these advantages over compute instance runtimes:
- Automatically manage the lifecycle of sessions and underlying compute. You don't need to manually create or manage them anymore.
- Customize packages easily by adding them to the `requirements.txt` file in the flow folder instead of creating a custom environment.

Switch a compute instance runtime to a compute session with these steps:
- Prepare the `requirements.txt` file in the flow folder. Don't pin the versions of `promptflow` and `promptflow-tools` in `requirements.txt` because they are already included in the base image. The compute session installs the packages in the `requirements.txt` file when it starts.
- If you create a custom environment for a compute instance runtime, get the image from the environment detail page and specify it in the `flow.dag.yaml` file in the flow folder. To learn more, see [Change the base image for compute session](#change-the-base-image-for-compute-session). Ensure that you or the related user-assigned managed identity on the workspace has `acr pull` permission for the image.

:::image type="content" source="./media/how-to-manage-compute-session/image-path-environment-detail.png" alt-text="Screenshot showing how to find the image in the environment detail page." lightbox = "./media/how-to-manage-compute-session/image-path-environment-detail.png":::

- For the compute resource, continue using the existing compute instance to manually manage the lifecycle, or try serverless compute, which is managed by the system.

## Next steps

- [Customize base image of compute session](how-to-customize-session-base-image.md)
- [Develop a standard flow](how-to-develop-a-standard-flow.md)
- [Develop a chat flow](how-to-develop-a-chat-flow.md)
