# WAVE - Multiple load generator for computer network experimentation

Experimentation is fundamental in computer networks research, especially for validating hypotheses in controlled scenarios. In this context, this work presents a new version of WAVE (Workload Assay for Verified Experiments) integrated with Mininet, a widely used network emulator. This integration allows researchers to have greater control over the network environment where the generated traffic will be evaluated, enabling the configuration of network characteristics such as delay and packet loss. Currently, WAVE supports the linear and tree topologies, which are configured through user-defined parameters, allowing greater flexibility in the creation of experimental scenarios.

## README Structure

- **Seals Considered**: describes the artifact evaluation criteria.
- **Project Information**: provides useful resources such as documentation, previous work, and demonstration videos.
- **Basic Information**: outlines hardware and operating system requirements.
- **Dependencies**: lists required tools and their expected versions.
- **Security Concerns**: highlights potential risks and safe execution practices.
- **Checking the Required Requirements**: explains how to install dependencies, including the automated installation script (`install.sh`) and manual fallback steps.
- **Running**: describes how to start the WAVE environment.
- **Troubleshooting**: provides guidance for common issues and links to the troubleshooting guide.
- **Minimum Test**: presents a validation procedure to confirm the correct setup of the environment.
- **Ending the WAVE Execution**: explains how to properly stop and clean up the environment.
- **Experiments**: details how to reproduce experiments presented in the paper.
- **LICENSE**: provides licensing information.

## Seals Considered

The seals considered for this artifact are:

- **Available**
- **Functional**
- **Reproducible**

## Project information

This section provides useful resources related to the WAVE tool, including documentation, previous publications, and demonstration videos.

[WAVE User Manual](WAVE_User_Manual.pdf)

[Salão de Ferramentas SBRC 2025 (previous work)](https://doi.org/10.5753/sbrc_estendido.2025.6301)

[Demonstrative videos of the WAVE tool](https://drive.google.com/drive/folders/1E3_Gj1HX8jhLEx9tRARIDYxlm8bzkNN3?usp=drive_link)
> [!NOTE]
> The video **demo01-wave** demonstrates how to download, run, and validate the tool.
> The video **demo02-wave-delay** shows an experiment where delay is injected into the network.
> The video **demo03-wave-linkdown** presents a scenario in which a network link is disabled to observe traffic interruption at the server interface, followed by re-enabling the link to restore connectivity.

## Basic information

- CPU: 4 cores or higher
- Memory: at least 8 GB RAM
- Storage: at least 10 GB of free space

### Operating System

WAVE has been tested on Linux-based systems, especially:

- Ubuntu 22.04 or higher

### Environment Overview

WAVE integrates multiple technologies for network experimentation:

- Docker containers for service orchestration
- Mininet for network emulation
- Grafana for metrics visualization
- Vagrant and VirtualBox for optional virtual machine provisioning

## Dependencies

To run WAVE, the following dependencies are required:

- **Python 3** (version 3.10 or higher)
- **Virtualenv** (version 3.10 or higher)
- **Docker** (version 27.x or higher)
- **Docker Compose** (version 2.32.x or higher)
- **Mininet** (installation via the official website is recommended)
- **VirtualBox** (version 7.1.6 or higher)
- **Vagrant** (version 2.3.4 or higher)

## Security concerns

WAVE uses technologies that may impact the host system, such as Docker and Mininet.

- Mininet may modify system network configurations.
- Docker may run with elevated privileges depending on the configuration.

### Recommendations

- Avoid running in production environments
- Ensure the user has appropriate permissions
- Monitor CPU and memory usage during experiments

No critical risks were identified, provided that the best practices above are followed.

## Checking the Required Requirements

To simplify the setup process and improve reproducibility, we provide an automated installation script that installs and configures all required dependencies. If the script fails for any reason, you can follow the manual step-by-step installation described in this README.

If you're going to use the dependency installation script, you need to do a git clone of the repository first.

```
git clone https://github.com/1valcl3b/last_wave.git
```

> [!NOTE]
> Ensure you are in the correct directory before executing the commands below. The commands assume that you are inside the project path `last_wave/wave/`, where the `install.sh` script is located. This script requires sudo privileges. You may be prompted for your password during execution.

```
chmod +x install.sh
./install.sh
```

### If the script fails, or if you prefer to perform the installation manually, follow the steps below:

#### Checking if Python3 is installed and it's version:

<!-- ![wave-version-python3](./screenshots/wave-version-python32.png) -->

```
python3 --version
```
If it is not installed:

```
sudo apt update && sudo apt install python3
```

#### Additionally, the VirtualEnv virtual environment is required:

<!-- ![wave-version-venv](./screenshots/wave-version-venv2.png) -->

```
sudo apt list | grep python3-venv
```
If it is not installed:

```
sudo apt update && sudo apt install python3-venv
```

#### Checking the Docker and docker compose components:

<!-- ![wave-version-docker](./screenshots/wave-version-docker2.png)

![wave-version-docker-compose](./screenshots/wave-version-docker-compose2.png)] -->


```
docker --version
docker compose version
```
If it is not installed:

Install curl if you don't already have it.

```
sudo apt install -y curl
```

```
curl -fsSL https://get.docker.com -o get-docker.sh
chmod +x get-docker.sh 
sudo sh ./get-docker.sh
```
After installation, you may need to configure permissions and add your user to the docker group.

#### Checking what version of Virtualbox is installed:

<!-- ![wave-version-virtualbox](./screenshots/wave-version-virtualbox2.png) -->

```
vboxmanage --version
```

If it is not installed:

```
sudo apt install virtualbox
```
If VirtualBox is not available in the repository, install it from the [official website](https://www.virtualbox.org/wiki/Linux_Downloads).

#### Checking what version of Vagrant is installed:

<!-- ![wave-version-vagrant](./screenshots/wave-version-vagrant2.png) -->

```
vagrant --version
```

If it is not installed:

Manual installation of Vagrant from the [official website](https://developer.hashicorp.com/vagrant/install#linux).
```
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vagrant

```

#### Checking what version of Mininet is installed

<!-- ![wave-version-mininet](./screenshots/wave-version-mininet.png) -->

```
mn --version
```

If it is not installed:

```
sudo apt update && sudo apt install mininet
```

We recommend installing Mininet from the official website, as it provides the most up-to-date version:  
https://mininet.org/download/

Although Mininet can also be installed using `apt install mininet`, the version available in the distribution repositories may not be the most recent one.


The versions shown in the figures were those tested at the time of this manual's creation.

## Running

### Cloning the official repository and starting the system:

```
git clone https://github.com/1valcl3b/last_wave.git
```
```
cd last_wave/wave
```
```
./app-compose.sh --start
```

### Checking the execution in a Docker environment:

![wave-cli-docker](./screenshots/wave3-cli-docker.png)

As can be seen in the figure above, the WAVE Initialization module uses two containers for its execution: wave_app, grafana and node-exporter. On the left side of the figure, we have the output of the WAVE startup command.

### The WAVE WEB module can be accessed via a browser. We recommend using Google Chrome or another Chromium-based browser for better compatibility.

![wave-web-home](./screenshots/wave-configurator-2026.png)

The form contains fields for entering network data for both the traffic load source and destination. In addition to specifying the IP address, the user can choose how the environment will be provisioned, either through a container or a virtual machine, with configurable memory size and number of virtual CPUs. It is also possible to configure the network topology through user-defined parameters. Currently, the WAVE supports linear and tree topologies. Finally, the user can select which workload model to apply, such as sinusoid, flashcrowd, or step, and optionally enable the use of micro-burst traffic.

## Troubleshooting

During installation and execution, issues may arise depending on the host environment, system configuration, or network setup.

A curated list of common problems and their respective solutions is available in:

[Troubleshooting Guide](./docs/troubleshooting.md)

This document includes real issues observed during testing, including known environment-specific problems such as Docker port binding restrictions (`net.ipv4.ip_unprivileged_port_start=80`), among others.

> [!IMPORTANT]
> The number of possible environment-specific issues is large. The troubleshooting guide contains known and reproducible cases, but it is not exhaustive.

> [!NOTE]
> If you encounter an issue not documented in the troubleshooting guide, please contact the authors.  
> New issues and their respective solutions will be analyzed and added to improve reproducibility.

## Minimum Test

This test aims to validate whether the environment has been correctly configured.

### Procedure

1. Clone the repository:

```
git clone https://github.com/1valcl3b/last_wave.git
cd last_wave/wave
```

2. Start the environment:

```
./app-compose.sh --start
```

3. Verify that the containers are running:

```
docker ps
```

It is expected that the containers `wave_app`, `node-exporter`, and `grafana` are active.

4. Access the web interface in the browser (use Chrome or Brave):

> [!NOTE]
> If running on a remote server, replace `localhost` with the machine's IP address.
```
http://localhost
```
> [!NOTE]
> Ensure that the required ports (e.g., 80) are open and accessible in your environment (firewall, cloud security groups, or VM networking).

5. Configure a simple experiment:

- Platform: VM
- Topology: Linear
- Number of switches: 5
- Workload model: stair step

6. Execute the experiment. 

7. Return to the terminal to enter the root password (Mininet requires root privileges; you can configure the visudo file to avoid password prompts)

8. After entering the password, you may return to the web interface

If this is your first execution, the process may take longer because the Vagrant boxes (client and server) need to be downloaded. The total time will depend on your internet connection.

### Expected result

- The environment will be provisioned (this may take some time)
- The results web interface should appear, Metrics should be visualized through charts

![wave-web-grafana](./screenshots/wave-web-grafana2026.png)

If you prefer a visual walkthrough of this process, you can watch the following [video](https://drive.google.com/file/d/1zQZR1eSVeXidqYWtyl0KJyLb4BZZFsvv/view), It demonstrates the complete workflow, from cloning the repository to executing the tool and visualizing the results.

## Ending the WAVE Execution

Finalizing and removing the container environment:

```
./app-compose.sh --destroy
```

By running the command above, the user terminates the WAVE WEB module and removes the containers responsible for the other initiated modules. To restart the entire system, simply execute the same command, replacing the --destroy argument with --start.

## Experiments

This section describes how to reproduce one of the main claims presented in the paper: **WAVE can dynamically configure Mininet network parameters and demonstrate their impact on network traffic behavior.**

The experiment reproduces the delay analysis scenario presented in the **“Impact of Mininet Parameters”** section of the paper, where different delay values are injected into the network topology to evaluate their impact on network throughput.

### Experiment Configuration

Make sure all dependencies have been installed.

1. Clone the repository:

```
git clone https://github.com/1valcl3b/last_wave.git
cd last_wave/wave
```

2. Start the WAVE environment:

```bash
./app-compose.sh --start
```

3. Access the Web interface (use chrome or brave):

> [!NOTE]
> If running on a remote server, replace `localhost` with the machine's IP address.
```
http://localhost
```
4. Use the following base configuration:

- Platform: Docker
- Topology: Linear, Number of switches: 5
- Workload model: Stair Step, Interval: 5, Jump: 10, Duration: 10

### Important Note on Metrics

In the original paper, the evaluation considers metrics such as:

- Throughput
- Round-Trip Time (RTT)

WAVE, by design, does not natively compute or expose these metrics directly in its interface. Instead, it relies on an observability stack composed of:

- Prometheus (metrics collection)
- Grafana (visualization)

This architecture allows users to extract and analyze network behavior in a flexible way.

---

#### Reproducing Paper Results

The results presented in the paper were obtained by collecting metrics from Prometheus during the experiments and plotting the corresponding graphs externally.

These graphs include:

- RTT comparison between scenarios with injected delay and without
delay
- Throughput comparison between scenarios with packet loss and without loss.
  
Although WAVE does not natively generate these specific plots, the integration with Prometheus and Grafana enables straightforward extraction of the required data, allowing full reproduction of the figures shown in the paper.

---

### Experiment Execution

Now you will configure scenarios with different delay values. For each scenario, a new environment must be configured, changing only the delay parameter while keeping the remaining settings the same. There is no need to repeat the installation or startup steps, since the Analysis Result screen includes a `Destroy` button that terminates the current environment and returns you to the home page.

### Scenario 1: Baseline

Configure:

- Delay: 0 ms

![wave-exper-input-delay](./screenshots/wave-baseline1.png)

Execute the experiment.

Expected result:

![wave-exper-input-delay](./screenshots/wave-baseline2.png)

- The environment should be provisioned successfully
- The Analysis Result screen should be displayed
- A higher Mbps rate should be observed arriving at the server interface

Expected execution time:

- Approximately 3–5 minutes

### Scenario 2: Delay Injection (10 ms)

Configure:

- Delay: 10 ms
  
![wave-exper-input-delay](./screenshots/wave-delay10ms.png)

Execute the experiment.

Expected result:

![wave-exper-input-delay](./screenshots/wave-delay10ms-res.png)

- The Analysis Result screen should be displayed
- Traffic should continue reaching the server interface
- The observed Mbps rate should be lower than the baseline scenario

Expected execution time:

- Approximately 3–5 minutes

### Scenario 3: Delay Injection (50 ms)

Configure:

- Delay: 50 ms
  
![wave-exper-input-delay](./screenshots/wave-delay50ms.png)

Execute the experiment.

Expected result:

![wave-exper-input-delay](./screenshots/wave-delay50ms-res.png)

- The Analysis Result screen should be displayed
- Traffic should continue reaching the server interface
- The observed Mbps rate should be lower than the 10 ms scenario

Expected execution time:

- Approximately 3–5 minutes

## Expected Result

In all scenarios, the **Analysis Results** screen should display:

- Traffic arriving at the server network interface
- CPU usage
- Memory usage
  
The expected behavior is that, as the configured delay increases, the amount of Mbps reaching the server interface decreases proportionally. This behavior is consistent with the results presented in the paper and demonstrates that WAVE correctly applies Mininet delay parameters in a reproducible experimental environment. Additionally, by leveraging Prometheus and Grafana, users can further analyze:

- Throughput variations over time
- Latency-related effects
- Resource utilization under different network conditions

This enables a more detailed evaluation aligned with the metrics discussed in the paper.

## LICENSE

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the LICENSE file for more details.
