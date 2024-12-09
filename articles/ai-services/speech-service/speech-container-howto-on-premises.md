---
title: Use Speech service containers with Kubernetes and Helm
titleSuffix: Azure AI services
description: Using Kubernetes and Helm to define the speech to text and text to speech container images, we create a Kubernetes package. This package is deployed to a Kubernetes cluster on-premises.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 9/24/2024
ms.author: eur
#Customer intent: As a developer, I want to learn how to use Speech service containers with Kubernetes and Helm.
---

# Use Speech service containers with Kubernetes and Helm

One option to manage your Speech containers on-premises is to use Kubernetes and Helm. Using Kubernetes and Helm to define the speech to text and text to speech container images, we create a Kubernetes package. This package is deployed to a Kubernetes cluster on-premises. Finally, we explore how to test the deployed services and various configuration options. For more information about running Docker containers without Kubernetes orchestration, see [install and run Speech service containers](speech-container-howto.md).

## Prerequisites

The following prerequisites before using Speech containers on-premises:

| Required | Purpose |
|----------|---------|
| Azure Account | If you don't have an Azure subscription, create a [free account][free-azure-account] before you begin. |
| Container Registry access | In order for Kubernetes to pull the docker images into the cluster, it needs access to the container registry. |
| Kubernetes CLI | The [Kubernetes CLI][kubernetes-cli] is required for managing the shared credentials from the container registry. Kubernetes is also needed before Helm, which is the Kubernetes package manager. |
| Helm CLI | Install the [Helm CLI][helm-install], which is used to install a helm chart (container package definition). |
|Speech resource |In order to use these containers, you must have:<br><br>A _Speech_ Azure resource to get the associated billing key and billing endpoint URI. Both values are available on the Azure portal's **Speech** Overview and Keys pages and are required to start the container.<br><br>**{API_KEY}**: resource key<br><br>**{ENDPOINT_URI}**: endpoint URI example is: `https://eastus.api.cognitive.microsoft.com/sts/v1.0`|

## The recommended host computer configuration

Refer to the [Speech service container host computer][speech-container-host-computer] details as a reference. This *helm chart* automatically calculates CPU and memory requirements based on how many decodes (concurrent requests) that the user specifies. Additionally, it adjusts based on whether optimizations for audio/text input are configured as `enabled`. The helm chart defaults to, two concurrent requests and disabling optimization.

| Service | CPU / Container | Memory / Container |
|--|--|--|
| **speech to text** | one decoder requires a minimum of 1,150 millicores. If the `optimizedForAudioFile` is enabled, then 1,950 millicores are required. (default: two decoders) | Required: 2 GB<br>Limited:  4 GB |
| **text to speech** | one concurrent request requires a minimum of 500 millicores. If the `optimizeForTurboMode` is enabled, then 1,000 millicores are required. (default: two concurrent requests) | Required: 1 GB<br> Limited: 2 GB |

## Connect to the Kubernetes cluster

The host computer is expected to have an available Kubernetes cluster. See this tutorial on [deploying a Kubernetes cluster](/azure/aks/tutorial-kubernetes-deploy-cluster) for a conceptual understanding of how to deploy a Kubernetes cluster to a host computer.

## Configure Helm chart values for deployment

Visit the [Microsoft Helm Hub][ms-helm-hub] for all the publicly available helm charts offered by Microsoft. From the Microsoft Helm Hub, you find the **Azure AI Speech On-Premises Chart**. The **Azure AI Speech On-Premises** is the chart we install, but we must first create an `config-values.yaml` file with explicit configurations. Let's start by adding the Microsoft repository to our Helm instance.

```console
helm repo add microsoft https://microsoft.github.io/charts/repo
```

Next, we configure our Helm chart values. Copy and paste the following YAML into a file named `config-values.yaml`. For more information on customizing the **Azure AI Speech On-Premises Helm Chart**, see [customize helm charts](#customize-helm-charts). Replace the `# {ENDPOINT_URI}` and `# {API_KEY}` comments with your own values.

```yaml
# These settings are deployment specific and users can provide customizations
# speech to text configurations
speechToText:
  enabled: true
  numberOfConcurrentRequest: 3
  optimizeForAudioFile: true
  image:
    registry: mcr.microsoft.com
    repository: azure-cognitive-services/speechservices/speech-to-text
    tag: latest
    pullSecrets:
      - mcr # Or an existing secret
    args:
      eula: accept
      billing: # {ENDPOINT_URI}
      apikey: # {API_KEY}

# text to speech configurations
textToSpeech:
  enabled: true
  numberOfConcurrentRequest: 3
  optimizeForTurboMode: true
  image:
    registry: mcr.microsoft.com
    repository: azure-cognitive-services/speechservices/neural-text-to-speech
    tag: latest
    pullSecrets:
      - mcr # Or an existing secret
    args:
      eula: accept
      billing: # {ENDPOINT_URI}
      apikey: # {API_KEY}
```

> [!IMPORTANT]
> If the `billing` and `apikey` values are not provided, the services will expire after 15 min. Likewise, verification will fail as the services will not be available.

### The Kubernetes package (Helm chart)

The *Helm chart* contains the configuration of which docker image(s) to pull from the `mcr.microsoft.com` container registry.

> A [Helm chart][helm-charts] is a collection of files that describe a related set of Kubernetes resources. A single chart might be used to deploy something simple, like a memcached pod, or something complex, like a full web app stack with HTTP servers, databases, caches, and so on.

The provided *Helm charts* pull the docker images of the Speech service, both text to speech and the speech to text services from the `mcr.microsoft.com` container registry.

## Install the Helm chart on the Kubernetes cluster

Run the [`helm install`][helm-install-cmd] command to install the helm chart, replacing the `<config-values.yaml>` with the appropriate path and file name argument. The `microsoft/cognitive-services-speech-onpremise` Helm chart is available on the [Microsoft Helm Hub][ms-helm-hub-speech-chart].

```console
helm install onprem-speech microsoft/cognitive-services-speech-onpremise \
    --version 0.1.1 \
    --values <config-values.yaml> 
```

Here's an example output you might expect to see from a successful install execution:

```console
NAME:   onprem-speech
LAST DEPLOYED: Tue Jul  2 12:51:42 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Pod(related)
NAME                             READY  STATUS             RESTARTS  AGE
speech-to-text-7664f5f465-87w2d  0/1    Pending            0         0s
speech-to-text-7664f5f465-klbr8  0/1    ContainerCreating  0         0s
neural-text-to-speech-56f8fb685b-4jtzh  0/1    ContainerCreating  0         0s
neural-text-to-speech-56f8fb685b-frwxf  0/1    Pending            0         0s

==> v1/Service
NAME            TYPE          CLUSTER-IP    EXTERNAL-IP  PORT(S)       AGE
speech-to-text  LoadBalancer  10.0.252.106  <pending>    80:31811/TCP  1s
neural-text-to-speech  LoadBalancer  10.0.125.187  <pending>    80:31247/TCP  0s

==> v1beta1/PodDisruptionBudget
NAME                                MIN AVAILABLE  MAX UNAVAILABLE  ALLOWED DISRUPTIONS  AGE
speech-to-text-poddisruptionbudget  N/A            20%              0                    1s
neural-text-to-speech-poddisruptionbudget  N/A            20%              0                    1s

==> v1beta2/Deployment
NAME            READY  UP-TO-DATE  AVAILABLE  AGE
speech-to-text  0/2    2           0          0s
neural-text-to-speech  0/2    2           0          0s

==> v2beta2/HorizontalPodAutoscaler
NAME                       REFERENCE                  TARGETS        MINPODS  MAXPODS  REPLICAS  AGE
speech-to-text-autoscaler  Deployment/speech-to-text  <unknown>/50%  2        10       0         0s
neural-text-to-speech-autoscaler  Deployment/neural-text-to-speech  <unknown>/50%  2        10       0         0s


NOTES:
cognitive-services-speech-onpremise has been installed!
Release is named onprem-speech
```

The Kubernetes deployment can take over several minutes to complete. To confirm that both pods and services are properly deployed and available, execute the following command:

```console
kubectl get all
```

You should expect to see something similar to the following output:

```console
NAME                                  READY     STATUS    RESTARTS   AGE
pod/speech-to-text-7664f5f465-87w2d   1/1       Running   0          34m
pod/speech-to-text-7664f5f465-klbr8   1/1       Running   0          34m
pod/neural-text-to-speech-56f8fb685b-4jtzh   1/1       Running   0          34m
pod/neural-text-to-speech-56f8fb685b-frwxf   1/1       Running   0          34m

NAME                     TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)        AGE
service/kubernetes       ClusterIP      10.0.0.1       <none>           443/TCP        3h
service/speech-to-text   LoadBalancer   10.0.252.106   52.162.123.151   80:31811/TCP   34m
service/neural-text-to-speech   LoadBalancer   10.0.125.187   65.52.233.162    80:31247/TCP   34m

NAME                             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/speech-to-text   2         2         2            2           34m
deployment.apps/neural-text-to-speech   2         2         2            2           34m

NAME                                        DESIRED   CURRENT   READY     AGE
replicaset.apps/speech-to-text-7664f5f465   2         2         2         34m
replicaset.apps/neural-text-to-speech-56f8fb685b   2         2         2         34m

NAME                                                            REFERENCE                   TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
horizontalpodautoscaler.autoscaling/speech-to-text-autoscaler   Deployment/speech-to-text   1%/50%    2         10        2          34m
horizontalpodautoscaler.autoscaling/neural-text-to-speech-autoscaler   Deployment/neural-text-to-speech   0%/50%    2         10        2          34m
```

### Verify Helm deployment with Helm tests

The installed Helm charts define *Helm tests*, which serve as a convenience for verification. These tests validate service readiness. To verify both speech to text and text to speech features, we execute the [Helm test][helm-test] command.

```console
helm test onprem-speech
```

> [!IMPORTANT]
> These tests will fail if the POD status is not `Running` or if the deployment is not listed under the `AVAILABLE` column. Be patient as this can take over ten minutes to complete.

These tests output various status results:

```console
RUNNING: speech to text-readiness-test
PASSED: speech to text-readiness-test
RUNNING: text to speech-readiness-test
PASSED: text to speech-readiness-test
```

As an alternative to executing the *helm tests*, you could collect the *External IP* addresses and corresponding ports from the `kubectl get all` command. Using the IP and port, open a web browser and navigate to `http://<external-ip>:<port>:/swagger/index.html` to view the API swagger page(s).

## Customize Helm charts

Helm charts are hierarchical. Being hierarchical allows for chart inheritance, it also caters to the concept of specificity, where settings that are more specific override inherited rules.

[!INCLUDE [Speech umbrella-helm-chart-config](includes/speech-umbrella-helm-chart-config.md)]

[!INCLUDE [Speech to text Helm Chart Config](includes/speech-to-text-chart-config.md)]

[!INCLUDE [Text to speech Helm Chart Config](includes/text-to-speech-chart-config.md)]

## Next steps

For more details on installing applications with Helm in Azure Kubernetes Service (AKS), [visit here][installing-helm-apps-in-aks].

> [!div class="nextstepaction"]
> [Azure AI containers][cog-svcs-containers]

<!-- LINKS - external -->
[free-azure-account]: https://azure.microsoft.com/free
[git-download]: https://git-scm.com/downloads
[azure-cli]: /cli/azure/install-azure-cli
[docker-engine]: https://www.docker.com/products/docker-engine
[kubernetes-cli]: https://kubernetes.io/docs/tasks/tools/install-kubectl
[helm-install]: https://helm.sh/docs/intro/install/
[helm-install-cmd]: https://helm.sh/docs/intro/using_helm/#helm-install-installing-a-package
[tiller-install]: https://helm.sh/docs/install/#installing-tiller
[helm-charts]: https://helm.sh/docs/topics/charts/
[kubectl-create]: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#create
[kubectl-get]: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get
[helm-test]: https://v2.helm.sh/docs/helm/#helm-test
[ms-helm-hub]: https://artifacthub.io/packages/search?repo=microsoft
[ms-helm-hub-speech-chart]: https://hub.helm.sh/charts/microsoft/cognitive-services-speech-onpremise

<!-- LINKS - internal -->
[speech-container-host-computer]: speech-container-howto.md#host-computer-requirements-and-recommendations
[installing-helm-apps-in-aks]: /azure/aks/kubernetes-helm
[cog-svcs-containers]: ../cognitive-services-container-support.md
