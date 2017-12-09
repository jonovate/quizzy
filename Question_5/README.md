# Question 5
> *Microservices:* testing Docker, Kubernetes. Deploy and explain each of the below.
>
>   5.1. Docker: install and deploy the SMACK Stack, and highlight an example: <https://hub.docker.com/r/omrison/smack-stack/>, <http://datastrophic.io/data-processing-platforms-architectures-with-spark-mesos-akka-cassandra-and-kafka/>.
>
>   5.2. Kubernetes: getting started, <https://blog.codeship.com/getting-started-with-kubernetes/>

## Solution

### Docker

SMACK is Spark (processing of ingested and digested stream data), Mesos (resource/cluster management, hold the workers for all the components), Akka (model, ingestion tool for stream data, handling event processing out of the stack -- also seen it used for reading data out of Cassandra), Cassandra (storage), Kafka (streaming data, decouple ingestion from processing)

Can be thought of as Mini DataLake solution with no real ETL capabilities.

**The SMACK stack is not on Docker Hub, so cannot run it**
*If time was infinite, could create own docker-compose file but that would be 1-2 day effort to fully learn & test everything.*

SMACK can be seen as a pattern for handling both real-time analysis of a stream of data coming into the system, along with triggering events accordingly when a certain condition is detected. A use case could be sending product view information from an ecommerce site: tracking how many views and which users (IP address or username). If we detect that a user has now viewed the page X times over Y days, we could fire an event to the ecommerce site to show a Limited Time discount to the User. Whether the user converted would of course be tracked as well (..could lend itself to A/B testing also).

### Kubernetes

A container management and cluster orchestration system which Google open-sourced from their internal Borg.
Docker Inc. has competing product called Swarm.

Kubernetes is concept of Master/Worker model. Master has a Controller, Scheduler, API Services, and etcd for configuration across cluster.
The workers are Nodes, where it contains a container runtime resources with groupings of Pods where the containers themselves actually ran.
Kubernetes also has concept of a Replica Set, which is a defined layout of pods/nodes.  This seems to be similar to Docker Stacks.

Most recent, recommended guide: <https://kubernetes.io/docs/getting-started-guides/minikube/>

*Unfortunately for this commit, I am running Windows and ran out of time to install VirtualBox to setup cluster on a Linux box. Basically once Cluster is running in VirtualBox, I would then use kubectl on Windows to manage it.*
