#!/usr/bin/env python
import random
from kubernetes import client, config, watch
import logging

# Load kubeconfig
config.load_incluster_config()

# Initialize Kubernetes API client
v1 = client.CoreV1Api()

# Scheduler name
scheduler_name = "my-scheduler"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)


def nodes_available():
    """
    Get a list of available nodes that are in the "Ready" state.
    """
    ready_nodes = []
    for node in v1.list_node().items:
        if "control-plane" in node.metadata.name:
            continue
        for condition in node.status.conditions:
            if condition.type == "Ready" and condition.status == "True":
                ready_nodes.append(node.metadata.name)
    return ready_nodes


def schedule_pod(name, node, namespace="default"):
    try:
        logging.info(f"binding to node -> {node}")
        target = client.V1ObjectReference(
            kind="Node", api_version="v1", name=node, namespace=namespace
        )
        meta = client.V1ObjectMeta(name=name)
        body = client.V1Binding(target=target, metadata=meta)
        return v1.create_namespaced_pod_binding(
            name, namespace, body, _preload_content=False
        )
    except Exception as e:
        logging.error(f"Exception -> scheduler \n{e}")


def main():
    """
    Main function to watch for pending pods and schedule them to random nodes.
    """
    logging.info("Random Scheduler is running...")
    w = watch.Watch()
    for event in w.stream(v1.list_pod_for_all_namespaces):
        pod = event["object"]
        # Check if the pod is pending and assigned to this scheduler
        if (
            pod.status.phase == "Pending"
            and pod.spec.scheduler_name == scheduler_name
            and not pod.spec.node_name
        ):
            pod_name = pod.metadata.name
            namespace = pod.metadata.namespace
            # Get available nodes
            nodes = nodes_available()
            if nodes:
                # Select a random node
                selected_node = random.choice(nodes)
                # Schedule the pod to the selected node
                schedule_pod(pod_name, selected_node, namespace)
            else:
                logging.warning("No available nodes to schedule the pod.")


if __name__ == "__main__":
    main()
