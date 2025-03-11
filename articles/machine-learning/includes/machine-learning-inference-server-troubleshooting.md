---
author: shohei1029
ms.service: azure-machine-learning
ms.topic: include
ms.date: 01/06/2025
ms.author: shnagata
---

<a name="frequently-asked-questions"></a>
### Check installed packages

Follow these steps to address issues with installed packages:

1. Gather information about installed packages and versions for your Python environment.

1. In your environment file, check the version of the `azureml-inference-server-http` Python package that's specified. In the Azure Machine Learning inference HTTP server [startup logs](../how-to-inference-server-http.md#view-startup-logs), check the version of the inference server that's displayed. Confirm that the two versions match.

   In some cases, the pip dependency resolver installs unexpected package versions. You might need to run `pip` to correct installed packages and versions.

1. If you specify Flask or its dependencies in your environment, remove these items.

   - Dependent packages include `flask`, `jinja2`, `itsdangerous`, `werkzeug`, `markupsafe`, and `click`.
   - The `flask` package is listed as a dependency in the inference server package. The best approach is to allow the inference server to install the `flask` package.
   - When the inference server is configured to support new versions of Flask, the inference server automatically receives the package updates as they become available.

### Check the inference server version

The `azureml-inference-server-http` server package is published to PyPI. The [PyPI page](https://pypi.org/project/azureml-inference-server-http/) lists the changelog and all versions of the package.

If you use an early package version, update your configuration to the latest version. The following table summarizes stable versions, common issues, and recommended adjustments:

| Package version | Description | Issue | Resolution |
| --- | --- | --- | --- |
| 0.4.x | Bundled in training images dated `20220601` or earlier and `azureml-defaults` package versions 0.1.34 through 1.43. Latest stable version is 0.4.13. | For server versions earlier than 0.4.11, you might encounter Flask dependency issues, such as `can't import name Markup from jinja2`. | Upgrade to version 0.4.13 or 1.4.x, the latest version, if possible. |
| 0.6.x | Preinstalled in inferencing images dated `20220516` and earlier. Latest stable version is 0.6.1. | N/A | N/A |
| 0.7.x | Supports Flask 2. Latest stable version is 0.7.7. | N/A | N/A |
| 0.8.x | Uses an updated log format. Ends support for Python 3.6. | N/A | N/A |
| 1.0.x | Ends support for Python 3.7. | N/A | N/A |
| 1.1.x | Migrates to `pydantic` 2.0. | N/A | N/A |
| 1.2.x | Adds support for Python 3.11. Updates `gunicorn` to version 22.0.0. Updates `werkzeug` to version 3.0.3 and later versions. | N/A | N/A |
| 1.3.x | Adds support for Python 3.12. Upgrades `certifi` to version 2024.7.4. Upgrades `flask-cors` to version 5.0.0. Upgrades the `gunicorn` and `pydantic` packages. | N/A | N/A |
| 1.4.x | Upgrades `waitress` to version 3.0.1. Ends support for Python 3.8. Removes the compatibility layer that prevents the Flask 2.0 upgrade from breaking request object code. | If you depend on the compatibility layer, your request object code might not work. | Migrate your score script to Flask 2. |

### Check package dependencies

The most relevant dependent packages for the `azureml-inference-server-http` server package include:

- `flask`
- `opencensus-ext-azure`
- `inference-schema`
  
If you specify the `azureml-defaults` package in your Python environment, the `azureml-inference-server-http` package is a dependent package. The dependency is installed automatically.

> [!TIP]
> If you use the Azure Machine Learning SDK for Python v1 and don't explicitly specify the `azureml-defaults` package in your Python environment, the SDK might automatically add the package. However, the package version is locked relative to the SDK version. For example, if the SDK version is 1.38.0, the `azureml-defaults==1.38.0` entry is added to the environment's pip requirements.

### TypeError during inference server startup

You might encounter the following `TypeError` during inference server startup:

```bash
TypeError: register() takes 3 positional arguments but 4 were given

  File "/var/azureml-server/aml_blueprint.py", line 251, in register

    super(AMLBlueprint, self).register(app, options, first_registration)

TypeError: register() takes 3 positional arguments but 4 were given
```

This error occurs when you have Flask 2 installed in your Python environment, but your `azureml-inference-server-http` package version doesn't support Flask 2. Support for Flask 2 is available in the `azureml-inference-server-http` 0.7.0 package and later versions, and the `azureml-defaults` 1.44 package and later versions.

- If you don't use the Flask 2 package in an Azure Machine Learning Docker image, use the latest version of the `azureml-inference-server-http` or `azureml-defaults` package.
- If you use the Flask 2 package in an Azure Machine Learning Docker image, confirm that the image build version is `July 2022` or later.

  You can find the image version in the container logs. For example, see the following log statements:

  ```console
  2022-08-22T17:05:02,147738763+00:00 | gunicorn/run | AzureML Container Runtime Information
  2022-08-22T17:05:02,161963207+00:00 | gunicorn/run | ###############################################
  2022-08-22T17:05:02,168970479+00:00 | gunicorn/run | 
  2022-08-22T17:05:02,174364834+00:00 | gunicorn/run | 
  2022-08-22T17:05:02,187280665+00:00 | gunicorn/run | AzureML image information: openmpi4.1.0-ubuntu20.04, Materialization Build:20220708.v2
  2022-08-22T17:05:02,188930082+00:00 | gunicorn/run | 
  2022-08-22T17:05:02,190557998+00:00 | gunicorn/run | 
  ```

  The build date of the image appears after the `Materialization Build` notation. In the preceding example, the image version is `20220708`, or July 8, 2022. The image in this example is compatible with Flask 2.

  If you don't see a similar message in your container log, your image is out-of-date and should be updated. If you use a Compute Unified Device Architecture (CUDA) image and you can't find a newer image, check the [AzureML-Containers](https://github.com/Azure/AzureML-Containers) repo to see whether your image is deprecated. You can find designated replacements for deprecated images.

  If you use the inference server with an online endpoint, you can also find the logs in Azure Machine Learning studio. On the page for your endpoint, select the **Logs** tab.

If you deploy with the SDK v1 and don't explicitly specify an image in your deployment configuration, the inference server applies the `openmpi4.1.0-ubuntu20.04` package with a version that matches your local SDK toolset. However, the installed version might not be the latest available version of the image.

For SDK version 1.43, the inference server installs the `openmpi4.1.0-ubuntu20.04:20220616` package version by default, but this package version isn't compatible with SDK 1.43. Make sure you use the latest SDK for your deployment.

If you can't update the image, you can temporarily avoid the issue by pinning the `azureml-defaults==1.43` or `azureml-inference-server-http~=0.4.13` entries in your environment file. These entries direct the inference server to install the older version with `flask 1.0.x`.

### ImportError or ModuleNotFoundError during inference server startup

You might encounter an `ImportError` or `ModuleNotFoundError` on specific modules, such as  `opencensus`, `jinja2`, `markupsafe`, or `click`, during inference server startup. The following example shows the error message:

```bash
ImportError: cannot import name 'Markup' from 'jinja2'
```

The import and module errors occur when you use version 0.4.10 or earlier versions of the inference server that don't pin the Flask dependency to a compatible version. To prevent the issue, install a later version of the inference server.
