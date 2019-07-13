# EDDN Spark Compose
This is a local Apache Spark cluster with Apache Cassandra database, which can be built quickly and easily using Docker Compose. The focus is on the integration of Elite Dangerous (EDDN) data, which is loaded directly into Cassandra. This makes it possible to run Pyspark tests and analyses with Spark directly after initialization.

# Table of Content
[Installation](#Installation)
- [Python 3](#Python%203)
- [Docker](#Docker)
- [Docker Compose](#Docker%20Compose)

[Usage](#Usage)
- [Project sections](#Project%20sections)
  1. [Load Data from eddb<span></span>.io](#Load%20Data%20from%20eddb<span></span>.io)
  2. [Run Docker-Compose file](#Run%20Docker-Compose%20file)
  3. [Copy Data to Cassandra](#Copy%20Data%20to%20Cassandra)
  4. [Run pyspark skripts](#Run%20pyspark%20skripts)
- [Run all in one](#Run%20all%20in%20one)
- [Remove and cleane](#Remove%20and%20clean)

 # Installation
To use the cluster, the installation of

1. Python 3
2. Docker
3. Docker Compose 

is required. <br>
Docker is needed for the individual components, each of them running in its own container. Docker Compose starts all containers together. And Python 3 is used to load the Elite Dangerous data.

## Python 3
It is recomanded to install the latest version of python 3.

### Linux
Before installing the latest version, check if currently a python 3 installed version on your machine. <br>
To check this, run:

```sh
$ python3 --version
```
Is a version of python 3 installed you can upgrade this to latest version:
```sh
$ sudo apt-get upgrade python3 
```

If you want to install the latest version of python3 you can run: 
```sh
$ sudo apt-get install python3 
```

After the installation you need to check if `pip` (python package manager) is installed along with your python installation:
```sh
$ pip3 -V 
```
If `pip` isn't installed on your machine, run the following command to install it: 
```sh
$ sudo apt install python3-pip
```

### Windows
Download the excecutable installer from https://www.python.org/downloads/windows/ .<br>
After that execute the installer and following the instruction.<br>
Also it possible to install python with Anaconda or with configuration in power shell.

### MacOS

Before installing python make sure that xcode and homebrew are installed on your computer.

Isn't that so, then run this in terminal to install xcode:
```sh
$ xcode-select –install 
```
and this to install Homebrew:
```sh
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" 
```

Now check if a python version is already installed:
```sh
$ python3 --version 
```

Is a version installed you can upgrade this to latest version:
```sh
$ brew update 
```
```sh
$ brew upgrade python3 
```

To install python 3 run this command in your terminal:
```sh
$ brew install python3 
```

After the installation you need to check if `pip` (python package manager) is installed along with your python installation:
```sh
$ pip3 -V 
```

If `pip` isn't installed on your machine, run the following command to install it: 
```sh
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
```
```sh
$ python3 get-pip.py
```

## Docker
### Linux
#### Uninstall the old version
Make sure that no outdated Docker version is installed:
```sh
$ sudo apt-get remove docker docker-engine docker.io containerd runc 
```

#### Then install the current version of Docker
Update the apt package index:
```sh
$ sudo apt-get update 
```

Install the latest version of Docker:
```sh
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### Microsoft Windows 

If you haven’t already downloaded the installer (Docker Desktop Installer.exe), you can get it from download.docker.com.<br>
1. Double-click Docker Desktop for Windows Installer.exe to run the installer. 

2. Follow the install wizard to accept the license, authorize the installer, and proceed with the install. 

3. Click Finish on the setup dialog to complete and launch Docker.


### MacOS 

To install Docker Desktop for Mac download the Docker.dmg from [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-mac).<br>
*It is required to sign up on docker hub to download docker for mac.*

1. Double-click Docker.dmg to open the installer, then drag Moby the whale to the Applications folder.

2. Double-click Docker.app in the Applications folder to start Docker.


## Docker Compose
### Linux

To install docker compose with curl, run this command to download the current stable release of Docker Compose:
```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose 
```

Apply executable permissions to the binary: 
```sh
sudo chmod +x /usr/local/bin/docker-compose 
```

Alternativly you can use pip to install docker compose: 
```sh
sudo pip install docker-compose 
```

Test if the installation was successful: 
```sh
$ docker-compose –version 
```
 
### Windows and MacOS 

The desktop version of docker include docker compose.<br> 
So the installation is already done.

# Usage
The execution is devided in single shell scripts. The functionality and benefits are explained in the chapter project section. There is also a shell script which executes all steps together in the correct order. The project is designed for Linux systems, but can be ported with adaptations of the shell scripts for the respective operating system.

## Project Section 

Following all steps are described that you need to run in the chapter order to make the project/cluster works.

### Load Data from eddb<span></span>.io