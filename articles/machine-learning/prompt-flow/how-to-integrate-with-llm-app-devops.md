---
title: Integrate prompt flow with DevOps for LLM-based applications
titleSuffix: Azure Machine Learning
description: Integrate prompt flow with DevOps to enhance your LLM-based application development workflows in Azure Machine Learning.
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: how-to
author: lgayhardt
ms.author: lagayhar
ms.reviewer: chenlujiao
ms.date: 10/29/2024
---

# Integrate prompt flow with DevOps for LLM-based applications

Prompt flow is a developer-friendly and easy-to-use code-first experience to develop and iterate flows for large language model (LLM)-based application development. Prompt flow provides an SDK and CLI, a Visual Studio Code extension, and a flow UI. These tools facilitate local flow development, local flow run and evaluation run triggering, and transitioning flows from local to Azure Machine Learning cloud workspace environments.

You can combine the prompt flow code capability experience with developer operations (DevOps) to enhance your LLM-based application development workflows. This article focuses on integrating prompt flow with LLM-based application DevOps in Azure Machine Learning.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/devops-process.png" alt-text="Diagram showing the following flow: create flow, develop and test flow, versioning in code repo, submit runs to cloud, and debut and iteration." border="false" lightbox = "./media/how-to-integrate-with-llm-app-devops/devops-process.png":::

## Prerequisites

- An Azure Machine Learning workspace. To create one, see [Create resources to get started](../quickstart-create-resources.md).

- A Python environment with the Azure Machine Learning Python SDK v2 installed, created by following the instructions at [](https://github.com/Azure/azureml-examples/tree/sdk-preview/sdk#getting-started).

  This environment is for defining and controlling your Azure Machine Learning resources and is separate from the environment the compute session uses. For more information about the compute session, see [Manage prompt flow compute session in Azure Machine Learning studio](how-to-manage-compute-session.md).

- The prompt flow SDK installed by running `pip install promptflow` and `pip install promptflow-tools` in a command shell.

- Visual Studio Code with the Python and Prompt flow extensions installed.

  :::image type="content" source="./media/how-to-integrate-with-llm-app-devops/vs-code-extension.png" alt-text="Screenshot of the Python and Prompt flow extensions in Visual Studio Code."

## Use a code-first experience in prompt flow

When you develop applications that use LLMs, you usually follow a standardized application engineering process that includes code repositories and continuous integration/continuous deployment (CI/CD) pipelines. This integration allows for a streamlined development process, version control, and collaboration among team members.

The prompt flow code experience offers code developers a more efficient GenAIOps or LLMOps iteration process with the following key features and benefits:

- **Flow versioning in the code repository**. You define flows in YAML format, which stays aligned with the referenced source files in a folder structure.
- **Flow run integration with CI/CD pipelines**. You can seamlessly integrate into your CI/CD pipeline and delivery process by using the prompt flow CLI or SDK to trigger flow runs.
- **Smooth transition from local to cloud**. You can easily export your flow folder to your local or upstream code repository for version control, local development, and sharing. You can also effortlessly import the flow folder back to Azure Machine Learning for further authoring, testing, and deployment in cloud resources.

## Access prompt flow code

Each prompt flow has a flow folder structure that contains essential files for defining the flow in code. The folder structure organizes your flow, facilitating smoother transitions.

Azure Machine Learning offers a shared file system for all workspace users. Upon flow creation, a corresponding flow folder is automatically generated and stored in the *Users/\<username>/promptflow* directory.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-folder-created-in-file-share-storage.png" alt-text="Screenshot of standard flow creation showing a new flow." lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-folder-created-in-file-share-storage.png":::

### Flow folder structure

Once you create a flow, you can use the **Files** section of the flow authoring page to view, edit, and manage the flow files. Any modifications you make to the files reflect directly in the file share storage.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-file-explorer.png" alt-text="Screenshot of a standard flow authoring page highlighting the Files pane." lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-file-explorer.png":::

The flow folder structure contains the following key files:

- *flow.dag.yaml* is the primary flow definition file, in YAML format. This file is integral to authoring and defining the prompt flow and includes information about inputs, outputs, nodes, tools, and variants the flow uses.
- User-managed source code files in Python or Jinja 2 format refer to the tools and nodes in the flow. The Python tool uses *.py* files to define custom Python logic. The prompt tool and LLM tool use *.jinja2* files to define prompt context.
- Nonsource files like utility files and data files can be included in the flow folder with the source files.

Enable **Raw file mode** to view and edit the raw content of the files in the file editor, including the *flow.dag.yaml* flow definition file and the source files.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-day-yaml-raw-file.png" alt-text="Screenshot of Raw file mode on a standard flow." lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-day-yaml-raw-file.png":::

Alternatively, you can access all your flow folders and files directly from the Azure Machine Learning **Notebooks** page.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/notebook-user-path.png" alt-text="Screenshot of Notebooks in Azure Machine Learning with the prompt flow folder showing the files." lightbox = "./media/how-to-integrate-with-llm-app-devops/notebook-user-path.png":::

## Download and check in prompt flow code

To check in your flow into your code repository, you can export the flow folder from the flow authoring page to your local system. Select the download icon to download a ZIP package containing all the flow files to your local machine, which you can then check into your code repository or unzip to work with the files locally.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-export.png" alt-text="Screenshot showing the download icon in the Files explorer.":::

For more information about DevOps integration with Azure Machine Learning, see [Git integration for Azure Machine Learning](../concept-train-model-git-integration.md).

## Submit runs to the cloud from a local repository

You can complete the following procedure by using Azure CLI or the Python SDK. For more information, see the [pfazure](https://microsoft.github.io/promptflow/reference/pfazure-command-reference.html) prompt flow CLI documentation for Azure.

### Connect to your Azure Machine Learning workspace

# [Azure CLI](#tab/cli)

```sh
az login
```

# [Python SDK](#tab/python)

```python
import json

# Import required libraries
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# azure version promptflow apis
from promptflow.azure import PFClient

# Configure credential
try:
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
    credential = InteractiveBrowserCredential()

# Get a handle to workspace, it will use config.json in current and parent directory.
pf = PFClient.from_config(
    credential=credential,
)
```

---

### Upload the flow and create a run

# [Azure CLI](#tab/cli)

Prepare the *run.yml* file to define the configuration for this flow run in the cloud.

```yaml
$schema: https://azuremlschemas.azureedge.net/promptflow/latest/Run.schema.json
flow: <path_to_flow>
data: <path_to_flow>/data.jsonl

column_mapping:
  url: ${data.url}

# define cloud resource

# if using serverless compute type
# resources:
#   instance_type: <instance_type> 

# if using compute instance compute type
# resources:
#   compute: <compute_instance_name> 

# overrides connections 
connections:
  classify_with_llm:
    connection: <connection_name>
    deployment_name: <deployment_name>
  summarize_text_content:
    connection: <connection_name>
    deployment_name: <deployment_name>
```

You can specify the connection and deployment name for each tool in the flow. If you don't specify the connection and deployment name, the tool uses the one connection and deployment in the *flow.dag.yaml* file. Use the following code to format the connections:

```yaml
...
connections:
  <node_name>:
    connection: <connection_name>
      deployment_name: <deployment_name>
...

```

Create the *run.yml* file.

```sh
pfazure run create --file run.yml
```

# [Python SDK](#tab/python)

Load the flow, define resources and connections, and create the run.

```python
# load flow
flow = "<path_to_flow>"
data = "<path_to_flow>/data.jsonl"


# define cloud resource

# define instance type when using serverless compute type
# resources = {"instance_type": <instance_type>}

# specify the compute instance name when using compute instance compute type
# resources = {"compute": <compute_instance_name>}

# overrides connections 
connections = {"classify_with_llm":
                  {"connection": <connection_name>,
                  "deployment_name": <deployment_name>},
               "summarize_text_content":
                  {"connection": <connection_name>,
                  "deployment_name": <deployment_name>}
                }
# create run
run = Run(
    # local flow file
    flow=flow,
    # remote data
    data=data,
    column_mapping={
        "url": "${data.url}"
    }, 
    connections=connections, 
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

---

### Create an evaluation flow run

# [Azure CLI](#tab/cli)

Prepare the *run_evaluation.yml* to define the configuration for this evaluation flow run in the cloud.

```yaml
$schema: https://azuremlschemas.azureedge.net/promptflow/latest/Run.schema.json
flow: <path_to_flow>
data: <path_to_flow>/data.jsonl
run: <id of web-classification flow run>
column_mapping:
  groundtruth: ${data.answer}
  prediction: ${run.outputs.category}

# define cloud resource

# if using serverless compute type
# resources:
#   instance_type: <instance_type> 

# if using compute instance compute type
# resources:
#   compute: <compute_instance_name> 


# overrides connections 
connections:
  classify_with_llm:
    connection: <connection_name>
    deployment_name: <deployment_name>
  summarize_text_content:
    connection: <connection_name>
    deployment_name: <deployment_name>

```

```sh
pfazure run create --file run_evaluation.yml
```

# [Python SDK](#tab/python)

```python
# load flow
flow = "<path_to_flow>"
data = "<path_to_flow>/data.jsonl"

# define cloud resource

# define instance type when using serverless compute type
# resources = {"instance_type": <instance_type>}

# specify the compute instance name when using compute instance compute type
# resources = {"compute": <compute_instance_name>}

# overrides connections 
connections = {"classify_with_llm":
                  {"connection": <connection_name>,
                  "deployment_name": <deployment_name>},
               "summarize_text_content":
                  {"connection": <connection_name>,
                  "deployment_name": <deployment_name>}
                }

# create evaluation run
eval_run = Run(
    # local flow file
    flow=flow,
    # remote data
    data=data,
    run=base_run,
    column_mapping={
        "groundtruth": "${data.answer}",
        "prediction": "${run.outputs.category}",
    },
    connections=connections,
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

eval_run = pf.runs.create_or_update(run=eval_run)
```

---

### View run results in Azure Machine Learning workspace

Submit the flow run to the cloud to return the portal URL of the run. You can open the URL to view the run results in the portal.

You can also use following commands to view run results.

#### Stream the logs

# [Azure CLI](#tab/cli)

```sh
pfazure run stream --name <run_name>
```

# [Python SDK](#tab/python)

```python
pf.stream("<run_name>")
```

---

#### View run outputs

# [Azure CLI](#tab/cli)

```sh
pfazure run show-details --name <run_name>
```

# [Python SDK](#tab/python)

```python
details = pf.get_details(eval_run)
details.head(10)
```

---

#### View evaluation run metrics

# [Azure CLI](#tab/cli)

```sh
pfazure run show-metrics --name <evaluation_run_name>
```

# [Python SDK](#tab/python)

```python
pf.get_metrics("evaluation_run_name")
```
---

## Develop and test locally

During iterative development, as you refine and fine-tune your flow or prompts, you can carry out multiple iterations locally within your code repository. The VS Code community version, VS Code Prompt flow extension, and prompt flow local SDK and CLI facilitate pure local development and testing without Azure binding.

### VS Code Prompt flow extension

With the Prompt flow VS Code extension, you can easily author your flow locally in the VS Code editor with a similar UI experience as in the cloud.

To use the extension:

1. In VS Code with the Prompt flow extension enabled, open a prompt flow folder.
1. Open the *flow.dag.yaml* file and select the **Visual editor** link at the top of the file.
1. Use the editor to make any necessary changes to your flow, such as tuning the prompts in variants or adding more tools.
1. To test your flow, select the **Run** icon at the top of the visual editor to trigger a flow test.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/run-flow-visual-editor.png" alt-text="Screenshot of VS Code showing running the flow in the visual editor. " lightbox = "./media/how-to-integrate-with-llm-app-devops/run-flow-visual-editor.png":::

### Use the local prompt flow SDK and CLI

If you prefer to work directly with code, or use Jupyter, PyCharm, Visual Studio, or other integrated development environments (IDEs), you can directly modify the YAML code in the *flow.dag.yaml* file.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-directory-and-yaml.png" alt-text="Screenshot of a yaml file in VS Code highlighting the default input and flow directory. " lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-directory-and-yaml.png":::

You can then trigger a flow single run for testing using either the prompt flow CLI or SDK.

# [Azure CLI](#tab/cli)

To trigger a run from the working directory *\<sample-repo>/examples/flows/standard/\<directory-name>*, run the following code:

```sh
pf flow test --flow <directory-name>
```

The following screenshot shows the flow test logs and outputs.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-test-output-cli.png" alt-text="Screenshot of the flow test output in PowerShell." lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-test-output-cli.png":::

# [Python SDK](#tab/python)

The return value of the `test` function is the flow and node outputs.

```python
from promptflow import PFClient

pf_client = PFClient()

flow_path = "web-classification"  # "web-classification" is the directory name

# Test flow
flow_inputs = {"url": "https://www.youtube.com/watch?v=o5ZQyXaAv1g", "answer": "Channel", "evidence": "Url"}  # The inputs of the flow.
flow_result = pf_client.test(flow=flow_path, inputs=inputs)
print(f"Flow outputs: {flow_result}")

# Test node in the flow
node_name = "fetch_text_content_from_url"  # The node name in the flow.
node_inputs = {"url": "https://www.youtube.com/watch?v=o5ZQyXaAv1g"}  # The inputs of the node.
node_result = pf_client.test(flow=flow_path, inputs=node_inputs, node=node_name)
print(f"Node outputs: {node_result}")
```

The following screenshot shows the flow test logs and outputs.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-test-output.png" alt-text="Screenshot of the flow test output in Python. " lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-test-output.png":::

---

Working locally allows you to make and test changes quickly, without needing to update the main code repository each time. For more details and guidance on using the local versions, you can refer to the [Prompt flow](https://github.com/microsoft/promptflow) GitHub community.

### Go back to studio UI for continuous development

Once you're satisfied with the results of your local testing, you can repeat the procedure to [submit runs to the cloud from the local repository](#submit-runs-to-the-cloud-from-a-local-repository).

Alternatively, you can go back to the Azure Machine Learning studio UI and use the cloud resources and experience to make changes to your flow in the flow authoring page.

To continue developing and working with the most up-to-date versions of the flow files, access a terminal on the **Notebook** page and pull the latest changes of the flow files from your repository. Or, you can directly import a local flow folder as a new draft flow to seamlessly transition between local and cloud development.

:::image type="content" source="./media/how-to-integrate-with-llm-app-devops/flow-import-local-upload.png" alt-text="Screenshot of the create a new flow panel with upload to local highlighted. " lightbox = "./media/how-to-integrate-with-llm-app-devops/flow-import-local-upload.png":::

## CI/CD integration

### CI: Trigger flow runs in CI pipeline

Once you have successfully developed and tested your flow, and checked it in as the initial version, you're ready for the next tuning and testing iteration. At this stage, you can trigger flow runs, including batch testing and evaluation runs, using the prompt flow CLI. This could serve as an automated workflow in your Continuous Integration (CI) pipeline.

Throughout the lifecycle of your flow iterations, several operations can be automated:

- Running prompt flow after a Pull Request
- Running prompt flow evaluation to ensure results are high quality
- Registering of prompt flow models
- Deployment of prompt flow models

For a comprehensive guide on an end-to-end MLOps pipeline that executes a web classification flow, see [Set up end to end GenAIOps with prompt Flow and GitHub](how-to-end-to-end-llmops-with-prompt-flow.md), and the [GitHub demo project](https://github.com/Azure/llmops-gha-demo).

### CD: Continuous deployment

The last step to go to production is to deploy your flow as an online endpoint in Azure Machine Learning. This allows you to integrate your flow into your application and make it available for use.

For more information on how to deploy your flow, see [Deploy flows to Azure Machine Learning managed online endpoint for real-time inference with CLI and SDK](how-to-deploy-to-code.md).

## Collaborate on flow development in production

In the context of developing a LLM-based application with prompt flow, collaboration amongst team members is often essential. Team members might be engaged in the same flow authoring and testing, working on diverse facets of the flow or making iterative changes and enhancements concurrently.

Such collaboration necessitates an efficient and streamlined approach to sharing code, tracking modifications, managing versions, and integrating these changes into the final project.

The introduction of the prompt flow **SDK/CLI** and the **Visual Studio Code Extension** as part of the code experience of prompt flow facilitates easy collaboration on flow development within your code repository. It is advisable to utilize a cloud-based **code repository**, such as GitHub or Azure DevOps, for tracking changes, managing versions, and integrating these modifications into the final project.

### Best practices for collaborative development

1. Authoring and single testing your flow locally - Code repository and VSC Extension

    - The first step of this collaborative process involves using a code repository as the base for your project code, which includes the prompt flow code. 
        - This centralized repository enables efficient organization, tracking of all code changes, and collaboration among team members.
    - Once the repository is set up, team members can use the VSC extension for local authoring and single input testing of the flow.
        - This standardized integrated development environment fosters collaboration among multiple members working on different aspects of the flow.
        :::image type="content" source="media/how-to-integrate-with-llm-app-devops/prompt-flow-local-develop.png" alt-text="Screenshot of local development. " lightbox = "media/how-to-integrate-with-llm-app-devops/prompt-flow-local-develop.png":::
1. Cloud-based experimental batch testing and evaluation - prompt flow CLI/SDK and workspace portal UI
    - Following the local development and testing phase, flow developers can use the pfazure CLI or SDK to submit batch runs and evaluation runs from the local flow files to the cloud.
        - This action provides a way for cloud resource consuming, results to be stored persistently and managed efficiently with a portal UI in the Azure Machine Learning workspace. This step allows for cloud resource consumption including compute and storage and further endpoint for deployments.
        :::image type="content" source="media/how-to-integrate-with-llm-app-devops/pfazure-run.png" alt-text="Screenshot of pfazure command to submit run to cloud. " lightbox = "media/how-to-integrate-with-llm-app-devops/pfazure-run.png":::
    - Post submissions to cloud, team members can access the cloud portal UI to view the results and manage the experiments efficiently.
        - This cloud workspace provides a centralized location for gathering and managing all the runs history, logs, snapshots, comprehensive results including the instance level inputs and outputs.
        :::image type="content" source="media/how-to-integrate-with-llm-app-devops/pfazure-run-snapshot.png" alt-text="Screenshot of cloud run snapshot. " lightbox = "media/how-to-integrate-with-llm-app-devops/pfazure-run-snapshot.png":::
        - In the run list that records all run history from during the development, team members can easily compare the results of different runs, aiding in quality analysis and necessary adjustments.
        :::image type="content" source="media/how-to-integrate-with-llm-app-devops/cloud-run-list.png" alt-text="Screenshot of run list in workspace. " lightbox = "media/how-to-integrate-with-llm-app-devops/cloud-run-list.png":::
        :::image type="content" source="media/how-to-integrate-with-llm-app-devops/cloud-run-compare.png" alt-text="Screenshot of run comparison in workspace. " lightbox = "media/how-to-integrate-with-llm-app-devops/cloud-run-compare.png":::
1. Local iterative development or one-step UI deployment for production
    - Following the analysis of experiments, team members can return to the code repository for another development and fine-tuning. Subsequent runs can then be submitted to the cloud in an iterative manner. 
        - This iterative approach ensures consistent enhancement until the team is satisfied with the quality ready for production.
    - Once the team is fully confident in the quality of the flow, it can be seamlessly deployed via a UI wizard as an online endpoint in Azure Machine Learning. Once the team is entirely confident in the flow's quality, it can be seamlessly transitioned into production via a UI deploy wizard as an online endpoint in a robust cloud environment.
        - This deployment on an online endpoint can be based on a run snapshot, allowing for stable and secure serving, further resource allocation and usage tracking, and log monitoring in the cloud.
        :::image type="content" source="media/how-to-integrate-with-llm-app-devops/deploy-from-snapshot.png" alt-text="Screenshot of deploying flow from a run snapshot. " lightbox = "media/how-to-integrate-with-llm-app-devops/deploy-from-snapshot.png":::
        :::image type="content" source="media/how-to-integrate-with-llm-app-devops/deploy-wizard.png" alt-text="Screenshot of deploy wizard. " lightbox = "media/how-to-integrate-with-llm-app-devops/deploy-wizard.png":::

### Why we recommend using the code repository for collaborative development
For iterative development, a combination of a local development environment and a version control system, such as Git, is typically more effective. You can make modifications and test your code locally, then commit the changes to Git. This creates an ongoing record of your changes and offers the ability to revert to earlier versions if necessary.

When **sharing flows** across different environments is required, using a cloud-based code repository like GitHub or Azure Repos is advisable. This enables you to access the most recent version of your code from any location and provides tools for collaboration and code management.

By following this best practice, teams can create a seamless, efficient, and productive collaborative environment for prompt flow development.

## Next steps

- [Set up end-to-end GenAIOps with prompt flow and GitHub](how-to-end-to-end-llmops-with-prompt-flow.md)
- [Prompt flow CLI documentation for Azure](https://microsoft.github.io/promptflow/reference/pfazure-command-reference.html)
