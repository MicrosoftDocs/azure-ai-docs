---
title: Set up MLOps with Azure DevOps
titleSuffix: Azure Machine Learning
description: Learn how to set up a sample MLOps environment in Azure Machine Learning
services: machine-learning
ms.author: scottpolly
author: s-polly
ms.service: azure-machine-learning
ms.reviewer: jturuk
ms.subservice: mlops
ms.date: 01/29/2026
ms.topic: concept-article
ms.custom:
  - cli-v2
  - sdk-v2
  - sfi-image-nochange
  - dev-focus
ai-usage: ai-assisted
---

# Set up MLOps with Azure DevOps

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

Azure Machine Learning integrates with [Azure DevOps pipeline](/azure/devops/pipelines/) to automate the machine learning lifecycle. Some of the operations you can automate are:

* Deployment of Azure Machine Learning infrastructure
* Data preparation (extract, transform, and load operations)
* Training machine learning models with on-demand scale-out and scale-up
* Deployment of machine learning models as public or private web services
* Monitoring deployed machine learning models (such as for performance analysis)

In this article, you learn how to use Azure Machine Learning to set up an end-to-end MLOps pipeline that runs a linear regression to predict taxi fares in NYC. The pipeline is made up of components, each serving different functions. You can register these components with the workspace, version them, and reuse them with various inputs and outputs. Use the [recommended Azure architecture for MLOps](/azure/architecture/data-guide/technology-choices/machine-learning-operations-v2) and [AzureMLOps (v2) solution accelerator](https://github.com/Azure/mlops-v2) to quickly set up an MLOps project in Azure Machine Learning.

> [!TIP]
> Before implementing any solution, review some of the [recommended Azure architectures](/azure/architecture/data-guide/technology-choices/machine-learning-operations-v2) for MLOps. Choose the best architecture for your machine learning project.

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure Machine Learning workspace.
- Git running on your local machine.
- Python 3.10 or later, if using the Python SDK v2 locally.
- An [organization](/azure/devops/organizations/accounts/create-organization) in Azure DevOps.
- [Azure DevOps project](how-to-devops-machine-learning.md) that hosts the source repositories and pipelines.
- The [Terraform extension for Azure DevOps](https://marketplace.visualstudio.com/items?itemName=ms-devlabs.custom-terraform-tasks) if you're using Azure DevOps + Terraform to spin up infrastructure.

> [!NOTE]
>
>Git version 2.27 or newer is required. For more information on installing the Git command, see https://git-scm.com/downloads and select your operating system.

> [!IMPORTANT]
>The CLI commands in this article were tested using Bash. If you use a different shell, you might encounter errors.

## Set up authentication with Azure and DevOps

Before you can set up an MLOps project with Azure Machine Learning, you need to set up authentication for Azure DevOps.

### Create service principal

> [!TIP]
> For enhanced security, consider using [workload identity federation](/azure/devops/pipelines/library/connect-to-azure) instead of service principals with secrets. Workload identity federation eliminates the need for secret rotation and is the recommended approach for new service connections.

For the demo, create one or two service principals, depending on how many environments you want to work on (Dev, Prod, or both). You can create these principals by using one of the following methods:

# [Create from Azure Cloud Shell](#tab/azure-shell)

1. Launch the [Azure Cloud Shell](https://shell.azure.com).

    > [!TIP]
    > The first time you launch the Cloud Shell, you're prompted to create a storage account for the Cloud Shell.

1. If prompted, choose **Bash** as the environment used in the Cloud Shell. You can also change environments in the drop-down on the top navigation bar.

    ![Screenshot of the cloud shell environment dropdown.](./media/how-to-setup-mlops-azureml/ps-cli1-1.png)

1. Copy the following bash commands to your computer and update the **projectName**, **subscriptionId**, and **environment** variables with the values for your project. If you're creating both a Dev and Prod environment, run this script once for each environment, creating a service principal for each environment. This command also grants the **Contributor** role to the service principal in the subscription you provide. Azure DevOps needs this role to properly use resources in that subscription. 

    ``` bash
    projectName="<your project name>"
    roleName="Contributor"
    subscriptionId="<subscription Id>"
    environment="<Dev|Prod>" #First letter should be capitalized
    servicePrincipalName="Azure-ARM-${environment}-${projectName}"
    # Verify the ID of the active subscription
    echo "Using subscription ID $subscriptionID"
    echo "Creating SP for RBAC with name $servicePrincipalName, with role $roleName and in scopes     /subscriptions/$subscriptionId"
    az ad sp create-for-rbac --name $servicePrincipalName --role $roleName --scopes /subscriptions/$subscriptionId
    echo "Please ensure that the information created here is properly save for future use."
    ```

1. Copy your edited commands into the Azure Shell and run them (**Ctrl** + **Shift** + **v**).

1. After running these commands, you see information related to the service principal. Save this information to a safe location. You use it later in the demo to configure Azure DevOps.

    ```json
    {
       "appId": "<application id>",
       "displayName": "Azure-ARM-dev-Sample_Project_Name",
       "password": "<password>",
       "tenant": "<tenant id>"
    }
    ```

1. Repeat **Step 3** if you're creating service principals for Dev and Prod environments. For this demo, you create only one environment, which is Prod.

1. Close the Cloud Shell once the service principals are created. 
      

# [Create from Azure portal](#tab/azure-portal)

1. Go to [Azure App Registrations](https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade/quickStartType~/null/sourceTypeMicrosoft_AAD_IAM).

1. Select **New Registration**.

    ![Screenshot of service principal setup.](./media/how-to-setup-mlops-azureml/SP-setup-ownership-tab.png)

1. Create a service principal (SP) by selecting **Accounts in any organizational directory (Any Microsoft Entra directory - Multitenant)**. Name the service principal **Azure-ARM-Dev-ProjectName**. After creating it, create a new service principal named **Azure-ARM-Prod-ProjectName**. Replace **ProjectName** with the name of your project so that the service principal can be uniquely identified. 

1. Go to **Certificates & Secrets** and add **New client secret** for each service principal. Store the value and secret separately.

1. To assign the necessary permissions to these principals, select your respective [subscription](https://portal.azure.com/#view/Microsoft_Azure_BillingSubscriptionsBlade?) and go to IAM. Select **+Add** and then select **Add Role Assignment**.

    ![Screenshot of the add role assignment page.](./media/how-to-setup-mlops-azureml/SP-setup-iam-tab.png)

1. Select Contributor and add members by selecting + **Select Members**. Add the member **Azure-ARM-Dev-ProjectName** as created earlier.

    ![Screenshot of the add role assignment selection.](./media/how-to-setup-mlops-azureml/SP-setup-role-assignment.png)

1. Repeat this step if you deploy dev and prod into the same subscription. Otherwise, change to the prod subscription and repeat with **Azure-ARM-Prod-ProjectName**. The basic service principal setup is finished.

---

### Set up Azure DevOps

1. Go to [Azure DevOps](https://go.microsoft.com/fwlink/?LinkId=2014676&githubsi=true&clcid=0x409&WebUserId=2ecdcbf9a1ae497d934540f4edce2b7d). 
   
1. Select **create a new project**. Name the project `mlopsv2` for this tutorial.
   
     ![Screenshot of ADO Project.](./media/how-to-setup-mlops-azureml/ado-create-project.png)
   
1. In the project, under **Project Settings** (at the bottom left of the project page), select **Service Connections**.
   
1. Select **Create Service Connection**.

     ![Screenshot of ADO New Service connection button.](./media/how-to-setup-mlops-azureml/create_first_service_connection.png)

1. Select **Azure Resource Manager**, and then select **Next**.

   > [!NOTE]
   > For new projects, select **App registration or Managed identity (manual)** with **Workload identity federation** credential for improved security. The steps in this article use the legacy **Service principal (manual)** approach with a secret, which requires manual rotation.

   Select **Service principal (manual)**, select **Next**, and select the Scope Level **Subscription**.

     - **Subscription Name** - Use the name of the subscription where your service principal is stored.
     - **Subscription Id** - Use the `subscriptionId` you used in **Step 1** input as the Subscription ID
     - **Service Principal Id** - Use the `appId` from **Step 1** output as the Service Principal ID
     - **Service principal key** - Use the `password` from **Step 1** output as the Service Principal Key
     - **Tenant ID** - Use the `tenant` from **Step 1** output as the Tenant ID


1. Name the service connection **Azure-ARM-Prod**.  
 
1. Select **Grant access permission to all pipelines**, and then select **Verify and Save**. 

The Azure DevOps setup finishes successfully.

### Set up source repository with Azure DevOps
   
1. Open the project you created in [Azure DevOps](https://dev.azure.com/).
   
1. Open the Repos section and select **Import Repository**.

    ![Screenshot of Azure DevOps import repo first time.](./media/how-to-setup-mlops-azureml/import_repo_first_time.png)

1. Enter `https://github.com/Azure/mlops-v2-ado-demo` into the Clone URL field. Select **import** at the bottom of the page.

    ![Screenshot of Azure DevOps import MLOps demo repo.](./media/how-to-setup-mlops-azureml/import-repo-git-template.png)

    > [!NOTE]
    > The demo repository might have pending dependency updates. After importing, check for any Dependabot security alerts and apply updates as needed. For the latest features and fixes, also review the main [Azure MLOps (v2) solution accelerator](https://github.com/Azure/mlops-v2) repository.

1. Open the **Project settings** at the bottom of the left hand navigation pane.

1.  Under the Repos section, select **Repositories**. Select the repository you created in previous step. Select the **Security** tab.

1. Under the User permissions section, select the **mlopsv2 Build Service** user. Change the permission **Contribute** permission to **Allow** and the **Create branch** permission to **Allow**.
   ![Screenshot of Azure DevOps permissions.](./media/how-to-setup-mlops-azureml/ado-permissions-repo.png)

1. Open the **Pipelines** section in the left hand navigation pane and select on the 3 vertical dots next to the **Create Pipelines** button. Select **Manage Security**.

   ![Screenshot of Pipeline security.](./media/how-to-setup-mlops-azureml/ado-open-pipelinesSecurity.png)

1. Select the **mlopsv2 Build Service** account for your project under the Users section. Change the permission **Edit build pipeline** to **Allow**.

   ![Screenshot of Add security.](./media/how-to-setup-mlops-azureml/ado-add-pipelinesSecurity.png)

> [!NOTE]
> This finishes the prerequisite section. You can now deploy the solution accelerator.


## Deploy infrastructure via Azure DevOps
This step deploys the training pipeline to the Azure Machine Learning workspace that you created in the previous steps. 

> [!TIP]
> Before you check out the MLOps v2 repo and deploy the infrastructure, make sure you understand the [Architectural Patterns](/azure/architecture/data-guide/technology-choices/machine-learning-operations-v2) of the solution accelerator. In the examples, you use the [classical ML project type](/azure/architecture/data-guide/technology-choices/machine-learning-operations-v2#classical-machine-learning-architecture).

### Run Azure infrastructure pipeline
1. Go to your repository, `mlops-v2-ado-demo`, and select the **config-infra-prod.yml** file.

    > [!IMPORTANT]
    > Make sure you select the **main** branch of the repo.
   
   ![Screenshot of Repo in ADO.](./media/how-to-setup-mlops-azureml/ADO-repo.png)
   
   This config file uses the namespace and postfix values the names of the artifacts to ensure uniqueness. Update the following section in the config to your liking.
   
   ```
    namespace: [5 max random new letters]
    postfix: [4 max random new digits]
    location: eastus
   ```
   > [!NOTE]
   > If you're running a deep learning workload such as CV or NLP, ensure your GPU compute is available in your deployment zone.

1. Select **Commit** to push code and get these values into the pipeline. 

1. Go to the **Pipelines** section. 
   
   ![Screenshot of ADO Pipelines.](./media/how-to-setup-mlops-azureml/ADO-pipelines.png)
   
1. Select **Create Pipeline**.
   
1. Select **Azure Repos Git**.
   
   ![Screenshot of ADO Where's your code.](./media/how-to-setup-mlops-azureml/ado-wheresyourcode.png)
   
1. Select the repository that you cloned from the previous section, `mlops-v2-ado-demo`.
   
1. Select **Existing Azure Pipelines YAML file**.
   
   ![Screenshot of Azure DevOps Pipeline page on configure step.](./media/how-to-setup-mlops-azureml/ADO-configure-pipelines.png)
   
   
1. Select the `main` branch and choose `mlops/devops-pipelines/cli-ado-deploy-infra.yml`, then select **Continue**. 

1. Run the pipeline. It takes a few minutes to finish. The pipeline creates the following artifacts:
   * Resource group for your workspace including storage account, container registry, Application Insights, Key Vault, and the Azure Machine Learning Workspace itself.
   * In the workspace, it also creates a compute cluster.
   
1. Now the infrastructure for your MLOps project is deployed.
    ![Screenshot of ADO Infra Pipeline screen.](./media/how-to-setup-mlops-azureml/ADO-infra-pipeline.png)

    > [!NOTE]
    > You can ignore the **Unable move and reuse existing repository to required location** warnings.

## Sample training and deployment scenario

The solution accelerator includes code and data for a sample end-to-end machine learning pipeline that runs a linear regression to predict taxi fares in NYC. The pipeline is made up of components, each serving different functions. You can register these components with the workspace, version them, and reuse them with various inputs and outputs. Sample pipelines and workflows for the Computer Vision and NLP scenarios have different steps and deployment steps.

This training pipeline contains the following steps:

**Prepare Data**
   - This component takes multiple taxi datasets (yellow and green) and merges and filters the data. It prepares the train, validation, and evaluation datasets.
   - Input: Local data under ./data/ (multiple .csv files)
   - Output: Single prepared dataset (.csv) and train, validation, and test datasets.

**Train Model**
   - This component trains a Linear Regressor with the training set.
   - Input: Training dataset
   - Output: Trained model (pickle format)
   
**Evaluate Model**
   - This component uses the trained model to predict taxi fares on the test set.
   - Input: ML model and Test dataset
   - Output: Performance of model and a deploy flag whether to deploy or not.
   - This component compares the performance of the model with all previously deployed models on the new test dataset. It decides whether to promote the model into production. Promoting the model into production happens by registering the model in Azure Machine Learning workspace.

**Register Model**
   - This component scores the model based on how accurate the predictions are in the test set.
   - Input: Trained model and the deploy flag.
   - Output: Registered model in Azure Machine Learning.

## Deploy model training pipeline

1. Go to ADO pipelines.
   
   ![Screenshot of ADO Pipelines.](./media/how-to-setup-mlops-azureml/ADO-pipelines.png)

1. Select **New Pipeline**.
   
   ![Screenshot of ADO New Pipeline button.](./media/how-to-setup-mlops-azureml/ADO-new-pipeline.png)
   
1. Select **Azure Repos Git**.
   
   ![Screenshot of ADO Where's your code.](./media/how-to-setup-mlops-azureml/ado-wheresyourcode.png)
   
1. Select the repository that you cloned from the previous section, `mlopsv2`.
   
1. Select **Existing Azure Pipelines YAML file**.
   
   ![Screenshot of ADO Pipeline page on configure step.](./media/how-to-setup-mlops-azureml/ADO-configure-pipelines.png)
   
1. Select `main` as a branch and choose `/mlops/devops-pipelines/deploy-model-training-pipeline.yml`. Select **Continue**.  

1. **Save and Run** the pipeline.
   
> [!NOTE]
> At this point, the infrastructure is configured and the Prototyping Loop of the MLOps Architecture is deployed. You're ready to move to the trained model to production.      

## Deploying the trained model 

This scenario includes prebuilt workflows for two approaches to deploying a trained model: batch scoring or deploying a model to an endpoint for real-time scoring. Run either or both of these workflows to test the performance of the model in your Azure Machine Learning workspace. In this example, you use real-time scoring.

### Deploy ML model endpoint
1. Go to ADO pipelines.
   
   ![Screenshot of ADO Pipelines.](./media/how-to-setup-mlops-azureml/ADO-pipelines.png)

1. Select **New Pipeline**.
   
   ![Screenshot of ADO New Pipeline button for endpoint.](./media/how-to-setup-mlops-azureml/ADO-new-pipeline.png)
   
1. Select **Azure Repos Git**.
   
   ![Screenshot of ADO Where's your code.](./media/how-to-setup-mlops-azureml/ado-wheresyourcode.png)
   
1. Select the repository that you cloned from the previous section, `mlopsv2`.
   
1. Select **Existing Azure Pipelines YAML file**.
   
   ![Screenshot of Azure DevOps Pipeline page on configure step.](./media/how-to-setup-mlops-azureml/ADO-configure-pipelines.png)
   
1. Select `main` as a branch and choose Managed Online Endpoint `/mlops/devops-pipelines/deploy-online-endpoint-pipeline.yml` then select **Continue**.  
   
1. Online endpoint names need to be unique, so change `taxi-online-$(namespace)$(postfix)$(environment)` to another unique name and then select **Run**. You don't need to change the default if it doesn't fail.

   ![Screenshot of Azure DevOps batch deploy script.](./media/how-to-setup-mlops-azureml/ADO-batch-pipeline.png)
   
   > [!IMPORTANT]
   > If the run fails due to an existing online endpoint name, recreate the pipeline as described previously and change **[your endpoint-name]** to **[your endpoint-name (random number)]**
   
1. When the run completes, you see output similar to the following image:
   
   ![Screenshot of ADO Pipeline batch run result page.](./media/how-to-setup-mlops-azureml/ADO-batch-pipeline-run.png)

1. To test this deployment, go to the **Endpoints** tab in your Azure Machine Learning workspace, select the endpoint, and select the **Test** tab. You can use the sample input data located in the cloned repo at `/data/taxi-request.json` to test the endpoint.

## Clean up resources

1. If you don't plan to continue using your pipeline, delete your Azure DevOps project. 
1. In Azure portal, delete your resource group and Azure Machine Learning instance.

## Next steps

* [Install and set up Python SDK v2](https://aka.ms/sdk-v2-install)
* [Install and set up Python CLI v2](how-to-configure-cli.md)
* [Azure MLOps (v2) solution accelerator](https://github.com/Azure/mlops-v2) on GitHub
* Training course on [MLOps with Machine Learning](/training/paths/introduction-machine-learn-operations/)
* Learn more about [Azure Pipelines with Azure Machine Learning](how-to-devops-machine-learning.md)
* Learn more about [GitHub Actions with Azure Machine Learning](how-to-github-actions-machine-learning.md)
* Deploy MLOps on Azure in Less Than an Hour - [Community MLOps V2 Accelerator video](https://www.youtube.com/watch?v=5yPDkWCMmtk)
