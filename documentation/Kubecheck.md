This section provides information about the Kubecheck functionality.

- [Procedure Execution From CLI](#procedure-execution-from-cli)
- [Check Procedures](#check-procedures)
  - [IAAS Procedure](#iaas-procedure)
    - [001 Connectivity](#001-connectivity)
    - [002 Latency - Single Thread](#002-latency-single-thread)
    - [003 Latency - Multi Thread](#003-latency-multi-thread)
    - [004 Sudoer Access](#004-sudoer-access)
    - [005 Items Amount](#005-items-amount)
      - [005 VIPs Amount](#005-vips-amount)
      - [005 Balancers Amount](#005-balancers-amount)
      - [005 Masters Amount](#005-masters-amount)
      - [005 Workers Amount](#005-workers-amount)
      - [005 Total Nodes Amount](#005-total-nodes-amount)
    - [006 VCPUs Amount](#006-vcpus-amount)
      - [006 VCPUs Amount - Balancers](#006-vcpus-amount-balancers)
      - [006 VCPUs Amount - Masters](#006-vcpus-amount-masters)
      - [006 VCPUs Amount - Workers](#006-vcpus-amount-workers)
    - [007 RAM Amount](#007-ram-amount)
      - [007 RAM Amount - Balancers](#007-ram-amount-balancers)
      - [007 RAM Amount - Masters](#007-ram-amount-masters)
      - [007 RAM Amount - Workers](#007-ram-amount-workers)
    - [008 Distributive](#008-distributive)
  - [PAAS Procedure](#paas-procedure)
    - [201 Service Status](#201-service-status)
      - [201 Haproxy Status](#201-haproxy-status)
      - [201 Keepalived Status](#201-keepalived-status)
      - [201 Container Runtime Status](#201-container-runtime-status)
      - [201 Kubelet Status](#201-kubelet-status)
    - [202 Kubelet Version](#202-kubelet-version)
    - [203 Recommended packages versions](#203-recommended-packages-version)  
    - [204 Docker Version](#204-cri-versions)
    - [204 HAproxy Version](#204-haproxy-version)
    - [204 Keepalived Version](#204-keepalived-version)
    - [205 Generic Packages Version](#205-generic-packages-version)
    - [206 Pods Condition](#206-pods-condition)
    - [207 Dashboard Availability](#207-dashboard-availability)
    - [208 Nodes Existence](#208-nodes-existence)
    - [209 Nodes Roles](#209-nodes-roles)
    - [210 Nodes Condition](#210-nodes-condition)
      - [210 Nodes Condition - NetworkUnavailable](#210-nodes-condition-networkunavailable)
      - [210 Nodes Condition - MemoryPressure](#210-nodes-condition-memorypressure)
      - [210 Nodes Condition - DiskPressure](#210-nodes-condition-diskpressure)
      - [210 Nodes Condition - PIDPressure](#210-nodes-condition-pidpressure)
      - [210 Nodes Condition - Ready](#210-nodes-condition-ready)
- [Report File Generation](#report-file-generation)
  - [HTML Report](#html-report)
  - [CSV Report](#csv-report)


# Kubernetes Check

The Kubernetes Check procedure provides an opportunity to automatically verify the environment and quickly get a report on the results. The environment is checked against the following criteria, which is defined in advance:

* Minimal - The minimum results that the test environment must meet. If it does not satisfy this, there is no guarantee that this environment will be operational.
* Recommended - The recommended results in which the test development environment for the Full-HA cluster scheme showed the best results and performance. If you have a production environment, you must independently calculate the number of resources for your cluster. This number is more than that recommended by the Kubernetes Check procedure.

If the detected test results deviate from the criteria, the following status types are assigned to them:

* **OK** - This status indicates the compliance with the recommended values, if any, and successful completion of the test without errors.
* **WARN** - This status indicates that the test deviated slightly from the expected values. For example, the results found do not correspond to the recommended values. However, this test passed the minimum requirements and has not failed.
* **FAIL** - This status indicates that the test does not meet the minimum requirements or it has failed. This test requires attention to fix the environment.
* **ERROR?** - This status indicates that an internal error occurred in the test and it cannot be continued.

At the end of the logs of the procedure, a summary report table with all the test results is displayed. For example:

```
           Group    Status   ID    Test                                                               Actual result        Minimal   Recommended
 
             SSH      OK     001  Connectivity .......................................................... Connected                             
             SSH     WARN    002  Latency - Single Thread .................................................. 1500ms          10000          1000
             SSH     FAIL    003  Latency - Multi Thread .................................................. 50000ms          15000          2000   

 OVERALL RESULTS:  1 SUCCEEDED   1 WARNED   1 FAILED  
```

The following columns are presented in this table:

* Group - The logical group of checks to which the test belongs.
* Status - The final status assigned to the test according to the results of the check.
* ID - The test identifier.
* Name - The short test name.
* Actual result - The actual value detected by the test on the environment.
* Minimal (optional) - The minimum required value for this test.
* Recommended (optional) - The recommended required value for this test.

The final report is generated in a file. For more information, see [Report File Generation](#report-file-generation).

### Procedure Execution From CLI

Check procedure execution form CLI can be started with the following command:

```bash
./kubetools check %{CHECK_TYPE}
./kubetools check iaas
./kubetools check paas
```

It begins the execution of all tasks available in the procedure in accordance with the procedure type. For more information about how a tasks list can be redefined, see [Tasks List Redefinition](/documentation/public/Installation.md#tasks-list-redefinition) in _Kubetools Installation Procedure_.

### Check Procedures

A check procedure is divided into logical sub-procedures. Each of them is responsible for its own set of tests conducted on the environment.

#### IAAS Procedure

The IAAS procedure verifies only the infrastructure. For example, it checks the amount of hardware resources or checks the speed of the environment. These tests do not perform cluster checks and are intended to be performed both on a completely empty environment and an environment with the cluster installed.

The task tree is as follows:

* ssh
  * connectivity
  * latency
    * single
    * multiple
  * sudoer_access
* network
  * pod_subnet_connectivity
  * service_subnet_connectivity
  * check_tcp_ports
* hardware
  * members_amount
    * vips
    * balancers
    * masters
    * workers
    * total
  * cpu
    * balancers
    * masters
    * workers
  * ram
    * balancers
    * masters
    * workers
* system
  * distributive

##### 001 Connectivity

*Task*: `ssh.connectivity`

This test checks whether it is possible to establish the SSH-connection with nodes. If you are unable to connect to the nodes, check and fix the following:

* The credentials for the connection are correct (verify the ip address, user, and key).
* The node is up.
* The node is online.
* The network connection to the node is available.
* The node port 22 (or other custom, if configured) is open and can be binded.
* The SSHD is running and its configuration is correct. 

##### 002 Latency - Single Thread

*Task*: `ssh.latency.single`

This test checks the delay between the nodes in the single-threaded mode. The test of the nodes passes one after another.

##### 003 Latency - Multi Thread

*Task*: `ssh.latency.multiple`

This test checks the delay between the nodes in the multi-threaded mode. The test of all nodes passes at the same time.

##### 004 Sudoer Access

*Task*: `ssh.sudoer_access`

##### 005 Items Amount

Tests of this type check the availability of the required amount of resources.

###### 005 VIPs Amount

*Task*: `hardware.members_amount.vips`

This test checks the number of VIPs present for Keepalived.

###### 005 Balancers Amount

*Task*: `hardware.members_amount.balancers`

This test checks the number of nodes present with the `balancer` role.

###### 005 Masters Amount

*Task*: `hardware.members_amount.masters`

This test checks the number of nodes present with the `master` role.

###### 005 Workers Amount

*Task*: `hardware.members_amount.workers`

This test checks the number of nodes present with the `worker` role.

###### 005 Total Nodes Amount

*Task*: `hardware.members_amount.total`

This test checks the number of all the nodes present.

##### 006 VCPUs Amount

Tests of this type check the availability of the required number of processors.

###### 006 VCPUs Amount - Balancers

*Task*: `hardware.cpu.balancers`

This test checks the number of processors on the nodes with the `balancer` role.

###### 006 VCPUs Amount - Masters

*Task*: `hardware.cpu.masters`

This test checks the number of processors on the nodes with the `master` role.

###### 006 VCPUs Amount - Workers

*Task*: `hardware.cpu.workers`

This test checks the number of processors on the nodes with the `worker` role.

##### 007 RAM Amount

Tests of this type check the availability of the required number of RAM.

###### 007 RAM Amount - Balancers

*Task*: `hardware.ram.balancers`

This test checks the amount of RAM on nodes with the `balancer` role.

###### 007 RAM Amount - Masters

*Task*: `hardware.ram.masters`

This test checks the amount of RAM on nodes with the `master` role.

###### 007 RAM Amount - Workers

*Task*: `hardware.ram.workers`

This test checks the amount of RAM on nodes with the `worker` role.

##### 008 Distributive

*Task*: `system.distributive`

This test checks the family and release version of the operating system on the hosts.

##### 009 PodSubnet

*Task*: `network.pod_subnet_connectivity`

This test checks the connectivity between nodes inside a pod's subnetwork.

##### 010 ServiceSubnet

*Task*: `network.service_subnet_connectivity`

This test checks the connectivity between nodes inside the service's subnetwork.

##### 011 TCPPorts

*Task*: `network.check_tcp_ports`

This test checks if necessary ports are opened on the nodes.

#### PAAS Procedure

The PAAS procedure verifies the platform solution. For example, it checks the health of a cluster or service statuses on nodes. This test checks the already configured environment. All services and the Kubernetes cluster must be installed and should be in working condition. Apart from the environment installed and configured by Kubetools, the test can check other environments too.

The task tree is as follows:

* services
  * haproxy
    * status
  * keepalived
    * status
  * container_runtime
    * status
  * kubelet
    * status
* kubernetes
  * version
  * nodes
    * existence
    * roles
    * condition
      * network
      * memory
      * disk
      * pid
      * ready

##### 201 Service Status

Tests of this type verify the correctness of service statuses.

###### 201 Haproxy Status

*Task*: `services.haproxy.status`

This test checks the status of the Haproxy service on all hosts in the cluster where this service is expected.

###### 201 Keepalived Status

*Task*: `services.keepalived.status`

This test checks the status of the Keepalived service on all hosts in the cluster where this service is expected.

###### 201 Container Runtime Status

*Task*: `services.container_runtime.status`

This test checks the status of the Container Runtime (docker/containerd) service on all hosts in the cluster where this service is expected.

###### 201 Kubelet Status

*Task*: `services.kubelet.status`

This test checks the status of the Kubelet service on all hosts in the cluster where this service is expected.

##### 202 Nodes pid_max

*Task*: `services.kubelet.configuration`

This test checks that kubelet `maxPods` and `podPidsLimit` are correctly alligned with kernel `pid_max`.

##### 203 Kubelet Version

*Task*: `services.kubelet.version`

This test checks the Kubelet version on all hosts in a cluster.

##### 204 Recommended Packages Version

*Task*: `packages.system.recommened_versions`

This test checks that system package versions in the inventory are recommended.

##### 205 CRI Versions

*Task*: `packages.system.cri_version`

This test checks that the configured CRI package is installed on all nodes and has an equal version.

##### 205 HAproxy Version

*Task*: `packages.system.haproxy`

This test checks that the configured HAproxy package is installed on all nodes and has an equal version.

##### 205 Keepalived Version

*Task*: `packages.system.keepalived`

This test checks that the configured Keepalived package is installed on all nodes and has an equal version.

##### 206 Generic Packages Version

*Task*: `packages.generic.versions`

This test checks that the configured generic packages are installed on all nodes and have equal versions.

##### 212 Thirdparties hashes

*Task*: `thirdparties.hashes`

This test checks that configured thirdparties hashes are equal to actual files hashes on nodes.

##### 207 Pods Condition

*Task*: `kubernetes.pods`

This test checks that system pods are in good condition.

##### 208 Dashboard Availability

*Task*: `kubernetes.plugins.dashboard`

This test checks that the dashboard is available by its URL.

##### 209 Nodes Existence

*Task*: `kubernetes.nodes.existence`

This test checks for the presence of nodes in the Kubernetes cluster.

##### 210 Nodes Roles

*Task*: `kubernetes.nodes.roles`

This test checks the nodes' roles in the Kubernetes cluster.

##### 211 Nodes Condition

Tests of this type check the condition of the nodes that the Kubernetes reports.

###### 211 Nodes Condition - NetworkUnavailable

*Task*: `kubernetes.nodes.condition.network`

This test checks the condition `NetworkUnavailable` of the Kubernetes nodes of the cluster.

###### 211 Nodes Condition - MemoryPressure

*Task*: `kubernetes.nodes.condition.memory`

This test checks the condition `MemoryPressure` of the Kubernetes nodes of the cluster.

###### 211 Nodes Condition - DiskPressure

*Task*: `kubernetes.nodes.condition.disk`

This test checks the condition `DiskPressure` of the Kubernetes nodes of the cluster.

###### 211 Nodes Condition - PIDPressure

*Task*: `kubernetes.nodes.condition.pid`

This test checks the condition `PIDPressure` of the Kubernetes nodes of the cluster.

###### 211 Nodes Condition - Ready

*Task*: `kubernetes.nodes.condition.ready

This test checks the condition `Ready` of the Kubernetes nodes of the cluster.

### Report File Generation

In addition to the resulting table in the log output, the same report is presented in the form of files.

#### HTML Report

The report allows you to visually see the final report. All content, including styles, is already included inside a single file. You can use the following supported command line arguments:

|Argument|Default|Description|
|---|---|---|
|**--html-report**|`report.html`|The full absolute path to the file location where the report is saved.|
|**--disable-html-report**| |If specified, the report generation is disabled.|

Report file example (trimmed):

```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>PAAS Check Report</title>
	</head>
	<body>
		<div id="date">2020-04-29 10:09:31.096773</div>
		<div id="stats">
			<div class="succeeded">12 succeeded</div>
		</div>
		<h1>PAAS Check Report</h1>
		<table>
			<thead>
				<tr>
					<td>Group</td>
					<td>Status</td>
					<td>ID</td>
					<td>Test</td>
					<td>Actual Result</td>
					<td>Minimal</td>
					<td>Recommended</td>
				</tr>
			</thead>
			<tbody>
				<tr class="ok">
					<td>services</td>
					<td>
						<div>ok</div>
					</td>
					<td>201</td>
					<td>Haproxy Status</td>
					<td>active (running)</td>
					<td></td>
					<td></td>
				</tr>
				<tr class="ok">
					<td>services</td>
					<td>
						<div>ok</div>
					</td>
					<td>201</td>
					<td>Keepalived Status</td>
					<td>active (running)</td>
					<td></td>
					<td></td>
				</tr>
				<tr class="ok">
					<td>services</td>
					<td>
						<div>ok</div>
					</td>
					<td>201</td>
					<td>Docker Status</td>
					<td>active (running)</td>
					<td></td>
					<td></td>
				</tr>
			</tbody>
		</table>
	</body>
</html>
```

#### CSV Report

This report allows a thirdparty software to parse the report result. This is convenient when working with Excel or automatic metrics collection systems. You can use the following supported command line arguments:

|Argument|Default|Description|
|---|---|---|
|**--csv-report**|`report.csv`|The full absolute path to the file location where the report is saved.|
|**--csv-report-delimiter**|`;`|The character used as a column separator.|
|**--disable-csv-report**| |If specified, the report generation is disabled.|

Report file example:

```csv
group;status;test_id;test_name;current_result;minimal_result;recommended_result
services;ok;201;Haproxy Status;active (running);;
services;ok;201;Keepalived Status;active (running);;
services;ok;201;Docker Status;active (running);;
services;ok;201;Kubelet Status;active (running);;
kubernetes;ok;202;Kubelet Version;v1.16.3;;
kubernetes;ok;203;Nodes Existence;All nodes presented;;
kubernetes;ok;204;Nodes Roles;All nodes have the correct roles;;
kubernetes;ok;205;Nodes Condition - NetworkUnavailable;CalicoIsUp;;
kubernetes;ok;205;Nodes Condition - MemoryPressure;KubeletHasSufficientMemory;;
kubernetes;ok;205;Nodes Condition - DiskPressure;KubeletHasNoDiskPressure;;
kubernetes;ok;205;Nodes Condition - PIDPressure;KubeletHasSufficientPID;;
kubernetes;ok;205;Nodes Condition - Ready;KubeletReady;;
```