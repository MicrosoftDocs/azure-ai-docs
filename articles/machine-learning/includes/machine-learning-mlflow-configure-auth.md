---
author: santiagxf
ms.service: azure-machine-learning
ms.topic: include
ms.date: 11/20/2024
ms.author: fasantia
---

For interactive jobs where there's a user connected to the session, you can rely on interactive authentication. No further action is required.

> [!WARNING]
> *Interactive browser* authentication blocks code execution when it prompts for credentials. This approach isn't suitable for authentication in unattended environments like training jobs. We recommend that you configure a different authentication mode in those environments.

For scenarios that require unattended execution, you have to configure a service principal to communicate with Azure Machine Learning.

# [MLflow SDK](#tab/mlflow)

```python
import os

os.environ["AZURE_TENANT_ID"] = "<Azure-tenant-ID>"
os.environ["AZURE_CLIENT_ID"] = "<Azure-client-ID>"
os.environ["AZURE_CLIENT_SECRET"] = "<Azure-client-secret>"
```

# [Environment variables](#tab/environ)

```bash
export AZURE_TENANT_ID="<Azure-tenant-ID>"
export AZURE_CLIENT_ID="<Azure-client-ID>"
export AZURE_CLIENT_SECRET="<Azure-client-secret>"
```

---

> [!TIP]
> When you work in shared environments, we recommend that you configure these environment variables at the compute level. As a best practice, manage them as secrets in an instance of Azure Key Vault.
>
> For instance, in Azure Databricks you can use secrets in environment variables as follows in the cluster configuration: `AZURE_CLIENT_SECRET={{secrets/<scope-name>/<secret-name>}}`. For more information about implementing this approach in Azure Databricks, see [Reference a secret in an environment variable](/azure/databricks/security/secrets/secrets#reference-a-secret-in-an-environment-variable), or refer to documentation for your platform.
